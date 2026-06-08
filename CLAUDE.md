# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal **reference / knowledge repository** about how to set up and operate Claude Code itself. It is **not** a software project — there is no package manager, build system, test suite, CI, or git history. Treat changes as content edits, not engineering tasks.

Three files make up the whole repo, and they are designed to stay in sync:

| File | Role |
|---|---|
| `claude_code_master_guide.html` | The canonical artifact — a self-contained single-page reference (~880 lines) describing the 5-tier setup, skills, agents, hooks, walkthrough, and daily workflow. |
| `ALL_Skills.md` | The source-of-truth SKILL.md blocks for the custom skills the master guide references. Each block has YAML frontmatter and is meant to be split out to `~/.claude/skills/{name}/SKILL.md` by the user. |
| `BestPractices.md` | Six-bullet executive summary of the top insights from the master guide. |

The master guide is the spec. `ALL_Skills.md` is the implementation of the slash-commands it advertises. `BestPractices.md` is the elevator pitch. When any one changes, check whether the other two need to follow.

## Working with `claude_code_master_guide.html`

A **single self-contained HTML file** — inline `<style>`, inline `<script>` at the bottom, no external assets, no build step. Preserve that pattern; do not split into separate CSS/JS files or introduce a bundler.

It is a tabbed single-page app. Each tab is a `<section id="...">`; the inline `show(id)` function toggles the `.active` class. When adding a new tab, update three places:

1. A new `<div class="nav-item" onclick="show('xxx')" id="nav-xxx">` entry in the left `<nav>`.
2. A new `<section id="xxx">` block in `<main>`.
3. Reuse the existing CSS classes — do not invent new ones unless adding a genuinely new visual primitive.

Current sections (in nav order):

- **Foundation**: `overview`, `tier1` (Minimal Setup), `tier2` (Token Efficiency), `tier3` (Workflow Skills)
- **Advanced**: `tier4` (Agent Stack), `tier5` (Memory & Indexing)
- **Reference**: `skills-ref` (Skills Quick-Ref), agent definitions, hooks-and-settings, walkthrough, daily-workflow

The content model is the "5-tier incremental setup" (Tier 1 Minimal → Tier 5 Memory/Indexing). New tools, skills, or agents should slot into the matching tier rather than spawning a new top-level concept.

### Visual conventions (load-bearing — match these when editing)

- `<div class="card [green|warn|blue|purple|red]">` — bordered callouts.
- `<div class="hl [green|warn|purple]">` — highlighted tip boxes.
- `<span class="cmd">/slash-command</span>` — slash-command pills.
- `<span class="tag tg|tb|to|tw|tr|tp">` — inline coloured tags.
- `<div class="tier">` + `<div class="tier-badge tN">` — tier rows.
- `<pre>` for copy-paste shell snippets; `<code>` for inline code.

Colours are defined once in `:root` CSS variables (`--accent`, `--blue`, `--green`, `--warn`, `--purple`, `--red`). Reuse variables; don't hardcode hex.

## Working with `ALL_Skills.md`

A concatenation of seven `SKILL.md` files, separated by banner comments of the form `# SKILL N: <name>` / `# Path: ~/.claude/skills/<name>/SKILL.md`. Currently included: `session-start`, `session-end`, `security-review`, `ship-feature`, `parallel-review`, `refresh-docs`, `new-feature`.

Each block starts with YAML frontmatter (`name`, `description`, `user-invocable`, `argument-hint?`, `allowed-tools`) — that frontmatter is what Claude Code's skill loader actually parses, so keep it well-formed when editing.

Important consistency rule: the master guide's overview tab advertises **eight** custom skills (the seven above **plus** `project-bootstrap`). `ALL_Skills.md` does not yet contain a `project-bootstrap` block. If you add or rename a skill, update both:

- The skill block in `ALL_Skills.md` (with valid frontmatter and a banner header).
- The skills table in `claude_code_master_guide.html` (the `overview` section and the `skills-ref` tab) so command, description, and replacement-prompt all match.

When editing a skill body, keep the operational style the existing skills use: numbered `## Step N` sections, fenced bash blocks for the exact commands the skill should run, and explicit "Do NOT" lines at the end where over-eager behaviour is a real risk.

## Working with `BestPractices.md`

Six numbered insights that mirror the master guide's top-level recommendations (Plan Mode, CLAUDE.md as the highest-leverage file, subagents, hooks, multi-agent orchestrators, team size). If a top-level recommendation in the HTML guide changes (e.g., the recommended orchestrator, the CLAUDE.md token budget, or the Plan Mode workflow), update the matching numbered item here so the two stay aligned.

## What not to do

- Don't introduce a `package.json`, build tooling, linter config, or test runner — there is nothing to build or test, and tooling here is pure maintenance overhead.
- Don't split the HTML into multiple files. The single-file, copy-anywhere shape is the entire point of the artifact.
- Don't split `ALL_Skills.md` into separate files inside this repo. It is intentionally one file so it can be reviewed/edited in one place; splitting into individual SKILL.md files is the **user's** install step into `~/.claude/skills/`, not a repo refactor.
- Don't `git`-anything — this directory is not a git repo. If the user wants version control, ask before running `git init`.
- Don't invent new tiers, agents, or skills. The named external tools (GrapeRoot, Hail Hydra, Caveman, Context-Mode, Superpowers, Trail of Bits skills, gstack, Repomix, Claude Context MCP, claude-mem, Ruflo, etc.) are real third-party projects. If a fact about one of them might be stale, verify before editing rather than guessing.


## Understanding the Current Folder Development
- @import read CreatingClaudeSetup/00-START-HERE.md
