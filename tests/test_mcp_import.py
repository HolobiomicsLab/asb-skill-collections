"""The `mcp` extra installs an SDK the server can import, and says why when it cannot.

mcp 2.x renamed ``FastMCP`` to ``MCPServer``, so an unbounded ``mcp>=1.2`` extra
resolves to a release under which ``asb-mcp`` cannot start. The extra therefore
carries an upper bound, and the import guard reports the exception it met
rather than claiming the package is missing.
"""

from __future__ import annotations

import importlib.metadata
import os
import pathlib
import subprocess
import sys
import tomllib

import pytest
from packaging.requirements import Requirement

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SERVER = "asb_skill_collections.asb_mcp_server"


def _mcp_requirement() -> Requirement:
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    (line,) = pyproject["project"]["optional-dependencies"]["mcp"]
    requirement = Requirement(line)
    assert requirement.name == "mcp"
    return requirement


def test_the_mcp_extra_excludes_mcp_2():
    specifier = _mcp_requirement().specifier

    assert not specifier.contains("2.0.0")
    assert not specifier.contains("2.3.0")
    assert specifier.contains("1.2.0")


def test_the_server_imports_under_an_mcp_the_extra_allows():
    pytest.importorskip("mcp", reason="the MCP server needs the 'mcp' extra")
    installed = importlib.metadata.version("mcp")
    if not _mcp_requirement().specifier.contains(installed):
        pytest.skip(f"installed mcp {installed} is outside the extra's range")
    sys.path.insert(0, str(REPO_ROOT))
    sys.modules.pop(SERVER, None)

    server = __import__(SERVER, fromlist=["mcp"])

    assert type(server.mcp).__name__ == "FastMCP"
    assert callable(server.main)


def _import_server(tmp_path, *python_flags):
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(tmp_path), str(REPO_ROOT)])}
    return subprocess.run(
        [sys.executable, *python_flags, "-c", f"import {SERVER}"],
        capture_output=True, text=True, cwd=tmp_path, env=env, timeout=120,
    )


def test_an_mcp_without_fastmcp_is_reported_with_its_error_and_the_pin(tmp_path):
    """A stub ``mcp`` package shaped like 2.x: ``mcp.server`` exists, ``fastmcp`` does not."""
    (tmp_path / "mcp" / "server").mkdir(parents=True)
    (tmp_path / "mcp" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "mcp" / "server" / "__init__.py").write_text("", encoding="utf-8")

    result = _import_server(tmp_path)

    assert result.returncode == 1
    assert "No module named 'mcp.server.fastmcp'" in result.stderr
    assert "mcp<2" in result.stderr
    assert "uvx" not in result.stderr
    assert "Traceback" not in result.stderr


def test_a_missing_mcp_is_reported_with_its_error_and_the_install_command(tmp_path):
    """``-S`` leaves site-packages off the path, so no ``mcp`` can be found."""
    result = _import_server(tmp_path, "-S")

    assert result.returncode == 1
    assert "No module named 'mcp'" in result.stderr
    assert "[mcp]" in result.stderr
    assert "uvx" not in result.stderr
    assert "Traceback" not in result.stderr
