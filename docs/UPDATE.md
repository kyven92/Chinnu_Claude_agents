# Updating

## Run the update command

```bash
./bin/claude-setup update
```

The updater runs three passes in sequence:

1. **Self-update** — pulls the latest kit from the upstream git remote (`git pull`). If the repo is not a git clone (e.g. you installed via `curl | bash`), this step is skipped with a note.
2. **Vendored file refresh** — re-copies skills, agents, hooks, and settings fragments from the kit into `~/.claude/`. Files you've modified since install will prompt the same `[k/o/m]` conflict resolution dialog as the installer.
3. **Upstream source refresh** — re-runs the `update` command for each installed upstream source (e.g. `npx hail-hydra-cc --update`, `claude mcp add context7 --update`).

## What's safe to update automatically

| Component | Auto-updated | Notes |
|---|---|---|
| Skills (`~/.claude/skills/`) | Yes | Conflict dialog if you've edited locally |
| Agents (`~/.claude/agents/`) | Yes | Conflict dialog if you've edited locally |
| Hooks (`~/.claude/hooks/`) | Yes | Conflict dialog if you've edited locally |
| `settings.json` fragments | Yes | Merged additively; your own keys are preserved |
| Context7 MCP | Yes | `claude mcp add` is idempotent |
| Repomix MCP | Yes | `claude mcp add` is idempotent |
| Hail Hydra | Yes | `npx hail-hydra-cc --update` |
| Matt Pocock skills | Yes | `npx skills update mattpocock/skills` |

## What requires manual follow-up

**Plugin-marketplace sources** (adr-kit only) cannot be updated automatically because they use interactive `/plugin install` commands inside Claude Code. After `claude-setup update`, the updater will print the exact command to paste:

```
Manual update required for plugin-marketplace sources:
  adr-kit:  /plugin install adr-kit@rvdbreemen
```

Paste this into a Claude Code session to refresh the plugin. All other sources — including threat-modeling (npx-based) — are updated automatically.

## Verify after update

```bash
./bin/claude-setup doctor
```

Doctor checks that all installed pieces are present and reachable. If anything is missing it tells you exactly what to re-run.

## Keeping your customisations

If you want to preserve local edits to a skill or agent and **never** have them overwritten by updates, add the file path to your local settings:

```bash
# In ~/.claude/settings.json, add:
"claude-setup": {
  "force-ours": ["skills/session-start/SKILL.md"]
}
```

Or pass `--force-ours` on the command line:

```bash
./bin/claude-setup update --force-ours skills/session-start/SKILL.md
```
