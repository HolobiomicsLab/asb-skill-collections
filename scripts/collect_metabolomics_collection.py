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
      collection.yaml                 # SkillCollection record (asb-schema v0.3)
      CITATION.cff                    # Citation File Format 1.2.0
      skills/<slug>/SKILL.md          # one per deduped skill, YAML frontmatter
      tools/<slug>.yaml               # one per deduped tool

Grounding (the formats this script targets) was read from:
  * asb-schema/.../asb_skill_collection.yaml  (SkillCollection v0.3 slots)
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
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from asb_skill_collections import layout

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
    "from 17 method papers (journal articles or preprints) and their code. "
    "Each skill is deduplicated across "
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
    """Remove banned marketing substrings, matching the shared description lint.

    The collector's historical list is a stricter superset of the shared
    normalizer's list, so generated descriptions satisfy both policies.
    """
    out = desc
    for term in sorted(MARKETING_TERMS, key=len, reverse=True):
        out = re.sub(re.escape(term), "", out, flags=re.IGNORECASE)
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

def _split_description_opening(text: str) -> tuple[str, str] | None:
    """Return a canonical approved opening and its remaining source text."""
    aliases = (
        ("Apply this skill when", "Use when"),
        ("Use this skill when", "Use when"),
        ("Apply this skill", "Use when"),
    )
    for source, canonical in (*aliases, *((p, p) for p in APPROVED_PREFIXES)):
        match = re.match(rf"^{re.escape(source)}\b", text, flags=re.IGNORECASE)
        if match:
            remainder = re.sub(r"^[\s:;,.–—-]+", "", text[match.end():])
            return canonical, remainder
    return None


def _canonicalize_description_opening(text: str) -> str | None:
    """Normalize one existing opening and collapse repeated copies of it."""
    split = _split_description_opening(text)
    if split is None:
        return None
    opening, remainder = split
    nested = _split_description_opening(remainder)
    while nested is not None and nested[0] == opening:
        _, remainder = nested
        nested = _split_description_opening(remainder)
    return f"{opening} {remainder}".strip()


def _truncate_description(description: str) -> str:
    """Bound a description, preferring a real sentence or word boundary."""
    if len(description) <= MAX_LEN:
        return description.strip()
    cut = description[:MAX_LEN]
    ends = [
        match for match in re.finditer(r"[.;]", cut)
        if not re.search(r"\b(e\.g|i\.e|vs|etc|cf|Fig)\.?$", cut[:match.end()])
    ]
    if ends and ends[-1].end() >= MIN_LEN:
        return cut[:ends[-1].end()].strip()
    word_end = cut[: MAX_LEN - 1].rfind(" ")
    if word_end >= MIN_LEN:
        return cut[:word_end].rstrip(".,;:(- ") + "."
    return cut[: MAX_LEN - 1].rstrip(".,;:(- ") + "."


def _description_contexts(domain_label: str | None) -> tuple[str, str]:
    """Return workflow and analysis phrases for an optional domain label."""
    label = _strip_trailing_marketing(_collapse_ws(domain_label or ""))
    if label:
        return f"in a {label} workflow", f"in {label} analysis"
    return "in the workflow it documents", "in the analysis it documents"


#: A leading "when", "use when" or "if/when" clause opener. A source that opens
#: with one loses it before "Use when" is added, or the description reads
#: "Use when when ...".
_LEADING_WHEN_RE = re.compile(r"^(?:use\s+)?(?:if\s*/\s*when|when)\b[\s,:]*", re.IGNORECASE)


def _strip_leading_when(text: str) -> str:
    """Drop one leading when-clause opener ("When", "Use when", "If/when")."""
    return _LEADING_WHEN_RE.sub("", text, count=1)


def _use_when(text: str, bridge: str) -> str:
    """Give ``text`` one canonical opening, never a doubled "Use when"."""
    canonical = _canonicalize_description_opening(text)
    if canonical is not None:
        if not canonical.startswith("Use when"):
            return canonical
        rest = canonical[len("Use when"):].strip()
        return f"Use when {_strip_leading_when(rest)}".strip()
    stripped = _strip_leading_when(text)
    if stripped != text:
        bridge = ""
    if not stripped:
        return ""
    return f"Use when {bridge}{stripped[0].lower()}{stripped[1:]}"


