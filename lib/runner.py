"""Run, detect, and verify external source install commands."""
import platform
import shutil
import subprocess

RUNTIME_BINS = {
    "node": "node",
    "npx": "npx",
    "python3": "python3",
    "pip": "pip",
    "bun": "bun",
    "git": "git",
    "gh": "gh",
    "claude": "claude",
}

_INSTALL_HINTS = {
    "node": {
        "linux": "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs",
        "darwin": "brew install node",
    },
    "npx": {
        "linux": "npx is bundled with node — install node first",
        "darwin": "npx is bundled with node — install node first",
    },
    "bun": {
        "linux": "curl -fsSL https://bun.sh/install | bash",
        "darwin": "curl -fsSL https://bun.sh/install | bash",
    },
    "git": {
        "linux": "sudo apt-get install git",
        "darwin": "brew install git",
    },
    "gh": {
        "linux": "sudo apt-get install gh  # or https://cli.github.com",
        "darwin": "brew install gh",
    },
    "python3": {
        "linux": "sudo apt-get install python3",
        "darwin": "brew install python3",
    },
    "pip": {
        "linux": "sudo apt-get install python3-pip",
        "darwin": "python3 -m ensurepip --upgrade",
    },
    "claude": {
        "linux": "npm install -g @anthropic-ai/claude-code",
        "darwin": "npm install -g @anthropic-ai/claude-code",
    },
}


def detect_runtime(name: str) -> bool:
    return shutil.which(RUNTIME_BINS.get(name, name)) is not None


def detect_missing_runtimes(needed: list) -> list:
    return [r for r in needed if not detect_runtime(r)]


def install_hint(runtime: str, os_name: str) -> str:
    os_key = "darwin" if os_name == "darwin" else "linux"
    return _INSTALL_HINTS.get(runtime, {}).get(os_key, f"Install {runtime} for your OS")


def run_install(source: dict, dry_run: bool = False) -> tuple:
    """Run source's install command, capturing output. Returns (exit_code, log)."""
    cmd = source.get("install")
    needed = source.get("needs_runtime", [])

    missing = detect_missing_runtimes(needed)
    if missing:
        return (1, f"missing runtimes: {', '.join(missing)}")

    if cmd is None:
        return (0, "no install command — skipped")

    if dry_run:
        return (0, f"dry-run: {cmd}")

    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    log = (result.stdout + result.stderr).strip()
    return (result.returncode, log)


def run_source(entry: dict, dry_run: bool = False) -> dict:
    """Run source's install command (non-capturing). Returns status dict."""
    sid = entry["id"]
    cmd = entry.get("install")
    needed = entry.get("needs_runtime", [])
    missing = detect_missing_runtimes(needed)

    if missing:
        return {"id": sid, "status": "skipped", "reason": f"missing runtimes: {', '.join(missing)}"}

    if cmd is None:
        return {"id": sid, "status": "skipped", "reason": "run-on-demand — no install command"}

    if dry_run:
        return {"id": sid, "status": "would-run", "command": cmd}

    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode == 0:
        return {"id": sid, "status": "ok"}
    return {"id": sid, "status": "failed", "returncode": result.returncode}


def verify_source(entry: dict) -> dict:
    sid = entry["id"]
    verify_cmd = entry.get("verify")
    if not verify_cmd:
        return {"id": sid, "status": "unverifiable"}
    result = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return {"id": sid, "status": "ok"}
    return {"id": sid, "status": "missing"}
