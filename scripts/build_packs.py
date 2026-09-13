#!/usr/bin/env python3
"""Re-derive every technique pack from its parent collection.

A pack is a *view* of a collection: the leaves whose ``techniques`` carry the
pack's declared tag, their ``SKILL.md`` bytes, and the two published indexes
filtered to that set. Membership is declared as data in ``packs/<domain>/
packs.yaml`` — never here — so adding a pack or retagging one is an edit to a
map, not to code.

Why this exists at all: the packs were split from the collection once, by hand,
on 2026-06-22. Nothing re-derived them afterwards, so the leaf added on
2026-06-23 never reached ``lc-ms``; three front-matter keys
(``provenance_tier``, ``tool_license``, ``grounding_tier``) were dropped from
every copy; a later DOI repair and a URL fix landed in the collection and not in
the copies; and both pack indexes lost ``provenance_tier``, ``grounding_tier``
and ``tools_used``. Every one of those is a *divergence from a source that
exists*, which is the only class of defect this script can have.

**Copies are byte-for-byte.** A pack leaf is the collection leaf's bytes, not a
re-render of selected fields. A declared field list has to be maintained in step
with the collection's front-matter vocabulary, and the three keys missing today
are exactly what happens when it is not; a byte copy cannot drift, cannot omit a
key nobody thought to list, and cannot carry a value the collection does not
have. The licence signal the collection leaves already carry (``license_tier``
plus the canonical banner) comes along for free, and
:func:`scripts.stamp_skill_license.stamp_copies` is still run afterwards to
re-assert it from the source — on a byte copy it must change nothing, and the
build reports it if it ever does.

Idempotence: ``build(build(tree)) == build(tree)``. The second run reports no
change, because every output is a pure function of the collection.

Scope: ``leaves/``, ``skills_index.json`` and ``kb_bundle.json``. Everything
else a pack ships — ``bin/``, ``commands/``, ``skills/`` (the router),
``.claude-plugin/`` and ``GROUNDING.md`` — is hand-maintained or owned by
:mod:`scripts.build_grounding_bundle`, and is deliberately not touched.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from asb_skill_collections import layout
from scripts.build_grounding_bundle import _read_corpus, filter_and_enrich_bundle
from scripts.propagate_license_tiers import detect_indent
from scripts.skill_index import split_frontmatter
from scripts.stamp_skill_license import stamp_copies

SCHEMA = "asb-pack-map/1.0"
MAP_FILENAME = "packs.yaml"
#: Where pack maps are discovered, relative to the repository root. One per
#: domain, beside the packs it describes.
MAP_GLOB = f"packs/*/{MAP_FILENAME}"
INDEX_FILENAME = "skills_index.json"
BUNDLE_FILENAME = "kb_bundle.json"
#: The JSON shape each generated file ships in, matching the producer that owns
#: it elsewhere: scripts/skill_index.py writes skills_index.json at indent 1 and
#: scripts/build_grounding_bundle.py writes kb_bundle.json at indent 2. Used
#: only when the file does not exist yet -- an existing file keeps its own shape,
#: so a rebuild never reformats a tree it did not create.
DEFAULT_INDENT = {INDEX_FILENAME: 1, BUNDLE_FILENAME: 2}


@dataclass(frozen=True)
class PackSpec:
    """One declared pack: where it lives and which technique tag selects it."""

    directory: Path
    tag: str
    map_path: Path

    @property
    def name(self) -> str:
        """The pack's directory name, as the map spells it."""
        return self.directory.name


@dataclass(frozen=True)
class PackMap:
    """One ``packs.yaml``: the parent collection and the packs derived from it."""

    path: Path
    collection_dir: Path
    packs: tuple[PackSpec, ...]


@dataclass(frozen=True)
class Divergence:
    """One way a pack is not the view of its collection that its map declares.

    Structured rather than a formatted string because two callers need it: this
    script's ``--check``, which prints it, and scripts/unit_closure.py, which
    turns it into a release-gate violation keyed by slug and file.
    """

    slug: str
    where: str
    reason: str

    def __str__(self) -> str:
        return f"{self.slug}: {self.reason}"


