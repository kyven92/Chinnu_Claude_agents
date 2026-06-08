"""Tests for lib/backup.py — 3 cases."""
import json
import tarfile
import tempfile
import time
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.backup import create_backup, prune_old_backups, write_install_manifest


class TestBackup(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.backup_root = Path(tempfile.mkdtemp())

    def _patch_backup_root(self):
        import lib.backup as bmod
        self._orig = bmod.Path.home
        bmod_home = lambda: self.backup_root
        return bmod_home

    def test_backup_creates_tarball(self):
        target = self.tmpdir
        file_a = target / "skills" / "test" / "SKILL.md"
        file_a.parent.mkdir(parents=True)
        file_a.write_text("test skill content")

        import lib.backup as bmod
        orig_home = bmod.Path.home
        bmod.Path.home = lambda: self.backup_root

        try:
            tarball = create_backup(target, [Path("skills/test/SKILL.md")])
            self.assertTrue(tarball.exists())
            self.assertTrue(tariff := tarfile.open(tarball))
            tariff.close()
        finally:
            bmod.Path.home = orig_home

    def test_write_install_manifest_creates_json(self):
        tarball = self.backup_root / "20260607T000000Z.tar.gz"
        tarball.touch()
        records = [
            {"src_repo_path": "skills/test/SKILL.md", "dst_path": "~/.claude/skills/test/SKILL.md",
             "sha256": "abc123", "action": "wrote"}
        ]
        write_install_manifest(tarball, records)
        manifest_file = Path(str(tarball).replace(".tar.gz", "-manifest.json"))
        self.assertTrue(manifest_file.exists())
        data = json.loads(manifest_file.read_text())
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["action"], "wrote")

    def test_prune_keeps_last_n_never_deletes_most_recent(self):
        backup_dir = self.backup_root / ".claude-setup-backups"
        backup_dir.mkdir()

        tarballs = []
        for i in range(8):
            tb = backup_dir / f"2026060{i}T000000Z.tar.gz"
            tb.touch()
            time.sleep(0.01)
            tarballs.append(tb)

        prune_old_backups(backup_dir, keep_last=5)

        remaining = sorted(backup_dir.glob("*.tar.gz"), key=lambda p: p.stat().st_mtime)
        self.assertEqual(len(remaining), 5)
        self.assertIn(tarballs[-1], remaining)


if __name__ == "__main__":
    unittest.main()
