"""Compare public collection-count claims with their on-disk units.

The checker discovers marketplace collection and pack sources, count
metadata, plugin descriptions, router frontmatter and release-facing Markdown.
It deliberately derives totals from shipped records rather than from another
advertised index value. Manifest releases supply external censuses. Root-document
claims follow a release named in their own sentence, then on their line, then in
the nearest heading (a sibling ``collections/<slug>/v<N>`` tree named there is
censused on the spot); otherwise they follow the unit selected by the README
badges, falling back to the marketplace.
"""

from __future__ import annotations

import argparse
import functools
import json
import pathlib
import re
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from urllib.parse import unquote

import yaml

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))


from asb_skill_collections import layout
from scripts.regen_catalogue import load_collections_manifest

COUNT_KINDS = ("skills", "tools", "workflows", "papers", "entries")
WORD_COUNTS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}
NUMBER = r"(?P<count>\d{1,3}(?:,\d{3})*|\d+)"
PROSE_PATTERNS = {
    "workflows": (
        re.compile(
            rf"{NUMBER}\s+composite(?:\s+\S+){{0,6}}\s+super-skills?\b",
            re.IGNORECASE,
        ),
        re.compile(rf"{NUMBER}\s+(?:composite\s+)?workflows?\b", re.IGNORECASE),
    ),
    "skills": (
        re.compile(rf"{NUMBER}\s+(?:evidence-grounded\s+)?skills?\b", re.IGNORECASE),
    ),
    "tools": (
        re.compile(
            rf"{NUMBER}\s+(?:software[- ]tool(?:\s+records?)?|tools?)\b",
            re.IGNORECASE,
        ),
    ),
    "papers": (
        re.compile(
            rf"{NUMBER}\s+(?:(?:peer-reviewed|source|method)\s+){{0,3}}papers?\b",
            re.IGNORECASE,
        ),
    ),
}
SENTENCE_BREAK = re.compile(r"(?<=[.;!?])\s+")
NON_TOTAL_CONTEXT = re.compile(
    r"\b(?:dropped|excluded|held out|duplicate(?:d|s)?|technique-agnostic|checked)\b",
    re.IGNORECASE,
)
ROOT_ADVERTISING_DOCS = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
)


@dataclass(frozen=True)
class Unit:
    """One collection or pack and the counts derived from its shipped files."""

    root: pathlib.Path
    relative: pathlib.Path
    slug: str
    version: str | None
    census: dict[str, int]
    sources: dict[str, str]
    release_tag: str | None = None
    version_doi: str | None = None
    repository: str | None = None
    external: bool = False


@dataclass(frozen=True)
class CountClaim:
    """One numeric public claim tied to a discovered unit and count kind."""

    site: pathlib.Path
    line: int
    unit: pathlib.Path
    kind: str
    advertised: int
    actual: int | None
    census_source: str


@dataclass(frozen=True)
class CountFailure:
    """A stale or unverifiable advertised count."""

    claim: CountClaim

    def render(self) -> str:
        """Return the actionable one-line failure shown by the CLI."""
        claim = self.claim
        actual = "unavailable" if claim.actual is None else f"{claim.actual:,}"
        return (
            f"{claim.site.as_posix()}:{claim.line}: [{claim.unit.as_posix()}] "
            f"{claim.kind} advertises {claim.advertised:,}; census is {actual} "
            f"({claim.census_source})"
        )


def _load_yaml(path: pathlib.Path) -> dict:
    """Load one YAML mapping, returning an empty mapping for an empty file."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _load_frontmatter(path: pathlib.Path) -> dict:
    """Load YAML frontmatter without parsing the Markdown body as YAML."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line == "---")
    except StopIteration:
        return {}
    value = yaml.safe_load("\n".join(lines[1:end]))
    return value if isinstance(value, dict) else {}


def _record_values(record: dict, key: str) -> list[str]:
    """Return string facet values from top-level or skill metadata."""
    metadata = record.get("metadata")
    container = metadata if isinstance(metadata, dict) else record
    values = container.get(key, record.get(key, []))
    return [str(value) for value in values] if isinstance(values, list) else []


