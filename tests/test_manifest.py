"""Tests for lib/manifest.py — 3 cases."""
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.manifest import load, validate

VALID_ENTRY = {
    "id": "test-tool",
    "kind": "npx",
    "install": "npx test-tool",
    "update": "npx test-tool",
    "verify": "command -v test-tool",
    "opt_in": False,
    "tier": 2,
}


def _write_manifest(entries):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        json.dump({"sources": entries}, f)
        return Path(f.name)


class TestManifest(unittest.TestCase):
    def test_valid_manifest_parses(self):
        p = _write_manifest([VALID_ENTRY])
        entries = load(str(p))
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["id"], "test-tool")

    def test_missing_required_field_fails_validation(self):
        bad = {k: v for k, v in VALID_ENTRY.items() if k != "tier"}
        errors = validate([bad])
        self.assertTrue(any("tier" in e for e in errors))

    def test_unknown_kind_fails_validation(self):
        bad = {**VALID_ENTRY, "kind": "magic-installer"}
        errors = validate([bad])
        self.assertTrue(any("unknown kind" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
