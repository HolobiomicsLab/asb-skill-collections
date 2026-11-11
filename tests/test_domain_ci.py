"""Reusable domain workflows and their registry-backed generator."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import yaml

from scripts import render_domain_ci


REPO = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
SHA = "a" * 40


def workflow_key(document: dict) -> str:
    """Return YAML's workflow trigger key despite YAML 1.1 boolean parsing."""
    return next(key for key in document if key == "on" or key is True)


def read_workflow(path: Path) -> dict:
    """Parse one workflow without applying GitHub expression interpolation."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_reusable_workflow_declares_the_domain_contract() -> None:
    """The reusable caller interface exposes only the five supported inputs."""
    path = REPO / ".github" / "workflows" / "domain-gates.yml"
    document = read_workflow(path)
    trigger = document[workflow_key(document)]["workflow_call"]
    assert set(trigger["inputs"]) == {"domain", "collection_path", "receipts_path", "strict", "edam_strict"}
    assert trigger["inputs"]["strict"] == {
        "description": "Require a passing strict release gate.",
        "required": False,
        "default": True,
        "type": "boolean",
    }
    assert trigger["inputs"]["edam_strict"] == {
        "description": "Fail on EDAM identifiers that do not resolve to a valid term.",
        "required": False,
        "default": False,
        "type": "boolean",
    }
    job = document["jobs"]["content-gates"]
    edam_step = next(step for step in job["steps"] if step["name"] == "Check EDAM IRIs")
    assert edam_step["env"]["EDAM_STRICT"] == "${{ inputs.edam_strict }}"
    assert "--edam-strict" in edam_step["run"]
    checkouts = [step for step in job["steps"] if step.get("uses", "").startswith("actions/checkout@")]
    assert checkouts[0]["with"] == {"path": "content"}
    assert checkouts[1]["with"] == {
        "repository": "HolobiomicsLab/asb-skill-collections",
        "ref": "${{ github.job_workflow_sha }}",
        "token": "${{ github.token }}",
        "path": "tooling",
    }


def test_workflow_orders_all_required_gates() -> None:
    """Named steps preserve the legacy content-gate execution order."""
    document = read_workflow(REPO / ".github" / "workflows" / "domain-gates.yml")
    steps = document["jobs"]["content-gates"]["steps"]
    names = [step["name"] for step in steps]
    expected = [
        "Every skill is in every index its collection publishes",
        "Lint skill descriptions",
        "Check derived_from DOIs resolve (sample)",
        "Check EDAM IRIs",
        "Advertised counts",
        "License tiers",
        "Provenance tiers",
        "Tool catalogue",
        "Related skills",
        "Proposals",
        "Release surface",
        "Release gate",
    ]
    assert [name for name in names if name in expected] == expected
    assert names[-1] == "Receipt re-verification"
    assert steps[names.index(expected[2])]["continue-on-error"] is True
    assert "--verify" in steps[-1]["run"]


def test_caller_template_has_a_deliberate_sha_placeholder() -> None:
    """A copied caller cannot silently track the tooling default branch."""
    text = (REPO / "scripts" / "templates" / "domain-ci.yml").read_text(encoding="utf-8")
    assert "domain-gates.yml@<TOOLING_SHA>" in text
    assert "Bump this full commit SHA deliberately" in text
    assert "<MATRIX_ROWS>" in text


def manifest_fixture(tmp_path: Path) -> Path:
    """Write a compact manifest with current and legacy releases."""
    document = {
        "domains": {
            "fixture": {
                "releases": [
                    {"path": "collections/fixture/v3"},
                    {"path": "collections/fixture/v2"},
                    {"path": "collections/fixture/v1", "status": "legacy"},
                ]
            },
            "old": {"releases": [{"path": "collections/old/v1", "status": "legacy"}]},
        }
    }
    path = tmp_path / "collections.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


def test_generator_renders_published_releases_and_omits_legacy(tmp_path: Path) -> None:
    """Each current release receives one row and legacy releases receive none."""
    paths = render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", tmp_path / "out"
    )
    assert [path.name for path in paths] == [
        "gates.yml", "plugin-validate.yml", "intake.yml", "retraction-watch.yml"
    ]
    document = read_workflow(paths[0])
    rows = document["jobs"]["released-collections"]["strategy"]["matrix"]["collection"]
    assert rows == [
        {"domain": "fixture", "collection_path": "collections/fixture/v3", "receipts_path": ""},
        {"domain": "fixture", "collection_path": "collections/fixture/v2", "receipts_path": ""},
    ]
    assert document["jobs"]["released-collections"]["uses"].endswith("@" + SHA)
    assert "<TOOLING_SHA>" not in paths[0].read_text(encoding="utf-8")
    assert read_workflow(paths[1])["jobs"]["plugin-manifest"]["steps"][2]["run"].startswith("npm install")
    assert read_workflow(paths[2])["name"] == "Paper issue intake"
    retraction = paths[3].read_text(encoding="utf-8")
    assert "ref: " + SHA in retraction
    assert "<TOOLING_SHA>" not in retraction
    assert read_workflow(paths[3])["name"] == "Retraction watch"


def test_generator_renders_an_unregistered_candidate(tmp_path: Path) -> None:
    """Candidate CI needs one collection, no registry release and no plugin caller."""
    paths = render_domain_ci.render(
        manifest_fixture(tmp_path), "new-domain", SHA, REPO / "scripts" / "templates",
        tmp_path / "candidate", stage="candidate", collection_path="collections/new-domain/v1",
    )
    assert [path.name for path in paths] == ["gates.yml", "intake.yml", "retraction-watch.yml"]
    assert not (tmp_path / "candidate/plugin-validate.yml").exists()
    text = paths[0].read_text(encoding="utf-8")
    assert "# candidate stage: rendered before the first registry release; re-render after registration" in text
    document = read_workflow(paths[0])
    assert document["jobs"]["released-collections"]["strategy"]["matrix"]["collection"] == [
        {"domain": "new-domain", "collection_path": "collections/new-domain/v1", "receipts_path": ""}
    ]
    assert read_workflow(paths[1])["name"] == "Paper issue intake"
    assert read_workflow(paths[2])["name"] == "Retraction watch"


def test_candidate_rendering_removes_a_stale_plugin_caller(tmp_path: Path) -> None:
    """Rerendering at candidate stage does not leave the released plugin caller behind."""
    output = tmp_path / "out"
    render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", output
    )
    assert (output / "plugin-validate.yml").is_file()
    paths = render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", output,
        stage="candidate", collection_path="collections/fixture/v3",
    )
    assert [path.name for path in paths] == ["gates.yml", "intake.yml", "retraction-watch.yml"]
    assert not (output / "plugin-validate.yml").exists()


def test_candidate_requires_a_collection_path(tmp_path: Path) -> None:
    """The candidate matrix cannot invent a collection location."""
    try:
        render_domain_ci.render(
            manifest_fixture(tmp_path), "new-domain", SHA, REPO / "scripts" / "templates",
            tmp_path / "candidate", stage="candidate",
        )
    except ValueError as exc:
        assert "candidate stage requires --collection-path" in str(exc)
    else:
        raise AssertionError("candidate rendering without a collection path must fail")


def test_candidate_cli_accepts_an_unregistered_domain(tmp_path: Path) -> None:
    """The CLI exposes the same candidate contract as the in-process renderer."""
    result = subprocess.run(
        [PYTHON, str(REPO / "scripts/render_domain_ci.py"), "--manifest", str(manifest_fixture(tmp_path)),
         "--domain", "new-domain", "--tooling-sha", SHA, "--stage", "candidate",
         "--collection-path", "collections/new-domain/v1", "--out", str(tmp_path / "candidate")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not (tmp_path / "candidate/plugin-validate.yml").exists()
    assert (tmp_path / "candidate/retraction-watch.yml").is_file()


def test_candidate_rejects_a_malformed_collection_path(tmp_path: Path) -> None:
    """The candidate path is one concrete versioned directory, not a prefix."""
    import pytest
    with pytest.raises(ValueError, match="collection path"):
        render_domain_ci.candidate_release("fixture", "collections/fixture/v1/../../other")


def test_generator_cli_rejects_a_legacy_only_domain(tmp_path: Path) -> None:
    """An empty current-release matrix is an error, not a green empty job."""
    result = subprocess.run(
        [PYTHON, str(REPO / "scripts" / "render_domain_ci.py"), "--manifest", str(manifest_fixture(tmp_path)),
         "--domain", "old", "--tooling-sha", SHA, "--out", str(tmp_path / "out")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2
    assert "no non-legacy releases" in result.stderr
    assert not (tmp_path / "out").exists()


def test_local_rehearsal_runs_on_the_router_fixture(tmp_path: Path) -> None:
    """The local shell entry point completes every offline fixture gate."""
    collection = subprocess.run(
        [PYTHON, str(REPO / "tests" / "helpers" / "prepare_gate_fixture.py"),
         str(REPO / "tests" / "fixtures" / "router_collection"), str(tmp_path)],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert Path(collection).is_dir()
    result = subprocess.run(
        ["bash", str(REPO / "scripts" / "run_domain_gates.sh"), str(REPO), str(tmp_path), "collections/fixture/v1"],
        capture_output=True, text=True, check=False,
        env={"PATH": str(Path(PYTHON).parent) + ":/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "11 passed, 0 failed" in result.stdout


def test_local_rehearsal_help_is_successful_and_truthful() -> None:
    """The onboarding discovery command is not mistaken for a gate failure."""
    result = subprocess.run(
        ["bash", str(REPO / "scripts" / "run_domain_gates.sh"), "--help"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0
    assert "<tooling-root> <content-root> <collection_path>" in result.stdout
    assert "--strict" in result.stdout and "advisory" in result.stdout


def test_receipt_verification_is_read_only(tmp_path: Path) -> None:
    """A supplied external receipt verifies after the advisory content gate."""
    subprocess.run(
        [PYTHON, str(REPO / "tests" / "helpers" / "prepare_gate_fixture.py"),
         str(REPO / "tests" / "fixtures" / "router_collection"), str(tmp_path)],
        check=True, capture_output=True, text=True,
    )
    collection = tmp_path / "collections" / "fixture" / "v1"
    receipts = tmp_path / "receipts" / "current"
    receipts.mkdir(parents=True)
    receipt = receipts / "gate_report.json"
    subprocess.run(
        [PYTHON, str(REPO / "scripts" / "release_gate.py"), str(collection), "--strict", "--report", str(receipt)],
        check=True, capture_output=True, text=True,
    )
    before = receipt.read_bytes()
    result = subprocess.run(
        ["bash", str(REPO / "scripts" / "run_domain_gates.sh"), str(REPO), str(tmp_path),
         "collections/fixture/v1", "receipts/current"],
        capture_output=True, text=True, check=False,
        env={"PATH": str(Path(PYTHON).parent) + ":/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "12 passed, 0 failed" in result.stdout
    assert "Strict receipt and target re-verified" in result.stdout
    assert receipt.read_bytes() == before


def test_renderer_preserves_the_registry_release_commit_comment(tmp_path: Path) -> None:
    """The rendered caller retains the instruction linking SHA and registry."""
    output = tmp_path / "out"
    render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", output
    )
    text = (output / "gates.yml").read_text(encoding="utf-8")
    assert "collections.yaml" in text
    assert "collections/fixture/v1" not in text


def test_generator_applies_an_explicit_receipt_map(tmp_path: Path) -> None:
    """Receipt pins come from the caller when the registry does not record them."""
    receipts = {"collections/fixture/v2": "receipts/current"}
    paths = render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", tmp_path / "out", receipts
    )
    document = read_workflow(paths[0])
    rows = document["jobs"]["released-collections"]["strategy"]["matrix"]["collection"]
    assert rows[0]["receipts_path"] == ""
    assert rows[1]["receipts_path"] == "receipts/current"


def test_intake_template_renders_both_placeholders_and_exact_permissions(tmp_path: Path) -> None:
    """The intake caller names its domain, pin and only the three write scopes."""
    paths = render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", tmp_path / "out"
    )
    text = (tmp_path / "out" / "intake.yml").read_text(encoding="utf-8")
    assert "<TOOLING_SHA>" not in text
    assert "<DOMAIN>" not in text
    document = read_workflow(tmp_path / "out" / "intake.yml")
    assert document["permissions"] == {
        "contents": "write",
        "pull-requests": "write",
        "issues": "write",
    }
    assert document["concurrency"] == {
        "group": "intake-fixture-${{ github.event.issue.number }}",
        "cancel-in-progress": False,
    }
    trigger = document[workflow_key(document)]["issues"]
    assert trigger["types"] == ["opened", "edited", "reopened", "labeled"]
    job = document["jobs"]["intake"]
    assert job["if"].count("contains(github.event.issue.labels.*.name") == 2
    assert "'propose'" in job["if"]
    assert "'paper-intake'" in job["if"]
    checkouts = [step for step in job["steps"] if step.get("uses", "").startswith("actions/checkout@")]
    assert [step["with"]["path"] for step in checkouts] == ["content", "tooling"]
    assert checkouts[1]["with"]["repository"] == "HolobiomicsLab/asb-skill-collections"
    assert checkouts[1]["with"]["ref"] == SHA
    assert paths[2].name == "intake.yml"


def test_intake_template_keeps_issue_text_out_of_shell_interpolation() -> None:
    """The issue body reaches the core as a file, never as a shell string."""
    text = (REPO / "scripts" / "templates" / "domain-intake.yml").read_text(encoding="utf-8")
    assert "github.event.issue.body" not in text
    assert "github.event.issue.title" not in text
    assert "gh issue view" in text
    assert "issue.json" in text
    assert "actions/checkout@v7" in text
    assert "cancel-in-progress: false" in text


def test_intake_template_passes_actionlint_when_available(tmp_path: Path) -> None:
    """The rendered caller is a valid workflow for actionlint when installed."""
    render_domain_ci.render(
        manifest_fixture(tmp_path), "fixture", SHA, REPO / "scripts" / "templates", tmp_path / "out"
    )
    if shutil.which("actionlint") is None:
        import pytest
        pytest.skip("actionlint is not installed on PATH")
    result = subprocess.run(
        ["actionlint", str(tmp_path / "out" / "intake.yml")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
