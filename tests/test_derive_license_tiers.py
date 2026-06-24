import pathlib, sys, textwrap, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import derive_license_tiers as d


def test_parse_repo_variants():
    assert d.parse_repo("https://github.com/iomega/spec2vec") == ("iomega", "spec2vec")
    assert d.parse_repo("https://github.com/a/b.git") == ("a", "b")
    assert d.parse_repo("owner/repo") == ("owner", "repo")
    assert d.parse_repo("") is None
    assert d.parse_repo("https://example.org/x") is None

def test_parse_repo_tolerates_punctuation_and_paths():
    assert d.parse_repo("idrblab/NOREVA;") == ("idrblab", "NOREVA")
    assert d.parse_repo("https://github.com/a/b/tree/main") == ("a", "b")
    assert d.parse_repo("https://github.com/a/b?tab=readme") == ("a", "b")
    assert d.parse_repo("https://github.com/a/b#readme") == ("a", "b")
    assert d.parse_repo("https://github.com/a/b.git") == ("a", "b")   # still works

def test_tier_for_repo_maps_spdx():
    det = lambda o, r, t: ({"iomega/spec2vec": "Apache-2.0"}.get(f"{o}/{r}"), "github-api")
    tier, lic, src = d.tier_for_repo("https://github.com/iomega/spec2vec", _detect=det)
    assert (tier, lic) == ("open", "Apache-2.0")

def test_tier_for_repo_noncommercial():
    det = lambda o, r, t: ("CC-BY-NC-4.0", "github-api")
    tier, lic, src = d.tier_for_repo("https://github.com/x/y", _detect=det)
    assert (tier, lic) == ("noncommercial", "CC-BY-NC-4.0")

def test_tier_for_repo_no_license_is_restricted():
    tier, lic, src = d.tier_for_repo("https://github.com/x/y", _detect=lambda o, r, t: (None, "none"))
    assert (tier, lic) == ("restricted", None)
    tier, lic, src = d.tier_for_repo("not-a-repo", _detect=lambda o, r, t: ("MIT", "github-api"))
    assert (tier, lic) == ("restricted", None)

def test_tier_for_repo_uses_cache(tmp_path):
    calls = []
    def det(o, r, t): calls.append((o, r)); return ("MIT", "github-api")
    cache = {}
    d.tier_for_repo("https://github.com/a/b", cache=cache, _detect=det)
    d.tier_for_repo("https://github.com/a/b", cache=cache, _detect=det)
    assert calls == [("a", "b")]            # second call served from cache
    assert cache == {"a/b": {"id": "MIT", "source": "github-api"}}

def test_apply_to_corpus_writes_tiers(tmp_path):
    corpus = tmp_path / "corpus.yaml"
    corpus.write_text(textwrap.dedent('''
        schema: asb-corpus/1.0
        papers:
        - name: A
          doi: 10.1/a
          repo_url: https://github.com/a/open
          status: included
          access: {type: repo-oa, is_oa: true}
        - name: B
          doi: 10.1/b
          repo_url: https://github.com/b/nc
          status: included
          access: {type: repo-oa, is_oa: true}
    '''))
    def det(o, r, t):
        lic = {"a/open": "MIT", "b/nc": "CC-BY-NC-4.0"}.get(f"{o}/{r}")
        return (lic, "github-api")
    summary = d.apply_to_corpus(str(corpus), token=None, _detect=det)
    out = yaml.safe_load(corpus.read_text())["papers"]
    assert out[0]["license_tier"] == "open" and out[0]["access"]["license"] == "MIT"
    assert out[1]["license_tier"] == "noncommercial" and out[1]["access"]["license"] == "CC-BY-NC-4.0"
    assert out[0]["access"]["type"] == "repo-oa"
    assert out[1]["access"]["type"] == "repo-oa"
    assert out[0]["license_detection"] == "github-api"
    assert out[1]["license_detection"] == "github-api"
    assert summary == {"open": 1, "noncommercial": 1}

def test_apply_to_corpus_respects_license_locked(tmp_path):
    corpus = tmp_path / "corpus.yaml"
    corpus.write_text(textwrap.dedent('''
        papers:
        - name: Locked
          doi: 10.1/x
          repo_url: https://github.com/a/b
          license_tier: noncommercial
          license_locked: true
          access: {type: repo-oa, license: "Academic; commercial by permission"}
        - name: Auto
          doi: 10.1/y
          repo_url: https://github.com/c/d
          access: {type: repo-oa}
    '''))
    # _detect would say both are MIT(open); the locked one must stay noncommercial.
    summary = d.apply_to_corpus(str(corpus), token=None, _detect=lambda o, r, t: ("MIT", "github-api"))
    out = yaml.safe_load(corpus.read_text())["papers"]
    assert out[0]["license_tier"] == "noncommercial"               # locked, untouched
    assert out[0]["access"]["license"] == "Academic; commercial by permission"
    assert out[1]["license_tier"] == "open"                        # auto-derived
    assert out[1]["license_detection"] == "github-api"
    assert summary == {"noncommercial": 1, "open": 1}


