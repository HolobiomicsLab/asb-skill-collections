"""Every shipped unit vendors the current binder, not the one it was built with.

`bin/perspicacite_kb_bind.py` is a copy of `scripts/perspicacite_kb_bind.py` taken
at build time, and it is the file an installed unit actually runs. Nothing compared
the two, so a binder change could land in the repository and never reach a consumer:
the non-open link-only guard (`5f79a87db`) did exactly that, staying inert in all
nine copies while every bundle record carried the `license_tier` it reads.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
SOURCE = ROOT / "scripts" / "perspicacite_kb_bind.py"


def _vendored():
    return sorted(ROOT.glob("collections/*/*/bin/perspicacite_kb_bind.py")) + sorted(
        ROOT.glob("packs/*/*/bin/perspicacite_kb_bind.py")
    )


def test_there_is_something_to_check():
    assert SOURCE.is_file()
    assert _vendored(), "no unit vendors the binder; this guard would be vacuous"


def test_every_vendored_binder_is_the_current_one():
    source = SOURCE.read_bytes()
    stale = [
        str(p.relative_to(ROOT)) for p in _vendored() if p.read_bytes() != source
    ]
    assert not stale, f"stale vendored binder(s): {stale}"
