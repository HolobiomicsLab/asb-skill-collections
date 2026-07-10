"""Schema conformance tests for .claude-plugin/marketplace.json."""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent


def test_marketplace_json_parseable():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert "schema_version" in data
    assert "plugins" in data
    assert isinstance(data["plugins"], list)


def test_marketplace_json_has_publisher():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert "publisher" in data
    assert "name" in data["publisher"]


def _plugin_sources():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    for p in data["plugins"]:
        src = p.get("source") or p.get("path")
        yield p["name"], (src or "").lstrip("./")


def test_every_marketplace_plugin_exists_on_disk():
    """No phantom plugins: each listed source must carry a real plugin.json.

    Guards the README scope claim from the other direction too -- a domain can only
    be advertised as shipping if its plugin actually exists.
    """
    missing = [
        name
        for name, src in _plugin_sources()
        if not (ROOT / src / ".claude-plugin" / "plugin.json").is_file()
    ]
    assert not missing, f"marketplace lists plugins with no plugin.json on disk: {missing}"


def test_readme_does_not_overclaim_unshipped_domain_plugins():
    """The README must not present unshipped domains as shipping plugins.

    v0 is metabolomics-only (CLAUDE.md). Every domain the marketplace ships is
    metabolomics; the README must not state, in the present tense, that every domain
    ships a plugin -- proteomics/transcriptomics/epigenomics are staged/internal.
    """
    shipped_domains = {
        src.split("/")[1]
        for _, src in _plugin_sources()
        if src.startswith(("collections/", "packs/")) and len(src.split("/")) > 1
    }
    assert shipped_domains == {"metabolomics"}, (
        f"marketplace ships domains beyond metabolomics {shipped_domains}; "
        "update the README scope claim and this test together"
    )
    readme = (ROOT / "README.md").read_text()
    assert "Each domain ships a full plugin" not in readme, (
        "README carries the retired over-claim 'Each domain ships a full plugin'; "
        "v0 ships metabolomics only"
    )
