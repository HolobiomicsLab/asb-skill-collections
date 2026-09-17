#!/usr/bin/env python3
"""validate_workflows — release-gate validator for the composite workflow super-skill subtree.

Validates `workflows/<slug>/{SKILL.md,workflow.yaml}` against the ASB composite-workflow
contract (SPEC docs/asbb/superskills). Intended to be called by release_gate.py before a
`workflows/` subtree is promoted from staging into a released collection.

Checks per workflow:
  - SKILL.md frontmatter parses; metadata.kind == composite-workflow; schema_version 0.3.0.
  - every member_skills slug AND every workflow.yaml steps[].skills slug resolves in the
    target collection's skills_index.json.
  - workflow.yaml parses; steps[].after / inputs_from reference only earlier step ids,
    and every inputs_from type is declared by both endpoint steps.
  - collection.yaml workflows_count, when declared, matches the workflow directories.
  - no cross-stage skill collisions (a leaf appears in only one stage).
  - tools carry no script-filename leaks (*.py) and no case-duplicates.

``verification.final_outputs[].type`` is intentionally not compared with step output
types: final outputs describe file kinds and use a different vocabulary from step ports.

Exit 0 if all pass, 1 otherwise. Usage:
  python validate_workflows.py --workflows <dir> --collection <released-or-staged collection dir>
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import yaml


def _frontmatter(path):
    # Parse the block between the first two lines that are exactly '---', so a
    # stray '---' inside a value/body cannot truncate it (the v0.2.0 bug) and a
    # fenceless file yields {} instead of an IndexError.
    lines = open(path).read().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return yaml.safe_load("\n".join(lines[1:i])) or {}
    return {}


def validate_port_types(workflow_name, steps):
    """Return type errors for earlier-step ``inputs_from`` edges.

    Only step input/output ports share this vocabulary.  The file kinds under
    ``verification.final_outputs[].type`` are intentionally outside this check.
    Dangling or forward producer ids remain the caller's DAG-validation concern.
    """
    errors, earlier_steps = [], {}
    for consumer in steps:
        consumer_id = consumer.get("id")
        consumer_types = {
            declared_type
            for port in (consumer.get("inputs") or [])
            if isinstance(port, dict) and "type" in port
            for declared_type in (
                port["type"],
                f"{port['type']}:{port['flavour']}" if port.get("flavour") else port["type"],
            )
        }
        for producer_id, transferred_types in (consumer.get("inputs_from") or {}).items():
            producer = earlier_steps.get(producer_id)
            if producer is None:
                continue
            producer_types = {
                declared_type
                for port in (producer.get("outputs") or [])
                if isinstance(port, dict) and "type" in port
                for declared_type in (
                    port["type"],
                    f"{port['type']}:{port['flavour']}" if port.get("flavour") else port["type"],
                )
            }
            declared_types = sorted(str(port_type) for port_type in producer_types)
            for port_type in transferred_types or []:
                prefix = (
                    f"{workflow_name}/{consumer_id}: inputs_from producer {producer_id!r} "
                    f"requests type {port_type!r}"
                )
                if port_type not in producer_types:
                    errors.append(f"{prefix}, but producer outputs declare {declared_types}")
                if port_type not in consumer_types:
                    errors.append(
                        f"{prefix}, but consumer inputs do not declare it; "
                        f"producer outputs declare {declared_types}"
                    )
        earlier_steps[consumer_id] = consumer
    return errors


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
    steps = wf.get("steps", [])
    errs.extend(validate_port_types(name, steps))
    ids, seen = set(), {}
    for st in steps:
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
    collection_yaml = os.path.join(a.collection, "collection.yaml")
    if os.path.isfile(collection_yaml):
        collection_meta = yaml.safe_load(open(collection_yaml)) or {}
        if ("workflows_count" in collection_meta
                and collection_meta["workflows_count"] != len(dirs)):
            all_errs.append(
                "collection.yaml workflows_count mismatch: "
                f"declared {collection_meta['workflows_count']}, "
                f"on-disk workflow directories {len(dirs)}"
            )
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
