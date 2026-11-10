"""scripts/sync_marketplace.py: registry-governed marketplace pins."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location("sync_marketplace", ROOT / "scripts" / "sync_marketplace.py")
sm = importlib.util.module_from_spec(spec)
sys.modules["sync_marketplace"] = sm
spec.loader.exec_module(sm)

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40


def registry(**overrides):
    prot = {"version": 1, "path": "collections/proteomics/v1", "tag": "proteomics-v1.0.0", "commit": SHA_B}
    prot.update(overrides)
    return {
        "schema": "asb-collections-manifest/1",
        "domains": {
            "metabolomics": {
                "repository": "Org/asb-skills-metabolomics",
                "releases": [
                    {"version": 3, "path": "collections/metabolomics/v3", "tag": "metabolomics-v3.0.0", "commit": SHA_A},
                    {"version": 2, "path": "collections/metabolomics/v2", "tag": None, "commit": SHA_A},
                    {"version": 1, "status": "legacy", "path": "collections/metabolomics/v1", "tag": None, "commit": SHA_C},
                ],
            },
            "proteomics": {"repository": "Org/asb-skills-proteomics", "releases": [prot]},
        },
    }


def entry(name, url, path, sha, version, description="Existing description."):
    return {
        "name": name,
        "source": {"source": "git-subdir", "url": url, "path": path, "ref": "main", "sha": sha},
        "description": description,
        "version": version,
        "author": {"name": "Holobiomics Lab", "url": "https://github.com/HolobiomicsLab"},
        "homepage": sm.REGISTRY_URL,
        "repository": sm.REGISTRY_URL,
        "license": "CC-BY-4.0",
        "keywords": ["metabolomics", "é"],
    }


def marketplace(with_proteomics=False, sha=SHA_A, version="3.0.0"):
    plugins = [
        entry("metabolomics", "Org/asb-skills-metabolomics", "collections/metabolomics/v3", sha, version),
        entry("metabolomics-nmr", "Org/asb-skills-metabolomics", "packs/metabolomics/nmr", SHA_C, "0.1.0"),
    ]
    if with_proteomics:
        plugins.append(entry("proteomics", "Org/asb-skills-proteomics", "collections/proteomics/v1", SHA_B, "1.0.0"))
    return {"name": "m", "description": "d", "owner": {"name": "o"}, "plugins": plugins}


@pytest.fixture
def files(tmp_path):
    def make(market, reg=None):
        m = tmp_path / "marketplace.json"
        r = tmp_path / "collections.yaml"
        m.write_text(sm.dump(market), encoding="utf-8")
        r.write_text(yaml.safe_dump(reg or registry(), sort_keys=False), encoding="utf-8")
        return ["--marketplace", str(m), "--manifest", str(r)], m, r

    return make


def test_check_passes_and_reports_missing_and_packs(files, capsys):
    args, _, _ = files(marketplace())
    assert sm.main(["--check", *args]) == 0
    out = capsys.readouterr().out
    assert "metabolomics: ok (3.0.0" in out
    assert "metabolomics-nmr: not governed" in out
    assert "proteomics: missing" in out


def test_default_mode_is_check(files):
    args, _, _ = files(marketplace())
    assert sm.main(args) == 0


def test_missing_entry_fails_only_with_require_all(files):
    args, _, _ = files(marketplace())
    assert sm.main(["--check", "--require-all", *args]) == 1


def test_sha_drift_fails(files, capsys):
    args, _, _ = files(marketplace(sha=SHA_C))
    assert sm.main(["--check", *args]) == 1
    assert "DISAGREES, sha" in capsys.readouterr().out


def test_version_drift_fails(files, capsys):
    args, _, _ = files(marketplace(version="3.0.1"))
    assert sm.main(["--check", *args]) == 1
    assert "version '3.0.1'" in capsys.readouterr().out


def test_pack_with_different_sha_never_fails(files):
    market = marketplace()
    market["plugins"][1]["source"]["sha"] = SHA_B
    market["plugins"][1]["version"] = "9.9.9"
    args, _, _ = files(market)
    assert sm.main(["--check", *args]) == 0


def test_older_release_path_is_not_governed(files, capsys):
    market = marketplace()
    market["plugins"].append(
        entry("old", "Org/asb-skills-metabolomics", "collections/metabolomics/v2", SHA_C, "0.0.1")
    )
    args, _, _ = files(market)
    assert sm.main(["--check", *args]) == 0
    assert "old: not governed" in capsys.readouterr().out


def test_release_without_tag_is_skipped(files, capsys):
    reg = registry(tag=None)
    args, _, _ = files(marketplace(), reg)
    assert sm.main(["--check", "--require-all", *args]) == 0
    assert "skipped" in capsys.readouterr().out


def test_unreadable_input_is_exit_2(tmp_path):
    assert sm.main(["--marketplace", str(tmp_path / "none.json"), "--manifest", str(tmp_path / "none.yaml")]) == 2


def test_bad_tag_prefix_is_exit_2(files):
    args, _, _ = files(marketplace(), registry(tag="other-v1.0.0"))
    assert sm.main(["--check", *args]) == 2


def test_write_adds_entry_with_description_option(files):
    args, m, _ = files(marketplace())
    assert sm.main(["--write", *args, "--description", "proteomics=ASB Proteomics: test."]) == 0
    data = json.loads(m.read_text(encoding="utf-8"))
    added = data["plugins"][-1]
    assert added == entry(
        "proteomics", "Org/asb-skills-proteomics", "collections/proteomics/v1", SHA_B, "1.0.0",
        "ASB Proteomics: test.",
    ) | {"keywords": ["proteomics", "agentic-science", "skills"]}
    assert sm.main(["--check", "--require-all", *args]) == 0


def test_write_reads_description_from_checkout(files, tmp_path):
    plugin = tmp_path / "co" / "collections" / "proteomics" / "v1" / ".claude-plugin"
    plugin.mkdir(parents=True)
    (plugin / "plugin.json").write_text(json.dumps({"description": "From plugin.json."}))
    args, m, _ = files(marketplace())
    assert sm.main(["--write", *args, "--checkout", f"proteomics={tmp_path / 'co'}"]) == 0
    assert json.loads(m.read_text())["plugins"][-1]["description"] == "From plugin.json."


def test_write_without_description_writes_nothing(files, capsys):
    market = marketplace(sha=SHA_C, version="2.0.0")
    args, m, _ = files(market)
    before = m.read_bytes()
    assert sm.main(["--write", *args]) == 2
    assert m.read_bytes() == before
    assert "proteomics: no description" in capsys.readouterr().err


def test_patch_release_moves_sha_and_version_and_keeps_description(files):
    reg = registry()
    reg["domains"]["metabolomics"]["releases"][0].update(tag="metabolomics-v3.0.1", commit=SHA_C)
    args, m, _ = files(marketplace(with_proteomics=True), reg)
    assert sm.main(["--write", *args]) == 0
    data = json.loads(m.read_text(encoding="utf-8"))
    main = data["plugins"][0]
    assert (main["source"]["sha"], main["version"]) == (SHA_C, "3.0.1")
    assert main["description"] == "Existing description."
    assert main["keywords"] == ["metabolomics", "é"]
    assert data["plugins"][1]["source"]["sha"] == SHA_C  # pack untouched (it already was SHA_C)
    assert data["plugins"][1]["version"] == "0.1.0"


def test_existing_only_moves_governed_entries_and_adds_none(files, capsys):
    reg = registry()
    reg["domains"]["metabolomics"]["releases"][0].update(tag="metabolomics-v3.0.1", commit=SHA_C)
    args, m, _ = files(marketplace(), reg)
    assert sm.main(["--write", "--existing-only", *args]) == 0
    data = json.loads(m.read_text(encoding="utf-8"))
    assert [p["name"] for p in data["plugins"]] == ["metabolomics", "metabolomics-nmr"]
    assert (data["plugins"][0]["source"]["sha"], data["plugins"][0]["version"]) == (SHA_C, "3.0.1")
    assert "proteomics: not added (--existing-only)" in capsys.readouterr().out
    assert sm.main(["--check", *args]) == 0
    assert sm.main(["--check", "--require-all", *args]) == 1


def test_existing_only_with_nothing_to_move_is_byte_identical(files):
    args, m, _ = files(marketplace())
    before = m.read_bytes()
    assert sm.main(["--write", "--existing-only", *args]) == 0
    assert m.read_bytes() == before


def test_noop_write_is_byte_identical_and_idempotent(files):
    args, m, _ = files(marketplace(with_proteomics=True))
    before = m.read_bytes()
    assert sm.main(["--write", *args]) == 0
    assert m.read_bytes() == before
    assert "é".encode() in before


def test_committed_files_agree():
    assert sm.main(["--check"]) == 0


def test_committed_marketplace_round_trips_byte_identically():
    path = ROOT / ".claude-plugin" / "marketplace.json"
    text = path.read_text(encoding="utf-8")
    assert sm.dump(json.loads(text)) == text
