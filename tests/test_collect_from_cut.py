"""Contract tests for collecting a consolidated cut into a release candidate."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pytest
import yaml

from scripts import collect_from_cut as collector
from scripts import collect_metabolomics_collection as collection_writer
from scripts import lint_skill_descriptions as description_lint
from scripts import release_gate, skill_index


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
CREATORS = REPO / "scripts" / "release_creators.yaml"
DOMAIN = "metabarcoding"
VERSION = "v1"
PLUGIN_REPO = "https://github.com/HolobiomicsLab/asb-skills-metabarcoding"
STRICT_DOI = "10.1002/ece3.6594"
EXPECTED_OUTPUT_COUNT = 3
VARIANT_CHUNK_MIN = 40
EVIDENCE_SPAN_CAP = 300
EVIDENCE_DOI_CAP = 1500
MAPPING_KEYS = {
    "output_id",
    "leaf_slug",
    "member_ids",
    "canonical_member_id",
    "capsules",
    "merge_kind",
    "merged_aliases",
    "dois",
    "description_rewritten",
    "evidence_trimmed",
}


def _args(
    fixture: Path,
    candidate: Path,
    *,
    corpus: bool = True,
    receipts: Path | None = None,
    dry_run: bool = False,
) -> list[str]:
    """Build the public collector arguments for one isolated run."""
    result = [
        "--cut",
        str(fixture / "corpus"),
        "--domain",
        DOMAIN,
        "--version",
        VERSION,
        "--out",
        str(candidate),
        "--license",
        "CC-BY-4.0",
        "--plugin-repo",
        PLUGIN_REPO,
        "--creators",
        str(CREATORS),
    ]
    if corpus:
        result.extend(("--corpus", str(fixture / "corpus.yaml")))
    if receipts is not None:
        result.extend(("--receipts", str(receipts)))
    if dry_run:
        result.append("--dry-run")
    return result


def _collect(
    tmp_path: Path, fixture: Path = FIXTURE, *, corpus: bool = True
) -> tuple[Path, Path]:
    """Run the collector and return its candidate and receipt roots."""
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    assert (
        collector.main(_args(fixture, candidate, corpus=corpus, receipts=receipts)) == 0
    )
    return candidate, receipts


def _coverage_by_output(fixture: Path = FIXTURE) -> dict[str, dict]:
    """Load every output coverage record in stable path order."""
    paths = sorted((fixture / "corpus" / "skills").glob("*/coverage.json"))
    return {
        path.parent.name: json.loads(path.read_text(encoding="utf-8")) for path in paths
    }


def _read_skill(path: Path) -> tuple[dict, str]:
    """Read one skill with the repository's canonical frontmatter parser."""
    frontmatter, body = skill_index.split_frontmatter(path.read_text(encoding="utf-8"))
    assert frontmatter is not None, path
    return frontmatter, body


def _write_skill(path: Path, frontmatter: dict, body: str) -> None:
    """Rewrite fixture-copy frontmatter while preserving its body value."""
    rendered = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
    path.write_text(f"---\n{rendered}---\n{body}", encoding="utf-8")


def _tree_bytes(root: Path) -> dict[str, bytes]:
    """Return a byte-exact snapshot of a possibly absent output tree."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _normal_doi(value: object) -> str:
    """Normalize DOI identity with the release gate's policy function."""
    return release_gate._norm_doi(value)


def _skill_evidence(path: Path) -> list[tuple[str, str]]:
    """Return gate-parsed ``(doi, text)`` evidence in file order."""
    frontmatter, body = _read_skill(path)
    default_dois = release_gate._skill_dois(frontmatter)
    default_doi = default_dois[0] if default_dois else ""
    return [
        (_normal_doi(span.get("doi") or default_doi), span["text"])
        for span in release_gate._collect_evidence_spans(frontmatter, body)
    ]


