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
