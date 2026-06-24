import pathlib, sys, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import license_tier as lt

V2 = pathlib.Path(__file__).parent.parent / "collections/metabolomics/v2/skills"

def _frontmatter(skill_md: pathlib.Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    assert text.startswith("---\n"), skill_md
    fm = text.split("---\n", 2)[1]
    return yaml.safe_load(fm)

def test_masster_declares_noncommercial_gate():
    fm = _frontmatter(V2 / "masster" / "SKILL.md")
    tl = fm["metadata"]["tool_license"]
    assert tl["tier"] == "noncommercial"
    assert tl["requires_ack"] is True
    assert "Noncommercial" in tl["ref"]
    assert tl["url"].startswith("https://github.com/zamboni-lab/masster-dist")

def test_gate_flag_consistent_with_tier():
    fm = _frontmatter(V2 / "masster" / "SKILL.md")
    tl = fm["metadata"]["tool_license"]
    assert tl["requires_ack"] == lt.ack_required(tl["tier"])

def test_body_has_license_notice():
    text = (V2 / "masster" / "SKILL.md").read_text(encoding="utf-8")
    assert "## License notice" in text
    assert "noncommercial" in text.lower()
