"""The same tool entity carries one licence across collections."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_tool_licence_consistency as c


def _col(tmp_path, name, entries):
    d = tmp_path / name
    d.mkdir()
    (d / "tools_index.json").write_text(json.dumps(
        [{"slug": s, "name": e.pop("name", s)} for s, e in entries.items()]))
    (d / "tool_licenses.json").write_text(json.dumps(entries))
    return d


def ev(address, licence="MIT", tier="open", **extra):
    return {"license": licence, "license_tier": tier, "license_evidence": address,
            "route": "registry:bioconda", "matched": "x", **extra}


def test_one_entity_one_licence_passes(tmp_path):
    a = _col(tmp_path, "a", {"bwa": ev("https://anaconda.org/bioconda/bwa")})
    b = _col(tmp_path, "b", {"bwa": ev("https://anaconda.org/bioconda/bwa")})
    assert c.check([a, b]) == ([], [])
    assert c.main([str(a), str(b)]) == 0


def test_one_entity_two_licences_fails(tmp_path):
    a = _col(tmp_path, "a", {"bwa": ev("https://anaconda.org/bioconda/bwa", "MIT")})
    b = _col(tmp_path, "b", {"bwa": ev("https://anaconda.org/bioconda/bwa", "GPL-3.0-only")})
    violations, _ = c.check([a, b])
    assert len(violations) == 1 and "bioconda/bwa" in violations[0]
    assert c.main([str(a), str(b)]) == 1


def test_one_name_two_entities_is_reported_not_failed(tmp_path):
    a = _col(tmp_path, "a", {"umap": ev("https://github.com/lmcinnes/umap", name="UMAP")})
    b = _col(tmp_path, "b", {"umap": ev("https://anaconda.org/bioconda/umap", "GPL-3.0-only",
                                        name="Umap")})
    violations, notes = c.check([a, b])
    assert violations == [] and len(notes) == 1 and "'umap'" in notes[0]


def test_unknown_entries_are_ignored(tmp_path):
    a = _col(tmp_path, "a", {"x": {"license": None, "license_tier": "unknown",
                                   "route": "reviewed", "matched": "x"}})
    assert c.check([a]) == ([], [])
