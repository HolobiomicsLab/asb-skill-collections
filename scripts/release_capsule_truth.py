#!/usr/bin/env python
"""Make a promoted capsule's own documents describe the capsule the release ships.

The promotion step deliberately ships a *slim* capsule
(``promote_benchmark_layer._CAPSULE_KEEP``): ledger, evaluation, evidence, inputs,
the provenance manifest and the RO-Crate.  Two documents inside that capsule were written
against the *build*, and were promoted unchanged, so both described files the
release does not carry:

* the benchmark card ended with "See the ``ro-crate-metadata.json`` in this
  capsule for full provenance" — no released capsule contains that file;
* ``artifact_provenance.json`` listed the build's artefacts — measured over the
  three benchmark collections, 2,085 declared paths of which **0** existed in the
  released capsule.

This module holds the single rule that fixes both, so the generator and the
already-promoted tree cannot drift: ``promote_benchmark_layer`` calls it while
promoting, and ``--check`` / ``--write`` below applies the same functions to a
collection that is already on disk.  Both are idempotent.

The capsule's RO-Crate is the third such document, and the one the card footer
used to name.  The build writes one per capsule; promotion now ships it, pruned to
the capsule the release carries (``prune_crate``).  A verbatim copy would not do:
measured over the 417 capsules, the build crates describe 18,097 files the slim
capsule does not hold, point ``repme:buildManifestRef`` outside the capsule, and
carry 12,425 absolute paths of the build machine in ``oa:source``.  Their
descriptor also claims the Workflow Run Crate 0.5 profile, which requires a
``mainEntity`` workflow that none of the 417 declares, so the release copy claims
RO-Crate 1.1 only.  ``crate_problems`` is the rule gate 8 enforces on the result.

Usage:
  release_capsule_truth.py --check collections/metabolomics/v1
  release_capsule_truth.py --write collections/metabolomics/v1
  release_capsule_truth.py --write collections/metabolomics/v1 \\
      --import-crates-from <ASB outputs/asbb_<domain>>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

__all__ = [
    "BUILD_CARD_FOOTER_RE",
    "CRATE",
    "align_capsule_provenance",
    "capsule_for_card",
    "card_footer",
    "align_collection",
    "crate_problems",
    "import_build_crates",
    "prune_crate",
    "released_capsules",
    "slug_from_build",
]

CRATE = "ro-crate-metadata.json"
ROCRATE_1_1 = "https://w3id.org/ro/crate/1.1"
ROCRATE_1_1_CONTEXT = "https://w3id.org/ro/crate/1.1/context"
# The profiles gate 8 can check.  A crate claiming another one would ship a claim
# nothing in this repository measures; add a profile here with its validator.
CHECKED_PROFILES = (ROCRATE_1_1,)
# Where a build-machine path is re-stated: the build is named, the machine is not.
BUILD_LOCATOR = "urn:asb:build:"
# The two capsule documents promotion rewrites; every other file is the build's, byte for byte.
REWRITTEN_BY_PROMOTION = ("artifact_provenance.json", CRATE)

_URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
# A whole string value that is a filesystem path: two segments at least, so a unit
# such as "/min" is not one.
_PATH_VALUE = re.compile(r"(?:file://)?(?:/[^\s/]+){2,}/?|[A-Za-z]:[\\/]\S+")
# Anywhere in a crate's text, as the receipt test checks receipts.
_ABSOLUTE_IN_TEXT = re.compile(
    r"(^|[\"'\s(])(file://|/Users/|/home/|/private/|/tmp/|/var/folders/|[A-Za-z]:\\\\)"
)
# As the build's own crates declare them (measured over the 417); others get none.
_ENCODING_BY_SUFFIX = {
    ".json": "application/json",
    ".jsonl": "application/jsonlines",
    ".jsonld": "application/ld+json",
    ".md": "text/markdown",
    ".sh": "application/x-sh",
    ".svg": "image/svg+xml",
    ".txt": "text/plain",
}

# The footer as ASB's renderer writes it.  Matched loosely on the crate sentence
# so a reworded preamble upstream still gets retargeted rather than silently kept.
BUILD_CARD_FOOTER_RE = re.compile(
    r"See the `ro-crate-metadata\.json` in this capsule for full provenance\."
)

_RELEASE_NOTE = (
    "This capsule is the slim subset promoted into the release. `artifacts` lists the "
    "build-recorded artefacts this capsule carries; `omitted_from_release` lists those it "
    "does not, and `contents` lists every file that is here."
)


def card_footer(rel_to_provenance: str) -> str:
    """The sentence that replaces the crate claim, pointing at a file that exists."""
    return (
        f"See [`artifact_provenance.json`]({rel_to_provenance}) for what this release "
        "carries; it also lists the build artefacts the release does not promote."
    )


def capsule_for_card(card: Path, collection_dir: Path) -> Path | None:
    """The released capsule a promoted card belongs to, or None.

    Cards are promoted to ``benchmark/cards/<tool>/task_NNN.md`` and capsules to
    ``capsules/<tool>/<capsule>/``, where the capsule directory is either the task
    id itself or ``<paper>__<task id>``.
    """
    tool = card.parent.name
    task = card.stem
    capdir = collection_dir / "capsules" / tool
    if not capdir.is_dir():
        return None
    hits = [
        d
        for d in sorted(capdir.iterdir())
        if d.is_dir() and (d.name == task or d.name.endswith(f"__{task}"))
    ]
    return hits[0] if len(hits) == 1 else None


def align_capsule_provenance(manifest: dict, capsule_dir: Path) -> dict:
    """Return the manifest rewritten to describe ``capsule_dir`` as it ships.

    Entries whose path is absent move to ``release.omitted_from_release`` instead
    of being deleted: the release should not carry them, and should not pretend
    the build never produced them either.
    """
    present: list = []
    omitted: list[str] = []
    # A manifest already aligned no longer carries the absent entries under
    # ``artifacts``; re-reading its own record is what makes this a fixed point,
    # so a second pass neither loses the omissions nor reports a change.
    for path in (manifest.get("release") or {}).get("omitted_from_release") or []:
        if isinstance(path, str) and path not in omitted:
            omitted.append(path)
    for entry in manifest.get("artifacts") or []:
        if not isinstance(entry, dict):
            continue
        path = str(entry.get("path", ""))
        target = path.split("#", 1)[0]
        if target and (capsule_dir / target).exists():
            present.append(entry)
        elif path and path not in omitted:
            omitted.append(path)

    contents = sorted(
        str(f.relative_to(capsule_dir).as_posix())
        for f in capsule_dir.rglob("*")
        if f.is_file()
    )
    out = dict(manifest)
    out["artifacts"] = present
    out["release"] = {
        "profile": "slim",
        "note": _RELEASE_NOTE,
        "contents": contents,
        "omitted_from_release": omitted,
    }
    return out


def write_capsule_provenance(capsule_dir: Path) -> bool:
    """Align one capsule's manifest in place.  True if the file changed."""
    path = capsule_dir / "artifact_provenance.json"
    if not path.is_file():
        return False
    before = path.read_text(encoding="utf-8")
    manifest = json.loads(before)
    after = json.dumps(align_capsule_provenance(manifest, capsule_dir), indent=2) + "\n"
    if after == before:
        return False
    path.write_text(after, encoding="utf-8")
    return True


