"""Tests for the synthetic meta-skill synthesizer helper (Task 2).

The deterministic half of the ``synthesize-meta-skill`` flow:

* ``cluster_subskills`` — thin wrapper over the (injectable) matcher, returning
  the clustered sub-skills + their tools. A FAKE matcher is injected so no
  network/server is needed.
* ``meta_frontmatter`` — assemble a schema-correct ``super``/``synthetic``
  frontmatter (reusing ``normalize_skill.normalized_frontmatter``); must yield
  zero ``frontmatter_violations``.
* ``stage_meta_skill`` — delegate to ``propose_skill.stage_proposal`` (DRY, same
  rail), writing a ``wave-meta-skills-<date>.yaml`` ledger; idempotent, no
  git/gh. The staged tree must pass ``check_proposals.check_collection``.
"""
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_proposals as cp
from scripts import synthesize_meta_skill as s
from scripts.normalize_skill import frontmatter_violations


# --- in-memory collection fixture (mirrors skills_index / tools_index) --------

SUBSKILLS = ("lc-ms-feature-extraction", "spectral-similarity-scoring")
TOOLS = ("mzmine", "matchms")

VALID_DESC = (
    "Use when you have raw LC-MS/MS data and need to build a molecular network "
    "by detecting features, scoring spectral similarity, and propagating "
    "annotations across the network."
)


def _collection(tmp_path, skill_slugs=SUBSKILLS, tool_slugs=TOOLS):
    col = tmp_path / "v2"
    col.mkdir(parents=True)
    skills = [
        {
            "slug": sl,
            "name": sl,
            "description": f"Use when you need {sl.replace('-', ' ')} in LC-MS.",
            "tools_used": [tool_slugs[i % len(tool_slugs)]],
        }
        for i, sl in enumerate(skill_slugs)
    ]
    (col / "skills_index.json").write_text(json.dumps(skills))
    tools = [
        {"slug": t, "license_tier": "open", "used_by_skills": []} for t in tool_slugs
    ]
    (col / "tools_index.json").write_text(json.dumps(tools))
    return col


def _fake_matcher(returns):
    """A drop-in for ``match_skills(text, collection_dir, *, k, http=None)``.

    Records the call and returns a fixed list of ``{slug, score, backend}``
    hits — no network, no server, deterministic.
    """
    calls = []

    def matcher(text, collection_dir, *, k=10, http=None):
        calls.append({"text": text, "collection_dir": str(collection_dir), "k": k})
        return [dict(r) for r in returns]

    matcher.calls = calls
    return matcher


# --- cluster_subskills -------------------------------------------------------

def test_cluster_subskills_returns_matcher_shape(tmp_path):
    col = _collection(tmp_path)
    matcher = _fake_matcher(
        [
            {"slug": "lc-ms-feature-extraction", "score": 0.9, "backend": "lexical"},
            {"slug": "spectral-similarity-scoring", "score": 0.7, "backend": "lexical"},
        ]
    )
    out = s.cluster_subskills("molecular networking", str(col), matcher=matcher)
    assert set(out) == {"subskills", "tools"}
    # subskills carry the matcher's slug+score
    sub = out["subskills"]
    assert [x["slug"] for x in sub] == list(SUBSKILLS)
    assert all("score" in x for x in sub)
    # tools are {slug, score} resolved against the indexes (union of tools_used)
    assert out["tools"], "expected at least one clustered tool"
    assert all(set(t) >= {"slug", "score"} for t in out["tools"])
    tool_slugs = {t["slug"] for t in out["tools"]}
    assert tool_slugs <= set(TOOLS)


def test_cluster_subskills_passes_k_and_seed_to_matcher(tmp_path):
    col = _collection(tmp_path)
    matcher = _fake_matcher([{"slug": "lc-ms-feature-extraction", "score": 0.5}])
    s.cluster_subskills("seed text", str(col), k=15, matcher=matcher)
    assert matcher.calls[0]["k"] == 15
    assert matcher.calls[0]["text"] == "seed text"
    assert matcher.calls[0]["collection_dir"] == str(col)


def test_cluster_subskills_defaults_to_real_match_skills(tmp_path):
    # No matcher injected => falls back to the real lexical match_skills (no
    # server). The seed text overlaps the fixture skills lexically.
    col = _collection(tmp_path)
    out = s.cluster_subskills(
        "lc-ms feature extraction spectral similarity scoring", str(col)
    )
    slugs = {x["slug"] for x in out["subskills"]}
    assert slugs & set(SUBSKILLS)


def test_cluster_subskills_empty_match_yields_empty_tools(tmp_path):
    col = _collection(tmp_path)
    matcher = _fake_matcher([])
    out = s.cluster_subskills("nothing matches", str(col), matcher=matcher)
    assert out["subskills"] == []
    assert out["tools"] == []


# --- meta_frontmatter --------------------------------------------------------

def test_meta_frontmatter_sets_synthetic_super_fields():
    fm = s.meta_frontmatter(
        name="molecular-networking",
        description=VALID_DESC,
        orchestrates=list(SUBSKILLS),
        synthesized_from=list(SUBSKILLS),
        tools_used=list(TOOLS),
    )
    meta = fm["metadata"]
    assert meta["provenance_tier"] == "synthetic"
    assert meta["skill_kind"] == "super"
    assert meta["orchestrates"] == list(SUBSKILLS)
    assert meta["synthesized_from"] == list(SUBSKILLS)
    assert meta["tools_used"] == list(TOOLS)
    assert meta["license_tier"] == "open"
    assert fm["status"] == "hold"
    # related_skills mirrors orchestrates (so community-key expectations hold too)
    assert fm["related_skills"] == list(SUBSKILLS)
    assert fm["name"] == "molecular-networking"
    assert fm["description"] == VALID_DESC


