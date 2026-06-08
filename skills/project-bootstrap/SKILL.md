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