def retarget_card(card: Path, collection_dir: Path) -> bool:
    """Retarget one promoted card's footer.  True if the file changed."""
    text = card.read_text(encoding="utf-8")
    if not BUILD_CARD_FOOTER_RE.search(text):
        return False
    capsule = capsule_for_card(card, collection_dir)
    if capsule is None:
        return False
    rel = Path(os.path.relpath(capsule / "artifact_provenance.json", card.parent)).as_posix()
    card.write_text(BUILD_CARD_FOOTER_RE.sub(card_footer(rel), text), encoding="utf-8")
    return True


def released_capsules(collection_dir: Path) -> list[Path]:
    """Every capsule directory a collection ships: ``capsules/<tool>/<capsule>/``."""
    capdir = Path(collection_dir) / "capsules"
    if not capdir.is_dir():
        return []
    return sorted(d for d in capdir.glob("*/*") if d.is_dir())


def _local_id(value) -> bool:
    """A reference to a path inside the crate, as opposed to a URI or a graph node."""
    return (
        isinstance(value, str)
        and value not in ("./", ".", CRATE)
        and not value.startswith("#")
        and not (_URI_SCHEME.match(value) and not _PATH_VALUE.fullmatch(value))
    )


def _resolves(value: str, capsule_dir: Path) -> bool:
    target = value.split("#", 1)[0]
    if not target or _PATH_VALUE.fullmatch(target) or target.startswith("/"):
        return False
    root = capsule_dir.resolve()
    path = (root / target).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return path.exists()


