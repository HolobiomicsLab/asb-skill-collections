"""Regression tests for DOI identity and the P2 text-reuse regime."""

from pathlib import Path

import yaml

from scripts import release_gate

REPO = Path(__file__).resolve().parents[1]


def _quoted_collection(tmp_path, doi: str, quote_length: int):
    collection = tmp_path / "collection"
    leaf = collection / "leaves" / "example"
    leaf.mkdir(parents=True)
    (leaf / "SKILL.md").write_text(
        "---\n"
        "name: example\n"
        "derived_from:\n"
        f"- doi: {doi}\n"
        "---\n"
        f'- [methods] extraction: "{"x" * quote_length}"\n',
        encoding="utf-8",
    )
    return collection


def _failures(result):
    return [detail for detail in result.details if detail["status"] == release_gate.FAIL]


def test_doi_variants_resolve_to_the_same_access_and_reuse_flags(tmp_path):
    corpus = {
        "papers": [
            {
                "doi": "10.1093/BIB/BBAE608",
                "license_subject": "paper",
                "license_tier": "open",
                "access": {"type": "open-access"},
            }
        ]
    }
    collection = _quoted_collection(
        tmp_path, "https://doi.org/10.1093/bib/bbae608", 301
    )

    access = release_gate._access_tier_from_corpus(corpus)
    reuse = release_gate._reuse_by_doi_from_corpus(corpus)
    result = release_gate.check_strip_verbatim(collection, access, reuse)

    assert access == {"10.1093/bib/bbae608": "open-access"}
    assert reuse == {"10.1093/bib/bbae608": True}
    assert not _failures(result)


def test_all_supported_doi_prefixes_share_one_identity():
    variants = (
        " 10.1093/BIB/BBAE608 ",
        "https://doi.org/10.1093/bib/bbae608",
        "http://doi.org/10.1093/BIB/BBAE608",
        " DOI:10.1093/bib/bbae608 ",
    )

    assert {release_gate._norm_doi(doi) for doi in variants} == {
        "10.1093/bib/bbae608"
    }


def test_explicit_span_doi_is_normalized_before_policy_lookup(tmp_path):
    collection = tmp_path / "collection"
    leaf = collection / "leaves" / "example"
    leaf.mkdir(parents=True)
    (leaf / "SKILL.md").write_text(
        "---\n"
        "name: example\n"
        "evidence_spans:\n"
        "- doi: ' DOI:10.1093/BIB/BBAE608 '\n"
        f"  text: '{'x' * 301}'\n"
        "---\n",
        encoding="utf-8",
    )

    result = release_gate.check_strip_verbatim(
        collection,
        {"http://doi.org/10.1093/bib/bbae608": "open-access"},
        {"10.1093/bib/bbae608": True},
    )

    assert not _failures(result)


