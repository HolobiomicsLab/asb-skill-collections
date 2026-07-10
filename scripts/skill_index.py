"""Keep a collection's indexes complete: every indexable skill has an entry.

`skills_index.json` and `kb_bundle.json` are what `asbb search`, the MCP skill-server
and the documentation site read. Nothing derives them from the skills directory --
`propagate_license_tiers.py` only joins tiers onto entries that already exist, keyed
by DOI. So a skill grounded on a tool with no paper DOI (a tool admitted on its
licence tier rather than on an open-access paper) can ship on disk while appearing in
no index at all, invisible to every consumer. `check_license_tiers.py` then skips it,
because it only cross-checks skills the index already knows, and CI stays green.

This module closes that hole. It derives an index entry from the skill's own
frontmatter, so the skills directory is the source of truth for what exists, and it
fails when an index is missing a skill that belongs in it.

Two kinds of skill are deliberately not indexed, identified by declarative properties
rather than by name: infrastructure skills in `_`-prefixed directories (the same
convention `release_gate.py` uses) and meta skills declaring `metadata.role: meta`.
"""
from __future__ import annotations

import argparse
import glob as globlib
import json
import pathlib
import sys

import yaml

from scripts.propagate_license_tiers import detect_indent

META_ROLE = "meta"
INFRASTRUCTURE_PREFIX = "_"
DEFAULT_COLLECTION_GLOB = "collections/*/v*"


