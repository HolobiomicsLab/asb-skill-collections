"""Derive a chosen set of skills as an installable, pack-shaped unit.

A technique pack is the view of a collection whose membership is a technique
tag. A selection is the same view whose membership is a list of slugs, so it is
derived by the code that builds the packs: ``scripts/build_packs.py`` for the
leaves and the two filtered indexes, ``scripts/build_grounding_bundle.py`` for
the grounding helpers, and ``scripts/router_shape.py`` for the search script and
the router. The result is staged in a directory the caller owns and handed to
the ordinary installer, which copies it into a managed snapshot. What the agent
sees is a pack: one advertised router over ``leaves/``, ``skills_index.json``
and ``kb_bundle.json`` filtered to the selection, and the same helpers.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .repo import PackRef

#: Hex digits of the slug-list digest in a default selection name.
NAME_DIGEST_LENGTH = 8
MAX_NAME_LENGTH = 64
#: Lower-case words joined by single hyphens, like every marketplace pack name.
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DESCRIPTOR = Path(".claude-plugin") / "plugin.json"
UNVERSIONED = "unversioned"


class SelectionError(ValueError):
    """A selection that cannot be installed: empty, unknown slugs or a bad name."""


@dataclass(frozen=True)
class Selection:
    """What to derive: which slugs of which collection, under which unit name."""

    repo: Path
    collection_dir: Path
    name: str
    slugs: tuple[str, ...]


def parse_slugs(values) -> list[str]:
    """Split ``a,b`` style arguments into slugs, dropping blanks."""
    pieces = (piece.strip() for value in values for piece in value.split(","))
    return [slug for slug in pieces if slug]


def read_slugs_file(path: Path) -> list[str]:
    """Read one slug per line; ``#`` starts a comment, blank lines are skipped."""
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise SelectionError(f"cannot read the skills file {path}: {exc}") from exc
    uncommented = (line.split("#", 1)[0].strip() for line in lines)
    return [slug for slug in uncommented if slug]


def query_slugs(collection_dir: Path, query: str, top: int) -> list[str]:
    """Slugs of the first ``top`` hits the offline selector ranks for ``query``.

    Same index, same selector and same filters as ``asbb search``, so a reader
    who previews a query with search installs exactly what it listed.
    """
    from .. import asb_skill_index as idx

    rows = idx.load_rows(collection_dir, "skills")
    hits = idx.keyword_search(
        rows, query, k=top, collection=idx.collection_id(collection_dir)
    )
    return [hit["slug"] for hit in hits]


def check_slugs(requested: list[str], rows: list[dict]) -> list[str]:
    """Return the requested slugs without repeats, refusing empty or unknown ones."""
    slugs = list(dict.fromkeys(requested))
    if not slugs:
        raise SelectionError(
            "the selection is empty: --skills, --skills-file and --query named no skill"
        )
    known = {row.get("slug") for row in rows}
    unknown = [slug for slug in slugs if slug not in known]
    if unknown:
        raise SelectionError(
            f"{len(unknown)} slug(s) not in the collection index: {', '.join(unknown)}"
        )
    return slugs


def default_name(collection_dir: Path, slugs: list[str]) -> str:
    """``<collection>-subset-<digest>``, the digest taken over the sorted slugs.

    Order-independent on purpose: the same set of skills always gets the same
    name, so reinstalling it refreshes one unit instead of adding a second.
    """
    listing = "\n".join(sorted(set(slugs))).encode("utf-8")
    digest = hashlib.sha256(listing).hexdigest()[:NAME_DIGEST_LENGTH]
    return f"{Path(collection_dir).parent.name}-subset-{digest}"


def check_name(name: str, reserved: list[str]) -> None:
    """Refuse a malformed name, or one a marketplace pack already uses.

    The install record is keyed by name, so a selection named like a pack would
    take over that pack's record and its uninstall.
    """
    if len(name) > MAX_NAME_LENGTH or not NAME_PATTERN.fullmatch(name):
        raise SelectionError(
            f"selection name {name!r} must be lower-case letters and digits joined "
            f"by single hyphens, at most {MAX_NAME_LENGTH} characters"
        )
    if name in reserved:
        raise SelectionError(f"selection name {name!r} is a marketplace pack; choose another")


def _checkout_script(repo: Path, module: str):
    """Import ``scripts.<module>`` from the checkout the selection is drawn from.

    The pack derivation lives in the checkout's ``scripts/``, which the wheel
    does not ship. Installing a selection already needs that checkout, so the
    unit is derived by the same code that built the packs beside it.
    """
    root = str(Path(repo).resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    return importlib.import_module(f"scripts.{module}")


def _write_descriptor(selection: Selection, unit: Path) -> dict:
    """Write the unit's plugin.json from the collection's, renamed to the selection."""
    source = selection.collection_dir / DESCRIPTOR
    parent = json.loads(source.read_text(encoding="utf-8")) if source.is_file() else {}
    title = (parent.get("description") or "").split(".")[0].strip()
    collection = f"{selection.collection_dir.parent.name}/{selection.collection_dir.name}"
    descriptor = {
        **parent,
        "name": selection.name,
        "description": (
            f"{title or collection} (selection {selection.name}). "
            f"{len(selection.slugs)} selected skill(s) of the {collection} collection."
        ),
        "version": str(parent.get("version", UNVERSIONED)),
    }
    path = unit / DESCRIPTOR
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(descriptor, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return descriptor


def derive(selection: Selection, stage: Path) -> PackRef:
    """Build the selection as a pack under ``stage/<name>`` and return its reference.

    The steps and their order are the ones that produce the shipped technique
    packs; only the membership differs.
    """
    build_packs = _checkout_script(selection.repo, "build_packs")
    grounding = _checkout_script(selection.repo, "build_grounding_bundle")
    router_shape = _checkout_script(selection.repo, "router_shape")
    unit = Path(stage) / selection.name
    descriptor = _write_descriptor(selection, unit)
    spec = build_packs.PackSpec(unit, slugs=frozenset(selection.slugs))
    built = build_packs.build_pack(spec, selection.collection_dir)
    # The binder build_grounding_bundle ships by default, beside the module.
    binder = Path(grounding.__file__).with_name("perspicacite_kb_bind.py")
    grounding.build_unit(unit, selection.collection_dir, binder)
    router_shape.refresh_scripts(unit)
    router_shape.write_router(unit, built.selected)
    return PackRef(
        slug=selection.name,
        source=selection.collection_dir.relative_to(Path(selection.repo).resolve()).as_posix(),
        skills_dir=unit / "skills",
        version=descriptor["version"],
    )
