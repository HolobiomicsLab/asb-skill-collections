import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import stamp_provenance as P
from scripts.provenance_tier import DEFAULT


def _skill(tmp, slug, body="# t\n\nuse it.\n", meta=None, null_meta=False):
    d = tmp / "skills" / slug
    d.mkdir(parents=True)
    if null_meta:
        (d / "SKILL.md").write_text(
            "---\nname: " + slug + "\nmetadata:\n---\n" + body, encoding="utf-8"
        )
    else:
        fm = {"name": slug, "license": "CC-BY-4.0", "metadata": (meta or {})}
        (d / "SKILL.md").write_text(
            "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body,
            encoding="utf-8",
        )
    return d / "SKILL.md"


def _collection(tmp):
    """One skill with metadata:, one without; matching skills_index + kb_bundle."""
    _skill(tmp, "with-meta", meta={"license_tier": "restricted"})
    _skill(tmp, "null-meta", null_meta=True)
    si = [
        {"slug": "with-meta", "dois": ["10.1/a"], "license_tier": "restricted"},
        {"slug": "null-meta", "dois": ["10.2/b"], "license_tier": "open"},
    ]
    kb = {
        "collection": "x",
        "skills": {
            "with-meta": {"dois": ["10.1/a"]},
            "null-meta": {"dois": ["10.2/b"]},
        },
    }
    (tmp / "skills_index.json").write_text(json.dumps(si, indent=2), encoding="utf-8")
    (tmp / "kb_bundle.json").write_text(json.dumps(kb, indent=2), encoding="utf-8")
    return tmp


# --- propagate_indices -------------------------------------------------------

def test_propagate_sets_default_on_entries_with_dois(tmp_path):
    _collection(tmp_path)
    summary = P.propagate_indices(
        tmp_path / "skills_index.json", tmp_path / "kb_bundle.json"
    )
    assert summary == {DEFAULT: 2}
    si = json.loads((tmp_path / "skills_index.json").read_text())
    assert all(e["provenance_tier"] == DEFAULT for e in si)
    kb = json.loads((tmp_path / "kb_bundle.json").read_text())
    assert all(r["provenance_tier"] == DEFAULT for r in kb["skills"].values())


def test_propagate_skips_entries_without_dois(tmp_path):
    si = [{"slug": "a", "dois": ["10.1/a"]}, {"slug": "b", "dois": []}, {"slug": "c"}]
    kb = {"skills": {"a": {"dois": ["10.1/a"]}, "b": {"dois": []}, "c": {}}}
    (tmp_path / "skills_index.json").write_text(json.dumps(si, indent=2), encoding="utf-8")
    (tmp_path / "kb_bundle.json").write_text(json.dumps(kb, indent=2), encoding="utf-8")
    summary = P.propagate_indices(
        tmp_path / "skills_index.json", tmp_path / "kb_bundle.json"
    )
    assert summary == {DEFAULT: 1}
    si2 = json.loads((tmp_path / "skills_index.json").read_text())
    assert si2[0]["provenance_tier"] == DEFAULT
    assert "provenance_tier" not in si2[1]
    assert "provenance_tier" not in si2[2]


def test_propagate_is_idempotent(tmp_path):
    _collection(tmp_path)
    P.propagate_indices(tmp_path / "skills_index.json", tmp_path / "kb_bundle.json")
    first_si = (tmp_path / "skills_index.json").read_text()
    first_kb = (tmp_path / "kb_bundle.json").read_text()
    P.propagate_indices(tmp_path / "skills_index.json", tmp_path / "kb_bundle.json")
    assert (tmp_path / "skills_index.json").read_text() == first_si
    assert (tmp_path / "kb_bundle.json").read_text() == first_kb


# --- stamp_skill_provenance --------------------------------------------------

def test_stamp_sets_field_no_banner(tmp_path):
    md = _skill(tmp_path, "s", meta={"license_tier": "open"})
    assert P.stamp_skill_provenance(md, "literature") is True
    text = md.read_text()
    fm = yaml.safe_load(text.split("---\n", 2)[1])
    assert fm["metadata"]["provenance_tier"] == "literature"
    assert fm["metadata"]["license_tier"] == "open"  # preserved
    assert "asb-license-banner" not in text  # no banner added by us


def test_stamp_handles_null_metadata(tmp_path):
    md = _skill(tmp_path, "s-null", null_meta=True)
    assert P.stamp_skill_provenance(md, "literature") is True
    fm = yaml.safe_load(md.read_text().split("---\n", 2)[1])
    assert fm["metadata"]["provenance_tier"] == "literature"


def test_stamp_is_idempotent(tmp_path):
    md = _skill(tmp_path, "s2", meta={"license_tier": "open"})
    P.stamp_skill_provenance(md, "literature")
    first = md.read_text()
    assert P.stamp_skill_provenance(md, "literature") is False
    assert md.read_text() == first


def test_stamp_no_frontmatter_returns_false(tmp_path):
    d = tmp_path / "skills" / "raw"
    d.mkdir(parents=True)
    md = d / "SKILL.md"
    md.write_text("# no frontmatter\n", encoding="utf-8")
    assert P.stamp_skill_provenance(md, "literature") is False


# --- stamp_all + main --------------------------------------------------------

def test_stamp_all_uses_index_tier(tmp_path):
    _collection(tmp_path)
    P.propagate_indices(tmp_path / "skills_index.json", tmp_path / "kb_bundle.json")
    res = P.stamp_all(str(tmp_path / "skills"), str(tmp_path / "skills_index.json"))
    assert res["changed"] == 2
    assert res["tiers"] == {DEFAULT: 2}
    for slug in ("with-meta", "null-meta"):
        fm = yaml.safe_load(
            (tmp_path / "skills" / slug / "SKILL.md").read_text().split("---\n", 2)[1]
        )
        assert fm["metadata"]["provenance_tier"] == DEFAULT
    # second pass: nothing changes
    res2 = P.stamp_all(str(tmp_path / "skills"), str(tmp_path / "skills_index.json"))
    assert res2["changed"] == 0


def test_main_runs_on_collection(tmp_path):
    _collection(tmp_path)
    rc = P.main(["--collection", str(tmp_path)])
    assert rc == 0
    si = json.loads((tmp_path / "skills_index.json").read_text())
    assert all(e["provenance_tier"] == DEFAULT for e in si)
    for slug in ("with-meta", "null-meta"):
        fm = yaml.safe_load(
            (tmp_path / "skills" / slug / "SKILL.md").read_text().split("---\n", 2)[1]
        )
        assert fm["metadata"]["provenance_tier"] == DEFAULT
