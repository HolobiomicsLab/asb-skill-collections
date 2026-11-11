"""A tool's licence may only come from the tool. These tests hold that line.

Everything here is offline: recorded registry answers (trimmed copies of real
Bioconda, Bioconductor, CRAN and bio.tools records, and PyPI answers reduced to
the fields the resolver reads) sit in tests/fixtures/tool_licences/cache, which
the resolver reads as its cache, so no test reaches the network.
"""
import json
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import resolve_tool_licenses as r

def paper(name, licence, detection, repo="owner/repo"):
    entry = {"doi": "10.1/p", "name": name, "repo_url": repo, "access": {}}
    if detection.endswith("-paper"):
        entry.update(license_detection=detection, access={"license": licence})
    else:
        entry["tool_license"] = {
            "spdx": licence,
            "detection": detection,
            "verified_on": None,
            "source": repo,
        }
    return entry


def tool(slug, name, dois=("10.1/p",)):
    return {"slug": slug, "name": name, "dois": list(dois)}


# --------------------------------------------------------------------------- #
# Route A -- the introducing paper                                            #
# --------------------------------------------------------------------------- #

def test_the_introducing_papers_repository_licence_is_the_tools():
    papers = {"10.1/p": paper("ANN-SoLo", "Apache-2.0", "github-api", "bittremieux-lab/ANN-SoLo")}
    e = r.self_published_evidence(tool("ann-solo", "ANN-SoLo"), papers)
    assert e["license"] == "Apache-2.0"
    assert e["repo_url"] == "bittremieux-lab/ANN-SoLo"
    assert e["route"] == "self_published"


def test_a_paper_subject_licence_is_refused_even_from_the_introducing_paper():
    """The #42 defect. Crossref describes the publication, not the software."""
    for detection in ("crossref-paper", "biorxiv_api-paper"):
        papers = {"10.1/p": paper("ANN-SoLo", "CC-BY-4.0", detection)}
        assert r.self_published_evidence(tool("ann-solo", "ANN-SoLo"), papers) is None


def test_a_paper_that_merely_cites_the_tool_is_not_its_introducing_paper():
    papers = {"10.1/p": paper("LipidIN", "Apache-2.0", "github-api", "LinShuhaiLAB/LipidIN")}
    assert r.self_published_evidence(tool("camera", "CAMERA"), papers) is None


def test_the_name_match_is_exact_not_substring():
    """`XCMS Online` is a different tool from `XCMS`."""
    papers = {"10.1/p": paper("XCMS Online", "MIT", "github-api")}
    assert r.introducing_paper(tool("xcms", "XCMS"), papers) is None


def test_an_unresolved_paper_licence_yields_no_evidence():
    papers = {"10.1/p": paper("Tool", None, "none")}
    assert r.self_published_evidence(tool("tool", "Tool"), papers) is None


# --------------------------------------------------------------------------- #
# Reconciliation                                                              #
# --------------------------------------------------------------------------- #

def test_the_registry_supersedes_a_repository_read_of_the_same_tier():
    """xcms: DESCRIPTION says GPL (>= 2); the LICENSE file classifies as LGPL-3.0."""
    a = {"license": "LGPL-3.0", "license_detection": "license-file",
         "repo_url": "sneumann/xcms", "route": "self_published", "matched": "XCMS"}
    b = {"license": "GPL-2.0-or-later", "license_detection": "bioconductor-package",
         "repo_url": None, "route": "registry:bioconductor", "matched": "xcms"}
    evidence, conflict = r.reconcile(a, b)
    assert conflict is None
    assert evidence["license"] == "GPL-2.0-or-later"
    assert evidence["superseded"]["license"] == "LGPL-3.0"
    # the repository the registry lacked is carried over, not dropped
    assert evidence["repo_url"] == "sneumann/xcms"


