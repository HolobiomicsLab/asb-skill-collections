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
    # Re-blessed: both of these asserted `open` until 2026-08-20. A DOI the corpus
    # does not know, and no DOI at all, are the same state -- nothing established
    # the tier -- and `open` is the most permissive answer available to guess.
    assert p.skill_tier(["10.1/unknown"], tiers) == p.UNESTABLISHED_TIER
    assert p.skill_tier([], tiers) == p.UNESTABLISHED_TIER

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

def test_propagate_preserves_indent(tmp_path):
    si = tmp_path / "skills_index.json"
    si.write_text('[\n {\n  "slug": "s1",\n  "dois": ["10.1/a"]\n }\n]')   # 1-space indent
    kb = tmp_path / "kb_bundle.json"
    kb.write_text('{\n  "skills": {\n    "s1": {\n      "dois": ["10.1/a"]\n    }\n  }\n}')  # 2-space
    tiers = {"10.1/a": {"tier": "open"}}
    p.propagate_indices(str(si), str(kb), tiers)

    si_text = si.read_text()
    kb_text = kb.read_text()

    # skills_index should preserve 1-space indent at array entry level
    assert '\n {\n' in si_text, "skills_index should have 1-space indent on opening brace"
    # Verify license_tier was added
    assert json.loads(si_text)[0]["license_tier"] == "open"

    # kb_bundle should preserve 2-space indent at top level
    assert '\n  "skills"' in kb_text, "kb_bundle should have 2-space indent on top-level keys"
    # Verify license_tier was added
    assert json.loads(kb_text)["skills"]["s1"]["license_tier"] == "open"

def test_tool_license_block_consistency():
    b = p.tool_license_block("noncommercial", "CC-BY-NC-4.0", "https://github.com/x/y")
    assert b["tier"] == "noncommercial"
    assert b["requires_ack"] == lt.ack_required("noncommercial") is True
    assert b["ref"] == "CC-BY-NC-4.0" and b["url"] == "https://github.com/x/y"


# --- an unestablished tier must never be reported as the most permissive one --

def test_a_skill_with_no_doi_does_not_become_open():
    """`open` was the old default. asb-metabolomics tells agents to default
    discovery to open-tier skills, so guessing open advertises an unchecked
    tool as free to use."""
    assert p.skill_tier([], {}) == p.UNESTABLISHED_TIER
    assert p.skill_tier(None, {}) != "open"


def test_a_skill_with_no_doi_uses_its_own_declared_tier():
    assert p.skill_tier([], {}, declared="noncommercial") == "noncommercial"
    assert p.skill_tier([], {}, declared="open") == "open"


def test_a_nonsense_declared_tier_falls_back_to_the_safe_answer():
    assert p.skill_tier([], {}, declared="probably-fine") == p.UNESTABLISHED_TIER


def test_a_doi_derived_tier_still_wins_over_the_declaration():
    """The other side: the corpus is authoritative where it has an answer."""
    tiers = {"10.1/a": {"tier": "restricted"}}
    assert p.skill_tier(["10.1/a"], tiers, declared="open") == "restricted"


def test_the_most_restrictive_doi_still_governs():
    tiers = {"10.1/a": {"tier": "open"}, "10.2/b": {"tier": "noncommercial"}}
    assert p.skill_tier(["10.1/a", "10.2/b"], tiers) == "noncommercial"


def test_declared_tiers_reads_a_router_shaped_collection(tmp_path):
    col = tmp_path / "c"
    (col / "leaves" / "nc-tool").mkdir(parents=True)
    (col / "leaves" / "nc-tool" / "SKILL.md").write_text(
        "---\nname: nc-tool\nmetadata:\n  tool_license:\n    tier: noncommercial\n---\nbody\n",
        encoding="utf-8")
    (col / "leaves" / "plain").mkdir()
    (col / "leaves" / "plain" / "SKILL.md").write_text(
        "---\nname: plain\nmetadata: {}\n---\nbody\n", encoding="utf-8")
    found = p.declared_tiers(col)
    assert found == {"nc-tool": "noncommercial"}, "only a declared tier counts"


def test_declared_tiers_survives_a_malformed_skill(tmp_path):
    col = tmp_path / "c"
    (col / "leaves" / "broken").mkdir(parents=True)
    (col / "leaves" / "broken" / "SKILL.md").write_text("no fence here\n", encoding="utf-8")
    assert p.declared_tiers(col) == {}
