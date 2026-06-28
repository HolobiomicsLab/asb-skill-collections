#!/usr/bin/env python3
"""validate_workflows — release-gate validator for the composite workflow super-skill subtree.

Validates `workflows/<slug>/{SKILL.md,workflow.yaml}` against the ASB composite-workflow
contract (SPEC docs/asbb/superskills). Intended to be called by release_gate.py before a
`workflows/` subtree is promoted from staging into a released collection.

Checks per workflow:
  - SKILL.md frontmatter parses; metadata.kind == composite-workflow; schema_version 0.3.0.
  - every member_skills slug AND every workflow.yaml steps[].skills slug resolves in the
    target collection's skills_index.json.
  - workflow.yaml parses; steps[].after / inputs_from reference only earlier step ids
    (valid DAG, no cycles, no dangling refs).
  - no cross-stage skill collisions (a leaf appears in only one stage).
  - tools carry no script-filename leaks (*.py) and no case-duplicates.

Exit 0 if all pass, 1 otherwise. Usage:
  python validate_workflows.py --workflows <dir> --collection <released-or-staged collection dir>
"""
from __future__ import annotations
import argparse, json, os, sys, glob
import yaml


def _frontmatter(path):
    return yaml.safe_load(open(path).read().split("---")[1])


def validate_one(d, idx):
    errs = []
    sk_md, wf_y = os.path.join(d, "SKILL.md"), os.path.join(d, "workflow.yaml")
    if not (os.path.exists(sk_md) and os.path.exists(wf_y)):
        return [f"{os.path.basename(d)}: missing SKILL.md or workflow.yaml"]
    fm = _frontmatter(sk_md)
    wf = yaml.safe_load(open(wf_y))
    name = os.path.basename(d)
    m = fm.get("metadata", {})
    if m.get("kind") != "composite-workflow":
        errs.append(f"{name}: metadata.kind != composite-workflow")
    if str(fm.get("schema_version")) != "0.3.0":
        errs.append(f"{name}: schema_version != 0.3.0")
    ms = m.get("member_skills", [])
    for s in ms:
        if s not in idx:
            errs.append(f"{name}: member_skill unresolved: {s}")
    ids, seen = set(), {}
    for st in wf.get("steps", []):
        for s in (st.get("skills") or []):
            if s not in idx:
                errs.append(f"{name}/{st['id']}: skill unresolved: {s}")
            if s in seen and seen[s] != st["id"]:
                errs.append(f"{name}: collision {s}: {seen[s]} & {st['id']}")
            seen[s] = st["id"]
        for a in (st.get("after") or []):
            if a not in ids:
                errs.append(f"{name}/{st['id']}: dangling after -> {a}")
        for k in (st.get("inputs_from") or {}):
            if k not in ids:
                errs.append(f"{name}/{st['id']}: dangling inputs_from -> {k}")
        ids.add(st["id"])
    mt = m.get("member_tools", [])
    for t in mt:
        if str(t).endswith(".py"):
            errs.append(f"{name}: script-filename leaked as tool: {t}")
    low = {}
    for t in mt:
        low.setdefault(str(t).lower(), []).append(t)
    for k, v in low.items():
        if len(v) > 1:
            errs.append(f"{name}: case-duplicate tool: {v}")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workflows", required=True, help="dir holding workflows/<slug>/ subdirs")
    ap.add_argument("--collection", required=True, help="collection dir with skills_index.json")
    a = ap.parse_args()
    idx = {r["slug"] for r in json.load(open(os.path.join(a.collection, "skills_index.json")))}
    dirs = [d for d in sorted(glob.glob(os.path.join(a.workflows, "*")))
            if os.path.isdir(d) and not os.path.basename(d).startswith("_")
            and os.path.basename(d) not in ("_archive", "bin")]
    all_errs, n_ok = [], 0
    for d in dirs:
        errs = validate_one(d, idx)
        if errs:
            all_errs += errs
        else:
            n_ok += 1
            print(f"  OK  {os.path.basename(d)}")
    for e in all_errs:
        print(f"  ERR {e}", file=sys.stderr)
    print(f"\n{n_ok}/{len(dirs)} workflows valid; {len(all_errs)} errors")
    sys.exit(0 if not all_errs else 1)


if __name__ == "__main__":
    main()
