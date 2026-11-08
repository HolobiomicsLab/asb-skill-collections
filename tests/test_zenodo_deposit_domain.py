"""Deposits from domain repositories resolve tooling separately."""

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from scripts import zenodo_deposit
from tests.test_zenodo_deposit import DATE, ZENODO_JSON, FakeZenodo, make_repo


TOOLING_FILES = (
    "scripts/perspicacite_kb_bind.py",
    "scripts/requirements.txt",
    "AGENTS.md",
    "governance/LICENSE_TIERS.md",
)


def make_domain_repo(root: Path) -> Path:
    collection = root / "collections" / "dom" / "v1"
    collection.mkdir(parents=True)
    (collection / ".zenodo.json").write_text(json.dumps(ZENODO_JSON))
    (collection / "collection.yaml").write_text("name: dom\n")
    (root / "LICENSING.md").write_text("domain licensing\n")
    (root / "LICENSE").write_text("domain license\n")
    return root


def make_tooling_root(root: Path) -> Path:
    for relative in TOOLING_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"tooling {relative}\n")
    (root / "scripts" / "release_creators.yaml").write_text(
        "creators:\n- family: Doe\n  given: Jane\n  orcid: 0000-0000-0000-0000\n"
    )
    return root


@pytest.fixture
def domain_repo(tmp_path):
    return make_domain_repo(tmp_path / "domain")


@pytest.fixture
def tooling_root(tmp_path):
    return make_tooling_root(tmp_path / "tooling")


def test_domain_archive_and_plan_use_the_tooling_root(domain_repo, tooling_root, tmp_path, capsys):
    built = zenodo_deposit.build_archive(
        domain_repo, "dom", "v1", tmp_path / "out", tooling_root=tooling_root
    )
    with zipfile.ZipFile(built.path) as archive:
        for relative in TOOLING_FILES:
            assert archive.read(f"dom/v1/{relative}") == (tooling_root / relative).read_bytes()
        for relative in ("LICENSING.md", "LICENSE"):
            assert archive.read(f"dom/v1/{relative}") == (domain_repo / relative).read_bytes()
    code = zenodo_deposit.main([
        "plan", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(tooling_root), "--publication-date", DATE,
    ])
    out = capsys.readouterr().out
    assert code == 0
    assert f"repository root: {domain_repo}" in out
    assert f"tooling root: {tooling_root}" in out


def test_domain_archive_without_tooling_names_both_roots(domain_repo, capsys):
    code = zenodo_deposit.main([
        "archive", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(domain_repo / "absent-tooling"),
    ])
    err = capsys.readouterr().err
    assert code == 1
    assert "license text not found: governance/LICENSE_TIERS.md" in err
    assert str(domain_repo) in err
    assert str(domain_repo / "absent-tooling") in err


def test_domain_plan_without_creators_names_both_roots(domain_repo, capsys):
    absent = domain_repo / "absent-tooling"
    code = zenodo_deposit.main([
        "plan", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(absent), "--publication-date", DATE,
    ])
    err = capsys.readouterr().err
    assert code == 1
    assert "scripts/release_creators.yaml not found under" in err
    assert str(domain_repo) in err
    assert str(absent) in err


def test_master_archive_is_byte_identical_with_an_empty_tooling_root(tmp_path):
    repo = make_repo(tmp_path / "repo")
    baseline = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "one")
    with_tooling = zenodo_deposit.build_archive(
        repo, "dom", "v1", tmp_path / "two", tooling_root=tmp_path / "empty"
    )
    assert baseline.sha256 == with_tooling.sha256


def test_repository_files_win_over_tooling_files(tmp_path):
    repo = make_repo(tmp_path / "repo")
    tooling = make_tooling_root(tmp_path / "tooling")
    built = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "out", tooling)
    with zipfile.ZipFile(built.path) as archive:
        for relative in TOOLING_FILES:
            assert archive.read(f"dom/v1/{relative}") == (repo / relative).read_bytes()


