"""Gate 1 (LinkML) blocks once its schema is resolvable, and says so when it is not.

History. The step ran `linkml-validate --schema asb_skill_bundle.yaml` against a
path that exists nowhere in this repository, so every run printed
"FAIL: LinkML validation failures" once per collection and exited 1 — and
`continue-on-error: true` turned that into a green Validate. Measured on the last
green run on `main` (33977932675, 2026-09-05): four failures, all of them
"Error: Invalid value for '-s' / '--schema': File 'asb_skill_bundle.yaml' does not
exist.", job conclusion `success`. The first repair made the step say it did not
run. It also showed that the bundle schema was the wrong file, and that
`asb-schema` 0.2 could not validate the released manifests at all: they carry
seven keys (ten for `metabolomics/v2`) that its `SkillCollection` class did not
declare.

`asb-schema` 0.3.0 declares those keys. The gate now validates every
`collection.yaml` closed against `SkillCollection` in that schema and fails the
job when one does not validate. When the schema cannot be resolved, or resolves
to a version older than 0.3.0, it still says it did not run and exits 0.

The static tests pin the step's text. The behavioural tests run the step's own
script with a stand-in `linkml-validate` on PATH, so they need neither linkml nor
asb-schema and cannot pass vacuously when either is absent.
"""
import os
import pathlib
import re
import subprocess
import sys
import textwrap

import pytest

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"
SCHEMA_NAME = "asb_skill_collection.yaml"
OLD_SCHEMA_NAME = "asb_skill_bundle.yaml"


def _gate1_section() -> str:
    """Return the gate-1 section (its comment block + the step body)."""
    text = VALIDATE.read_text()
    start_marker = "# -- Gate 1:"
    assert start_marker in text, "gate-1 section comment not found"
    start = text.index(start_marker)
    rest = text[start:]
    nxt = rest.find("\n      # -- Gate", 1)
    return rest if nxt == -1 else rest[:nxt]


def _gate1_script() -> str:
    """Return the Python heredoc that gate 1 runs, dedented."""
    match = re.search(r"python - <<'EOF'\n(.*?)\n\s*EOF\n", _gate1_section(), re.S)
    assert match, "gate-1 python heredoc not found"
    return textwrap.dedent(match.group(1))


# -- static contract ----------------------------------------------------------


def test_gate1_is_not_behind_continue_on_error():
    assert not re.search(r"^\s*continue-on-error:", _gate1_section(), re.M), (
        "gate 1 must be able to fail the job once its schema resolves; "
        "continue-on-error is what kept a red step inside a green job"
    )


def test_gate1_installs_the_first_schema_that_matches_the_manifests():
    section = _gate1_section()
    assert '"asb-schema>=0.3.0"' in section, (
        "asb-schema 0.2 refuses every released manifest; the install must pin 0.3.0"
    )
    assert "--only-binary :all:" in section, (
        "install a wheel only, so no sdist build code runs in CI"
    )


def test_gate1_validates_the_collection_class_not_the_bundle_schema():
    section = _gate1_section()
    assert f'SCHEMA_NAME = "{SCHEMA_NAME}"' in section
    assert OLD_SCHEMA_NAME not in section, (
        f"{OLD_SCHEMA_NAME} describes skills, not collections"
    )
    assert '"--schema", str(schema)' in section, (
        "gate 1 must pass the schema it resolved, not a fixed file name"
    )
    assert '"--target-class", "SkillCollection"' in section, (
        "without a target class linkml-validate guesses the tree root"
    )


def test_gate1_warns_and_says_it_did_not_run():
    section = _gate1_section()
    assert "::warning" in section
    assert "did not run" in section.lower()
    assert "if schema is None:" in section


def test_gate1_checks_the_cli_is_present():
    assert 'shutil.which("linkml-validate")' in _gate1_section(), (
        "importing linkml_runtime does not put the linkml-validate CLI on PATH"
    )


def test_header_describes_gate1_as_it_now_behaves():
    """The description has to sit on gate 1's own entry, not merely somewhere above it."""
    header = VALIDATE.read_text().split("name: Validate", 1)[0]
    start = header.index("#   1.")
    entry = header[start:header.index("#   2.", start)]
    assert "BLOCKING once resolvable" in entry
    assert "WARN-ONLY until" in entry
    assert "0.3.0" in entry