def _build_locator(path: str) -> str:
    """Re-state a build-machine path without the machine.

    ASB writes its builds under an ``outputs/`` directory, so what follows it names
    the build and the artefact; without that anchor only the last component is kept.
    """
    text = path.replace("\\", "/")
    text = text[len("file://"):] if text.startswith("file://") else text
    head, sep, tail = text.rpartition("/outputs/")
    name = tail if sep else text.rstrip("/").rsplit("/", 1)[-1]
    return BUILD_LOCATOR + name


def _present_files(capsule_dir: Path) -> list[str]:
    return sorted(
        f.relative_to(capsule_dir).as_posix()
        for f in capsule_dir.rglob("*")
        if f.is_file() and f.relative_to(capsule_dir).as_posix() != CRATE
    )


def prune_crate(crate: dict, capsule_dir: Path) -> dict:
    """Return ``crate`` rewritten to describe ``capsule_dir`` as the release ships it.

    * a data entity whose path is not in the capsule is dropped, and so is every
      reference to a path that is not in the capsule (a property left with no value
      is removed rather than kept empty);
    * a string value that is a filesystem path becomes a ``urn:asb:build:`` locator;
    * every file the capsule holds is described and listed in the root's ``hasPart``;
    * the descriptor keeps only the conformance claims gate 8 checks.

    Applying it to its own output changes nothing.
    """
    capsule_dir = Path(capsule_dir)
    dropped: set[str] = set()
    graph = []
    for entity in crate.get("@graph") or []:
        if not isinstance(entity, dict):
            continue
        eid = entity.get("@id")
        if _local_id(eid) and not _resolves(eid, capsule_dir):
            dropped.add(eid)
            continue
        graph.append(entity)

    missing = object()

    def rewrite(value):
        if isinstance(value, dict):
            if set(value) == {"@id"} and _local_id(value["@id"]):
                return missing if not _resolves(value["@id"], capsule_dir) else value
            out = {}
            for key, item in value.items():
                if key == "@id":
                    out[key] = item
                    continue
                new = rewrite(item)
                if new is missing or new == []:
                    continue
                out[key] = new
            return out
        if isinstance(value, list):
            kept = [rewrite(item) for item in value]
            return [item for item in kept if item is not missing]
        if isinstance(value, str) and _PATH_VALUE.fullmatch(value):
            return _build_locator(value)
        return value

    graph = [rewrite(entity) for entity in graph]
    by_id = {entity.get("@id"): entity for entity in graph}

    descriptor = by_id.get(CRATE)
    if descriptor is not None:
        claims = descriptor.get("conformsTo")
        claims = claims if isinstance(claims, list) else [claims] if claims else []
        kept = [c for c in claims if isinstance(c, dict) and c.get("@id") in CHECKED_PROFILES]
        descriptor["conformsTo"] = kept or [{"@id": ROCRATE_1_1}]

    root = by_id.get("./")
    if root is not None:
        parts = root.get("hasPart")
        parts = parts if isinstance(parts, list) else [parts] if parts else []
        listed = {p.get("@id") for p in parts if isinstance(p, dict)}
        for rel in _present_files(capsule_dir):
            if rel not in by_id:
                entity = {"@id": rel, "@type": "File", "name": rel}
                encoding = _ENCODING_BY_SUFFIX.get(Path(rel).suffix)
                if encoding:
                    entity["encodingFormat"] = encoding
                graph.append(entity)
                by_id[rel] = entity
            if rel not in listed:
                parts.append({"@id": rel})
                listed.add(rel)
        root["hasPart"] = parts

    out = dict(crate)
    out["@graph"] = graph
    return out


def _dump_crate(crate: dict) -> str:
    return json.dumps(crate, indent=2, ensure_ascii=False) + "\n"


def write_capsule_crate(capsule_dir: Path) -> bool:
    """Prune one capsule's crate in place.  True if the file changed."""
    path = Path(capsule_dir) / CRATE
    if not path.is_file():
        return False
    before = path.read_text(encoding="utf-8")
    after = _dump_crate(prune_crate(json.loads(before), Path(capsule_dir)))
    if after == before:
        return False
    path.write_text(after, encoding="utf-8")
    return True


