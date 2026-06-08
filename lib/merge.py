"""
Additive merge for ~/.claude/settings.json.

Schema observed on 2026-06-07 (Claude Code cli, no pinned version):
  hooks.<HookType> is a list of objects:
    { "matcher": "<regex>", "hooks": [ { "type": "command", "command": "<path>", ...} ] }
  PostCompact entries omit "matcher".

We tag every entry we inject with "_origin": "claude-setup" so update/uninstall
can identify and manage only our entries.
"""
import copy
import json
from pathlib import Path


def load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text().strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON in {path}: {exc}") from exc


def _hook_command(hook_obj: dict) -> str:
    return hook_obj.get("command", "")


def _commands_in_group(group: dict) -> set:
    return {_hook_command(h) for h in group.get("hooks", [])}


def _find_matching_group(groups: list, matcher: str | None) -> dict | None:
    for g in groups:
        if matcher is None and "matcher" not in g:
            return g
        if matcher is not None and g.get("matcher") == matcher:
            return g
    return None


def merge_additive(existing: dict, fragment: dict) -> dict:
    result = copy.deepcopy(existing)
    result.setdefault("hooks", {})

    for hook_type, new_groups in fragment.get("hooks", {}).items():
        result["hooks"].setdefault(hook_type, [])
        existing_groups = result["hooks"][hook_type]

        for new_group in new_groups:
            matcher = new_group.get("matcher")
            target_group = _find_matching_group(existing_groups, matcher)

            if target_group is None:
                tagged = copy.deepcopy(new_group)
                for h in tagged.get("hooks", []):
                    h.setdefault("_origin", "claude-setup")
                existing_groups.append(tagged)
            else:
                existing_cmds = _commands_in_group(target_group)
                target_group.setdefault("hooks", [])
                for h in new_group.get("hooks", []):
                    if _hook_command(h) not in existing_cmds:
                        tagged_h = copy.deepcopy(h)
                        tagged_h.setdefault("_origin", "claude-setup")
                        target_group["hooks"].append(tagged_h)

    return result


def validate_merged(merged: dict) -> bool:
    try:
        json.dumps(merged)
    except (TypeError, ValueError):
        return False

    hooks = merged.get("hooks", {})
    if not isinstance(hooks, dict):
        return False
    for hook_type, groups in hooks.items():
        if not isinstance(groups, list):
            return False
        for group in groups:
            if not isinstance(group, dict):
                return False
            if "hooks" in group and not isinstance(group["hooks"], list):
                return False
    return True
