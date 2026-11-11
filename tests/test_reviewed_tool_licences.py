"""governance/tool_licences_reviewed.yaml: its loader, its validator, and how contexts apply."""
import copy
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import reviewed_tool_licences as rv
from scripts.tool_identity import RecordContext

PLAIN = {"names": ["scikit-learn", "sklearn", "Scikit-learn"], "entity": "scikit-learn",
         "entry_kind": "software", "category": "package", "license": "BSD-3-Clause",
         "license_tier": "open", "repo_url": "https://github.com/scikit-learn/scikit-learn",
         "homepage": "https://scikit-learn.org",
         "evidence_url": "https://github.com/scikit-learn/scikit-learn/blob/main/COPYING",
         "verified": "2026-11-11", "note": None}

AMBIGUOUS = {"names": ["UMAP", "umap"], "entity": None, "ambiguous": True,
             "verified": "2026-11-11", "contexts": [
                 {"when": "dimension reduction, embedding, single-cell",
                  "match": {"any_terms": ["single-cell", "dimension reduction"],
                            "none_terms": ["mappability"]},
                  "entity": "UMAP (umap-learn)", "entry_kind": "software",
                  "license": "BSD-3-Clause", "license_tier": "open",
                  "repo_url": "https://github.com/lmcinnes/umap",
                  "evidence_url": "https://github.com/lmcinnes/umap/blob/master/LICENSE.txt"},
                 {"when": "genome mappability tracks (Umap and Bismap)",
                  "match": {"any_terms": ["mappability", "Bismap"]},
                  "entity": "Umap (Hoffman lab)", "leave_unknown": True}]}


def doc(*entries):
    return {"version": 1, "reviewed": "2026-11-11", "entries": [copy.deepcopy(e) for e in entries]}


def ctx(text="", collection="transcriptomics"):
    return RecordContext(collection=collection, life_science=True, names=["UMAP"],
                         local_text=text, skill_text="")


def test_the_brief_format_validates():
    assert rv.validate(doc(PLAIN, AMBIGUOUS)) == []


def test_the_shipped_file_validates_and_loads():
    loaded = rv.load()
    assert loaded["entries"], "the reviewed map ships with entries"
    assert rv.validate(loaded) == []


def test_a_missing_file_is_an_empty_map(tmp_path):
    assert rv.load(tmp_path / "absent.yaml")["entries"] == []


def test_a_malformed_file_refuses_to_load(tmp_path):
    bad = doc(PLAIN)
    bad["entries"][0]["license_tier"] = "closed"
    p = tmp_path / "m.yaml"
    p.write_text(yaml.safe_dump(bad))
    with pytest.raises(rv.ReviewedMapError):
        rv.load(p)


@pytest.mark.parametrize("change,needle", [
    ({"license": "CC-BY-NC-4.0"}, "reads as 'noncommercial'"),
    ({"license": "GPL-3.0-only", "license_tier": "restricted"}, "reads as 'open'"),
    ({"entry_kind": "plugin"}, "entry_kind"),
    ({"evidence_url": None}, "evidence_url"),
    ({"verified": "11/11/2026"}, "verified"),
    ({"license": None}, "tier open needs a licence"),
    ({"category": "library"}, "category"),
])
def test_an_inconsistent_plain_entry_is_reported(change, needle):
    entry = {**PLAIN, **change}
    problems = rv.validate(doc(entry))
    assert any(needle in p for p in problems), problems


def test_an_artefact_has_no_licence():
    entry = {**PLAIN, "entry_kind": "artefact"}
    assert any("artefact" in p for p in rv.validate(doc(entry)))


def test_a_vendor_product_is_restricted_or_unknown():
    entry = {**PLAIN, "entry_kind": "vendor_product", "license": None, "license_tier": "open"}
    assert any("vendor product" in p for p in rv.validate(doc(entry)))


def test_a_name_may_be_listed_once():
    other = {**PLAIN, "names": ["SKLEARN"], "entity": "dup"}
    assert any("also in" in p for p in rv.validate(doc(PLAIN, other)))


