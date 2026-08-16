"""Canonical resolution of where a collection keeps its skill files.

A plugin host registers every ``SKILL.md`` it finds under the plugin's
``skills/`` directory and injects each one's name + description into the
session prompt. A collection with thousands of leaves therefore costs more
context than a session has, purely from being installed.

**Router-shaped** collections avoid that: leaf skills live in ``leaves/`` —
shipped as data, retrieved on demand — while ``skills/`` holds only the small
number of entry points meant to be advertised (the router, gate skills).
**Legacy** collections keep every leaf in ``skills/``.

Both layouts are supported. Resolution is a property of the tree on disk, not
of the collection's name, so no consumer needs to special-case a domain.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Iterator

LEAF_DIRNAME = "leaves"
ADVERTISED_DIRNAME = "skills"


def is_router_shaped(collection_dir: str | os.PathLike) -> bool:
    """True when the collection keeps its leaves out of the advertised dir."""
    return (Path(collection_dir) / LEAF_DIRNAME).is_dir()


def leaf_dir(collection_dir: str | os.PathLike) -> Path:
    """The directory a collection's leaf skills are written to and read from.

    Returns ``leaves/`` for a router-shaped collection, ``skills/`` otherwise.
    The path is returned whether or not it exists, so callers can use it as a
    write target that preserves the collection's existing shape.
    """
    base = Path(collection_dir)
    return base / LEAF_DIRNAME if is_router_shaped(base) else base / ADVERTISED_DIRNAME


def skill_dirs(collection_dir: str | os.PathLike) -> list[Path]:
    """Every directory that may hold this collection's ``SKILL.md`` files.

    A router-shaped collection has two: the leaf corpus and the small
    advertised set. Enumerating both keeps validation coverage identical
    across layouts — an advertised skill is still a skill.
    """
    base = Path(collection_dir)
    if not is_router_shaped(base):
        return [base / ADVERTISED_DIRNAME]
    return [base / LEAF_DIRNAME, base / ADVERTISED_DIRNAME]


def iter_skill_md(
    collection_dir: str | os.PathLike, include_infrastructure: bool = False
) -> Iterator[Path]:
    """Yield every ``SKILL.md`` in a collection, in stable path order.

    Skips skills in ``_``-prefixed directories (routing scaffolds such as
    ``_router``) unless ``include_infrastructure`` is set: they are not
    paper-derived, so provenance and verbatim checks do not apply to them.
    Falls back to the collection root when no skill directory exists, matching
    the historical behaviour of the release gate.
    """
    roots: Iterable[Path] = [d for d in skill_dirs(collection_dir) if d.is_dir()]
    if not roots:
        roots = [Path(collection_dir)]
    seen: set[Path] = set()
    for root in roots:
        for path in sorted(root.rglob("SKILL.md")):
            if path in seen:
                continue
            parents = path.relative_to(root).parts[:-1]
            if not include_infrastructure and any(p.startswith("_") for p in parents):
                continue
            seen.add(path)
            yield path


def slugs(collection_dir: str | os.PathLike) -> set[str]:
    """Slugs of every skill in the collection, both leaf and advertised."""
    return {p.parent.name for p in iter_skill_md(collection_dir)}


if __name__ == "__main__":
    import sys
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        legacy = Path(tmp) / "legacy"
        (legacy / "skills" / "alpha").mkdir(parents=True)
        (legacy / "skills" / "alpha" / "SKILL.md").write_text("x")
        assert not is_router_shaped(legacy)
        assert leaf_dir(legacy).name == ADVERTISED_DIRNAME
        assert slugs(legacy) == {"alpha"}

        router = Path(tmp) / "router"
        (router / "leaves" / "beta").mkdir(parents=True)
        (router / "leaves" / "beta" / "SKILL.md").write_text("x")
        (router / "skills" / "_router").mkdir(parents=True)
        (router / "skills" / "_router" / "SKILL.md").write_text("x")
        (router / "skills" / "gate").mkdir(parents=True)
        (router / "skills" / "gate" / "SKILL.md").write_text("x")
        assert is_router_shaped(router)
        assert leaf_dir(router).name == LEAF_DIRNAME
        assert slugs(router) == {"beta", "gate"}, slugs(router)
        assert len(list(iter_skill_md(router, include_infrastructure=True))) == 3

    print("layout.py smoke check OK", file=sys.stderr)