def _ids_and_references(value, found: list[str]) -> None:
    if isinstance(value, dict):
        if "@id" in value and _local_id(value["@id"]):
            found.append(value["@id"])
        for key, item in value.items():
            if key != "@id":
                _ids_and_references(item, found)
    elif isinstance(value, list):
        for item in value:
            _ids_and_references(item, found)


def crate_problems(capsule_dir: Path) -> list[str]:
    """What is wrong with the RO-Crate a released capsule ships.  Empty when nothing is.

    The rule gate 8 enforces: RO-Crate 1.1's structural requirements, no claim of a
    profile this repository does not check, no path that is not in the capsule, no
    file in the capsule the crate does not describe, and no build-machine path.
    """
    capsule_dir = Path(capsule_dir)
    path = capsule_dir / CRATE
    if not path.is_file():
        return [f"no {CRATE}"]
    text = path.read_text(encoding="utf-8")
    try:
        crate = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"{CRATE} is not JSON: {exc}"]
    if not isinstance(crate, dict):
        return [f"{CRATE} is not a JSON object"]

    problems: list[str] = []
    context = crate.get("@context")
    contexts = context if isinstance(context, list) else [context]
    if ROCRATE_1_1_CONTEXT not in contexts:
        problems.append(f"@context does not include {ROCRATE_1_1_CONTEXT}")
    graph = crate.get("@graph")
    if not isinstance(graph, list) or not all(isinstance(e, dict) and "@id" in e for e in graph):
        return problems + ["@graph is not a list of entities with an @id"]
    by_id = {e["@id"]: e for e in graph}

    descriptor = by_id.get(CRATE)
    if descriptor is None:
        problems.append("no metadata descriptor entity")
    else:
        if descriptor.get("about") != {"@id": "./"}:
            problems.append("the descriptor is not about ./")
        claims = descriptor.get("conformsTo")
        claims = claims if isinstance(claims, list) else [claims]
        iris = [c.get("@id") for c in claims if isinstance(c, dict)]
        if ROCRATE_1_1 not in iris:
            problems.append(f"the descriptor does not conform to {ROCRATE_1_1}")
        for iri in iris:
            if iri not in CHECKED_PROFILES:
                problems.append(f"the descriptor claims {iri}, which this gate does not check")

    root = by_id.get("./")
    types = (root or {}).get("@type")
    if root is None or "Dataset" not in (types if isinstance(types, list) else [types]):
        problems.append("no root Dataset ./")
        listed: set = set()
    else:
        parts = root.get("hasPart") or []
        listed = {p.get("@id") for p in (parts if isinstance(parts, list) else [parts]) if isinstance(p, dict)}

    references: list[str] = []
    _ids_and_references(graph, references)
    for ref in sorted(set(references)):
        if not _resolves(ref, capsule_dir):
            problems.append(f"names {ref!r}, which the capsule does not hold")
    for rel in _present_files(capsule_dir):
        if rel not in by_id:
            problems.append(f"does not describe {rel!r}")
        elif rel not in listed:
            problems.append(f"does not list {rel!r} in the root's hasPart")
    leaks = len(_ABSOLUTE_IN_TEXT.findall(text))
    if leaks:
        problems.append(f"carries {leaks} absolute filesystem path(s)")
    return problems


def slug_from_build(dirname: str) -> str:
    """The tool slug a build directory is promoted under (``coll_x`` / ``x_grounded`` -> ``x``)."""
    s = re.sub(r"^coll_", "", dirname)
    s = re.sub(r"_grounded$", "", s)  # e.g. spec2vec_grounded -> spec2vec
    return s.strip("_").lower()


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def import_build_crates(collection_dir: Path, builds_root: Path, write: bool) -> dict:
    """Give every released capsule that lacks one the pruned crate of the build it came from.

    For a collection promoted before crates were kept.  A build capsule is the
    source only if every file the released capsule holds, other than the two
    documents promotion rewrites, is byte-identical in it; a capsule with no such
    build, or with identical builds that disagree on the crate, is reported and left
    alone.  The ``_cq`` suffix of a build directory is ignored when matching slugs.
    """
    collection_dir, builds_root = Path(collection_dir), Path(builds_root)
    by_slug: dict[str, list[Path]] = {}
    for build in sorted(builds_root.iterdir()):
        if build.is_dir() and (build / "capsules").is_dir():
            for slug in {slug_from_build(build.name), re.sub(r"_cq$", "", slug_from_build(build.name))}:
                by_slug.setdefault(slug, []).append(build)

    report: dict[str, list[str]] = {"imported": [], "present": [], "unmatched": [], "ambiguous": []}
    for capsule in released_capsules(collection_dir):
        rel = str(capsule.relative_to(collection_dir))
        if (capsule / CRATE).is_file():
            report["present"].append(rel)
            continue
        shipped = [
            f.relative_to(capsule)
            for f in capsule.rglob("*")
            if f.is_file() and f.relative_to(capsule).as_posix() not in REWRITTEN_BY_PROMOTION
        ]
        sources = []
        for build in by_slug.get(capsule.parent.name, []):
            candidate = build / "capsules" / capsule.name
            if not (candidate / CRATE).is_file():
                continue
            if all(
                (candidate / f).is_file() and _digest(candidate / f) == _digest(capsule / f)
                for f in shipped
            ):
                sources.append(candidate / CRATE)
        crates = {_digest(p) for p in sources}
        if not crates:
            report["unmatched"].append(rel)
            continue
        if len(crates) > 1:
            report["ambiguous"].append(rel)
            continue
        if write:
            pruned = prune_crate(json.loads(sources[0].read_text(encoding="utf-8")), capsule)
            (capsule / CRATE).write_text(_dump_crate(pruned), encoding="utf-8")
        report["imported"].append(rel)
    return report


