"""Join corpus license_tier onto skills_index.json + kb_bundle.json (by DOI),
and build the metadata.tool_license block for non-open SKILL.md frontmatters.
"""
from __future__ import annotations

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

import json
import pathlib

import yaml

from asb_skill_collections import layout
from scripts.license_tier import ack_required

_ORDER = {"open": 0, "noncommercial": 1, "restricted": 2}


def detect_indent(text: str, default: int = 2) -> int:
    """Infer the leading-space indent width from the first indented line."""
    for line in text.splitlines():
        stripped = line.lstrip(" ")
        if stripped and stripped != line:
            return len(line) - len(stripped)
    return default


def corpus_tier_by_doi(corpus_path) -> dict:
    doc = yaml.safe_load(pathlib.Path(corpus_path).read_text(encoding="utf-8"))
    out = {}
    for p in doc.get("papers", []):
        doi, tier = p.get("doi"), p.get("license_tier")
        if doi and tier:
            out[doi] = {"tier": tier, "license": (p.get("access") or {}).get("license"),
                        "repo_url": p.get("repo_url")}
    return out


# What a skill's tier is when nothing establishes it. `open` would be the most
# permissive answer to a question nobody answered, and `asb-metabolomics` tells
# agents to default discovery to open-tier skills -- so an unestablished tier
# advertised as open is how a noncommercial tool gets presented as free to use.
UNESTABLISHED_TIER = "restricted"


def declared_tiers(collection_dir) -> dict[str, str]:
    """Each skill's own `metadata.tool_license.tier`, keyed by slug.

    A skill grounded on a repository rather than a paper has no corpus DOI, so
    the DOI join can say nothing about it -- but the skill itself often knows,
    because the tool's licence was read when the skill was written.
    """
    out: dict[str, str] = {}
    for md in layout.iter_skill_md(collection_dir):
        try:
            text = md.read_text(encoding="utf-8")
            fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        except (OSError, IndexError, yaml.YAMLError):
            continue
        tier = ((fm.get("metadata") or {}).get("tool_license") or {}).get("tier")
        if tier in _ORDER:
            out[md.parent.name] = tier
    return out


def skill_tier(dois, tiers, declared=None) -> str:
    """Most-restrictive tier across a skill's DOIs.

    With no DOI-derived tier, fall back to the skill's own declared
    `tool_license.tier`, and failing that to :data:`UNESTABLISHED_TIER`. Never
    to `open`: "we did not establish this" and "this is freely usable" are
    different answers, and only one of them is safe to guess.
    """
    found = [tiers[d]["tier"] for d in (dois or []) if d in tiers]
    if found:
        return max(found, key=lambda t: _ORDER[t])
    return declared if declared in _ORDER else UNESTABLISHED_TIER


def propagate_indices(skills_index_path, kb_bundle_path, tiers, declared=None) -> dict:
    si_path, kb_path = pathlib.Path(skills_index_path), pathlib.Path(kb_bundle_path)
    si_raw = si_path.read_text(encoding="utf-8")
    kb_raw = kb_path.read_text(encoding="utf-8")
    si = json.loads(si_raw)
    kb = json.loads(kb_raw)
    si_indent = detect_indent(si_raw)
    kb_indent = detect_indent(kb_raw)
    summary: dict[str, int] = {}
    declared = declared or {}
    for entry in si:
        t = skill_tier(entry.get("dois"), tiers, declared.get(entry.get("slug")))
        entry["license_tier"] = t
        summary[t] = summary.get(t, 0) + 1
    for slug, rec in (kb.get("skills") or {}).items():
        rec["license_tier"] = skill_tier(rec.get("dois"), tiers, declared.get(slug))
    si_path.write_text(json.dumps(si, indent=si_indent, ensure_ascii=False), encoding="utf-8")
    kb_path.write_text(json.dumps(kb, indent=kb_indent, ensure_ascii=False), encoding="utf-8")
    return summary


def tool_license_block(tier, license, repo_url) -> dict:
    return {"tier": tier, "requires_ack": ack_required(tier),
            "ref": license or "unknown", "url": repo_url or ""}


# --------------------------------------------------------------------------- #
# Backfill: a non-open leaf that carries no `tool_license` block at all.        #
#                                                                              #
# The block is what `asb-metabolomics` reads to decide whether to raise the     #
# blocking use acknowledgment. A leaf missing it is not "unacknowledged by      #
# default" -- it is invisible to the gate, so a noncommercial tool is applied   #
# with no acknowledgment at all while the frontmatter still says               #
# `license_tier: noncommercial`. The human-readable banner in the body does not #
# close that hole: no reader parses prose.                                      #
# --------------------------------------------------------------------------- #


def _dump_block(block: dict, indent: int, newline: str = "\n") -> str:
    """Render `tool_license:` + children at `indent`, in the corpus's own style."""
    dumped = yaml.safe_dump({"tool_license": block}, sort_keys=False,
                            default_flow_style=False, allow_unicode=True)
    pad = " " * indent
    text = "".join(pad + line for line in dumped.splitlines(keepends=True))
    return text if newline == "\n" else text.replace("\n", newline)


