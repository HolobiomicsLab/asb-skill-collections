#!/usr/bin/env python3
"""build_workflows_index — regenerate workflows_index.json from the staged workflow dirs.

One row per composite workflow super-skill, read from each `<slug>/SKILL.md` frontmatter +
`workflow.yaml`. The leaf/workflow routers and `bin/semantic_search.py` consume this index,
so it must be rebuilt whenever the workflows are (re)generated.

Usage: build_workflows_index.py --workflows <dir>   (writes <dir>/workflows_index.json)
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml


def _frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    return yaml.safe_load(text[3:end]) if end != -1 else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workflows", required=True)
    a = ap.parse_args()
    root = Path(a.workflows)
    rows = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name == "bin":
            continue
        sk, wf = d / "SKILL.md", d / "workflow.yaml"
        if not (sk.is_file() and wf.is_file()):
            print(f"  skip {d.name}: missing SKILL.md/workflow.yaml", file=sys.stderr)
            continue
        fm = _frontmatter(sk.read_text(encoding="utf-8"))
        meta = fm.get("metadata", {})
        doc = yaml.safe_load(wf.read_text(encoding="utf-8")) or {}
        steps = doc.get("steps", [])
        rows.append({
            "slug": d.name,
            "name": fm.get("name", d.name),
            "description": fm.get("description", ""),
            "techniques": meta.get("techniques", []),
            "stage_count": len(steps),
            "stages": [s["id"] for s in steps],
            "member_tools": meta.get("member_tools", []),
            "coverage_gaps": meta.get("coverage_gaps", []),
            "bound_by": meta.get("bound_by", "perspicacite-semantic"),
        })
    out = root / "workflows_index.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(rows)} workflows)")


if __name__ == "__main__":
    main()