def _add_facets(
    counts: dict[str, int],
    sources: dict[str, str],
    kind: str,
    records: Iterable[dict],
    source: str,
) -> None:
    """Add technique and EDAM-topic facet censuses for concrete records."""
    materialised = list(records)
    for dimension, field in (("technique", "techniques"), ("edam", "edam_topics")):
        values = Counter(
            value
            for record in materialised
            for value in set(_record_values(record, field))
        )
        for value, count in values.items():
            key = f"{kind}:{dimension}:{value}"
            counts[key] = count
            sources[key] = f"{source} {field}={value}"


def _count_records(root: pathlib.Path) -> tuple[dict[str, int], dict[str, str]]:
    """Derive all available count kinds from concrete records in one unit."""
    counts: dict[str, int] = {}
    sources: dict[str, str] = {}
    leaf_dir = layout.leaf_dir(root)
    if leaf_dir.is_dir():
        leaf_paths = list(leaf_dir.glob("*/SKILL.md"))
        counts["skills"] = len(leaf_paths)
        sources["skills"] = f"{leaf_dir.name}/*/SKILL.md"
        _add_facets(
            counts,
            sources,
            "skills",
            (_load_frontmatter(path) for path in leaf_paths),
            sources["skills"],
        )
    entries = root / layout.ADVERTISED_DIRNAME
    if entries.is_dir() and layout.is_router_shaped(root):
        counts["entries"] = sum(1 for _ in entries.glob("*/SKILL.md"))
        sources["entries"] = f"{layout.ADVERTISED_DIRNAME}/*/SKILL.md"
    tool_paths = list(root.glob("tools/*.yaml"))
    if (root / "tools").is_dir():
        counts["tools"] = len(tool_paths)
        sources["tools"] = "tools/*.yaml"
        _add_facets(
            counts,
            sources,
            "tools",
            (_load_yaml(path) for path in tool_paths),
            sources["tools"],
        )
    if (root / "workflows").is_dir():
        counts["workflows"] = sum(1 for _ in root.glob("workflows/*/workflow.yaml"))
        sources["workflows"] = "workflows/*/workflow.yaml"
    corpus = root / "corpus.yaml"
    if corpus.is_file():
        papers = _load_yaml(corpus).get("papers")
        if isinstance(papers, list):
            counts["papers"] = len(papers)
            sources["papers"] = "corpus.yaml papers[]"
            statuses = [
                str(paper.get("status", "")).casefold()
                for paper in papers
                if isinstance(paper, dict)
            ]
            counts["papers_included"] = statuses.count("included")
            sources["papers_included"] = "corpus.yaml papers[status=included]"
            counts["papers_hold"] = sum(
                status in {"hold", "held"} for status in statuses
            )
            sources["papers_hold"] = "corpus.yaml papers[status=hold]"
    return counts, sources


def _unit(root: pathlib.Path, repo: pathlib.Path) -> Unit:
    """Build a unit record from its path and optional collection metadata."""
    metadata_path = root / "collection.yaml"
    metadata = _load_yaml(metadata_path) if metadata_path.is_file() else {}
    relative = root.relative_to(repo)
    slug = str(metadata.get("slug") or root.name)
    version = metadata.get("version")
    if version is None and root.name.startswith("v"):
        version = root.name[1:]
    counts, sources = _count_records(root)
    return Unit(
        root,
        relative,
        slug,
        str(version) if version is not None else None,
        counts,
        sources,
    )


def _marketplace_plugins(repo: pathlib.Path) -> list[dict]:
    """Return marketplace plugins when the repository declares them."""
    path = repo / ".claude-plugin" / "marketplace.json"
    if not path.is_file():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    return value.get("plugins", []) if isinstance(value, dict) else []


def _manifest_units(repo: pathlib.Path) -> list[Unit]:
    """Build external census units from domain releases in collections.yaml."""
    domains = load_collections_manifest(repo).get("domains")
    if not isinstance(domains, dict):
        return []
    units = []
    for slug, domain in domains.items():
        if not isinstance(domain, dict):
            continue
        releases = domain.get("releases")
        if not isinstance(releases, list):
            continue
        for index, release in enumerate(releases):
            if not isinstance(release, dict) or not isinstance(
                release.get("path"), str
            ):
                continue
            relative = pathlib.Path(release["path"])
            if relative.is_absolute() or ".." in relative.parts:
                continue
            census = {
                kind: release[kind]
                for kind in COUNT_KINDS
                if isinstance(release.get(kind), int)
            }
            sources = {
                kind: f"collections.yaml domains.{slug}.releases[{index}].{kind}"
                for kind in census
            }
            version = release.get("version")
            units.append(
                Unit(
                    repo / relative,
                    relative,
                    str(slug),
                    str(version) if version is not None else None,
                    census,
                    sources,
                    str(release["tag"]) if release.get("tag") else None,
                    str(release["version_doi"])
                    if release.get("version_doi")
                    else None,
                    str(domain["repository"])
                    if domain.get("repository")
                    else None,
                    external=True,
                )
            )
    return units