def test_a_tier_disagreement_resolves_to_nothing():
    """Two sources giving materially different advice is not a resolution."""
    a = {"license": "MIT", "license_detection": "github-api", "route": "self_published"}
    b = {"license": "CC-BY-NC-4.0", "license_detection": "bioconda-package",
         "route": "registry:bioconda"}
    evidence, conflict = r.reconcile(a, b)
    assert evidence is None
    assert conflict["self_published"]["license"] == "MIT"


def test_one_route_alone_is_used_as_is():
    a = {"license": "MIT", "license_detection": "github-api", "route": "self_published"}
    assert r.reconcile(a, None) == (a, None)
    assert r.reconcile(None, a) == (a, None)
    assert r.reconcile(None, None) == (None, None)


# --------------------------------------------------------------------------- #
# End to end, with recorded registry answers                                   #
# --------------------------------------------------------------------------- #

FIXTURE_CACHE = pathlib.Path(__file__).parent / "fixtures" / "tool_licences" / "cache"


def _collection(tmp_path, records, domain="transcriptomics", skills=(), papers=()):
    """A collection of tool records, each ``(slug, name, yaml_fields)``."""
    d = tmp_path / domain
    (d / "tools").mkdir(parents=True)
    index = []
    for slug, name, fields in records:
        index.append({"slug": slug, "name": name, "dois": fields.pop("dois", ["10.1/x"]),
                      "used_by_skills": fields.pop("used_by_skills", [])})
        doc = {"name": name, "slug": slug, "version_used": None, "evidence_spans": [],
               "derived_from": [], "source_repos": [], **fields}
        (d / "tools" / f"{slug}.yaml").write_text(yaml.safe_dump(doc, sort_keys=False))
    (d / "tools_index.json").write_text(json.dumps(index))
    (d / "skills_index.json").write_text(json.dumps(list(skills)))
    (d / "corpus.yaml").write_text(yaml.safe_dump({"papers": list(papers)}))
    return d


def _resolve(tmp_path, records, reviewed=None, **kw):
    import shutil
    cache = tmp_path / "cache"
    if not cache.exists():
        shutil.copytree(FIXTURE_CACHE, cache)
    d = _collection(tmp_path, records, **kw)
    summary = r.resolve(d, cache, offline=True,
                        reviewed=reviewed if reviewed is not None else {"version": 1, "entries": []},
                        report=tmp_path / "report.json")
    out = json.loads((d / "tool_licenses.json").read_text())
    report = {o["slug"]: o for o in json.loads((tmp_path / "report.json").read_text())}
    return out, report, summary


def test_resolve_writes_only_tool_backed_entries(tmp_path):
    """CAMERA is cited by an Apache-2.0 paper; the citing paper never contributes."""
    out, report, _ = _resolve(tmp_path, [
        ("deseq2", "DESeq2", {"evidence_spans": ["library(DESeq2)"]}),
        ("camera", "CAMERA", {"dois": ["10.1/lipidin"]}),
        ("nothing", "Nothing", {}),
    ], papers=[{"doi": "10.1/lipidin", "name": "LipidIN", "repo_url": "LinShuhaiLAB/LipidIN",
                "license_detection": "github-api", "access": {"license": "Apache-2.0"}}])
    assert out["deseq2"]["license"] == "LGPL-3.0-or-later"
    assert out["deseq2"]["license_detection"] == "bioconductor-package"
    assert out["deseq2"]["license_evidence"] == "https://bioconductor.org/packages/DESeq2"
    assert out["deseq2"]["repo_url"] == "https://github.com/thelovelab/DESeq2"
    assert "camera" not in out and "nothing" not in out
    assert report["nothing"]["reason"] == "no-registry-match"


def test_every_resolved_record_names_its_source_and_address(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("deseq2", "DESeq2", {"evidence_spans": ["library(DESeq2)"]}),
        ("devtools", "devtools", {"evidence_spans": ["devtools::install_github('x/y')"]}),
    ])
    for slug, ev in out.items():
        assert ev["license_detection"] and ev["license_evidence"].startswith("https://"), slug
        assert ev["license_raw"], slug


# Trap 1: an exact name in a life-science registry is a different entity.

