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