def test_meta_frontmatter_yields_zero_violations():
    fm = s.meta_frontmatter(
        name="molecular-networking",
        description=VALID_DESC,
        orchestrates=list(SUBSKILLS),
        synthesized_from=list(SUBSKILLS),
        tools_used=list(TOOLS),
        license_tier="open",
    )
    assert frontmatter_violations(fm) == []


def test_meta_frontmatter_honors_license_tier():
    fm = s.meta_frontmatter(
        name="m",
        description=VALID_DESC,
        orchestrates=list(SUBSKILLS),
        synthesized_from=list(SUBSKILLS),
        tools_used=[],
        license_tier="noncommercial",
    )
    assert fm["metadata"]["license_tier"] == "noncommercial"
    assert frontmatter_violations(fm) == []


def test_meta_frontmatter_does_not_mutate_inputs():
    orch = list(SUBSKILLS)
    syn = list(SUBSKILLS)
    tools = list(TOOLS)
    s.meta_frontmatter(
        name="m",
        description=VALID_DESC,
        orchestrates=orch,
        synthesized_from=syn,
        tools_used=tools,
    )
    assert orch == list(SUBSKILLS)
    assert syn == list(SUBSKILLS)
    assert tools == list(TOOLS)


# --- stage_meta_skill --------------------------------------------------------

BODY = "# Molecular Networking\n\nOrdered orchestration body.\n"
DATE = "2026-06-26"


def _ledger_meta():
    return {
        "slug": "molecular-networking",
        "synthesized_from": list(SUBSKILLS),
        "orchestrates": list(SUBSKILLS),
        "tools_used": list(TOOLS),
        "license_tier": "open",
        "date": DATE,
    }


def _frontmatter():
    return s.meta_frontmatter(
        name="molecular-networking",
        description=VALID_DESC,
        orchestrates=list(SUBSKILLS),
        synthesized_from=list(SUBSKILLS),
        tools_used=list(TOOLS),
    )


def test_stage_meta_skill_writes_tree(tmp_path):
    col = _collection(tmp_path)
    res = s.stage_meta_skill(str(col), _frontmatter(), BODY, _ledger_meta())
    skill_md = col / "proposals" / "skills" / "molecular-networking" / "SKILL.md"
    ledger = col / "proposals" / "wave-meta-skills-2026-06-26.yaml"
    assert skill_md.is_file()
    assert ledger.is_file()
    assert pathlib.Path(res["skill_md"]) == skill_md
    assert pathlib.Path(res["ledger"]) == ledger
    # the SKILL.md round-trips to the synthetic/super frontmatter
    text = skill_md.read_text()
    assert text.startswith("---\n")
    fm = yaml.safe_load(text.split("---\n", 2)[1])
    assert fm["metadata"]["skill_kind"] == "super"
    assert fm["metadata"]["provenance_tier"] == "synthetic"
    assert "Ordered orchestration body." in text.split("---\n", 2)[2]


def test_stage_meta_skill_ledger_schema_and_entry(tmp_path):
    col = _collection(tmp_path)
    s.stage_meta_skill(str(col), _frontmatter(), BODY, _ledger_meta())
    ledger = yaml.safe_load(
        (col / "proposals" / "wave-meta-skills-2026-06-26.yaml").read_text()
    )
    assert ledger["schema"] == "asb-skill-proposals/1.0"
    entry = next(
        e for e in ledger["proposals"] if e["slug"] == "molecular-networking"
    )
    assert entry["status"] == "hold"
    assert entry["submitted_on"] == DATE
    assert entry["orchestrates"] == list(SUBSKILLS)


def test_stage_meta_skill_is_idempotent(tmp_path):
    col = _collection(tmp_path)
    first = s.stage_meta_skill(str(col), _frontmatter(), BODY, _ledger_meta())
    md1 = pathlib.Path(first["skill_md"]).read_text()
    led1 = pathlib.Path(first["ledger"]).read_text()
    second = s.stage_meta_skill(str(col), _frontmatter(), BODY, _ledger_meta())
    md2 = pathlib.Path(second["skill_md"]).read_text()
    led2 = pathlib.Path(second["ledger"]).read_text()
    assert md1 == md2
    assert led1 == led2
    ledger = yaml.safe_load(led2)
    assert [e["slug"] for e in ledger["proposals"]].count(
        "molecular-networking"
    ) == 1


def test_stage_meta_skill_result_passes_check_collection(tmp_path):
    col = _collection(tmp_path)
    s.stage_meta_skill(str(col), _frontmatter(), BODY, _ledger_meta())
    assert cp.check_collection(str(col)) == []


def test_stage_meta_skill_does_no_git_or_network(tmp_path):
    # The helper must not import or shell out to git/gh; staging only writes the
    # proposals tree. (A behavioral proxy: nothing outside proposals/ appears.)
    col = _collection(tmp_path)
    before = {p.name for p in col.iterdir()}
    s.stage_meta_skill(str(col), _frontmatter(), BODY, _ledger_meta())
    after = {p.name for p in col.iterdir()}
    assert after - before == {"proposals"}