@dataclass
class PackBuild:
    """What one pack's build did, or would do under ``--dry-run``."""

    spec: PackSpec
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    refreshed: list[str] = field(default_factory=list)
    rewritten: list[str] = field(default_factory=list)
    restamped: list[str] = field(default_factory=list)
    selected: int = 0

    @property
    def changed(self) -> bool:
        """True when the build was not already a fixed point."""
        return bool(
            self.added
            or self.removed
            or self.refreshed
            or self.rewritten
            or self.restamped
        )

    def as_dict(self) -> dict:
        """A JSON-friendly summary, counts first and names after."""
        return {
            "pack": self.spec.name,
            "tag": self.spec.tag,
            "selected": self.selected,
            "added": self.added,
            "removed": self.removed,
            "refreshed": self.refreshed,
            "rewritten": self.rewritten,
            "restamped": self.restamped,
        }


def load_map(path: Path, root: Path) -> PackMap:
    """Read one ``packs.yaml`` into a :class:`PackMap`.

    Every path it names is resolved against ``root`` and required to stay inside
    it, so a map cannot point a build at a tree outside the repository.
    """
    path, root = Path(path), Path(root).resolve()
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if document.get("schema") != SCHEMA:
        raise ValueError(f"{path}: schema is not {SCHEMA!r}")
    source = str(document.get("source") or "")
    if not source:
        raise ValueError(f"{path}: no source collection declared")
    collection_dir = (root / source).resolve()
    if not collection_dir.is_relative_to(root) or not collection_dir.is_dir():
        raise ValueError(f"{path}: source {source!r} is not a directory inside {root}")
    entries = document.get("packs")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path}: packs must be a non-empty list")
    specs = []
    for entry in entries:
        directory, tag = (entry or {}).get("dir"), (entry or {}).get("tag")
        if not isinstance(directory, str) or "/" in directory or directory in ("", ".", ".."):
            raise ValueError(f"{path}: {directory!r} is not a single directory name")
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError(f"{path}: pack {directory!r} declares no technique tag")
        specs.append(PackSpec(path.parent / directory, tag, path))
    if len(specs) != len({spec.name for spec in specs}):
        raise ValueError(f"{path}: a pack directory is declared twice")
    return PackMap(path, collection_dir, tuple(specs))


def discover_maps(root: Path) -> list[PackMap]:
    """Every declared pack map in the repository, in stable path order."""
    root = Path(root).resolve()
    return [load_map(path, root) for path in sorted(root.glob(MAP_GLOB))]


def read_index(path: Path) -> list[dict]:
    """Read a ``skills_index.json``, accepting the list and wrapped-list forms."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("skills", []) if isinstance(data, dict) else data


def selected_slugs(index: list[dict], tag: str) -> set[str]:
    """The membership rule, stated once: ``tag ∈ entry.techniques``."""
    return {
        entry["slug"]
        for entry in index
        if isinstance(entry, dict)
        and isinstance(entry.get("slug"), str)
        and tag in (entry.get("techniques") or [])
    }


def pack_leaf_dir(pack_dir: Path, collection_dir: Path) -> Path:
    """Where a pack keeps its leaves: the shape of the collection it is a view of.

    ``layout.leaf_dir`` resolves shape from the tree on disk, which is right for
    a unit that already exists and wrong for one being derived: a pack with no
    ``leaves/`` yet resolves to the legacy ``skills/``, and a router-shaped
    collection's 2,617 copies would land in the dir a plugin host injects into
    every session prompt -- the cost router shape exists to avoid. A pack is a
    view of exactly one collection, and the pack's own router resolves leaves
    through the same module, so it takes that collection's shape.
    """
    return Path(pack_dir) / layout.leaf_dir(collection_dir).name


def _render_json(path: Path, payload) -> tuple[str, str | None]:
    """What this file should hold, and what it holds now, in its own shape.

    One renderer for both the build and its ``--dry-run``: a dry run that
    formatted differently from the build would report work that is not there.
    """
    previous = path.read_text(encoding="utf-8") if path.is_file() else None
    indent = (
        detect_indent(previous)
        if previous is not None
        else DEFAULT_INDENT.get(path.name, 1)
    )
    trailing = "\n" if previous is None or previous.endswith("\n") else ""
    return json.dumps(payload, indent=indent, ensure_ascii=False) + trailing, previous


def _write_json(path: Path, payload) -> bool:
    """Write JSON in the destination's own indent and newline; report a change."""
    rendered, previous = _render_json(path, payload)
    if rendered == previous:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- #
# Divergence: why a pack is not the view of its collection that it claims to be.
#
# Used by the build to decide what to write, and by scripts/unit_closure.py to
# fail a pack that has drifted. Both read the same rule and the same comparison,
# so the gate cannot pass a tree the generator would change.
# --------------------------------------------------------------------------- #


