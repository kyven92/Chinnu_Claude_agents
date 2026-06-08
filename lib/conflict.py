"""File comparison utilities."""
import difflib
import hashlib
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def compare_files(src: Path, dst: Path) -> str:
    if not dst.exists():
        return "missing"
    if sha256_of(src) == sha256_of(dst):
        return "identical"
    return "differs"


def unified_diff(src: Path, dst: Path) -> str:
    src_lines = src.read_text(errors="replace").splitlines(keepends=True)
    dst_lines = dst.read_text(errors="replace").splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(dst_lines, src_lines, fromfile=str(dst), tofile=str(src))
    )
