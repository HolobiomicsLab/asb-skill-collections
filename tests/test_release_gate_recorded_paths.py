"""A receipt ships inside its collection, so it must not carry the gate machine's paths.

`gate_report.json` recorded `collection_dir` and `corpus_path` as absolute paths.
The four receipts regenerated for the release therefore each carried
`/Users/<account>/git/<worktree>/collections/...`, including the one in
`collections/metabolomics/v2`, the public collection, whose tree on `main` held no
such path before receipts were added. Verification never reads either field
(it recomputes the bindings from the tree), so the absolute form bought nothing
and published the directory layout of whichever machine ran the gate.
"""
import json
import pathlib
import re

import yaml

from scripts import release_gate

ROOT = pathlib.Path(__file__).parent.parent
ABSOLUTE = re.compile(r"(^|[\"'\s])(/Users/|/home/|/private/|/tmp/|/var/folders/|[A-Za-z]:\\\\)")


def _write_collection(collection):
    collection.mkdir(parents=True)
    papers = [{"doi": "10.0000/synthetic-receipt", "status": "included", "access": {"type": "gold-oa"}}]
    (collection / "corpus.yaml").write_text(yaml.safe_dump({"papers": papers}))
    leaf = collection / "leaves" / "synthetic-operation" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    frontmatter = {
        "name": "synthetic-operation",
        "license": "CC-BY-4.0",
        "derived_from": [{"doi": papers[0]["doi"]}],
        "evidence_spans": [{"doi": papers[0]["doi"], "text": "Synthetic evidence."}],
    }
    leaf.write_text("---\n" + yaml.safe_dump(frontmatter) + "---\n# Procedure\n")
    return collection


def test_a_collection_in_a_checkout_is_recorded_relative_to_it(tmp_path):
    checkout = tmp_path / "checkout"
    (checkout / ".git").mkdir(parents=True)
    collection = _write_collection(checkout / "collections" / "synthetic" / "v1")

    release_gate.main([str(collection), "--strict", "--quiet"])
    text = (collection / "gate_report.json").read_text()
    report = json.loads(text)

    assert report["collection_dir"] == "collections/synthetic/v1"
    assert report["corpus_path"] == "collections/synthetic/v1/corpus.yaml"
    assert str(tmp_path.resolve()) not in text
    assert str(tmp_path) not in text


def test_a_worktree_checkout_is_an_anchor_too(tmp_path):
    """A linked worktree has a `.git` file, not a directory."""
    checkout = tmp_path / "worktree"
    checkout.mkdir()
    (checkout / ".git").write_text("gitdir: /elsewhere/.git/worktrees/worktree\n")
    collection = _write_collection(checkout / "collections" / "synthetic" / "v1")

    report = release_gate.run_gate(collection, None, True)

    assert report["collection_dir"] == "collections/synthetic/v1"


def test_outside_a_checkout_the_path_is_recorded_as_given(tmp_path):
    collection = _write_collection(tmp_path / "loose")

    report = release_gate.run_gate(collection, None, True)

    assert report["collection_dir"] == str(collection.resolve())


def test_the_verification_still_passes_on_a_relative_receipt(tmp_path):
    checkout = tmp_path / "checkout"
    (checkout / ".git").mkdir(parents=True)
    collection = _write_collection(checkout / "collections" / "synthetic" / "v1")
    assert release_gate.main([str(collection), "--strict", "--quiet"]) == 0

    assert release_gate.main([str(collection), "--verify", "--quiet"]) == 0


def test_no_shipped_receipt_carries_an_absolute_path():
    receipts = sorted(ROOT.glob("collections/*/v*/gate_report.json"))
    assert receipts, "no receipt found; this test would pass over nothing"
    offenders = {}
    for path in receipts:
        hits = ABSOLUTE.findall(path.read_text(encoding="utf-8"))
        if hits:
            offenders[str(path.relative_to(ROOT))] = len(hits)
    assert not offenders, f"receipts carry absolute paths: {offenders}"
