#!/usr/bin/env python3
"""Write the cross-domain card of the evaluation definitions held by the build-capsule packs.

Every number comes from the descriptive files of the packs (`MANIFEST.json`, `capsules.jsonl`,
`benchmark-manifest.json`), which are also files of each capsules record; nothing is read from the build archives
and nothing is sent anywhere. The card states what exists (definitions) and what does not (any validation of them).

    python scripts/render_evaluation_card.py --packs <pack root> --out docs/evaluation-definitions.md

A domain without `MANIFEST.json` under the pack root is refused unless `--allow-missing` is given, in which case
the card says so in its first lines and cannot be mistaken for the ten-domain card.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

DOMAINS = ("agentic-ai", "astronomy", "epigenomics", "genomics", "metabarcoding", "metabolomics", "metagenomics",
           "multi-omics", "proteomics", "transcriptomics")
MACHINE_KINDS_NOTE = "every kind other than `expert_review`"
COLUMNS = (
    ("builds", "Builds"), ("left_out", "Builds left out"), ("capsules", "Capsules"), ("complete", "Complete"),
    ("partial", "Partial"), ("checks", "Checks"), ("expert", "Expert review"), ("machine", "Machine"),
    ("unresolved", "Unresolved references"), ("assets", "Input entries"), ("hashed", "With hash"),
    ("hinted", "With download hint"),
)


def read_rows(path: Path) -> list[dict]:
    """Return the JSON objects of one JSON Lines file."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def domain_counts(pack: Path) -> tuple[dict, Counter, Counter, dict]:
    """Count one domain's pack: table row, check kinds, claim-grounding labels, and its provenance fields."""
    manifest = json.loads((pack / "MANIFEST.json").read_text(encoding="utf-8"))
    listing = json.loads((pack / "benchmark-manifest.json").read_text(encoding="utf-8"))
    capsules = read_rows(pack / "capsules.jsonl")
    states = Counter(row["eval_state"] for row in capsules)
    unexpected = set(states) - {"complete", "partial"}
    if unexpected:
        raise SystemExit(f"{pack.name}: evaluation states outside complete and partial: {sorted(unexpected)}")
    if listing["capsule_count"] != states["complete"]:
        raise SystemExit(f"{pack.name}: listing holds {listing['capsule_count']} capsules, table {states['complete']}")
    kinds = Counter(listing["totals"]["checks_by_kind"])
    totals = listing["totals"]
    row = {
        "builds": manifest["builds_packed"], "left_out": manifest["builds_left_out"],
        "capsules": manifest["capsule_count"], "complete": states["complete"], "partial": states["partial"],
        "checks": sum(kinds.values()), "expert": kinds["expert_review"],
        "machine": sum(kinds.values()) - kinds["expert_review"], "unresolved": totals["unresolved_references"],
        "assets": totals["input_assets"], "hashed": totals["input_assets_with_hash"],
        "hinted": totals["input_assets_with_download_hint"],
    }
    grounding = Counter(row_["validation_state"] for row_ in capsules)
    provenance = {key: manifest[key] for key in ("tooling_commit", "collection_version_doi", "generation_date")}
    return row, kinds, grounding, provenance


