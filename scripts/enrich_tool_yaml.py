"""Propagate per-tool license fields from ``tools_index.json`` into the LinkML
per-tool records ``tools/<slug>.yaml``.

``tools_index.json`` already carries ``license_tier`` / ``license`` /
``license_detection`` / ``license_subject`` (written by ``enrich_tools_index.py``);
the 909 generated ``tools/<slug>.yaml`` records do not. This post-processor joins by
``slug`` and writes those fields into each tool YAML, idempotently and
style-preserving. It also drops ``canonical_url``, which held a citing paper's
repository under a name claiming it was the tool's own (issue #42); the same value is
kept, honestly named, in ``source_repos``.

Design mirrors ``propagate_license_tiers.py`` / ``enrich_tools_index.py``:
- idempotent, format-preserving writer over committed artifacts;
- no git / gh / network; no ``Date.now``-style nondeterminism;
- the license fields land immediately after ``schema_version`` (before any
  later-appended block such as ``techniques``), a deterministic position so
  re-runs are byte-stable.
"""
from __future__ import annotations

import json
import pathlib

import yaml

_LICENSE_KEYS = ("entry_kind", "license_tier", "license", "license_detection",
                 "license_subject", "repo_url")

# Retired keys, stripped on every pass. `canonical_url` was a copy of one arbitrary
# member of `source_repos` -- a repository belonging to a paper that cites the tool,
# not to the tool. All 700 populated values were already in `source_repos`, so
# removing the key loses nothing and stops the claim being restated.
_RETIRED_KEYS = ("canonical_url",)


def _yaml_dump(data: dict) -> str:
    """Match ``collect_metabolomics_collection.render_tool_yaml`` serialization."""
    return yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000
    )


def tier_map(tools_index) -> dict:
    """``{slug: {license_tier, license, license_detection, license_subject}}``.

    Missing values default to ``None`` so every row is complete; entries without a
    ``slug`` are skipped.
    """
    out: dict[str, dict] = {}
    for t in tools_index:
        slug = t.get("slug")
        if not slug:
            continue
        out[slug] = {k: t.get(k) for k in _LICENSE_KEYS}
    return out


def _reorder_with_license(data: dict, fields: dict) -> dict:
    """Return a new dict with the license fields placed right after
    ``schema_version`` (or appended if absent), preserving all other key order.
    Retired keys are dropped.
    """
    # Strip existing license keys so we can re-place them deterministically.
    drop = set(_LICENSE_KEYS) | set(_RETIRED_KEYS)
    base = {k: v for k, v in data.items() if k not in drop}
    rebuilt: dict = {}
    inserted = False
    for k, v in base.items():
        rebuilt[k] = v
        if k == "schema_version":
            for lk in _LICENSE_KEYS:
                rebuilt[lk] = fields[lk]
            inserted = True
    if not inserted:
        for lk in _LICENSE_KEYS:
            rebuilt[lk] = fields[lk]
    return rebuilt


def enrich(collection_dir) -> dict:
    d = pathlib.Path(collection_dir)
    tools_index = json.loads((d / "tools_index.json").read_text(encoding="utf-8"))
    tiers = tier_map(tools_index)

    tools_dir = d / "tools"
    enriched = 0
    skipped = 0
    if not tools_dir.is_dir():
        return {"enriched": 0, "skipped": 0}

    for yaml_path in sorted(tools_dir.glob("*.yaml")):
        slug = yaml_path.stem
        fields = tiers.get(slug)
        if fields is None:
            skipped += 1
            continue
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        rebuilt = _reorder_with_license(data, fields)
        new_text = _yaml_dump(rebuilt)
        if new_text != yaml_path.read_text(encoding="utf-8"):
            yaml_path.write_text(new_text, encoding="utf-8")
        enriched += 1

    return {"enriched": enriched, "skipped": skipped}


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection",
        required=True,
        help="collection dir with tools_index.json and a tools/ subdir of <slug>.yaml",
    )
    a = ap.parse_args(argv)
    res = enrich(a.collection)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
