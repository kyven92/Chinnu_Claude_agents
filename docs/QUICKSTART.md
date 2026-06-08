# Quickstart

## Before you begin — install Claude Code

This kit configures Claude Code. You need Claude Code installed and authenticated first.

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Log in (opens browser to authenticate with your Anthropic account)
claude login
```

You need an Anthropic account. A free tier account works, but the agents in this kit use Opus and Sonnet models — **Pro or Team subscription is recommended** for regular use.

Full Claude Code setup guide: https://docs.anthropic.com/en/docs/claude-code/getting-started

---

## Fresh user (no existing `~/.claude/`)

Run the one-liner and you're done:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/ClaudeSetup/main/install.sh | bash
```

The installer will:
1. Check Python 3.8+ is available (version check is in `install.sh`)
2. Copy skills, agents, and hooks into `~/.claude/`
3. Merge settings fragments into `~/.claude/settings.json`
4. Install upstream integrations (Context7 MCP, Repomix, Hail Hydra, etc.)
5. Print a summary of everything installed

Open a new Claude Code session and type `/session-start` to verify the skills are live.

---

## Existing user (already have `~/.claude/`)

**Step 1 — Preview what will change:**

```bash
./bin/claude-setup install --dry-run
```

This prints every file that would be written or merged — no changes are made.

**Step 2 — Review any conflicts:**

If a file you've already customised conflicts with a kit file, the installer will prompt:

```
CONFLICT: ~/.claude/settings.json already exists and differs.
  [overwrite] replace with kit version
  [skip]      keep your version (default)
  [diff]      view the diff, then decide
  [abort]     stop the install entirely
```

Choose `overwrite` to take the kit's version, `skip` to keep yours, or `diff` to review changes first.

**Step 3 — Install:**

```bash
./bin/claude-setup install
```

A timestamped backup of every touched file is saved to `~/.claude-setup-backups/` before any change is made.

**Step 4 — Verify:**

```bash
./bin/claude-setup doctor
```

This checks that all installed pieces are present and the upstream integrations are reachable.

---

## GrapeRoot opt-in warning

GrapeRoot wraps the `claude` binary with a proxy that intercepts all subprocess calls. This is powerful but has a known side-effect: some MCP servers and multi-agent patterns that rely on direct `claude` invocation may behave unexpectedly.

The installer **does not** install GrapeRoot by default. If you want it:

```bash
./bin/claude-setup install --with-graperoot
```

You will be shown a full-screen warning and must type `y` explicitly. If you later have issues with Claude Code behaving unexpectedly, run:

```bash
./bin/claude-setup doctor
```

and look for the `graperoot` check — it will tell you whether GrapeRoot is active. To remove it:

```bash
pip uninstall graperoot
```