def _frontmatter_reasons(copy_text: str, source_text: str) -> list[str]:
    """Name the front-matter keys a copy lost or changed, source keys first."""
    copy_fm = split_frontmatter(copy_text)[0] or {}
    source_fm = split_frontmatter(source_text)[0] or {}
    reasons = []
    for label, on_copy, on_source in (
        ("", copy_fm, source_fm),
        ("metadata.", copy_fm.get("metadata") or {}, source_fm.get("metadata") or {}),
    ):
        if not isinstance(on_copy, dict) or not isinstance(on_source, dict):
            continue
        absent = sorted(key for key in on_source if key not in on_copy)
        if absent:
            reasons.append(
                "front matter absent from the copy: "
                + ", ".join(label + key for key in absent)
            )
        differing = sorted(
            key
            for key in on_source
            if key in on_copy and key != "metadata" and on_copy[key] != on_source[key]
        )
        if differing:
            reasons.append(
                "front matter differs from the collection: "
                + ", ".join(label + key for key in differing)
            )
        extra = sorted(key for key in on_copy if key not in on_source)
        if extra:
            reasons.append(
                "front matter the collection does not have: "
                + ", ".join(label + key for key in extra)
            )
    return reasons


def leaf_divergences(copy_path: Path, source_path: Path) -> list[str]:
    """Why one copied leaf is not its collection original.

    A copy is byte-for-byte, so difference is decided on bytes; the reasons
    that follow are diagnosis, not the test. Front matter is named key by key —
    an absent key is the failure that let ``provenance_tier`` go missing from
    4,949 copies while every one of them still looked well-formed.
    """
    copy_bytes = copy_path.read_bytes()
    source_bytes = source_path.read_bytes()
    if copy_bytes == source_bytes:
        return []
    copy_text = copy_bytes.decode("utf-8")
    source_text = source_bytes.decode("utf-8")
    reasons = _frontmatter_reasons(copy_text, source_text)
    if split_frontmatter(copy_text)[1] != split_frontmatter(source_text)[1]:
        reasons.append("body differs from the collection")
    return reasons or ["bytes differ from the collection"]


def pack_divergences(
    spec: PackSpec, collection_dir: Path, index: list[dict] | None = None
) -> list[Divergence]:
    """Every way one pack differs from the view its map declares.

    Three kinds, in the order a reader needs them: a selected leaf the pack does
    not ship, a shipped leaf the rule does not select, and a shipped leaf whose
    content is not its collection original.
    """
    collection_dir = Path(collection_dir)
    index = read_index(collection_dir / INDEX_FILENAME) if index is None else index
    wanted = selected_slugs(index, spec.tag)
    leaves = pack_leaf_dir(spec.directory, collection_dir)
    present = {
        path.parent.name for path in leaves.glob("*/SKILL.md") if path.is_file()
    }
    source_root = layout.leaf_dir(collection_dir)
    here = leaves.name
    findings = [
        Divergence(
            slug,
            f"{here}/{slug}/SKILL.md",
            f"selected by techniques ∋ {spec.tag!r} but absent from the pack",
        )
        for slug in sorted(wanted - present)
    ]
    findings += [
        Divergence(
            slug,
            f"{here}/{slug}/SKILL.md",
            f"shipped by the pack but not selected by techniques ∋ {spec.tag!r}",
        )
        for slug in sorted(present - wanted)
    ]
    for slug in sorted(present & wanted):
        source = source_root / slug / "SKILL.md"
        where = f"{here}/{slug}/SKILL.md"
        if not source.is_file():
            findings.append(
                Divergence(slug, where, "no collection leaf to derive the copy from")
            )
            continue
        findings += [
            Divergence(slug, where, reason)
            for reason in leaf_divergences(leaves / slug / "SKILL.md", source)
        ]
    return findings


# --------------------------------------------------------------------------- #
# The build.                                                                    #
# --------------------------------------------------------------------------- #


