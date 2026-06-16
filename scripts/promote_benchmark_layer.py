#!/usr/bin/env python
"""Promote the ASB benchmark layer into a skill collection (per-collection subdirs).

Lifts the cards / challenges / indicium / (slim) capsules from each grounded build
dir into ``collections/<domain>/v<N>/`` alongside ``skills/`` + ``tools/``, and
writes a ``MANIFEST.yaml`` declaring selective install/release **layers** so a
consumer can take *skills-only*, *skills+kb-bundle*, *benchmark-only*, or *full*.

Layout produced (everything-together, but layer-addressable):

    collections/<domain>/v<N>/
      collection.yaml  corpus.yaml  CITATION.cff      # core (existing)
      skills/  tools/                                  # skills layer (existing)
      benchmark/
        cards/<tool>/task_*.{json,md}                 # SciTask benchmark tasks
        challenges/<tool>/{WORKFLOW_CHALLENGE.md,workflow.yaml}
      capsules/<tool>/<capsule>/                       # slim: ledger+evaluation+evidence+inputs
      indicium/<tool>.jsonld                           # per-tool knowledge graph
      links.json                                       # skill <-> task cross-links
      MANIFEST.yaml                                    # install/release layers

Heavy capsule internals (figures/, logs/, artifacts/) are NOT promoted — they stay
in the build dirs.  Use ``--with-figures`` to include figures.

Usage:
  promote_benchmark_layer.py --collection-dir collections/<domain>/v1 \
      --builds-root <ASB outputs/asbb_<domain>> [--with-figures] [--clean]
"""
from __future__ import annotations
import argparse, json, re, shutil
from pathlib import Path

import yaml

# Capsule subpaths to promote (text/reproducibility-relevant); the rest is heavy.
_CAPSULE_KEEP = ["ledger", "evaluation", "evidence", "inputs", "artifact_provenance.json"]
_CAPSULE_KEEP_FIGS = _CAPSULE_KEEP + ["figures"]


def _slug_from_build(dirname: str) -> str:
    s = re.sub(r"^coll_", "", dirname)
    s = re.sub(r"_grounded$", "", s)  # e.g. spec2vec_grounded -> spec2vec
    return s.strip("_").lower()


def _iter_build_dirs(builds_root: Path):
    # A build dir is any immediate subdir carrying a build_manifest.json — covers
    # both coll_* and special names (e.g. spec2vec_grounded).
    for d in sorted(builds_root.iterdir()):
        if d.is_dir() and (d / "build_manifest.json").is_file():
            yield d


def _skill_slugs(collection_dir: Path) -> set[str]:
    return {p.parent.name for p in (collection_dir / "skills").glob("*/SKILL.md")}


def _load_assembler(corpus_path: Path):
    """Reuse the assembler's exact discovery + build-dir -> corpus matching so the
    benchmark layer mirrors the skills collection precisely.  Returns
    (corpus_index, resolve_fn, discover_fn) or (None, None, None)."""
    if not corpus_path:
        return None, None, None
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from collect_metabolomics_collection import (
        load_corpus_index, resolve_build_to_corpus, discover_build_dirs,
    )
    return load_corpus_index(corpus_path), resolve_build_to_corpus, discover_build_dirs


def _card_skill_links(card_json: dict, known_skills: set[str]) -> list[str]:
    """Resolve a card's referenced skills to actual collection skill slugs."""
    out = []
    for s in card_json.get("skills") or []:
        slug = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
        if slug in known_skills:
            out.append(slug)
    return out