def _rewrite_json(path: pathlib.Path, payload) -> None:
    """Write JSON back in the file's own indent, byte-compatible with the generator."""
    raw = path.read_text(encoding="utf-8")
    path.write_text(json.dumps(payload, indent=detect_indent(raw), ensure_ascii=False), encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    """Split a SKILL.md into (frontmatter, body).

    The delimiter is a line that is exactly `---`. Splitting on the *substring*
    `---` truncates any frontmatter containing a rule or a `-----` run inside a
    quoted value, so YAML then fails and the skill is silently dropped from
    whatever index is being built. This is the one parser; do not copy it.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for end, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                frontmatter = yaml.safe_load("\n".join(lines[1:end]))
            except yaml.YAMLError:
                return None, text
            return frontmatter or {}, "\n".join(lines[end + 1:])
    return None, text


def parse_frontmatter(skill_md: pathlib.Path) -> dict:
    """Parse a SKILL.md YAML frontmatter, tolerating `---` inside the body."""
    frontmatter, _ = split_frontmatter(skill_md.read_text(encoding="utf-8"))
    return frontmatter or {}


def is_indexable(slug: str, frontmatter: dict) -> bool:
    """Content skills are indexed; infrastructure and meta skills are not."""
    if slug.startswith(INFRASTRUCTURE_PREFIX):
        return False
    return (frontmatter.get("metadata") or {}).get("role") != META_ROLE


def untiered(slug: str, frontmatter: dict) -> bool:
    """A skill with no licence tier must never be indexed.

    The tier is what tells a consumer that a tool is noncommercial or restricted.
    Indexing a skill without one makes it searchable while stripping the very
    label that governs whether it may be used -- a silent downgrade, not a gap.
    """
    return (frontmatter.get("metadata") or {}).get("license_tier") not in ("open", "noncommercial", "restricted")


def entry_from_frontmatter(slug: str, frontmatter: dict) -> dict:
    """Build a skills_index entry from a skill's own frontmatter."""
    metadata = frontmatter.get("metadata") or {}
    return {
        "slug": slug,
        "name": frontmatter.get("name") or slug,
        "description": frontmatter.get("description") or "",
        "edam_operation": metadata.get("edam_operation"),
        "edam_topics": metadata.get("edam_topics") or [],
        "tools": metadata.get("tools") or [],
        "dois": _dois(frontmatter),
        "techniques": metadata.get("techniques") or [],
        "license_tier": metadata.get("license_tier"),
    }


def kb_entry_from_frontmatter(frontmatter: dict) -> dict:
    """Build a kb_bundle skills entry from a skill's own frontmatter."""
    metadata = frontmatter.get("metadata") or {}
    repo_url = metadata.get("repo_url")
    return {
        "dois": _dois(frontmatter),
        "kb_slugs": [],
        "license_tier": metadata.get("license_tier"),
        "repo_urls": [repo_url] if repo_url else [],
        "tools": metadata.get("tools") or [],
    }


def _dois(frontmatter: dict) -> list[str]:
    entries = frontmatter.get("derived_from") or []
    return [str(e.get("doi")) for e in entries if isinstance(e, dict) and e.get("doi")]


def indexable_skills(version_dir: pathlib.Path) -> dict[str, dict]:
    """Map slug -> frontmatter for every skill that belongs in an index."""
    found = {}
    for skill_md in sorted((version_dir / "skills").glob("*/SKILL.md")):
        slug = skill_md.parent.name
        frontmatter = parse_frontmatter(skill_md)
        if is_indexable(slug, frontmatter):
            found[slug] = frontmatter
    return found


def missing_from_indexes(version_dir: pathlib.Path) -> dict[str, list[str]]:
    """Slugs absent from each index this collection publishes."""
    expected = set(indexable_skills(version_dir))
    gaps: dict[str, list[str]] = {}
    skills_index = version_dir / "skills_index.json"
    if skills_index.exists():
        present = {e.get("slug") for e in json.loads(skills_index.read_text(encoding="utf-8"))}
        gaps["skills_index.json"] = sorted(expected - present)
    kb_bundle = version_dir / "kb_bundle.json"
    if kb_bundle.exists():
        present = set((json.loads(kb_bundle.read_text(encoding="utf-8")).get("skills") or {}))
        gaps["kb_bundle.json"] = sorted(expected - present)
    return {name: slugs for name, slugs in gaps.items() if slugs}


def add_missing(version_dir: pathlib.Path) -> dict[str, list[str]]:
    """Insert every missing entry, keeping both indexes sorted by slug.

    Refuses to index a skill that declares no licence tier; raises so the caller
    reports it rather than writing a null tier into a consumer-facing index.
    """
    gaps = missing_from_indexes(version_dir)
    skills = indexable_skills(version_dir)
    blocked = sorted({s for slugs in gaps.values() for s in slugs if untiered(s, skills[s])})
    if blocked:
        raise ValueError(f"cannot index without metadata.license_tier: {', '.join(blocked)}")
    if gaps.get("skills_index.json"):
        path = version_dir / "skills_index.json"
        entries = json.loads(path.read_text(encoding="utf-8"))
        entries += [entry_from_frontmatter(s, skills[s]) for s in gaps["skills_index.json"]]
        entries.sort(key=lambda e: e["slug"])
        _rewrite_json(path, entries)
    if gaps.get("kb_bundle.json"):
        path = version_dir / "kb_bundle.json"
        bundle = json.loads(path.read_text(encoding="utf-8"))
        for slug in gaps["kb_bundle.json"]:
            bundle.setdefault("skills", {})[slug] = kb_entry_from_frontmatter(skills[slug])
        bundle["skills"] = dict(sorted(bundle["skills"].items()))
        _rewrite_json(path, bundle)
    return gaps


def _version_dirs(pattern: str) -> list[pathlib.Path]:
    return [pathlib.Path(p) for p in sorted(globlib.glob(pattern)) if (pathlib.Path(p) / "skills").is_dir()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--collections", default=DEFAULT_COLLECTION_GLOB)
    parser.add_argument("--fix", action="store_true", help="insert the missing entries instead of failing")
    parser.add_argument("--smoke", action="store_true", help="run the module's self-check and exit")
    args = parser.parse_args(argv)

    if args.smoke:
        return _smoke()

    violations = 0
    for version_dir in _version_dirs(args.collections):
        try:
            gaps = add_missing(version_dir) if args.fix else missing_from_indexes(version_dir)
        except ValueError as exc:
            print(f"  {version_dir}: {exc}")
            violations += 1
            continue
        for index_name, slugs in gaps.items():
            verb = "added to" if args.fix else "MISSING from"
            print(f"  {version_dir}/{index_name}: {len(slugs)} {verb} index -> {', '.join(slugs)}")
            violations += 0 if args.fix else len(slugs)
    if violations:
        print(f"\nFAIL: {violations} skill(s) exist on disk but appear in no index.")
        print("A skill absent from the index cannot be found by search, the MCP server, or the docs site.")
        print("Run: python -m scripts.skill_index --fix")
        return 1
    print("PASS: every indexable skill is present in every index its collection publishes.")
    return 0


def _smoke() -> int:
    assert is_indexable("some-skill", {}) is True
    assert is_indexable("_router", {}) is False
    assert is_indexable("meta-skill", {"metadata": {"role": "meta"}}) is False
    built = entry_from_frontmatter("s", {"name": "s", "description": "d",
                                         "metadata": {"license_tier": "noncommercial", "tools": ["T"]},
                                         "derived_from": [{"doi": "x/y"}]})
    assert built["license_tier"] == "noncommercial" and built["dois"] == ["x/y"] and built["tools"] == ["T"]
    assert kb_entry_from_frontmatter({"metadata": {"repo_url": "https://example.org/r"}})["repo_urls"] == ["https://example.org/r"]
    print("PASS: skill_index smoke check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