def discover_units(repo: pathlib.Path) -> tuple[list[Unit], dict[str, Unit]]:
    """Discover advertised collection and pack roots without a site allowlist."""
    roots: set[pathlib.Path] = set()
    plugins = _marketplace_plugins(repo)
    plugin_roots: dict[str, pathlib.Path] = {}
    for plugin in plugins:
        source = str(plugin.get("source", "")).removeprefix("./")
        candidate = (repo / source).resolve()
        if (
            source
            and (candidate == repo or repo in candidate.parents)
            and candidate.is_dir()
        ):
            roots.add(candidate)
            plugin_roots[str(plugin.get("name", ""))] = candidate
    if not roots:
        roots.update(
            path.parent for path in repo.glob("collections/*/v*/collection.yaml")
        )
    units = [_unit(path, repo) for path in sorted(roots)]
    by_root = {unit.root: unit for unit in units}
    plugin_units = {name: by_root[path] for name, path in plugin_roots.items()}
    return [*units, *_manifest_units(repo)], plugin_units


def _line_for(path: pathlib.Path, pattern: str, start: int = 0) -> int:
    """Return the one-based line of the first regex match at or after start."""
    lines = path.read_text(encoding="utf-8").splitlines()
    for offset, line in enumerate(lines[start:], start):
        if re.search(pattern, line):
            return offset + 1
    return 1


def _json_value_line(path: pathlib.Path, key: str, value: str) -> int:
    """Locate a scalar JSON value while accepting escaped or literal Unicode."""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if f'"{key}"' not in line:
            continue
        try:
            parsed = json.loads("{" + line.strip().removesuffix(",") + "}")
        except json.JSONDecodeError:
            continue
        if parsed.get(key) == value:
            return number
    return 1


def _claim(
    repo: pathlib.Path,
    site: pathlib.Path,
    line: int,
    unit: Unit,
    kind: str,
    advertised: int,
    census_kind: str | None = None,
) -> CountClaim:
    """Construct one claim using the unit's independently derived census."""
    census_key = census_kind or kind
    return CountClaim(
        site.relative_to(repo),
        line,
        unit.relative,
        kind,
        advertised,
        unit.census.get(census_key),
        unit.sources.get(census_key, "no on-disk record set discovered"),
    )


def _prose_claims(
    repo: pathlib.Path,
    site: pathlib.Path,
    text: str,
    unit: Unit,
    start_line: int = 1,
    include_entries: bool = True,
    unit_at: Callable[[int], Unit] | None = None,
) -> list[CountClaim]:
    """Extract total-like numeric noun phrases from prose.

    ``unit_at`` resolves the unit of the claim starting at a text offset; without
    it every claim belongs to ``unit``.
    """
    claims: list[CountClaim] = []
    for kind, patterns in PROSE_PATTERNS.items():
        for pattern in patterns:
            for match in pattern.finditer(text):
                context = text[max(0, match.start() - 80) : match.end() + 120]
                if NON_TOTAL_CONTEXT.search(context):
                    continue
                if match.start() and text[match.start() - 1] in "~≈":
                    continue
                line = start_line + text.count("\n", 0, match.start())
                value = int(match.group("count").replace(",", ""))
                claim_unit = unit_at(match.start()) if unit_at else unit
                claims.append(_claim(repo, site, line, claim_unit, kind, value))
    if include_entries:
        claims.extend(_entry_claims(repo, site, text, unit, start_line))
    return claims


def _entry_count(raw: str) -> int:
    """Parse a small word or digit used for advertised entry counts."""
    lowered = raw.casefold()
    return WORD_COUNTS.get(lowered, int(raw) if raw.isdigit() else 0)


def _listed_entry_count(items: str) -> int:
    """Count a short natural-language list joined by commas or ``and``."""
    return len([item for item in re.split(r"\s+and\s+|\s*,\s*", items) if item.strip()])


