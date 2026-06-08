# Agents Guide

## What are agents?

Agents are specialized Claude Code sub-sessions with a fixed tool set, model, and behaviour rules. They live in `~/.claude/agents/` after install. When Claude Code spawns one, it gets a fresh context window with only the tools and instructions defined in its agent file — so it cannot go off-script.

This kit installs 9 agents. Each has a specific role; using the right one keeps costs down and quality up.

---

## How agents are invoked

There are three ways an agent runs:

### 1. Automatically (hook or skill)

Some agents fire without you doing anything:

| Trigger | Agent(s) invoked |
|---|---|
| `/new-feature` skill | `chinnu-architect` (if architectural scope) → `chinnu-planner` |
| `/security-review` skill | `chinnu-security-auditor` |
| `/ship-feature` skill | `chinnu-code-reviewer` |
| `/parallel-review` skill | `chinnu-code-reviewer` + test-runner (Bash) + `chinnu-build-error-resolver` simultaneously |

### 2. Explicitly by name

Tell Claude to use an agent by mentioning it:

```
Use the chinnu-debugger agent to find why the payment webhook fails.
Use the chinnu-e2e-runner agent to write tests for the login flow.
Use the chinnu-planner agent before we start this feature.
```

Claude Code routes the task to that agent's isolated context.

### 3. Via Claude Code's `--agent` flag (CLI)

```bash
claude --agent chinnu-security-auditor "audit the auth module"
```

---

## Agent reference

### `chinnu-planner`
**Model:** Opus &nbsp;|&nbsp; **Tools:** Read, Glob, Grep &nbsp;|&nbsp; **Max turns:** 30

Designs features and produces a PRD + discrete issue list before any code is written. Use before anything that touches 3+ files or needs architectural decisions. The `/new-feature` skill invokes it automatically.

**When to use explicitly:**
```
Use the chinnu-planner agent — I want to add multi-tenant support to the billing module.
```

---

### `chinnu-architect`
**Model:** Opus &nbsp;|&nbsp; **Tools:** Read, Glob, Grep &nbsp;|&nbsp; **Max turns:** 25

System design, DB schema choices, new service boundaries, tech selection. Runs ADR (Architecture Decision Record) output via `adr-kit` and STRIDE threat modelling when security scope is detected. Invoked automatically by `/new-feature` when the planner output has architectural scope.

**When to use explicitly:**
```
Use the chinnu-architect agent — should we use Postgres JSONB or a separate table for user preferences?
```

---

### `chinnu-implementer`
**Model:** Sonnet &nbsp;|&nbsp; **Tools:** Read, Write, Edit, Bash, Glob, Grep &nbsp;|&nbsp; **Max turns:** 40

Implements features from an approved issues file. Enforces TDD (red → green → refactor), 80%+ coverage, and a 1–3 file scope gate. For larger tasks use `chinnu-implementer-large`.

**Requires:** an issues file (output of the `chinnu-planner` agent's `/to-issues` skill).

**When to use explicitly:**
```
Use the chinnu-implementer agent to implement the issues in issues.md.
```

---

### `chinnu-implementer-large`
**Model:** Sonnet &nbsp;|&nbsp; **Tools:** Read, Write, Edit, Bash, Glob, Grep &nbsp;|&nbsp; **Max turns:** 80

Same as `chinnu-implementer` but for features spanning 4+ files. Uses git worktrees for isolation and dispatches sub-agents per task to prevent context rot. Only reach for this when the task is genuinely large.

**When to use explicitly:**
```
Use the chinnu-implementer-large agent — this refactor touches 8 files across 3 modules.
```

---

### `chinnu-code-reviewer`
**Model:** Sonnet &nbsp;|&nbsp; **Tools:** Read, Glob, Grep &nbsp;|&nbsp; **Max turns:** 15

Two-layer review:
- **Layer 1** (automatic, lightweight): fires on every Write/Edit via hook — reviews the diff only.
- **Layer 2** (this agent): deep review after an implementer completes. Invoked by `/ship-feature` and `/parallel-review` skills.

**When to use explicitly:**
```
Use the chinnu-code-reviewer agent to review the changes in the auth module.
```

---

### `chinnu-security-auditor`
**Model:** Opus &nbsp;|&nbsp; **Tools:** Read, Glob, Grep, Bash &nbsp;|&nbsp; **Max turns:** 25

Deep security audit using Trail of Bits methodology — static analysis, insecure defaults detection, variant analysis. This is a **slow, expensive** agent. Use it for auth, payments, user data, and external API surface — not routine reviews. The `/security-review` skill invokes it.

**When to use explicitly:**
```
Use the chinnu-security-auditor agent on the OAuth callback handler.
```

---

### `chinnu-debugger`
**Model:** Sonnet &nbsp;|&nbsp; **Tools:** Read, Bash, Glob, Grep &nbsp;|&nbsp; **Max turns:** 25

Systematic root-cause debugging. Requires full reproduction before proposing any fix — it finds root causes, not symptoms. For build/type errors use `chinnu-build-error-resolver` instead (it's faster and cheaper).

**When to use explicitly:**
```
Use the chinnu-debugger agent — the webhook is silently dropping events in production but not staging.
```

---

### `chinnu-build-error-resolver`
**Model:** Haiku (fast/cheap) &nbsp;|&nbsp; **Tools:** Read, Bash, Glob, Grep, Edit &nbsp;|&nbsp; **Max turns:** 20

Fixes build failures, type errors, and compilation errors. Also used as a read-only build-check inside `/parallel-review`. Has a 5% file-change limit — if the fix is larger than that, it stops and reports rather than making sweeping changes.

**When to use explicitly:**
```
Use the chinnu-build-error-resolver agent — the TypeScript build is failing.
```

---

### `chinnu-e2e-runner`
**Model:** Sonnet &nbsp;|&nbsp; **Tools:** Read, Bash, Glob, Grep, Write, Edit &nbsp;|&nbsp; **Max turns:** 25

Writes and runs Playwright end-to-end tests for critical user flows. Uses Page Object Model structure, handles CI/CD integration, and manages flaky test quarantine.

**When to use explicitly:**
```
Use the chinnu-e2e-runner agent to write tests for the checkout flow.
chinnu-e2e-runner test the login and signup journeys.
```

---

## Typical workflow

```
You:    /new-feature "add Stripe subscription billing"
        → chinnu-architect runs (DB schema + auth scope detected)
        → chinnu-planner writes PRD + issues file

You:    Use the chinnu-implementer agent to implement issue 1 from the issues file.
        → chinnu-implementer writes code with TDD (red → green → refactor)

You:    /parallel-review
        → chinnu-code-reviewer + test-runner + chinnu-build-error-resolver run simultaneously

You:    Use the chinnu-security-auditor agent on the billing module before we ship.

You:    Use the chinnu-e2e-runner agent to add E2E tests for the subscription flow.

You:    /ship-feature
        → chinnu-code-reviewer does final deep review → PR opened
```

---

## Where the files live after install

```
~/.claude/agents/
  chinnu-planner.md
  chinnu-architect.md
  chinnu-implementer.md
  chinnu-implementer-large.md
  chinnu-code-reviewer.md
  chinnu-security-auditor.md
  chinnu-debugger.md
  chinnu-build-error-resolver.md
  chinnu-e2e-runner.md
```

You can customise any agent by editing its file directly. The installer will prompt before overwriting a customised file on next update.
