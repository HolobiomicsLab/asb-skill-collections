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

Local load counting is **off unless `ASB_SKILLS_USAGE_PATH` is set**, and even
then it is purely local: it appends nothing to the network, records no user,
session or host identifier, and never stores a query string. See
`docs/design/skill-load-telemetry.md`; the network beacon described there stays
deferred pending the CNRS GDPR audit.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

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

from . import asb_skill_index as idx

mcp = FastMCP("asb-skills")


# --------------------------------------------------------------------------- #
# Local skill-load counter — dormant by default.                              #
# --------------------------------------------------------------------------- #
#: Setting this to a writable path turns the counter on. Unset (or empty), the
#: server counts nothing and touches no file: `docs/design/skill-load-telemetry.md`
#: is deferred pending a GDPR audit by CNRS legal counsel, and a telemetry
#: feature that is on by default while its legal review is open is exactly the
#: thing that audit exists to prevent.
USAGE_PATH_ENV = "ASB_SKILLS_USAGE_PATH"

USAGE_SCHEMA_VERSION = "0.1"

#: The whole record. Nothing here identifies a user, a session, a machine or a
#: query: which skill was loaded, through which tool, how many times, and the
#: first and last hour it happened. Adding a field to this tuple is a privacy
#: decision, not a formatting one.
USAGE_FIELDS = ("skill_slug", "tool_name", "count", "first_seen", "last_seen")


def usage_path() -> Path | None:
    """The counter's output file, or ``None`` when the counter is off."""
    raw = (os.environ.get(USAGE_PATH_ENV) or "").strip()
    return Path(raw) if raw else None


def _utc_hour() -> str:
    """Now, truncated to the hour, UTC.

    The telemetry design rounds timestamps to the hour so individual sessions
    cannot be reconstructed from a sequence of events. The local counter keeps
    that property, because this file is meant to be handed over as-is when the
    collection-level rollup is eventually built — a local file that records
    minute-resolution activity would have to be sanitised first, and the step
    that has to be remembered is the step that gets forgotten.
    """
    return datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat()


def _read_usage(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def record_skill_load(skill_slug: str, tool_name: str) -> bool:
    """Count one skill load in the local usage file. Returns whether it counted.

    A no-op returning ``False`` unless ``ASB_SKILLS_USAGE_PATH`` names a file.
    Read-modify-write of a small JSON document; a corrupt or unwritable file
    costs the caller nothing, because a counter that can break a skill lookup
    is worse than no counter.
    """
    path = usage_path()
    if path is None:
        return False
    now = _utc_hour()
    try:
        doc = _read_usage(path)
        records = doc.get("records")
        records = [r for r in records if isinstance(r, dict)] if isinstance(records, list) else []
        for record in records:
            if record.get("skill_slug") == skill_slug and record.get("tool_name") == tool_name:
                count = record.get("count")
                record["count"] = (count if isinstance(count, int) else 0) + 1
                record["last_seen"] = now
                break
        else:
            records.append(
                {
                    "skill_slug": skill_slug,
                    "tool_name": tool_name,
                    "count": 1,
                    "first_seen": now,
                    "last_seen": now,
                }
            )
        payload = {"schema_version": USAGE_SCHEMA_VERSION, "records": records}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        return False
    return True


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
    if text is None:
        return f"NOT FOUND: skill {slug!r} in {collection!r}"
    record_skill_load(slug, "get_skill")
    return text


@mcp.tool()
def get_workflow(slug: str, collection: str) -> str:
    """Return the full SKILL.md of one composite workflow super-skill."""
    text = idx.get_item_text(collection, "workflows", slug)
    if text is None:
        return f"NOT FOUND: workflow {slug!r} in {collection!r}"
    record_skill_load(slug, "get_workflow")
    return text


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
