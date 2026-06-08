"""Load and validate sources.json manifest."""
import json

VALID_KINDS = {"npx", "pip", "pipx", "git-clone", "plugin-marketplace", "mcp-add", "npm-global"}
REQUIRED_FIELDS = {"id", "kind", "install", "update", "verify", "opt_in", "tier"}


def load(path: str) -> list:
    with open(path, "r") as f:
        data = json.load(f)
    return data["sources"]


def validate(entries: list) -> list:
    errors = []
    seen_ids = set()

    for i, entry in enumerate(entries):
        ref = entry.get("id", f"entry[{i}]")

        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{ref}: missing required field '{field}'")

        kind = entry.get("kind")
        if kind and kind not in VALID_KINDS:
            errors.append(f"{ref}: unknown kind '{kind}'")

        if entry.get("install_manual") and not entry.get("install_steps"):
            errors.append(f"{ref}: install_manual=true requires install_steps")

        entry_id = entry.get("id")
        if entry_id:
            if entry_id in seen_ids:
                errors.append(f"{ref}: duplicate id '{entry_id}'")
            seen_ids.add(entry_id)

    return errors