def test_the_dimension_reduction_method_is_not_the_mappability_package(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("umap", "UMAP", {"evidence_spans": ["cells were embedded with UMAP for visualisation"],
                          "derived_from": [{"doi": "10.1/x", "title": "A single-cell atlas"}]}),
    ])
    assert "umap" not in out
    assert report["umap"]["reason"].startswith("identity:")


def test_the_language_model_is_not_the_bioconductor_package(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("bert", "BERT", {"evidence_spans": ["we fine-tune BERT on the corpus"]}),
    ], domain="agentic-ai")
    assert "bert" not in out
    assert report["bert"]["reason"] == "identity:outside-life-science-needs-corroboration"


def test_the_particle_physics_tool_is_not_the_microbial_one(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("gambit", "GAMBIT", {"evidence_spans": ["global fits with GAMBIT"]}),
    ], domain="astronomy")
    assert "gambit" not in out


def test_an_english_word_name_needs_corroboration(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("singularity", "Singularity", {"evidence_spans": ["run inside a Singularity image"]}),
        ("cooler", "cooler", {"evidence_spans": ["matrices were stored with cooler"]}),
    ], domain="epigenomics")
    assert out == {}
    assert report["cooler"]["reason"] == "identity:weak-name-needs-corroboration"


def test_a_repository_named_by_the_record_corroborates_a_weak_name(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("cooler", "cooler", {"source_repos": ["https://github.com/open2c/cooler"]}),
    ], domain="epigenomics")
    assert out["cooler"]["license"] == "BSD-3-Clause"
    assert out["cooler"]["identity"]["corroboration"][0]["kind"] == "repository"


def test_a_data_package_is_not_the_database_it_wraps(tmp_path):
    out, report, _ = _resolve(tmp_path, [("msigdb", "MSigDB", {})])
    assert "msigdb" not in out
    assert report["msigdb"]["reason"] == "identity:data-package"


def test_a_distinctive_name_needs_some_corroboration(tmp_path):
    """`CoLoRMap` (long-read correction) and `colormap` (matplotlib) share a key."""
    out, report, _ = _resolve(tmp_path, [
        ("colormap", "CoLoRMap", {"evidence_spans": ["hybrid correction of PacBio reads"]}),
    ], domain="genomics")
    assert "colormap" not in out
    assert report["colormap"]["reason"] == "identity:uncorroborated"


def test_a_described_distinctive_name_resolves(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("nextflow", "Nextflow", {"evidence_spans": [
            "pipelines written in the Nextflow DSL for data-driven computational pipelines"]}),
    ], domain="genomics")
    assert out["nextflow"]["license"] == "Apache-2.0"


def test_a_reviewed_exclusion_still_blocks_the_match(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("ggplot", "ggplot", {"evidence_spans": ["an extremely un-pythonic package for ggplot2"]}),
    ], domain="metabolomics")
    assert "ggplot" not in out
    assert report["ggplot"]["reason"] == "reviewed-exclusion"


# Trap 4: general registries, and R and Python packages that share a name.

def test_without_ecosystem_evidence_general_registries_are_not_used(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("devtools", "devtools", {}), ("shiny", "Shiny", {}), ("igraph", "igraph", {}),
    ])
    assert out == {}
    assert report["shiny"]["reason"] == "identity:general-registry-needs-corroboration"


def test_r_evidence_picks_cran_never_pypi(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("devtools", "devtools", {"evidence_spans": ["devtools::install_github('a/b')"]}),
        ("shiny", "Shiny", {"evidence_spans": ["library(shiny)"]}),
        ("tidyverse", "tidyverse", {"evidence_spans": ['install.packages("tidyverse")']}),
        ("igraph", "igraph", {"evidence_spans": ["the R package igraph"]}),
    ])
    assert {slug: e["route"] for slug, e in out.items()} == {
        "devtools": "registry:cran", "shiny": "registry:cran",
        "tidyverse": "registry:cran", "igraph": "registry:cran"}
    assert out["shiny"]["license"] == "MIT"
    assert out["igraph"]["license"] == "GPL-2.0-or-later"


