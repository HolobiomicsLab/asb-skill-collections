"""Gate 8 (RO-Crate) must advertise itself as inert, for the same reason gate 9 does.

No collection in this repository ships an `ro-crate-metadata.json`. The four
`collection.yaml` files used to declare `ro_crate_path: ro-crate-metadata.json`
anyway; the field was dropped when the crate claim was retired, so nothing now points
at a file that does not exist. The step validates zero files, and it used to print
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


def test_no_crate_is_shipped_and_none_is_declared():
    """The premise of this file, asserted rather than assumed.

    Gate 8 is inert because there is nothing to validate *and* nothing claims there
    is. Either half changing is the moment to revisit the labelling: a crate
    appearing makes the gate real, and a manifest declaring `ro_crate_path` again
    re-creates the dangling path that dropping the field removed.
    """
    crates = list((ROOT / "collections").rglob("ro-crate-metadata.json"))
    manifests = sorted((ROOT / "collections").rglob("collection.yaml"))
    declaring = [m for m in manifests if "ro_crate_path" in m.read_text()]

    assert manifests, "no collection manifest found"
    assert not crates, f"a crate now ships ({crates}); gate 8 is no longer inert"
    assert not declaring, (
        "no collection manifest may declare ro_crate_path while no crate ships; "
        f"{[str(m.relative_to(ROOT)) for m in declaring]} do"
    )


def test_the_generator_does_not_reintroduce_the_field():
    """Dropping it from the four manifests is undone by the next generation run
    unless the generator stops writing it."""
    gen = (ROOT / "scripts" / "collect_metabolomics_collection.py").read_text()
    assert "ro_crate_path" not in gen, (
        "the collection generator still writes ro_crate_path; the field would come "
        "back on the next run"
    )


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
