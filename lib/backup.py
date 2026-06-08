"""Backup creation, install-manifest writing, and backup pruning."""
import hashlib
import json
import os
import tarfile
from datetime import datetime, timezone
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def create_backup(target: Path, paths_to_back_up: list) -> Path:
    backup_root = Path.home() / ".claude-setup-backups"
    backup_root.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tarball = backup_root / f"{ts}.tar.gz"

    with tarfile.open(tarball, "w:gz") as tar:
        for p in paths_to_back_up:
            full = target / p if not p.is_absolute() else p
            if full.exists():
                tar.add(full, arcname=str(p))

    return tarball


def write_install_manifest(backup_dir: Path, files_written: list) -> None:
    manifest_path = backup_dir.parent / (backup_dir.stem.replace(".tar", "") + "-manifest.json")
    with open(str(backup_dir).replace(".tar.gz", "-manifest.json"), "w") as f:
        json.dump(files_written, f, indent=2)


def prune_old_backups(backup_dir: Path, keep_last: int = 5) -> None:
    tarballs = sorted(backup_dir.glob("*.tar.gz"), key=lambda p: p.stat().st_mtime)
    to_delete = tarballs[: max(0, len(tarballs) - keep_last)]
    for old in to_delete:
        old.unlink(missing_ok=True)
        manifest = Path(str(old).replace(".tar.gz", "-manifest.json"))
        if manifest.exists():
            manifest.unlink()