def _description_from_sources(when_to_use: str, fallback_desc: str) -> str:
    """Choose the richest source and give it one canonical opening."""
    core = _strip_trailing_marketing(_collapse_ws(when_to_use))
    if core:
        return _use_when(core, "")
    fallback = _strip_trailing_marketing(_collapse_ws(fallback_desc))
    if not fallback:
        return ""
    return _use_when(fallback, "you need to ")


def _pad_description(description: str, pretty_name: str, context: str) -> str:
    """Pad a short description with neutral, documented procedure context."""
    description = _truncate_description(description)
    if len(description) >= MIN_LEN:
        return description
    subject = f"the {pretty_name} procedure" if pretty_name else "the documented procedure"
    description = (
        description.rstrip(".") + f". Applies {subject} {context} as documented."
    )
    if len(description) < MIN_LEN:
        description = description.rstrip(".") + ". Follow the documented procedure."
    return _truncate_description(description)


def _build_description(
    skill_name: str,
    when_to_use: str,
    fallback_desc: str,
    domain_label: str | None = None,
) -> str:
    """Synthesize a description accepted by the shared description lint."""
    pretty_name = _strip_trailing_marketing(
        _collapse_ws(skill_name.replace("-", " "))
    )
    workflow_context, analysis_context = _description_contexts(domain_label)
    desc = _description_from_sources(when_to_use, fallback_desc)
    if not desc:
        action = f"apply {pretty_name}" if pretty_name else "follow the procedure"
        desc = f"Use when you need to {action} {workflow_context}"
    return _pad_description(desc, pretty_name, analysis_context)


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

    # No frontmatter evidence_spans: the only spans a build dir offers per skill
    # are its tools' (tools.json), and copying the first of each tool's into
    # every leaf naming that tool grounded unrelated leaves with one sentence
    # (561 spans were each shared by more than ten v2 leaves). A leaf's own
    # verbatim evidence is in its body, which is kept whole below.

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
                # The extractor's repo claim for this tool. Folded into
                # `source_repos` below rather than published as the tool's
                # canonical home: it is a repository belonging to the paper being
                # extracted, not to the tool it cites. See issue #42.
                "extracted_repo_url": rec.get("canonical_url") or "",
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


def render_skill_md(rec: dict, domain_label: str | None = None) -> str:
    """Render one skill record with an optional collection-domain label."""
    description = _build_description(
        rec["skill_name"],
        rec["when_to_use"],
        rec["description_src"],
        domain_label=domain_label,
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
    }
    return _yaml_dump(data)


# ---------------------------------------------------------------------------
# CITATION.cff references: CFF 1.2.0 requires type, title and authors on each
# ---------------------------------------------------------------------------

#: Crossref work types -> CFF 1.2.0 reference types; anything else is "generic".
CROSSREF_CFF_TYPES = {
    "journal-article": "article",
    "posted-content": "article",
    "proceedings-article": "conference-paper",
    "book": "book",
    "monograph": "book",
    "edited-book": "edited-work",
    "reference-book": "book",
    "dataset": "data",
    "report": "report",
    "dissertation": "thesis",
    "standard": "standard",
}
#: DataCite resourceTypeGeneral -> CFF 1.2.0 reference types.
DATACITE_CFF_TYPES = {
    "JournalArticle": "article",
    "Preprint": "article",
    "Text": "article",
    "ConferencePaper": "conference-paper",
    "Software": "software",
    "Dataset": "data",
    "Report": "report",
    "Dissertation": "thesis",
    "Book": "book",
}
CROSSREF_WORKS = "https://api.crossref.org/works/"
DATACITE_DOIS = "https://api.datacite.org/dois/"
REFERENCE_USER_AGENT = (
    "asb-skill-collections/collect_metabolomics_collection "
    "(+https://github.com/HolobiomicsLab/asb-skill-collections)"
)
#: Seconds between two metadata requests, to stay well inside both APIs' limits.
REFERENCE_REQUEST_INTERVAL = 0.25


