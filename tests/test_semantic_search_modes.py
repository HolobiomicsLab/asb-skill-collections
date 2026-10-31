"""`--mode semantic` fails loudly; `--mode auto` falls back and says why.

bin/semantic_search.py used to answer `--mode semantic` with a keyword search
and exit 0 whenever numpy, the leaf embedding cache or the API key was missing,
so a caller who asked for semantic ranking could not tell that none ran (issue
#63). It now exits 2 with a one-line reason in that case; `--mode auto` keeps
the keyword fallback and writes the reason to stderr.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
COLLECTION = ROOT / "collections" / "metabolomics" / "v2"
SCRIPT = COLLECTION / "bin" / "semantic_search.py"
QUERY = ["--collection", str(COLLECTION), "--query", "untargeted annotation", "--k", "3"]


@pytest.fixture
def module(monkeypatch):
    monkeypatch.delenv("ASB_LEAF_EMB_CACHE", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "placeholder-not-used")
    spec = importlib.util.spec_from_file_location("collection_semantic_modes", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


@pytest.fixture
def without_numpy(monkeypatch):
    """Make `import numpy` raise ImportError, as on a machine without it."""
    monkeypatch.setitem(sys.modules, "numpy", None)


@pytest.fixture
def numpy_present(monkeypatch):
    """A stand-in numpy: the cache check runs before numpy is used."""
    monkeypatch.setitem(sys.modules, "numpy", types.ModuleType("numpy"))


def test_semantic_mode_without_numpy_exits_2_with_a_reason(module, without_numpy, capsys):
    assert module.main([*QUERY, "--mode", "semantic"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    [line] = captured.err.splitlines()
    assert "--mode semantic cannot run" in line and "numpy is not installed" in line


def test_auto_mode_without_numpy_falls_back_with_a_note(module, without_numpy, capsys):
    assert module.main([*QUERY, "--mode", "auto"]) == 0

    captured = capsys.readouterr()
    assert json.loads(captured.out)["mode"] == "keyword"
    [line] = captured.err.splitlines()
    assert "numpy is not installed" in line and "falling back" in line


def test_semantic_mode_without_a_cache_exits_2_with_a_reason(
    module, numpy_present, monkeypatch, capsys
):
    monkeypatch.setattr(module, "_cache_for", lambda collection: None)

    assert module.main([*QUERY, "--mode", "semantic"]) == 2

    assert "no leaf embedding cache" in capsys.readouterr().err


def test_auto_mode_without_a_cache_falls_back_with_a_note(
    module, numpy_present, monkeypatch, capsys
):
    monkeypatch.setattr(module, "_cache_for", lambda collection: None)

    assert module.main([*QUERY, "--mode", "auto"]) == 0

    captured = capsys.readouterr()
    assert json.loads(captured.out)["mode"] == "keyword"
    assert "no leaf embedding cache" in captured.err


def test_keyword_mode_says_nothing_on_stderr(module, capsys):
    assert module.main([*QUERY, "--mode", "keyword"]) == 0

    assert capsys.readouterr().err == ""


def test_the_cli_exit_status_is_the_return_value(tmp_path):
    env = {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *QUERY, "--mode", "semantic"],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=120,
    )

    assert result.returncode == 2, result.stdout + result.stderr
    assert result.stdout == ""
    assert "--mode semantic cannot run" in result.stderr
