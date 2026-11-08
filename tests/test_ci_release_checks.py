"""The surviving CITATION and plugin-manifest jobs of validate.yml."""

import pathlib
import re

import pytest

yaml = pytest.importorskip("yaml")

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"


def _jobs():
    return yaml.safe_load(VALIDATE.read_text(encoding="utf-8"))["jobs"]


def _step(job, name_part):
    found = [step for step in job["steps"] if name_part in step.get("name", "")]
    assert len(found) == 1
    return found[0]


def test_cffconvert_is_pinned_in_its_own_environment():
    install = _step(_jobs()["citation"], "Install cffconvert")["run"]
    assert 'python -m venv "$RUNNER_TEMP/cffconvert"' in install
    assert '"cffconvert==2.0.0"' in install


def test_the_root_citation_file_is_validated():
    run = _step(_jobs()["citation"], "Validate the root")["run"]
    assert '"$RUNNER_TEMP/cffconvert/bin/cffconvert" --validate -i CITATION.cff' in run
    assert "git ls-files" not in run
    assert "legacy" not in run


def test_gate10_is_the_strict_plugin_validator():
    run = _step(_jobs()["plugin-manifest"], "Validate the marketplace")["run"].strip()
    assert run == "claude plugin validate --strict .claude-plugin/marketplace.json"


def test_the_validator_is_a_pinned_release_on_a_node_it_supports():
    job = _jobs()["plugin-manifest"]
    install = _step(job, "Install Claude Code")["run"]
    assert re.search(r'"@anthropic-ai/claude-code@\d+\.\d+\.\d+"', install)
    node = _step(job, "Node.js")["with"]["node-version"]
    assert int(str(node).split(".")[0]) >= 22


def test_the_release_check_jobs_only_read_the_repository():
    for name in ("citation", "plugin-manifest"):
        assert _jobs()[name].get("permissions") == {"contents": "read"}


def test_no_release_check_hides_behind_continue_on_error():
    for name in ("citation", "plugin-manifest"):
        job = _jobs()[name]
        assert "continue-on-error" not in job
        for step in job["steps"]:
            assert "continue-on-error" not in step