def align_collection(collection_dir: Path, write: bool) -> dict:
    """Apply the rules across one collection.  Returns what was (or would be) changed."""
    collection_dir = Path(collection_dir)
    cards: list[str] = []
    capsules: list[str] = []
    crates: list[str] = []

    # The crate first: a crate that is new to the capsule is one of the files the
    # provenance manifest's `contents` has to list.
    for capsule in released_capsules(collection_dir):
        path = capsule / CRATE
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if _dump_crate(prune_crate(json.loads(text), capsule)) != text:
            if write:
                write_capsule_crate(capsule)
            crates.append(str(capsule.relative_to(collection_dir)))

    for card in sorted((collection_dir / "benchmark" / "cards").rglob("task_*.md")):
        if BUILD_CARD_FOOTER_RE.search(card.read_text(encoding="utf-8")):
            if write:
                if retarget_card(card, collection_dir):
                    cards.append(str(card.relative_to(collection_dir)))
            else:
                cards.append(str(card.relative_to(collection_dir)))

    capdir = collection_dir / "capsules"
    if capdir.is_dir():
        for manifest in sorted(capdir.rglob("*/*/artifact_provenance.json")):
            capsule = manifest.parent
            current = json.loads(manifest.read_text(encoding="utf-8"))
            aligned = align_capsule_provenance(current, capsule)
            if aligned != current:
                if write:
                    write_capsule_provenance(capsule)
                capsules.append(str(capsule.relative_to(collection_dir)))

    return {"cards": cards, "capsules": capsules, "crates": crates}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("collection", type=Path, nargs="+", help="collection directory")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report without writing")
    mode.add_argument("--write", action="store_true", help="align in place")
    parser.add_argument(
        "--import-crates-from",
        type=Path,
        metavar="BUILDS_ROOT",
        help="first give each capsule without a crate the pruned crate of its build",
    )
    args = parser.parse_args(argv)

    pending = 0
    for coll in args.collection:
        if args.import_crates_from:
            imported = import_build_crates(coll, args.import_crates_from, write=args.write)
            verb = "imported" if args.write else "would import"
            print(
                f"{coll}: {verb} {len(imported['imported'])} crate(s); "
                f"{len(imported['present'])} already present, "
                f"{len(imported['unmatched'])} without a matching build, "
                f"{len(imported['ambiguous'])} ambiguous"
            )
            for p in imported["unmatched"][:5] + imported["ambiguous"][:5]:
                print(f"    {p}")
            pending += len(imported["unmatched"]) + len(imported["ambiguous"])
        found = align_collection(coll, write=args.write)
        n = len(found["cards"]) + len(found["capsules"]) + len(found["crates"])
        verb = "aligned" if args.write else "would change"
        print(
            f"{coll}: {verb} {len(found['cards'])} card(s), "
            f"{len(found['capsules'])} capsule manifest(s) and {len(found['crates'])} crate(s)"
        )
        for p in found["cards"][:5] + found["capsules"][:5] + found["crates"][:5]:
            print(f"    {p}")
        if not args.write:
            pending += n
    if pending:
        print(
            f"\n{pending} promoted document(s) still describe the build rather than the "
            "release, or have no build to come from; see above"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
