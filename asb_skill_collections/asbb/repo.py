"""Resolve asb-skill-collections packs from a local checkout."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

MARKETPLACE_REL = Path(".claude-plugin") / "marketplace.json"


@dataclass(frozen=True)
class PackRef:
    slug: str
    source: str          # repo-relative, e.g. "packs/demo/pack"
    skills_dir: Path     # absolute <repo>/<source>/skills


def find_repo_root(start: Path) -> Path:
    start = Path(start).resolve()
    for d in (start, *start.parents):
        if (d / MARKETPLACE_REL).is_file():
            return d
    raise FileNotFoundError(
        f"no .claude-plugin/marketplace.json in any parent of {start}; "
        "run from a clone of asb-skill-collections or pass --repo"
    )


def _load_marketplace(repo: Path) -> dict:
    return json.loads((repo / MARKETPLACE_REL).read_text(encoding="utf-8"))


def list_pack_slugs(repo: Path) -> list[str]:
    return [p["name"] for p in _load_marketplace(repo).get("plugins", [])]


def resolve_pack(repo: Path, slug: str) -> PackRef:
    for p in _load_marketplace(repo).get("plugins", []):
        if p["name"] == slug:
            source = p["source"]
            if source.startswith("./"):
                source = source[2:]
            skills_dir = (Path(repo) / source / "skills").resolve()
            return PackRef(slug=slug, source=source, skills_dir=skills_dir)
    raise KeyError(slug)


def iter_skill_dirs(pack: PackRef) -> list[Path]:
    if not pack.skills_dir.is_dir():
        return []
    return sorted(
        d for d in pack.skills_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )
