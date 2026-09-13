"""Resolve asb-skill-collections packs from a local checkout."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .paths import resolve_within

MARKETPLACE_REL = Path(".claude-plugin") / "marketplace.json"


@dataclass(frozen=True)
class PackRef:
    slug: str
    source: str  # repo-relative, e.g. "packs/demo/pack"
    skills_dir: Path  # absolute <repo>/<source>/skills
    version: str = "unversioned"

    @property
    def source_dir(self) -> Path:
        """Return the complete pack root beside its advertised skills directory."""
        return self.skills_dir.parent


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
            source_dir = (
                Path(repo).resolve()
                if source in ("", ".")
                else resolve_within(repo, source)
            )
            skills_dir = resolve_within(source_dir, "skills")
            descriptor = resolve_within(source_dir, ".claude-plugin/plugin.json")
            metadata = (
                json.loads(descriptor.read_text()) if descriptor.is_file() else {}
            )
            version = str(metadata.get("version", p.get("version", "unversioned")))
            return PackRef(
                slug=slug, source=source, skills_dir=skills_dir, version=version
            )
    raise KeyError(slug)


def iter_skill_dirs(pack: PackRef) -> list[Path]:
    """List advertised skill directories only after validating their containment."""
    if not pack.skills_dir.is_dir():
        return []
    directories = []
    for child in sorted(pack.skills_dir.iterdir()):
        directory = resolve_within(pack.source_dir, f"skills/{child.name}")
        if directory.is_dir():
            skill = resolve_within(pack.source_dir, f"skills/{child.name}/SKILL.md")
            if skill.is_file():
                directories.append(directory)
    return directories
