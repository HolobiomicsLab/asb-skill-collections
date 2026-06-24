import pathlib

R = pathlib.Path(__file__).parent.parent / "collections/metabolomics/v2/skills/_router/SKILL.md"


def test_router_is_tier_aware():
    t = R.read_text().lower()
    assert "license_tier" in t
    assert "open" in t and "noncommercial" in t and "restricted" in t
    assert "acknowledg" in t or "ack" in t        # surfaces the NC gate
