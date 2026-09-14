"""Gate 8 (RO-Crate) must advertise itself as inert, for the same reason gate 9 does.

No collection in this repository ships an `ro-crate-metadata.json`, while all four
`collection.yaml` files declare `ro_crate_path: ro-crate-metadata.json`. The step
therefore validates zero files, and it used to print
"PASS: RO-Crate validation OK (0 crates checked)" — which reads, in the PR checks, the
way an enforced gate that passed reads. Gate 9's labelling discipline
(`tests/test_ci_gate_labelling.py`) is applied here to the second inert gate: say what
was measured, and emit a ::warning:: rather than a pass.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"


def _gate8_step() -> str:
    """Return the gate-8 section (its comment block + the step body)."""
    text = VALIDATE.read_text()
    start_marker = "# -- Gate 8:"
    assert start_marker in text, "gate-8 section comment not found"
    start = text.index(start_marker)
    rest = text[start:]
    nxt = rest.find("\n      # -- Gate", 1)
    return rest if nxt == -1 else rest[:nxt]


def test_gate8_emits_a_warning_when_there_is_no_crate_to_validate():
    step = _gate8_step()
    assert "::warning" in step, "gate 8 must emit a ::warning:: annotation when it finds no crate"


def test_gate8_says_it_did_not_run():
    step = _gate8_step().lower()
    assert "did not run" in step or "measured nothing" in step, (
        "gate 8 must state plainly that it validated nothing"
    )


def test_gate8_exits_before_reporting_a_pass_over_zero_crates():
    step = _gate8_step()
    assert "if not crate_files:" in step, (
        "gate 8 must branch on the empty case instead of falling through to its PASS line"
    )


def test_header_marks_gate8_warn_only():
    """The mark has to sit on gate 8's own entry, not merely somewhere above it."""
    header = VALIDATE.read_text().split("name: Validate", 1)[0]
    start = header.index("#   8.")
    entry = header[start:header.index("#   9.", start)]

    assert "WARN-ONLY" in entry, (
        "the gate list must mark gate 8 as WARN-ONLY, not a plain implemented gate"
    )


def test_no_collection_ships_the_crate_its_manifest_declares():
    """The premise of this file, asserted rather than assumed.

    If a crate is ever added, this test fails and gate 8 stops being inert — which
    is the moment to restore its enforced labelling.
    """
    crates = list((ROOT / "collections").rglob("ro-crate-metadata.json"))
    manifests = sorted((ROOT / "collections").rglob("collection.yaml"))
    declaring = [m for m in manifests if "ro_crate_path" in m.read_text()]

    assert manifests, "no collection manifest found"
    assert not crates, f"a crate now ships ({crates}); gate 8 is no longer inert"
    assert declaring == manifests, (
        "every collection manifest is expected to declare ro_crate_path; "
        f"{len(declaring)} of {len(manifests)} do"
    )


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
