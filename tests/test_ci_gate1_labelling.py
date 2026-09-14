"""Gate 1 (LinkML) must say it did not run, instead of failing where nobody looks.

The step ran `linkml-validate --schema asb_skill_bundle.yaml` against a path that
exists nowhere in this repository, so every run printed
"FAIL: LinkML validation failures" once per collection and exited 1 — and
`continue-on-error: true` turned that into a green Validate. Measured on the last
green run on `main` (33977932675, 2026-09-05): four failures, all of them
"Error: Invalid value for '-s' / '--schema': File 'asb_skill_bundle.yaml' does not
exist.", job conclusion `success`. No `collection.yaml` has ever been validated
against the schema, while `docs/RELEASE_TRAIN_v0.md` listed the gate as blocking.

Same discipline as gates 8 and 9: name what was measured, warn, and do not leave a
red step inside a green job.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"
SCHEMA_NAME = "asb_skill_bundle.yaml"


def _gate1_step() -> str:
    """Return the gate-1 section (its comment block + the step body)."""
    text = VALIDATE.read_text()
    start_marker = "# -- Gate 1:"
    assert start_marker in text, "gate-1 section comment not found"
    start = text.index(start_marker)
    rest = text[start:]
    nxt = rest.find("\n      # -- Gate", 1)
    return rest if nxt == -1 else rest[:nxt]


def test_gate1_emits_a_warning_when_it_cannot_validate():
    step = _gate1_step()
    assert "::warning" in step, (
        "gate 1 must emit a ::warning:: annotation when no schema is resolvable"
    )


def test_gate1_says_it_did_not_run():
    step = _gate1_step().lower()
    assert "did not run" in step, "gate 1 must state plainly that it validated nothing"


def test_gate1_branches_on_the_missing_schema_before_it_validates():
    step = _gate1_step()
    assert "if schema is None:" in step, (
        "gate 1 must branch on an unresolvable schema instead of running "
        "linkml-validate against a path that does not exist"
    )


def test_gate1_resolves_the_schema_instead_of_assuming_a_checkout_path():
    step = _gate1_step()
    assert '"--schema", str(schema)' in step, (
        "gate 1 must pass the schema it resolved, not a fixed file name"
    )
    assert f'"--schema", "{SCHEMA_NAME}"' not in step, (
        "the hard-coded schema path is what failed on every run"
    )


def test_gate1_checks_the_cli_is_present():
    step = _gate1_step()
    assert 'shutil.which("linkml-validate")' in step, (
        "importing linkml_runtime does not put the linkml-validate CLI on PATH; "
        "without this guard the step dies on FileNotFoundError inside a green job"
    )


def test_header_marks_gate1_warn_only():
    """The mark has to sit on gate 1's own entry, not merely somewhere above it."""
    header = VALIDATE.read_text().split("name: Validate", 1)[0]
    start = header.index("#   1.")
    entry = header[start:header.index("#   2.", start)]

    assert "WARN-ONLY" in entry, (
        "the gate list must mark gate 1 as WARN-ONLY, not a plain implemented gate"
    )


def test_the_schema_gate1_needs_is_not_in_this_repository():
    """The premise of this file, asserted rather than assumed.

    `asb_skill_bundle.yaml` ships in the sibling `asb-schema` package. The day it
    is vendored here or published, this test fails — which is the moment to
    restore gate 1's enforced labelling.
    """
    found = [p for p in ROOT.rglob(SCHEMA_NAME) if ".git" not in p.parts]
    assert not found, f"the schema now ships here ({found}); gate 1 is no longer inert"


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