def _entry_claims(
    repo: pathlib.Path,
    site: pathlib.Path,
    text: str,
    unit: Unit,
    start_line: int,
) -> list[CountClaim]:
    """Extract counts of host-visible ``skills/`` entries, including word numbers."""
    patterns = (
        (
            re.compile(
                r"\b(?P<count>\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+skills?\s+(?:is|are)\s+advertised\b",
                re.IGNORECASE,
            ),
            "count",
        ),
        (
            re.compile(
                r"\b(?P<count>\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+host-visible\s+(?:adapters?|entries|skills?)\b",
                re.IGNORECASE,
            ),
            "count",
        ),
        (re.compile(r"\bthe\s+only\s+advertised\s+skill\b", re.IGNORECASE), "one"),
        (
            re.compile(
                r"\bonly\s+(?P<items>[^.;]{1,180}?)\s+(?:is|are)\s+advertised\b",
                re.IGNORECASE,
            ),
            "items",
        ),
        (
            re.compile(
                r"\bonly\s+(?P<items>[^.;\n]{1,180}?)\s+sit\s+under\s+`?skills/?`?",
                re.IGNORECASE,
            ),
            "items",
        ),
    )
    claims: list[CountClaim] = []
    for pattern, mode in patterns:
        for match in pattern.finditer(text):
            value = (
                1
                if mode == "one"
                else (
                    _entry_count(match.group("count"))
                    if mode == "count"
                    else _listed_entry_count(match.group("items"))
                )
            )
            line = start_line + text.count("\n", 0, match.start())
            claims.append(_claim(repo, site, line, unit, "entries", value))
    return claims


def _strip_fences(markdown: str) -> str:
    """Blank fenced examples while preserving their original line numbers."""
    inside = False
    output = []
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            inside = not inside
            output.append("")
        else:
            output.append("" if inside else line)
    return "\n".join(output)


def _unit_for_site(site: pathlib.Path, units: Iterable[Unit]) -> Unit | None:
    """Resolve a document below a unit, preferring the deepest root."""
    candidates = [
        unit for unit in units if site == unit.root or unit.root in site.parents
    ]
    return max(candidates, key=lambda unit: len(unit.root.parts), default=None)


def _released_collection_units(plugin_units: dict[str, Unit]) -> list[Unit]:
    """Return unique marketplace units that live below collections/."""
    unique = {
        unit.relative: unit
        for unit in plugin_units.values()
        if unit.relative.parts[0] == "collections"
    }
    return list(unique.values())


def _root_doc_unit(
    text: str, units: list[Unit], plugin_units: dict[str, Unit]
) -> Unit | None:
    """Resolve a root document's default census, preferring its badge target."""
    badge_units = _badge_units(text, units)
    if len(badge_units) == 1:
        return badge_units[0]
    local_units = [unit for unit in units if not unit.external]
    lowered = text.lower()
    matched = [
        unit for unit in local_units if unit.relative.as_posix().lower() in lowered
    ]
    if len(matched) == 1:
        return matched[0]
    released = _released_collection_units(plugin_units)
    return released[0] if len(released) == 1 else None


def _badge_links(text: str) -> list[str]:
    """Return the link targets that wrap a count badge."""
    html_link = re.compile(
        r"<a\s+[^>]*href=[\"']([^\"']+)[\"'][^>]*>\s*<img[^>]*"
        r"badge/(?:skills|tools|workflows|papers)-",
        re.IGNORECASE,
    )
    markdown_link = re.compile(
        r"\[![^]]*\]\([^)]*badge/(?:skills|tools|workflows|papers)-[^)]*\)\]"
        r"\(([^)]+)\)",
        re.IGNORECASE,
    )
    return [
        match.group(1)
        for pattern in (html_link, markdown_link)
        for match in pattern.finditer(text)
    ]


def _badge_units(text: str, units: list[Unit]) -> list[Unit]:
    """Return manifest units whose version DOI links a count badge."""
    badge_links = _badge_links(text)
    return [
        unit
        for unit in units
        if unit.external
        and unit.version_doi
        and any(unit.version_doi in unquote(link) for link in badge_links)
    ]


