"""A released capsule's RO-Crate describes the capsule the release ships, and nothing else.

The build writes one crate per capsule; promotion used to drop it, and the card
footer kept naming it (§8b of the decision annex). Shipping it verbatim would have
been worse than dropping it: measured over the 417 released capsules, the build
crates describe 18,097 files the slim capsule does not hold, point
`repme:buildManifestRef` outside the capsule, carry 12,425 absolute paths of the
build machine in `oa:source`, and claim the Workflow Run Crate 0.5 profile without
the `mainEntity` workflow that profile requires.

`scripts/release_capsule_truth.py` holds the rule (`prune_crate`) and the check
(`crate_problems`, which gate 8 runs); `promote_benchmark_layer.py` keeps the crate
and applies the rule while promoting. This file holds the shipped tree to the check,
the rule to each of its halves, the one-time import to its identity guard, and the
promoter to keeping the crate.
"""
import copy
import json
import pathlib
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from release_capsule_truth import (  # noqa: E402
    CRATE,
    align_collection,
    crate_problems,
    import_build_crates,
    prune_crate,
    released_capsules,
)

COLLECTIONS = sorted(p.parent for p in (ROOT / "collections").glob("*/*/collection.yaml"))
CAPSULES = [c for coll in COLLECTIONS for c in released_capsules(coll)]
RUN_PROFILE = "https://w3id.org/ro/wfrun/workflow/0.5"


# -- the shipped tree ------------------------------------------------------------


def test_the_measurement_this_file_rests_on_is_not_empty():
    assert len(CAPSULES) == 417, f"expected the 417 released capsules, collected {len(CAPSULES)}"


@pytest.mark.parametrize("capsule", CAPSULES, ids=lambda p: str(p.relative_to(ROOT)))
def test_each_shipped_crate_has_no_problem(capsule):
    assert crate_problems(capsule) == []


@pytest.mark.parametrize("collection", COLLECTIONS, ids=str)
def test_the_crate_rule_is_a_fixed_point_on_the_shipped_tree(collection):
    assert align_collection(collection, write=False)["crates"] == []


def test_the_provenance_manifest_lists_the_crate_it_ships_beside():
    for capsule in CAPSULES:
        manifest = json.loads((capsule / "artifact_provenance.json").read_text(encoding="utf-8"))
        assert CRATE in manifest["release"]["contents"], capsule


# -- the rule, on a synthetic capsule --------------------------------------------


def _build_crate():
    return {
        "@context": ["https://w3id.org/ro/crate/1.1/context", {"oa": "http://www.w3.org/ns/oa#"}],
        "@graph": [
            {
                "@id": CRATE,
                "@type": "CreativeWork",
                "about": {"@id": "./"},
                "conformsTo": [{"@id": "https://w3id.org/ro/crate/1.1"}, {"@id": RUN_PROFILE}],
            },
            {
                "@id": "./",
                "@type": ["Dataset"],
                "hasPart": [{"@id": "evidence/source_snippets.md"}, {"@id": "logs/run.md"}],
                "mentions": [{"@id": "#env"}],
            },
            {"@id": "evidence/source_snippets.md", "@type": "File", "name": "evidence/source_snippets.md"},
            {"@id": "logs/run.md", "@type": "File", "name": "logs/run.md"},
            {"@id": "#env", "@type": "repme:ComputationalEnvironment",
             "repme:buildManifestRef": {"@id": "../../build_manifest.json"}, "repme:buildId": "B1"},
            {
                "@id": "urn:asb:claim:claim_001",
                "@type": ["oa:Annotation"],
                "oa:target": {
                    "@type": "oa:SpecificResource",
                    "oa:source": "/Users/someone/git/ASB/outputs/asbb_pilot/coll_tool/synthesized_package",
                },
                "schema:name": "A claim quoting a rate of 3 /min",
            },
            {"@id": "urn:asb:claim:claim_002", "@type": ["oa:Annotation"],
             "oa:target": {"oa:source": "/scratch/job/elsewhere/package"}},
        ],
    }


@pytest.fixture
def capsule(tmp_path):
    root = tmp_path / "capsules" / "tool" / "task_001"
    (root / "evidence").mkdir(parents=True)
    (root / "evidence" / "source_snippets.md").write_text("evidence\n")
    (root / "ledger").mkdir()
    (root / "ledger" / "claims.jsonl").write_text("{}\n")
    (root / "artifact_provenance.json").write_text("{}\n")
    return root


