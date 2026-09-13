"""Check shipped-unit index closure and declared helper containment offline.

Every indexed unit discovered through ``DEFAULT_COLLECTION_GLOBS`` must name
exactly its indexable leaves in both indexes. ``--prune`` removes stale pack
rows only when their declared collection/version parent also excludes them;
it never copies, removes or invents a leaf.

``metadata.helper`` paths are unit-relative executable assets, including on
advertised, infrastructure and workflow skills. ``metadata.issue_templates``
contains repository pointers read on GitHub, not executed local assets, and is
therefore exempt from the helper rule.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from asb_skill_collections import layout
from scripts import skill_index
from scripts.propagate_license_tiers import detect_indent


@dataclass(frozen=True)
class Violation:
    """One named file/slug/direction that violates a unit's shipping contract."""

    unit: Path
    file: str
    slug: str | None
    direction: str
    message: str


@dataclass
class IndexClosure:
    """The two leaf sets and findings, also used for the gate's count suffix."""

    has_index: bool
    indexed: set[str] = field(default_factory=set)
    on_disk: set[str] = field(default_factory=set)
    violations: list[Violation] = field(default_factory=list)


def discover_units(root: Path) -> list[Path]:
    """Find every directory publishing skills_index.json in the configured trees."""
    root = root.resolve()
    return sorted(
        {
            unit
            for pattern in skill_index.DEFAULT_COLLECTION_GLOBS
            for unit in root.glob(pattern)
            if (unit / "skills_index.json").is_file()
        }
    )


def index_slugs(index_path: Path) -> tuple[set[str], str | None]:
    """Read the gate's list/wrapped-list/string index forms, preserving its errors."""
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return set(), f"unreadable ({exc})"
    if isinstance(data, dict):
        data = data.get("skills", [])
    if not isinstance(data, list):
        return set(), "not a list of entries"
    slugs: set[str] = set()
    for i, entry in enumerate(data):
        if isinstance(entry, str):
            slugs.add(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("slug"), str):
            slugs.add(entry["slug"])
        else:
            return slugs, f"entry {i} declares no slug"
    return slugs, None


def _leaf_slugs(unit: Path) -> set[str]:
    leaves = layout.leaf_dir(unit)
    return {
        path.parent.name
        for path in leaves.glob("*/SKILL.md")
        if path.is_file()
        and skill_index.is_indexable(
            path.parent.name, skill_index.parse_frontmatter(path)
        )
    }


def _kb_slugs(path: Path) -> tuple[set[str], str | None]:
    try:
        bundle = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return set(), f"unreadable ({exc})"
    if not isinstance(bundle, dict) or not isinstance(bundle.get("skills"), dict):
        return set(), "skills is not an object"
    return set(bundle["skills"]), None


def _index_findings(unit: Path, filename: str, sets: IndexClosure) -> list[Violation]:
    leaves = layout.leaf_dir(unit)
    findings = [
        Violation(
            unit,
            filename,
            slug,
            "index-to-disk",
            f"{filename} names {slug!r}, which has no SKILL.md under {leaves.name}/.",
        )
        for slug in sorted(sets.indexed - sets.on_disk)
    ]
    return findings + [
        Violation(
            unit,
            filename,
            slug,
            "disk-to-index",
            f"{leaves.name}/{slug} is not named in {filename} — it cannot "
            "be reached through the router.",
        )
        for slug in sorted(sets.on_disk - sets.indexed)
    ]


def inspect_indexes(unit: Path) -> IndexClosure:
    """Compare both published indexes to indexable direct children of leaf_dir()."""
    unit = Path(unit)
    result = IndexClosure(has_index=(unit / "skills_index.json").is_file())
    if not result.has_index:
        return result
    result.on_disk = _leaf_slugs(unit)
    for filename, reader in (
        ("skills_index.json", index_slugs),
        ("kb_bundle.json", _kb_slugs),
    ):
        if not (unit / filename).is_file():
            continue
        indexed, error = reader(unit / filename)
        if filename == "skills_index.json":
            result.indexed = indexed
        if error:
            result.violations.append(
                Violation(
                    unit, filename, None, "invalid-index", f"{filename}: {error}."
                )
            )
        result.violations.extend(
            _index_findings(unit, filename, IndexClosure(True, indexed, result.on_disk))
        )
    return result


