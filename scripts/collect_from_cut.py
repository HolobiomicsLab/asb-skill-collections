#!/usr/bin/env python3
"""Collect one consolidated cut into a deterministic release candidate (S3)."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# ``python scripts/collect_from_cut.py`` puts only scripts/ on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import collect_metabolomics_collection as description_writer
from scripts import release_gate, router_shape, skill_index
from asb_skill_collections import layout


APPROVED_PREFIXES = description_writer.APPROVED_PREFIXES
SPAN_CAP = release_gate._TEXT_FIELD_CAP
DOI_CAP = release_gate._CUMULATIVE_CAP
_SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
_VERSION_RE = re.compile(r"^v([1-9][0-9]*)$")
_SECTION_RE = re.compile(r"(?m)^## (?P<name>[^\n]+)\s*\n(?P<body>.*?)(?=^## |\Z)", re.S)


class CollectorError(RuntimeError):
    """An invalid or incomplete collector input."""


class ConflictError(CollectorError):
    """A destination already contains different bytes."""


def _json_bytes(value: Any) -> bytes:
    """Render stable, human-readable JSON."""
    return (
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    ).encode()


def _yaml_bytes(value: Any) -> bytes:
    """Render deterministic YAML without aliases or generated metadata."""
    return yaml.safe_dump(
        value,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    ).encode()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _read_bytes(path: Path) -> bytes:
    if not path.is_file() or path.is_symlink():
        raise CollectorError(f"required regular file is missing: {path}")
    return path.read_bytes()


def _read_json(path: Path) -> Any:
    try:
        return json.loads(_read_bytes(path).decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CollectorError(f"invalid JSON in {path}: {exc}") from exc


def _read_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(_read_bytes(path).decode("utf-8"))
    except (UnicodeError, yaml.YAMLError) as exc:
        raise CollectorError(f"invalid YAML in {path}: {exc}") from exc


def _normal_doi(value: Any) -> str:
    """Use the gate identity and strip resolver-only query/fragment suffixes."""
    return release_gate._norm_doi(value).split("#", 1)[0].split("?", 1)[0].strip()


def _stable_unique(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _validate_slug(value: str, label: str = "slug") -> str:
    if not isinstance(value, str) or not _SLUG_RE.fullmatch(value):
        raise CollectorError(f"invalid {label}: {value!r}")
    return value


def _section(body: str, name: str) -> str:
    """Return one level-two section exactly as description synthesis sees it."""
    for match in _SECTION_RE.finditer(body):
        if match.group("name").strip() == name:
            return match.group("body").strip()
    return ""


def _render_skill(frontmatter: dict[str, Any], body: str) -> bytes:
    rendered = _yaml_bytes(frontmatter)
    suffix = body.rstrip() + "\n"
    return b"---\n" + rendered + b"---\n" + suffix.encode("utf-8")


def _tree_digest(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(files):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(files[relative]).digest())
    return digest.hexdigest()


def _disk_tree(path: Path) -> dict[str, bytes]:
    if not path.exists():
        return {}
    if not path.is_dir() or path.is_symlink():
        raise ConflictError(f"output is not a regular directory: {path}")
    files: dict[str, bytes] = {}
    for child in sorted(path.rglob("*")):
        if child.is_symlink():
            raise ConflictError(f"output contains a symlink: {child}")
        if child.is_file():
            files[child.relative_to(path).as_posix()] = child.read_bytes()
    return files


def _boundary_prefix(text: str, limit: int) -> str:
    """Cut prose at a sentence boundary; drop it if none fits the cap."""
    if len(text) <= limit:
        return text
    prefix = text[:limit]
    endings = list(re.finditer(r"[.!?](?=\s|$)", prefix))
    if endings:
        return prefix[: endings[-1].end()].strip()
    return ""


@dataclass
class QuoteBudget:
    """Apply the release gate's strict DOI classes and evidence parser contract."""

    corpus: dict[str, Any] | None
    access_by_doi: dict[str, str] = field(init=False, default_factory=dict)
    reuse_by_doi: dict[str, bool] = field(init=False, default_factory=dict)
    used: Counter[str] = field(default_factory=Counter)
    exhausted: set[str] = field(default_factory=set)
    kept: list[dict[str, Any]] = field(default_factory=list)
    dropped: list[dict[str, Any]] = field(default_factory=list)
    parser_stats: Counter[str] = field(default_factory=Counter)

    def __post_init__(self) -> None:
        if self.corpus is None:
            return
        for paper in self.corpus.get("papers") or []:
            if not isinstance(paper, dict):
                continue
            doi = _normal_doi(paper.get("doi"))
            access = (
                paper.get("access") if isinstance(paper.get("access"), dict) else {}
            )
            if doi:
                self.access_by_doi[doi] = release_gate._normalize_access_type(
                    str(access.get("type") or "")
                )
        self.reuse_by_doi = {
            _normal_doi(doi): permitted
            for doi, permitted in release_gate._reuse_by_doi_from_corpus(
                self.corpus
            ).items()
            if _normal_doi(doi)
        }

    @property
    def applied(self) -> bool:
        return self.corpus is not None

    def strict(self, doi: str) -> bool:
        normalized = _normal_doi(doi)
        access_is_strict = (
            self.access_by_doi.get(normalized, "unknown")
            in release_gate._CAPPED_VERBATIM_TIERS
            or normalized not in self.access_by_doi
        )
        reuse_is_strict = (
            normalized in self.reuse_by_doi and not self.reuse_by_doi[normalized]
        )
        return access_is_strict or reuse_is_strict

    def retain(self, text: str, context: dict[str, Any]) -> str:
        """Return allowed text and receipt every shortening or removal."""
        original = text.strip()
        if not self.applied:
            return original
        doi = _normal_doi(context.get("doi"))
        strict = self.strict(doi)
        kept = _boundary_prefix(original, SPAN_CAP) if strict else original
        reason = "per_span_cap" if kept != original else None
        if strict and (doi in self.exhausted or self.used[doi] + len(kept) > DOI_CAP):
            kept = ""
            reason = "cumulative_budget_exhausted"
            self.exhausted.add(doi)
        record = {**context, "doi": doi}
        if kept != original:
            self.dropped.append(
                {
                    **record,
                    "text": original,
                    "kept_text": kept,
                    "dropped_text": original[len(kept) :],
                    "reason": reason,
                }
            )
        if kept:
            self.used[doi] += len(kept)
            self.kept.append(
                {
                    **record,
                    "text": kept,
                    "characters": len(kept),
                    "capped": strict,
                }
            )
        return kept

    def _frontmatter_spans(
        self, frontmatter: dict[str, Any], leaf: str, default_doi: str
    ) -> bool:
        changed = False
        for key in ("evidence_spans", "evidence"):
            original_items = frontmatter.get(key)
            if not isinstance(original_items, list):
                continue
            rendered: list[Any] = []
            for item in original_items:
                if isinstance(item, str):
                    text = item.strip()
                    doi = default_doi
                    text_key = None
                elif isinstance(item, dict):
                    text_key = "text" if item.get("text") is not None else "quote"
                    text = str(item.get(text_key) or "").strip()
                    doi = _normal_doi(item.get("doi")) or default_doi
                else:
                    rendered.append(item)
                    continue
                if not text:
                    rendered.append(item)
                    continue
                kept = self.retain(
                    text,
                    {
                        "kind": "leaf",
                        "leaf": leaf,
                        "tool": None,
                        "source": f"frontmatter.{key}",
                        "doi": doi,
                    },
                )
                changed |= kept != text
                if not kept:
                    continue
                if isinstance(item, str):
                    rendered.append(kept)
                else:
                    updated = copy.deepcopy(item)
                    updated[text_key] = kept
                    rendered.append(updated)
            frontmatter[key] = rendered
        return changed

    def _body_blocks(self, body: str) -> list[tuple[int, int, str, str]]:
        """Locate exactly the blocks recognized by the gate-owned parser."""
        lines = body.splitlines()
        blocks: list[tuple[int, int, str, str]] = []
        index = 0
        while index < len(lines):
            line = lines[index]
            complete = release_gate._EVIDENCE_VERBATIM_RE.match(line)
            if complete:
                blocks.append(
                    (index, index + 1, complete.group(1), complete.group("text"))
                )
                index += 1
                continue
            start = release_gate._EVIDENCE_VERBATIM_START_RE.match(line)
            if not start:
                index += 1
                continue
            text_lines = [start.group("text")]
            stop = index + 1
            found = False
            while stop < len(lines):
                candidate = lines[stop]
                if release_gate._EVIDENCE_ITEM_RE.match(candidate):
                    break
                closing = candidate.rstrip()
                if closing.endswith('"'):
                    text_lines.append(closing[:-1])
                    stop += 1
                    found = True
                    break
                text_lines.append(candidate)
                stop += 1
            if found:
                blocks.append((index, stop, start.group(1), "\n".join(text_lines)))
                index = stop
            else:
                index += 1
        parsed, stats = release_gate._parse_evidence_body(body)
        located = [block[3] for block in blocks]
        if located != parsed:
            raise CollectorError(
                "collector evidence locator disagrees with release gate parser"
            )
        self.parser_stats.update(stats)
        return blocks

    def trim_leaf(
        self,
        frontmatter: dict[str, Any],
        body: str,
        leaf: str,
        default_doi: str,
    ) -> tuple[str, bool]:
        """Trim one leaf in the same span order the gate counts."""
        if not self.applied:
            return body, False
        changed = self._frontmatter_spans(frontmatter, leaf, default_doi)
        blocks = self._body_blocks(body)
        if not blocks:
            return body, changed
        lines = body.splitlines()
        output: list[str] = []
        cursor = 0
        for start, stop, prefix, text in blocks:
            output.extend(lines[cursor:start])
            kept = self.retain(
                text,
                {
                    "kind": "leaf",
                    "leaf": leaf,
                    "tool": None,
                    "source": "body",
                    "body_line": start + 1,
                    "doi": default_doi,
                },
            )
            changed |= kept != text.strip()
            if kept:
                if kept == text.strip():
                    output.extend(lines[start:stop])
                else:
                    parts = kept.splitlines() or [""]
                    if len(parts) == 1:
                        output.append(f'{prefix}: "{parts[0]}"')
                    else:
                        output.append(f'{prefix}: "{parts[0]}')
                        output.extend(parts[1:-1])
                        output.append(parts[-1] + '"')
            cursor = stop
        output.extend(lines[cursor:])
        suffix = "\n" if body.endswith("\n") else ""
        return "\n".join(output) + suffix, changed


