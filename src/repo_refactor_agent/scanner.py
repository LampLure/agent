"""Repository scanning utilities."""

from __future__ import annotations

from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
}
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".txt", ".toml", ".yaml", ".yml"}


def iter_source_files(root: Path) -> list[Path]:
    """Return source-like files under *root*, ignoring generated and dependency folders."""

    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files)
