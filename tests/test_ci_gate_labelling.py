"""The description lint enforces its rules directly on fixture trees."""

import os
import pathlib
import shlex
import subprocess
import sys

import yaml

from scripts import lint_skill_descriptions


def _skill(root, slug, description):
    directory = root / "skills" / slug
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\n{yaml.safe_dump({'description': description})}---\n", encoding="utf-8"
    )


def test_lint_accepts_a_bounded_use_when_description(tmp_path):
    _skill(tmp_path, "valid", "Use when testing a skill description in a compact fixture tree.")
    assert lint_skill_descriptions.lint([tmp_path]) == []
    assert lint_skill_descriptions.main([str(tmp_path)]) == 0


def test_lint_rejects_an_invalid_description(tmp_path):
    _skill(tmp_path, "invalid", "Best tool.")
    failures = lint_skill_descriptions.lint([tmp_path])
    assert len(failures) == 3
    assert any("description must start" in failure for failure in failures)
    assert any("description too short" in failure for failure in failures)
    assert any("marketing term" in failure for failure in failures)
    assert lint_skill_descriptions.main([str(tmp_path)]) == 1


ROOT = pathlib.Path(__file__).parent.parent
DOMAIN_TEMPLATE = ROOT / "scripts" / "templates" / "domain-plugin-validate.yml"


def _gate9_script():
    workflow = yaml.safe_load(DOMAIN_TEMPLATE.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["claim-verification"]["steps"]
    return next(step["run"] for step in steps if step.get("name") == "Gate 9: verify declared claims")


def test_gate9_template_is_enforced_and_version_pinned():
    text = DOMAIN_TEMPLATE.read_text(encoding="utf-8")
    assert "9. Indicium claim verification" in text[:300]
    assert "Gate 9: Indicium claim verification (enforced)" in text
    assert '"indicium-adapters[asb]>=0.6,<0.7"' in text
    assert "continue-on-error" not in text
    assert "WARN-ONLY" not in text


def _write_claim_fixture(root, claims):
    skill = root / "collections" / "example" / "v1" / "leaves" / "fixture" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\n" + yaml.safe_dump({"name": "fixture", "claims": claims}) + "---\n",
        encoding="utf-8",
    )


def _write_verifier_stub(root):
    bin_dir = root / "bin"
    bin_dir.mkdir()
    python3 = bin_dir / "python3"
    python3.write_text(
        f"#!/bin/sh\nexec {shlex.quote(sys.executable)} \"$@\"\n",
        encoding="utf-8",
    )
    python3.chmod(0o755)
    executable = bin_dir / "verify-claims"
    executable.write_text(
        "#!/bin/sh\nprintf '%s\\n' \"$VERIFY_CLAIMS_OUTPUT\"\nexit \"$VERIFY_CLAIMS_STATUS\"\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    return bin_dir


def test_gate9_decision_logic_offline(tmp_path, monkeypatch):
    bin_dir = _write_verifier_stub(tmp_path)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ['PATH']}")
    monkeypatch.setenv("RUNNER_TEMP", str(tmp_path))

    cases = [
        (["https://example.org/claim/1", "https://example.org/claim/2"],
         '{"unresolved":[{"claim_iri":"https://example.org/claim/2"}],"resolved_count":1}',
         "1", 0, "resolved 1 of 2 declared claim(s)"),
        (["https://example.org/claim/1"],
         '{"unresolved":[{"claim_iri":"https://example.org/claim/1"}],"resolved_count":0}',
         "1", 1, "declares 1 claim(s), but none resolved"),
        ([], "stub must not run", "99", 0, "nothing to verify"),
    ]

    for claims, output, status, expected_status, message in cases:
        case_root = tmp_path / f"case-{len(claims)}-{expected_status}"
        _write_claim_fixture(case_root, claims)
        environment = {
            **os.environ,
            "VERIFY_CLAIMS_OUTPUT": output,
            "VERIFY_CLAIMS_STATUS": status,
        }
        result = subprocess.run(
            ["bash", "-c", _gate9_script()], cwd=case_root,
            env=environment, capture_output=True, text=True, check=False,
        )
        assert result.returncode == expected_status, result.stdout + result.stderr
        assert message in result.stdout
