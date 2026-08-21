"""A tool's licence may only come from the tool. These tests hold that line.

Everything here is offline: registry responses are pre-seeded into the cache
directory the resolver memoises into, so no test reaches the network.
"""
import json
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import resolve_tool_licenses as r

BIOC = {"id": "bioconductor", "detection": "bioconductor-package",
        "index_url": "https://example.invalid/ls", "index_shape": "name_list",
        "package_url": "https://example.invalid/packages/{name}",
        "license_field": "License", "license_format": "r_description_field",
        "repo_fields": ["URL", "RemoteUrl"]}

CONDA = {"id": "bioconda", "detection": "bioconda-package",
         "index_url": "https://example.invalid/channeldata.json",
         "index_shape": "packages_map", "license_field": "license",
         "license_format": "spdx_or_text", "repo_fields": ["dev_url", "home"]}


@pytest.fixture
def cache(tmp_path):
    """A seeded cache: the resolver reads these instead of the network."""
    d = tmp_path / "cache"
    d.mkdir()
    (d / "bioconductor-index.json").write_text(json.dumps(["xcms", "CAMERA", "mist"]))
    (d / "bioconductor-xcms.json").write_text(json.dumps(
        {"License": "GPL (>= 2) + file LICENSE", "URL": "https://github.com/sneumann/xcms"}))
    (d / "bioconductor-camera.json").write_text(json.dumps(
        {"License": "GPL (>= 2)", "RemoteUrl": "https://github.com/bioc/CAMERA"}))
    (d / "bioconductor-mist.json").write_text(json.dumps({"License": "MIT + file LICENSE"}))
    (d / "bioconda-index.json").write_text(json.dumps({"packages": {
        "mzmine": {"license": "MIT", "dev_url": "https://github.com/mzmine/mzmine"},
        "vague": {"license": "see the enclosed terms of use"},
    }}))
    return d


def paper(name, licence, detection, repo="owner/repo"):
    return {"doi": "10.1/p", "name": name, "repo_url": repo,
            "license_detection": detection, "access": {"license": licence}}


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
# Route B -- curated registries                                               #
# --------------------------------------------------------------------------- #

def test_a_registry_match_is_case_insensitive(cache):
    """The catalogue records `XCMS`; Bioconductor names it `xcms`."""
    indexes = {"bioconductor": r.registry_names(BIOC, cache)}
    e = r.registry_evidence(tool("xcms", "XCMS"), [BIOC], indexes, cache)
    assert e["license"] == "GPL-2.0-or-later"
    assert e["repo_url"] == "https://github.com/sneumann/xcms"
    assert e["license_detection"] == "bioconductor-package"


def test_an_unreadable_registry_licence_resolves_to_nothing(cache):
    """Rather than the `restricted` fallback: unread is not established."""
    indexes = {"bioconda": r.registry_names(CONDA, cache)}
    assert r.registry_evidence(tool("vague", "vague"), [CONDA], indexes, cache) is None


def test_a_reviewed_exclusion_blocks_the_match(cache):
    """A reviewed name collision stays unresolved, per governance data."""
    indexes = {"bioconductor": r.registry_names(BIOC, cache)}
    t = tool("mist", "MIST")
    assert r.registry_evidence(t, [BIOC], indexes, cache) is not None
    assert r.registry_evidence(t, [BIOC], indexes, cache,
                               excluded={("mist", "bioconductor")}) is None


def test_an_unknown_name_matches_nothing(cache):
    indexes = {"bioconductor": r.registry_names(BIOC, cache)}
    assert r.registry_evidence(tool("nosuchtool", "NoSuchTool"), [BIOC], indexes, cache) is None


def test_an_unreachable_registry_yields_an_empty_index(tmp_path):
    """A failed fetch must not look like an empty registry that resolved fine."""
    assert r.registry_names(BIOC, tmp_path / "empty") == {}


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
# End to end                                                                  #
# --------------------------------------------------------------------------- #

def test_resolve_writes_only_tool_backed_entries(tmp_path, cache):
    d = tmp_path / "col"
    d.mkdir()
    (d / "tools_index.json").write_text(json.dumps([
        tool("xcms", "XCMS", ["10.1/xcms"]),
        tool("camera", "CAMERA", ["10.1/lipidin"]),
        tool("nothing", "Nothing", ["10.1/lipidin"]),
    ]))
    (d / "corpus.yaml").write_text(yaml.safe_dump({"papers": [
        {"doi": "10.1/xcms", "name": "XCMS", "repo_url": "sneumann/xcms",
         "license_detection": "license-file", "access": {"license": "LGPL-3.0"}},
        {"doi": "10.1/lipidin", "name": "LipidIN", "repo_url": "LinShuhaiLAB/LipidIN",
         "license_detection": "github-api", "access": {"license": "Apache-2.0"}},
    ]}))
    summary = r.resolve(str(d), cache, registries=[BIOC, CONDA])
    out = json.loads((d / "tool_licenses.json").read_text())

    assert summary["conflicts"] == {}
    # CAMERA is cited by an Apache-2.0 paper and is itself GPL. The registry wins,
    # and the citing paper never contributes.
    assert out["camera"]["license"] == "GPL-2.0-or-later"
    assert out["xcms"]["license"] == "GPL-2.0-or-later"
    # A tool with neither route resolves to nothing at all.
    assert "nothing" not in out


def test_the_shipped_registry_config_is_well_formed():
    """Every declared registry and exclusion carries the fields the resolver reads."""
    config = r.load_registry_config()
    assert config["registries"], "no registries declared"
    for reg in config["registries"]:
        for field in ("id", "detection", "index_url", "index_shape",
                      "license_field", "license_format", "repo_fields"):
            assert reg.get(field), f"{reg.get('id')}: missing {field}"
        if reg["index_shape"] == "name_list":
            assert reg.get("package_url"), f"{reg['id']}: name_list needs package_url"
    ids = {reg["id"] for reg in config["registries"]}
    for excl in config.get("excluded_matches") or []:
        assert excl.get("tool") and excl.get("reason"), f"incomplete exclusion: {excl}"
        assert excl["registry"] in ids, f"{excl['tool']}: unknown registry {excl['registry']!r}"


def test_every_registry_detection_counts_as_tool_evidence():
    """A detection the tier resolver does not recognise would silently stay unknown."""
    from scripts.license_tier import TOOL_DETECTIONS
    for reg in r.load_registry_config()["registries"]:
        assert reg["detection"] in TOOL_DETECTIONS, reg["detection"]


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