def test_python_evidence_picks_pypi_never_cran(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("igraph", "igraph", {"evidence_spans": ["import igraph as ig"]}),
        ("scanpy", "Scanpy", {"evidence_spans": ["pip install scanpy"]}),
    ])
    assert out["igraph"]["route"] == "registry:pypi"
    assert out["igraph"]["license"] == "GNU General Public License (GPL)"
    assert out["scanpy"]["license"] == "BSD-3-Clause"


def test_evidence_for_both_ecosystems_with_different_licences_stays_unknown(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("igraph", "igraph", {"evidence_spans": ["import igraph", "library(igraph)"]}),
    ])
    assert "igraph" not in out
    assert report["igraph"]["reason"].startswith("several-packages-differ")


def test_docker_is_not_the_python_sdk(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("docker", "Docker", {"evidence_spans": ["docker run -it image", "written in Python"]}),
    ])
    assert "docker" not in out


def test_bio_tools_needs_a_shared_repository_or_publication(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("dssp", "DSSP", {"source_repos": ["https://github.com/PDB-REDO/dssp"]}),
    ], domain="proteomics")
    assert out["dssp"]["route"] == "registry:biotools"
    assert out["dssp"]["license"] == "BSD-2-Clause"
    assert out["dssp"]["license_evidence"] == "https://bio.tools/dssp"


def test_bio_tools_without_a_shared_repository_is_refused(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("dssp", "DSSP", {"derived_from": [{"doi": "10.9/other", "title": "DSSP: a review"}]}),
    ], domain="proteomics")
    assert "dssp" not in out


def test_a_registry_and_a_same_name_package_that_disagree_leave_the_record_unknown(tmp_path):
    """bio.tools still says GPL-2.0 for bedtools; the Bioconda package has been MIT since 2.28."""
    out, report, _ = _resolve(tmp_path, [
        ("bedtools", "bedtools", {"source_repos": ["https://github.com/arq5x/bedtools2"],
                                  "derived_from": [{"doi": "10.1/x", "title": "bedtools: x"}]}),
    ], domain="transcriptomics")
    assert out == {}
    assert report["bedtools"]["reason"].startswith("registries-disagree")


def test_one_repository_in_two_registries_is_one_tool(tmp_path):
    """A package declaring the repository an accepted entry declares is the same tool."""
    import copy
    from scripts import resolve_tool_licenses as R

    class Reg:
        def __init__(self, rid, scope, repo):
            self.id, self.scope, self.repo = rid, scope, repo
            self.spec = {"detection": f"{rid}-package"}

        def repo_values(self, record):
            return [self.repo]

        def address(self, name, record):
            return f"https://example.org/{self.id}/{name}"

    from scripts.tool_identity import Verdict
    a = {"registry": "bioconda", "registry_obj": Reg("bioconda", "life_science", "https://github.com/o/t"),
         "canonical": "t", "record": {}, "verdict": Verdict(False, "uncorroborated"),
         "reading": {"license": "MIT", "tier": "open", "raw": "MIT"}}
    b = {"registry": "biotools", "registry_obj": Reg("biotools", "general", "https://github.com/o/t.git"),
         "canonical": "t", "record": {},
         "verdict": Verdict(True, "corroborated", [{"kind": "repository", "value": "github.com/o/t"}]),
         "reading": {"license": "GPL-2.0-only", "tier": "open", "raw": "GPL-2.0"}}
    cands = [a, b]
    R._share_identity(cands)
    evidence, reason = R.choose(cands)
    assert reason == "resolved" and evidence["license"] == "MIT"
    assert evidence["superseded"][0]["license"] == "GPL-2.0-only"


# Trap 2: licence strings.