def _leaf_evidence_by_context(root: Path, filename: str) -> dict[str, list[str]]:
    """Group gate-parsed evidence by DOI across sorted cut or output leaves."""
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in sorted(root.glob(f"*/{filename}")):
        for doi, text in _skill_evidence(path):
            grouped[doi].append(text)
    return dict(grouped)


def _tool_evidence(candidate: Path) -> dict[str, list[str]]:
    """Read output tool evidence by tool slug."""
    result = {}
    for path in sorted((candidate / "tools").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        result[path.stem] = [
            span.get("text") or span.get("quote") or ""
            if isinstance(span, dict)
            else span
            for span in payload.get("evidence_spans") or []
        ]
    return result


def _original_tool_evidence(fixture: Path, doi: str) -> list[tuple[str, str]]:
    """Read source tool spans for one DOI from all fixture builds."""
    result = []
    for index_path in sorted((fixture / "builds").glob("*/tools/_index.json")):
        build = index_path.parent.parent
        manifest = json.loads(
            (build / "build_manifest.json").read_text(encoding="utf-8")
        )
        flags = (manifest.get("cli_invocation") or {}).get("flags_resolved") or {}
        records = json.loads(index_path.read_text(encoding="utf-8")).get("records", [])
        for record in records:
            record_doi = _normal_doi(record.get("source_paper_doi") or flags.get("doi"))
            if record_doi != doi:
                continue
            for span in record.get("evidence_spans") or []:
                text = (
                    span.get("text") or span.get("quote") or ""
                    if isinstance(span, dict)
                    else span
                )
                if str(text).strip():
                    result.append((record["slug"], str(text).strip()))
    return result


def _citation_author(creator: dict) -> dict:
    """Convert one release creator to its exact CFF author representation."""
    if "name" in creator:
        return {"name": creator["name"]}
    orcid = str(creator["orcid"])
    if not orcid.startswith(("https://", "http://")):
        orcid = f"https://orcid.org/{orcid}"
    return {
        "family-names": creator["family"],
        "given-names": creator["given"],
        "orcid": orcid,
        "affiliation": creator["affiliation"],
    }


@pytest.fixture
def collected(tmp_path: Path) -> tuple[Path, Path]:
    """Provide one successfully collected fixture candidate."""
    return _collect(tmp_path)


def test_tree_is_router_shaped_and_leaves_root_is_created_first(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Create the corpus root before leaves and finish with router artifacts."""
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    mkdir_calls: list[Path] = []
    original_mkdir = pathlib.Path.mkdir

    def recording_mkdir(self: Path, *args: object, **kwargs: object) -> None:
        try:
            relative = self.relative_to(candidate)
        except ValueError:
            pass
        else:
            if relative != Path("."):
                mkdir_calls.append(relative)
        original_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "mkdir", recording_mkdir)
    assert collector.main(_args(FIXTURE, candidate, receipts=receipts)) == 0

    coverages = _coverage_by_output()
    leaf_files = sorted((candidate / "leaves").glob("*/SKILL.md"))
    assert {path.parent.name for path in leaf_files} == set(coverages)
    assert len(coverages) == EXPECTED_OUTPUT_COUNT
    required = (
        "collection.yaml",
        "CITATION.cff",
        ".claude-plugin/plugin.json",
        "mapping.json",
        "skills_index.json",
        "skills/_router/SKILL.md",
        "bin/search_skills.py",
    )
    assert all((candidate / relative).is_file() for relative in required)
    assert list((candidate / "tools").glob("*.yaml"))
    index = json.loads((candidate / "skills_index.json").read_text(encoding="utf-8"))
    assert {row["slug"] for row in index} == set(coverages)

    leaves_root_index = mkdir_calls.index(Path("leaves"))
    leaf_dir_indices = [
        index
        for index, path in enumerate(mkdir_calls)
        if path.parts[:1] == ("leaves",) and len(path.parts) > 1
    ]
    assert leaf_dir_indices
    assert leaves_root_index < min(leaf_dir_indices)


def test_mapping_round_trips_coverage_and_merged_aliases(
    collected: tuple[Path, Path],
) -> None:
    """Map every cut member exactly once and retain the declared merge alias."""
    candidate, _ = collected
    coverages = _coverage_by_output()
    mapping = json.loads((candidate / "mapping.json").read_text(encoding="utf-8"))

    assert set(mapping) == {"mappings", "summary"}
    assert len(mapping["mappings"]) == EXPECTED_OUTPUT_COUNT
    rows = {row["output_id"]: row for row in mapping["mappings"]}
    assert set(rows) == set(coverages)
    for output_id, coverage in coverages.items():
        row = rows[output_id]
        assert set(row) == MAPPING_KEYS
        assert row["leaf_slug"] == output_id
        assert row["member_ids"] == [m["member_id"] for m in coverage["members"]]
        assert row["canonical_member_id"] == coverage["canonical_member_id"]
        assert row["capsules"] == coverage.get("capsules", [])
        assert row["merge_kind"] == coverage["merge_kind"]
        assert row["merged_aliases"] == coverage.get("merged_slugs", [])

    merged = [row for row in rows.values() if row["merged_aliases"]]
    assert len(merged) == 1
    assert merged[0]["merged_aliases"] == ["16s-amplicon-sequence-denoising"]
    frontmatter, _ = _read_skill(
        candidate / "leaves" / merged[0]["leaf_slug"] / "SKILL.md"
    )
    assert frontmatter["merged_aliases"] == ["16s-amplicon-sequence-denoising"]


def test_variants_and_sidecars_are_never_copied(collected: tuple[Path, Path]) -> None:
    """Exclude sidecars and every body passage unique to noncanonical variants."""
    candidate, _ = collected
    assert not list(candidate.rglob("variants"))
    assert not list(candidate.rglob("skill_kb.json"))
    expected_leaf_files = {
        f"{output_id}/SKILL.md" for output_id in _coverage_by_output()
    }
    actual_leaf_files = {
        path.relative_to(candidate / "leaves").as_posix()
        for path in (candidate / "leaves").rglob("*")
        if path.is_file()
    }
    assert actual_leaf_files == expected_leaf_files
    output_text = "\n".join(
        data.decode("utf-8", errors="replace")
        for data in _tree_bytes(candidate).values()
    )

    checked_variants = 0
    for output_id, coverage in _coverage_by_output().items():
        canonical_text = (
            FIXTURE / "corpus" / "skills" / output_id / "skill.md"
        ).read_text(encoding="utf-8")
        for member in coverage["members"]:
            if member["member_id"] == coverage["canonical_member_id"]:
                continue
            variant_path = (
                FIXTURE / "corpus" / "skills" / output_id / member["variant_path"]
            )
            variant = json.loads(variant_path.read_text(encoding="utf-8"))
            _, variant_body = skill_index.split_frontmatter(variant["body"])
            chunks = [
                line.strip()
                for line in variant_body.splitlines()
                if len(line.strip()) >= VARIANT_CHUNK_MIN
                and line.strip() not in canonical_text
            ]
            assert chunks, variant_path
            assert all(chunk not in output_text for chunk in chunks)
            checked_variants += 1
    assert checked_variants


def test_description_preservation_and_repository_rewrite(tmp_path: Path) -> None:
    """Preserve valid metadata and rewrite only an overlong description."""
    fixture_copy = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture_copy)
    skill_dirs = sorted((fixture_copy / "corpus" / "skills").glob("*/skill.md"))
    preserved_path, overlong_path = skill_dirs[:2]

    preserved_frontmatter, preserved_body = _read_skill(preserved_path)
    preserved_opening = description_lint.APPROVED_PREFIXES[1]
    preserved = (
        f"{preserved_opening} applying an already documented procedure while retaining "
        "the curator-provided description exactly."
    )
    assert description_lint.check_description(preserved) == []
    preserved_frontmatter["description"] = preserved
    _write_skill(preserved_path, preserved_frontmatter, preserved_body)

    overlong_frontmatter, overlong_body = _read_skill(overlong_path)
    overlong = "Explains " + ("a documented analytical procedure with evidence; " * 12)
    assert len(overlong) > collection_writer.MAX_LEN
    overlong_frontmatter["description"] = overlong
    _write_skill(overlong_path, overlong_frontmatter, overlong_body)
    expected_rewrite = collection_writer._build_description(
        overlong_frontmatter["name"],
        collection_writer._read_skill_md_section(overlong_path, "When to use"),
        overlong,
        domain_label=DOMAIN,
    )

    candidate, _ = _collect(tmp_path / "run", fixture_copy)
    preserved_output, _ = _read_skill(
        candidate / "leaves" / preserved_path.parent.name / "SKILL.md"
    )
    rewritten_output, _ = _read_skill(
        candidate / "leaves" / overlong_path.parent.name / "SKILL.md"
    )

    assert preserved_output["description"] == preserved
    assert preserved_output["description"].count(preserved_opening) == 1
    rewritten = rewritten_output["description"]
    assert rewritten == expected_rewrite != overlong
    assert len(rewritten) <= collection_writer.MAX_LEN == description_lint.MAX_LEN
    assert rewritten.startswith(description_lint.APPROVED_PREFIXES)
    assert (
        sum(
            rewritten.startswith(prefix)
            for prefix in description_lint.APPROVED_PREFIXES
        )
        == 1
    )
    assert description_lint.check_description(rewritten) == []


def test_citation_authors_exactly_convert_release_creators(
    collected: tuple[Path, Path],
) -> None:
    """Render person and entity creators without substituting collection defaults."""
    candidate, _ = collected
    source = yaml.safe_load(CREATORS.read_text(encoding="utf-8"))
    citation = yaml.safe_load((candidate / "CITATION.cff").read_text(encoding="utf-8"))

    expected = [_citation_author(creator) for creator in source["creators"]]
    assert citation["authors"] == expected
    assert len(citation["authors"]) == 2


def test_evidence_policy_trims_strict_doi_and_preserves_permissive_text(
    collected: tuple[Path, Path],
) -> None:
    """Apply one shared leaf-then-tool budget and receipt every changed span."""
    candidate, receipts = collected
    trim = json.loads(
        (receipts / "evidence_trim_receipt.json").read_text(encoding="utf-8")
    )
    strict_doi = _normal_doi(STRICT_DOI)
    output_tools = _tool_evidence(candidate)
    kept = [row for row in trim["kept"] if _normal_doi(row["doi"]) == strict_doi]
    strict_dropped = [
        row for row in trim["dropped"] if _normal_doi(row["doi"]) == strict_doi
    ]
    leaf_contexts = [row["leaf"] for row in trim["kept"] if row["kind"] == "leaf"]
    tool_contexts = [row["tool"] for row in trim["kept"] if row["kind"] == "tool"]

    assert kept
    assert leaf_contexts == sorted(leaf_contexts)
    assert tool_contexts == sorted(tool_contexts)
    assert [row["kind"] for row in trim["kept"]] == sorted(
        (row["kind"] for row in trim["kept"]), key={"leaf": 0, "tool": 1}.get
    )
    assert any(row["kind"] == "tool" for row in kept + strict_dropped)
    assert all(len(row["text"]) <= EVIDENCE_SPAN_CAP for row in kept)
    assert sum(len(row["text"]) for row in kept) <= EVIDENCE_DOI_CAP
    for row in kept:
        if row["kind"] == "leaf":
            leaf = candidate / "leaves" / row["leaf"] / "SKILL.md"
            assert row["text"] in [text for _, text in _skill_evidence(leaf)]
        else:
            assert row["text"] in output_tools[row["tool"]]

    dropped = {
        (row["kind"], row.get("leaf") or row.get("tool"), row["text"])
        for row in strict_dropped
    }
    for output_id in _coverage_by_output():
        source_path = FIXTURE / "corpus" / "skills" / output_id / "skill.md"
        published_path = candidate / "leaves" / output_id / "SKILL.md"
        published = {text for _, text in _skill_evidence(published_path)}
        for doi, text in _skill_evidence(source_path):
            if doi == strict_doi and text not in published:
                assert ("leaf", output_id, text) in dropped
    for tool_slug, text in _original_tool_evidence(FIXTURE, strict_doi):
        if text not in output_tools.get(tool_slug, []):
            assert ("tool", tool_slug, text) in dropped

    corpus = yaml.safe_load((FIXTURE / "corpus.yaml").read_text(encoding="utf-8"))
    permissive = {
        _normal_doi(paper["doi"])
        for paper in corpus["papers"]
        if (paper.get("access") or {}).get("source_reuse") == "permissive"
    }
    original_by_doi = _leaf_evidence_by_context(
        FIXTURE / "corpus" / "skills", "skill.md"
    )
    output_by_doi = _leaf_evidence_by_context(candidate / "leaves", "SKILL.md")
    tested = [doi for doi in sorted(permissive) if original_by_doi.get(doi)]
    assert tested
    for doi in tested:
        assert output_by_doi[doi] == original_by_doi[doi]


def test_dry_run_writes_neither_candidate_nor_default_receipts(tmp_path: Path) -> None:
    """Keep both default output roots absent during a successful dry run."""
    candidate = tmp_path / "candidate"
    receipts = candidate.parent / "receipts"

    assert collector.main(_args(FIXTURE, candidate, dry_run=True)) == 0
    assert not candidate.exists()
    assert not receipts.exists()


def test_second_run_is_byte_identical_for_candidate_and_receipts(
    tmp_path: Path,
) -> None:
    """Make an identical second invocation a successful no-op."""
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    args = _args(FIXTURE, candidate, receipts=receipts)

    assert collector.main(args) == 0
    candidate_before = _tree_bytes(candidate)
    receipts_before = _tree_bytes(receipts)
    assert candidate_before and receipts_before
    assert collector.main(args) == 0
    assert _tree_bytes(candidate) == candidate_before
    assert _tree_bytes(receipts) == receipts_before


def test_omitted_corpus_records_not_applied_without_trimming(tmp_path: Path) -> None:
    """Distinguish an unapplied evidence policy from a checked-clean corpus."""
    candidate, receipts = _collect(tmp_path, corpus=False)
    trim = json.loads(
        (receipts / "evidence_trim_receipt.json").read_text(encoding="utf-8")
    )
    mapping = json.loads((candidate / "mapping.json").read_text(encoding="utf-8"))

    assert trim["status"] == "not_applied"
    assert trim.get("kept", []) == []
    assert trim.get("dropped", []) == []
    assert all(not row["evidence_trimmed"] for row in mapping["mappings"])
    for output_id in _coverage_by_output():
        source = FIXTURE / "corpus" / "skills" / output_id / "skill.md"
        published = candidate / "leaves" / output_id / "SKILL.md"
        assert _skill_evidence(published) == _skill_evidence(source)


def test_conflicting_existing_output_exits_two_without_mutation(tmp_path: Path) -> None:
    """Reject a different destination before writing any candidate or receipt file."""
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    candidate.mkdir()
    (candidate / "collection.yaml").write_bytes(b"different existing output\n")
    before = _tree_bytes(candidate)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.collect_from_cut",
            *_args(FIXTURE, candidate, receipts=receipts),
        ],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 2, completed.stderr
    assert _tree_bytes(candidate) == before
    assert not receipts.exists()


def test_invalid_release_policy_exits_one_without_output(tmp_path: Path) -> None:
    """Translate an expected validation failure to CLI status one."""
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    args = _args(FIXTURE, candidate, receipts=receipts)
    args[args.index("--license") + 1] = "MIT"

    completed = subprocess.run(
        [sys.executable, "-m", "scripts.collect_from_cut", *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 1, completed.stderr
    assert not candidate.exists()
    assert not receipts.exists()


def test_overlong_evidence_requires_a_sentence_boundary() -> None:
    """Keep a complete sentence under the cap and drop an uncuttable span."""
    complete = "A complete evidence sentence."
    assert collector._boundary_prefix(f"{complete} {'word ' * 100}", 300) == complete
    assert collector._boundary_prefix("x" * 301, 300) == ""


def test_read_only_symlink_build_tree_is_accepted(tmp_path: Path) -> None:
    """Follow the provisional view's input symlinks without writing through them."""
    fixture_copy = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture_copy, ignore=shutil.ignore_patterns("builds"))
    build_root = fixture_copy / "builds"
    build_root.mkdir()
    for source in sorted((FIXTURE / "builds").iterdir()):
        (build_root / source.name).symlink_to(source, target_is_directory=True)

    candidate = tmp_path / "candidate"
    assert collector.main(_args(fixture_copy, candidate, dry_run=True)) == 0
    assert not candidate.exists()


def test_tool_records_keep_build_repository_without_canonical_url(
    collected: tuple[Path, Path],
) -> None:
    """Join each indexed tool to its build repository without the banned key."""
    candidate, _ = collected
    expected_by_slug: dict[str, set[str]] = defaultdict(set)
    for index_path in sorted((FIXTURE / "builds").glob("*/tools/_index.json")):
        manifest = json.loads(
            (index_path.parent.parent / "build_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        raw_repos = (manifest.get("cli_invocation") or {}).get(
            "flags_resolved", {}
        ).get("github_repo") or []
        if isinstance(raw_repos, str):
            raw_repos = [raw_repos]
        repos = {
            repo if repo.startswith("https://") else f"https://github.com/{repo}"
            for repo in raw_repos
        }
        for record in json.loads(index_path.read_text(encoding="utf-8"))["records"]:
            expected_by_slug[record["slug"]].update(repos)

    for slug, expected in expected_by_slug.items():
        tool = yaml.safe_load(
            (candidate / "tools" / f"{slug}.yaml").read_text(encoding="utf-8")
        )
        assert tool["license_tier"] == "unknown"
        assert "canonical_url" not in tool
        assert expected <= set(tool["source_repos"])


def test_output_symlink_is_a_conflict_and_is_not_followed(tmp_path: Path) -> None:
    """Accept symlinked inputs but never redirect candidate writes through one."""
    target = tmp_path / "target"
    target.mkdir()
    candidate = tmp_path / "candidate"
    candidate.symlink_to(target, target_is_directory=True)

    assert (
        collector.main(_args(FIXTURE, candidate, receipts=tmp_path / "receipts")) == 2
    )
    assert not list(target.iterdir())


def test_repository_metadata_uses_only_the_first_declared_repo(tmp_path: Path) -> None:
    """Do not silently replace a non-GitHub first value with a later repository."""
    fixture_copy = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture_copy)
    source = next(iter(sorted((fixture_copy / "corpus" / "skills").glob("*/skill.md"))))
    frontmatter, body = _read_skill(source)
    frontmatter["tools"] = [
        {"name": "first", "repo": "https://example.org/not-github"},
        {"name": "second", "repo": "https://github.com/example/later"},
        *(frontmatter.get("tools") or []),
    ]
    _write_skill(source, frontmatter, body)

    candidate, _ = _collect(tmp_path / "run", fixture_copy)
    published, _ = _read_skill(candidate / "leaves" / source.parent.name / "SKILL.md")
    assert "repo_url" not in published["metadata"]
