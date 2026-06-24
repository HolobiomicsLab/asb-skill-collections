import json, pathlib, sys, textwrap, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import propagate_license_tiers as p
from scripts import license_tier as lt


def test_corpus_tier_by_doi(tmp_path):
    c = tmp_path / "corpus.yaml"
    c.write_text(textwrap.dedent('''
        papers:
        - {name: A, doi: 10.1/a, repo_url: https://github.com/a/b, license_tier: noncommercial, access: {license: CC-BY-NC-4.0}}
        - {name: B, doi: 10.1/b, license_tier: open, access: {license: MIT}}
    '''))
    m = p.corpus_tier_by_doi(str(c))
    assert m["10.1/a"]["tier"] == "noncommercial" and m["10.1/a"]["license"] == "CC-BY-NC-4.0"

def test_skill_tier_most_restrictive():
    tiers = {"10.1/a": {"tier": "open"}, "10.1/b": {"tier": "noncommercial"}}
    assert p.skill_tier(["10.1/a", "10.1/b"], tiers) == "noncommercial"
    assert p.skill_tier(["10.1/a"], tiers) == "open"
    assert p.skill_tier(["10.1/unknown"], tiers) == "open"   # unknown -> open
    assert p.skill_tier([], tiers) == "open"

def test_propagate_indices(tmp_path):
    si = tmp_path / "skills_index.json"
    si.write_text(json.dumps([
        {"slug": "s1", "dois": ["10.1/a"]},
        {"slug": "s2", "dois": ["10.1/b"]},
    ]))
    kb = tmp_path / "kb_bundle.json"
    kb.write_text(json.dumps({"skills": {"s1": {"dois": ["10.1/a"]}, "s2": {"dois": ["10.1/b"]}}}))
    tiers = {"10.1/a": {"tier": "noncommercial"}, "10.1/b": {"tier": "open"}}
    summary = p.propagate_indices(str(si), str(kb), tiers)
    out_si = {e["slug"]: e["license_tier"] for e in json.loads(si.read_text())}
    out_kb = {k: v["license_tier"] for k, v in json.loads(kb.read_text())["skills"].items()}
    assert out_si == {"s1": "noncommercial", "s2": "open"}
    assert out_kb == {"s1": "noncommercial", "s2": "open"}
    assert summary == {"noncommercial": 1, "open": 1}

def test_tool_license_block_consistency():
    b = p.tool_license_block("noncommercial", "CC-BY-NC-4.0", "https://github.com/x/y")
    assert b["tier"] == "noncommercial"
    assert b["requires_ack"] == lt.ack_required("noncommercial") is True
    assert b["ref"] == "CC-BY-NC-4.0" and b["url"] == "https://github.com/x/y"
