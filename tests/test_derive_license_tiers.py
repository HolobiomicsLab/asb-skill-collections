import pathlib, sys, textwrap

import pytest
import yaml
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


# --- R packages declare their licence in DESCRIPTION, not LICENSE ------------

@pytest.mark.parametrize("field,expected", [
    ("MIT + file LICENSE", "MIT"),
    ("GPL-3", "GPL-3.0-only"),
    ("BSD_3_clause + file LICENSE", "BSD-3-Clause"),
    ("Artistic-2.0", "Artistic-2.0"),
    ("mit", "MIT"),
])
def test_an_r_description_licence_field_resolves(field, expected):
    """`usethis::use_mit_license()` writes a LICENSE holding only YEAR and
    COPYRIGHT HOLDER; the licence itself is only ever in DESCRIPTION."""
    assert d.spdx_from_r_description(f"Package: x\nLicense: {field}\n") == expected


@pytest.mark.parametrize("text", [
    "Package: x\nLicense: file LICENSE\n",   # names a file, declares nothing
    "Package: x\n",                          # no License field at all
    "Package: x\nLicense: Some Bespoke Academic Terms\n",
    "",
])
def test_an_r_description_that_declares_nothing_returns_none(text):
    """The other side. A guess here would stamp a tier on an unread licence."""
    assert d.spdx_from_r_description(text) is None


def test_the_r_path_only_runs_when_the_licence_text_could_not_be_read():
    """It must not override a LICENSE file the classifier *did* understand."""
    out = d.detect_license(
        "o", "r", None,
        _fetch_api=lambda *a: None,
        _contents=lambda *a: ["LICENSE", "DESCRIPTION"],
        _fetch_file=lambda o, r, name, t: (
            "Permission is hereby granted, free of charge" if name == "LICENSE"
            else "License: GPL-3\n"),
    )
    assert out == ("MIT", "license-file")


def test_an_r_stub_licence_is_rescued_by_the_description():
    out = d.detect_license(
        "o", "r", None,
        _fetch_api=lambda *a: None,
        _contents=lambda *a: ["LICENSE", "DESCRIPTION"],
        _fetch_file=lambda o, r, name, t: (
            "YEAR: 2024\nCOPYRIGHT HOLDER: someone\n" if name == "LICENSE"
            else "Package: x\nLicense: MIT + file LICENSE\n"),
    )
    assert out == ("MIT", "r-description")


def test_a_repo_with_no_description_still_reports_the_stub_honestly():
    out = d.detect_license(
        "o", "r", None,
        _fetch_api=lambda *a: None,
        _contents=lambda *a: ["LICENSE"],
        _fetch_file=lambda *a: "YEAR: 2024\nCOPYRIGHT HOLDER: someone\n",
    )
    assert out == (None, "file-present-unclassified")


def test_a_repo_with_no_licence_file_at_all_is_unchanged():
    out = d.detect_license("o", "r", None, _fetch_api=lambda *a: None,
                           _contents=lambda *a: [], _fetch_file=lambda *a: "")
    assert out == (None, "none")


def test_an_entry_with_no_repository_keeps_what_the_paper_resolver_established(tmp_path):
    """Both scripts write license_tier / access.license / license_detection.

    Only one of them has evidence for any given entry: this one reads a code
    repository, `resolve_paper_license` reads the DOI registry. Overwriting a
    registry-established CC-BY with `restricted` because there is no repo to
    read is how 45 resolved licences got destroyed in one run.
    """
    c = tmp_path / "corpus.yaml"
    c.write_text(textwrap.dedent('''
        papers:
        - name: from-registry
          doi: 10.1/a
          repo_url: ""
          access: {license: CC-BY-4.0, type: open-access}
          license_tier: open
          license_detection: crossref-paper
    ''').strip() + "\n", encoding="utf-8")
    d.apply_to_corpus(c, token=None, _detect=lambda *a, **k: (None, "none"))
    entry = yaml.safe_load(c.read_text())["papers"][0]
    assert entry["license_tier"] == "open"
    assert entry["access"]["license"] == "CC-BY-4.0"
    assert entry["license_detection"] == "crossref-paper"


