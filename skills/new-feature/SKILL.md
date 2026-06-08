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
