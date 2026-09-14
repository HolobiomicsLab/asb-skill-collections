"""A receipt has to verify where the release is read, not only where it was written.

The gate binds the tree it finds on disk. Anything a local run leaves behind is
therefore bound as if the release shipped it, and the receipt then fails for
every reader who does not have that file. The case measured here is the one
that reached `collections/metabolomics/v2`: two `__pycache__` entries written
by running the collection's own `bin/` scripts, ignored by the repository and
absent from every checkout and deposition.
"""

import json

import pytest
import yaml

from scripts import release_gate, release_receipt


def _collection(root):
    """A minimal strict-verifiable collection: one paper, one grounded leaf."""
    root.mkdir(parents=True)
    doi = "10.0000/synthetic-receipt"
    (root / "corpus.yaml").write_text(yaml.safe_dump(
        {"papers": [{"doi": doi, "status": "included", "access": {"type": "gold-oa"}}]}))
    leaf = root / "leaves" / "synthetic-operation" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text("---\n" + yaml.safe_dump({
        "name": "synthetic-operation",
        "license": "CC-BY-4.0",
        "derived_from": [{"doi": doi}],
        "evidence_spans": [{"doi": doi, "text": "Synthetic evidence."}],
    }) + "---\n# Procedure\n")
    return root


def _cache(root, *, parts=("bin",)):
    """Write a bytecode cache where running a shipped script would put one."""
    cache = root.joinpath(*parts, "__pycache__")
    cache.mkdir()
    (cache / "search_skills.cpython-311.pyc").write_bytes(b"\xcb\r\r\n compiled")
    return cache


@pytest.mark.parametrize("parts", [("bin",), (), ("bin", "nested")])
def test_a_bytecode_cache_is_never_part_of_what_the_receipt_binds(tmp_path, parts):
    collection = _collection(tmp_path / "collection")
    (collection / "bin").mkdir()
    (collection / "bin" / "search_skills.py").write_text("print('search')\n")
    collection.joinpath(*parts).mkdir(parents=True, exist_ok=True)
    clean = release_receipt.capture_target(collection, collection / "gate_report.json")

    _cache(collection, parts=parts)
    bound = release_receipt.capture_target(collection, collection / "gate_report.json")

    assert not [entry for entry in bound["payload"]["entries"]
                if "__pycache__" in entry["path"]]
    assert bound["payload"] == clean["payload"], (
        "A cache left by a local run must not change the payload digest.")


def test_a_receipt_written_beside_a_cache_reverifies_where_the_cache_is_absent(tmp_path):
    collection = _collection(tmp_path / "collection")
    (collection / "bin").mkdir()
    (collection / "bin" / "search_skills.py").write_text("print('search')\n")
    cache = _cache(collection)

    assert release_gate.main([str(collection), "--strict", "--quiet"]) == 0
    receipt = json.loads((collection / "gate_report.json").read_text())

    for path in sorted(cache.iterdir()):
        path.unlink()
    cache.rmdir()

    assert release_gate.main([str(collection), "--verify", "--quiet"]) == 0, (
        "The consumer's tree is the release; the generating machine's cache is not.")
    assert json.loads((collection / "gate_report.json").read_text()) == receipt, (
        "--verify must not rewrite the receipt it checks.")


def test_a_real_file_whose_own_name_resembles_a_cache_is_still_bound(tmp_path):
    collection = _collection(tmp_path / "collection")
    (collection / "__pycache__.md").write_text("Not a cache directory.\n")

    bound = release_receipt.capture_target(collection, collection / "gate_report.json")

    assert any(entry["path"] == "__pycache__.md" for entry in bound["payload"]["entries"])
