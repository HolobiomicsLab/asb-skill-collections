#!/usr/bin/env python
"""Make a promoted capsule's own documents describe the capsule the release ships.

The promotion step deliberately ships a *slim* capsule
(``promote_benchmark_layer._CAPSULE_KEEP``): ledger, evaluation, evidence, inputs
and the provenance manifest.  Two documents inside that capsule were written
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

Usage:
  release_capsule_truth.py --check collections/metabolomics/v1
  release_capsule_truth.py --write collections/metabolomics/v1
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

__all__ = [
    "BUILD_CARD_FOOTER_RE",
    "align_capsule_provenance",
    "capsule_for_card",
    "card_footer",
    "align_collection",
]

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


def align_collection(collection_dir: Path, write: bool) -> dict:
    """Apply both rules across one collection.  Returns what was (or would be) changed."""
    collection_dir = Path(collection_dir)
    cards: list[str] = []
    capsules: list[str] = []

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

    return {"cards": cards, "capsules": capsules}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("collection", type=Path, nargs="+", help="collection directory")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report without writing")
    mode.add_argument("--write", action="store_true", help="align in place")
    args = parser.parse_args(argv)

    pending = 0
    for coll in args.collection:
        found = align_collection(coll, write=args.write)
        n = len(found["cards"]) + len(found["capsules"])
        verb = "aligned" if args.write else "would change"
        print(
            f"{coll}: {verb} {len(found['cards'])} card(s) and "
            f"{len(found['capsules'])} capsule manifest(s)"
        )
        for p in found["cards"][:5] + found["capsules"][:5]:
            print(f"    {p}")
        if not args.write:
            pending += n
    if pending:
        print(
            f"\n{pending} promoted document(s) still describe the build rather than the "
            "release; run with --write"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