def test_licensing_fallback_is_noticed_in_the_plan(domain_repo, tooling_root, capsys):
    (domain_repo / "LICENSING.md").unlink()
    (tooling_root / "LICENSING.md").write_text("tooling licensing\n")
    code = zenodo_deposit.main([
        "plan", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(tooling_root), "--publication-date", DATE,
    ])
    out = capsys.readouterr().out
    assert code == 0
    assert "LICENSING.md supplied by tooling root; release text may differ" in out
    assert "source: LICENSING.md  tooling root" in out


def test_plan_lists_extra_files_with_size_and_sha256(domain_repo, tooling_root, tmp_path, capsys):
    extras = [tmp_path / "first cache.bin", tmp_path / "second.bin"]
    for index, path in enumerate(extras):
        path.write_bytes(bytes([index + 1]) * (index + 3))
    argv = [
        "plan", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(tooling_root), "--publication-date", DATE,
    ]
    for extra in extras:
        argv += ["--extra-file", str(extra)]
    assert zenodo_deposit.main(argv) == 0
    out = capsys.readouterr().out
    for extra in extras:
        digest = hashlib.sha256(extra.read_bytes()).hexdigest()
        assert f"  {extra.name}  {extra.stat().st_size} bytes  sha256 {digest}" in out


def test_draft_uploads_extra_files_after_the_archive_in_order(
        domain_repo, tooling_root, tmp_path, monkeypatch, capsys):
    extras = [tmp_path / "first cache.bin", tmp_path / "second.bin"]
    for index, path in enumerate(extras):
        path.write_bytes(f"extra {index}\n".encode())
    fake = FakeZenodo(zenodo_deposit.ZENODO_URL)
    monkeypatch.setattr(zenodo_deposit, "_request", fake)
    monkeypatch.setenv("ZENODO_TOKEN", "tok-test-only")
    argv = [
        "draft", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(tooling_root), "--out-dir", str(tmp_path / "out"),
        "--publication-date", DATE,
    ]
    for extra in extras:
        argv += ["--extra-file", str(extra)]
    assert zenodo_deposit.main(argv) == 0
    assert fake.steps()[4:7] == [
        ("PUT", "/api/files/bkt/dom-v1.zip"),
        ("PUT", "/api/files/bkt/first%20cache.bin"),
        ("PUT", "/api/files/bkt/second.bin"),
    ]
    out = capsys.readouterr().out
    for extra in extras:
        digest = hashlib.sha256(extra.read_bytes()).hexdigest()
        assert f"uploaded {extra.name} sha256 {digest}" in out


def test_missing_extra_file_stops_before_any_request(
        domain_repo, tooling_root, tmp_path, monkeypatch, capsys):
    fake = FakeZenodo(zenodo_deposit.ZENODO_URL)
    monkeypatch.setattr(zenodo_deposit, "_request", fake)
    monkeypatch.setenv("ZENODO_TOKEN", "tok-test-only")
    code = zenodo_deposit.main([
        "draft", "dom", "v1", "--repo-root", str(domain_repo),
        "--tooling-root", str(tooling_root), "--out-dir", str(tmp_path / "out"),
        "--publication-date", DATE, "--extra-file", str(tmp_path / "missing.bin"),
    ])
    assert code == 1
    assert fake.calls == []
    assert "extra file not found:" in capsys.readouterr().err


def test_default_tooling_root_is_the_script_repository(domain_repo, capsys):
    default_root = Path(zenodo_deposit.__file__).resolve().parents[1]
    template = domain_repo / "collections" / "dom" / "v1" / ".zenodo.json"
    metadata = json.loads(template.read_text())
    metadata["creators"] = zenodo_deposit.expected_creators(default_root)
    template.write_text(json.dumps(metadata))
    code = zenodo_deposit.main([
        "plan", "dom", "v1", "--repo-root", str(domain_repo), "--publication-date", DATE,
    ])
    out = capsys.readouterr().out
    assert code == 0
    assert f"tooling root: {default_root}" in out
    assert "source: scripts/release_creators.yaml  tooling root" in out


def test_archive_rejects_extra_file_option():
    with pytest.raises(SystemExit):
        zenodo_deposit._parser().parse_args([
            "archive", "dom", "v1", "--extra-file", "cache.npz",
        ])
