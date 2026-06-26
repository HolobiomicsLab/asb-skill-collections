import json, pathlib, sys, textwrap
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import enrich_tools_index as e


# corpus_by_doi maps doi -> full paper dict (as corpus.yaml papers are shaped).
CORPUS = {
    "10.1/open": {
        "doi": "10.1/open", "license_tier": "open",
        "access": {"license": "MIT"}, "license_detection": "github-api",
    },
    "10.1/restricted": {
        "doi": "10.1/restricted", "license_tier": "restricted",
        "access": {"license": None}, "license_detection": "none",
    },
    "10.1/nc": {
        "doi": "10.1/nc", "license_tier": "noncommercial",
        "access": {"license": "CC-BY-NC-4.0"}, "license_detection": "readme-llm",
    },
}


def test_tool_license_single_match():
    assert e.tool_license(["10.1/open"], CORPUS) == ("open", "MIT", "github-api")


def test_tool_license_most_restrictive_rollup():
    # open + noncommercial -> noncommercial (the most restrictive of the two),
    # and the returned license/detection come from the most-restrictive paper.
    tier, lic, det = e.tool_license(["10.1/open", "10.1/nc"], CORPUS)
    assert tier == "noncommercial"
    assert lic == "CC-BY-NC-4.0"
    assert det == "readme-llm"


def test_tool_license_restricted_when_unmatched():
    assert e.tool_license(["10.1/does-not-exist"], CORPUS) == ("restricted", None, None)
    assert e.tool_license([], CORPUS) == ("restricted", None, None)


def test_link_maps_mutual_inversion():
    skills_index = [
        {"slug": "s_open", "dois": ["10.1/open"]},
        {"slug": "s_both", "dois": ["10.1/open", "10.1/nc"]},
        {"slug": "s_none", "dois": ["10.1/unmatched"]},
    ]
    tools_index = [
        {"slug": "t_open", "dois": ["10.1/open"]},
        {"slug": "t_nc", "dois": ["10.1/nc"]},
    ]
    tools_used, used_by = e.link_maps(skills_index, tools_index)
    # s_open shares a DOI with t_open only
    assert tools_used["s_open"] == ["t_open"]
    # s_both shares DOIs with both tools
    assert tools_used["s_both"] == ["t_nc", "t_open"]
    # s_none matches nothing
    assert tools_used["s_none"] == []
    # inverse map
    assert used_by["t_open"] == ["s_both", "s_open"]
    assert used_by["t_nc"] == ["s_both"]
    # mutual inversion invariant: t in tools_used[s]  <=>  s in used_by[t]
    for s, ts in tools_used.items():
        for t in ts:
            assert s in used_by[t]
    for t, ss in used_by.items():
        for s in ss:
            assert t in tools_used[s]


def _write_collection(tmp_path):
    d = tmp_path
    (d / "corpus.yaml").write_text(textwrap.dedent("""
        papers:
        - {doi: 10.1/open, license_tier: open, license_detection: github-api, access: {license: MIT}}
        - {doi: 10.1/restricted, license_tier: restricted, license_detection: none, access: {license: null}}
        - {doi: 10.1/nc, license_tier: noncommercial, license_detection: readme-llm, access: {license: CC-BY-NC-4.0}}
    """))
    (d / "tools_index.json").write_text(json.dumps([
        {"slug": "t_open", "name": "ToolOpen", "dois": ["10.1/open"]},
        {"slug": "t_mix", "name": "ToolMix", "dois": ["10.1/open", "10.1/nc"]},
        {"slug": "t_unmatched", "name": "ToolU", "dois": ["10.1/ghost"]},
    ], indent=2))
    (d / "skills_index.json").write_text(json.dumps([
        {"slug": "s1", "dois": ["10.1/open"]},
        {"slug": "s2", "dois": ["10.1/nc"]},
    ], indent=2))
    (d / "kb_bundle.json").write_text(json.dumps({
        "skills": {
            "s1": {"dois": ["10.1/open"]},
            "s2": {"dois": ["10.1/nc"]},
        }
    }, indent=2))
    return d


def test_enrich_writes_back_all_fields(tmp_path):
    d = _write_collection(tmp_path)
    summary = e.enrich(str(d))

    tools = {t["slug"]: t for t in json.loads((d / "tools_index.json").read_text())}
    # most-restrictive rollup on the mixed tool
    assert tools["t_open"]["license_tier"] == "open"
    assert tools["t_open"]["license"] == "MIT"
    assert tools["t_open"]["license_detection"] == "github-api"
    assert tools["t_mix"]["license_tier"] == "noncommercial"
    # restricted-when-unmatched
    assert tools["t_unmatched"]["license_tier"] == "restricted"
    assert tools["t_unmatched"]["license"] is None
    assert tools["t_unmatched"]["license_detection"] is None
    # used_by_skills populated by DOI intersection
    assert tools["t_open"]["used_by_skills"] == ["s1"]
    assert tools["t_mix"]["used_by_skills"] == ["s1", "s2"]
    assert tools["t_unmatched"]["used_by_skills"] == []

    # skills_index gets tools_used (sorted)
    si = {s["slug"]: s for s in json.loads((d / "skills_index.json").read_text())}
    assert si["s1"]["tools_used"] == ["t_mix", "t_open"]
    assert si["s2"]["tools_used"] == ["t_mix"]

    # kb_bundle skill records get tools_used too
    kb = json.loads((d / "kb_bundle.json").read_text())["skills"]
    assert kb["s1"]["tools_used"] == ["t_mix", "t_open"]
    assert kb["s2"]["tools_used"] == ["t_mix"]

    # summary
    assert summary["tools"] == 3
    assert summary["skills_linked"] == 2
    assert summary["tool_tiers"]["open"] == 1
    assert summary["tool_tiers"]["noncommercial"] == 1
    assert summary["tool_tiers"]["restricted"] == 1


def test_enrich_idempotent(tmp_path):
    d = _write_collection(tmp_path)
    e.enrich(str(d))
    after_first = {
        "tools": (d / "tools_index.json").read_text(),
        "skills": (d / "skills_index.json").read_text(),
        "kb": (d / "kb_bundle.json").read_text(),
    }
    summary2 = e.enrich(str(d))
    after_second = {
        "tools": (d / "tools_index.json").read_text(),
        "skills": (d / "skills_index.json").read_text(),
        "kb": (d / "kb_bundle.json").read_text(),
    }
    assert after_first == after_second
    assert summary2["tools"] == 3


def test_enrich_preserves_indent(tmp_path):
    d = tmp_path
    (d / "corpus.yaml").write_text("papers:\n- {doi: 10.1/open, license_tier: open, license_detection: github-api, access: {license: MIT}}\n")
    # 4-space indented tools_index
    (d / "tools_index.json").write_text('[\n    {\n        "slug": "t_open",\n        "dois": ["10.1/open"]\n    }\n]')
    (d / "skills_index.json").write_text('[\n    {\n        "slug": "s1",\n        "dois": ["10.1/open"]\n    }\n]')
    (d / "kb_bundle.json").write_text('{\n  "skills": {\n    "s1": {\n      "dois": ["10.1/open"]\n    }\n  }\n}')
    e.enrich(str(d))
    tools_text = (d / "tools_index.json").read_text()
    assert '\n    {\n' in tools_text, "tools_index should preserve 4-space indent"
    kb_text = (d / "kb_bundle.json").read_text()
    assert '\n  "skills"' in kb_text, "kb_bundle should preserve 2-space indent"
