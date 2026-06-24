import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_license_tiers as c


def _collection(tmp_path, corpus_papers, si_entries, skills=None):
    d = tmp_path / "v"
    (d / "skills").mkdir(parents=True)
    (d / "corpus.yaml").write_text("papers:\n" + "".join(corpus_papers))
    (d / "skills_index.json").write_text(json.dumps(si_entries))
    for slug, fm in (skills or {}).items():
        (d / "skills" / slug).mkdir()
        (d / "skills" / slug / "SKILL.md").write_text(f"---\n{fm}---\nbody\n")
    return d

def test_clean_collection_passes(tmp_path):
    d = _collection(tmp_path,
        ["- {name: A, doi: 10.1/a, license_tier: open}\n"],
        [{"slug": "s1", "license_tier": "open"}])
    assert c.check_collection(str(d)) == []

def test_missing_tier_is_violation(tmp_path):
    d = _collection(tmp_path,
        ["- {name: A, doi: 10.1/a}\n"],                         # no license_tier
        [{"slug": "s1", "license_tier": "open"}])
    v = c.check_collection(str(d))
    assert any("license_tier" in x and "A" in x for x in v)

def test_inconsistent_ack_is_violation(tmp_path):
    d = _collection(tmp_path,
        ["- {name: A, doi: 10.1/a, license_tier: noncommercial}\n"],
        [{"slug": "s1", "license_tier": "noncommercial"}],
        skills={"s1": "name: s1\nmetadata:\n  tool_license:\n    tier: noncommercial\n    requires_ack: false\n"})
    v = c.check_collection(str(d))
    assert any("requires_ack" in x for x in v)

def test_missing_si_tier_is_violation(tmp_path):
    d = _collection(tmp_path,
        ["- {name: A, doi: 10.1/a, license_tier: open}\n"],   # corpus clean
        [{"slug": "s1"}])                                       # skills_index entry has no license_tier
    v = c.check_collection(str(d))
    assert any("license_tier" in x and "s1" in x for x in v)

def test_frontmatter_tier_mismatch_is_violation(tmp_path):
    d = _collection(tmp_path,
        ["- {name: A, doi: 10.1/a, license_tier: open}\n"],
        [{"slug": "s1", "license_tier": "restricted"}],
        skills={"s1": "name: s1\nmetadata:\n  license_tier: open\n"})   # SKILL says open, index says restricted
    v = c.check_collection(str(d))
    assert any("license_tier" in x and "s1" in x and ("mismatch" in x or "!=" in x or "index" in x) for x in v)
