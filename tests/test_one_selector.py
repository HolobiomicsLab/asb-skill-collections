"""One offline selector must behave identically through every public surface."""

from __future__ import annotations

import importlib.util
import inspect
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

from asb_skill_collections import asb_skill_index as idx
from asb_skill_collections.asbb_cli import main as cli_main


ROOT = pathlib.Path(__file__).resolve().parent.parent
V2 = ROOT / "collections" / "metabolomics" / "v2"
COLLECTION = "metabolomics/v2"
ROUTER_PATH = V2 / "bin" / "search_skills.py"
K = 3

SEARCH_CASES = (
    {
        "id": "skill_lcms_alignment_filtered",
        "target": "skills",
        "query": "align chromatographic peaks across LC-MS samples",
        "technique": "LC-MS",
        "expect_match": True,
    },
    {
        "id": "skill_formula_unfiltered",
        "target": "skills",
        "query": "predict molecular formula from tandem mass spectra",
        "technique": None,
        "expect_match": True,
    },
    {
        "id": "skill_massql_filtered",
        "target": "skills",
        "query": "query spectra by neutral loss with MassQL",
        "technique": "LC-MS",
        "expect_match": True,
    },
    {
        "id": "skill_gcms_filtered",
        "target": "skills",
        "query": "deconvolute gas chromatography mass spectra",
        "technique": "GC-MS",
        "expect_match": True,
    },
    {
        "id": "skill_real_no_match",
        "target": "skills",
        "query": "pulsar scintillation interferometry",
        "technique": None,
        "expect_match": False,
    },
    {
        "id": "workflow_untargeted_filtered",
        "target": "workflows",
        "query": "untargeted LC-MS/MS annotation",
        "technique": "LC-MS",
        "expect_match": True,
    },
    {
        "id": "workflow_nmr_filtered",
        "target": "workflows",
        "query": "profile metabolites from NMR spectra",
        "technique": "NMR",
        "expect_match": True,
    },
    {
        "id": "workflow_imaging_filtered",
        "target": "workflows",
        "query": "spatial metabolite annotation from mass spectrometry imaging",
        "technique": "MS-imaging",
        "expect_match": True,
    },
    {
        "id": "workflow_repository_unfiltered",
        "target": "workflows",
        "query": "search public repositories for matching mass spectra",
        "technique": None,
        "expect_match": True,
    },
    {
        "id": "workflow_flux_filtered",
        "target": "workflows",
        "query": "stable isotope tracing flux analysis",
        "technique": "LC-MS",
        "expect_match": True,
    },
)

RESULT_KEYS = {
    "slug",
    "name",
    "description",
    "score",
    "techniques",
    "tools",
    "collection",
    "target",
    "qualified_slug",
    "selector",
    "matched_fields",
    "filters",
    "fallback",
}
MATCHED_FIELDS = {"name", "description", "techniques", "tools", "member_tools"}
BEGIN_MARKER = b"# BEGIN VENDORED SELECTOR\n"
END_MARKER = b"# END VENDORED SELECTOR\n"


@pytest.fixture(autouse=True)
def _default_selector_rule(monkeypatch):
    """Ambient compatibility configuration must not change default assertions."""
    monkeypatch.delenv("ASB_SELECTOR_RULE", raising=False)


