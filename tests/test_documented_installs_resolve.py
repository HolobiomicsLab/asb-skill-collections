"""Copy-paste install commands in the docs must resolve to something real.

The distribution is deliberately unpublished for v0 (design decision 5: the CLI
without the corpus it reads is not a working install), yet the README shipped
``pip install asb-skill-collections`` in a bash fence — the project's own front
page handing readers a command that 404s.

The check looks *only inside fenced code blocks*, because that is what a reader
copies. Prose that names the command in order to explain why it does not work is
fine, and the README relies on that distinction.

``docs/RELEASING_PYPI.md`` is exempt: it is the v1 publish procedure, whose
post-publish verification steps are index installs by definition, and it opens
with a banner saying it is dormant.
"""

from __future__ import annotations

import pathlib
import re
import tomllib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
RELEASE_PROCEDURE = "docs/RELEASING_PYPI.md"

FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.MULTILINE | re.DOTALL)
INSTALLERS = ("pip install", "pip3 install", "pipx install", "uv pip install",
              "uv tool install", "uvx --from")


def distribution_name() -> str:
    """The one canonical name; never retype it in a pattern."""
    with (REPO / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["name"]


def index_installs(markdown: str, dist: str) -> list[str]:
    """Fenced commands that install ``dist`` from a package index.

    A local or VCS install names a path or a URL right after the distribution
    (``-e .``, ``dist @ git+https://…``), so it is not an index install and is
    not reported. Extras are part of the requirement, hence the optional group.
    """
    requirement = re.compile(re.escape(dist) + r"(?:\[[a-z0-9,_-]+\])?")
    invoked = re.compile(
        rf"""(?:{"|".join(re.escape(i) for i in INSTALLERS)})\s+(["'][^"']+["']|\S+)"""
    )
    hits: list[str] = []
    for block in FENCE.findall(markdown):
        for line in block.splitlines():
            spec = invoked.search(line)
            if spec and requirement.fullmatch(spec.group(1).strip("\"'")):
                hits.append(line.strip())
    return hits


def _docs() -> list[str]:
    """Every markdown file a reader might copy from, bar the v1 procedure."""
    paths = [p.relative_to(REPO).as_posix()
             for p in [REPO / "README.md", *sorted((REPO / "docs").rglob("*.md"))]]
    return [p for p in paths if p != RELEASE_PROCEDURE]


@pytest.mark.parametrize("rel", _docs())
def test_a_doc_never_tells_a_reader_to_install_from_an_index(rel):
    hits = index_installs((REPO / rel).read_text(encoding="utf-8"), distribution_name())
    assert not hits, (
        f"{rel} hands the reader an index install of an unpublished distribution: {hits}. "
        f"Install from the checkout instead, or publish first."
    )


def test_the_release_procedure_is_marked_dormant():
    """Exempting it is only safe while it says not to run it."""
    head = (REPO / RELEASE_PROCEDURE).read_text(encoding="utf-8")[:1200].lower()
    assert "dormant" in head and "do not run" in head


def test_a_fenced_index_install_is_detected():
    doc = "Install it:\n\n```bash\npip install widget-cli\n```\n"
    assert index_installs(doc, "widget-cli") == ["pip install widget-cli"]


def test_an_extra_does_not_hide_an_index_install():
    doc = '```bash\nuvx --from "widget-cli[mcp]" widget-mcp\n```\n'
    assert index_installs(doc, "widget-cli")


def test_prose_explaining_the_command_is_not_an_instruction():
    doc = "A `pip install widget-cli` from an index would fetch the CLI alone.\n"
    assert index_installs(doc, "widget-cli") == []


def test_a_checkout_or_vcs_install_is_not_an_index_install():
    doc = (
        "```bash\nuv pip install -e .\n"
        "pip install 'widget-cli[mcp] @ git+https://example.invalid/widget'\n```\n"
    )
    assert index_installs(doc, "widget-cli") == []


if __name__ == "__main__":
    dist = distribution_name()
    offenders = {rel: index_installs((REPO / rel).read_text(encoding="utf-8"), dist)
                 for rel in _docs()}
    print(dist, "->", {k: v for k, v in offenders.items() if v} or "no index installs documented")
