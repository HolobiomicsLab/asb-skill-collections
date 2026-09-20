"""Contract tests for the S4 build-to-corpus join."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest
import yaml

from scripts import join_corpus_records as join


REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
DEFAULT_ACCESS_MAP = REPO / "scripts" / "access_map_p1.yaml"
DOMAIN = "metabarcoding"
VERSION = "v1"
VERIFIED_ON = "2026-09-18"
CONTROL_DOI = "10.1002/ece3.6594"
NORMALIZED_TEST_DOI = "10.1093/nar/gkab1275"
RECEIPT_KEYS = {
    "schema",
    "stage",
    "domain",
    "inputs",
    "access_map",
    "counts",
    "duplicate_dois",
    "unmatched_rows",
    "capped_rows",
}


def _copy_inputs(tmp_path: Path) -> tuple[Path, Path]:
    """Copy the immutable fixture inputs for one isolated join."""
    fixture = tmp_path / "fixture"
    builds = fixture / "builds"
    tiered = fixture / "metabarcoding_tiered.json"
    shutil.copytree(FIXTURE / "builds", builds)
    shutil.copy2(FIXTURE / "metabarcoding_tiered.json", tiered)
    return builds, tiered


def _arguments(
    builds: Path,
    tiered: Path,
    output: Path,
    *,
    receipts: Path | None = None,
    access_map: Path | None = None,
    domain: str = DOMAIN,
    version: str = VERSION,
    verified_on: str = VERIFIED_ON,
    dry_run: bool = False,
) -> list[str]:
    """Build the public CLI arguments for one test invocation."""
    result = [
        "--builds",
        str(builds),
        "--tiered",
        str(tiered),
        "--domain",
        domain,
        "--version",
        version,
        "--out",
        str(output),
        "--verified-on",
        verified_on,
    ]
    if receipts is not None:
        result.extend(("--receipts", str(receipts)))
    if access_map is not None:
        result.extend(("--access-map", str(access_map)))
    if dry_run:
        result.append("--dry-run")
    return result


def _read_json(path: Path) -> object:
    """Read one JSON test input or receipt."""
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: object) -> None:
    """Write one JSON fixture-copy input deterministically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _tier_rows(path: Path) -> list[dict]:
    """Load the copied tier inventory as mutable rows."""
    rows = _read_json(path)
    assert isinstance(rows, list)
    return rows


def _add_build(
    builds: Path,
    name: str,
    doi: str,
    *,
    repository: str = "example/project",
    enrichment_doi: str | None = None,
    title: str = "General fixture paper",
) -> Path:
    """Plant a minimal, schema-shaped build in a fixture copy."""
    build = builds / name
    manifest = {
        "schema_version": "0.2.0",
        "build_id": name,
        "cli_invocation": {"flags_resolved": {"doi": doi, "github_repo": [repository]}},
    }
    observed_doi = enrichment_doi or doi
    enrichment = {
        "crossref": {"doi": observed_doi, "title": title},
        "unpaywall": {"doi": observed_doi},
    }
    _write_json(build / "build_manifest.json", manifest)
    _write_json(build / "external_enrichment.json", enrichment)
    return build


def _tier_row(
    doi: str,
    *,
    access_type: str | None = "gold",
    licence: str | None = "cc-by",
    source_reuse: str | None = "permissive",
    title: str = "General fixture paper",
) -> dict:
    """Return one real-shape tier inventory row."""
    access = {"license": licence, "is_oa": access_type != "closed", "title": title}
    if access_type is not None:
        access["type"] = access_type
    if source_reuse is not None:
        access["source_reuse"] = source_reuse
    return {
        "name": doi.replace(".", "_").replace("/", "_"),
        "display": doi,
        "domain": DOMAIN,
        "repo": "example/project",
        "doi": doi,
        "title": None,
        "publication_url": None,
        "access": access,
        "tier": "B",
    }


def _papers(path: Path) -> dict[str, dict]:
    """Index generated corpus rows by DOI."""
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {paper["doi"]: paper for paper in document["papers"]}


