# Adding a Custom Skill

This guide walks through adding a new skill to the kit so it installs alongside the built-in eight.

## Step 1 — Create the skill file

Create `skills/<name>/SKILL.md` with valid YAML frontmatter:

```yaml
---
name: my-skill
description: >
  One-line description shown in /help output.
user-invocable: true
argument-hint: "[optional args]"
allowed-tools:
  - Read
  - Bash
---

## What this skill does

Write the skill body here. Use numbered `## Step N` sections,
fenced bash blocks for exact commands, and explicit "Do NOT" lines
where over-eager behaviour is a risk.
```

The `name` field must match the directory name (`skills/<name>/`).

## Step 2 — Add a reference to the HTML guide

Open `claude_code_master_guide.html` and add a row to the skills table in the `overview` section and the `skills-ref` tab:

```html
<tr>
  <td><span class="cmd">/my-skill</span></td>
  <td>One-line description</td>
  <td>What it replaces / what triggers it</td>
</tr>
```

Both the `overview` section and `skills-ref` tab have skills tables — update both.

## Step 3 — Regenerate `ALL_Skills.md`

```bash
bash scripts/build-all-skills.sh
```

This concatenates all `skills/*/SKILL.md` files into `ALL_Skills.md` with banner headers. Commit the result.

## Step 4 — Verify drift-free

```bash
bash scripts/verify-guide-sync.sh
```

The script exits 0 if every skill referenced in the HTML guide has a matching `skills/<name>/SKILL.md` and vice versa. Fix any mismatch it reports before proceeding.

## Step 5 — Test install into a temp directory

```bash
./install.sh --dry-run --target /tmp/test-install
```

Confirm the new skill appears in the dry-run output. Then do a real install:

```bash
./install.sh --target /tmp/test-install
ls /tmp/test-install/skills/my-skill/
```

## Keeping skills in sync

After adding a skill:
- The `build-all-skills.sh` script is the source of truth for `ALL_Skills.md`
- The HTML guide's skills tables must list every skill in `skills/`
- `verify-guide-sync.sh` enforces this — run it as part of any PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full test checklist.