def test_a_non_commercial_licence_never_reads_as_open(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("unitas", "unitas", {"evidence_spans": [
            "annotation of small non-coding RNA sequence datasets with unitas"],
            "source_repos": ["http://www.smallrnagroup.uni-mainz.de/software.html"]}),
        ("annevo", "ANNEVO", {"source_repos": ["https://github.com/xjtu-omics/ANNEVO"]}),
    ], domain="genomics")
    assert out["unitas"]["license"] == "CC-BY-NC-2.0"
    assert out["unitas"]["license_tier"] == "noncommercial"
    assert "annevo" not in out


def test_a_versioned_gpl_string_keeps_its_version(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("epic", "epic", {"source_repos": ["http://github.com/endrebak/epic"]}),
    ], domain="epigenomics")
    assert out["epic"]["license"] == "GPL-3.0-only"
    assert out["epic"]["license_raw"] == "GNU General Public License v3 (GPLv3)"


# The reviewed map.

REVIEWED = {"version": 1, "reviewed": "2026-11-11", "entries": [
    {"names": ["scikit-learn", "sklearn"], "entity": "scikit-learn", "entry_kind": "software",
     "category": "package", "license": "BSD-3-Clause", "license_tier": "open",
     "repo_url": "https://github.com/scikit-learn/scikit-learn",
     "evidence_url": "https://github.com/scikit-learn/scikit-learn/blob/main/COPYING",
     "verified": "2026-11-11"},
    {"names": ["UMAP"], "entity": None, "ambiguous": True, "verified": "2026-11-11", "contexts": [
        {"when": "dimension reduction", "match": {"any_terms": ["single-cell", "embedding"],
                                                   "none_terms": ["mappability"]},
         "entity": "umap-learn", "entry_kind": "software", "license": "BSD-3-Clause",
         "license_tier": "open", "repo_url": "https://github.com/lmcinnes/umap",
         "evidence_url": "https://github.com/lmcinnes/umap/blob/master/LICENSE.txt"},
        {"when": "mappability", "match": {"any_terms": ["mappability"]},
         "entity": "Umap (Hoffman lab)", "leave_unknown": True}]},
    {"names": ["Thermo Xcalibur"], "entity": "Xcalibur", "entry_kind": "vendor_product",
     "license": None, "license_tier": "restricted",
     "evidence_url": "https://www.thermofisher.com/", "verified": "2026-11-11"},
]}


def test_a_reviewed_entry_outranks_every_registry(tmp_path):
    out, _, _ = _resolve(tmp_path, [
        ("scikit-learn", "Scikit-learn", {}), ("sklearn", "sklearn", {}),
    ], reviewed=REVIEWED)
    for slug in ("scikit-learn", "sklearn"):
        assert out[slug]["license"] == "BSD-3-Clause"
        assert out[slug]["license_detection"] == "reviewed-map"
        assert out[slug]["license_evidence"].endswith("/COPYING")
        assert out[slug]["repo_url"] == "https://github.com/scikit-learn/scikit-learn"


def test_an_ambiguous_reviewed_name_resolves_only_in_its_one_context(tmp_path):
    out, report, _ = _resolve(tmp_path, [
        ("umap", "UMAP", {"evidence_spans": ["a single-cell embedding with UMAP"]}),
    ], reviewed=REVIEWED)
    assert out["umap"]["license"] == "BSD-3-Clause"
    assert report["umap"]["reason"] == "reviewed-context"


def test_an_ambiguous_reviewed_name_in_the_other_context_stays_unknown(tmp_path):
    """And no registry is consulted: the Bioconda `umap` must not come back."""
    out, report, _ = _resolve(tmp_path, [
        ("umap", "Umap", {"evidence_spans": ["mappability tracks from Umap"]}),
    ], reviewed=REVIEWED, domain="genomics")
    assert out == {}
    assert report["umap"]["reason"] == "reviewed-context-leave-unknown"


def test_an_ambiguous_reviewed_name_without_context_stays_unknown(tmp_path):
    out, report, _ = _resolve(tmp_path, [("umap", "UMAP", {})], reviewed=REVIEWED)
    assert out == {}
    assert report["umap"]["reason"] == "reviewed-ambiguous-no-single-context"