def test_the_schema_gate1_needs_is_not_in_this_repository():
    """The premise of the did-not-run branch, asserted rather than assumed.

    The schema ships in the sibling `asb-schema` package. The day a copy lands
    here, gate 1 validates against that copy instead, and this test says so.
    """
    found = [p for p in ROOT.rglob(SCHEMA_NAME) if ".git" not in p.parts]
    assert not found, f"the schema now ships here ({found}); gate 1 resolves it first"


# -- behaviour, with a stand-in CLI --------------------------------------------

STUB_CLI = """\
#!{python}
import json, os, sys
with open(os.environ["STUB_LOG"], "a") as fh:
    fh.write(json.dumps(sys.argv[1:]) + "\\n")
if os.environ.get("STUB_FAIL_ON") and sys.argv[-1].endswith(os.environ["STUB_FAIL_ON"]):
    print("[ERROR] stand-in refusal", file=sys.stderr)
    sys.exit(1)
"""


@pytest.fixture
def workspace(tmp_path):
    pytest.importorskip("yaml")  # installed by the Validate job before pytest runs
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    cli = bin_dir / "linkml-validate"
    cli.write_text(STUB_CLI.format(python=sys.executable))
    cli.chmod(0o755)
    stubs = tmp_path / "stubs" / "linkml_runtime"
    stubs.mkdir(parents=True)
    (stubs / "__init__.py").write_text("")
    for slug in ("alpha/v1", "beta/v2"):
        manifest = tmp_path / "repo" / "collections" / slug / "collection.yaml"
        manifest.parent.mkdir(parents=True)
        manifest.write_text("id: x\n")
    (tmp_path / "repo" / "gate1.py").write_text(_gate1_script())
    return tmp_path


def _run(workspace, *, with_cli=True, extra_env=None):
    env = {
        "PATH": (str(workspace / "bin") + os.pathsep if with_cli else "") + "/usr/bin:/bin",
        "PYTHONPATH": str(workspace / "stubs"),
        "STUB_LOG": str(workspace / "calls.log"),
        "HOME": str(workspace),
    }
    env.update(extra_env or {})
    result = subprocess.run(
        [sys.executable, "gate1.py"], cwd=workspace / "repo",
        capture_output=True, text=True, env=env,
    )
    calls = (workspace / "calls.log").read_text().splitlines() if (workspace / "calls.log").exists() else []
    return result, calls


def _write_schema(workspace, version):
    (workspace / "repo" / SCHEMA_NAME).write_text(f'id: s\nversion: "{version}"\n')


def test_no_schema_warns_and_exits_zero(workspace):
    result, calls = _run(workspace)
    assert result.returncode == 0, result.stderr
    assert "GATE 1 DID NOT RUN" in result.stdout
    assert "::warning title=Gate 1 did not run::" in result.stdout
    assert calls == []


def test_a_schema_older_than_0_3_does_not_validate(workspace):
    _write_schema(workspace, "0.2.0")
    result, calls = _run(workspace)
    assert result.returncode == 0, result.stderr
    assert "declares version 0.2.0" in result.stdout
    assert calls == [], "0.2 refuses every released manifest; running it reports nothing new"


def test_a_missing_cli_warns_and_exits_zero(workspace):
    _write_schema(workspace, "0.3.0")
    result, calls = _run(workspace, with_cli=False)
    assert result.returncode == 0, result.stderr
    assert "linkml-validate CLI is not on PATH" in result.stdout
    assert calls == []


def test_every_manifest_is_validated_against_the_collection_class(workspace):
    _write_schema(workspace, "0.3.0")
    result, calls = _run(workspace)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("PASS: 2 collection.yaml files")
    assert len(calls) == 2
    schema = str((workspace / "repo" / SCHEMA_NAME).resolve())
    for call in calls:
        assert call.startswith(f'["--schema", "{schema}", "--target-class", "SkillCollection", ')


def test_one_refused_manifest_fails_the_step(workspace):
    _write_schema(workspace, "0.3.0")
    result, calls = _run(workspace, extra_env={"STUB_FAIL_ON": "beta/v2/collection.yaml"})
    assert result.returncode == 1
    assert "FAIL: 1 of 2 collection.yaml files do not validate" in result.stdout
    assert "stand-in refusal" in result.stdout
    assert len(calls) == 2, "a refusal must not stop the other manifests being checked"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