def build_pack(
    spec: PackSpec,
    collection_dir: Path,
    *,
    index: list[dict] | None = None,
    bundle: dict | None = None,
    corpus: list | None = None,
    dry_run: bool = False,
) -> PackBuild:
    """Re-derive one pack's leaf set, leaf bytes and both indexes.

    ``index``/``bundle``/``corpus`` are the collection's, passed in so a build of
    eight packs reads a 2 MB index and a 206 KB corpus once rather than eight
    times. Omitted, they are read here.
    """
    collection_dir = Path(collection_dir)
    index = read_index(collection_dir / INDEX_FILENAME) if index is None else index
    if bundle is None:
        bundle = json.loads((collection_dir / BUNDLE_FILENAME).read_text(encoding="utf-8"))
    corpus = _read_corpus(collection_dir) if corpus is None else corpus

    wanted = selected_slugs(index, spec.tag)
    source_root = layout.leaf_dir(collection_dir)
    leaves = pack_leaf_dir(spec.directory, collection_dir)
    present = {path.name for path in leaves.iterdir() if path.is_dir()} if leaves.is_dir() else set()
    result = PackBuild(spec, selected=len(wanted))

    for slug in sorted(present - wanted):
        result.removed.append(slug)
        if not dry_run:
            shutil.rmtree(leaves / slug)

    for slug in sorted(wanted):
        source = source_root / slug / "SKILL.md"
        if not source.is_file():
            raise ValueError(
                f"{collection_dir}: {INDEX_FILENAME} names {slug!r} with no leaf on disk"
            )
        target = leaves / slug / "SKILL.md"
        payload = source.read_bytes()
        if not target.is_file():
            result.added.append(slug)
        elif target.read_bytes() != payload:
            result.refreshed.append(slug)
        else:
            continue
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)

    outputs = (
        (INDEX_FILENAME, [entry for entry in index if entry.get("slug") in wanted]),
        (BUNDLE_FILENAME, filter_and_enrich_bundle(bundle, wanted, corpus)),
    )
    if dry_run:
        for name, payload in outputs:
            rendered, previous = _render_json(spec.directory / name, payload)
            if rendered != previous:
                result.rewritten.append(name)
        return result

    for name, payload in outputs:
        if _write_json(spec.directory / name, payload):
            result.rewritten.append(name)

    # The collection leaves are already stamped, so a byte copy arrives stamped.
    # Running the stamper anyway is the assertion, not the repair: anything it
    # reports here is a source leaf whose own tier and banner disagree, and the
    # build says so instead of silently correcting a copy away from its source.
    result.restamped = stamp_copies(spec.directory, collection_dir)
    return result


def build_map(pack_map: PackMap, *, dry_run: bool = False) -> list[PackBuild]:
    """Re-derive every pack in one map, reading the collection once."""
    index = read_index(pack_map.collection_dir / INDEX_FILENAME)
    bundle = json.loads(
        (pack_map.collection_dir / BUNDLE_FILENAME).read_text(encoding="utf-8")
    )
    corpus = _read_corpus(pack_map.collection_dir)
    return [
        build_pack(
            spec,
            pack_map.collection_dir,
            index=index,
            bundle=bundle,
            corpus=corpus,
            dry_run=dry_run,
        )
        for spec in pack_map.packs
    ]


def check_map(pack_map: PackMap) -> dict[str, list[Divergence]]:
    """Divergences per pack for one map; an empty mapping is a clean tree."""
    index = read_index(pack_map.collection_dir / INDEX_FILENAME)
    found = {
        spec.name: pack_divergences(spec, pack_map.collection_dir, index)
        for spec in pack_map.packs
    }
    return {name: reasons for name, reasons in found.items() if reasons}


def main(argv: list[str] | None = None) -> int:
    """Build the declared packs, or report how far they have drifted."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument(
        "--map",
        type=Path,
        action="append",
        dest="maps",
        help=f"a {MAP_FILENAME} to build; repeatable. Default: every {MAP_GLOB}.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report divergence from the collection and write nothing (exit 1 on any)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="report what a build would write"
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    maps = (
        [load_map(path, root) for path in args.maps] if args.maps else discover_maps(root)
    )
    if not maps:
        print(f"FAIL: no pack map matched {MAP_GLOB} under {root}.")
        return 1

    if args.check:
        divergent = 0
        for pack_map in maps:
            for name, reasons in check_map(pack_map).items():
                divergent += 1
                print(f"FAIL {pack_map.path.parent.relative_to(root)}/{name}:")
                for divergence in reasons:
                    print(f"  - {divergence}")
        packs = sum(len(pack_map.packs) for pack_map in maps)
        print(
            f"{'FAIL' if divergent else 'PASS'}: {divergent} of {packs} declared "
            f"pack(s) differ from their collection."
        )
        return 1 if divergent else 0

    changed = 0
    for pack_map in maps:
        for build in build_map(pack_map, dry_run=args.dry_run):
            changed += bool(build.changed)
            print(json.dumps(build.as_dict(), ensure_ascii=False))
    verb = "would change" if args.dry_run else "changed"
    print(f"{verb} {changed} pack(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