def _release_for_context(
    context: str, local_units: list[Unit], manifest_units: list[Unit]
) -> Unit | None:
    """Resolve explicit release identities, preferring tags, DOIs and repositories."""
    lowered = context.casefold()
    strong_matches = [
        unit
        for unit in manifest_units
        if any(
            identity and identity.casefold() in lowered
            for identity in (
                unit.release_tag,
                unit.version_doi,
                unit.repository,
                pathlib.PurePosixPath(unit.repository).name
                if unit.repository
                else None,
            )
        )
    ]
    if len(strong_matches) == 1:
        return strong_matches[0]
    path_matches = [
        unit
        for unit in local_units
        if unit.relative.as_posix().casefold() in lowered
    ]
    if len(path_matches) == 1:
        return path_matches[0]
    version_matches = [
        unit
        for unit in [*local_units, *manifest_units]
        if unit.version
        and re.search(
            rf"(?<![\w.])v{re.escape(unit.version)}(?:\.\d+){{0,2}}(?![\w.])",
            context,
            re.IGNORECASE,
        )
    ]
    unique: dict[pathlib.Path, Unit] = {}
    for unit in version_matches:
        unique.setdefault(unit.relative, unit)
    return next(iter(unique.values())) if len(unique) == 1 else None


def _sibling_collection_unit(
    repo: pathlib.Path, context: str, units: list[Unit]
) -> Unit | None:
    """Census a collection version named in ``context`` that no unit covers.

    A root document may describe an earlier or later ``collections/<slug>/v<N>``
    tree that the marketplace does not list (an unreleased legacy collection kept
    beside the candidate, for instance); its counts are checked against that tree
    rather than against the advertised unit.
    """
    known = {unit.root for unit in units}
    slugs = sorted({unit.slug for unit in units if not unit.external})
    versions = sorted(
        {
            match.group("version")
            for match in re.finditer(
                r"(?<![\w.])v(?P<version>\d+)(?![\w.])", context, re.IGNORECASE
            )
        }
    )
    found = [
        root
        for slug in slugs
        for version in versions
        if (root := repo / "collections" / slug / f"v{version}") not in known
        and (root / "collection.yaml").is_file()
    ]
    return _unit(found[0], repo) if len(found) == 1 else None


def _sentence_at(text: str, offset: int) -> str:
    """Return the sentence of ``text`` that contains ``offset``."""
    start = 0
    for boundary in SENTENCE_BREAK.finditer(text):
        if boundary.end() > offset:
            return text[start : boundary.start()]
        start = boundary.end()
    return text[start:]


def _root_doc_claim_unit(
    repo: pathlib.Path,
    text: str,
    line: int,
    default: Unit,
    units: list[Unit],
    offset: int | None = None,
) -> Unit:
    """Resolve one claim from its sentence, its line, then its nearest heading.

    A line that names several releases ("Collection v1 (166 skills) ... lists v2
    only") binds each claim to the release named in the claim's own sentence when
    ``offset`` (the claim's column on the line) is given. Each context is tried
    against the known units first, then against a sibling collection tree it
    names.
    """
    lines = text.splitlines()
    claim_line = lines[line - 1] if 0 < line <= len(lines) else ""
    local_units = [unit for unit in units if not unit.external]
    manifest_units = [unit for unit in units if unit.external]
    heading = next(
        (
            candidate
            for candidate in reversed(lines[: max(0, line - 1)])
            if candidate.lstrip().startswith("#")
        ),
        "",
    )
    contexts = [claim_line, f"{heading}\n{claim_line}"]
    if offset is not None:
        contexts.insert(0, _sentence_at(claim_line, offset))
    for context in contexts:
        selected = _release_for_context(
            context, local_units, manifest_units
        ) or _sibling_collection_unit(repo, context, units)
        if selected is not None:
            return selected
    return default


