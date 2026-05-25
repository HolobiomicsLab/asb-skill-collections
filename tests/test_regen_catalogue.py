"""Unit tests for regen_catalogue.py."""
import json
import pathlib
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"
MINI_COLLECTION_DIR = FIXTURES / "mini_collection"


@pytest.fixture()
def tmp_repo(tmp_path):
    """A minimal fake repo root with one collection."""
    collections_dir = tmp_path / "collections" / "test-domain" / "v1"
    collections_dir.mkdir(parents=True)
    # Copy mini collection YAML
    import shutil
    shutil.copy(MINI_COLLECTION_DIR / "collection.yaml", collections_dir / "collection.yaml")
    return tmp_path


def test_catalogue_has_context(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    cat = build_catalogue(tmp_repo)
    assert "@context" in cat
    assert "@type" in cat
    assert cat["@type"] == "asb:SkillCollectionRegistry"


def test_catalogue_lists_collection(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    cat = build_catalogue(tmp_repo)
    assert "collections" in cat
    assert len(cat["collections"]) == 1
    entry = cat["collections"][0]
    assert entry["title"] == "Test Domain Collection"


def test_catalogue_has_required_fields(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    cat = build_catalogue(tmp_repo)
    entry = cat["collections"][0]
    required = ["@id", "title", "version", "slug", "skills_count", "tools_count"]
    for field in required:
        assert field in entry, f"Missing field: {field}"


def test_catalogue_is_alphabetically_ordered(tmp_path):
    """Multiple collections should be sorted alphabetically by slug."""
    from scripts.regen_catalogue import build_catalogue
    import yaml
    for slug in ["zebra-domain", "alpha-domain", "metabolomics"]:
        col_dir = tmp_path / "collections" / slug / "v1"
        col_dir.mkdir(parents=True)
        (col_dir / "collection.yaml").write_text(yaml.dump({
            "@type": "asb:SkillCollection",
            "@id": f"https://w3id.org/holobiomicslab/asb-skill/collection/{slug}/v1",
            "title": f"{slug.title()} Collection",
            "version": "1",
            "slug": slug,
            "domain_topics": [],
            "doi": None,
            "released_at": None,
            "lead_curators": [],
            "skills_count": 0,
            "tools_count": 0,
        }))
    cat = build_catalogue(tmp_path)
    slugs = [e["slug"] for e in cat["collections"]]
    assert slugs == sorted(slugs)


def test_catalogue_generated_at_is_iso(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    import re
    cat = build_catalogue(tmp_repo)
    ts = cat.get("generated_at", "")
    # ISO 8601 UTC: 2026-05-25T00:00:00Z
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ts), f"Bad timestamp: {ts}"


def test_catalogue_write_to_file(tmp_repo, tmp_path):
    from scripts.regen_catalogue import build_catalogue, write_catalogue
    cat = build_catalogue(tmp_repo)
    out = tmp_path / "catalogue.jsonld"
    write_catalogue(cat, out)
    reloaded = json.loads(out.read_text())
    assert reloaded["@type"] == "asb:SkillCollectionRegistry"
