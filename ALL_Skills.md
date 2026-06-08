## HOW TO INSTALL THESE SKILLS
## Save each block as: ~/.claude/skills/{skill-name}/SKILL.md
## After saving: restart Claude Code or wait for live reload


# ════════════════════════════════════════════════════════
# SKILL 1: new-feature
# Path: ~/.claude/skills/new-feature/SKILL.md
# Invoke: /new-feature
# ════════════════════════════════════════════════════════

---
name: new-feature
description: >
  Start a new feature from scratch. Checks whether an architectural
  decision is needed first, then routes to planner automatically.
  The single entry point for starting any non-trivial new work.
  Arguments: brief feature description (optional — will ask if missing)
user-invocable: true
argument-hint: "[brief feature description]"
allowed-tools: Read, Bash
---

# New Feature

Route a new feature request to the right starting agent automatically.

## Step 1 — Get feature description

If argument provided: use it.
If no argument: ask once — "What are we building?"

## Step 2 — Assess: does this need an architect first?

Ask yourself (silently — don't explain to user):
- Does this touch the database schema?
- Does this add a new service or major module?
- Does this change how authentication or authorization works?
- Does this affect more than 5 files across more than 2 layers?
- Is there a meaningful technical decision to be made before building?

If ANY answer is yes → architect first.
If ALL answers are no → planner directly.

## Step 3a — Architect first (if needed)

Tell the user:
```
This feature involves architectural decisions. Starting with the chinnu-architect agent.
Read docs/adr/ and docs/ai/ARCHITECTURE.md first, then we'll plan.
```

Invoke chinnu-architect agent:
"We want to build: {feature description}.
Read docs/ai/ARCHITECTURE.md and all ADRs in docs/adr/ before reasoning.
Identify any architectural decisions that need to be made before planning begins.
If decisions are needed: produce an ADR. If not: say 'No architectural decisions needed — proceed to planning.'"

After architect completes → proceed to Step 3b.

## Step 3b — Planner

Invoke chinnu-planner agent:
"Plan the following feature: {feature description}.
{If ADR was produced: Read docs/adr/{latest-adr} before planning.}
Run grill-me first, then produce a PRD and issues file."

## Step 4 — Confirm and hand off

After planner completes:
```
Planning complete.
  PRD:    docs/ai/specs/{date}-{feature}-prd.md
  Issues: docs/ai/specs/{date}-{feature}-issues.md

Review both files, then run:
  /implement [issue number] to start implementing
```


# ════════════════════════════════════════════════════════
# SKILL 2: parallel-review
# Path: ~/.claude/skills/parallel-review/SKILL.md
# Invoke: /parallel-review
# ════════════════════════════════════════════════════════

---
name: parallel-review
description: >
  Dispatch code-reviewer, test-runner, and docs-checker simultaneously
  on the current session's changes. More thorough than single-agent review.
  Use after a significant block of implementation work.
user-invocable: true
allowed-tools: Read, Bash
---

# Parallel Review

Dispatch three review tasks simultaneously against the current branch diff.

## Step 1 — Get changed files

```bash
git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD~1
```

## Step 2 — Dispatch simultaneously

Issue all three tasks in one message to run in parallel:

"Do all three simultaneously:

1. [chinnu-code-reviewer]: Review the diff on the current branch against main.
   Check: code quality, spec compliance, naming, error handling.
   Output: numbered findings by severity.

2. [test-runner (using Bash tool)]: Run the full test suite and coverage report.
   Show: pass/fail counts, coverage %, any failing test names.

3. [build-error-resolver (read-only check)]: Check that the build passes cleanly.
   Run: the project's build command (npm run build / go build / python -m py_compile).
   Output: PASS or list of errors."

## Step 3 — Consolidate results

After all three complete, print a combined summary:
```
Parallel Review Results
──────────────────────
Code Review:  {n findings: X HIGH, Y MED, Z LOW}
Tests:        {PASSING / FAILING — n failures} | Coverage: {n}%
Build:        {PASS / FAIL}

Verdict: {READY TO SHIP / FIXES NEEDED}
```

If any BLOCK_MERGE findings or failing tests: list what must be fixed first.


# ════════════════════════════════════════════════════════
# SKILL 3: project-bootstrap
# Path: ~/.claude/skills/project-bootstrap/SKILL.md
# Invoke: /project-bootstrap
# ════════════════════════════════════════════════════════

---
name: project-bootstrap
description: >
  Scaffold the docs/ai/ context layer for a project. Detects whether the project
  is NEW (no codebase yet), EXISTING (existing codebase to onboard), or REFRESH
  (docs/ai/ already exists and needs updating). Run this once per project, the
  first time you open Claude Code in it. For subsequent refreshes, use /refresh-docs.
user-invocable: true
allowed-tools: Read, Write, Bash
---

# Project Bootstrap

Scaffold the docs/ai/ AI-context layer so future Claude Code sessions can load
project context cheaply.

## Step 1 — Detect mode

```bash
if [ -f docs/ai/ARCHITECTURE.md ]; then
  echo "REFRESH"
elif find . -maxdepth 3 -type d \( -name src -o -name app -o -name lib -o -name api \) 2>/dev/null | grep -q .; then
  echo "EXISTING"
else
  echo "NEW"
fi
```

Pick one of NEW / EXISTING / REFRESH.

## Step 2 — Confirm with user

```
📁 Project bootstrap — detected mode: {MODE}

Files I will create:
  docs/ai/ARCHITECTURE.md
  docs/ai/PATTERNS.md
  docs/ai/API-CONTRACTS.md
  docs/ai/SESSION-NOTES.md
  docs/adr/.gitkeep
  CONTEXT.md (bridge file at repo root)

I will NOT create or modify:
  CLAUDE.md (if exists — leave it)
  .claudeignore (if exists — leave it)

Proceed? [y/n]
```

If `n`, exit silently.

## Step 3a — NEW mode

The project has no code yet. Create skeleton docs with TODO placeholders:

- `docs/ai/ARCHITECTURE.md` — heading "Architecture" + TODO list: tech stack, layers, data flow, key invariants.
- `docs/ai/PATTERNS.md` — heading + TODO list: naming, error handling, state management.
- `docs/ai/API-CONTRACTS.md` — heading + TODO list: endpoints, request/response shapes, auth.
- `docs/ai/SESSION-NOTES.md` — empty (will be populated by /session-end).
- `docs/adr/.gitkeep` — empty marker.
- `CONTEXT.md` at repo root — single line:
  `Read docs/ai/ARCHITECTURE.md and docs/ai/PATTERNS.md before any work.`

## Step 3b — EXISTING mode

Use Repomix to scan the codebase and infer current state:

```bash
npx repomix \
  --include "src/**,app/**,lib/**,api/**,server/**,services/**,components/**,pages/**" \
  --exclude "**/*.test.*,**/*.spec.*,**/fixtures/**,**/dist/**,**/build/**,**/node_modules/**" \
  --compress \
  --output .repomix-bootstrap.xml
```

Read the output. Identify:
- Top-level module structure
- Primary languages and frameworks
- Existing patterns (naming, error handling, state management)
- API surface (endpoints, exported functions)

Generate the four `docs/ai/*.md` files from your observations.
Mark anything you're uncertain about with:
`<!-- verify: may need review -->`

`docs/adr/.gitkeep` — create empty.
`CONTEXT.md` — same single-line content as NEW mode.

Then clean up:
```bash
rm -f .repomix-bootstrap.xml
```

## Step 3c — REFRESH mode

Hand off to `/refresh-docs` skill instead — that skill is purpose-built for
re-analyzing an already-bootstrapped project. Print to user:

```
docs/ai/ already exists. For refreshing after major changes, run:
  /refresh-docs

This skill (/project-bootstrap) only initializes — it does not refresh.
```

Exit.

## Step 4 — Confirm completion

```
✅ Project bootstrap complete
   Mode: {MODE}
   Files created: {list}

   Next steps:
   1. Review docs/ai/ARCHITECTURE.md and fill in any TODOs
   2. Run /session-start to begin a work session
   3. Use /refresh-docs after major refactors
```

Do NOT invoke other skills automatically. Do NOT modify existing CLAUDE.md.


# ════════════════════════════════════════════════════════
# SKILL 4: refresh-docs
# Path: ~/.claude/skills/refresh-docs/SKILL.md
# Invoke: /refresh-docs
# ════════════════════════════════════════════════════════

---
name: refresh-docs
description: >
  Refresh docs/ai/ARCHITECTURE.md and docs/ai/PATTERNS.md after a major
  refactor, new service, or significant codebase change.
  Compares existing docs to current code, updates only what has changed.
  Does NOT touch SESSION-NOTES.md or ADRs — those are permanent records.
user-invocable: true
allowed-tools: Read, Write, Bash
---

# Refresh Docs

Update the AI context docs to reflect the current state of the codebase.
This is the REFRESH mode of project-bootstrap, run standalone.

## Step 1 — Confirm with user

```
📄 Refreshing AI context docs:
   docs/ai/ARCHITECTURE.md
   docs/ai/PATTERNS.md
   CONTEXT.md (bridge file)

   ADRs in docs/adr/ will NOT be touched.
   SESSION-NOTES.md will NOT be touched.

   This takes 2-4 minutes. Proceed? [y/n]
```

## Step 2 — Read existing docs first

Read the current contents of:
- docs/ai/ARCHITECTURE.md
- docs/ai/PATTERNS.md

Note what's there. You'll compare against what you find in the code.

## Step 3 — Analyse current codebase

```bash
npx repomix \
  --include "src/**,app/**,lib/**,api/**,server/**,services/**,components/**,pages/**" \
  --exclude "**/*.test.*,**/*.spec.*,**/fixtures/**,**/dist/**,**/build/**" \
  --compress \
  --output .repomix-refresh-tmp.xml 2>&1
```

Read the output. Compare to existing docs.

## Step 4 — Update only what has changed

For ARCHITECTURE.md: update sections where the code no longer matches.
Mark any section you are uncertain about with:
`<!-- verify: may need review -->`

Do NOT rewrite sections that are still accurate.
Do NOT delete the "What NOT to do" section — add to it, never remove.

For PATTERNS.md: update examples if patterns have changed.
Add new patterns discovered. Mark deprecated patterns as deprecated,
don't delete them (they explain why things look the way they do).

## Step 5 — Update CONTEXT.md bridge

Ensure CONTEXT.md still correctly imports docs/ai/ARCHITECTURE.md.
The content of CONTEXT.md should not change — just verify it's intact.

## Step 6 — Clean up and report

```bash
rm -f .repomix-refresh-tmp.xml
```

Report:
```
✅ Docs refreshed
   docs/ai/ARCHITECTURE.md — {n sections updated, n unchanged}
   docs/ai/PATTERNS.md     — {n sections updated, n unchanged}
   
   Sections marked for your review:
   {list any <!-- verify --> flags}
```


# ════════════════════════════════════════════════════════
# SKILL 5: security-review
# Path: ~/.claude/skills/security-review/SKILL.md
# Invoke: /security-review
# ════════════════════════════════════════════════════════

---
name: security-review
description: >
  Invoke the chinnu-security-auditor agent on auth code, payment flows,
  user data handling, or external API integrations.
  Use before merging any feature that touches sensitive code.
  Arguments: optional path or feature name to scope the review.
  Example: /security-review src/auth/ or /security-review "OAuth feature"
user-invocable: true
argument-hint: "[path or feature description]"
allowed-tools: Read, Bash, Glob, Grep
---

# Security Review

Invoke the chinnu-security-auditor agent on the specified scope.

## Step 1 — Determine scope

If the user passed an argument, use that as the scope.
If no argument, determine scope automatically:
```bash
git diff --name-only HEAD~1  # files changed in last commit
git diff --name-only         # uncommitted changed files
```

Filter to security-sensitive files:
- Auth: anything matching `*auth*`, `*login*`, `*session*`, `*token*`, `*oauth*`
- Payments: anything matching `*payment*`, `*stripe*`, `*billing*`
- User data: anything matching `*user*`, `*profile*`, `*pii*`
- APIs: anything matching `*api*`, `*webhook*`, `*external*`

## Step 2 — Report scope to user and confirm

```
🔒 Security review scope:
   {list of files or feature description}

   This will invoke the chinnu-security-auditor agent (Opus, forked context).
   Estimated time: 2-5 minutes.
   Proceed? [y/n]
```

Wait for confirmation before invoking.

## Step 3 — Invoke security-auditor

Pass the scope to the chinnu-security-auditor agent with this prompt:

"Security audit the following files/feature: {scope}

Use your loaded Trail of Bits skills:
- audit-context-building: read and understand the code first
- static-analysis: check for injection, auth bypass, data exposure  
- insecure-defaults: check for insecure configuration
- variant-analysis: if you find a vulnerability, search the whole
  codebase for the same pattern

Output findings in SARIF format:
[CWE-{id}] {SEVERITY} | {file}:{line} | {description} | {remediation}

After findings: state overall verdict — SAFE / NEEDS FIXES / CRITICAL"

## Step 4 — Surface findings to user

After the agent completes, show the verdict and findings summary.
If CRITICAL findings: recommend blocking merge.
If NEEDS FIXES: list fixes required before merge.
If SAFE: confirm the review passed.


# ════════════════════════════════════════════════════════
# SKILL 6: session-end
# Path: ~/.claude/skills/session-end/SKILL.md
# Invoke: /session-end
# ════════════════════════════════════════════════════════

---
name: session-end
description: >
  End a work session cleanly. Saves session notes to docs/ai/SESSION-NOTES.md,
  checks for uncommitted work, and prepares the handoff for next session.
  Run this before closing Claude Code or taking a long break.
user-invocable: true
allowed-tools: Read, Write, Bash
---

# Session End

Save the session state so the next session can continue without re-explaining
anything. Be concise — this file is read by future Claude sessions, not humans.

## Step 1 — Gather session facts

```bash
git diff --stat HEAD        # what changed
git log --oneline -3        # recent commits
git status --short          # uncommitted work
```

## Step 2 — Write to docs/ai/SESSION-NOTES.md

Prepend a new entry at the TOP of docs/ai/SESSION-NOTES.md
(most recent entry always first). Keep the file under 200 lines total —
if it exceeds 200 lines, trim the oldest entry.

Entry format:
```markdown
## Session: {YYYY-MM-DD HH:MM}

### What was done
- {file or feature}: {one-line description of change}
- {repeat for each significant change}

### Decisions made
- {any architectural, pattern, or tech decisions made this session}
- {include WHY if non-obvious}

### Files modified
{git diff --stat output — just the file list}

### Open problems
- {anything unresolved, with enough context to pick up cold}

### Next steps
- {exactly what the next session should do first}
- {be specific enough that a fresh Claude can start without asking}

### Gotchas learned
- {anything surprising about this codebase discovered today}

---
```

## Step 3 — Check for uncommitted work

```bash
git status --short
```

If uncommitted changes exist, warn the user:
```
⚠️  Uncommitted changes in: {file list}
    Commit or stash before closing if this work matters.
```

## Step 4 — Confirm to user

```
✅ Session saved to docs/ai/SESSION-NOTES.md
   Next session: run /session-start to pick up where we left off
```

Do NOT run /clear. The user decides when to clear.


# ════════════════════════════════════════════════════════
# SKILL 7: session-start
# Path: ~/.claude/skills/session-start/SKILL.md
# Invoke: /session-start
# ════════════════════════════════════════════════════════

---
name: session-start
description: >
  Start a new work session. Loads previous session notes, confirms
  current state, and orients you for the day's work.
  Run this at the beginning of every session before doing anything else.
user-invocable: true
allowed-tools: Read, Bash
---

# Session Start

You are orienting yourself at the start of a new session.
Do this silently and efficiently — no long preambles.

## Step 1 — Load previous session notes

Check if docs/ai/SESSION-NOTES.md exists and has content:

```bash
[ -f docs/ai/SESSION-NOTES.md ] && wc -l docs/ai/SESSION-NOTES.md
```

If it exists and has content, read the last 60 lines:
```bash
tail -60 docs/ai/SESSION-NOTES.md
```

If it doesn't exist or is empty, say:
"No previous session notes found. This appears to be a fresh start."

## Step 2 — Check git state

```bash
git status --short
git log --oneline -5
```

## Step 3 — Confirm current state to user

Print a brief orientation (max 10 lines):
```
📍 Session Start — {date}

Last session: {one line summary from SESSION-NOTES or "none"}
Branch: {current branch}
Uncommitted changes: {count or "none"}
Last 3 commits: {from git log}

Ready. What are we working on today?
```

Do NOT ask clarifying questions. Do NOT load the full codebase.
Do NOT invoke any other agents. Just orient and wait.


# ════════════════════════════════════════════════════════
# SKILL 8: ship-feature
# Path: ~/.claude/skills/ship-feature/SKILL.md
# Invoke: /ship-feature
# ════════════════════════════════════════════════════════

---
name: ship-feature
description: >
  Finish and ship a completed feature branch. Runs the full
  test suite, triggers deep code review, then presents options
  to merge, open a PR, or keep the branch.
  Run when implementation is complete and you're ready to ship.
  Arguments: optional branch name (defaults to current branch)
user-invocable: true
argument-hint: "[branch-name, defaults to current]"
allowed-tools: Read, Bash, Glob, Grep
---

# Ship Feature

Run the pre-ship checklist then hand off to finishing-a-development-branch.

## Step 1 — Confirm branch

```bash
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
```

If argument passed, checkout that branch first:
```bash
git checkout {argument}
```

## Step 2 — Run full test suite

```bash
# Detect test runner
if [ -f "package.json" ]; then
  npm test 2>&1 | tail -30
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  python -m pytest --tb=short 2>&1 | tail -30
elif [ -f "go.mod" ]; then
  go test ./... 2>&1 | tail -30
fi
```

If tests fail: STOP. Report failures. Do not proceed.
```
❌ Tests failing — cannot ship.
   Fix these before running /ship-feature again:
   {test failure summary}
```

## Step 3 — Run coverage check

```bash
# TypeScript/JS
npx jest --coverage --coverageReporters=text-summary 2>/dev/null | grep "All files"
# Python
python -m pytest --cov --cov-report=term-missing 2>/dev/null | tail -5
# Go  
go test -cover ./... 2>/dev/null | grep -E "coverage|ok"
```

If coverage below 80%: warn but don't block (blocking is implementer's job):
```
⚠️  Coverage: {n}% — below 80% target
    Consider adding tests before shipping.
    Continue anyway? [y/n]
```