def _markdown_claims(
    repo: pathlib.Path, units: list[Unit], plugin_units: dict[str, Unit]
) -> list[CountClaim]:
    """Scan release-facing Markdown, excluding copied command transcripts."""
    sites = [repo / name for name in ROOT_ADVERTISING_DOCS if (repo / name).is_file()]
    sites.extend(path for unit in units for path in unit.root.glob("*.md"))
    sites.extend(
        path
        for unit in units
        for path in (unit.root / layout.ADVERTISED_DIRNAME).glob("*/SKILL.md")
    )
    claims: list[CountClaim] = []
    for site in sorted({path for path in sites if path.is_file()}):
        raw = site.read_text(encoding="utf-8")
        local_unit = _unit_for_site(site, [unit for unit in units if not unit.external])
        unit = local_unit or _root_doc_unit(raw, units, plugin_units)
        if unit is not None:
            text = _strip_fences(raw)
            if local_unit is not None:
                claims.extend(_prose_claims(repo, site, text, unit))
                continue
            for number, line in enumerate(text.splitlines(), 1):
                if not any(
                    pattern.search(line)
                    for patterns in PROSE_PATTERNS.values()
                    for pattern in patterns
                ):
                    continue
                line_unit = _root_doc_claim_unit(repo, raw, number, unit, units)
                claims.extend(
                    _prose_claims(
                        repo,
                        site,
                        line,
                        line_unit,
                        number,
                        include_entries=False,
                        unit_at=functools.partial(
                            _root_doc_claim_unit, repo, raw, number, line_unit, units
                        ),
                    )
                )
            fallback = _root_doc_unit(
                "", [u for u in units if not u.external], plugin_units
            )
            if fallback is not None:
                claims.extend(_entry_claims(repo, site, text, fallback, 1))
    return claims


def _badge_claims(
    repo: pathlib.Path, units: list[Unit], plugin_units: dict[str, Unit]
) -> list[CountClaim]:
    """Read shields-style count badges from the root README."""
    site = repo / "README.md"
    if not site.is_file():
        return []
    text = site.read_text(encoding="utf-8")
    unit = _root_doc_unit(text, units, plugin_units)
    if unit is None:
        return []
    pattern = re.compile(
        r"badge/(skills|tools|workflows|papers)-([0-9%,]+)-", re.IGNORECASE
    )
    return [
        _claim(
            repo,
            site,
            number,
            unit,
            match.group(1).lower(),
            int(unquote(match.group(2)).replace(",", "")),
        )
        for number, line in enumerate(text.splitlines(), 1)
        for match in pattern.finditer(line)
    ]


def _metadata_claims(repo: pathlib.Path, units: list[Unit]) -> list[CountClaim]:
    """Read explicit ``*_count`` fields from collection and router YAML."""
    claims: list[CountClaim] = []
    for unit in units:
        sites = [unit.root / "collection.yaml"]
        sites.extend((unit.root / layout.ADVERTISED_DIRNAME).glob("*/SKILL.md"))
        for site in sites:
            if not site.is_file():
                continue
            for number, line in enumerate(
                site.read_text(encoding="utf-8").splitlines(), 1
            ):
                match = re.match(
                    r"\s*(skills|tools|workflows|papers)_count:\s*(\d+)\s*$", line
                )
                if match:
                    claims.append(
                        _claim(
                            repo,
                            site,
                            number,
                            unit,
                            match.group(1),
                            int(match.group(2)),
                        )
                    )
    return claims


def _corpus_summary_claims(repo: pathlib.Path, units: list[Unit]) -> list[CountClaim]:
    """Treat corpus summary totals as paper-count advertisements."""
    claims: list[CountClaim] = []
    for unit in units:
        site = unit.root / "corpus.yaml"
        if not site.is_file() or "papers" not in unit.census:
            continue
        data = _load_yaml(site)
        summary = data.get("summary") if isinstance(data.get("summary"), dict) else {}
        for key, census_kind in (
            ("total", "papers"),
            ("included", "papers_included"),
            ("hold", "papers_hold"),
        ):
            if isinstance(summary.get(key), int):
                line = _line_for(site, rf"^\s+{key}:\s*{summary[key]}\s*$")
                claims.append(
                    _claim(
                        repo,
                        site,
                        line,
                        unit,
                        "papers",
                        summary[key],
                        census_kind,
                    )
                )
    return claims


def _description_claims(
    repo: pathlib.Path, units: list[Unit], plugin_units: dict[str, Unit]
) -> list[CountClaim]:
    """Scan marketplace, local plugin and archive descriptions."""
    claims: list[CountClaim] = []
    marketplace = repo / ".claude-plugin/marketplace.json"
    for plugin in _marketplace_plugins(repo):
        unit = plugin_units.get(str(plugin.get("name", "")))
        description = plugin.get("description")
        if unit is not None and isinstance(description, str):
            line = _json_value_line(marketplace, "description", description)
            claims.extend(_prose_claims(repo, marketplace, description, unit, line))
    for unit in units:
        for site in (
            unit.root / ".claude-plugin/plugin.json",
            unit.root / ".zenodo.json",
        ):
            if not site.is_file():
                continue
            data = json.loads(site.read_text(encoding="utf-8"))
            description = data.get("description")
            if isinstance(description, str):
                line = _json_value_line(site, "description", description)
                claims.extend(_prose_claims(repo, site, description, unit, line))
    return claims


