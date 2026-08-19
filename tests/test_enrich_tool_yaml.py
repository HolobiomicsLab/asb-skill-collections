import pathlib
import sys
import textwrap

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import enrich_tool_yaml as e


# ---------------------------------------------------------------------------
# tier_map
# ---------------------------------------------------------------------------

def test_tier_map_extracts_license_fields():
    tools_index = [
        {"slug": "t_open", "license_tier": "open", "license": "MIT",
         "license_detection": "github-api"},
        {"slug": "t_nc", "license_tier": "noncommercial", "license": "CC-BY-NC-4.0",
         "license_detection": "readme-llm"},
        {"slug": "t_restricted", "license_tier": "restricted", "license": None,
         "license_detection": "none"},
    ]
    m = e.tier_map(tools_index)
    assert m["t_open"] == {"license_tier": "open", "license": "MIT",
                           "license_detection": "github-api"}
    assert m["t_nc"]["license_tier"] == "noncommercial"
    assert m["t_restricted"]["license"] is None
    assert m["t_restricted"]["license_detection"] == "none"


def test_tier_map_defaults_missing_fields():
    # A tools_index entry that only carries the tier still yields a complete row.
    m = e.tier_map([{"slug": "t1", "license_tier": "open"}])
    assert m["t1"] == {"license_tier": "open", "license": None,
                       "license_detection": None}


# ---------------------------------------------------------------------------
# enrich — fixture with two tool YAMLs
# ---------------------------------------------------------------------------

def _write_collection(tmp_path):
    d = tmp_path
    tools = d / "tools"
    tools.mkdir()
    # tool A: a "generated" style record ending in schema_version, with a
    # later-appended techniques block (matches the real committed shape).
    (tools / "tool-a.yaml").write_text(textwrap.dedent("""\
        name: ToolA
        slug: tool-a
        canonical_url: https://github.com/x/tool-a
        version_used: '1.0'
        evidence_spans:
        - tool-a is used here
        derived_from:
        - doi: 10.1/open
          title: A paper
        source_repos:
        - x/tool-a
        schema_version: 0.2.0
        techniques:
        - LC-MS
        """))
    # tool B: minimal record, no canonical_url, no techniques.
    (tools / "tool-b.yaml").write_text(textwrap.dedent("""\
        name: ToolB
        slug: tool-b
        evidence_spans:
        - tool-b is used here
        derived_from:
        - doi: 10.1/restricted
          title: Another paper
        schema_version: 0.2.0
        """))
    tools_index = [
        {"slug": "tool-a", "license_tier": "open", "license": "MIT",
         "license_detection": "github-api"},
        {"slug": "tool-b", "license_tier": "restricted", "license": None,
         "license_detection": "none"},
    ]
    import json
    (d / "tools_index.json").write_text(json.dumps(tools_index, indent=2))
    return d


def test_enrich_writes_license_fields(tmp_path):
    d = _write_collection(tmp_path)
    summary = e.enrich(str(d))
    a = yaml.safe_load((d / "tools" / "tool-a.yaml").read_text())
    b = yaml.safe_load((d / "tools" / "tool-b.yaml").read_text())
    assert a["license_tier"] == "open"
    assert a["license"] == "MIT"
    assert a["license_detection"] == "github-api"
    assert b["license_tier"] == "restricted"
    assert b["license"] is None
    assert b["license_detection"] == "none"
    # untouched fields survive
    assert a["techniques"] == ["LC-MS"]
    assert a["canonical_url"] == "https://github.com/x/tool-a"
    assert summary["enriched"] == 2


def test_enrich_key_placement_after_schema_version(tmp_path):
    # License fields land right after schema_version, before techniques —
    # deterministic so re-runs are stable.
    d = _write_collection(tmp_path)
    e.enrich(str(d))
    keys = list(yaml.safe_load((d / "tools" / "tool-a.yaml").read_text()).keys())
    sv = keys.index("schema_version")
    assert keys[sv + 1:sv + 4] == ["license_tier", "license", "license_detection"]
    assert keys.index("techniques") > keys.index("license_detection")


def test_enrich_idempotent(tmp_path):
    d = _write_collection(tmp_path)
    e.enrich(str(d))
    first_a = (d / "tools" / "tool-a.yaml").read_text()
    first_b = (d / "tools" / "tool-b.yaml").read_text()
    e.enrich(str(d))
    assert (d / "tools" / "tool-a.yaml").read_text() == first_a
    assert (d / "tools" / "tool-b.yaml").read_text() == first_b


def test_enrich_updates_stale_tier(tmp_path):
    # If a YAML already carries a (now-stale) tier, enrich corrects it to match
    # the tools_index source of truth.
    d = _write_collection(tmp_path)
    e.enrich(str(d))
    import json
    ti = json.loads((d / "tools_index.json").read_text())
    for t in ti:
        if t["slug"] == "tool-a":
            t["license_tier"] = "noncommercial"
            t["license"] = "CC-BY-NC-4.0"
    (d / "tools_index.json").write_text(json.dumps(ti, indent=2))
    e.enrich(str(d))
    a = yaml.safe_load((d / "tools" / "tool-a.yaml").read_text())
    assert a["license_tier"] == "noncommercial"
    assert a["license"] == "CC-BY-NC-4.0"


def test_enrich_skips_yaml_without_index_entry(tmp_path):
    # A tools/<slug>.yaml with no tools_index row is left untouched.
    d = _write_collection(tmp_path)
    orphan = (d / "tools" / "orphan.yaml")
    orphan.write_text("name: Orphan\nslug: orphan\nschema_version: 0.2.0\n")
    before = orphan.read_text()
    summary = e.enrich(str(d))
    assert orphan.read_text() == before
    assert summary["skipped"] == 1