def _clean_text(value) -> str:
    """One line of text from a metadata field that may hold markup or a list."""
    if isinstance(value, list):
        value = value[0] if value else ""
    text = re.sub(r"<[^>]+>", "", str(value or ""))
    return _collapse_ws(text)


def _cff_person(given: str, family: str, name: str) -> dict | None:
    """A CFF person (family/given names) or entity (name); None when nameless."""
    given, family, name = _clean_text(given), _clean_text(family), _clean_text(name)
    if family:
        person = {"family-names": family}
        if given:
            person["given-names"] = given
        return person
    if name:
        return {"name": name}
    return None


def _complete_reference(kind: str, title: str, authors: list, doi: str,
                        year, journal: str) -> dict | None:
    """Assemble one CFF reference, or None when title or authors are missing.

    CFF requires the authors of a reference to be unique items, so a second
    entry identical to an earlier one (two co-authors who share a name and
    carry nothing else) is written once.
    """
    unique: list[dict] = []
    for author in authors:
        if author and author not in unique:
            unique.append(author)
    authors = unique
    if not title or not authors:
        return None
    reference = {"type": kind, "title": title, "authors": authors, "doi": doi}
    if isinstance(year, int):
        reference["year"] = year
    if journal and kind == "article":
        reference["journal"] = journal
    return reference


def reference_from_crossref(doi: str, work: dict) -> dict | None:
    """A complete CFF reference from a Crossref ``/works`` message, else None."""
    authors = [
        _cff_person(a.get("given", ""), a.get("family", ""), a.get("name", ""))
        for a in work.get("author") or []
        if isinstance(a, dict)
    ]
    issued = (work.get("issued") or work.get("published") or {}).get("date-parts") or [[]]
    year = issued[0][0] if issued and issued[0] and isinstance(issued[0][0], int) else None
    return _complete_reference(
        CROSSREF_CFF_TYPES.get(str(work.get("type") or ""), "generic"),
        _clean_text(work.get("title")),
        authors,
        doi,
        year,
        _clean_text(work.get("container-title")),
    )


def reference_from_datacite(doi: str, attributes: dict) -> dict | None:
    """A complete CFF reference from DataCite ``/dois`` attributes, else None."""
    authors = [
        _cff_person(c.get("givenName", ""), c.get("familyName", ""), c.get("name", ""))
        if c.get("nameType") != "Organizational"
        else _cff_person("", "", c.get("name", ""))
        for c in attributes.get("creators") or []
        if isinstance(c, dict)
    ]
    titles = [t.get("title") for t in attributes.get("titles") or [] if isinstance(t, dict)]
    general = str((attributes.get("types") or {}).get("resourceTypeGeneral") or "")
    year = attributes.get("publicationYear")
    return _complete_reference(
        DATACITE_CFF_TYPES.get(general, "generic"),
        _clean_text(titles),
        authors,
        doi,
        int(year) if str(year or "").isdigit() else None,
        "",
    )