def _catalogue_claims(repo: pathlib.Path, units: list[Unit]) -> list[CountClaim]:
    """Read collection totals from the generated JSON-LD catalogue."""
    site = repo / "catalogue.jsonld"
    if not site.is_file():
        return []
    entries = json.loads(site.read_text(encoding="utf-8")).get("collections", [])
    by_id = {(unit.slug, unit.version): unit for unit in units}
    claims: list[CountClaim] = []
    cursor = 0
    for entry in entries:
        unit = by_id.get((str(entry.get("slug")), str(entry.get("version"))))
        if unit is None:
            continue
        cursor = _line_for(site, rf'"slug":\s*"{re.escape(unit.slug)}"', cursor) - 1
        for kind in COUNT_KINDS:
            value = entry.get(f"{kind}_count")
            if isinstance(value, int):
                line = _line_for(site, rf'"{kind}_count":\s*{value}', cursor)
                claims.append(_claim(repo, site, line, unit, kind, value))
    return claims


def _pack_table_claims(
    repo: pathlib.Path, plugin_units: dict[str, Unit]
) -> list[CountClaim]:
    """Discover count columns in pack README tables keyed by plugin name."""
    claims: list[CountClaim] = []
    for site in repo.glob("packs/*/README.md"):
        headers: list[str] = []
        for number, line in enumerate(site.read_text(encoding="utf-8").splitlines(), 1):
            cells = [
                cell.strip().strip("`") for cell in line.strip().strip("|").split("|")
            ]
            if line.lstrip().startswith("|") and any(
                cell.lower() in COUNT_KINDS for cell in cells
            ):
                headers = [cell.lower() for cell in cells]
                continue
            if not headers or not cells or cells[0] not in plugin_units:
                continue
            unit = plugin_units[cells[0]]
            for index, kind in enumerate(headers):
                if (
                    kind in COUNT_KINDS
                    and index < len(cells)
                    and cells[index].replace(",", "").isdigit()
                ):
                    claims.append(
                        _claim(
                            repo,
                            site,
                            number,
                            unit,
                            kind,
                            int(cells[index].replace(",", "")),
                        )
                    )
    return claims


def _plain_cell(cell: str) -> str:
    """Remove common Markdown decoration from a table cell."""
    return re.sub(r"[`*]", "", cell).strip()


def _facet_key(unit: Unit, kind: str, dimension: str, label: str) -> str | None:
    """Resolve one table label against facet values discovered from records."""
    prefix = f"{kind}:{dimension}:"
    available = {
        key[len(prefix) :].casefold(): key
        for key in unit.census
        if key.startswith(prefix)
    }
    plain = _plain_cell(label)
    if dimension == "edam":
        marker = re.search(r"\btopic_\d+\b", plain, re.IGNORECASE)
        if marker:
            suffix = marker.group().casefold()
            matches = [
                key for value, key in available.items() if value.endswith(suffix)
            ]
            return matches[0] if len(matches) == 1 else None
        return None
    canonical = re.sub(r"\s*\([^)]*\)\s*$", "", plain).strip().casefold()
    return available.get(canonical)