@pytest.fixture(scope="module")
def router_module():
    """Import the installed collection's retrieval entry point as a module."""
    spec = importlib.util.spec_from_file_location("asb_packaged_router", ROUTER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def mcp_server():
    """Use the real MCP-decorated Python functions when the extra is installed."""
    pytest.importorskip("mcp", reason="selector parity exercises the MCP extra")
    from asb_skill_collections import asb_mcp_server

    return asb_mcp_server


def _cli_payload(case: dict, capsys: pytest.CaptureFixture[str]) -> dict:
    argv = [
        "search",
        case["query"],
        "--repo",
        str(ROOT),
        "--collection",
        COLLECTION,
        "--target",
        case["target"],
        "--k",
        str(K),
    ]
    if case["technique"]:
        argv += ["--technique", case["technique"]]
    assert cli_main(argv) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    return json.loads(captured.out)


def _mcp_results(case: dict, server) -> list[dict]:
    common = {
        "query": case["query"],
        "collection": COLLECTION,
        "technique": case["technique"],
        "k": K,
    }
    if case["target"] == "skills":
        return server.search_skills(**common)
    return server.search_workflows(**common)


def _router_payload(case: dict, router, capsys: pytest.CaptureFixture[str]) -> dict:
    argv = [
        "--query",
        case["query"],
        "--collection",
        str(V2),
        "--target",
        case["target"],
        "-k",
        str(K),
        "--json",
    ]
    if case["technique"]:
        argv += ["--technique", case["technique"]]
    router.main(argv)
    captured = capsys.readouterr()
    assert captured.err == ""
    return json.loads(captured.out)


def _assert_hit_shape(hit: dict, case: dict, rule: str) -> None:
    assert set(hit) == RESULT_KEYS
    assert hit["collection"] == COLLECTION
    assert hit["target"] == case["target"]
    assert hit["qualified_slug"] == f"{COLLECTION}/{case['target']}/{hit['slug']}"
    assert hit["selector"] == {
        "name": "asb-keyword",
        "version": "1.0.0",
        "rule": rule,
    }
    assert hit["filters"] == {
        "technique": case["technique"].casefold() if case["technique"] else None,
        "tool": None,
        "edam": None,
        "max_tools": 25 if case["target"] == "skills" else 0,
    }
    assert hit["fallback"] == "keyword"
    assert isinstance(hit["slug"], str) and hit["slug"]
    assert isinstance(hit["name"], str)
    assert isinstance(hit["description"], str)
    assert type(hit["score"]) is float
    assert all(isinstance(value, str) for value in hit["techniques"])
    assert all(isinstance(value, str) for value in hit["tools"])
    assert set(hit["matched_fields"]) <= MATCHED_FIELDS
    query_tokens = set(re.findall(r"[a-z0-9]+", case["query"].casefold()))
    matched_tokens = [
        token
        for tokens in hit["matched_fields"].values()
        for token in tokens
    ]
    assert matched_tokens
    assert set(matched_tokens) <= query_tokens


def test_parity_matrix_has_the_required_shape():
    assert len(SEARCH_CASES) == 10
    assert sum(not case["expect_match"] for case in SEARCH_CASES) == 1
    for target in ("skills", "workflows"):
        filtered_states = {
            case["technique"] is not None
            for case in SEARCH_CASES
            if case["target"] == target
        }
        assert filtered_states == {False, True}


@pytest.mark.parametrize("case", SEARCH_CASES, ids=lambda case: case["id"])
def test_cli_mcp_and_packaged_router_have_one_result_contract(
    case,
    router_module,
    mcp_server,
    monkeypatch,
    capsys,
):
    monkeypatch.setenv("ASB_COLLECTIONS_ROOT", str(ROOT))
    cli_payload = _cli_payload(case, capsys)
    mcp_results = _mcp_results(case, mcp_server)
    router_payload = _router_payload(case, router_module, capsys)

    envelope = {"mode": "keyword", "target": case["target"], "query": case["query"]}
    assert {key: cli_payload[key] for key in envelope} == envelope
    assert {key: router_payload[key] for key in envelope} == envelope
    assert set(cli_payload) == {*envelope, "results"}
    assert set(router_payload) == {*envelope, "results"}

    package_results = cli_payload["results"]
    assert package_results == mcp_results
    assert router_payload["results"] == package_results
    assert [hit["slug"] for hit in package_results] == [
        hit["slug"] for hit in router_payload["results"]
    ]
    assert bool(package_results) is case["expect_match"]

    for hit in package_results:
        _assert_hit_shape(hit, case, "router")
    for hit in router_payload["results"]:
        _assert_hit_shape(hit, case, "router")
    # The documented order, restated here rather than imported from
    # result_order: descending score, then the default rule's title tie-break
    # inside an equal-score block (how many query terms reached the name, then
    # how much of the name they are), then the slug as the deterministic
    # fallback.
    order = []
    for hit in package_results:
        named = len(hit["matched_fields"].get("name", ()))
        terms = max(1, len(idx.tokenize(hit["name"], "router")))
        order.append((-hit["score"], -named, -named / terms, hit["slug"]))
    assert order == sorted(order)


def test_public_search_signatures_keep_compat(mcp_server, monkeypatch):
    signature = inspect.signature(idx.search)
    parameters = list(signature.parameters)
    assert parameters[:6] == [
        "collection",
        "target",
        "query",
        "technique",
        "k",
        "root",
    ]
    required_options = {"selector", "tool", "edam", "max_tools", "fallback"}
    assert required_options <= set(parameters[6:])
    for name in ("selector", "tool", "edam", "max_tools", "fallback"):
        assert signature.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
    for name in ("selector", "tool", "edam", "max_tools"):
        assert signature.parameters[name].default is None
    assert signature.parameters["fallback"].default == "keyword"

    skills = inspect.signature(mcp_server.search_skills)
    workflows = inspect.signature(mcp_server.search_workflows)
    assert list(skills.parameters)[:4] == ["query", "collection", "technique", "k"]
    assert list(workflows.parameters)[:4] == ["query", "collection", "k", "technique"]
    assert skills.parameters["collection"].default is None
    assert skills.parameters["technique"].default is None
    assert skills.parameters["k"].default == 10
    assert workflows.parameters["collection"].default is None
    assert workflows.parameters["k"].default == 5
    assert workflows.parameters["technique"].default is None
    monkeypatch.setenv("ASB_COLLECTIONS_ROOT", str(ROOT))
    assert mcp_server.search_skills(
        "pulsar scintillation interferometry", COLLECTION, None, K
    ) == []
    assert mcp_server.search_workflows(
        "pulsar scintillation interferometry", COLLECTION, K
    ) == []


@pytest.mark.parametrize(
    ("start", "target", "expected"),
    [
        (V2, "skills", V2 / "skills_index.json"),
        (V2, "workflows", V2 / "workflows" / "workflows_index.json"),
        (V2, "tools", V2 / "tools_index.json"),
        (V2 / "workflows", "skills", V2 / "skills_index.json"),
        (V2 / "workflows", "workflows", V2 / "workflows" / "workflows_index.json"),
        (V2 / "workflows", "tools", V2 / "tools_index.json"),
    ],
)
def test_index_resolver_works_from_collection_root_and_workflows(start, target, expected):
    assert idx.index_path(start, target) == expected
    assert idx.load_rows(start, target) == json.loads(expected.read_text(encoding="utf-8"))


def _make_synthetic_collection(root: pathlib.Path, domain: str, rows: list[dict]) -> None:
    collection_dir = root / "collections" / domain / "v1"
    collection_dir.mkdir(parents=True)
    (collection_dir / "skills_index.json").write_text(json.dumps(rows), encoding="utf-8")


@pytest.fixture
def science_root(tmp_path):
    rows = {
        "astronomy": {
            "slug": "exoplanet-transit-photometry",
            "name": "Exoplanet transit photometry",
            "description": "Fit stellar light curves and measure planetary transit depth.",
            "tools": ["AstroPy"],
            "techniques": ["photometry"],
        },
        "climate": {
            "slug": "monsoon-rainfall-forecast",
            "name": "Monsoon rainfall forecast",
            "description": "Forecast rainfall anomalies from atmospheric circulation.",
            "tools": ["xarray"],
            "techniques": ["climate-modeling"],
        },
        "proteomics": {
            "slug": "peptide-spectrum-matching",
            "name": "Peptide spectrum matching",
            "description": "Identify peptides from tandem mass spectra.",
            "tools": ["MSFragger"],
            "techniques": ["LC-MS/MS"],
        },
        "genomics": {
            "slug": "germline-variant-calling",
            "name": "Germline variant calling",
            "description": "Call germline variants from aligned sequencing reads.",
            "tools": ["GATK"],
            "techniques": ["short-read-sequencing"],
        },
    }
    for domain, row in rows.items():
        _make_synthetic_collection(tmp_path, domain, [row])
    return tmp_path


@pytest.mark.parametrize(
    ("domain", "query", "slug"),
    [
        ("astronomy", "stellar light curves planetary transit", "exoplanet-transit-photometry"),
        ("climate", "forecast monsoon rainfall anomalies", "monsoon-rainfall-forecast"),
        ("proteomics", "identify peptides from tandem spectra", "peptide-spectrum-matching"),
        ("genomics", "call variants from sequencing reads", "germline-variant-calling"),
    ],
)
def test_selector_fires_across_unrelated_sciences(science_root, domain, query, slug):
    hits = idx.search(f"{domain}/v1", "skills", query, k=K, root=science_root)
    assert [hit["slug"] for hit in hits] == [slug]


def test_selector_has_a_genuine_cross_domain_no_match(science_root):
    hits = idx.search(
        None, "skills", "pulsar scintillation interferometry", k=K, root=science_root
    )
    assert hits == []


def test_tied_scores_sort_by_slug_independent_of_input_order(tmp_path):
    rows = [
        {
            "slug": slug,
            "name": "Periodic signal detection",
            "description": "Detect periodic signals in observations.",
            "tools": ["ExampleTool"],
            "techniques": ["time-series"],
        }
        for slug in ("zeta-procedure", "alpha-procedure")
    ]
    _make_synthetic_collection(tmp_path, "demo", rows)
    index = tmp_path / "collections" / "demo" / "v1" / "skills_index.json"

    first = idx.search("demo/v1", "skills", "periodic detection", k=K, root=tmp_path)
    index.write_text(json.dumps(list(reversed(rows))), encoding="utf-8")
    second = idx.search("demo/v1", "skills", "periodic detection", k=K, root=tmp_path)

    expected = ["alpha-procedure", "zeta-procedure"]
    assert [hit["slug"] for hit in first] == expected
    assert [hit["slug"] for hit in second] == expected
    assert first[0]["score"] == first[1]["score"]


def test_historical_router_rule_is_explicit_in_results(science_root):
    hits = idx.search(
        "astronomy/v1",
        "skills",
        "stellar transit photometry",
        k=K,
        root=science_root,
        selector="router",
    )
    assert hits
    assert {hit["selector"]["rule"] for hit in hits} == {"router"}


def test_workflow_member_tools_are_searchable_filterable_and_returned(tmp_path):
    collection_dir = tmp_path / "collections" / "demo" / "v1"
    workflows_dir = collection_dir / "workflows"
    workflows_dir.mkdir(parents=True)
    (collection_dir / "skills_index.json").write_text("[]", encoding="utf-8")
    rows = [
        {
            "slug": "embedding-annotation",
            "name": "Embedding annotation",
            "description": "Annotate spectra with a learned embedding.",
            "member_tools": ["Spec2Vec", "MatchMS"],
            "techniques": ["LC-MS"],
            "edam_topics": ["http://edamontology.org/topic_0121"],
        }
    ]
    (workflows_dir / "workflows_index.json").write_text(json.dumps(rows), encoding="utf-8")

    by_member = idx.search("demo/v1", "workflows", "Spec2Vec", k=K, root=tmp_path)
    filtered = idx.search(
        "demo/v1",
        "workflows",
        "spectral embedding",
        k=K,
        root=tmp_path,
        tool="SPEC2VEC",
        edam="TOPIC_0121",
    )

    assert [hit["slug"] for hit in by_member] == ["embedding-annotation"]
    assert by_member[0]["tools"] == ["Spec2Vec", "MatchMS"]
    assert filtered[0]["tools"] == ["Spec2Vec", "MatchMS"]
    assert filtered[0]["filters"] == {
        "technique": None,
        "tool": "spec2vec",
        "edam": "topic_0121",
        "max_tools": 0,
    }


def _vendored_body(path: pathlib.Path) -> bytes:
    source = path.read_bytes()
    assert source.count(BEGIN_MARKER) == 1, path
    assert source.count(END_MARKER) == 1, path
    before_end, after_end = source.split(END_MARKER)
    assert after_end, f"{path} has no wrapper after its vendored selector"
    return before_end.split(BEGIN_MARKER)[1]


PACK_VENDORS = sorted(ROOT.glob("packs/*/*/bin/search_skills.py"))
VENDORED_PATHS = [V2 / "bin" / "search_skills.py", V2 / "bin" / "semantic_search.py", *PACK_VENDORS]


def test_all_eight_pack_routers_are_in_the_drift_guard():
    assert len(PACK_VENDORS) == 8


def test_router_generator_replaces_a_stale_vendor_block():
    from scripts import router_shape

    wrapper = b"#!/usr/bin/env python3\n" + BEGIN_MARKER + b"stale\n" + END_MARKER + b"main()\n"
    generated = router_shape.embed_selector(wrapper)
    canonical = (ROOT / "asb_skill_collections" / "asb_skill_index.py").read_bytes()
    before_end, after_end = generated.split(END_MARKER)
    assert before_end.split(BEGIN_MARKER)[1] == canonical
    assert after_end == b"main()\n"


@pytest.mark.parametrize("vendored_path", VENDORED_PATHS, ids=lambda path: str(path.relative_to(ROOT)))
def test_every_vendored_selector_is_byte_for_byte_canonical(vendored_path):
    canonical = (ROOT / "asb_skill_collections" / "asb_skill_index.py").read_bytes()
    assert _vendored_body(vendored_path) == canonical


def test_vendored_router_runs_with_only_the_standard_library(tmp_path):
    env = dict(os.environ)
    env["PYTHONPATH"] = ""
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("ASB_COLLECTIONS_ROOT", None)
    env.pop("OPENAI_API_KEY", None)
    completed = subprocess.run(
        [
            sys.executable,
            "-S",
            str(ROUTER_PATH),
            "--query",
            "untargeted LC-MS/MS annotation",
            "--collection",
            str(V2),
            "--target",
            "workflows",
            "-k",
            str(K),
            "--json",
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["mode"] == "keyword"
    assert payload["results"]
    assert all(hit["selector"]["rule"] == "router" for hit in payload["results"])
