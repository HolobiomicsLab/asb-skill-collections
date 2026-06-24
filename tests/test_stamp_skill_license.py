import pathlib, sys, yaml, json
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import stamp_skill_license as S

MARK = "<!-- asb-license-banner -->"

def _skill(tmp, slug, body="# t\n\nuse it.\n", meta=None):
    d = tmp/"skills"/slug; d.mkdir(parents=True)
    fm = {"name": slug, "license": "CC-BY-4.0", "metadata": (meta or {})}
    (d/"SKILL.md").write_text("---\n"+yaml.safe_dump(fm, sort_keys=False)+"---\n"+body)
    return d/"SKILL.md"

def test_banner_open_is_none():
    assert S.license_banner("open") is None

def test_banner_nonopen_has_marker_and_tier():
    for t in ("noncommercial","restricted"):
        b = S.license_banner(t)
        assert MARK in b and t in b and b.lstrip().startswith(">")

def test_stamp_open_sets_field_no_banner(tmp_path):
    md = _skill(tmp_path, "s-open")
    assert S.stamp_skill(md, "open") is True
    text = md.read_text(); fm = yaml.safe_load(text.split("---\n",2)[1])
    assert fm["metadata"]["license_tier"] == "open"
    assert MARK not in text

def test_stamp_restricted_adds_banner_after_h1(tmp_path):
    md = _skill(tmp_path, "s-r")
    S.stamp_skill(md, "restricted")
    text = md.read_text()
    assert yaml.safe_load(text.split("---\n",2)[1])["metadata"]["license_tier"] == "restricted"
    body = text.split("---\n",2)[2]
    assert MARK in body and body.index("# t") < body.index(MARK)   # banner after the H1

def test_stamp_is_idempotent(tmp_path):
    md = _skill(tmp_path, "s-r2")
    S.stamp_skill(md, "restricted")
    first = md.read_text()
    assert S.stamp_skill(md, "restricted") is False   # no change second time
    assert md.read_text() == first

def test_stamp_preserves_tool_license_block(tmp_path):
    md = _skill(tmp_path, "s-nc", meta={"tool_license": {"tier":"noncommercial","requires_ack":True,"ref":"X","url":"y"}})
    S.stamp_skill(md, "noncommercial")
    fm = yaml.safe_load(md.read_text().split("---\n",2)[1])
    assert fm["metadata"]["tool_license"]["requires_ack"] is True   # preserved
    assert fm["metadata"]["license_tier"] == "noncommercial"

def test_stamp_handles_null_metadata(tmp_path):
    d = tmp_path/"skills"/"s-null"; d.mkdir(parents=True)
    (d/"SKILL.md").write_text("---\nname: s-null\nmetadata:\n---\n# t\n\nbody.\n")
    assert S.stamp_skill(d/"SKILL.md", "open") is True
    fm = yaml.safe_load((d/"SKILL.md").read_text().split("---\n",2)[1])
    assert fm["metadata"]["license_tier"] == "open"

def test_stamp_all(tmp_path):
    _skill(tmp_path, "a"); _skill(tmp_path, "b")
    (tmp_path/"skills_index.json").write_text(json.dumps([
        {"slug":"a","license_tier":"open"},{"slug":"b","license_tier":"restricted"}]))
    res = S.stamp_all(str(tmp_path/"skills"), str(tmp_path/"skills_index.json"))
    assert res["tiers"] == {"open":1,"restricted":1}
