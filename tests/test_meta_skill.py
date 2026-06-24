import pathlib
import yaml


META = pathlib.Path(__file__).parent.parent / "collections/metabolomics/v2/skills/asb-metabolomics/SKILL.md"


def _parts():
    text = META.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    fm, body = text.split("---\n", 2)[1], text.split("---\n", 2)[2]
    return yaml.safe_load(fm), body


def test_meta_skill_frontmatter_valid():
    fm, _ = _parts()
    assert fm["name"] == "asb-metabolomics"
    assert isinstance(fm.get("description"), str) and fm["description"]


def test_meta_skill_documents_router_and_gate():
    _, body = _parts()
    assert "_router" in body                      # hands off routing
    assert "tool_license" in body                 # reads the gate contract
    assert "acknowledg" in body.lower()           # runs the opt-in gate
    assert "link-only" in body.lower()            # states the grounding rule
