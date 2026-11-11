"""Deterministic EDAM facets are valid slug-list selections."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from asb_skill_collections.asbb import subset
from scripts import build_facets

FIXTURE = Path(__file__).parent / "fixtures" / "router_collection"
V3 = (
    Path(os.environ.get("ASB_METABOLOMICS_CHECKOUT", ""))
    / "collections"
    / "metabolomics"
    / "v3"
)
LABELS = Path(__file__).parent.parent / "scripts" / "data" / "edam_labels.json"


def generate(collection: Path, output: Path, threshold: int = 2) -> dict:
    """Generate facets without depending on the command-line wrapper."""
    return build_facets.run(
        collection=collection,
        out=output,
        threshold=threshold,
        kind="topics",
        labels=LABELS,
    )


def test_label_refresh_records_release_provenance(tmp_path: Path) -> None:
    source = tmp_path / "EDAM.csv"
    source.write_text(
        "Class ID,Preferred Label,Synonyms,Parents,Created in\n"
        "http://edamontology.org/topic_0001,One,First|1st,,1.24\n"
        "http://edamontology.org/operation_0002,Two,Second,http://edamontology.org/operation_0001,1.25\n"
        "http://edamontology.org/data_0003,Three,Third,,1.25\n",
        encoding="utf-8",
    )

    table = build_facets.derive_labels(source, tmp_path / "labels.json", "2026-11-08")

    assert table["edam_version"] == "1.25"
    assert table["source_file"] == "EDAM.csv"
    assert table["generated"] == "2026-11-08"
    assert table["license"] == "CC-BY-SA-4.0"
    assert table["terms"] == {
        "operation_0002": {
            "id": "operation_0002",
            "label": "Two",
            "synonyms": ["Second"],
            "parents": ["operation_0001"],
        },
        "topic_0001": {
            "id": "topic_0001",
            "label": "One",
            "synonyms": ["First", "1st"],
            "parents": [],
        },
    }


def test_fixture_is_deterministic_and_counts_recompute(tmp_path: Path) -> None:
    first = generate(FIXTURE, tmp_path / "first")
    second = generate(FIXTURE, tmp_path / "second")

    assert [facet["id"] for facet in first["facets"]] == ["topic_3172"]
    assert first["facets"][0]["label"] == "Metabolomics"
    assert first["facets"][0]["count"] == 3
    assert first["facets"][0]["overlaps"] == {}
    assert first["covered"] == 3
    assert first["uncovered"] == {"no_topic": 7, "under_threshold": 0, "total": 7}
    assert first == second
    assert (tmp_path / "first/topics/topic_3172.txt").read_bytes() == (
        tmp_path / "second/topics/topic_3172.txt"
    ).read_bytes()


def test_overlap_is_symmetric_and_uncovered_closes_the_union(tmp_path: Path) -> None:
    rows = [
        {"slug": "alpha", "edam_topics": ["topic_0001", "topic_0002"]},
        {"slug": "beta", "edam_topics": ["topic_0001", "topic_0002"]},
        {"slug": "gamma", "edam_topics": ["topic_0001"]},
        {"slug": "delta", "edam_topics": []},
        {"slug": "epsilon", "edam_topics": ["topic_0003"]},
    ]
    collection = tmp_path / "collection"
    collection.mkdir()
    (collection / "skills_index.json").write_text(json.dumps(rows), encoding="utf-8")

    result = generate(collection, tmp_path / "facets")
    facets = {facet["id"]: facet for facet in result["facets"]}

    assert facets["topic_0001"]["overlaps"] == {"topic_0002": 2}
    assert facets["topic_0002"]["overlaps"] == {"topic_0001": 2}
    lists = {
        facet["id"]: set(
            subset.read_slugs_file(tmp_path / "facets/topics" / f"{facet['id']}.txt")
        )
        for facet in result["facets"]
    }
    for identifier, facet in facets.items():
        assert facet["count"] == len(lists[identifier])
        for other, overlap in facet["overlaps"].items():
            assert overlap == len(lists[identifier] & lists[other])
            assert facets[other]["overlaps"][identifier] == overlap
    assert result["covered"] == len(set().union(*lists.values()))
    assert result["covered"] + result["uncovered"]["total"] == len(rows)
    assert result["uncovered"] == {"no_topic": 1, "under_threshold": 1, "total": 2}


def test_changed_source_refuses_without_force(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    collection = tmp_path / "collection"
    collection.mkdir()
    index = collection / "skills_index.json"
    index.write_text(json.dumps([{"slug": "alpha", "edam_topics": ["topic_0001"]}]))
    generate(collection, tmp_path / "facets", threshold=1)
    original = (tmp_path / "facets/topics/topic_0001.txt").read_bytes()
    index.write_text(json.dumps([{"slug": "beta", "edam_topics": ["topic_0001"]}]))

    with pytest.raises(build_facets.SourceDigestMismatch) as error:
        generate(collection, tmp_path / "facets", threshold=1)

    message = str(error.value)
    assert "source digest changed" in message
    assert "expected" in message and "actual" in message
    assert "--force" in message
    assert (tmp_path / "facets/topics/topic_0001.txt").read_bytes() == original
    forced = build_facets.run(
        collection=collection,
        out=tmp_path / "facets",
        threshold=1,
        kind="topics",
        labels=LABELS,
        force=True,
    )
    assert forced["facets"][0]["count"] == 1
    assert subset.read_slugs_file(tmp_path / "facets/topics/topic_0001.txt") == ["beta"]
    assert capsys.readouterr().out.count("topic_0001") == 2


def test_operations_are_opt_in(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    collection = tmp_path / "collection"
    collection.mkdir()
    rows = json.loads((FIXTURE / "skills_index.json").read_text())
    for row in rows:
        row["edam_operation"] = row["edam_topics"][0]
        row["edam_topics"] = []
    (collection / "skills_index.json").write_text(json.dumps(rows), encoding="utf-8")

    result = build_facets.run(
        collection=collection,
        out=tmp_path / "operations",
        threshold=2,
        kind="operations",
        labels=LABELS,
    )

    assert result["kind"] == "operations"
    assert result["facet_count"] == 2
    assert result["covered"] == 6
    assert result["uncovered"] == {"no_operation": 3, "under_threshold": 1, "total": 4}
    assert (tmp_path / "operations/operations/operation_3629.txt").is_file()
    assert capsys.readouterr().out.count("operation_") == 2


def test_cli_defaults_to_topics_and_dry_run(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    status = build_facets.main(
        [
            "--collection",
            str(FIXTURE),
            "--out",
            str(tmp_path / "facets"),
            "--threshold",
            "2",
            "--dry-run",
        ]
    )

    assert status == 0
    assert "topic_3172" in capsys.readouterr().out
    assert not (tmp_path / "facets").exists()


def test_dry_run_prints_without_writing(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    result = build_facets.run(
        collection=FIXTURE,
        out=tmp_path / "facets",
        threshold=2,
        kind="topics",
        labels=LABELS,
        dry_run=True,
    )

    assert result["facet_count"] == 1
    assert "topic_3172" in capsys.readouterr().out
    assert not (tmp_path / "facets").exists()


def test_fixture_lists_use_the_asbb_parser_and_unknown_slugs_are_refused(
    tmp_path: Path,
) -> None:
    generate(FIXTURE, tmp_path / "facets")
    rows = json.loads((FIXTURE / "skills_index.json").read_text())
    path = tmp_path / "facets/topics/topic_3172.txt"

    slugs = subset.read_slugs_file(path)

    assert slugs == sorted(set(slugs))
    assert subset.check_slugs(slugs, rows) == slugs
    with pytest.raises(subset.SelectionError, match="not in the collection index"):
        subset.check_slugs(["not-a-fixture-skill"], rows)


@pytest.mark.skipif(not (V3 / "skills_index.json").is_file(), reason="local v3 collection is unavailable")
def test_every_real_facet_passes_the_asbb_slug_file_parser(tmp_path: Path) -> None:
    generate(V3, tmp_path / "facets", threshold=50)
    rows = json.loads((V3 / "skills_index.json").read_text())

    for path in sorted((tmp_path / "facets/topics").glob("*.txt")):
        slugs = subset.read_slugs_file(path)
        assert subset.check_slugs(slugs, rows) == slugs


@pytest.mark.skipif(not (V3 / "skills_index.json").is_file(), reason="local v3 collection is unavailable")
def test_real_v3_acceptance_counts(tmp_path: Path) -> None:
    result = generate(V3, tmp_path / "facets", threshold=50)

    assert result["facet_count"] == 40
    assert result["covered"] == 10526
    assert result["uncovered"] == {
        "no_topic": 903,
        "under_threshold": 401,
        "total": 1304,
    }
    assert result["collection"]["version"] == 3
    assert result["edam_version"] == "1.25"
    assert (
        result["source_digest"]
        == hashlib.sha256((V3 / "skills_index.json").read_bytes()).hexdigest()
    )
    proteomics = next(
        facet for facet in result["facets"] if facet["id"] == "topic_3520"
    )
    assert proteomics["label"] == "Proteomics experiment"
    assert "Mass spectrometry" in proteomics["synonyms"]


def test_index_records_no_local_path(tmp_path: Path) -> None:
    released = tmp_path / "checkout/collections/metabolomics/v3"
    assert build_facets.collection_label(released) == "collections/metabolomics/v3"
    assert build_facets.collection_label(tmp_path / "candidate") == "candidate"
    index = generate(FIXTURE, tmp_path / "facets")
    assert not Path(index["collection"]["path"]).is_absolute()
