"""Corpus tool-licence field migration contract."""

from __future__ import annotations

import pathlib
import textwrap

import yaml

from scripts import migrate_tool_license_field as migration


def _corpus(tmp_path: pathlib.Path) -> pathlib.Path:
    path = tmp_path / "corpus.yaml"
    path.write_text(textwrap.dedent("""
        papers:
        - name: tool
          repo_url: https://example.org/tool
          access: {type: repo-oa, license: MIT, verified_on: 2026-11-07}
          license_detection: license-file
          license_subject: tool
        - name: paper
          access: {type: open-access, license: CC-BY-4.0}
          license_detection: crossref-paper
          license_subject: paper
        - name: blank
          access: {type: link-only, license: null}
    """).lstrip(), encoding="utf-8")
    return path


def test_migration_moves_tool_and_leaves_paper_license(tmp_path):
    path = _corpus(tmp_path)
    summary, changed = migration.migrate(path, path)
    papers = yaml.safe_load(path.read_text())["papers"]
    assert changed and summary == {"moved": 1, "left": 2, "refused": 0, "changed": True}
    assert papers[0]["tool_license"] == {
        "spdx": "MIT",
        "detection": "license-file",
        "verified_on": __import__("datetime").date(2026, 11, 7),
        "source": "https://example.org/tool",
    }
    assert "license" not in papers[0]["access"]
    assert papers[1]["access"]["license"] == "CC-BY-4.0"
    assert all("license_subject" not in paper for paper in papers)


def test_migration_is_idempotent(tmp_path, capsys):
    path = _corpus(tmp_path)
    assert migration.main(["--corpus", str(path)]) == 0
    first = path.read_bytes()
    assert migration.main(["--corpus", str(path)]) == 0
    assert path.read_bytes() == first
    assert "No changes needed." in capsys.readouterr().out


def test_out_writes_a_copy_and_preserves_the_source(tmp_path):
    source = _corpus(tmp_path)
    output = tmp_path / "migrated.yaml"
    before = source.read_bytes()
    assert migration.main(["--corpus", str(source), "--out", str(output)]) == 0
    assert source.read_bytes() == before
    assert "license_subject" not in output.read_text()


def test_migration_refuses_an_unclassifiable_licence(tmp_path):
    path = tmp_path / "corpus.yaml"
    path.write_text("papers:\n- name: ambiguous\n  access: {license: MIT}\n")
    before = path.read_bytes()
    assert migration.main(["--corpus", str(path)]) == 2
    assert path.read_bytes() == before