def _rewrite_description(frontmatter: dict[str, Any], body: str, domain: str) -> bool:
    original = str(frontmatter.get("description") or "")
    if len(original) <= description_writer.MAX_LEN and original.startswith(
        APPROVED_PREFIXES
    ):
        return False
    frontmatter["description"] = description_writer._build_description(
        str(frontmatter.get("name") or ""),
        _section(body, "When to use"),
        original,
        domain_label=domain,
    )
    return True


def _github_url(value: Any) -> str | None:
    raw = str(value or "").strip().rstrip("/")
    if not raw:
        return None
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", raw):
        return f"https://github.com/{raw}"
    if re.match(r"^https://github\.com/[^/]+/[^/]+$", raw, re.I):
        return raw
    return None


def _resolve_build(cut: Path, build_name: str) -> Path:
    _validate_slug(build_name.replace("_", "-"), "build directory")
    candidates = (cut.parent / "builds" / build_name, cut.parent / build_name)
    # Provisional views bind build directories through a read-only symlink tree.
    # Inputs may therefore be symlinks; only output paths are required to be
    # regular, non-symlink locations.
    found = [path for path in candidates if path.is_dir()]
    if len(found) != 1:
        raise CollectorError(
            f"expected one build directory for {build_name}, found {len(found)}"
        )
    return found[0]


