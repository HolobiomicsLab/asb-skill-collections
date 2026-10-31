"""Paths as a receipt records them, without the layout of the machine that wrote it.

Receipts ship beside the collection they describe, in public repositories, so
an absolute path in one publishes the account name and scratch directories of
whichever machine ran the pipeline, and changes on every run. A path inside a
git checkout is recorded relative to that checkout. Any other path is recorded
by its final component, which still names the directory or file without saying
where it was.
"""

from __future__ import annotations

import os
from pathlib import Path


def recorded_path(path: str | os.PathLike[str]) -> str:
    """Return ``path`` relative to its git checkout, or else its final component."""
    resolved = Path(path).resolve()
    for anchor in (resolved, *resolved.parents):
        if (anchor / ".git").exists():
            return resolved.relative_to(anchor).as_posix() or "."
    return resolved.name or "."


def recorded_child(root: str | os.PathLike[str], path: str | os.PathLike[str]) -> str:
    """Record a path below ``root`` as the recorded root plus its relative part."""
    try:
        relative = Path(path).relative_to(Path(root)).as_posix()
    except ValueError:
        return recorded_path(path)
    label = recorded_path(root)
    if relative == ".":
        return label
    return relative if label == "." else f"{label}/{relative}"
