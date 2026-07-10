"""Gate 9 (indicium round-trip) must advertise itself as inert, not enforced.

The verify-claims CLI ships in indicium-adapters, which is not on PyPI, so the gate
never runs in public CI. It must therefore emit a GitHub ::warning:: annotation and
say plainly that it did not run — a bare `exit 0` would let a green Validate read as
if an enforced gate passed. This guards that honest labelling (the `gate9-inert` item).
"""
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"


def _gate9_step() -> str:
    """Return the gate-9 section (its comment block + the step body)."""
    text = VALIDATE.read_text()
    start_marker = "# -- Gate 9:"
    assert start_marker in text, "gate-9 section comment not found"
    start = text.index(start_marker)
    rest = text[start:]
    # the section runs until the next `# -- Gate` banner (Gate 1 / LinkML follows)
    nxt = rest.find("\n      # -- Gate", 1)
    return rest if nxt == -1 else rest[:nxt]


def test_gate9_emits_a_warning_annotation():
    step = _gate9_step()
    assert "::warning" in step, "gate 9 must emit a ::warning:: annotation when inert"


def test_gate9_says_it_did_not_run():
    step = _gate9_step().lower()
    assert "did not run" in step or "not enforced" in step, (
        "gate 9 must state plainly that it did not run / is not enforced"
    )


def test_gate9_points_at_the_register_item():
    assert "gate9-inert" in _gate9_step(), "gate 9 must reference the gate9-inert register item"


def test_header_marks_gate9_warn_only():
    header = VALIDATE.read_text()[:1200]
    assert "9." in header and "WARN-ONLY" in header, (
        "the gate list must mark gate 9 as WARN-ONLY, not a plain implemented gate"
    )


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
