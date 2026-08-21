import json, pathlib, sys, textwrap
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import enrich_tools_index as e


# --------------------------------------------------------------------------- #
# tool_license: evidence about the TOOL, or `unknown`. Never a paper's licence. #
# --------------------------------------------------------------------------- #

def test_a_tool_repository_lookup_yields_a_real_tier():
    assert e.tool_license({"license": "MIT", "license_detection": "github-api",
                           "repo_url": "owner/tool"}) == (
        "open", "MIT", "github-api", "tool", "owner/tool")


def test_the_resolved_repository_is_recorded_so_the_claim_can_be_disputed():
    """Every licence was previously unauditable: no entry named its source."""
    *_, repo = e.tool_license({"license": "GPL-2.0-or-later", "repo_url": "sneumann/xcms",
                               "license_detection": "bioconductor-package"})
    assert repo == "sneumann/xcms"


def test_an_r_description_lookup_yields_a_real_tier():
    tier, lic, det, subject, _ = e.tool_license(
        {"license": "GPL-3.0-only", "license_detection": "r-description"})
    assert (tier, lic, subject) == ("open", "GPL-3.0-only", "tool")
    assert det == "r-description"


def test_a_noncommercial_tool_licence_survives():
    tier, _, _, subject, _repo = e.tool_license(
        {"license": "CC-BY-NC-4.0", "license_detection": "license-file"})
    assert (tier, subject) == ("noncommercial", "tool")


def test_a_citing_papers_licence_is_never_the_tools_licence():
    """The #42 regression, both directions.

    A permissive paper must not make a GPL tool look permissive, and a CC-BY-NC-ND
    preprint must not make a BSD tool look academic-only.
    """
    for detection in ("crossref-paper", "biorxiv_api-paper", "unpaywall-paper"):
        for licence in ("Apache-2.0", "MIT", "CC-BY-4.0", "CC-BY-NC-ND-4.0"):
            tier, lic, _, subject, _repo = e.tool_license(
                {"license": licence, "license_detection": detection})
            assert tier == "unknown", f"{detection}/{licence} leaked onto the tool axis"
            assert lic is None and subject is None


def test_no_evidence_is_unknown_not_restricted():
    """`unknown` is an open question; `restricted` is a verdict. Not the same."""
    for evidence in (None, {}, {"license": None, "license_detection": "none"},
                     {"license": None, "license_detection": "file-present-unclassified"}):
        tier, lic, det, subject, repo = e.tool_license(evidence)
        assert tier == "unknown"
        assert lic is None and det is None and subject is None and repo is None


def test_source_paper_repos_reads_the_tool_yaml(tmp_path):
    tools = tmp_path / "tools"
    tools.mkdir()
    (tools / "camera.yaml").write_text(
        "name: CAMERA\nsource_repos:\n- b2slab/mWISE\n- LinShuhaiLAB/LipidIN\n")
    assert e.source_paper_repos("camera", tools) == ["LinShuhaiLAB/LipidIN", "b2slab/mWISE"]
    assert e.source_paper_repos("absent", tools) == []


# --------------------------------------------------------------------------- #
# link_maps                                                                    #
# --------------------------------------------------------------------------- #

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
    assert tools_used["s_open"] == ["t_open"]
    assert tools_used["s_both"] == ["t_nc", "t_open"]
    assert tools_used["s_none"] == []
    assert used_by["t_open"] == ["s_both", "s_open"]
    assert used_by["t_nc"] == ["s_both"]
    # mutual inversion invariant: t in tools_used[s]  <=>  s in used_by[t]
    for s, ts in tools_used.items():
        for t in ts:
            assert s in used_by[t]
    for t, ss in used_by.items():
        for s in ss:
            assert t in tools_used[s]


# --------------------------------------------------------------------------- #
# enrich                                                                       #
# --------------------------------------------------------------------------- #