## Step 4 — Run Layer 2 deep code review

Invoke the chinnu-code-reviewer agent on the full branch diff:
"Review the diff between main and {branch}. 
Check: spec compliance, code quality, security basics.
Output: numbered findings by severity. State verdict: APPROVE or REQUEST CHANGES."

If code-reviewer outputs BLOCK_MERGE: STOP and show the HIGH findings.

## Step 5 — Present ship options

```
✅ Pre-ship checklist complete
   Branch: {branch}
   Tests: PASSING
   Coverage: {n}%
   Code review: {APPROVED / n findings}

   How would you like to ship?
   [1] Merge to main now
   [2] Open a draft PR
   [3] Open a ready PR
   [4] Keep branch, ship later
   [5] Discard branch and worktree
```

Wait for user choice, then execute.

For options 1-3, run:
```bash
# Option 1: merge
git checkout main && git merge {branch} && git push

# Option 2: draft PR (requires gh CLI)
gh pr create --draft --title "{branch}" --body "Closes #{issue}"

# Option 3: ready PR
gh pr create --title "{branch}" --body "Closes #{issue}"
```

## Step 6 — Clean up worktree if used

```bash
# Check if branch has a worktree
git worktree list | grep {branch}
# If yes, remove it:
git worktree remove {worktree-path}
```

## Step 7 — Prompt session-end

```
Feature shipped ✅
Run /session-end to save session notes before closing.
```

