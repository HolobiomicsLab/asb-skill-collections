#!/usr/bin/env python3
"""Build docs-site/edam_topic_labels.json from scripts/data/edam_labels.json.

The site shows EDAM topics by label. This writes the EDAM version, the source
and licence line, and an ``id -> label`` map of every topic term (``topic_NNNN``),
sorted, so two runs give the same bytes. Standard library only.

    python3 docs-site/build_edam_topic_labels.py            # write the file
    python3 docs-site/build_edam_topic_labels.py --check    # exit 1 if it differs

``--check`` also reads the domain files of ``docs-site/search_index/`` and fails
when a topic used there has no label, naming the ids.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
REPO = SITE.parent
SOURCE = REPO / "scripts" / "data" / "edam_labels.json"
OUTPUT = SITE / "edam_topic_labels.json"
INDEX_DIR = SITE / "search_index"
IRI_PREFIX = "http://edamontology.org/"


def build(source: Path = SOURCE) -> str:
    data = json.loads(source.read_text(encoding="utf-8"))
    labels = {
        term_id: term["label"]
        for term_id, term in data["terms"].items()
        if term_id.startswith("topic_") and term.get("label")
    }
    payload = {
        "edam_version": data["edam_version"],
        "source": f"EDAM {data['edam_version']} ({IRI_PREFIX}), via scripts/data/edam_labels.json",
        "license": data["license"],
        "labels": dict(sorted(labels.items())),
    }
    return json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=False) + "\n"


def index_topic_ids(index_dir: Path = INDEX_DIR) -> set[str]:
    """Every topic id that a row of a domain file of the search index carries."""
    manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
    ids: set[str] = set()
    for entry in manifest["domains"].values():
        payload = json.loads((index_dir / entry["file"]).read_text(encoding="utf-8"))
        for key in ("skills", "workflows", "tools", "papers"):
            for row in payload.get(key, []):
                for iri in row.get("edam_topics") or []:
                    ids.add(iri.rsplit("/", 1)[-1])
    return ids


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="compare with the committed file and the index; write nothing")
    args = parser.parse_args(argv)
    text = build()
    if not args.check:
        OUTPUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUTPUT.relative_to(REPO)}")
        return 0
    failures = []
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != text:
        failures.append(f"{OUTPUT.relative_to(REPO)} differs from what {Path(__file__).name} generates: rerun it")
    labels = json.loads(text)["labels"]
    if (INDEX_DIR / "manifest.json").is_file():
        missing = sorted(i for i in index_topic_ids() if i not in labels)
        if missing:
            failures.append("topics in the search index without a label: " + ", ".join(missing))
    for line in failures:
        print(f"FAIL: {line}", file=sys.stderr)
    if not failures:
        print(f"OK: {OUTPUT.relative_to(REPO)} is current ({len(labels)} topic labels)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
