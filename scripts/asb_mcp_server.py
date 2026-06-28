"""asb-mcp — an MCP skill-server for ASB skill collections.

The "skill provider, programmatically" endgame: exposes the collection's retrieval
surface as Model-Context-Protocol tools, so ANY MCP-capable agent (Claude Code,
Claude Desktop, Cursor, Cline, Codex, …) can search and fetch skills/workflows/
tools at run time — without installing the whole collection. It composes with a
Perspicacité MCP (evidence grounding): one server for skill retrieval, one for
grounding.

It reuses `asb_skill_index` (the same keyword retrieval as `asbb search` and each
collection's `bin/semantic_search.py` offline mode), so behaviour is identical
across the CLI, the docs-site, and MCP. Pure-offline, no API key required.

Run:
    ASB_COLLECTIONS_ROOT=/path/to/checkout asb-mcp        # after `pip install .[mcp]`
    uvx --from "asb-skill-collections[mcp]" asb-mcp        # zero-install

Claude Desktop / Code config (mcpServers):
    {
      "asb-skills": {
        "command": "uvx",
        "args": ["--from", "asb-skill-collections[mcp]", "asb-mcp"],
        "env": {"ASB_COLLECTIONS_ROOT": "/path/to/asb-skill-collections"}
      }
    }

Requires the `mcp` extra: `pip install "asb-skill-collections[mcp]"`.
"""
from __future__ import annotations

import sys

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # pragma: no cover - exercised only without the extra
    print(
        "asb-mcp requires the 'mcp' package. Install with:\n"
        '  pip install "asb-skill-collections[mcp]"\n'
        "  # or: uvx --from \"asb-skill-collections[mcp]\" asb-mcp",
        file=sys.stderr,
    )
    raise SystemExit(1)

from scripts import asb_skill_index as idx

mcp = FastMCP("asb-skills")


@mcp.tool()
def list_collections() -> list[dict]:
    """List the available ASB skill collections (slug, version, counts, what's
    present). Call this first to learn what can be searched."""
    return idx.discover_collections(None)


@mcp.tool()
def search_skills(query: str, collection: str | None = None,
                  technique: str | None = None, k: int = 10) -> list[dict]:
    """Search atomic skills by meaning/keywords. `collection` is 'slug' (latest)
    or 'slug/vN', or omit to search every collection. `technique` filters by tag
    (e.g. 'LC-MS'). Returns ranked {slug, name, score, description, techniques,
    tools, collection}."""
    return idx.search(collection, "skills", query, technique=technique, k=k)


@mcp.tool()
def search_workflows(query: str, collection: str | None = None, k: int = 5) -> list[dict]:
    """Search composite workflow super-skills (end-to-end pipelines). Use for a
    whole-pipeline goal rather than a single step."""
    return idx.search(collection, "workflows", query, k=k)


@mcp.tool()
def search_tools(query: str, collection: str | None = None, k: int = 10) -> list[dict]:
    """Search software-tool records (XCMS, SIRIUS, GNPS, …) across a collection."""
    return idx.search(collection, "tools", query, k=k)


@mcp.tool()
def get_skill(slug: str, collection: str) -> str:
    """Return the full SKILL.md of one skill. `collection` is 'slug' or 'slug/vN'."""
    text = idx.get_item_text(collection, "skills", slug)
    return text if text is not None else f"NOT FOUND: skill {slug!r} in {collection!r}"


@mcp.tool()
def get_workflow(slug: str, collection: str) -> str:
    """Return the full SKILL.md of one composite workflow super-skill."""
    text = idx.get_item_text(collection, "workflows", slug)
    return text if text is not None else f"NOT FOUND: workflow {slug!r} in {collection!r}"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