def insert_tool_license(fm_raw: str, block: dict) -> str:
    """Add `metadata.tool_license` to a frontmatter, changing no other byte.

    Anchored on the `license_tier` line the block expands, and inserted as text
    rather than re-dumped, because a round-trip through safe_dump reflows every
    quote, comment and line break in a frontmatter that is mostly unrelated to
    licensing. Raises on any shape it cannot edit in place -- refusing is the
    safe failure here, silently rewriting the file is not.
    """
    if any(isinstance(t, yaml.AliasToken) for t in yaml.scan(fm_raw)):
        raise ValueError("frontmatter uses YAML aliases; refusing an in-place edit")
    root = yaml.compose(fm_raw)
    metadata = next((v for k, v in (root.value if root else []) if k.value == "metadata"), None)
    if not isinstance(metadata, yaml.MappingNode) or metadata.flow_style or not metadata.value:
        raise ValueError("metadata is not a non-empty block mapping")
    entry = next(((k, v) for k, v in metadata.value if k.value == "license_tier"), None)
    if entry is None:
        raise ValueError("no metadata.license_tier to anchor the block to")
    key, value = entry
    if not isinstance(value, yaml.ScalarNode):
        raise ValueError("metadata.license_tier is not a scalar")
    eol = fm_raw.find("\n", value.end_mark.index)
    if eol < 0:
        raise ValueError("metadata.license_tier is on an unterminated line")
    at = eol + 1
    newline = "\r\n" if "\r\n" in fm_raw else "\n"
    new_fm = fm_raw[:at] + _dump_block(block, key.start_mark.column, newline) + fm_raw[at:]

    # The insertion point is computed from one key's span; a mis-anchored insert
    # would land the block in a neighbouring mapping and still look plausible.
    expected = yaml.safe_load(fm_raw) or {}
    expected.setdefault("metadata", {})["tool_license"] = block
    if (yaml.safe_load(new_fm) or {}) != expected:
        raise ValueError("insert changed the frontmatter's meaning; refusing")
    return new_fm


def governing_paper(dois, tiers) -> tuple:
    """The (tier, license, repo_url) of the most-restrictive DOI behind a skill.

    Same rule as :func:`skill_tier`; this returns the winning paper's licence and
    repository too, which is what the block has to carry. Ties are broken by the
    skill's own DOI order, so the answer does not depend on dict iteration.
    """
    found = [(d, tiers[d]) for d in (dois or []) if d in tiers]
    if not found:
        return None, None, None
    top = max(_ORDER[v["tier"]] for _, v in found)
    _, win = next((d, v) for d, v in found if _ORDER[v["tier"]] == top)
    return win["tier"], win.get("license"), win.get("repo_url")


def backfill_tool_license(collection_dir, corpus_path=None, index_path=None,
                          tiers_to_fix=None, dry_run=False) -> dict:
    """Write the missing `tool_license` block for every leaf that needs one.

    `tiers_to_fix` defaults to the tiers whose block actually gates something --
    the ones `ack_required` says must raise a blocking acknowledgment. That is
    deliberately the same predicate `check_license_tiers` uses to call a missing
    block a violation: a gate that flags what the fixer will not fix by default
    is a trap, and a fixer that writes blocks the gate never asked for is churn.
    """
    d = pathlib.Path(collection_dir)
    tiers = corpus_tier_by_doi(corpus_path or d / "corpus.yaml")
    index = json.loads(pathlib.Path(index_path or d / "skills_index.json").read_text(encoding="utf-8"))
    dois_by_slug = {e.get("slug"): e.get("dois") or [] for e in index}
    wanted = tiers_to_fix if tiers_to_fix is not None else {t for t in _ORDER if ack_required(t)}

    written, skipped, counts = [], [], {}
    for md in layout.iter_skill_md(d):
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        _, fm_raw, body = text.split("---\n", 2)
        meta = ((yaml.safe_load(fm_raw) or {}).get("metadata") or {})
        declared = meta.get("license_tier")
        if declared not in wanted or meta.get("tool_license"):
            continue
        slug = md.parent.name
        derived, license, repo_url = governing_paper(dois_by_slug.get(slug), tiers)
        # Two answers to the same question. Writing a block that contradicts the
        # tier already on the file would make the gate's own consistency check
        # the thing that discovers a corpus disagreement -- report it instead.
        if derived is None:
            skipped.append(f"{slug}: no corpus DOI establishes a tier")
            continue
        if derived != declared:
            skipped.append(f"{slug}: corpus says {derived!r}, frontmatter says {declared!r}")
            continue
        block = tool_license_block(derived, license, repo_url)
        try:
            new_fm = insert_tool_license(fm_raw, block)
        except ValueError as exc:
            skipped.append(f"{slug}: {exc}")
            continue
        if not dry_run:
            md.write_text("---\n" + new_fm + "---\n" + body, encoding="utf-8")
        written.append(slug)
        counts[derived] = counts.get(derived, 0) + 1
    return {"written": written, "skipped": skipped, "tiers": counts,
            "n_written": len(written), "n_skipped": len(skipped), "dry_run": dry_run}


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("collection", help="collection dir (holds corpus.yaml + skills_index.json)")
    ap.add_argument("--fix", action="store_true",
                    help="write the missing metadata.tool_license blocks")
    ap.add_argument("--tier", action="append", dest="tiers", metavar="TIER",
                    help="tier to backfill; repeatable. Default: every tier whose "
                         "block raises a blocking acknowledgment (noncommercial).")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    a = ap.parse_args(argv)
    if not a.fix:
        ap.error("nothing to do: pass --fix")
    res = backfill_tool_license(a.collection, tiers_to_fix=set(a.tiers) if a.tiers else None,
                                dry_run=a.dry_run)
    print(json.dumps(res, indent=2))
    return 1 if res["skipped"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
