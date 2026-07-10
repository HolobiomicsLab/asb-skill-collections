"""A skill that exists on disk must appear in every index its collection publishes.

The bug this guards: a skill grounded on a tool with no paper DOI never entered
`skills_index.json`, because the index was only ever joined onto entries that a
paper corpus had already created. It shipped, and nothing -- search, the MCP
server, the docs site, or CI -- could see it.
"""

import json
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import skill_index as si

# Four unrelated sciences. None of this module's logic may depend on the domain.
SCIENCES = ["metabolomics", "proteomics", "genomics", "astronomy"]


def write_skill(version_dir: pathlib.Path, slug: str, frontmatter: dict, body: str = "body") -> None:
    skill_dir = version_dir / "skills" / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"---\n{yaml.safe_dump(frontmatter)}---\n{body}\n", encoding="utf-8")


def leaf(name: str, tier: str = "open") -> dict:
    return {"name": name, "description": f"Use when working with {name}.",
            "metadata": {"license_tier": tier, "tools": [name.upper()]}}


def collection(tmp_path: pathlib.Path, science: str, skills: dict, indexed: list[str]) -> pathlib.Path:
    version_dir = tmp_path / "collections" / science / "v1"
    version_dir.mkdir(parents=True)
    for slug, frontmatter in skills.items():
        write_skill(version_dir, slug, frontmatter)
    entries = [si.entry_from_frontmatter(s, skills[s]) for s in indexed]
    (version_dir / "skills_index.json").write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding="utf-8")
    bundle = {"collection": science, "skills": {s: si.kb_entry_from_frontmatter(skills[s]) for s in indexed}}
    (version_dir / "kb_bundle.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    return version_dir


# --- Fires on every science: an unindexed content skill is always caught -------

@pytest.mark.parametrize("science", SCIENCES)
def test_orphan_skill_is_detected_in_every_science(tmp_path, science):
    skills = {"indexed-leaf": leaf("indexed-leaf"), "orphan-leaf": leaf("orphan-leaf")}
    version_dir = collection(tmp_path, science, skills, indexed=["indexed-leaf"])
    gaps = si.missing_from_indexes(version_dir)
    assert gaps["skills_index.json"] == ["orphan-leaf"], science
    assert gaps["kb_bundle.json"] == ["orphan-leaf"], science


@pytest.mark.parametrize("science", SCIENCES)
def test_fully_indexed_collection_is_clean_in_every_science(tmp_path, science):
    skills = {"a-leaf": leaf("a-leaf"), "b-leaf": leaf("b-leaf")}
    version_dir = collection(tmp_path, science, skills, indexed=["a-leaf", "b-leaf"])
    assert si.missing_from_indexes(version_dir) == {}, science


# --- Stays clean on genuinely not-indexable skills -----------------------------

def test_infrastructure_and_meta_skills_are_not_required_in_the_index(tmp_path):
    skills = {
        "_router": leaf("_router"),
        "collection-meta": {"name": "collection-meta", "description": "Use when starting.",
                            "metadata": {"role": "meta", "license_tier": "open"}},
        "real-leaf": leaf("real-leaf"),
    }
    version_dir = collection(tmp_path, "metabolomics", skills, indexed=["real-leaf"])
    assert si.missing_from_indexes(version_dir) == {}


def test_exclusion_is_by_declarative_property_not_by_name():
    assert si.is_indexable("masster", {"metadata": {"license_tier": "noncommercial"}})
    assert not si.is_indexable("_anything", {})
    assert not si.is_indexable("named-whatever", {"metadata": {"role": "meta"}})


def test_collection_publishing_no_index_is_not_flagged(tmp_path):
    version_dir = tmp_path / "collections" / "genomics" / "v1"
    write_skill(version_dir, "a-leaf", leaf("a-leaf"))
    assert si.missing_from_indexes(version_dir) == {}


# --- A non-open skill may never be indexed without its tier --------------------

def test_untiered_skill_is_refused_not_silently_nulled(tmp_path):
    untiered = {"name": "no-tier", "description": "Use when.", "metadata": {"tools": ["X"]}}
    version_dir = collection(tmp_path, "metabolomics", {"no-tier": untiered}, indexed=[])
    with pytest.raises(ValueError, match="license_tier"):
        si.add_missing(version_dir)


def test_untiered_predicate_rejects_every_invalid_tier():
    assert si.untiered("s", {})
    assert si.untiered("s", {"metadata": {"license_tier": None}})
    assert si.untiered("s", {"metadata": {"license_tier": "permissive"}})
    assert not si.untiered("s", {"metadata": {"license_tier": "noncommercial"}})


def test_noncommercial_skill_keeps_its_tier_through_indexing(tmp_path):
    skills = {"nc-leaf": leaf("nc-leaf", tier="noncommercial")}
    version_dir = collection(tmp_path, "metabolomics", skills, indexed=[])
    si.add_missing(version_dir)
    entry = json.loads((version_dir / "skills_index.json").read_text())[0]
    bundle = json.loads((version_dir / "kb_bundle.json").read_text())
    assert entry["license_tier"] == "noncommercial"
    assert bundle["skills"]["nc-leaf"]["license_tier"] == "noncommercial"


# --- add_missing is correct, sorted, idempotent, format-preserving -------------

def test_add_missing_inserts_sorted_and_is_idempotent(tmp_path):
    skills = {"zzz-leaf": leaf("zzz-leaf"), "aaa-leaf": leaf("aaa-leaf")}
    version_dir = collection(tmp_path, "proteomics", skills, indexed=["zzz-leaf"])
    si.add_missing(version_dir)
    slugs = [e["slug"] for e in json.loads((version_dir / "skills_index.json").read_text())]
    assert slugs == sorted(slugs) == ["aaa-leaf", "zzz-leaf"]
    assert si.missing_from_indexes(version_dir) == {}
    si.add_missing(version_dir)
    assert len(json.loads((version_dir / "skills_index.json").read_text())) == 2


def test_add_missing_preserves_the_files_own_indent(tmp_path):
    skills = {"a-leaf": leaf("a-leaf"), "b-leaf": leaf("b-leaf")}
    version_dir = collection(tmp_path, "genomics", skills, indexed=["a-leaf"])
    si.add_missing(version_dir)
    raw = (version_dir / "skills_index.json").read_text()
    assert raw.startswith("[\n {\n"), "skills_index.json is written with indent=1"
    assert not raw.endswith("\n"), "the generator writes no trailing newline"


def test_entry_is_derived_from_frontmatter(tmp_path):
    frontmatter = {"name": "n", "description": "d",
                   "metadata": {"license_tier": "open", "tools": ["T"], "techniques": ["LC-MS"],
                                "edam_operation": "op", "edam_topics": ["t1"], "repo_url": "https://example.org/r"},
                   "derived_from": [{"doi": "x/y"}, {"title": "no doi"}]}
    entry = si.entry_from_frontmatter("slug", frontmatter)
    assert entry == {"slug": "slug", "name": "n", "description": "d", "edam_operation": "op",
                     "edam_topics": ["t1"], "tools": ["T"], "dois": ["x/y"], "techniques": ["LC-MS"],
                     "license_tier": "open"}
    assert si.kb_entry_from_frontmatter(frontmatter)["repo_urls"] == ["https://example.org/r"]


# --- The canonical frontmatter parser -----------------------------------------

def test_a_rule_inside_frontmatter_does_not_truncate_it():
    """`raw.split('---', 2)` silently dropped skills whose frontmatter held `-----`."""
    text = "---\nname: s\nevidence:\n- '.mzML ----- toctree'\n---\nbody text\n"
    frontmatter, body = si.split_frontmatter(text)
    assert frontmatter["name"] == "s"
    assert frontmatter["evidence"] == [".mzML ----- toctree"]
    assert body.strip() == "body text"


def test_split_frontmatter_reports_malformed_input_as_none():
    assert si.split_frontmatter("no frontmatter here")[0] is None
    assert si.split_frontmatter("---\nunterminated: [\n---\nbody")[0] is None
    assert si.split_frontmatter("---\nname: s\nnever closed")[0] is None


def test_body_is_everything_after_the_closing_delimiter():
    _, body = si.split_frontmatter("---\nname: s\n---\nline one\n---\nline two\n")
    assert body == "line one\n---\nline two"