def _digest(path: Path) -> str:
    """Return one file's expected receipt digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _expected_input_digests(builds: Path, tiered: Path) -> dict[str, str]:
    """Build the exact logical input-digest table required by S4."""
    result = {"access_map": _digest(DEFAULT_ACCESS_MAP), "tiered": _digest(tiered)}
    for build in sorted(path for path in builds.iterdir() if path.is_dir()):
        for filename in ("build_manifest.json", "external_enrichment.json"):
            source = build / filename
            if source.is_file() and not build.name.startswith((".", "_")):
                result[f"builds/{build.name}/{filename}"] = _digest(source)
    return dict(sorted(result.items()))


def _without_fixture_controls(document: dict) -> dict:
    """Remove the documented fixture-only fields from a corpus document."""
    result = copy.deepcopy(document)
    for paper in result["papers"]:
        paper["access"].pop("verified_on", None)
        if paper["doi"] == CONTROL_DOI:
            paper["access"].pop("source_reuse", None)
    return result


def test_default_access_map_is_the_recorded_decision_7_table() -> None:
    """Keep every P1 policy branch in data, including its allowed outputs."""
    document = yaml.safe_load(DEFAULT_ACCESS_MAP.read_text(encoding="utf-8"))

    assert document == {
        "allowed_types": ["gold-oa", "green-oa", "open-access", "link-only"],
        "mapping": {
            "gold": {"permissive": "gold-oa", "otherwise": "open-access"},
            "green": "green-oa",
            "hybrid": {"cc": "open-access", "otherwise": "link-only"},
            "bronze": "link-only",
            "closed": "link-only",
            "unknown": "link-only",
            "otherwise": "link-only",
        },
    }
    header = DEFAULT_ACCESS_MAP.read_text(encoding="utf-8").splitlines()[0]
    assert header == (
        "# Decision 7 P1, owner decision 2026-09-18, hub docs/asbb/DECISIONS.md"
    )


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (" DOI:10.1234/ABC.Def#section ", "10.1234/abc.def"),
        ("https://doi.org/10.1234/ABC.Def?source=test", "10.1234/abc.def"),
        ("10.1234/abc.def/part", "10.1234/abc.def/part"),
    ],
)
def test_doi_normalization_strips_only_identity_wrappers(
    raw: str, expected: str
) -> None:
    """Normalize prefixes and suffixes without truncating a valid DOI path."""
    assert join.normalize_doi(raw) == expected


def test_fixture_join_matches_shipped_corpus_and_receipt_contract(
    tmp_path: Path,
) -> None:
    """Port the fixture rows field-for-field and digest every joined input."""
    builds, tiered = _copy_inputs(tmp_path)
    output = tmp_path / "candidate" / "corpus.yaml"

    assert join.main(_arguments(builds, tiered, output)) == 0

    actual = yaml.safe_load(output.read_text(encoding="utf-8"))
    expected = yaml.safe_load((FIXTURE / "corpus.yaml").read_text(encoding="utf-8"))
    assert _without_fixture_controls(actual) == _without_fixture_controls(expected)
    assert actual["version"] == 1
    assert [paper["doi"] for paper in actual["papers"]] == sorted(_papers(output))
    assert all(
        paper["access"]["verified_on"] == VERIFIED_ON for paper in actual["papers"]
    )
    assert _papers(output)[CONTROL_DOI]["access"]["source_reuse"] == "permissive"

    receipt_path = output.parent / "receipts" / "corpus_join_receipt.json"
    receipt = _read_json(receipt_path)
    access_map = yaml.safe_load(DEFAULT_ACCESS_MAP.read_text(encoding="utf-8"))
    assert set(receipt) == RECEIPT_KEYS
    assert receipt["schema"] == "asbb-corpus-join-receipt/1.0"
    assert receipt["stage"] == "S4"
    assert receipt["domain"] == DOMAIN
    assert receipt["inputs"] == _expected_input_digests(builds, tiered)
    assert receipt["access_map"] == access_map["mapping"]
    assert receipt["counts"] == {
        "builds": 3,
        "unique_dois": 3,
        "access.type": {"gold-oa": 3},
        "license_tier": {"open": 3},
        "oa_status_raw": {"gold": 3},
        "unmatched": 0,
        "capped": 0,
    }
    assert receipt["duplicate_dois"] == []
    assert receipt["unmatched_rows"] == []
    assert receipt["capped_rows"] == []
    assert "timestamp" not in receipt and "generated_at" not in receipt


def test_policy_branches_and_unmatched_builds_are_kept(tmp_path: Path) -> None:
    """Map both sides of P1 and make absent inventory rows loud but usable."""
    builds, tiered = _copy_inputs(tmp_path)
    rows = _tier_rows(tiered)
    rows[0]["access"].update(
        {"type": "gold", "license": "cc-by", "source_reuse": "permissive"}
    )
    rows[1]["access"].update(
        {
            "type": "gold",
            "license": "cc-by-nc-nd",
            "source_reuse": "restricted",
        }
    )
    rows[2]["access"].update(
        {"type": "hybrid", "license": "cc-by", "source_reuse": "permissive"}
    )
    cases = [
        ("visible-bronze__paper", "10.5555/bronze", "bronze", "cc-by", "permissive"),
        ("visible-unknown__paper", "10.5555/unknown", None, None, None),
    ]
    for name, doi, raw_type, licence, reuse in cases:
        _add_build(builds, name, doi)
        rows.append(
            _tier_row(
                doi,
                access_type=raw_type,
                licence=licence,
                source_reuse=reuse,
            )
        )
    unmatched_name = "visible-unmatched__paper"
    unmatched_doi = "10.5555/unmatched"
    _add_build(builds, unmatched_name, unmatched_doi)
    _write_json(tiered, rows)
    output = tmp_path / "corpus.yaml"
    receipts = tmp_path / "stage-receipts"

    assert join.main(_arguments(builds, tiered, output, receipts=receipts)) == 0

    papers = _papers(output)
    fixture_dois = [row["doi"] for row in rows[:3]]
    assert papers[fixture_dois[0]]["access"]["type"] == "gold-oa"
    assert papers[fixture_dois[1]]["access"]["type"] == "open-access"
    assert papers[fixture_dois[1]]["license_tier"] == "noncommercial"
    assert papers[fixture_dois[2]]["access"]["type"] == "open-access"
    assert papers["10.5555/bronze"]["access"]["type"] == "link-only"
    assert papers["10.5555/unknown"]["access"]["oa_status_raw"] == "unknown"
    assert "source_reuse" not in papers["10.5555/unknown"]["access"]
    assert "verified_via" not in papers["10.5555/bronze"]["access"]
    assert papers[unmatched_doi]["access"]["type"] == "link-only"
    assert papers[unmatched_doi]["access"]["license"] is None
    assert papers[unmatched_doi]["license_tier"] == "unknown"
    assert papers[unmatched_doi]["license_detection"] is None

    receipt = _read_json(receipts / "corpus_join_receipt.json")
    assert receipt["unmatched_rows"] == [
        {"build": unmatched_name, "doi": unmatched_doi}
    ]
    assert receipt["counts"]["unmatched"] == 1
    assert receipt["counts"]["oa_status_raw"]["unknown"] == 2
    assert receipt["counts"]["capped"] == len(receipt["capped_rows"])
    capped = {row["doi"]: row["reasons"] for row in receipt["capped_rows"]}
    assert "source_reuse!=permissive" in capped[fixture_dois[1]]
    assert "access.type=link-only" in capped["10.5555/bronze"]
    assert "access.type=link-only" in capped[unmatched_doi]


def test_duplicate_doi_variants_collapse_and_name_every_build(tmp_path: Path) -> None:
    """Collapse normalized DOI variants while recording the selected build."""
    builds, tiered = _copy_inputs(tmp_path)
    first = "alpha-run__paper"
    second = "zeta-run__paper"
    _add_build(builds, first, "10.1093/NAR/GKAB1275", repository="example/shared")
    _add_build(
        builds,
        second,
        "10.1093/nar/gkab1275#sec2",
        repository="https://github.com/example/shared.git",
        enrichment_doi="10.1093/nar/gkab1275?source=build",
    )
    rows = _tier_rows(tiered)
    rows.append(_tier_row("https://doi.org/10.1093/NAR/GKAB1275#inventory"))
    _write_json(tiered, rows)
    output = tmp_path / "corpus.yaml"
    receipts = tmp_path / "receipts"

    assert join.main(_arguments(builds, tiered, output, receipts=receipts)) == 0

    paper = _papers(output)[NORMALIZED_TEST_DOI]
    assert paper["name"] == first
    assert paper["repo_url"] == "https://github.com/example/shared"
    receipt = _read_json(receipts / "corpus_join_receipt.json")
    assert receipt["counts"]["builds"] == 5
    assert receipt["counts"]["unique_dois"] == 4
    assert receipt["duplicate_dois"] == [
        {"doi": NORMALIZED_TEST_DOI, "selected": first, "builds": [first, second]}
    ]


def test_repository_disagreement_is_conflict_without_outputs(tmp_path: Path) -> None:
    """Refuse duplicate DOI builds that identify different repositories."""
    builds, tiered = _copy_inputs(tmp_path)
    duplicate = "later-run__same-paper"
    _add_build(builds, duplicate, CONTROL_DOI, repository="different/project")
    output = tmp_path / "candidate" / "corpus.yaml"
    receipts = tmp_path / "receipts"

    code = join.main(_arguments(builds, tiered, output, receipts=receipts))

    assert code == 2
    assert not output.exists()
    assert not receipts.exists()


def test_doi_source_disagreement_is_conflict_without_outputs(tmp_path: Path) -> None:
    """Refuse a build whose manifest and enrichment identify different papers."""
    builds, tiered = _copy_inputs(tmp_path)
    manifest = next(builds.glob("*/build_manifest.json"))
    document = _read_json(manifest)
    document["cli_invocation"]["flags_resolved"]["doi"] = "10.5555/other-paper"
    _write_json(manifest, document)
    output = tmp_path / "corpus.yaml"

    assert join.main(_arguments(builds, tiered, output)) == 2
    assert not output.exists()
    assert not (tmp_path / "receipts").exists()


def test_duplicate_tier_inventory_rows_are_conflict(tmp_path: Path) -> None:
    """Refuse even identical duplicate policy rows instead of choosing silently."""
    builds, tiered = _copy_inputs(tmp_path)
    rows = _tier_rows(tiered)
    rows.append(copy.deepcopy(rows[0]))
    _write_json(tiered, rows)
    output = tmp_path / "corpus.yaml"

    assert join.main(_arguments(builds, tiered, output)) == 2
    assert not output.exists()


def test_visible_manifest_builds_are_discovered_without_name_coupling(
    tmp_path: Path,
) -> None:
    """Include any visible manifest child and ignore hidden or incomplete children."""
    builds, tiered = _copy_inputs(tmp_path)
    original = sorted(builds.iterdir())[0]
    visible = builds / "plain-run__paper"
    original.rename(visible)
    shutil.copytree(visible, builds / ".hidden-run")
    shutil.copytree(visible, builds / "_private-run")
    (builds / "ordinary-directory").mkdir()
    output = tmp_path / "corpus.yaml"

    assert join.main(_arguments(builds, tiered, output)) == 0

    names = {paper["name"] for paper in _papers(output).values()}
    assert visible.name in names
    assert ".hidden-run" not in names
    assert "_private-run" not in names
    receipt = _read_json(tmp_path / "receipts" / "corpus_join_receipt.json")
    assert receipt["counts"]["builds"] == 3


def test_dry_run_idempotence_and_output_conflict_contract(tmp_path: Path) -> None:
    """Write nothing on dry run, preserve identical bytes, and refuse drift."""
    builds, tiered = _copy_inputs(tmp_path)
    output = tmp_path / "candidate" / "corpus.yaml"
    receipt = output.parent / "receipts" / "corpus_join_receipt.json"
    arguments = _arguments(builds, tiered, output)

    assert join.main([*arguments, "--dry-run"]) == 0
    assert not output.exists() and not receipt.exists()
    assert join.main(arguments) == 0
    before = {"corpus": output.read_bytes(), "receipt": receipt.read_bytes()}
    assert join.main(arguments) == 0
    assert output.read_bytes() == before["corpus"]
    assert receipt.read_bytes() == before["receipt"]

    output.write_bytes(before["corpus"] + b"# drift\n")
    assert join.main(arguments) == 2
    assert output.read_bytes().endswith(b"# drift\n")
    assert receipt.read_bytes() == before["receipt"]


def test_receipt_parent_conflict_is_preflighted_before_corpus_write(
    tmp_path: Path,
) -> None:
    """Reject an invalid receipt parent before creating either output."""
    builds, tiered = _copy_inputs(tmp_path)
    output = tmp_path / "candidate" / "corpus.yaml"
    blocked_receipts = tmp_path / "blocked-receipts"
    blocked_receipts.write_text("not a directory\n", encoding="utf-8")

    code = join.main(_arguments(builds, tiered, output, receipts=blocked_receipts))

    assert code == 2
    assert not output.exists()
    assert blocked_receipts.read_text(encoding="utf-8") == "not a directory\n"


def test_version_date_and_domain_come_only_from_arguments(tmp_path: Path) -> None:
    """Render caller-owned identity fields without consulting a clock or path name."""
    builds, tiered = _copy_inputs(tmp_path)
    output = tmp_path / "corpus.yaml"
    verified_on = "2025-12-31"

    code = join.main(
        _arguments(
            builds,
            tiered,
            output,
            domain="environmental-genomics",
            version="v12",
            verified_on=verified_on,
        )
    )

    assert code == 0
    corpus = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert corpus["collection"] == "environmental-genomics"
    assert corpus["version"] == 12
    assert all(row["category"] == "environmental-genomics" for row in corpus["papers"])
    assert all(row["access"]["verified_on"] == verified_on for row in corpus["papers"])


def test_network_license_derivers_are_explicitly_out_of_scope(tmp_path: Path) -> None:
    """Document and preserve the offline boundary of the S4 join."""
    assert join.__doc__ is not None
    assert "derive_license_tiers.py" in join.__doc__
    assert "resolve_paper_license.py" in join.__doc__
    assert "does not call" in join.__doc__

    builds, tiered = _copy_inputs(tmp_path)
    output = tmp_path / "corpus.yaml"
    assert join.main(_arguments(builds, tiered, output)) == 0
