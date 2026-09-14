"""A promoted capsule's own documents must describe the capsule, not the build.

§8 removed `ro_crate_path` from the four manifests because it named a file the
release does not ship.  The same claim survived one layer down, in the two
documents a consumer actually opens:

* 417 benchmark cards ended with "See the `ro-crate-metadata.json` in this capsule
  for full provenance" — no released capsule contains that file;
* the 417 `artifact_provenance.json` files promoted with them listed 2,085 artefact
  paths, of which **0** existed in the released capsule.

`scripts/release_capsule_truth.py` holds the one rule that fixes both, and
`scripts/promote_benchmark_layer.py` applies it while promoting.  This file holds
each half: the tree is aligned, and the generator will not undo it.
"""
import json
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from release_capsule_truth import align_collection  # noqa: E402

COLLECTIONS = sorted(p.parent for p in (ROOT / "collections").glob("*/*/collection.yaml"))
CARDS = sorted((ROOT / "collections").rglob("benchmark/cards/*/task_*.md"))
MANIFESTS = sorted((ROOT / "collections").rglob("capsules/*/*/artifact_provenance.json"))

_FOOTER_LINK = re.compile(r"\[`artifact_provenance\.json`\]\(([^)]+)\)")


def test_the_measurement_this_file_rests_on_is_not_empty():
    """Guard the premise: these assertions are vacuous if nothing is collected."""
    assert COLLECTIONS, "no collection found"
    assert len(CARDS) == 417, f"expected the 417 promoted cards, collected {len(CARDS)}"
    assert len(MANIFESTS) == 417, f"expected 417 capsule manifests, collected {len(MANIFESTS)}"


@pytest.mark.parametrize("card", CARDS, ids=lambda p: str(p.relative_to(ROOT)))
def test_no_card_points_at_a_file_the_release_does_not_ship(card):
    text = card.read_text(encoding="utf-8")
    assert "ro-crate-metadata.json" not in text, (
        "a promoted card still tells the reader to open the build's RO-Crate; "
        "no released capsule contains one"
    )
    m = _FOOTER_LINK.search(text)
    assert m, "the card footer must name the provenance file this release does carry"
    target = (card.parent / m.group(1)).resolve()
    assert target.is_file(), f"the card's footer link does not resolve: {m.group(1)}"


@pytest.mark.parametrize("manifest", MANIFESTS, ids=lambda p: str(p.relative_to(ROOT)))
def test_capsule_manifest_describes_the_capsule_that_ships(manifest):
    capsule = manifest.parent
    d = json.loads(manifest.read_text(encoding="utf-8"))

    for key in ("schema_version", "task_id", "paper_doi", "generated_at", "artifacts"):
        assert key in d, f"missing required key {key}"

    for entry in d["artifacts"]:
        path = str(entry.get("path", "")).split("#", 1)[0]
        assert (capsule / path).exists(), (
            f"dangling path {path!r}: the manifest claims an artefact the released "
            "capsule does not carry"
        )

    release = d.get("release")
    assert release, "a promoted capsule must say it is the slim subset it is"
    real = sorted(
        str(f.relative_to(capsule).as_posix()) for f in capsule.rglob("*") if f.is_file()
    )
    assert release["contents"] == real, "the declared contents are not the capsule's files"
    assert release["omitted_from_release"], (
        "the release must record what the build produced and it does not promote, "
        "rather than silently dropping it"
    )


@pytest.mark.parametrize("collection", COLLECTIONS, ids=lambda p: p.name and str(p))
def test_the_rule_is_a_fixed_point_on_the_shipped_tree(collection):
    """`--check` is the gate form; it must report nothing to do on the release."""
    found = align_collection(collection, write=False)
    assert not found["cards"] and not found["capsules"], (
        f"{collection} still holds documents written against the build: {found}"
    )


def test_the_promotion_step_applies_the_rule():
    """Aligning the tree is undone by the next promotion unless promotion does it too.

    This is §8's lesson: fixing the artefacts without fixing the generator leaves the
    defect one run away from coming back.
    """
    src = (ROOT / "scripts" / "promote_benchmark_layer.py").read_text(encoding="utf-8")
    assert "from release_capsule_truth import align_collection" in src
    assert "align_collection(collection_dir, write=True)" in src


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