def render(rows: dict[str, dict], kinds: Counter, grounding: Counter, provenance: dict[str, dict],
           missing: list[str], deposited: bool) -> str:
    """Return the card as Markdown."""
    tooling = {item["tooling_commit"] for item in provenance.values()}
    dates = sorted({item["generation_date"] for item in provenance.values()})
    record_state = (
        "The capsules records are deposited; the counts are those of their descriptive files."
        if deposited else
        "The capsules records are prepared and not deposited: the counts are those of the packs generated on "
        + " and ".join(dates) + ", and a pack rebuilt before deposit replaces them."
    )
    total = Counter()
    for row in rows.values():
        total.update(row)
    share = f"{100 * total['expert'] / total['checks']:.1f}" if total["checks"] else "0"
    lines = ["# Evaluation definitions in the build capsules", ""]
    if missing:
        lines += [f"**Incomplete card: not packed yet: {', '.join(missing)}. Totals cover the other {len(rows)} of "
                  f"{len(DOMAINS)} domains.**", ""]
    lines += [
        "## Status",
        "",
        "The build capsules hold evaluation definitions only. **No validation of these definitions exists.** None has",
        "been run end to end, none has reference outputs produced or labelled by an expert, no agent result has been",
        "scored against one, and no ranking exists. The counts below describe what the files contain, not what they",
        "have been shown to measure.",
        "",
        record_state,
        "",
        "## What a definition is",
        "",
        "Each capsule is one task derived from one published article. Its `eval.json` names the task, the inputs it",
        "expects, the outputs it expects and the checks to apply to them. A definition is counted **complete** when",
        "it carries the four keys `task_id`, `inputs`, `expected_outputs` and `checks`, at least one check, and no",
        "recorded validation error; otherwise it is **partial**. Complete is a statement about structure. It does not",
        "say that the task can be run, that its inputs can be retrieved, or that its checks can be scored by a",
        "machine. `benchmark-manifest.json` of each record lists the complete definitions and carries this sentence.",
        "",
        "## Counts",
        "",
        "Checks, unresolved references and input entries are those of the complete definitions. Machine is",
        f"{MACHINE_KINDS_NOTE}.",
        "",
        "| Domain | " + " | ".join(label for _, label in COLUMNS) + " |",
        "| --- |" + " ---: |" * len(COLUMNS),
    ]
    for domain, row in rows.items():
        lines.append(f"| {domain} | " + " | ".join(f"{row[key]:,}" for key, _ in COLUMNS) + " |")
    lines.append("| **Total** | " + " | ".join(f"**{total[key]:,}**" for key, _ in COLUMNS) + " |")
    lines += [
        "",
        "## How to read them",
        "",
        f"- {total['complete']:,} of {total['capsules']:,} capsules ({100 * total['complete'] / total['capsules']:.1f} %) "
        "carry a complete definition.",
        f"- {total['expert']:,} of their {total['checks']:,} checks ({share} %) are of kind `expert_review`: a rubric "
        f"for a human reader, not a test a program can decide. The other {total['machine']:,} are: "
        + ", ".join(f"`{kind}` {count}" for kind, count in sorted(kinds.items()) if kind != "expert_review") + ".",
        f"- {total['hashed']:,} of the {total['assets']:,} input entries carry a content hash and "
        f"{total['hinted']:,} a download hint. The inputs of a task are therefore named, not pinned.",
        f"- {total['unresolved']:,} references of the complete definitions are recorded as unresolved in the "
        "definitions themselves.",
        f"- {total['left_out']:,} builds are left out of the records, because a required file is missing or because "
        "the screen found a residue it could not remove; their capsules are in no count above.",
        "",
        "## What `validation.json` is, and is not",
        "",
        "Each capsule also carries a `validation.json`. It records an automated comparison, made when the capsule was",
        "built, between the statements the capsule makes about its article and passages retrieved from that article.",
        "The labels derived from it (`present`, `clean`, `strict`) describe the grounding of the capsule's text in",
        "its source. They are not a validation of the evaluation definition, and they were not reviewed by a person.",
        "Over all capsules: "
        + ", ".join(f"`{label}` {grounding[label]:,}" for label in ("present", "clean", "strict")) + ".",
        "",
        "## What does not exist",
        "",
        "- An end-to-end runnable example with frozen inputs.",
        "- Reference outputs for any task, and expert labels on any output.",
        "- A calibrated judge or a final scoring policy.",
        "- Scored agent results, and therefore any leaderboard.",
        "",
        "## Provenance of this card",
        "",
        "This file is generated by `scripts/render_evaluation_card.py` from the descriptive files of the packs",
        "(`MANIFEST.json`, `capsules.jsonl`, `benchmark-manifest.json`), packed with tooling commit "
        + ", ".join(f"`{commit[:9]}`" for commit in sorted(tooling)) + ". Collection versions the packs describe:",
        "",
    ]
    lines += [f"- {domain}: {item['collection_version_doi']}" for domain, item in provenance.items()]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--packs", type=Path, required=True, help="pack root holding one directory per domain")
    parser.add_argument("--out", type=Path, required=True, help="Markdown file to write")
    parser.add_argument("--allow-missing", action="store_true", help="write a card marked incomplete when a domain is not packed")
    parser.add_argument("--deposited", action="store_true", help="say that the records are deposited, not only prepared")
    args = parser.parse_args(argv)
    rows, provenance, missing = {}, {}, []
    kinds, grounding = Counter(), Counter()
    for domain in DOMAINS:
        pack = args.packs / domain
        if not (pack / "MANIFEST.json").exists():
            missing.append(domain)
            continue
        rows[domain], domain_kinds, domain_grounding, provenance[domain] = domain_counts(pack)
        kinds.update(domain_kinds)
        grounding.update(domain_grounding)
    if missing and not args.allow_missing:
        print(f"not packed: {', '.join(missing)}", file=sys.stderr)
        return 1
    args.out.write_text(render(rows, kinds, grounding, provenance, missing, args.deposited), encoding="utf-8")
    print(f"wrote {args.out} ({len(rows)} domains)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