def _write_collection(tmp_path, with_evidence=True):
    d = tmp_path
    (d / "corpus.yaml").write_text(textwrap.dedent("""
        papers:
        - {doi: 10.1/open, license_tier: open, license_detection: github-api, access: {license: MIT}}
        - {doi: 10.1/nc, license_tier: noncommercial, license_detection: crossref-paper, access: {license: CC-BY-NC-4.0}}
    """))
    (d / "tools_index.json").write_text(json.dumps([
        {"slug": "t_open", "name": "ToolOpen", "canonical_url": "https://github.com/some/citing-paper",
         "dois": ["10.1/open"]},
        {"slug": "t_mix", "name": "ToolMix", "dois": ["10.1/open", "10.1/nc"]},
        {"slug": "t_unmatched", "name": "ToolU", "dois": ["10.1/ghost"]},
    ], indent=2))
    (d / "skills_index.json").write_text(json.dumps([
        {"slug": "s1", "dois": ["10.1/open"]},
        {"slug": "s2", "dois": ["10.1/nc"]},
    ], indent=2))
    (d / "kb_bundle.json").write_text(json.dumps({
        "skills": {"s1": {"dois": ["10.1/open"]}, "s2": {"dois": ["10.1/nc"]}}
    }, indent=2))
    (d / "tools").mkdir(exist_ok=True)
    (d / "tools" / "t_open.yaml").write_text(
        "name: ToolOpen\nsource_repos:\n- some/citing-paper\n")
    if with_evidence:
        (d / "tool_licenses.json").write_text(json.dumps({
            "t_open": {"license": "GPL-3.0-only", "license_detection": "github-api",
                       "repo_url": "https://github.com/x/tool-open"}}))
    return d


def test_enrich_writes_back_all_fields(tmp_path):
    d = _write_collection(tmp_path)
    summary = e.enrich(str(d))
    tools = {t["slug"]: t for t in json.loads((d / "tools_index.json").read_text())}

    # A tool with its own repository lookup keeps a real tier, labelled as the tool's.
    assert tools["t_open"]["license_tier"] == "open"
    assert tools["t_open"]["license"] == "GPL-3.0-only"
    assert tools["t_open"]["license_subject"] == "tool"
    assert tools["t_open"]["repo_url"] == "https://github.com/x/tool-open"

    # A tool with no lookup of its own is unknown, however well-licensed its papers.
    for slug in ("t_mix", "t_unmatched"):
        assert tools[slug]["license_tier"] == "unknown"
        assert tools[slug]["license"] is None
        assert tools[slug]["license_subject"] is None
        assert tools[slug]["repo_url"] is None

    # The citing-paper repository is published under a name that says what it is.
    assert tools["t_open"]["source_paper_repos"] == ["some/citing-paper"]
    assert "canonical_url" not in tools["t_open"]
    assert tools["t_mix"]["source_paper_repos"] == []

    assert tools["t_open"]["used_by_skills"] == ["s1"]
    assert tools["t_mix"]["used_by_skills"] == ["s1", "s2"]
    assert tools["t_unmatched"]["used_by_skills"] == []

    si = {s["slug"]: s for s in json.loads((d / "skills_index.json").read_text())}
    assert si["s1"]["tools_used"] == ["t_mix", "t_open"]
    assert si["s2"]["tools_used"] == ["t_mix"]

    kb = json.loads((d / "kb_bundle.json").read_text())["skills"]
    assert kb["s1"]["tools_used"] == ["t_mix", "t_open"]
    assert kb["s2"]["tools_used"] == ["t_mix"]

    assert summary["tools"] == 3
    assert summary["skills_linked"] == 2
    assert summary["tool_tiers"] == {"open": 1, "unknown": 2}


def test_enrich_without_any_tool_evidence_marks_everything_unknown(tmp_path):
    """The catalogue's real state today: no tool was looked up, so none is resolved."""
    d = _write_collection(tmp_path, with_evidence=False)
    summary = e.enrich(str(d))
    assert summary["tool_tiers"] == {"unknown": 3}


def test_enrich_idempotent(tmp_path):
    d = _write_collection(tmp_path)
    e.enrich(str(d))
    after_first = {n: (d / n).read_text() for n in
                   ("tools_index.json", "skills_index.json", "kb_bundle.json")}
    summary2 = e.enrich(str(d))
    after_second = {n: (d / n).read_text() for n in
                    ("tools_index.json", "skills_index.json", "kb_bundle.json")}
    assert after_first == after_second
    assert summary2["tools"] == 3


def test_enrich_preserves_indent(tmp_path):
    d = tmp_path
    (d / "tools_index.json").write_text('[\n    {\n        "slug": "t_open",\n        "dois": ["10.1/open"]\n    }\n]')
    (d / "skills_index.json").write_text('[\n    {\n        "slug": "s1",\n        "dois": ["10.1/open"]\n    }\n]')
    (d / "kb_bundle.json").write_text('{\n  "skills": {\n    "s1": {\n      "dois": ["10.1/open"]\n    }\n  }\n}')
    e.enrich(str(d))
    assert '\n    {\n' in (d / "tools_index.json").read_text(), "tools_index should preserve 4-space indent"
    assert '\n  "skills"' in (d / "kb_bundle.json").read_text(), "kb_bundle should preserve 2-space indent"
