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


# --- Release status and DOI placeholders -------------------------------------
#
# The catalogue listed three staged v1 collections with `doi: TODO-zenodo`, and
# the site rendered them as released with a link to doi.org/TODO-zenodo. A
# collection is released when the plugin marketplace serves it; every other
# catalogued collection is staged, and a DOI is published only once minted.

REPO = pathlib.Path(__file__).resolve().parent.parent


def _write_collection(root, slug, version, doi):
    import yaml
    col_dir = root / "collections" / slug / f"v{version}"
    col_dir.mkdir(parents=True)
    (col_dir / "collection.yaml").write_text(yaml.dump({
        "title": f"{slug} v{version}",
        "version": str(version),
        "slug": slug,
        "domain_topics": [],
        "doi": doi,
        "released_at": "2026-06-15T00:00:00Z",
        "lead_curators": [],
        "skills_count": 1,
        "tools_count": 1,
    }))


def _write_marketplace(root, sources):
    plugin_dir = root / ".claude-plugin"
    plugin_dir.mkdir()
    (plugin_dir / "marketplace.json").write_text(json.dumps({
        "name": "fixture",
        "plugins": [{"name": f"p{i}", "source": s} for i, s in enumerate(sources)],
    }))


def test_placeholder_doi_is_omitted(tmp_path):
    from scripts.regen_catalogue import build_catalogue
    _write_collection(tmp_path, "alpha", 1, "TODO-zenodo")
    entry = build_catalogue(tmp_path)["collections"][0]
    assert "doi" not in entry


def test_minted_doi_is_kept(tmp_path):
    from scripts.regen_catalogue import build_catalogue
    _write_collection(tmp_path, "alpha", 1, "10.5281/zenodo.20794027")
    entry = build_catalogue(tmp_path)["collections"][0]
    assert entry["doi"] == "10.5281/zenodo.20794027"


@pytest.mark.parametrize(
    "doi, minted",
    [
        ("10.5281/zenodo.20794027", True),
        ("https://doi.org/10.5281/zenodo.1", False),
        ("TODO-zenodo", False),
        ("", False),
        (None, False),
    ],
)
def test_is_minted_doi(doi, minted):
    from scripts.regen_catalogue import is_minted_doi
    assert is_minted_doi(doi) is minted


def test_status_follows_the_marketplace(tmp_path):
    from scripts.regen_catalogue import build_catalogue
    _write_collection(tmp_path, "alpha", 1, None)
    _write_collection(tmp_path, "alpha", 2, None)
    _write_collection(tmp_path, "beta", 1, None)
    _write_marketplace(tmp_path, ["./collections/alpha/v2", "./packs/alpha/lc-ms"])
    status = {
        f"{e['slug']}/v{e['version']}": e["status"]
        for e in build_catalogue(tmp_path)["collections"]
    }
    assert status == {"alpha/v1": "staged", "alpha/v2": "released", "beta/v1": "staged"}


def test_without_a_marketplace_every_collection_is_staged(tmp_path):
    from scripts.regen_catalogue import build_catalogue
    _write_collection(tmp_path, "alpha", 1, None)
    entry = build_catalogue(tmp_path)["collections"][0]
    assert entry["status"] == "staged"


def test_status_is_a_context_term(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    assert "status" in build_catalogue(tmp_repo)["@context"]


def test_committed_catalogue_matches_the_release_state():
    """The served catalogue carries no placeholder DOI and the marketplace's status."""
    from scripts.regen_catalogue import collection_status, is_minted_doi, released_collection_dirs
    entries = json.loads((REPO / "catalogue.jsonld").read_text(encoding="utf-8"))["collections"]
    released = released_collection_dirs(REPO)
    assert entries
    for entry in entries:
        rel = f"collections/{entry['slug']}/v{entry['version']}"
        assert entry.get("status") == collection_status(rel, released), rel
        if "doi" in entry:
            assert is_minted_doi(entry["doi"]), (rel, entry["doi"])