def _load_builds(
    cut: Path, coverages: dict[str, dict[str, Any]], digests: dict[str, str]
) -> dict[str, dict[str, Any]]:
    names: set[str] = set()
    for coverage in coverages.values():
        for member in coverage.get("members") or []:
            parts = Path(str(member.get("source_bundle") or "")).parts
            if len(parts) != 3 or parts[1] != "skills":
                raise CollectorError(
                    f"invalid source_bundle: {member.get('source_bundle')!r}"
                )
            names.add(parts[0])
    builds: dict[str, dict[str, Any]] = {}
    for name in sorted(names):
        root = _resolve_build(cut, name)
        manifest_path = root / "build_manifest.json"
        triage_path = root / layout.ADVERTISED_DIRNAME / "_triage_manifest.json"
        tools_path = root / "tools" / "_index.json"
        manifest = _read_json(manifest_path)
        triage_payload = _read_json(triage_path)
        tools_payload = _read_json(tools_path)
        rows = triage_payload.get("rows") or []
        triage = {row.get("slug"): row for row in rows if isinstance(row, dict)}
        if len(triage) != len(rows):
            raise CollectorError(f"duplicate or invalid triage rows in build {name}")
        records = tools_payload.get("records") or []
        if not all(isinstance(record, dict) for record in records):
            raise CollectorError(f"invalid tool index records in build {name}")
        logical_root = f"builds/{name}"
        for logical, path in (
            (f"{logical_root}/build_manifest.json", manifest_path),
            (f"{logical_root}/skills/_triage_manifest.json", triage_path),
            (f"{logical_root}/tools/_index.json", tools_path),
        ):
            digests[logical] = _sha256_bytes(_read_bytes(path))
        flags = (manifest.get("cli_invocation") or {}).get("flags_resolved") or {}
        builds[name] = {
            "root": root,
            "flags": flags,
            "triage": triage,
            "records": records,
            "tool_repos": defaultdict(set),
        }
    return builds