def _facet_table_claims(
    repo: pathlib.Path, units: list[Unit], plugin_units: dict[str, Unit]
) -> list[CountClaim]:
    """Read technique and stable-IRI EDAM count tables from release Markdown."""
    sites = [repo / name for name in ROOT_ADVERTISING_DOCS if (repo / name).is_file()]
    sites.extend(path for unit in units for path in unit.root.glob("*.md"))
    claims: list[CountClaim] = []
    for site in sorted(set(sites)):
        text = site.read_text(encoding="utf-8")
        unit = _unit_for_site(site, units) or _root_doc_unit(text, units, plugin_units)
        if unit is None:
            continue
        headers: list[str] = []
        for number, line in enumerate(text.splitlines(), 1):
            if not line.lstrip().startswith("|"):
                headers = []
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            plain_headers = [_plain_cell(cell).casefold() for cell in cells]
            is_facet_header = any(
                header in {"technique", "tag"} or header.startswith("edam topic")
                for header in plain_headers
            ) and any(header in {"skills", "tools"} for header in plain_headers)
            if is_facet_header:
                headers = plain_headers
                continue
            if not headers or all(
                not cell or re.fullmatch(r":?-+:?", cell) for cell in cells
            ):
                continue
            key_columns = [
                index
                for index, header in enumerate(headers)
                if header in {"technique", "tag"} or header.startswith("edam topic")
            ]
            for position, key_column in enumerate(key_columns):
                if key_column >= len(cells):
                    continue
                dimension = (
                    "edam"
                    if headers[key_column].startswith("edam topic")
                    else "technique"
                )
                end = (
                    key_columns[position + 1]
                    if position + 1 < len(key_columns)
                    else len(headers)
                )
                for index in range(key_column + 1, min(end, len(cells))):
                    kind = headers[index]
                    raw_count = cells[index].replace(",", "")
                    if kind not in {"skills", "tools"} or not raw_count.isdigit():
                        continue
                    census_key = _facet_key(unit, kind, dimension, cells[key_column])
                    claims.append(
                        _claim(
                            repo,
                            site,
                            number,
                            unit,
                            kind,
                            int(raw_count),
                            census_key or f"unresolved:{kind}:{dimension}",
                        )
                    )
    return claims


def _deduplicate(claims: Iterable[CountClaim]) -> list[CountClaim]:
    """Return stable claims without double-reporting overlapping scanners."""
    return sorted(
        set(claims),
        key=lambda claim: (
            claim.site.as_posix(),
            claim.line,
            claim.kind,
            claim.unit.as_posix(),
        ),
    )


def unbound_badge_dois(repo_root: pathlib.Path) -> list[str]:
    """Return Zenodo DOIs linked by README count badges that no registry row carries.

    Such badges select no unit, so their counts would not be audited at all. A
    repository whose registry records no version DOI is not judged.
    """
    repo = pathlib.Path(repo_root).resolve()
    site = repo / "README.md"
    if not site.is_file():
        return []
    registered = {
        unit.version_doi for unit in _manifest_units(repo) if unit.version_doi
    }
    if not registered:
        return []
    linked = {
        doi
        for link in _badge_links(site.read_text(encoding="utf-8"))
        for doi in re.findall(r"10\.5281/zenodo\.\d+", unquote(link))
    }
    return sorted(linked - registered)


def audit_repository(
    repo_root: pathlib.Path,
) -> tuple[list[CountClaim], list[CountFailure]]:
    """Discover all supported advertisements and return claims plus failures."""
    repo = pathlib.Path(repo_root).resolve()
    units, plugin_units = discover_units(repo)
    local_units = [unit for unit in units if not unit.external]
    claims = _deduplicate(
        [
            *_metadata_claims(repo, local_units),
            *_corpus_summary_claims(repo, local_units),
            *_description_claims(repo, local_units, plugin_units),
            *_catalogue_claims(repo, local_units),
            *_markdown_claims(repo, units, plugin_units),
            *_badge_claims(repo, units, plugin_units),
            *_pack_table_claims(repo, plugin_units),
            *_facet_table_claims(repo, local_units, plugin_units),
        ]
    )
    failures = [
        CountFailure(claim) for claim in claims if claim.actual != claim.advertised
    ]
    return claims, failures


def main(argv: list[str] | None = None) -> int:
    """Run the advertised-count audit and return a shell-friendly status."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        required=True,
        help="domain checkout containing collections/ and packs/",
    )
    args = parser.parse_args(argv)
    claims, failures = audit_repository(args.repo_root)
    unbound = unbound_badge_dois(args.repo_root)
    if unbound:
        print(
            "FAIL: README count badges link "
            + ", ".join(unbound)
            + ", which is not a version DOI of the registry; their counts are not audited"
        )
        if not failures:
            return 1
    if failures:
        print(
            f"FAIL: {len(failures)} stale advertised count site(s) across {len(claims)} claims"
        )
        for failure in failures:
            print(f"  - {failure.render()}")
        return 1
    print(f"PASS: {len(claims)} advertised count claim(s) match the on-disk census")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