def _get_json(url: str, opener) -> dict | None:
    """GET one JSON document; None on a 404, other HTTP errors propagate."""
    import urllib.error
    import urllib.request

    request = urllib.request.Request(
        url, headers={"User-Agent": REFERENCE_USER_AGENT, "Accept": "application/json"}
    )
    try:
        with opener(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def fetch_citation_reference(doi: str, opener=None) -> dict | None:
    """Look a DOI up in Crossref, then in DataCite (arXiv, Zenodo); read only."""
    import urllib.parse
    import urllib.request

    opener = opener or urllib.request.urlopen
    quoted = urllib.parse.quote(doi, safe="")
    work = _get_json(CROSSREF_WORKS + quoted, opener)
    if work is not None:
        return reference_from_crossref(doi, work.get("message") or {})
    record = _get_json(DATACITE_DOIS + quoted, opener)
    if record is not None:
        return reference_from_datacite(doi, (record.get("data") or {}).get("attributes") or {})
    return None


def fetch_citation_references(dois: list[str], opener=None, pause=None) -> dict[str, dict]:
    """Complete references for the DOIs both registries describe, keyed by lowercase DOI."""
    import time

    pause = REFERENCE_REQUEST_INTERVAL if pause is None else pause
    found: dict[str, dict] = {}
    for number, doi in enumerate(dois):
        if number and pause:
            time.sleep(pause)
        reference = fetch_citation_reference(doi, opener)
        if reference is not None:
            found[doi.lower()] = reference
    return found


def existing_citation_references(citation: pathlib.Path) -> dict[str, dict]:
    """The complete references an earlier CITATION.cff already carries, by lowercase DOI."""
    try:
        payload = yaml.safe_load(citation.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    out = {}
    for reference in payload.get("references") or []:
        if not isinstance(reference, dict) or not reference.get("doi"):
            continue
        complete = _complete_reference(
            str(reference.get("type") or "generic"),
            str(reference.get("title") or ""),
            list(reference.get("authors") or []),
            str(reference["doi"]),
            None,
            "",
        )
        if complete is not None:
            out[str(reference["doi"]).lower()] = reference
    return out


def citation_references(source_dois: list[str], references: dict[str, dict]) -> list[dict]:
    """The CFF references for the source DOIs that have a complete record, in DOI order.

    A DOI without a title and at least one author is left out rather than
    written as ``{type, doi}``, which fails CFF 1.2.0 validation.
    """
    return [references[d.lower()] for d in source_dois if d.lower() in references]


def render_citation_cff(
    source_dois: list[str], released_at: str, references: dict[str, dict] | None = None
) -> str:
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
    }
    complete = citation_references(source_dois, references or {})
    if complete:
        cff["references"] = complete
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
    fetch_references: bool = False,
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
                # union of DOIs, tools, edam_topics
                for d in rec["dois"]:
                    if d and d not in canonical["dois"]:
                        canonical["dois"].append(d)
                for t in rec["tools"]:
                    if t and t not in canonical["tools"]:
                        canonical["tools"].append(t)
                for t in rec["edam_topics"]:
                    if t and t not in canonical["edam_topics"]:
                        canonical["edam_topics"].append(t)

        # ---- tools ----
        for trec in extract_tools(bdir, paper_doi, paper_title, repo_url):
            key = trec["name"].strip().lower()
            if key not in tools_by_name:
                trec["_derived_from"] = []
                trec["_repos"] = set()
                tools_by_name[key] = trec
            canon = tools_by_name[key]
            # prefer a non-empty version
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
            if trec["extracted_repo_url"]:
                canon["_repos"].add(trec["extracted_repo_url"])

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
        skills_out = layout.leaf_dir(release_dir)
        tools_out = release_dir / "tools"
        if clean:
            _rmtree(skills_out)
            _rmtree(tools_out)
        skills_out.mkdir(parents=True, exist_ok=True)
        tools_out.mkdir(parents=True, exist_ok=True)

        domain_label = COLLECTION_SLUG.replace("-", " ")
        for slug in skill_slugs:
            rec = skills_by_slug[slug]
            sd = skills_out / slug
            sd.mkdir(parents=True, exist_ok=True)
            (sd / "SKILL.md").write_text(
                render_skill_md(rec, domain_label=domain_label), encoding="utf-8"
            )

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
        # References an earlier CITATION.cff already completed are reused, so a
        # re-run needs no network; --fetch-citation-references looks up the rest.
        citation = release_dir / "CITATION.cff"
        references = existing_citation_references(citation)
        if fetch_references:
            missing = [d for d in source_dois_sorted if d.lower() not in references]
            references.update(fetch_citation_references(missing))
        uncited = [d for d in source_dois_sorted if d.lower() not in references]
        if uncited:
            sys.stderr.write(
                f"NOTE: {len(uncited)} source DOIs have no title and author record and "
                "are left out of CITATION.cff references"
                + ("" if fetch_references else " (pass --fetch-citation-references)")
                + ".\n"
            )
        citation.write_text(
            render_citation_cff(source_dois_sorted, released_at, references),
            encoding="utf-8",
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
    parser.add_argument(
        "--fetch-citation-references",
        action="store_true",
        help="Look up, in Crossref then DataCite (read-only GET), the title and "
        "authors of every source DOI the existing CITATION.cff does not already "
        "reference. Without it, DOIs with no such record are left out of "
        "CITATION.cff references.",
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
        fetch_references=args.fetch_citation_references,
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