def _member_triage(
    member: dict[str, Any], builds: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    parts = Path(str(member.get("source_bundle") or "")).parts
    row = builds[parts[0]]["triage"].get(parts[2], {})
    return {
        "triage_status": row.get("triage_status") or "untriaged",
        "yes_rate": row.get("yes_rate"),
        "n_claims": row.get("n_claims"),
    }


def _leaf_dois(frontmatter: dict[str, Any]) -> list[str]:
    return _stable_unique(
        [
            doi
            for raw in release_gate._skill_dois(frontmatter)
            if (doi := _normal_doi(raw))
        ]
    )


def _prepare_leaf(
    source: Path,
    coverage: dict[str, Any],
    builds: dict[str, dict[str, Any]],
    budget: QuoteBudget,
    domain: str,
    license_name: str,
) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
    output_id = source.name
    if coverage.get("output_id") != output_id:
        raise CollectorError(f"coverage output id does not match directory: {source}")
    text = _read_bytes(source / "skill.md").decode("utf-8")
    frontmatter, body = skill_index.split_frontmatter(text)
    if not isinstance(frontmatter, dict):
        raise CollectorError(f"skill has no valid frontmatter: {source / 'skill.md'}")
    cut_tools = _read_json(source / "tools.json")
    if not isinstance(cut_tools, list) or not all(
        isinstance(name, str) for name in cut_tools
    ):
        raise CollectorError(f"tools.json must be a list of names: {source}")
    members = coverage.get("members") or []
    canonical = [
        member
        for member in members
        if member.get("member_id") == coverage.get("canonical_member_id")
    ]
    if len(canonical) != 1:
        raise CollectorError(f"coverage has no unique canonical member: {output_id}")

    tool_rows = frontmatter.get("tools") or []
    raw_repos = [
        tool.get("repo")
        for tool in tool_rows
        if isinstance(tool, dict) and tool.get("repo")
    ]
    first_repo = _github_url(raw_repos[0]) if raw_repos else None
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        frontmatter["metadata"] = metadata
    if first_repo:
        metadata["repo_url"] = first_repo
    else:
        metadata.pop("repo_url", None)
    tool_names = list(cut_tools) + [
        str(tool["name"])
        for tool in tool_rows
        if isinstance(tool, dict) and tool.get("name")
    ]
    metadata["tools"] = sorted(set(tool_names))
    metadata["edam_operation"] = frontmatter.get("edam_operation")
    metadata["edam_topics"] = copy.deepcopy(frontmatter.get("edam_topics") or [])
    frontmatter["license"] = license_name

    provenance = frontmatter.get("provenance")
    if not isinstance(provenance, dict):
        provenance = {}
        frontmatter["provenance"] = provenance
    for paper in provenance.get("source_papers") or []:
        if isinstance(paper, dict) and paper.get("doi"):
            paper["doi"] = _normal_doi(paper["doi"])
    derived_from = frontmatter.get("derived_from") or []
    for index, source_record in enumerate(derived_from):
        if isinstance(source_record, dict) and source_record.get("doi"):
            source_record["doi"] = _normal_doi(source_record["doi"])
        elif isinstance(source_record, str):
            derived_from[index] = _normal_doi(source_record)
    if frontmatter.get("doi"):
        frontmatter["doi"] = _normal_doi(frontmatter["doi"])
    if "content_hash" in frontmatter:
        provenance["source_content_hash"] = frontmatter.pop("content_hash")
    merged_aliases = list(coverage.get("merged_slugs") or [])
    if merged_aliases:
        frontmatter["merged_aliases"] = merged_aliases
    else:
        frontmatter.pop("merged_aliases", None)
        frontmatter.pop("merged_alias_records", None)

    rewritten = _rewrite_description(frontmatter, body, domain)
    dois = _leaf_dois(frontmatter)
    if not dois:
        raise CollectorError(f"cut leaf has no source DOI: {output_id}")
    body, trimmed = budget.trim_leaf(frontmatter, body, output_id, dois[0])
    if trimmed:
        frontmatter["evidence_trimmed"] = True
    else:
        frontmatter.pop("evidence_trimmed", None)

    triage = _member_triage(canonical[0], builds)
    frontmatter.update(triage)
    canonical_parts = Path(str(canonical[0]["source_bundle"])).parts
    canonical_build = builds[canonical_parts[0]]
    for tool in tool_rows:
        if not isinstance(tool, dict) or not tool.get("name"):
            continue
        repo = _github_url(tool.get("repo"))
        if repo:
            canonical_build["tool_repos"][str(tool["name"])].add(repo)

    mapping = {
        "output_id": output_id,
        "leaf_slug": output_id,
        "member_ids": [member["member_id"] for member in members],
        "canonical_member_id": coverage["canonical_member_id"],
        "capsules": list(coverage.get("capsules") or []),
        "merge_kind": coverage.get("merge_kind") or "single",
        "merged_aliases": merged_aliases,
        "dois": dois,
        "description_rewritten": rewritten,
        "evidence_trimmed": trimmed,
    }
    index = {
        "slug": output_id,
        "name": frontmatter.get("name") or output_id,
        "description": frontmatter.get("description") or "",
        "edam_operation": metadata.get("edam_operation"),
        "edam_topics": metadata.get("edam_topics") or [],
        "tools": metadata.get("tools") or [],
        "dois": dois,
        "techniques": metadata.get("techniques") or [],
        "license_tier": "unknown",
    }
    return _render_skill(frontmatter, body), mapping, index


def _tool_sources(
    builds: dict[str, dict[str, Any]],
) -> dict[str, list[tuple[str, dict, dict]]]:
    grouped: defaultdict[str, list[tuple[str, dict, dict]]] = defaultdict(list)
    for build_name in sorted(builds):
        build = builds[build_name]
        for record in build["records"]:
            slug = _validate_slug(str(record.get("slug") or ""), "tool slug")
            grouped[slug].append((build_name, build, record))
    return dict(sorted(grouped.items()))


def _prepare_tool(
    slug: str, sources: list[tuple[str, dict, dict]], budget: QuoteBudget
) -> dict[str, Any]:
    first = sources[0][2]
    versions: list[Any] = []
    papers: dict[str, dict[str, str]] = {}
    repos: list[str] = []
    spans: list[tuple[str, dict[str, Any]]] = []
    seen_spans: set[tuple[str, str]] = set()
    for build_name, build, record in sources:
        version = record.get("version_used")
        if version is not None and version not in versions:
            versions.append(version)
        repos.extend(sorted(build["tool_repos"].get(record.get("name"), set())))
        canonical = _github_url(record.get("canonical_url"))
        if canonical:
            repos.append(canonical)
        raw_build_repos = build["flags"].get("github_repo") or []
        if isinstance(raw_build_repos, str):
            raw_build_repos = [raw_build_repos]
        repos.extend(
            repo for raw_repo in raw_build_repos if (repo := _github_url(raw_repo))
        )
        doi = _normal_doi(record.get("source_paper_doi") or build["flags"].get("doi"))
        if doi:
            papers.setdefault(
                doi,
                {"doi": doi, "title": str(record.get("source_paper_title") or "")},
            )
        for span in record.get("evidence_spans") or []:
            text = (
                span
                if isinstance(span, str)
                else (
                    span.get("text") or span.get("quote") or ""
                    if isinstance(span, dict)
                    else ""
                )
            )
            text = str(text).strip()
            identity = (text, doi)
            if text and identity not in seen_spans:
                seen_spans.add(identity)
                spans.append(
                    (
                        text,
                        {
                            "kind": "tool",
                            "leaf": None,
                            "tool": slug,
                            "source": "tools/_index.json",
                            "build": build_name,
                            "doi": doi,
                        },
                    )
                )
    kept = [
        permitted
        for text, context in spans
        if (permitted := budget.retain(text, context))
    ]
    repos = _stable_unique(repos)
    return {
        "name": first.get("name") or slug,
        "slug": slug,
        "version_used": versions[0] if versions else None,
        "edam_topics": [],
        "evidence_spans": kept,
        "derived_from": list(papers.values()),
        "source_repos": repos,
        "schema_version": "0.2.0",
        "license_tier": "unknown",
        "license": None,
        "license_detection": None,
        "license_subject": None,
        "repo_url": repos[0] if repos else None,
    }


def _creator_to_cff(creator: dict[str, Any]) -> dict[str, Any]:
    if creator.get("name"):
        return {"name": creator["name"]}
    required = ("family", "given", "orcid", "affiliation")
    if not all(creator.get(key) for key in required):
        raise CollectorError(f"person creator lacks one of {required}: {creator!r}")
    orcid = str(creator["orcid"])
    if not orcid.startswith(("https://", "http://")):
        orcid = f"https://orcid.org/{orcid}"
    return {
        "family-names": creator["family"],
        "given-names": creator["given"],
        "orcid": orcid,
        "affiliation": creator["affiliation"],
    }


def _documents(
    options: argparse.Namespace,
    creators: dict[str, Any],
    mappings: list[dict[str, Any]],
    tools: dict[str, dict[str, Any]],
    cut_id: str,
    indexes: list[dict[str, Any]],
) -> dict[str, bytes]:
    reference = _read_yaml(
        Path(__file__).resolve().parent.parent
        / "collections"
        / "metabolomics"
        / "v2"
        / "collection.yaml"
    )
    people = copy.deepcopy(creators["creators"])
    lead_curators = copy.deepcopy(creators["lead_curators"])
    title_domain = options.domain.replace("-", " ").title()
    title = f"ASB {title_domain} Skill Collection {options.version}"
    iri = (
        "https://w3id.org/holobiomicslab/asb-skill/collection/"
        f"{options.domain}/{options.version}"
    )
    description = (
        f"ASB {title_domain}: {len(mappings)} evidence-grounded skills collected "
        "from a consolidated literature cut with local retrieval."
    )
    roles = copy.deepcopy(reference.get("roles") or {})
    roles["zenodo_authors"] = people
    descriptor = {
        "@context": copy.deepcopy(reference.get("@context")),
        "@type": reference.get("@type"),
        "@id": iri,
        "iri": iri,
        "title": title,
        "slug": options.domain,
        "version": int(options.version[1:]),
        "description": description,
        "license": options.license,
        "status": "candidate",
        "roles": roles,
        "lead_curators": lead_curators,
        "contributors": copy.deepcopy(reference.get("contributors") or []),
        "cut_id": cut_id,
        "skills_count": len(mappings),
        "tools_count": len(tools),
        "workflows_count": 0,
        "skills": sorted(mapping["leaf_slug"] for mapping in mappings),
        "tools": sorted(tools),
        "edam_topics": sorted(
            {
                topic
                for index in indexes
                for topic in index.get("edam_topics") or []
                if topic
            }
        ),
        "domain_topics": [],
        "source_collections": sorted(
            {doi for mapping in mappings for doi in mapping["dois"]}
        ),
        "catalogue_membership": copy.deepcopy(
            reference.get("catalogue_membership") or []
        ),
    }
    citation = {
        "cff-version": "1.2.0",
        "message": "If you use this collection, please cite it as below.",
        "title": title,
        "abstract": description,
        "version": str(int(options.version[1:])),
        "license": options.license,
        "url": options.plugin_repo,
        "type": "dataset",
        "authors": [_creator_to_cff(creator) for creator in people],
        "keywords": [options.domain, "scientific skills"],
    }
    plugin = {
        "name": options.domain,
        "description": description,
        "version": "0.1.0",
        "author": {
            "name": "Holobiomics Lab",
            "url": "https://github.com/HolobiomicsLab",
        },
        "homepage": options.plugin_repo,
        "repository": options.plugin_repo,
        "license": options.license,
        "keywords": [options.domain, "scientific skills"],
    }
    return {
        "collection.yaml": _yaml_bytes(descriptor),
        "CITATION.cff": _yaml_bytes(citation),
        ".claude-plugin/plugin.json": _json_bytes(plugin),
    }


def _shape(outputs: dict[str, bytes]) -> dict[str, bytes]:
    """Use the canonical router shaper against a provisional leaf index."""
    with tempfile.TemporaryDirectory(prefix="asb-collect-") as temporary:
        unit = Path(temporary) / "candidate"
        (unit / "leaves").mkdir(parents=True)
        for relative, data in sorted(outputs.items()):
            path = unit / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        router_shape.shape(unit, unit / "skills_index.json", set())
        return {
            path.relative_to(unit).as_posix(): path.read_bytes()
            for path in sorted(unit.rglob("*"))
            if path.is_file()
        }


def _assemble(options: argparse.Namespace) -> tuple[dict[str, bytes], dict[str, Any]]:
    cut = options.cut
    summary_path = cut / layout.ADVERTISED_DIRNAME / "coverage_summary.json"
    summary_bytes = _read_bytes(summary_path)
    summary = json.loads(summary_bytes.decode("utf-8"))
    if not isinstance(summary, dict):
        raise CollectorError("coverage_summary.json must be an output-id mapping")
    cut_id = _sha256_bytes(summary_bytes)[:12]
    digests = {"corpus/skills/coverage_summary.json": _sha256_bytes(summary_bytes)}

    source_root = cut / layout.ADVERTISED_DIRNAME
    source_dirs = sorted(path for path in source_root.iterdir() if path.is_dir())
    if not source_dirs:
        raise CollectorError("cut has no output skill directories")
    ids = [path.name for path in source_dirs]
    if set(ids) != set(summary):
        raise CollectorError("coverage summary and output directories disagree")
    coverages: dict[str, dict[str, Any]] = {}
    for source in source_dirs:
        _validate_slug(source.name, "output id")
        coverage_path = source / "coverage.json"
        coverage = _read_json(coverage_path)
        if not isinstance(coverage, dict):
            raise CollectorError(f"invalid coverage record: {coverage_path}")
        coverages[source.name] = coverage
        for name in ("skill.md", "tools.json", "coverage.json"):
            path = source / name
            digests[f"corpus/skills/{source.name}/{name}"] = _sha256_bytes(
                _read_bytes(path)
            )
    builds = _load_builds(cut, coverages, digests)

    creators_bytes = _read_bytes(options.creators)
    creators = yaml.safe_load(creators_bytes.decode("utf-8"))
    if not isinstance(creators, dict) or not isinstance(creators.get("creators"), list):
        raise CollectorError("creators file must define a creators list")
    if not isinstance(creators.get("lead_curators"), list):
        raise CollectorError("creators file must define a lead_curators list")
    digests["release_creators.yaml"] = _sha256_bytes(creators_bytes)

    corpus = None
    if options.corpus is not None:
        corpus_bytes = _read_bytes(options.corpus)
        corpus = yaml.safe_load(corpus_bytes.decode("utf-8"))
        if not isinstance(corpus, dict) or not isinstance(corpus.get("papers"), list):
            raise CollectorError("corpus must use the asb-corpus papers shape")
        digests["corpus.yaml"] = _sha256_bytes(corpus_bytes)
    budget = QuoteBudget(corpus)

    outputs: dict[str, bytes] = {}
    mappings: list[dict[str, Any]] = []
    indexes: list[dict[str, Any]] = []
    for source in source_dirs:
        data, mapping, index = _prepare_leaf(
            source,
            coverages[source.name],
            builds,
            budget,
            options.domain,
            options.license,
        )
        outputs[f"leaves/{source.name}/SKILL.md"] = data
        mappings.append(mapping)
        indexes.append(index)

    tools: dict[str, dict[str, Any]] = {}
    for slug, sources in _tool_sources(builds).items():
        tool = _prepare_tool(slug, sources, budget)
        tools[slug] = tool
        outputs[f"tools/{slug}.yaml"] = _yaml_bytes(tool)

    mappings.sort(key=lambda row: row["output_id"])
    indexes.sort(key=lambda row: row["slug"])
    mapping_summary = {
        "cut_id": cut_id,
        "skills": len(mappings),
        "tools": len(tools),
        "description_rewrites": sum(row["description_rewritten"] for row in mappings),
        "evidence_trimmed_leaves": sum(row["evidence_trimmed"] for row in mappings),
    }
    outputs["mapping.json"] = _json_bytes(
        {"mappings": mappings, "summary": mapping_summary}
    )
    outputs["skills_index.json"] = _json_bytes(indexes)
    outputs.update(_documents(options, creators, mappings, tools, cut_id, indexes))
    shaped = _shape(outputs)

    trim_receipt: dict[str, Any]
    if not budget.applied:
        trim_receipt = {
            "status": "not_applied",
            "cut_id": cut_id,
            "kept": [],
            "dropped": [],
            "summary": {"kept_spans": 0, "dropped_or_shortened_spans": 0},
        }
    else:
        policy_dois = sorted(set(budget.access_by_doi) | set(budget.reuse_by_doi))
        trim_receipt = {
            "status": "applied",
            "cut_id": cut_id,
            "text_field_cap": SPAN_CAP,
            "cumulative_cap": DOI_CAP,
            "order": "sorted leaves, frontmatter then gate-parsed body; sorted tools after leaves",
            "policy_source": "scripts.release_gate",
            "strict_dois": [doi for doi in policy_dois if budget.strict(doi)],
            "characters_by_doi": dict(sorted(budget.used.items())),
            "parser_stats": dict(sorted(budget.parser_stats.items())),
            "kept": budget.kept,
            "dropped": budget.dropped,
            "summary": {
                "kept_spans": len(budget.kept),
                "dropped_or_shortened_spans": len(budget.dropped),
                "dropped_leaf_spans": sum(
                    row["kind"] == "leaf" for row in budget.dropped
                ),
                "dropped_tool_spans": sum(
                    row["kind"] == "tool" for row in budget.dropped
                ),
            },
        }
    collect_receipt = {
        "status": "collected",
        "cut_id": cut_id,
        "domain": options.domain,
        "version": options.version,
        "input_sha256": dict(sorted(digests.items())),
        "output_tree_sha256": _tree_digest(shaped),
        "counts": {
            "skills": len(mappings),
            "tools": len(tools),
            "workflows": 0,
            "builds": len(builds),
            "input_files": len(digests),
        },
        "router_index": "provisional skills_index.json derived from leaf frontmatter before router_shape.shape",
    }
    return shaped, {
        "collect_receipt.json": collect_receipt,
        "evidence_trim_receipt.json": trim_receipt,
    }


def _check_receipts(destination: Path, receipts: dict[str, Any]) -> None:
    if destination.exists() and (not destination.is_dir() or destination.is_symlink()):
        raise ConflictError(f"receipts destination is not a directory: {destination}")
    for name, payload in receipts.items():
        path = destination / name
        expected = _json_bytes(payload)
        if path.exists() and (
            not path.is_file() or path.is_symlink() or path.read_bytes() != expected
        ):
            raise ConflictError(f"existing collector receipt differs: {path}")


def _check_output(destination: Path, outputs: dict[str, bytes]) -> bool:
    """Return whether an existing destination is exactly the planned tree."""
    if not destination.exists():
        return False
    current = _disk_tree(destination)
    if current.get("mapping.json") != outputs.get("mapping.json"):
        raise ConflictError(f"existing mapping differs: {destination / 'mapping.json'}")
    if _tree_digest(current) != _tree_digest(outputs) or set(current) != set(outputs):
        raise ConflictError(f"existing collector output tree differs: {destination}")
    return True


def _write_outputs(destination: Path, outputs: dict[str, bytes]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    # The public layout contract requires this root before any leaf directory.
    (destination / "leaves").mkdir(parents=True, exist_ok=True)
    for relative, data in sorted(outputs.items()):
        path = destination / relative
        if path.exists() and (not path.is_file() or path.is_symlink()):
            raise ConflictError(f"refusing non-regular output path: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def _write_receipts(destination: Path, receipts: dict[str, Any]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name, payload in sorted(receipts.items()):
        path = destination / name
        if path.exists() and (not path.is_file() or path.is_symlink()):
            raise ConflictError(f"refusing non-regular receipt path: {path}")
        path.write_bytes(_json_bytes(payload))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cut", required=True, type=Path)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--license", required=True)
    parser.add_argument("--plugin-repo", required=True)
    parser.add_argument("--creators", required=True, type=Path)
    parser.add_argument("--corpus", type=Path)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _validate_options(options: argparse.Namespace) -> None:
    _validate_slug(options.domain, "domain")
    if not _VERSION_RE.fullmatch(options.version):
        raise CollectorError("version must be v<N> with N greater than zero")
    expected_repo = f"https://github.com/HolobiomicsLab/asb-skills-{options.domain}"
    if options.plugin_repo != expected_repo:
        raise CollectorError(f"plugin repository must be {expected_repo}")
    if options.license != "CC-BY-4.0":
        raise CollectorError("Decision 7 requires CC-BY-4.0")
    options.cut = options.cut.resolve()
    # Normalize spelling without following a final output symlink. Conflict
    # checks must see and reject that symlink instead of writing through it.
    options.out = Path(os.path.abspath(options.out))
    options.creators = options.creators.resolve()
    if options.corpus is not None:
        options.corpus = options.corpus.resolve()
    options.receipts = (
        Path(os.path.abspath(options.receipts))
        if options.receipts is not None
        else options.out.parent / "receipts"
    )
    try:
        options.receipts.relative_to(options.out)
    except ValueError:
        pass
    else:
        raise CollectorError("receipts directory must not be inside the candidate")


def main(argv: list[str] | None = None) -> int:
    """Run the S3 collection stage with conflict-safe deterministic writes."""
    try:
        options = _parser().parse_args(argv)
        _validate_options(options)
        outputs, receipts = _assemble(options)
        _check_receipts(options.receipts, receipts)
        identical = _check_output(options.out, outputs)
        if not options.dry_run:
            if not identical:
                _write_outputs(options.out, outputs)
            _write_receipts(options.receipts, receipts)
        print(
            json.dumps(
                {
                    "status": "identical" if identical else "collected",
                    "dry_run": options.dry_run,
                    **receipts["collect_receipt.json"]["counts"],
                },
                sort_keys=True,
            )
        )
        return 0
    except ConflictError as exc:
        print(f"CONFLICT: {exc}", file=sys.stderr)
        return 2
    except (
        CollectorError,
        OSError,
        UnicodeError,
        yaml.YAMLError,
        json.JSONDecodeError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
