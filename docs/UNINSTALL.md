# Uninstalling

## Run the uninstall command

```bash
./bin/claude-setup uninstall
```

The uninstaller:
1. Reads the install manifest (`~/.claude-setup-backups/<timestamp>-manifest.json`) to know exactly which files it installed
2. For each managed file, prompts how to handle it (see below)
3. Strips the `_origin: claude-setup` marker from `~/.claude/settings.json` (your own settings keys are preserved)
4. Runs the uninstall command for each installed upstream source (e.g. removes MCP servers, uninstalls npx packages)
5. Prints manual removal steps for plugin-marketplace sources that need interactive `/plugin` commands inside Claude Code

## File handling prompts

For each file the kit installed, you will be asked:

```
~/.claude/skills/session-start/SKILL.md
  [delete]   delete the file
  [keep]     leave it in place
  [revert]   restore from backup
```

- **delete** — deletes the file entirely
- **keep** — leaves it unchanged (useful if you've customised it and want to keep your version)
- **revert** — restores the original file from the backup tarball created at install time

## Backup location

Every install (and update) creates a timestamped tarball in:

```
~/.claude-setup-backups/
  20260607T153012Z.tar.gz
  20260614T090145Z.tar.gz   ← most recent
  20260607T153012Z-manifest.json
  20260614T090145Z-manifest.json
```

To manually restore a file from a backup:

```bash
# List what's in the backup
tar -tzf ~/.claude-setup-backups/20260607T153012Z.tar.gz

# Extract a single file
tar -xzf ~/.claude-setup-backups/20260607T153012Z.tar.gz \
    -C / home/.claude/settings.json
```

## Upstream source removal

The uninstaller automatically removes sources it can reach non-interactively:

| Source | Removal method |
|---|---|
| Context7 MCP | `claude mcp remove context7 --global` |
| Hail Hydra | `echo y \| npx hail-hydra-cc --uninstall` |
| Matt Pocock skills | `npx skills remove mattpocock/skills --yes` |
| GrapeRoot | `pip uninstall -y graperoot` |

Plugin-marketplace sources (adr-kit, repomix-mcp) must be removed manually. After uninstall, you will see:

```
Manual removal required:
  adr-kit:     Open Claude Code and run: /plugin uninstall adr-kit
  repomix-mcp: Open Claude Code and run: /plugin uninstall repomix-mcp
```

## After uninstalling

Run `./bin/claude-setup doctor` — it will confirm nothing managed by the kit is still present. If items remain, re-run `uninstall` or remove them manually using the instructions printed during the uninstall run.