def test_a_reviewed_vendor_product_carries_its_kind(tmp_path):
    out, _, _ = _resolve(tmp_path, [("xcalibur", "Thermo Xcalibur", {})], reviewed=REVIEWED)
    assert out["xcalibur"]["license_tier"] == "restricted"
    assert out["xcalibur"]["entry_kind"] == "vendor_product"


def test_the_shipped_registry_config_is_well_formed():
    """Every declared registry and exclusion carries the fields the resolver reads."""
    config = r.load_registry_config()
    assert config["registries"], "no registries declared"
    for reg in config["registries"]:
        for field in ("id", "scope", "detection", "index_shape", "license_field",
                      "license_format", "repo_fields", "address"):
            assert reg.get(field), f"{reg.get('id')}: missing {field}"
        assert reg["scope"] in ("life_science", "general"), reg["id"]
        if reg["index_shape"] == "per_name":
            assert reg.get("package_url") and reg.get("ask_when"), reg["id"]
        else:
            assert reg.get("index_url"), reg["id"]
    assert {"pypi", "cran", "biotools"} <= {reg["id"] for reg in config["registries"]
                                           if reg["scope"] == "general"}
    ids = {reg["id"] for reg in config["registries"]}
    for excl in config.get("excluded_matches") or []:
        assert excl.get("tool") and excl.get("reason"), f"incomplete exclusion: {excl}"
        assert excl["registry"] in ids, f"{excl['tool']}: unknown registry {excl['registry']!r}"
    assert "astronomy" not in config["life_science_collections"]
    assert "agentic-ai" not in config["life_science_collections"]


def test_every_registry_detection_counts_as_tool_evidence():
    """A detection the tier resolver does not recognise would silently stay unknown."""
    from scripts.license_tier import TOOL_DETECTIONS
    for reg in r.load_registry_config()["registries"]:
        assert reg["detection"] in TOOL_DETECTIONS, reg["detection"]
    assert r.DETECTION_REVIEWED in TOOL_DETECTIONS


def test_a_refusing_registry_stops_the_run(tmp_path, monkeypatch):
    """HTTP 403 or 429 must not be read as "no such package"."""
    import urllib.error
    from scripts import tool_registry_sources as T

    def refuse(*_a, **_k):
        raise urllib.error.HTTPError("https://pypi.org/x", 429, "Too Many Requests", {}, None)

    monkeypatch.setattr(T.urllib.request, "urlopen", refuse)
    with pytest.raises(T.RegistryRefused):
        T.Fetcher(tmp_path).get("https://pypi.org/pypi/x/json", "pypi-x.json", 100)


# --------------------------------------------------------------------------- #
# Repository URL selection                                                    #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("values,expected", [
    # CAMERA: a lab homepage in URL, the repository buried in a BugReports path.
    (["http://msbi.ipb-halle.de/msbi/CAMERA/", "https://github.com/sneumann/CAMERA/issues/new"],
     "https://github.com/sneumann/CAMERA"),
    (["https://github.com/lgatto/MSnbase/issues"], "https://github.com/lgatto/MSnbase"),
    (["https://github.com/mzmine/mzmine"], "https://github.com/mzmine/mzmine"),
    (["https://github.com/bioc/limma.git"], "https://github.com/bioc/limma"),
    # Several URLs crammed into one field, comma- and newline-separated.
    (["https://github.com/hanhineva-lab/notame,\nhttps://hanhineva-lab.github.io/notame/"],
     "https://github.com/hanhineva-lab/notame"),
    # No code host: the declared URL is still better than nothing.
    (["https://www.ruby-lang.org"], "https://www.ruby-lang.org"),
    ([], None),
])
def test_pick_repo_url(values, expected):
    assert r.pick_repo_url(values) == expected


def test_pick_repo_url_prefers_a_code_host_over_an_earlier_homepage():
    assert r.pick_repo_url(["https://bioinf.wehi.edu.au/limma/",
                            "https://github.com/bioc/limma"]) == "https://github.com/bioc/limma"
