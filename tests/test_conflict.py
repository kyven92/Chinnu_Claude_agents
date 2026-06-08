"""Tests for lib/conflict.py — 3 cases."""
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.conflict import compare_files, sha256_of, unified_diff


class TestConflict(unittest.TestCase):
    def _tmp(self, content: str) -> Path:
        f = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt")
        f.write(content)
        f.close()
        return Path(f.name)

    def test_identical_files(self):
        src = self._tmp("hello world\n")
        dst = self._tmp("hello world\n")
        self.assertEqual(compare_files(src, dst), "identical")

    def test_missing_dst(self):
        src = self._tmp("hello\n")
        dst = Path("/nonexistent/path/file.txt")
        self.assertEqual(compare_files(src, dst), "missing")

    def test_differs(self):
        src = self._tmp("version A\n")
        dst = self._tmp("version B\n")
        self.assertEqual(compare_files(src, dst), "differs")

    def test_unified_diff_contains_changes(self):
        src = self._tmp("new content\n")
        dst = self._tmp("old content\n")
        diff = unified_diff(src, dst)
        self.assertIn("+new content", diff)
        self.assertIn("-old content", diff)


if __name__ == "__main__":
    unittest.main()
