"""Tests for lib/merge.py — 6 cases."""
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.merge import load_settings, merge_additive, validate_merged

FRAGMENT = {
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {"type": "command", "command": "~/.claude/hooks/pre-bash-guard.sh"}
                ],
            }
        ],
        "PostCompact": [
            {
                "hooks": [
                    {"type": "command", "command": "~/.claude/hooks/reinsert-identity.sh"}
                ]
            }
        ],
    }
}


class TestLoadSettings(unittest.TestCase):
    def test_empty_existing_returns_empty_dict(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            f.write(b"")
            p = Path(f.name)
        result = load_settings(p)
        self.assertEqual(result, {})

    def test_missing_file_returns_empty_dict(self):
        result = load_settings(Path("/nonexistent/settings.json"))
        self.assertEqual(result, {})

    def test_malformed_json_raises_value_error(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            f.write("{bad json")
            p = Path(f.name)
        with self.assertRaises(ValueError):
            load_settings(p)


class TestMergeAdditive(unittest.TestCase):
    def test_existing_with_no_hooks_gets_fragment_entries(self):
        existing = {"model": "claude-sonnet-4-6"}
        merged = merge_additive(existing, FRAGMENT)
        self.assertIn("hooks", merged)
        self.assertIn("PreToolUse", merged["hooks"])
        self.assertEqual(len(merged["hooks"]["PreToolUse"]), 1)

    def test_origin_tag_present_on_injected_hooks(self):
        merged = merge_additive({}, FRAGMENT)
        hook = merged["hooks"]["PreToolUse"][0]["hooks"][0]
        self.assertEqual(hook.get("_origin"), "claude-setup")

    def test_existing_hook_not_duplicated(self):
        existing_hook = {
            "type": "command",
            "command": "~/.claude/hooks/pre-bash-guard.sh",
            "_origin": "claude-setup",
        }
        existing = {
            "hooks": {
                "PreToolUse": [
                    {"matcher": "Bash", "hooks": [existing_hook]}
                ]
            }
        }
        merged = merge_additive(existing, FRAGMENT)
        hooks_in_group = merged["hooks"]["PreToolUse"][0]["hooks"]
        self.assertEqual(len(hooks_in_group), 1)

    def test_does_not_mutate_existing(self):
        existing = {"model": "sonnet"}
        original = json.dumps(existing)
        merge_additive(existing, FRAGMENT)
        self.assertEqual(json.dumps(existing), original)


class TestValidateMerged(unittest.TestCase):
    def test_valid_merged_passes(self):
        merged = merge_additive({}, FRAGMENT)
        self.assertTrue(validate_merged(merged))

    def test_empty_dict_passes(self):
        self.assertTrue(validate_merged({}))


if __name__ == "__main__":
    unittest.main()