def test_classify_license_text():
    assert d.classify_license_text("Apache License\nVersion 2.0") == "Apache-2.0"
    assert d.classify_license_text("Permission is hereby granted, free of charge") == "MIT"
    assert d.classify_license_text("GNU AFFERO GENERAL PUBLIC LICENSE") == "AGPL-3.0"
    assert d.classify_license_text("GNU GENERAL PUBLIC LICENSE\nVersion 3") == "GPL-3.0"
    assert d.classify_license_text("Mozilla Public License Version 2.0") == "MPL-2.0"
    assert d.classify_license_text("Creative Commons Attribution-NonCommercial 4.0") == "CC-BY-NC-4.0"
    assert d.classify_license_text("Creative Commons Attribution 4.0 International") == "CC-BY-4.0"
    assert d.classify_license_text("Redistribution and use in source and binary forms") == "BSD-3-Clause"
    assert d.classify_license_text("some random readme text") is None


def test_detect_license_primary_api_wins():
    det = d.detect_license("o", "r", "t", _fetch_api=lambda o, r, t: "MIT",
                           _contents=lambda o, r, t: (_ for _ in ()).throw(AssertionError("should not be called")),
                           _fetch_file=None)
    assert det == ("MIT", "github-api")


def test_detect_license_falls_back_to_license_file():
    det = d.detect_license("o", "r", "t", _fetch_api=lambda o, r, t: None,
                           _contents=lambda o, r, t: ["README.md", "LICENSE.md"],
                           _fetch_file=lambda o, r, p, t: "Apache License Version 2.0")
    assert det == ("Apache-2.0", "license-file")


def test_detect_license_file_present_unclassified():
    det = d.detect_license("o", "r", "t", _fetch_api=lambda o, r, t: None,
                           _contents=lambda o, r, t: ["COPYING"],
                           _fetch_file=lambda o, r, p, t: "see our website for terms")
    assert det == (None, "file-present-unclassified")


def test_detect_license_none_when_no_file():
    det = d.detect_license("o", "r", "t", _fetch_api=lambda o, r, t: None,
                           _contents=lambda o, r, t: ["README.md", "setup.py"],
                           _fetch_file=None)
    assert det == (None, "none")


def test_tier_for_repo_threetuple_and_unclassified_is_restricted():
    det = lambda o, r, t: (None, "file-present-unclassified")
    tier, lic, src = d.tier_for_repo("https://github.com/o/r", _detect=det)
    assert (tier, src) == ("restricted", "file-present-unclassified")


def test_apply_to_corpus_writes_license_detection(tmp_path):
    corpus = tmp_path / "corpus.yaml"
    corpus.write_text(textwrap.dedent('''
        papers:
        - {name: A, doi: 10.1/a, repo_url: https://github.com/a/open, status: included, access: {type: repo-oa}}
    '''))
    det = lambda o, r, t: ("MIT", "license-file")
    d.apply_to_corpus(str(corpus), token=None, _detect=det)
    p = yaml.safe_load(corpus.read_text())["papers"][0]
    assert p["license_tier"] == "open" and p["access"]["license"] == "MIT" and p["license_detection"] == "license-file"


def test_full_cc_by_nc_text_classifies_nc():
    # a realistic CC BY-NC file contains both the CC-BY phrase and "NonCommercial"
    txt = "Creative Commons Attribution-NonCommercial 4.0 International Public License"
    assert d.classify_license_text(txt) == "CC-BY-NC-4.0"


def test_passing_mention_of_noncommercial_does_not_become_nc():
    # a permissive license that merely mentions the word must NOT be classified NC
    txt = "MIT License. Note: a noncommercial companion dataset is available separately."
    assert d.classify_license_text(txt) == "MIT"   # MIT rule wins; not CC-BY-NC


def test_custom_noncommercial_without_cc_phrases_is_unclassified():
    txt = "This software is provided for noncommercial research purposes only."
    assert d.classify_license_text(txt) is None     # falls through -> file-present-unclassified upstream
