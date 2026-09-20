"""Contract tests for bootstrapping a collected release candidate's indexes."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

from scripts import bootstrap_indexes as bootstrap
from scripts import skill_index


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
CREATORS = REPO / "scripts" / "release_creators.yaml"
DOMAIN = "metabarcoding"
VERSION = "v1"
PLUGIN_REPO = "https://github.com/HolobiomicsLab/asb-skills-metabarcoding"
INDEX_NAMES = {"skills_index.json", "kb_bundle.json", "tools_index.json"}


def _collect_candidate(tmp_path: Path, *, unknown_tier: bool = False) -> Path:
    """Build the Task 3 candidate and install the Task 4 corpus output."""
    candidate = tmp_path / "candidate"
    collector_receipts = tmp_path / "collector-receipts"
    corpus = tmp_path / "corpus.yaml"
    corpus_payload = yaml.safe_load(
        (FIXTURE / "corpus.yaml").read_text(encoding="utf-8")
    )
    if unknown_tier:
        corpus_payload["papers"][0]["license_tier"] = "unknown"
        corpus_payload["papers"][0]["access"]["license"] = None
    corpus.write_text(
        yaml.safe_dump(corpus_payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    args = [
        "--cut",
        str(FIXTURE / "corpus"),
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
        "--corpus",
        str(corpus),
        "--receipts",
        str(collector_receipts),
    ]
    environment = dict(os.environ)
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(key, None)
    environment.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        ASB_EMBED_MODEL="bge-small-en-v1.5",
        PYTHONDONTWRITEBYTECODE="1",
    )
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "collect_from_cut.py"), *args],
        cwd=REPO,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout
    shutil.copy2(corpus, candidate / "corpus.yaml")
    return candidate


def _tree_bytes(root: Path) -> dict[str, bytes]:
    """Return a deterministic byte snapshot of a possibly absent tree."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _sha256(path: Path) -> str:
    """Return one file's hexadecimal SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bootstrap(candidate: Path, receipts: Path, *, dry_run: bool = False) -> int:
    """Invoke the public bootstrap interface for one candidate."""
    args = [
        str(candidate),
        "--corpus",
        str(candidate / "corpus.yaml"),
        "--receipts",
        str(receipts),
    ]
    if dry_run:
        args.append("--dry-run")
    return bootstrap.main(args)


def _frontmatter(path: Path) -> dict:
    """Read a generated leaf with the canonical frontmatter parser."""
    frontmatter, _ = skill_index.split_frontmatter(path.read_text(encoding="utf-8"))
    assert frontmatter is not None
    return frontmatter


def test_bootstrap_builds_indexes_links_stamps_and_receipt(tmp_path: Path) -> None:
    """Build all indexes from leaf/tool data and record every helper result."""
    candidate = _collect_candidate(tmp_path)
    receipts = tmp_path / "bootstrap-receipts"
    provisional_hash = _sha256(candidate / "skills_index.json")

    assert _bootstrap(candidate, receipts) == 0
    assert INDEX_NAMES <= {path.name for path in candidate.glob("*.json")}

    skills = json.loads((candidate / "skills_index.json").read_text(encoding="utf-8"))
    tools = json.loads((candidate / "tools_index.json").read_text(encoding="utf-8"))
    bundle = json.loads((candidate / "kb_bundle.json").read_text(encoding="utf-8"))
    by_slug = {row["slug"]: row for row in skills}
    assert len(skills) == 3
    assert bundle["distinct_dois"] == sorted(
        {doi for row in skills for doi in row["dois"]}
    )
    assert set(bundle["skills"]) == set(by_slug)
    assert {row["license_tier"] for row in tools} == {"unknown"}

    source_paper_leaf_count = 0
    for leaf in sorted((candidate / "leaves").glob("*/SKILL.md")):
        frontmatter = _frontmatter(leaf)
        row = by_slug[leaf.parent.name]
        source_papers = (frontmatter.get("provenance") or {}).get("source_papers") or []
        if source_papers:
            source_paper_leaf_count += 1
            assert row["dois"]
            assert row["dois"] == [paper["doi"] for paper in source_papers]
            assert row["dois"] == [doi.lower() for doi in row["dois"]]
        assert row["triage_status"] == frontmatter["triage_status"]
        assert row["yes_rate"] == frontmatter["yes_rate"]
        assert row["n_claims"] == frontmatter["n_claims"]
        assert (frontmatter["metadata"])["license_tier"] == row["license_tier"]
        assert (frontmatter["metadata"])["provenance_tier"] == row["provenance_tier"]
        assert bundle["skills"][leaf.parent.name]["tools_used"] == row["tools_used"]
        assert all(
            (candidate / "tools" / f"{tool_slug}.yaml").is_file()
            for tool_slug in row["tools_used"]
        )
    assert source_paper_leaf_count == 3

    denoising = by_slug["amplicon-sequence-denoising"]
    assert {"cutadapt", "dada2", "deblur", "qiime-2"} <= set(denoising["tools_used"])
    assert "VSEARCH" in denoising["tools"]
    assert "vsearch" not in denoising["tools_used"]

    receipt = json.loads(
        (receipts / "bootstrap_receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["stage"] == "S5-bootstrap"
    assert receipt["counts"] == {
        "skills": 3,
        "tools": len(tools),
        "dois": len(bundle["distinct_dois"]),
    }
    assert receipt["provisional_skills_index_sha256_before"] == provisional_hash
    assert receipt["skills_index_sha256_after"] == _sha256(
        candidate / "skills_index.json"
    )
    assert "VSEARCH" in receipt["unmatched_leaf_tool_names"]
    assert set(receipt["helpers"]) == {
        "propagate_license_tiers",
        "stamp_skill_license",
        "backfill_tool_license",
        "propagate_provenance_tiers",
        "stamp_provenance",
        "router_shape",
    }


def test_bootstrap_accepts_unknown_tier_and_is_idempotent(tmp_path: Path) -> None:
    """Accept the canonical unknown tier and keep a second run byte-identical."""
    candidate = _collect_candidate(tmp_path, unknown_tier=True)
    receipts = tmp_path / "bootstrap-receipts"

    assert _bootstrap(candidate, receipts) == 0
    skills = json.loads((candidate / "skills_index.json").read_text(encoding="utf-8"))
    assert "unknown" in {row["license_tier"] for row in skills}
    before = (_tree_bytes(candidate), _tree_bytes(receipts))

    assert _bootstrap(candidate, receipts) == 0
    assert (_tree_bytes(candidate), _tree_bytes(receipts)) == before


def test_bootstrap_dry_run_writes_nothing(tmp_path: Path, capsys) -> None:
    """Describe the planned bootstrap without changing either output tree."""
    candidate = _collect_candidate(tmp_path)
    receipts = tmp_path / "bootstrap-receipts"
    before = _tree_bytes(candidate)

    assert _bootstrap(candidate, receipts, dry_run=True) == 0
    assert _tree_bytes(candidate) == before
    assert not receipts.exists()
    plan = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert plan["dry_run"] is True
    assert plan["indexes"] == sorted(INDEX_NAMES)


def test_bootstrap_refuses_nonprovisional_index_outputs(tmp_path: Path) -> None:
    """Return conflict without replacing an index not owned by the bootstrap."""
    candidate = _collect_candidate(tmp_path)
    receipts = tmp_path / "bootstrap-receipts"
    foreign = b'{"skills": "owned elsewhere"}\n'
    (candidate / "kb_bundle.json").write_bytes(foreign)
    before = _tree_bytes(candidate)

    assert _bootstrap(candidate, receipts) == 2
    assert _tree_bytes(candidate) == before
    assert not receipts.exists()


def test_bootstrap_preflights_receipt_parent_before_candidate_write(
    tmp_path: Path,
) -> None:
    """Treat a non-directory receipt root as conflict before synchronizing."""
    candidate = _collect_candidate(tmp_path)
    receipts = tmp_path / "blocked-receipts"
    receipts.write_text("not a directory\n", encoding="utf-8")
    before = _tree_bytes(candidate)

    assert _bootstrap(candidate, receipts) == 2
    assert _tree_bytes(candidate) == before
    assert receipts.read_text(encoding="utf-8") == "not a directory\n"