def _by_id(crate):
    return {e["@id"]: e for e in crate["@graph"]}


def test_a_file_the_capsule_does_not_hold_is_dropped_with_its_references(capsule):
    pruned = _by_id(prune_crate(_build_crate(), capsule))
    assert "logs/run.md" not in pruned
    assert {"@id": "logs/run.md"} not in pruned["./"]["hasPart"]
    assert {"@id": "evidence/source_snippets.md"} in pruned["./"]["hasPart"]


def test_a_reference_leaving_the_capsule_is_removed_with_its_property(capsule):
    env = _by_id(prune_crate(_build_crate(), capsule))["#env"]
    assert "repme:buildManifestRef" not in env
    assert env["repme:buildId"] == "B1", "only the dangling reference goes"


def test_a_build_machine_path_names_the_build_not_the_machine(capsule):
    pruned = _by_id(prune_crate(_build_crate(), capsule))
    anchored = pruned["urn:asb:claim:claim_001"]["oa:target"]["oa:source"]
    unanchored = pruned["urn:asb:claim:claim_002"]["oa:target"]["oa:source"]
    assert anchored == "urn:asb:build:asbb_pilot/coll_tool/synthesized_package"
    assert unanchored == "urn:asb:build:package"
    assert pruned["urn:asb:claim:claim_001"]["schema:name"] == "A claim quoting a rate of 3 /min"


def test_every_file_the_capsule_holds_is_described_and_listed(capsule):
    pruned = _by_id(prune_crate(_build_crate(), capsule))
    for rel, encoding in (("ledger/claims.jsonl", "application/jsonlines"),
                          ("artifact_provenance.json", "application/json")):
        assert pruned[rel] == {"@id": rel, "@type": "File", "name": rel, "encodingFormat": encoding}
        assert {"@id": rel} in pruned["./"]["hasPart"]


def test_the_unchecked_run_profile_claim_is_dropped(capsule):
    descriptor = _by_id(prune_crate(_build_crate(), capsule))[CRATE]
    assert descriptor["conformsTo"] == [{"@id": "https://w3id.org/ro/crate/1.1"}]


def test_the_rule_is_idempotent_and_leaves_its_input_alone(capsule):
    original = _build_crate()
    before = copy.deepcopy(original)
    once = prune_crate(original, capsule)
    assert original == before
    assert prune_crate(once, capsule) == once


def test_a_pruned_crate_has_no_problem(capsule):
    (capsule / CRATE).write_text(json.dumps(prune_crate(_build_crate(), capsule)))
    assert crate_problems(capsule) == []


# -- the check, one defect at a time ---------------------------------------------


@pytest.mark.parametrize(
    "mutate, expected",
    [
        (lambda g: g[CRATE]["conformsTo"].append({"@id": RUN_PROFILE}),
         f"the descriptor claims {RUN_PROFILE}, which this gate does not check"),
        (lambda g: g["./"]["hasPart"].append({"@id": "logs/run.md"}),
         "names 'logs/run.md', which the capsule does not hold"),
        (lambda g: g["./"]["hasPart"].remove({"@id": "ledger/claims.jsonl"}),
         "does not list 'ledger/claims.jsonl' in the root's hasPart"),
        (lambda g: g["urn:asb:claim:claim_001"]["oa:target"].update(
            {"oa:source": "/Users/someone/outputs/x/y"}),
         "carries 1 absolute filesystem path(s)"),
        (lambda g: g.pop("./"), "no root Dataset ./"),
    ],
    ids=["run-profile-claim", "dangling-path", "not-in-hasPart", "absolute-path", "no-root"],
)
def test_the_check_names_each_defect(capsule, mutate, expected):
    pruned = prune_crate(_build_crate(), capsule)
    graph = _by_id(pruned)
    mutate(graph)
    pruned["@graph"] = list(graph.values())
    (capsule / CRATE).write_text(json.dumps(pruned))
    assert expected in crate_problems(capsule)


def test_an_undescribed_file_is_named(capsule):
    (capsule / CRATE).write_text(json.dumps(prune_crate(_build_crate(), capsule)))
    (capsule / "evidence" / "late.md").write_text("added after the crate\n")
    assert "does not describe 'evidence/late.md'" in crate_problems(capsule)