def test_tool_subject_licence_is_not_paper_text_evidence():
    corpus = {
        "papers": [
            {
                "doi": "10.1/tool-subject",
                "license_subject": "tool",
                "license_tier": "restricted",
                "access": {"type": "open-access", "license": "mit"},
            },
            {
                "doi": "10.1/paper-subject",
                "license_subject": "paper",
                "license_tier": "restricted",
                "access": {"type": "open-access", "license": "mit"},
            },
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/paper-subject": False
    }


def test_paper_subject_tiers_set_permissive_and_strict_reuse():
    corpus = {
        "papers": [
            {
                "doi": "10.1/open",
                "license_subject": "paper",
                "license_tier": "open",
                "access": {"type": "open-access"},
            },
            {
                "doi": "10.1/noncommercial",
                "license_subject": "paper",
                "license_tier": "noncommercial",
                "access": {"type": "open-access"},
            },
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/open": True,
        "10.1/noncommercial": False,
    }


def test_pre_subject_schema_reads_access_paper_licence():
    corpus = {
        "papers": [
            {
                "doi": "10.1/cc-by",
                "access": {"type": "gold-oa", "license": "cc-by"},
            },
            {
                "doi": "10.1/cc-by-nc-nd",
                "access": {
                    "type": "open-access",
                    "license": "CC-BY-NC-ND-4.0",
                },
            },
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/cc-by": True,
        "10.1/cc-by-nc-nd": False,
    }


def test_source_reuse_precedes_subject_and_tier():
    corpus = {
        "papers": [
            {
                "doi": "10.1/restricted-open",
                "license_subject": "paper",
                "license_tier": "open",
                "access": {"type": "open-access", "source_reuse": "restricted"},
            },
            {
                "doi": "10.1/restricted-restricted",
                "license_subject": "paper",
                "license_tier": "restricted",
                "access": {"type": "open-access", "source_reuse": "restricted"},
            },
            {
                "doi": "10.1/permissive-restricted",
                "license_subject": "paper",
                "license_tier": "restricted",
                "access": {"type": "open-access", "source_reuse": "permissive"},
            },
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/restricted-open": False,
        "10.1/restricted-restricted": False,
        "10.1/permissive-restricted": True,
    }


def test_unknown_paper_tier_falls_back_to_licence_or_stays_absent():
    corpus = {
        "papers": [
            {
                "doi": "10.1/unknown-missing",
                "license_subject": "paper",
                "license_tier": "unknown",
                "access": {"type": "open-access"},
            },
            {
                "doi": "10.1/unknown-open",
                "license_subject": "paper",
                "license_tier": "unknown",
                "access": {"type": "open-access", "license": "cc-by"},
            },
            {
                "doi": "10.1/unknown-restricted",
                "license_subject": "paper",
                "license_tier": "unknown",
                "access": {"type": "open-access", "license": "cc-by-nc-nd"},
            },
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/unknown-open": True,
        "10.1/unknown-restricted": False,
    }


def test_unknown_text_licence_follows_access_only_caps(tmp_path):
    open_collection = _quoted_collection(tmp_path / "open", "10.1/open", 301)
    closed_collection = _quoted_collection(tmp_path / "closed", "10.1/closed", 301)

    open_result = release_gate.check_strip_verbatim(
        open_collection, {"10.1/open": "open-access"}, {}
    )
    closed_result = release_gate.check_strip_verbatim(
        closed_collection, {"10.1/closed": "closed"}, {}
    )

    assert not _failures(open_result)
    assert open_result.coverage["strict_regime_dois"] == 0
    assert open_result.coverage["permissive_regime_dois"] == 1
    assert open_result.coverage["unknown_text_licence_dois"] == 1
    assert _failures(closed_result)
    assert closed_result.coverage["strict_regime_dois"] == 1
    assert closed_result.coverage["permissive_regime_dois"] == 0
    assert closed_result.coverage["unknown_text_licence_dois"] == 0


def test_policy_findings_keep_the_reader_facing_raw_doi(tmp_path):
    raw_doi = "https://doi.org/10.1/EXAMPLE"
    collection = _quoted_collection(tmp_path, raw_doi, 301)

    result = release_gate.check_strip_verbatim(
        collection,
        {"doi:10.1/example": "open-access"},
        {"http://doi.org/10.1/example": False},
    )

    assert _failures(result)[0]["doi"] == raw_doi


def test_released_v1_corpora_map_every_doi_to_true():
    """The v1 corpora mark every CC BY licence as paper-subject evidence."""
    for name in ("epigenomics", "transcriptomics"):
        corpus = yaml.safe_load(
            (REPO / "collections" / name / "v1" / "corpus.yaml").read_text(
                encoding="utf-8"
            )
        )
        expected_dois = {
            release_gate._norm_doi(paper["doi"]) for paper in corpus["papers"]
        }
        reuse = release_gate._reuse_by_doi_from_corpus(corpus)

        assert set(reuse) == expected_dois, name
        assert all(reuse.values()), (name, [doi for doi, ok in reuse.items() if not ok])


def test_legacy_access_only_path_warns_without_text_licence_class(tmp_path):
    collection = _quoted_collection(tmp_path, "10.1/example", 301)

    result = release_gate.check_strip_verbatim(
        collection, {"10.1/example": "open-access"}
    )

    assert not _failures(result)
    assert result.status == release_gate.WARN
    assert result.coverage["unknown_text_licence_dois"] == 0
    assert "P2 was not applied" in result.summary
    assert any("P2 was not applied" in detail["message"] for detail in result.details)
