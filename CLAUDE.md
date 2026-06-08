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

<!-- dgc-policy-v11 -->
# Dual-Graph Context Policy

This project uses a local dual-graph MCP server for efficient context retrieval.

## MANDATORY: Always follow this order

1. **Call `graph_continue` first** — before any file exploration, grep, or code reading.

2. **If `graph_continue` returns `needs_project=true`**: call `graph_scan` with the
   current project directory (`pwd`). Do NOT ask the user.

3. **If `graph_continue` returns `skip=true`**: project has fewer than 5 files.
   Do NOT do broad or recursive exploration. Read only specific files if their names
   are mentioned, or ask the user what to work on.

4. **Read `recommended_files`** using `graph_read` — **one call per file**.
   - `graph_read` accepts a single `file` parameter (string). Call it separately for each
     recommended file. Do NOT pass an array or batch multiple files into one call.
   - `recommended_files` may contain `file::symbol` entries (e.g. `src/auth.ts::handleLogin`).
     Pass them verbatim to `graph_read(file: "src/auth.ts::handleLogin")` — it reads only
     that symbol's lines, not the full file.
   - Example: if `recommended_files` is `["src/auth.ts::handleLogin", "src/db.ts"]`,
     call `graph_read(file: "src/auth.ts::handleLogin")` and `graph_read(file: "src/db.ts")`
     as two separate calls (they can be parallel).

5. **Check `confidence` and obey the caps strictly:**
   - `confidence=high` -> Stop. Do NOT grep or explore further.
   - `confidence=medium` -> If recommended files are insufficient, call `fallback_rg`
     at most `max_supplementary_greps` time(s) with specific terms, then `graph_read`
     at most `max_supplementary_files` additional file(s). Then stop.
   - `confidence=low` -> Call `fallback_rg` at most `max_supplementary_greps` time(s),
     then `graph_read` at most `max_supplementary_files` file(s). Then stop.

## Token Usage

A `token-counter` MCP is available for tracking live token usage.

- To check how many tokens a large file or text will cost **before** reading it:
  `count_tokens({text: "<content>"})`
- To log actual usage after a task completes (if the user asks):
  `log_usage({input_tokens: <est>, output_tokens: <est>, description: "<task>"})`
- To show the user their running session cost:
  `get_session_stats()`

Live dashboard URL is printed at startup next to "Token usage".

## Rules

- Do NOT use `rg`, `grep`, or bash file exploration before calling `graph_continue`.
- Do NOT do broad/recursive exploration at any confidence level.
- `max_supplementary_greps` and `max_supplementary_files` are hard caps - never exceed them.
- Do NOT dump full chat history.
- Do NOT call `graph_retrieve` more than once per turn.
- After edits, call `graph_register_edit` with the changed files. Use `file::symbol` notation (e.g. `src/auth.ts::handleLogin`) when the edit targets a specific function, class, or hook.

## Context Store

Whenever you make a decision, identify a task, note a next step, fact, or blocker during a conversation, call `graph_add_memory`.

**To add an entry:**
```
graph_add_memory(type="decision|task|next|fact|blocker", content="one sentence max 15 words", tags=["topic"], files=["relevant/file.ts"])
```

**Do NOT write context-store.json directly** — always use `graph_add_memory`. It applies pruning and keeps the store healthy.

**Rules:**
- Only log things worth remembering across sessions (not every minor detail)
- `content` must be under 15 words
- `files` lists the files this decision/task relates to (can be empty)
- Log immediately when the item arises — not at session end

## Session End

When the user signals they are done (e.g. "bye", "done", "wrap up", "end session"), proactively update `CONTEXT.md` in the project root with:
- **Current Task**: one sentence on what was being worked on
- **Key Decisions**: bullet list, max 3 items
- **Next Steps**: bullet list, max 3 items

Keep `CONTEXT.md` under 20 lines total. Do NOT summarize the full conversation — only what's needed to resume next session.