def promote(collection_dir: Path, builds_root: Path, with_figures: bool, clean: bool,
            exclude: set[str] | None = None, corpus_path: Path | None = None) -> dict:
    exclude = {e.strip().lower() for e in (exclude or set())}
    corpus_index, resolve_fn, discover_fn = _load_assembler(corpus_path)
    bench = collection_dir / "benchmark"
    caps = collection_dir / "capsules"
    indi = collection_dir / "indicium"
    if clean:
        for d in (bench, caps, indi):
            if d.exists():
                shutil.rmtree(d)
    (bench / "cards").mkdir(parents=True, exist_ok=True)
    (bench / "challenges").mkdir(parents=True, exist_ok=True)
    caps.mkdir(parents=True, exist_ok=True)
    indi.mkdir(parents=True, exist_ok=True)

    known_skills = _skill_slugs(collection_dir)
    keep = _CAPSULE_KEEP_FIGS if with_figures else _CAPSULE_KEEP
    links: dict[str, dict] = {}
    counts = {"tools": 0, "cards": 0, "capsules": 0, "indicium": 0, "challenges": 0, "skipped_not_in_collection": 0}

    build_dirs = discover_fn(builds_root) if discover_fn else list(_iter_build_dirs(builds_root))
    for bdir in build_dirs:
        slug = _slug_from_build(bdir.name)
        if slug in exclude:
            continue
        # Promote ONLY builds that match this collection's corpus (same matcher
        # as the assembler) so the benchmark layer mirrors the skills exactly.
        if corpus_index is not None and resolve_fn(bdir.name, corpus_index) is None:
            counts["skipped_not_in_collection"] += 1
            continue
        counts["tools"] += 1
        # --- cards ---
        src_cards = bdir / "cards"
        if src_cards.is_dir():
            dst = bench / "cards" / slug
            dst.mkdir(parents=True, exist_ok=True)
            for f in sorted(src_cards.glob("task_*.*")):
                if f.name.endswith((".json", ".md")) and ".orig." not in f.name:
                    shutil.copy2(f, dst / f.name)
                    if f.suffix == ".json":
                        counts["cards"] += 1
                        try:
                            cj = json.loads(f.read_text(encoding="utf-8"))
                            links[f"{slug}/{cj.get('task_id', f.stem)}"] = {
                                "tool": slug,
                                "task_kind": cj.get("task_kind"),
                                "title": cj.get("title"),
                                "skills": _card_skill_links(cj, known_skills),
                            }
                        except Exception:
                            pass
        # --- challenges ---
        ch_dst = bench / "challenges" / slug
        wrote_ch = False
        for fn in ("WORKFLOW_CHALLENGE.md", "workflow.yaml"):
            src = bdir / fn
            if src.is_file():
                ch_dst.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, ch_dst / fn)
                wrote_ch = True
        if wrote_ch:
            counts["challenges"] += 1
        # --- indicium ---
        ind = bdir / "indicium.jsonld"
        if ind.is_file():
            shutil.copy2(ind, indi / f"{slug}.jsonld")
            counts["indicium"] += 1
        # --- capsules (slim) ---
        src_caps = bdir / "capsules"
        if src_caps.is_dir():
            for cap in sorted(src_caps.iterdir()):
                if not cap.is_dir():
                    continue
                cdst = caps / slug / cap.name
                cdst.mkdir(parents=True, exist_ok=True)
                for item in keep:
                    s = cap / item
                    if s.is_dir():
                        shutil.copytree(s, cdst / item, dirs_exist_ok=True)
                    elif s.is_file():
                        shutil.copy2(s, cdst / item)
                counts["capsules"] += 1

    (collection_dir / "links.json").write_text(
        json.dumps({"schema": "asb-skill-task-links/1.0", "links": links}, indent=1),
        encoding="utf-8",
    )
    _write_manifest(collection_dir)
    return {**counts, "skill_task_links": len(links)}


def _write_manifest(collection_dir: Path) -> None:
    meta = yaml.safe_load((collection_dir / "collection.yaml").read_text(encoding="utf-8"))
    manifest = {
        "schema": "asb-collection-manifest/1.0",
        "collection": meta.get("slug"),
        "version": meta.get("version"),
        "description": "Layered install/release manifest — take any single layer or compose.",
        "layers": {
            "skills": {
                "description": "Evidence-grounded skills + tool records. Installs to ~/.claude/skills.",
                "include": ["collection.yaml", "CITATION.cff", "skills/**", "tools/**"],
                "install_target": "~/.claude/skills",
            },
            "bundle": {
                "description": "Skills + the re-enrichable KB bundle (source corpus + the skill-bundled resources already under skills/).",
                "extends": ["skills"],
                "include": ["corpus.yaml"],
            },
            "benchmark": {
                "description": "SciTask cards + workflow challenges (the benchmark tasks). links.json preserves skill<->task.",
                "include": ["collection.yaml", "corpus.yaml", "benchmark/**", "links.json"],
            },
            "full": {
                "description": "Everything incl. capsules (reproducible claim units) + indicium KG — for ablation experiments.",
                "extends": ["skills", "bundle", "benchmark"],
                "include": ["capsules/**", "indicium/**"],
            },
        },
    }
    (collection_dir / "MANIFEST.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=10**6),
        encoding="utf-8",
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection-dir", required=True)
    ap.add_argument("--builds-root", required=True)
    ap.add_argument("--with-figures", action="store_true", help="also promote capsule figures/ (heavier)")
    ap.add_argument("--clean", action="store_true", help="remove benchmark/capsules/indicium first")
    ap.add_argument("--exclude", nargs="*", default=[], help="build slugs to skip (e.g. held non-OA papers)")
    ap.add_argument("--corpus", default=None,
                    help="assembler corpus JSON — promote only builds matching it (mirrors the skills collection)")
    args = ap.parse_args()
    cd = Path(args.collection_dir).expanduser().resolve()
    br = Path(args.builds_root).expanduser().resolve()
    cp = Path(args.corpus).expanduser().resolve() if args.corpus else None
    summary = promote(cd, br, args.with_figures, args.clean, set(args.exclude), cp)
    print(f"promoted benchmark layer -> {cd}")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
