#!/usr/bin/env python3
"""build_grounding_bundle — emit self-contained grounding artifacts into a unit
(a per-technique pack or the full collection): filtered+enriched kb_bundle.json,
vendored perspicacite_kb_bind.py, /ground command, GROUNDING.md."""
from __future__ import annotations
import argparse
import json
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def resolve_repo_urls(skill_dois, corpus_papers, tools_index):
    doi_set = {d for d in skill_dois}
    out = []
    by_doi = {p.get("doi"): p for p in corpus_papers}
    for d in skill_dois:
        url = (by_doi.get(d) or {}).get("repo_url")
        if url and url not in out:
            out.append(url)
    for t in tools_index:
        if doi_set.intersection(t.get("dois") or []):
            url = t.get("canonical_url")
            if url and url not in out:
                out.append(url)
    return out


def filter_and_enrich_bundle(full_bundle, skill_slugs, corpus_papers, tools_index):
    src = full_bundle.get("skills") or {}
    kept = {}
    dois = set()
    for slug in sorted(skill_slugs):
        rec = src.get(slug)
        if rec is None:
            continue
        rec = dict(rec)
        rec["repo_urls"] = resolve_repo_urls(rec.get("dois") or [], corpus_papers, tools_index)
        kept[slug] = rec
        dois.update(rec.get("dois") or [])
    out = {k: full_bundle[k] for k in ("collection", "version", "perspicacite_kb_mode", "kb_prefix") if k in full_bundle}
    out["distinct_dois"] = sorted(dois)
    out["skills"] = kept
    return out


GROUND_COMMAND = '''---
description: Ground the ASB skill in play against its source paper/repo (Perspicacité KB, with a serverless local-clone fallback).
argument-hint: "[skill-slug-or-doi] [question]"
---
You are grounding an ASB skill against the evidence it was distilled from.

Steps:
1. Identify the target skill: use the argument if given, else the skill most recently applied in this conversation. Read its record in this plugin's `kb_bundle.json` (`dois`, `kb_slugs`, `repo_urls`).
2. If a Perspicacité server is reachable at $PERSPICACITE_BASE (default http://127.0.0.1:8000), ground via its KB (auto-creates + ingests on first use):
   `python "<plugin>/bin/perspicacite_kb_bind.py" query --collection "<plugin>" --skill <slug> --question "<question>"`
3. Otherwise fall back to serverless local grounding (clones the source repo, best-effort fetches the OA paper), then read the fetched files:
   `python "<plugin>/bin/perspicacite_kb_bind.py" local --collection "<plugin>" --skill <slug> --paper`
4. Answer the user's question grounded in what you retrieved; cite the KB/repo/paper. If neither backend yields a source, say so and proceed ungrounded.

Arguments: $ARGUMENTS
'''


def render_ground_command():
    return GROUND_COMMAND


def render_grounding_doc(unit_name):
    return (
        f"# Grounding — {unit_name}\n\n"
        "Every skill here is distilled from one peer-reviewed paper (`derived_from` DOI in its "
        "SKILL.md frontmatter). Grounding is **optional** — skills work without it.\n\n"
        "Two backends (KB-primary, local fallback):\n\n"
        "- **kb (Perspicacité):** RAG over full text + SI, persistent, citable. Needs a server at "
        "`PERSPICACITE_BASE` (default http://127.0.0.1:8000). First use auto-creates + ingests the "
        "`asb-paper-<doi>` KB.\n"
        "- **local (serverless):** `git clone` the source repo + best-effort OA paper fetch; read files "
        "directly. No server.\n\n"
        "Use `/ground [skill|doi] [question]`, or call `bin/perspicacite_kb_bind.py` "
        "(`query` / `local`) directly.\n"
    )


_SUFFIX = " Packaged auto-grounding (kb+local)."


def _read_corpus(collection_dir):
    p = collection_dir / "corpus.yaml"
    return (yaml.safe_load(p.read_text())["papers"]) if p.is_file() and yaml else []

def _read_tools(collection_dir):
    p = collection_dir / "tools_index.json"
    return json.loads(p.read_text()) if p.is_file() else []


def build_unit(unit_dir, collection_dir, bind_script):
    unit_dir, collection_dir, bind_script = Path(unit_dir), Path(collection_dir), Path(bind_script)
    if not (unit_dir / "skills").is_dir():
        raise ValueError(f"no skills/ dir in unit {unit_dir}")
    slugs = {d.name for d in (unit_dir / "skills").iterdir() if d.is_dir()}
    full = json.loads((collection_dir / "kb_bundle.json").read_text())
    bundle = filter_and_enrich_bundle(full, slugs, _read_corpus(collection_dir), _read_tools(collection_dir))
    written = []
    (unit_dir / "kb_bundle.json").write_text(json.dumps(bundle, indent=2) + "\n"); written.append("kb_bundle.json")
    (unit_dir / "bin").mkdir(exist_ok=True)
    shutil.copyfile(bind_script, unit_dir / "bin" / "perspicacite_kb_bind.py"); written.append("bin/perspicacite_kb_bind.py")
    (unit_dir / "commands").mkdir(exist_ok=True)
    (unit_dir / "commands" / "ground.md").write_text(render_ground_command()); written.append("commands/ground.md")
    (unit_dir / "GROUNDING.md").write_text(render_grounding_doc(unit_dir.name)); written.append("GROUNDING.md")
    pj_path = unit_dir / ".claude-plugin" / "plugin.json"
    if not pj_path.is_file():
        raise ValueError(f"no .claude-plugin/plugin.json in unit {unit_dir}")
    pj = json.loads(pj_path.read_text())
    if not pj.get("description", "").endswith(_SUFFIX):
        pj["description"] = pj.get("description", "") + _SUFFIX
        pj_path.write_text(json.dumps(pj, indent=2) + "\n"); written.append(".claude-plugin/plugin.json")
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--unit", required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--bind-script", default=str(Path(__file__).with_name("perspicacite_kb_bind.py")))
    a = ap.parse_args(argv)
    for w in build_unit(Path(a.unit), Path(a.collection), Path(a.bind_script)):
        print("wrote", Path(a.unit) / w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
