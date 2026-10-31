"""Guards for the static site under docs-site/, which Pages serves as is.

The site went unserved for months, so its defects were never seen: it listed
three staged collections as released with a DOI of "TODO-zenodo". These
checks hold the committed pages to what the site promises once Pages is
enabled.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib

from scripts.regen_catalogue import collection_status, released_collection_dirs

REPO = pathlib.Path(__file__).resolve().parent.parent
SITE = REPO / "docs-site"


def _build_search_index():
    spec = importlib.util.spec_from_file_location(
        "build_search_index", SITE / "build_search_index.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- #
# Release status (staged collections are labelled, not shown as released)     #
# --------------------------------------------------------------------------- #
def test_indexer_status_follows_the_marketplace():
    released = released_collection_dirs(REPO)
    labels = [p.parent.relative_to(REPO / "collections").as_posix()
              for p in sorted((REPO / "collections").glob("*/v*/collection.yaml"))]
    statuses = _build_search_index().collection_statuses(labels)
    assert statuses == {label: collection_status(f"collections/{label}", released) for label in labels}


def test_committed_search_index_labels_every_collection():
    index = json.loads((SITE / "search_index.json").read_text(encoding="utf-8"))
    released = released_collection_dirs(REPO)
    status = index.get("collection_status")
    assert isinstance(status, dict), "search_index.json has no collection_status: rebuild it"
    assert set(status) == set(index["collections"])
    for label, value in status.items():
        assert value == collection_status(f"collections/{label}", released), label
