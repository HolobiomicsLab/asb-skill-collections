"""Canonical containment checks for installer-owned paths."""

import os
from pathlib import Path


def resolve_within(root: Path, rel: str) -> Path:
    """Return a lexical child path only when all symlinks stay beneath root.

    Absolute paths, parent components and the root itself are never entries.
    Keeping the lexical path lets callers unlink a validated symlink itself.
    """
    root = Path(root).resolve()
    # A stored record can hold anything, including a null or a number where a
    # relative path belongs. Refuse it like any other unsafe entry, so callers
    # report and skip it instead of meeting a TypeError from pathlib.
    if not isinstance(rel, (str, os.PathLike)):
        raise ValueError(f"refusing non-path entry {rel!r} beneath {root}")
    relative = Path(rel)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError(f"refusing unsafe relative path {rel!r} beneath {root}")
    final = root / relative
    try:
        resolved = final.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError(f"cannot resolve {final}: {exc}") from exc
    if resolved == root or root not in resolved.parents:
        raise ValueError(f"refusing path outside {root}: {final}")
    return final


def recorded_root(value: str) -> Path:
    """Validate a recorded absolute root without accepting a retargeted ancestor."""
    root = Path(value)
    if not root.is_absolute() or ".." in root.parts or root.resolve() != root:
        raise ValueError(f"recorded root moved or follows a symlink: {value}")
    return root
