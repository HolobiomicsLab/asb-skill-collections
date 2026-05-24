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
