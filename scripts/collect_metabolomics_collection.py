#!/usr/bin/env python3
"""
Assemble the 17 grounded ASB metabolomics builds into the
asb-skill-collections registry format.

This is the *assembly* step of the ASB release train: it reads the per-paper
ASB build directories produced by AgenticScienceBuilder (each a tree of
``skills/<slug>/{README.md,skill_kb.json,tools.json,papers.json,
ontology_refs.json,skill.md,...}`` + ``tools/*.json`` + ``build_manifest.json``)
and emits a single curated *collection* under
``collections/metabolomics/v1/``:

    collections/metabolomics/v1/
      collection.yaml                 # SkillCollection record (asb-schema v0.2)
      CITATION.cff                    # Citation File Format 1.2.0
      skills/<slug>/SKILL.md          # one per deduped skill, YAML frontmatter
      tools/<slug>.yaml               # one per deduped tool

Grounding (the formats this script targets) was read from:
  * asb-schema/.../asb_skill_collection.yaml  (SkillCollection v0.2 slots)
  * asb-schema/.../asb_skill_bundle.yaml      (ASBSkill.description discipline)
  * asb-skill-collections/scripts/regen_catalogue.py
        -> reads collection.yaml keys: @id|slug+version, title, version, slug,
           skills_count, tools_count, domain_topics, doi, released_at,
           lead_curators[]
  * asb-skill-collections/.github/workflows/validate.yml
        -> Gate 5 (description discipline): SKILL.md frontmatter ``description``
           MUST start with one of APPROVED_PREFIXES and be MIN_LEN..MAX_LEN chars,
           no marketing terms.
        -> Gate 6 (EDAM IRI): ``metadata.edam_operation`` + ``metadata.edam_topics``
           must be full ``http://edamontology.org/...`` IRIs.
        -> Gate 2 (orphan): frontmatter ``derived_from`` carries source DOIs.

Source-tool / DOI mapping comes from
``asb-corpus-metabolomics/batch_metabolomics_v0.json`` — each build dir is matched
to its corpus tool by name/slug, and the *authoritative* DOI + repo_url are taken
from the corpus (build sidecars carry stale/missing DOIs for some builds, e.g.
``coll_commit``).

Dependencies: Python 3.8+ stdlib + PyYAML only.

Idempotent: re-running overwrites the generated tree deterministically (sorted
keys, stable ordering). Pass ``--clean`` to remove ``skills/`` and ``tools/``
under the release dir before writing (drops skills/tools that disappeared from
the inputs).

Usage:
    python scripts/collect_metabolomics_collection.py \
        --builds-root /Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot \
        --corpus /Users/nothiasl/git/asb-corpus-metabolomics/batch_metabolomics_v0.json \
        --repo-root . \
        [--clean] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "ERROR: PyYAML is required. Install with `pip install pyyaml` "
        "(or run inside the agentic-science-builder conda env).\n"
    )
    raise

# ---------------------------------------------------------------------------
# Constants — grounded in the read schema / CI gates
# ---------------------------------------------------------------------------

COLLECTION_SLUG = "metabolomics"
COLLECTION_VERSION = 1
COLLECTION_IRI = (
    "https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1"
)
COLLECTION_TITLE = "ASB Metabolomics Skill Collection v1"
COLLECTION_DESCRIPTION = (
    "Curated, evidence-grounded skills and software-tool records for "
    "computational metabolomics and adjacent mass-spectrometry / NMR / "
    "multi-omics analysis, assembled by the AgenticScienceBuilder pipeline "
    "from 17 peer-reviewed method papers. Each skill is deduplicated across "
    "papers, anchored to verbatim evidence spans, and annotated with EDAM "
    "operation/topic IRIs for retrieval."
)
COLLECTION_LICENSE = "CC-BY-4.0"
COLLECTION_DOI = "TODO-zenodo"  # minted at release time

LEAD_CURATORS = [
    {
        "name": "Louis-Felix Nothias",
        "orcid": "0000-0001-6711-6719",
        "github": "lfnothias",
    }
]
REGISTRY_ROOT_IRI = "https://w3id.org/holobiomicslab/asb-skill/registry"

# Gate 5 (validate.yml) — keep in sync with .github/workflows/validate.yml.
APPROVED_PREFIXES = ("Use when", "Reference for", "Explains", "Decision support for")
MIN_LEN = 50
MAX_LEN = 300
MARKETING_TERMS = [
    "best",
    "state-of-the-art",
    "revolutionary",
    "leading",
    "superior",
    "cutting-edge",
    "best-in-class",
    "powerful",
    "amazing",
    "groundbreaking",
    "world-class",
    "unparalleled",
]

EDAM_BASE = "http://edamontology.org/"

# The 17 build directories under --builds-root (spec2vec_grounded + coll_*).
# The grounded spec2vec build lives under a non-coll_ name.
SPECIAL_BUILD_DIRS = ["spec2vec_grounded"]

# Hand-verified slug aliases: build-dir slug -> normalized corpus key.
# (build dir name -> corpus 'name' normalized to [a-z0-9]). Covers cases where
# the dir slug does not directly normalize to the corpus name.
CORPUS_NAME_ALIASES = {
    "13c_spacem": "13cspacem",
    "chemprop_ir": "chempropir",
    "np_analyst": "npanalyst",
    "opentims": "opentimstimspyandtimsr",
}


# ---------------------------------------------------------------------------
# Small IO / text helpers
# ---------------------------------------------------------------------------

def _load_json(path: pathlib.Path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s or "unknown"


def _collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _strip_trailing_marketing(desc: str) -> str:
    """Remove banned marketing tokens (case-insensitive, whole words)."""
    out = desc
    for term in MARKETING_TERMS:
        out = re.sub(rf"\b{re.escape(term)}\b", "", out, flags=re.IGNORECASE)
    return _collapse_ws(out)


def _edam_curie_to_iri(term: str) -> str | None:
    """Convert 'EDAM:topic_3172' or a bare 'topic_3172' to a full EDAM IRI.

    Already-full IRIs are returned unchanged. Returns None if unrecognizable.
    """
    if not term:
        return None
    term = term.strip()
    if term.startswith(EDAM_BASE):
        return term
    if term.startswith("EDAM:"):
        return EDAM_BASE + term[len("EDAM:"):]
    if re.match(r"^(operation|topic|data|format)_\d+$", term):
        return EDAM_BASE + term
    return None


# ---------------------------------------------------------------------------
# Frontmatter parsing for the source build skill.md files
# ---------------------------------------------------------------------------

def _read_skill_md_frontmatter(skill_md: pathlib.Path) -> dict:
    """Return the YAML frontmatter of an ASB build skill.md (or {})."""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return fm if isinstance(fm, dict) else {}


def _read_skill_md_section(skill_md: pathlib.Path, header: str) -> str:
    """Return the body text under a '## <header>' section of the skill.md body."""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return ""
    # Strip frontmatter before scanning headers.
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    lines = text.splitlines()
    target = header.strip().lower()
    out: list[str] = []
    capture = False
    for line in lines:
        if line.lstrip().startswith("## "):
            current = line.lstrip()[3:].strip().lower()
            if capture:
                break
            capture = current == target
            continue
        if capture:
            out.append(line)
    return _collapse_ws("\n".join(out))


# ---------------------------------------------------------------------------
# Description synthesis — must satisfy Gate 5
# ---------------------------------------------------------------------------

def _build_description(skill_name: str, when_to_use: str, fallback_desc: str) -> str:
    """Synthesize a Gate-5-compliant 'Use when ...' description.

    Strategy (richest-first):
      1. If a '## When to use' body section exists, phrase it as 'Use when ...'.
      2. Else derive from the skill's index/frontmatter description.
      3. Truncate to MAX_LEN at a sentence/word boundary; pad to MIN_LEN.
    """
    pretty_name = _collapse_ws(skill_name.replace("-", " "))

    core = _collapse_ws(when_to_use)
    # Turn an "Apply this skill when you ... " phrasing into a "Use when ..." one.
    core = re.sub(r"^apply this skill when\b", "", core, flags=re.IGNORECASE).strip()
    core = re.sub(r"^use this skill when\b", "", core, flags=re.IGNORECASE).strip()
    core = re.sub(r"^apply this skill\b", "", core, flags=re.IGNORECASE).strip()

    if core:
        desc = f"Use when {core[0].lower()}{core[1:]}" if core else ""
    else:
        fb = _collapse_ws(fallback_desc)
        if fb:
            desc = f"Use when you need to {fb[0].lower()}{fb[1:]}"
        else:
            desc = f"Use when you need to apply {pretty_name} in a metabolomics workflow"

    desc = _strip_trailing_marketing(desc)

    # Ensure approved prefix (defensive; the above always yields "Use when").
    if not any(desc.startswith(p) for p in APPROVED_PREFIXES):
        desc = "Use when " + desc[0].lower() + desc[1:] if desc else (
            f"Use when applying {pretty_name}"
        )

    # Enforce MAX_LEN at a sentence then word boundary.
    if len(desc) > MAX_LEN:
        cut = desc[: MAX_LEN]
        # prefer last *real* sentence end (avoid cutting right after e.g./i.e./vs.)
        ends = [
            m
            for m in re.finditer(r"[.;]", cut)
            if not re.search(r"\b(e\.g|i\.e|vs|etc|cf|Fig)\.?$", cut[: m.start() + 1])
        ]
        if ends and ends[-1].end() >= MIN_LEN:
            desc = cut[: ends[-1].end()]
        else:
            desc = cut.rsplit(" ", 1)[0].rstrip(",;:(- ") + "."
    desc = desc.strip()

    # Enforce MIN_LEN by appending a grounded clause.
    if len(desc) < MIN_LEN:
        pad = f" Applies the {pretty_name} procedure in metabolomics analysis."
        desc = (desc.rstrip(".") + ".").strip()
        if len(desc) < MIN_LEN:
            desc = (desc + pad).strip()
        # last resort hard pad (kept descriptive, never marketing)
        while len(desc) < MIN_LEN:
            desc = desc.rstrip(".") + " in a reproducible metabolomics pipeline."
    if len(desc) > MAX_LEN:
        desc = desc[: MAX_LEN].rsplit(" ", 1)[0].rstrip(",;: ") + "."
    return desc


# ---------------------------------------------------------------------------
# Loading the build corpus mapping
# ---------------------------------------------------------------------------

def load_corpus_index(corpus_path: pathlib.Path) -> dict:
    """name-normalized corpus tool index: {norm_name: corpus_entry}."""
    data = _load_json(corpus_path)
    if not isinstance(data, list):
        raise ValueError(f"corpus {corpus_path} is not a JSON list")
    return {_norm_name(c.get("name", "")): c for c in data}


def resolve_build_to_corpus(build_dir_name: str, corpus_index: dict) -> dict | None:
    """Map a build dir name to its corpus entry (DOI + repo_url authority)."""
    slug = (
        build_dir_name[len("coll_"):]
        if build_dir_name.startswith("coll_")
        else build_dir_name.replace("_grounded", "")
    )
    key = CORPUS_NAME_ALIASES.get(slug, _norm_name(slug))
    if key in corpus_index:
        return corpus_index[key]
    # prefix fallback
    for ck, entry in corpus_index.items():
        if ck.startswith(key) or key.startswith(ck):
            return entry
    return None


def discover_build_dirs(builds_root: pathlib.Path) -> list[pathlib.Path]:
    dirs: list[pathlib.Path] = []
    for special in SPECIAL_BUILD_DIRS:
        p = builds_root / special
        if (p / "skills").is_dir():
            dirs.append(p)
    for p in sorted(builds_root.glob("coll_*")):
        if (p / "skills").is_dir():
            dirs.append(p)
    return dirs


# ---------------------------------------------------------------------------
# Per-skill richness scoring (to pick the canonical record on dedup)
# ---------------------------------------------------------------------------

def _skill_richness(rec: dict) -> tuple:
    """Sort key: larger == richer. Used to pick the canonical dup."""
    return (
        len(rec.get("evidence_spans", [])),
        len(rec.get("tools", [])),
        len(rec.get("edam_topics", [])),
        1 if rec.get("edam_operation") else 0,
        len(rec.get("skill_md_body") or ""),
        len(rec.get("description_src") or ""),
    )


# ---------------------------------------------------------------------------
# Extract one skill record from a build dir
# ---------------------------------------------------------------------------

def extract_skill(
    skill_dir: pathlib.Path,
    build_name: str,
    paper_doi: str,
    paper_title: str,
    repo_url: str,
) -> dict | None:
    slug = skill_dir.name
    if slug.startswith("_") or slug.startswith("."):
        return None

    fm = _read_skill_md_frontmatter(skill_dir / "skill.md")
    kb = _load_json(skill_dir / "skill_kb.json") or {}
    papers = _load_json(skill_dir / "papers.json") or []
    tools_doc = _load_json(skill_dir / "tools.json") or {}
    onto = _load_json(skill_dir / "ontology_refs.json") or []

    # ---- name + description source ----
    skill_name = fm.get("name") or slug
    fallback_desc = _collapse_ws(fm.get("description") or "")
    when_to_use = _read_skill_md_section(skill_dir / "skill.md", "When to use")

    # ---- EDAM operation + topics (prefer frontmatter full IRIs) ----
    edam_operation = None
    op = fm.get("edam_operation")
    if isinstance(op, str):
        edam_operation = _edam_curie_to_iri(op)
    edam_topics: list[str] = []
    for t in fm.get("edam_topics") or []:
        iri = _edam_curie_to_iri(t)
        if iri and iri not in edam_topics:
            edam_topics.append(iri)
    # Backfill from ontology_refs.json (CURIE form) if frontmatter was sparse.
    for ref in onto:
        if not isinstance(ref, dict):
            continue
        iri = _edam_curie_to_iri(ref.get("term_id", ""))
        if not iri:
            continue
        if "/operation_" in iri:
            edam_operation = edam_operation or iri
        elif "/topic_" in iri and iri not in edam_topics:
            edam_topics.append(iri)

    # ---- tools attached to this skill ----
    tool_names: list[str] = []
    for t in (tools_doc.get("tools") if isinstance(tools_doc, dict) else tools_doc) or []:
        if isinstance(t, dict):
            nm = t.get("name") or t.get("slug")
            if nm and nm not in tool_names:
                tool_names.append(nm)
    # also frontmatter tools[]
    for t in fm.get("tools") or []:
        if isinstance(t, dict):
            nm = t.get("name")
            if nm and nm not in tool_names:
                tool_names.append(nm)

    # ---- DOIs / evidence ----
    dois: list[str] = []
    if paper_doi:
        dois.append(paper_doi)
    for p in papers:
        if isinstance(p, dict) and p.get("doi") and p["doi"] not in dois:
            # keep build-local DOIs too, but corpus DOI stays first/authoritative
            dois.append(p["doi"])

    evidence_spans: list[str] = []
    tools_in_skill = tools_doc.get("tools") if isinstance(tools_doc, dict) else None
    for t in tools_in_skill or []:
        for span in (t.get("evidence_spans") or [])[:2]:
            span = _collapse_ws(span)
            if span and span not in evidence_spans:
                evidence_spans.append(span)
    evidence_spans = evidence_spans[:6]

    skill_md_body = ""
    try:
        skill_md_body = (skill_dir / "skill.md").read_text(encoding="utf-8")
    except OSError:
        pass

    return {
        "slug": slug,
        "skill_name": skill_name,
        "description_src": fallback_desc,
        "when_to_use": when_to_use,
        "edam_operation": edam_operation,
        "edam_topics": edam_topics,
        "tools": tool_names,
        "dois": dois,
        "primary_doi": paper_doi or (dois[0] if dois else ""),
        "primary_title": paper_title,
        "repo_url": repo_url,
        "evidence_spans": evidence_spans,
        "skill_md_body": skill_md_body,
        "source_build": build_name,
        "kb_notes": kb.get("notes") if isinstance(kb, dict) else None,
    }


# ---------------------------------------------------------------------------
# Extract tool records from a build dir (collection-level tools/_index.json)
# ---------------------------------------------------------------------------

def extract_tools(
    build_dir: pathlib.Path,
    paper_doi: str,
    paper_title: str,
    repo_url: str,
) -> list[dict]:
    out: list[dict] = []
    idx = _load_json(build_dir / "tools" / "_index.json")
    records = []
    if isinstance(idx, dict) and isinstance(idx.get("records"), list):
        records = idx["records"]
    else:
        # fall back to individual tools/*.json
        for tf in sorted((build_dir / "tools").glob("*.json")):
            if tf.name == "_index.json":
                continue
            rec = _load_json(tf)
            if isinstance(rec, dict):
                records.append(rec)

    for rec in records:
        if not isinstance(rec, dict):
            continue
        name = rec.get("name") or rec.get("tool_name") or rec.get("slug")
        if not name:
            continue
        evidence = [
            _collapse_ws(s) for s in (rec.get("evidence_spans") or [])[:3] if s
        ]
        edam_topics: list[str] = []
        for t in rec.get("edam_topics") or []:
            iri = _edam_curie_to_iri(t if isinstance(t, str) else "")
            if iri and iri not in edam_topics:
                edam_topics.append(iri)
        out.append(
            {
                "name": name,
                "slug": rec.get("slug") or _slugify(name),
                "canonical_url": rec.get("canonical_url") or "",
                "version_used": rec.get("version_used") or "",
                "edam_topics": edam_topics,
                "evidence_spans": evidence,
                "source_paper_doi": rec.get("source_paper_doi") or paper_doi,
                "source_paper_title": rec.get("source_paper_title") or paper_title,
                "source_repo_url": repo_url,
            }
        )
    return out


# ---------------------------------------------------------------------------
# Emission — SKILL.md, tools/*.yaml, collection.yaml, CITATION.cff
# ---------------------------------------------------------------------------

def _yaml_dump(data: dict) -> str:
    return yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
    )


def render_skill_md(rec: dict) -> str:
    description = _build_description(
        rec["skill_name"], rec["when_to_use"], rec["description_src"]
    )
    derived_from = [
        {"doi": d, "title": rec["primary_title"] if d == rec["primary_doi"] else ""}
        for d in rec["dois"]
    ] or [{"doi": rec["primary_doi"], "title": rec["primary_title"]}]
    # provenance: every source build that contributed this slug
    provenance_sources = [
        {
            "build": s["source_build"],
            "doi": s["primary_doi"],
            "title": s["primary_title"],
        }
        for s in rec["_all_sources"]
    ]

    frontmatter = {
        "name": rec["slug"],
        "description": description,
        "license": COLLECTION_LICENSE,
        "metadata": {
            "edam_operation": rec["edam_operation"] or "",
            "edam_topics": rec["edam_topics"],
            "tools": rec["tools"],
        },
        "derived_from": derived_from,
        "evidence_spans": rec["evidence_spans"],
        "claims": [],
        "provenance": {
            "collection": COLLECTION_IRI,
            "assembled_by": "scripts/collect_metabolomics_collection.py",
            "sources": provenance_sources,
            "dedup_kept_from": rec["source_build"],
        },
        "schema_version": "0.2.0",
    }
    # drop empty optional metadata keys for cleanliness (but keep edam_topics list)
    if not frontmatter["metadata"]["edam_operation"]:
        frontmatter["metadata"].pop("edam_operation")

    fm_yaml = _yaml_dump(frontmatter).rstrip("\n")

    # Body: reuse the richest source skill.md body (strip its own frontmatter),
    # else synthesize a minimal body.
    body = rec.get("skill_md_body") or ""
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2] if len(parts) >= 3 else body
    body = body.strip()
    if not body:
        pretty = _collapse_ws(rec["skill_name"].replace("-", " "))
        body = f"# {pretty}\n\n{description}\n"

    return f"---\n{fm_yaml}\n---\n\n{body}\n"


def render_tool_yaml(rec: dict) -> str:
    data = {
        "name": rec["name"],
        "slug": rec["slug"],
        "canonical_url": rec["canonical_url"],
        "version_used": rec["version_used"],
        "edam_topics": rec["edam_topics"],
        "evidence_spans": rec["evidence_spans"],
        "derived_from": [
            {"doi": d.get("doi", ""), "title": d.get("title", "")}
            for d in rec["_derived_from"]
        ],
        "source_repos": sorted(rec["_repos"]),
        "schema_version": "0.2.0",
    }
    # prune empties
    data = {k: v for k, v in data.items() if v not in ("", [], None)}
    return _yaml_dump(data)


def render_collection_yaml(
    skill_slugs: list[str],
    tool_slugs: list[str],
    edam_topics: list[str],
    source_dois: list[str],
    released_at: str,
) -> str:
    # We emit BOTH the schema slot name (edam_topics) and the name that
    # regen_catalogue.py actually reads (domain_topics), so the catalogue
    # generator picks them up unchanged while the LinkML schema stays valid.
    data = {
        "@context": {
            "@vocab": "https://schema.org/",
            "asb": "https://w3id.org/holobiomicslab/asb-skill/",
            "edam": "http://edamontology.org/",
        },
        "@type": "asb:SkillCollection",
        "@id": COLLECTION_IRI,
        "iri": COLLECTION_IRI,
        "title": COLLECTION_TITLE,
        "slug": COLLECTION_SLUG,
        "version": COLLECTION_VERSION,
        "description": COLLECTION_DESCRIPTION,
        "license": COLLECTION_LICENSE,
        "doi": COLLECTION_DOI,
        "released_at": released_at,
        "lead_curators": LEAD_CURATORS,
        "contributors": [
            {"name": c["name"], "orcid": f"https://orcid.org/{c['orcid']}"}
            for c in LEAD_CURATORS
        ],
        "skills_count": len(skill_slugs),
        "tools_count": len(tool_slugs),
        "skills": skill_slugs,
        "tools": tool_slugs,
        "edam_topics": edam_topics,
        "domain_topics": edam_topics,
        "source_collections": source_dois,
        "catalogue_membership": [REGISTRY_ROOT_IRI],
        "ro_crate_path": "ro-crate-metadata.json",
    }
    return _yaml_dump(data)


def render_citation_cff(source_dois: list[str], released_at: str) -> str:
    cff = {
        "cff-version": "1.2.0",
        "message": "If you use this collection, please cite it as below.",
        "title": COLLECTION_TITLE,
        "abstract": COLLECTION_DESCRIPTION,
        "version": str(COLLECTION_VERSION),
        "date-released": released_at[:10],
        "license": COLLECTION_LICENSE,
        "url": COLLECTION_IRI,
        "doi": COLLECTION_DOI,
        "type": "dataset",
        "authors": [
            {
                "family-names": "Nothias",
                "given-names": "Louis-Felix",
                "orcid": "https://orcid.org/0000-0001-6711-6719",
            },
            # TODO: add the remaining curators / contributors here.
            {
                "family-names": "TODO",
                "given-names": "Add-co-curators",
            },
        ],
        "keywords": [
            "metabolomics",
            "mass spectrometry",
            "scientific agents",
            "skills",
            "EDAM",
        ],
        "references": [
            {"type": "article", "doi": doi} for doi in source_dois
        ],
    }
    return _yaml_dump(cff)


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def assemble(
    builds_root: pathlib.Path,
    corpus_path: pathlib.Path,
    repo_root: pathlib.Path,
    clean: bool,
    dry_run: bool,
    exclude_dois: set[str] | None = None,
) -> dict:
    corpus_index = load_corpus_index(corpus_path)
    build_dirs = discover_build_dirs(builds_root)
    # DOIs whose builds are held out of this release (e.g. non-OA / restricted
    # reuse licences per OPEN_ACCESS_POLICY.md).  Normalised, case-insensitive.
    exclude_dois = {d.strip().lower() for d in (exclude_dois or set()) if d.strip()}
    excluded_builds: list[tuple[str, str]] = []

    release_dir = repo_root / "collections" / COLLECTION_SLUG / f"v{COLLECTION_VERSION}"

    # ---- gather per-skill records, keyed by slug, keeping all sources ----
    skills_by_slug: dict[str, dict] = {}
    # tools keyed by lowercase tool name (dedup by name)
    tools_by_name: dict[str, dict] = {}
    source_dois: list[str] = []
    build_report: list[tuple[str, str, int]] = []

    for bdir in build_dirs:
        bname = bdir.name
        corpus_entry = resolve_build_to_corpus(bname, corpus_index)
        if corpus_entry is None:
            sys.stderr.write(
                f"WARNING: build '{bname}' did not match any corpus tool; "
                f"skipping DOI grounding for it.\n"
            )
            paper_doi, paper_title, repo_url = "", "", ""
        else:
            paper_doi = corpus_entry.get("doi", "") or ""
            paper_title = corpus_entry.get("name", "") or ""
            repo_url = corpus_entry.get("repo_url", "") or ""
        if paper_doi and paper_doi.strip().lower() in exclude_dois:
            excluded_builds.append((bname, paper_doi))
            sys.stderr.write(
                f"EXCLUDED: build '{bname}' (DOI {paper_doi}) held out of release "
                "per --exclude-doi (non-OA / restricted reuse).\n"
            )
            continue
        if paper_doi and paper_doi not in source_dois:
            source_dois.append(paper_doi)

        # ---- skills ----
        skills_dir = bdir / "skills"
        n_skills_here = 0
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            rec = extract_skill(
                skill_dir, bname, paper_doi, paper_title, repo_url
            )
            if rec is None:
                continue
            n_skills_here += 1
            slug = rec["slug"]
            if slug not in skills_by_slug:
                rec["_all_sources"] = [rec]
                skills_by_slug[slug] = rec
            else:
                existing = skills_by_slug[slug]
                existing["_all_sources"].append(rec)
                # keep the richest as canonical, merge provenance/evidence/dois
                if _skill_richness(rec) > _skill_richness(existing):
                    rec["_all_sources"] = existing["_all_sources"]
                    skills_by_slug[slug] = rec
                    canonical = rec
                else:
                    canonical = existing
                # union of DOIs, tools, evidence, edam_topics
                for d in rec["dois"]:
                    if d and d not in canonical["dois"]:
                        canonical["dois"].append(d)
                for t in rec["tools"]:
                    if t and t not in canonical["tools"]:
                        canonical["tools"].append(t)
                for e in rec["evidence_spans"]:
                    if e and e not in canonical["evidence_spans"]:
                        canonical["evidence_spans"].append(e)
                for t in rec["edam_topics"]:
                    if t and t not in canonical["edam_topics"]:
                        canonical["edam_topics"].append(t)
                canonical["evidence_spans"] = canonical["evidence_spans"][:6]

        # ---- tools ----
        for trec in extract_tools(bdir, paper_doi, paper_title, repo_url):
            key = trec["name"].strip().lower()
            if key not in tools_by_name:
                trec["_derived_from"] = []
                trec["_repos"] = set()
                tools_by_name[key] = trec
            canon = tools_by_name[key]
            # prefer a non-empty canonical_url / version
            if not canon["canonical_url"] and trec["canonical_url"]:
                canon["canonical_url"] = trec["canonical_url"]
            if not canon["version_used"] and trec["version_used"]:
                canon["version_used"] = trec["version_used"]
            for t in trec["edam_topics"]:
                if t not in canon["edam_topics"]:
                    canon["edam_topics"].append(t)
            for e in trec["evidence_spans"]:
                if e and e not in canon["evidence_spans"]:
                    canon["evidence_spans"].append(e)
            canon["evidence_spans"] = canon["evidence_spans"][:6]
            if trec["source_paper_doi"]:
                df = {
                    "doi": trec["source_paper_doi"],
                    "title": trec["source_paper_title"],
                }
                if df not in canon["_derived_from"]:
                    canon["_derived_from"].append(df)
            if trec["source_repo_url"]:
                canon["_repos"].add(trec["source_repo_url"])
            if trec["canonical_url"]:
                canon["_repos"].add(trec["canonical_url"])

        build_report.append((bname, paper_doi, n_skills_here))

    # ---- aggregate collection-level edam topics ----
    coll_edam_topics: list[str] = []
    for rec in skills_by_slug.values():
        for t in rec["edam_topics"]:
            if t not in coll_edam_topics:
                coll_edam_topics.append(t)
    coll_edam_topics.sort()
    source_dois_sorted = sorted(source_dois)

    skill_slugs = sorted(skills_by_slug.keys())
    tool_slugs = sorted({t["slug"] for t in tools_by_name.values()})

    # Idempotency: reuse the prior released_at if a collection.yaml already
    # exists, so re-running does not churn the only volatile field.
    released_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    existing_coll = release_dir / "collection.yaml"
    if existing_coll.is_file():
        try:
            prev = yaml.safe_load(existing_coll.read_text(encoding="utf-8")) or {}
            if prev.get("released_at"):
                released_at = str(prev["released_at"])
        except (yaml.YAMLError, OSError):
            pass

    # ---- write outputs ----
    n_dups = sum(len(r["_all_sources"]) - 1 for r in skills_by_slug.values())

    if not dry_run:
        skills_out = release_dir / "skills"
        tools_out = release_dir / "tools"
        if clean:
            _rmtree(skills_out)
            _rmtree(tools_out)
        skills_out.mkdir(parents=True, exist_ok=True)
        tools_out.mkdir(parents=True, exist_ok=True)

        for slug in skill_slugs:
            rec = skills_by_slug[slug]
            sd = skills_out / slug
            sd.mkdir(parents=True, exist_ok=True)
            (sd / "SKILL.md").write_text(render_skill_md(rec), encoding="utf-8")

        for tname in sorted(tools_by_name.keys()):
            trec = tools_by_name[tname]
            (tools_out / f"{trec['slug']}.yaml").write_text(
                render_tool_yaml(trec), encoding="utf-8"
            )

        (release_dir / "collection.yaml").write_text(
            render_collection_yaml(
                skill_slugs,
                tool_slugs,
                coll_edam_topics,
                source_dois_sorted,
                released_at,
            ),
            encoding="utf-8",
        )
        (release_dir / "CITATION.cff").write_text(
            render_citation_cff(source_dois_sorted, released_at), encoding="utf-8"
        )

    return {
        "release_dir": release_dir,
        "n_builds": len(build_dirs) - len(excluded_builds),
        "n_builds_discovered": len(build_dirs),
        "n_skills": len(skill_slugs),
        "n_skill_dups": n_dups,
        "n_tools": len(tool_slugs),
        "n_dois": len(source_dois_sorted),
        "n_edam_topics": len(coll_edam_topics),
        "build_report": build_report,
        "excluded_builds": excluded_builds,
        "dry_run": dry_run,
    }


def _rmtree(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            child.rmdir()
    path.rmdir()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    global COLLECTION_SLUG, COLLECTION_VERSION, COLLECTION_IRI, COLLECTION_TITLE
    global COLLECTION_DESCRIPTION, SPECIAL_BUILD_DIRS, CORPUS_NAME_ALIASES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--builds-root",
        default="/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot",
        help="Directory containing the 17 ASB build dirs (spec2vec_grounded + coll_*).",
    )
    parser.add_argument(
        "--corpus",
        default="/Users/nothiasl/git/asb-corpus-metabolomics/batch_metabolomics_v0.json",
        help="batch_metabolomics_v0.json (source-tool -> DOI/repo authority).",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="asb-skill-collections repo root (output written under "
        "collections/metabolomics/v1/).",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing skills/ and tools/ under the release dir first.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and log the summary without writing any files.",
    )
    parser.add_argument(
        "--exclude-doi",
        action="append",
        default=[],
        metavar="DOI",
        help="Hold a paper's build out of this release (non-OA / restricted reuse "
        "per OPEN_ACCESS_POLICY.md).  Repeatable.",
    )
    # Domain parametrization — defaults reproduce the metabolomics collection;
    # override to assemble epigenomics / transcriptomics / any domain.
    parser.add_argument("--collection-slug", default=COLLECTION_SLUG,
                        help="Collection slug (default: metabolomics).")
    parser.add_argument("--collection-version", type=int, default=COLLECTION_VERSION,
                        help="Collection version integer (default: 1).")
    parser.add_argument("--collection-title", default=None,
                        help="Human title (default: 'ASB <Slug> Skill Collection v<N>').")
    parser.add_argument("--collection-description", default=None,
                        help="Collection description (default: a generic per-domain blurb).")
    args = parser.parse_args()

    # Resolve domain-specific module globals from CLI (functions read them lazily).
    COLLECTION_SLUG = args.collection_slug
    COLLECTION_VERSION = args.collection_version
    COLLECTION_IRI = (
        f"https://w3id.org/holobiomicslab/asb-skill/collection/"
        f"{COLLECTION_SLUG}/v{COLLECTION_VERSION}"
    )
    COLLECTION_TITLE = args.collection_title or (
        f"ASB {COLLECTION_SLUG.capitalize()} Skill Collection v{COLLECTION_VERSION}"
    )
    COLLECTION_DESCRIPTION = args.collection_description or (
        f"Curated, evidence-grounded skills and software-tool records for "
        f"computational {COLLECTION_SLUG}, assembled by the AgenticScienceBuilder "
        f"pipeline from open-access method papers. Each skill is deduplicated across "
        f"papers, anchored to verbatim evidence spans, and annotated with EDAM IRIs."
    )
    if COLLECTION_SLUG != "metabolomics":
        # metabolomics-build-specific aliasing does not apply to other domains;
        # their build dirs are coll_<slug> matching corpus name <slug> directly.
        SPECIAL_BUILD_DIRS = []
        CORPUS_NAME_ALIASES = {}

    builds_root = pathlib.Path(args.builds_root).expanduser().resolve()
    corpus_path = pathlib.Path(args.corpus).expanduser().resolve()
    repo_root = pathlib.Path(args.repo_root).expanduser().resolve()

    if not builds_root.is_dir():
        sys.exit(f"ERROR: builds-root not found: {builds_root}")
    if not corpus_path.is_file():
        sys.exit(f"ERROR: corpus not found: {corpus_path}")

    summary = assemble(
        builds_root=builds_root,
        corpus_path=corpus_path,
        repo_root=repo_root,
        clean=args.clean,
        dry_run=args.dry_run,
        exclude_dois=set(args.exclude_doi),
    )

    # ---- log summary ----
    print("=" * 64)
    print("ASB metabolomics collection assembly" + (" (DRY RUN)" if summary["dry_run"] else ""))
    print("=" * 64)
    print(f"builds consumed   : {summary['n_builds']}")
    print(f"skills written    : {summary['n_skills']}")
    print(f"skill duplicates  : {summary['n_skill_dups']} (merged into canonical slugs)")
    print(f"tools written     : {summary['n_tools']} (deduped by tool name)")
    print(f"source DOIs        : {summary['n_dois']}")
    print(f"collection EDAM    : {summary['n_edam_topics']} unique topic IRIs")
    print(f"output dir         : {summary['release_dir']}")
    print("-" * 64)
    print("per-build skill counts:")
    for bname, doi, n in summary["build_report"]:
        print(f"  {bname:24s} doi={doi or '<none>':32s} skills={n}")
    print("=" * 64)
    if summary["dry_run"]:
        print("DRY RUN — no files written. Re-run without --dry-run to emit.")


if __name__ == "__main__":
    main()