def record_index_closure(result, unit: Path) -> None:
    """Add the shared comparison to a gate result, retaining its messages/suffix."""
    closure = inspect_indexes(unit)
    if not closure.has_index:
        result.add(
            "pass", "No skills_index.json — index consistency is not applicable."
        )
        return
    for violation in closure.violations:
        extra = {"slug": violation.slug} if violation.slug is not None else {}
        result.add("fail", violation.message, file=violation.file, **extra)
    result.summary = (
        f"{result.summary}  ({len(closure.indexed)} indexed, "
        f"{len(closure.on_disk)} on disk)"
    )


def _helper_error(unit: Path, helper) -> str | None:
    if not isinstance(helper, str) or not helper.strip():
        return "must be a nonempty path string"
    try:
        target = (unit / helper).resolve()
        target.relative_to(unit.resolve())
    except (OSError, RuntimeError, ValueError):
        return "does not resolve inside the unit"
    return None if target.is_file() else "does not resolve to a file inside the unit"


def check_helpers(unit: Path) -> list[Violation]:
    """Check all shipped SKILL.md helpers; issue_templates are GitHub pointers.

    A helper may be one path or a list. Resolve symlinks before containment and
    require files, not directories. Repository issue-template pointers are read
    on GitHub rather than executed and need not exist inside an installed unit.
    """
    unit = Path(unit)
    findings = []
    for skill in sorted(unit.rglob("SKILL.md")):
        metadata = skill_index.parse_frontmatter(skill).get("metadata") or {}
        if "helper" not in metadata:
            continue
        helpers = metadata["helper"]
        for helper in helpers if isinstance(helpers, list) else [helpers]:
            error = _helper_error(unit, helper)
            if error:
                findings.append(
                    Violation(
                        unit,
                        str(skill.relative_to(unit)),
                        skill.parent.name,
                        "helper-to-unit",
                        f"metadata.helper {helper!r} {error}.",
                    )
                )
    return findings


def check_unit(unit: Path) -> list[Violation]:
    """Return index closure and helper violations for one shipped unit."""
    return inspect_indexes(unit).violations + check_helpers(unit)


def gate_findings(collection_dir: Path) -> list[Violation]:
    """Check collection helpers and all packs in its repository, without cwd lookup."""
    collection_dir = collection_dir.resolve()
    findings = check_helpers(collection_dir)
    trees = {Path(pattern).parts[0] for pattern in skill_index.DEFAULT_COLLECTION_GLOBS}
    if collection_dir.parent.parent.name not in trees:
        return findings
    root = collection_dir.parent.parent.parent
    for unit in discover_units(root):
        if unit != collection_dir and unit.parent.parent == root / "packs":
            findings.extend(check_unit(unit))
    return findings


def _declared_parent(root: Path, bundle: dict) -> set[str]:
    collection, version = bundle.get("collection"), bundle.get("version")
    for value in (collection, version):
        if not isinstance(value, (str, int)) or str(value) in ("", ".", ".."):
            raise ValueError("pack needs an explicit collection and version")
        if "/" in str(value) or "\\" in str(value):
            raise ValueError("collection and version must be single path components")
    parent = root / "collections" / str(collection) / f"v{version}"
    try:
        parent.resolve().relative_to((root / "collections").resolve())
    except ValueError as exc:
        raise ValueError("declared parent escapes collections/") from exc
    slugs, error = index_slugs(parent / "skills_index.json")
    if error:
        raise ValueError(f"cannot establish declared parent {parent}: {error}")
    return slugs


