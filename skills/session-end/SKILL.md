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
