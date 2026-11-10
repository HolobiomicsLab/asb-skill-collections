"""Check or bring the master marketplace in line with the release registry.

The registry (collections.yaml) records, per domain, the commit and tag of each
release. A marketplace plugin whose git-subdir source points at a registry
domain repository and at the path of that domain's latest published release is
"governed": its sha must equal the release commit and its version must equal
the release label (the tag without the "<domain>-v" prefix). Other entries,
such as technique packs, are never judged and never changed.

Exit codes: 0 clean, 1 a disagreement, 2 usage or unreadable input.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
DEFAULT_MANIFEST = ROOT / "collections.yaml"

AUTHOR = {"name": "Holobiomics Lab", "url": "https://github.com/HolobiomicsLab"}
REGISTRY_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"
LICENSE = "CC-BY-4.0"


class InputError(Exception):
    """Unreadable or malformed input; maps to exit code 2."""


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InputError(f"cannot read marketplace {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("plugins"), list):
        raise InputError(f"marketplace {path} has no plugins list")
    return data


def load_registry(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise InputError(f"cannot read registry {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("domains"), dict):
        raise InputError(f"registry {path} has no domains mapping")
    return data["domains"]


def release_label(slug: str, tag: str) -> str:
    prefix = f"{slug}-v"
    if not tag.startswith(prefix) or len(tag) == len(prefix):
        raise InputError(f"tag {tag!r} does not start with {prefix!r}")
    return tag[len(prefix):]


def latest_releases(domains: dict) -> dict[str, dict]:
    """Return the latest published (non-legacy) release of each domain."""
    latest: dict[str, dict] = {}
    for slug, domain in domains.items():
        published = [
            r for r in (domain or {}).get("releases") or [] if r.get("status") != "legacy"
        ]
        if not published:
            continue
        release = max(published, key=lambda r: int(r["version"]))
        latest[slug] = {
            "slug": slug,
            "repository": domain.get("repository"),
            "path": release.get("path"),
            "tag": release.get("tag"),
            "commit": release.get("commit"),
        }
    return latest


def governing(plugin: dict, latest: dict[str, dict]) -> dict | None:
    """Return the latest release that governs this plugin, or None."""
    source = plugin.get("source")
    if not isinstance(source, dict) or source.get("source") != "git-subdir":
        return None
    for release in latest.values():
        if source.get("url") == release["repository"] and source.get("path") == release["path"]:
            return release
    return None


def compare(marketplace: dict, latest: dict[str, dict], require_all: bool):
    """Return (lines, failed) describing every entry."""
    lines: list[str] = []
    failed = False
    seen: set[str] = set()
    for plugin in marketplace["plugins"]:
        name = plugin.get("name", "?")
        release = governing(plugin, latest)
        if release is None:
            lines.append(f"{name}: not governed by the registry")
            continue
        seen.add(release["slug"])
        if not release["tag"]:
            lines.append(f"{name}: skipped, registry release has no tag")
            continue
        label = release_label(release["slug"], release["tag"])
        problems = []
        if plugin["source"].get("sha") != release["commit"]:
            problems.append(f"sha {plugin['source'].get('sha')} != registry {release['commit']}")
        if plugin.get("version") != label:
            problems.append(f"version {plugin.get('version')!r} != registry {label!r}")
        if problems:
            failed = True
            lines.append(f"{name}: DISAGREES, " + "; ".join(problems))
        else:
            lines.append(f"{name}: ok ({label} at {release['commit'][:8]})")
    for slug, release in latest.items():
        if slug in seen:
            continue
        if not release["tag"]:
            lines.append(f"{slug}: skipped, registry release has no tag")
            continue
        release_label(slug, release["tag"])
        lines.append(f"{slug}: missing from the marketplace (registry {release['tag']})")
        if require_all:
            failed = True
    return lines, failed


def parse_pairs(values: list[str], option: str) -> dict[str, str]:
    pairs = {}
    for value in values or []:
        slug, sep, rest = value.partition("=")
        if not sep or not slug or not rest:
            raise InputError(f"{option} expects <slug>=<value>, got {value!r}")
        pairs[slug] = rest
    return pairs


def description_for(release: dict, texts: dict[str, str], checkouts: dict[str, str]) -> str:
    slug = release["slug"]
    if slug in texts:
        return texts[slug]
    if slug in checkouts:
        manifest = Path(checkouts[slug]) / release["path"] / ".claude-plugin" / "plugin.json"
        try:
            description = json.loads(manifest.read_text(encoding="utf-8")).get("description")
        except (OSError, ValueError) as exc:
            raise InputError(f"{slug}: cannot read {manifest}: {exc}") from exc
        if not isinstance(description, str) or not description:
            raise InputError(f"{slug}: {manifest} has no description")
        return description
    raise InputError(
        f"{slug}: no description; pass --description {slug}=<text> or --checkout {slug}=<path>"
    )


def new_entry(release: dict, description: str) -> dict[str, Any]:
    slug = release["slug"]
    return {
        "name": slug,
        "source": {
            "source": "git-subdir",
            "url": release["repository"],
            "path": release["path"],
            "ref": "main",
            "sha": release["commit"],
        },
        "description": description,
        "version": release_label(slug, release["tag"]),
        "author": dict(AUTHOR),
        "homepage": REGISTRY_URL,
        "repository": REGISTRY_URL,
        "license": LICENSE,
        "keywords": [slug, "agentic-science", "skills"],
    }


def apply_write(marketplace, latest, texts, checkouts, existing_only=False):
    """Mutate the marketplace in place; return the notes. Raises InputError first.

    With existing_only, governed entries move and no entry is added.
    """
    notes: list[str] = []
    seen: set[str] = set()
    for plugin in marketplace["plugins"]:
        release = governing(plugin, latest)
        if release is None:
            continue
        seen.add(release["slug"])
        if not release["tag"]:
            continue
        plugin["source"]["sha"] = release["commit"]
        plugin["version"] = release_label(release["slug"], release["tag"])
    additions = []
    for slug, release in latest.items():
        if slug in seen:
            continue
        if not release["tag"]:
            notes.append(f"{slug}: skipped, registry release has no tag")
            continue
        if existing_only:
            notes.append(f"{slug}: not added (--existing-only)")
            continue
        additions.append(new_entry(release, description_for(release, texts, checkouts)))
        notes.append(f"{slug}: added")
    marketplace["plugins"].extend(additions)
    return notes


def dump(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="read-only comparison (default)")
    mode.add_argument("--write", action="store_true", help="bring the marketplace to the registry")
    parser.add_argument("--require-all", action="store_true",
                        help="--check also fails when a latest release has no entry")
    parser.add_argument("--existing-only", action="store_true",
                        help="--write moves governed entries and adds none")
    parser.add_argument("--marketplace", type=Path, default=DEFAULT_MARKETPLACE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--description", action="append", default=[], metavar="SLUG=TEXT")
    parser.add_argument("--checkout", action="append", default=[], metavar="SLUG=PATH")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    try:
        marketplace = load_json(args.marketplace)
        latest = latest_releases(load_registry(args.manifest))
        if args.write:
            texts = parse_pairs(args.description, "--description")
            checkouts = parse_pairs(args.checkout, "--checkout")
            notes = apply_write(marketplace, latest, texts, checkouts, args.existing_only)
            new_text = dump(marketplace)
            if new_text != args.marketplace.read_text(encoding="utf-8"):
                args.marketplace.write_text(new_text, encoding="utf-8")
                notes.append(f"wrote {args.marketplace}")
            else:
                notes.append("no change")
            print("\n".join(notes))
            return 0
        lines, failed = compare(marketplace, latest, args.require_all)
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print("\n".join(lines))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