def _prune_payload(path: Path, removed: set[str]) -> None:
    raw = path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    if path.name == "kb_bundle.json":
        payload["skills"] = {
            k: v for k, v in payload["skills"].items() if k not in removed
        }
    else:
        entries = payload["skills"] if isinstance(payload, dict) else payload
        kept = [
            e
            for e in entries
            if (e if isinstance(e, str) else e["slug"]) not in removed
        ]
        if isinstance(payload, dict):
            payload["skills"] = kept
        else:
            payload = kept
    rendered = json.dumps(payload, indent=detect_indent(raw), ensure_ascii=False)
    path.write_text(rendered + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")


def prune_pack(pack: Path, root: Path) -> dict[str, list[str]]:
    """Drop rows absent from the declared parent; refuse ambiguous or leaf-losing repairs.

    Both indexes are validated before either is written. A dangling row still
    in the declared parent requires a curator's decision, as does an on-disk
    leaf outside that parent. Neither can be repaired by deleting index rows.
    """
    pack, root = pack.resolve(), root.resolve()
    if (
        not pack.is_relative_to(root / "packs")
        or len(pack.relative_to(root / "packs").parts) != 2
    ):
        raise ValueError(f"not a pack under {root / 'packs'}: {pack}")
    closure = inspect_indexes(pack)
    if not closure.has_index or any(
        v.direction == "invalid-index" for v in closure.violations
    ):
        raise ValueError(f"cannot prune missing or malformed indexes in {pack}")
    bundle = json.loads((pack / "kb_bundle.json").read_text(encoding="utf-8"))
    parent = _declared_parent(root, bundle)
    present = {
        "skills_index.json": closure.indexed,
        "kb_bundle.json": set(bundle["skills"]),
    }
    dangling = set().union(*present.values()) - closure.on_disk
    if dangling & parent:
        raise ValueError(
            f"dangling rows still belong to declared parent: {sorted(dangling & parent)}"
        )
    if closure.on_disk - parent:
        raise ValueError(
            f"on-disk leaves absent from declared parent: {sorted(closure.on_disk - parent)}"
        )
    removed = {
        name: sorted(slugs - parent)
        for name, slugs in present.items()
        if slugs - parent
    }
    for filename, slugs in removed.items():
        _prune_payload(pack / filename, set(slugs))
    return removed


def _report(findings: list[Violation], root: Path, units: int) -> int:
    grouped: dict[tuple, list[Violation]] = {}
    for finding in findings:
        detail = (
            finding.message
            if finding.direction in ("helper-to-unit", "invalid-index")
            else ""
        )
        key = (finding.unit, finding.slug or "", finding.direction, detail)
        grouped.setdefault(key, []).append(finding)
    for (unit, slug, direction, detail), rows in sorted(grouped.items()):
        files = ", ".join(row.file for row in rows)
        suffix = f" | {detail}" if detail else ""
        print(
            f"FAIL {unit.relative_to(root)} | {files} | slug={slug or '-'} | {direction}{suffix}"
        )
    print(
        f"{'FAIL' if grouped else 'PASS'}: {len(grouped)} violation(s) across {units} indexed unit(s)."
    )
    return int(bool(grouped))


def main(argv: list[str] | None = None) -> int:
    """Check all indexed units; optionally prune pack rows using their declared parent."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument(
        "--prune",
        action="store_true",
        help="drop pack rows absent from their declared parent",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    units = discover_units(root)
    if not units:
        print(
            f"FAIL: no indexed units matched {skill_index.DEFAULT_COLLECTION_GLOBS} under {root}."
        )
        return 1
    if args.prune:
        try:
            for unit in units:
                if unit.parent.parent != root / "packs":
                    continue
                removed = prune_pack(unit, root)
                for filename, slugs in removed.items():
                    print(
                        f"PRUNE {unit.relative_to(root)}/{filename}: removed {len(slugs)} row(s)."
                    )
        except (OSError, ValueError, KeyError) as exc:
            print(f"FAIL: prune stopped: {exc}")
            return 1
    return _report(
        [finding for unit in units for finding in check_unit(unit)], root, len(units)
    )


if __name__ == "__main__":
    raise SystemExit(main())