def test_a_capsule_without_a_crate_is_named(capsule):
    assert crate_problems(capsule) == [f"no {CRATE}"]


# -- the one-time import ----------------------------------------------------------


def _collection_with_build(tmp_path, build_name="coll_tool"):
    collection = tmp_path / "collection"
    capsule = collection / "capsules" / "tool" / "task_001"
    (capsule / "evidence").mkdir(parents=True)
    (capsule / "evidence" / "source_snippets.md").write_text("evidence\n")
    (capsule / "artifact_provenance.json").write_text('{"rewritten": true}\n')
    build = tmp_path / "builds" / build_name / "capsules" / "task_001"
    (build / "evidence").mkdir(parents=True)
    (build / "evidence" / "source_snippets.md").write_text("evidence\n")
    (build / "artifact_provenance.json").write_text('{"as built": true}\n')
    (build / CRATE).write_text(json.dumps(_build_crate()))
    return collection, tmp_path / "builds", capsule, build


@pytest.mark.parametrize("build_name", ["coll_tool", "coll_tool_cq", "tool_grounded"])
def test_an_identical_build_gives_its_crate_pruned(tmp_path, build_name):
    collection, builds, capsule, _ = _collection_with_build(tmp_path, build_name)
    report = import_build_crates(collection, builds, write=True)
    assert report["imported"] == ["capsules/tool/task_001"]
    assert crate_problems(capsule) == []
    assert import_build_crates(collection, builds, write=True)["present"] == ["capsules/tool/task_001"]


def test_a_build_differing_in_one_shipped_file_is_not_a_source(tmp_path):
    collection, builds, capsule, build = _collection_with_build(tmp_path)
    (build / "evidence" / "source_snippets.md").write_text("evidence, rebuilt\n")
    report = import_build_crates(collection, builds, write=True)
    assert report["unmatched"] == ["capsules/tool/task_001"]
    assert not (capsule / CRATE).exists()


def test_identical_builds_disagreeing_on_the_crate_are_left_alone(tmp_path):
    collection, builds, capsule, build = _collection_with_build(tmp_path)
    twin = builds / "coll_tool_cq" / "capsules" / "task_001"
    twin.parent.mkdir(parents=True)
    import shutil

    shutil.copytree(build, twin)
    other = _build_crate()
    other["@graph"][1]["name"] = "a different crate"
    (twin / CRATE).write_text(json.dumps(other))
    report = import_build_crates(collection, builds, write=True)
    assert report["ambiguous"] == ["capsules/tool/task_001"]
    assert not (capsule / CRATE).exists()


def test_a_dry_run_writes_nothing(tmp_path):
    collection, builds, capsule, _ = _collection_with_build(tmp_path)
    assert import_build_crates(collection, builds, write=False)["imported"] == ["capsules/tool/task_001"]
    assert not (capsule / CRATE).exists()


# -- the promoter ------------------------------------------------------------------


def test_promotion_keeps_the_crate_and_prunes_it(tmp_path):
    import promote_benchmark_layer

    collection = tmp_path / "collections" / "alpha" / "v1"
    collection.mkdir(parents=True)
    (collection / "collection.yaml").write_text(yaml.safe_dump({"slug": "alpha", "version": "1.0.0"}))
    build = tmp_path / "builds" / "coll_tool"
    (build / "build_manifest.json").parent.mkdir(parents=True)
    (build / "build_manifest.json").write_text("{}\n")
    source = build / "capsules" / "task_001"
    for rel in ("evidence/source_snippets.md", "logs/run.md"):
        (source / rel).parent.mkdir(parents=True, exist_ok=True)
        (source / rel).write_text("x\n")
    (source / "artifact_provenance.json").write_text(json.dumps({"artifacts": []}))
    (source / CRATE).write_text(json.dumps(_build_crate()))

    summary = promote_benchmark_layer.promote(collection, tmp_path / "builds", False, False)

    capsule = collection / "capsules" / "tool" / "task_001"
    assert (capsule / CRATE).is_file(), "promotion must keep the crate"
    assert not (capsule / "logs").exists(), "the capsule is still slim"
    assert summary["crates_pruned"] == 1
    assert crate_problems(capsule) == []


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