def test_an_entry_with_a_repository_is_still_derived(tmp_path):
    """The other side: skipping too much would make the script a no-op."""
    c = tmp_path / "corpus.yaml"
    c.write_text(textwrap.dedent('''
        papers:
        - name: from-repo
          doi: 10.1/b
          repo_url: https://github.com/o/r
          access: {}
          license_tier: restricted
          license_detection: none
    ''').strip() + "\n", encoding="utf-8")
    d.apply_to_corpus(c, token=None, _detect=lambda *a, **k: ("MIT", "github-api"))
    entry = yaml.safe_load(c.read_text())["papers"][0]
    assert entry["license_tier"] == "open"
    assert entry["license_detection"] == "github-api"


def test_a_failed_lookup_never_erases_an_established_licence(tmp_path):
    """Fifteen `readme-llm` licences were wiped by one re-run before this guard.

    The GitHub API and the LICENSE text both came back empty, and the empty
    answer was written straight over a licence somebody had already read.
    """
    c = tmp_path / "corpus.yaml"
    c.write_text(textwrap.dedent('''
        papers:
        - name: read-from-readme
          doi: 10.1/a
          repo_url: https://github.com/o/r
          access: {license: LGPL-3.0}
          license_tier: open
          license_detection: readme-llm
    ''').strip() + "\n", encoding="utf-8")
    d.apply_to_corpus(c, token=None, _detect=lambda *a, **k: (None, "none"))
    entry = yaml.safe_load(c.read_text())["papers"][0]
    assert entry["access"]["license"] == "LGPL-3.0"
    assert entry["license_detection"] == "readme-llm"


def test_a_failed_lookup_may_still_overwrite_an_unestablished_one(tmp_path):
    """The other side: a `none` entry has nothing to protect, and pinning it
    would freeze the corpus against every future improvement."""
    c = tmp_path / "corpus.yaml"
    c.write_text(textwrap.dedent('''
        papers:
        - name: never-established
          doi: 10.1/b
          repo_url: https://github.com/o/r
          access: {license: null}
          license_tier: restricted
          license_detection: none
    ''').strip() + "\n", encoding="utf-8")
    d.apply_to_corpus(c, token=None, _detect=lambda *a, **k: (None, "file-present-unclassified"))
    assert yaml.safe_load(c.read_text())["papers"][0]["license_detection"] == "file-present-unclassified"


def test_a_successful_lookup_still_updates_an_established_licence(tmp_path):
    """And a real answer must always win, or the corpus can never be corrected."""
    c = tmp_path / "corpus.yaml"
    c.write_text(textwrap.dedent('''
        papers:
        - name: now-known-properly
          doi: 10.1/c
          repo_url: https://github.com/o/r
          access: {license: BSD}
          license_tier: open
          license_detection: readme-llm
    ''').strip() + "\n", encoding="utf-8")
    d.apply_to_corpus(c, token=None, _detect=lambda *a, **k: ("Apache-2.0", "github-api"))
    entry = yaml.safe_load(c.read_text())["papers"][0]
    assert entry["access"]["license"] == "Apache-2.0"
    assert entry["license_detection"] == "github-api"


@pytest.mark.parametrize("field,expected", [
    ("GPL (>= 2)", "GPL-2.0-or-later"),
    ("GPL (>= 3)", "GPL-3.0-or-later"),
    ("LGPL (>= 2.1)", "LGPL-2.1-or-later"),
    ("AGPL (>= 3)", "AGPL-3.0-or-later"),
])
def test_an_r_version_floor_is_kept_not_discarded(field, expected):
    """`GPL (>= 2)` is "version 2 or later". Dropping the floor and mapping the
    bare family would record a version the package never declared."""
    assert d.spdx_from_r_description(f"License: {field}\n") == expected


def test_a_version_floor_on_a_non_versioned_family_is_ignored():
    """Only the GPL families carry a meaningful floor; MIT has no versions."""
    assert d.spdx_from_r_description("License: MIT (>= 2)\n") == "MIT"
