"""Classify what kind of thing each tools_index entry is: software, a vendor
product, or an extraction artefact.

The catalogue is built by extraction from papers, so it holds more than software.
Before this, all of it shared one `unknown` licence tier, and the count read as
outstanding lookup work when a large part of it is not: an instrument has no SPDX
licence to find, and a dotted module path is not a tool at all.

Every term this dispatches on lives in governance/tool_entry_kinds.yaml. Nothing
here names a vendor, a product or a tool.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

import yaml
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))


_VOCABULARY = pathlib.Path(__file__).resolve().parent.parent / "governance" / "tool_entry_kinds.yaml"

KIND_SOFTWARE = "software"
KIND_VENDOR = "vendor_product"
KIND_ARTEFACT = "artefact"


def load_vocabulary(path=None) -> dict:
    """The entry-kind vocabulary from governance/tool_entry_kinds.yaml."""
    return yaml.safe_load(pathlib.Path(path or _VOCABULARY).read_text(encoding="utf-8")) or {}


def _whole_word(term: str) -> re.Pattern:
    """A term bounded by string edges or separators, never mid-token.

    `thermo` must match `Thermo Xcalibur` and miss `ThermoRawFileParser`, which is
    Apache-2.0 open source. `\\b` is not enough: it treats `ThermoRaw` as a boundary.
    """
    return re.compile(rf"(?:^|[\s\-_/(,]){re.escape(term)}(?:[\s\-_/),.]|$)", re.I)


def vendor_match(name, vocabulary) -> str | None:
    """The vendor term, instrument term or product name this entry carries."""
    for key in ("vendors", "instrument_terms", "proprietary_products"):
        for term in vocabulary.get(key) or []:
            if _whole_word(term).search(name or ""):
                return term
    return None


# A trailing gloss: `PALS (Pathway Activity Level Scoring)`. Requires content, so
# `mzExacto()` -- a function call copied out of a code block -- is left intact.
_TRAILING_GLOSS = re.compile(r"\s*\([^)]+\)\s*$")


def without_gloss(name) -> str:
    """The entry name with a trailing parenthetical removed.

    A name followed by its expansion is a name, not a sentence fragment. Without
    this, the word-count rule reads `PALS (Pathway Activity Level Scoring)` and
    `COBRApy (for optGpSampler uniform sampling)` as prose and files two real tools
    as extraction defects.
    """
    return _TRAILING_GLOSS.sub("", (name or "").strip()).strip()


def artefact_match(name, vocabulary) -> str | None:
    """The id of the artefact shape this entry has, or None."""
    stripped = without_gloss(name)
    for shape in vocabulary.get("artefact_shapes") or []:
        if re.search(shape["pattern"], stripped):
            return shape["id"]
    return None


def classify(tool, vocabulary) -> tuple:
    """``(kind, reason)`` for one tools_index entry.

    A vendor product is decided before an artefact shape, because a full
    instrument name is a legitimate entry that also reads as a long phrase --
    `Agilent 6550 iFunnel Q-TOF mass spectrometer` is five words and a real machine.
    """
    name = tool.get("name") or ""
    vendor = vendor_match(name, vocabulary)
    if vendor:
        return KIND_VENDOR, vendor
    artefact = artefact_match(name, vocabulary)
    if artefact:
        return KIND_ARTEFACT, artefact
    return KIND_SOFTWARE, None


def classify_all(tools, vocabulary=None) -> dict:
    """``{slug: {kind, reason}}`` for every entry."""
    vocabulary = vocabulary if vocabulary is not None else load_vocabulary()
    out = {}
    for tool in tools:
        kind, reason = classify(tool, vocabulary)
        out[tool["slug"]] = {"kind": kind, "reason": reason}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collection", required=True, help="collection dir with tools_index.json")
    args = ap.parse_args(argv)
    tools = json.loads(
        (pathlib.Path(args.collection) / "tools_index.json").read_text(encoding="utf-8"))
    classified = classify_all(tools)
    counts: dict[str, int] = {}
    for record in classified.values():
        counts[record["kind"]] = counts.get(record["kind"], 0) + 1
    print(json.dumps({"tools": len(tools), "kinds": dict(sorted(counts.items()))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