def test_an_ambiguous_entry_needs_two_contexts_and_well_formed_match_keys():
    one = copy.deepcopy(AMBIGUOUS)
    one["contexts"] = one["contexts"][:1]
    assert any("two contexts" in p for p in rv.validate(doc(one)))
    bad_key = copy.deepcopy(AMBIGUOUS)
    bad_key["contexts"][0]["match"] = {"topics": ["x"]}
    assert any("match keys" in p for p in rv.validate(doc(bad_key)))


def test_a_plain_entry_applies_as_is():
    reading, reason = rv.apply(PLAIN, ctx())
    assert reading["license"] == "BSD-3-Clause" and reason == "reviewed"


def test_an_ambiguous_entry_applies_its_single_matching_context():
    reading, reason = rv.apply(AMBIGUOUS, ctx("clusters shown in a single-cell UMAP"))
    assert reading["entity"] == "UMAP (umap-learn)" and reason == "reviewed-context"


def test_an_ambiguous_entry_with_no_matching_context_stays_unknown():
    assert rv.apply(AMBIGUOUS, ctx("UMAP")) == (None, "reviewed-ambiguous-no-single-context")


def test_two_matching_contexts_leave_the_record_unknown():
    both = copy.deepcopy(AMBIGUOUS)
    both["contexts"][0]["match"].pop("none_terms")
    reading, reason = rv.apply(both, ctx("single-cell mappability"))
    assert reading is None and reason == "reviewed-ambiguous-several-contexts"


def test_a_leave_unknown_context_resolves_nothing():
    assert rv.apply(AMBIGUOUS, ctx("Umap and Bismap mappability tracks")) == (
        None, "reviewed-context-leave-unknown")


def test_a_context_without_match_keys_never_matches():
    """A `when` sentence is for the reader; it is never interpreted."""
    loose = copy.deepcopy(AMBIGUOUS)
    for context in loose["contexts"]:
        context.pop("match")
    assert rv.validate(doc(loose)) == []
    assert rv.apply(loose, ctx("single-cell dimension reduction"))[0] is None


def test_ecosystem_and_collection_keys():
    entry = copy.deepcopy(AMBIGUOUS)
    entry["contexts"][0]["match"] = {"ecosystems": ["python"], "collections": ["transcriptomics"]}
    assert rv.apply(entry, ctx("import umap"))[0]["entity"] == "UMAP (umap-learn)"
    assert rv.apply(entry, ctx("import umap", collection="genomics"))[0] is None
    assert rv.apply(entry, ctx("library(umap)"))[0] is None


def test_names_match_after_normalisation():
    index = rv.index(doc(PLAIN))
    assert index["scikitlearn"]["entity"] == "scikit-learn"
    assert "sklearn" in index


@pytest.mark.parametrize("name", ["SIRIUS", "Sirius", "SIRIUS4", "ZODIAC", "COSMIC"])
def test_the_sirius_family_is_academic_use_only_in_a_mass_spectrometry_collection(name):
    """The README reserves use to academic research; other users need a licence."""
    entry = rv.index(rv.load())[rv.normalize(name)]
    reading, reason = rv.apply(entry, ctx(collection="metabolomics"))
    assert reason == "reviewed-context"
    assert (reading["license_tier"], reading["license"]) == (
        "noncommercial", "LicenseRef-SIRIUS-academic-use")


def test_the_sirius_family_names_mean_something_else_elsewhere():
    index = rv.index(rv.load())
    # The Catalogue Of Somatic Mutations In Cancer, and a star.
    assert rv.apply(index[rv.normalize("COSMIC")], ctx(collection="genomics"))[0] is None
    assert rv.apply(index[rv.normalize("SIRIUS")], ctx(collection="astronomy"))[0] is None
    assert rv.apply(index[rv.normalize("ZODIAC")], ctx(collection="agentic-ai"))[0] is None

