# Troubleshooting

## "Python 3.8+ required"

The `install.sh` script checks your Python version before proceeding.

**Fix — macOS:**
```bash
brew install python3
```

**Fix — Ubuntu/Debian:**
```bash
sudo apt-get install python3
```

**Fix — other Linux:** Use your distro's package manager, or install from [python.org](https://www.python.org/downloads/).

After installing, re-run `./install.sh`.

---

## "MCP Server Connection Failed" / Claude behaving unexpectedly

GrapeRoot wraps the `claude` binary. If it's active, direct `claude` invocations from MCP servers or subagents may be intercepted unexpectedly.

**Check:**
```bash
./bin/claude-setup doctor
```
Look for the `graperoot` line. If it says "graperoot (dgc) is installed and managed by this kit" or "graperoot (dgc) is installed but not managed by this kit", GrapeRoot is active.

**Fix — use GrapeRoot's wrapper for normal sessions:**
```bash
dgc .
```

**Fix — remove GrapeRoot entirely:**
```bash
pip uninstall graperoot
```

---

## "settings.json parse error"

Claude Code's settings file has become invalid JSON (often from a failed merge).

**Fix:**
```bash
# Find the most recent backup
ls -lt ~/.claude-setup-backups/

# Restore settings.json from it
tar -xzf ~/.claude-setup-backups/<latest>.tar.gz \
    --strip-components=1 -C ~/.claude/ \
    home/<youruser>/.claude/settings.json

# Re-run install to re-apply kit settings
./bin/claude-setup install
```

---

## "Plugin install failed inside Claude Code"

Interactive `/plugin` commands (used by adr-kit and similar marketplace sources) must be pasted manually into a running Claude Code session — they cannot be automated.

**Fix:** Open Claude Code and paste the exact commands printed by the installer:

```
/plugin install adr-kit@rvdbreemen
```

If the plugin install still fails, check that you're on a supported Claude Code version and that your network can reach the plugin registry.

---

## "`bash -n hooks/<x>.sh` fails" / hook syntax error

This usually means the hook file contains unescaped HTML entities (e.g. `&amp;`, `&lt;`) that crept in during extraction from the HTML guide.

**Fix:**
1. Open `hooks/<x>.sh` and replace HTML entities manually:
   - `&amp;` → `&`
   - `&lt;` → `<`
   - `&gt;` → `>`
   - `&quot;` → `"`
2. Re-run `bash -n hooks/<x>.sh` to confirm it parses cleanly.
3. Re-install the hook: `./bin/claude-setup install`

---

## "verify-guide-sync.sh exits 1" / drift detected

The HTML guide (`claude_code_master_guide.html`) references a skill or agent that doesn't exist in `skills/` or `agents/`, or vice versa.

**Fix:**

```bash
bash scripts/verify-guide-sync.sh
```

Read the output — it names the missing reference. Either:
- Add the missing skill/agent file, **or**
- Remove the stale reference from the HTML guide's skills/agents table

Then re-run the script until it exits 0.

---

## Doctor shows a source as "not installed"

The upstream source's verify command returned a non-zero exit code.

**Fix:** Re-run install for that source only:
```bash
./bin/claude-setup install
```

The installer skips already-installed files and re-attempts any source whose verify check fails.
