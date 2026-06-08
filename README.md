# Chinnu-Claude-setup

A one-command-installable kit that deploys the full 5-tier Claude Code setup described in the included `claude_code_master_guide.html` into your `~/.claude/` directory — **additively**, **non-destructively**, with a clean upstream-sync model.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/ClaudeSetup/main/install.sh | bash
```

Or clone and install locally:

```bash
git clone https://github.com/YOUR_USERNAME/ClaudeSetup.git
cd ClaudeSetup
./install.sh
```

## What you get

- **8 custom skills** (`/session-start`, `/session-end`, `/security-review`, `/ship-feature`, `/parallel-review`, `/refresh-docs`, `/new-feature`, `/project-bootstrap`)
- **9 specialized agents** (planner, architect, code-reviewer, security-auditor, debugger, implementer, implementer-large, build-error-resolver, e2e-runner)
- **4 safety hooks** (pre-bash guard, secret-leak scan, identity reinsertion, post-write diff review)
- **18 upstream integrations** wired in — Hail Hydra, Context7 MCP, Repomix, Matt Pocock skills, Trail of Bits security skills, claude-mem, and more

All your existing `~/.claude/` files are backed up before anything is changed. Conflicts are resolved interactively.

## Quick links

| | |
|---|---|
| **First install** | [docs/QUICKSTART.md](docs/QUICKSTART.md) |
| **Using the agents** | [docs/AGENTS.md](docs/AGENTS.md) |
| **Keeping it current** | [docs/UPDATE.md](docs/UPDATE.md) |
| **Removing it** | [docs/UNINSTALL.md](docs/UNINSTALL.md) |
| **Something broke** | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| **Adding your own skill** | [docs/ADDING-A-SKILL.md](docs/ADDING-A-SKILL.md) |
| **Contributing** | [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) |
| **The full guide** | `claude_code_master_guide.html` — open in any browser |

## Requirements

**Claude Code must be installed first** — this kit configures it, it does not install it.

```bash
npm install -g @anthropic-ai/claude-code
claude login
```

You need an Anthropic account (free tier works, Pro/Team recommended for agents). See the [official Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/getting-started) for full setup.

Once Claude Code is running, you also need:
- Python 3.8+
- Bash

## License

MIT — see [LICENSE](LICENSE).
