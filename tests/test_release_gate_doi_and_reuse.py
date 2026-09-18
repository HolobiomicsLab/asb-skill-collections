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
                "license_tier": "open",
                "access": {"type": "open-access", "source_reuse": "restricted"},
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


def test_noncommercial_oa_source_uses_the_strict_caps(tmp_path):
    corpus = {
        "papers": [
            {
                "doi": "10.1/example",
                "license_tier": "noncommercial",
                "access": {"type": "open-access", "source_reuse": "permissive"},
            }
        ]
    }
    collection = _quoted_collection(tmp_path, "10.1/example", 301)

    result = release_gate.check_strip_verbatim(
        collection,
        release_gate._access_tier_from_corpus(corpus),
        release_gate._reuse_by_doi_from_corpus(corpus),
    )

    assert _failures(result)
    assert result.coverage["strict_regime_dois"] == 1
    assert result.coverage["permissive_regime_dois"] == 0


def test_policy_findings_keep_the_reader_facing_raw_doi(tmp_path):
    raw_doi = "https://doi.org/10.1/EXAMPLE"
    collection = _quoted_collection(tmp_path, raw_doi, 301)

    result = release_gate.check_strip_verbatim(
        collection,
        {"doi:10.1/example": "open-access"},
        {"http://doi.org/10.1/example": False},
    )

    assert _failures(result)[0]["doi"] == raw_doi


def test_reuse_map_falls_back_only_when_license_tier_is_absent():
    corpus = {
        "papers": [
            {
                "doi": "10.1/fallback",
                "access": {"type": "open-access", "source_reuse": "permissive"},
            },
            {
                "doi": "10.1/tier-wins",
                "license_tier": "restricted",
                "access": {"type": "open-access", "source_reuse": "permissive"},
            },
            {"doi": "10.1/missing", "access": {"type": "open-access"}},
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/fallback": True,
        "10.1/tier-wins": False,
        "10.1/missing": False,
    }


def test_reuse_map_reads_the_paper_licence_when_no_tier_or_reuse_field_exists():
    """The v1 corpora record the paper licence under ``access.license`` only."""
    corpus = {
        "papers": [
            {
                "doi": "10.1/cc-by",
                "access": {"type": "gold-oa", "license": "cc-by"},
                "license_subject": "paper",
            },
            {"doi": "10.1/cc-by-sa", "access": {"type": "gold-oa", "license": "CC-BY-SA-4.0"}},
            {"doi": "10.1/cc-by-nc", "access": {"type": "open-access", "license": "CC-BY-NC-ND-4.0"}},
            {"doi": "10.1/cc-by-nd", "access": {"type": "open-access", "license": "CC BY-ND 4.0"}},
            {"doi": "10.1/cc0", "access": {"type": "gold-oa", "license": "CC0-1.0"}},
            {"doi": "10.1/code-licence", "access": {"type": "repo-oa", "license": "MIT"}},
            {"doi": "10.1/no-licence", "access": {"type": "gold-oa", "license": None}},
        ]
    }

    assert release_gate._reuse_by_doi_from_corpus(corpus) == {
        "10.1/cc-by": True,
        "10.1/cc-by-sa": True,
        "10.1/cc-by-nc": False,
        "10.1/cc-by-nd": False,
        "10.1/cc0": True,
        "10.1/code-licence": False,
        "10.1/no-licence": False,
    }


def test_released_v1_corpora_resolve_every_doi_as_permissive():
    """Regression: the released epigenomics and transcriptomics v1 corpora are all CC BY.

    Without the paper-licence fallback every one of their DOIs fell closed into
    the strict regime and the released collections failed the gate they had
    passed at release time.
    """
    for name in ("epigenomics", "transcriptomics"):
        corpus = yaml.safe_load(
            (REPO / "collections" / name / "v1" / "corpus.yaml").read_text(encoding="utf-8")
        )
        reuse = release_gate._reuse_by_doi_from_corpus(corpus)
        assert reuse, name
        assert all(reuse.values()), (name, [doi for doi, ok in reuse.items() if not ok])


def test_omitted_reuse_map_keeps_legacy_behavior_with_warning(tmp_path):
    collection = _quoted_collection(tmp_path, "10.1/example", 301)

    result = release_gate.check_strip_verbatim(
        collection, {"10.1/example": "open-access"}
    )

    assert not _failures(result)
    assert result.status == release_gate.WARN
    assert "P2 was not applied" in result.summary
    assert any("P2 was not applied" in detail["message"] for detail in result.details)
