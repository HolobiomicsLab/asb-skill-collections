#!/usr/bin/env python3
"""Search a collection's skills index and print a few candidates.

The collection ships thousands of leaf skills. Reading the whole index into a
conversation would cost more context than the skills themselves, so retrieval
happens here: this script scans the index on disk and prints only the top
matches, then the agent reads the one ``SKILL.md`` it actually needs.

Standard library only, no network, no API key — it must run wherever the
plugin was installed.

A collection may publish two retrievable corpora: single-paper leaf skills and
composite workflow super-skills that chain them. ``--target`` picks which.

    python bin/search_skills.py --query "align LC-MS peaks across samples"
    python bin/search_skills.py --tool SIRIUS --technique LC-MS -k 5
    python bin/search_skills.py --target workflows --query "untargeted pipeline"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COLLECTION_ROOT = Path(__file__).resolve().parent.parent

# What each retrievable corpus is called on disk. Adding one here is the only
# change a new corpus needs: nothing below names a target.
TARGETS = {
    "skills": {"index": "skills_index.json", "subdir": ""},
    "workflows": {"index": "workflows/workflows_index.json", "subdir": "workflows"},
}

STOPWORDS = frozenset(
    "a an and are as at be by for from how in is it of on or that the to use using "
    "with what which when data set my our this these those i need want".split()
)


def tokenize(text: str) -> set[str]:
    """Lowercase alphanumeric tokens, minus stopwords and one-character noise."""
    tokens = re.findall(r"[a-z0-9]+", str(text).lower())
    return {t for t in tokens if len(t) > 1 and t not in STOPWORDS}


def load_index(collection: Path, target: str) -> list[dict]:
    """Read a target's index from a collection root."""
    path = collection / TARGETS[target]["index"]
    if not path.is_file():
        raise SystemExit(f"this collection publishes no {target} ({path} is absent)")
    return json.loads(path.read_text(encoding="utf-8"))


def read_dir(collection: Path, target: str) -> str:
    """Directory the target's SKILL.md files are read from, relative to the root."""
    subdir = TARGETS[target]["subdir"]
    if subdir:
        return subdir
    return "leaves" if (collection / "leaves").is_dir() else "skills"


def entry_tools(entry: dict) -> list[str]:
    """Tool names, whichever field the index uses (leaves `tools`, workflows `member_tools`)."""
    for field in ("tools", "member_tools"):
        if entry.get(field):
            return [str(v) for v in entry[field]]
    return []


def matches_filters(entry: dict, technique: str | None, edam: str | None) -> bool:
    """True when the entry satisfies every supplied exact-match filter."""
    if technique and technique.lower() not in [
        str(t).lower() for t in entry.get("techniques") or []
    ]:
        return False
    if edam:
        fields = [str(entry.get("edam_operation") or "")] + [
            str(t) for t in entry.get("edam_topics") or []
        ]
        return any(edam.lower() in f.lower() for f in fields)
    return True


def score(entry: dict, wanted: set[str], tool: str | None) -> float:
    """Rank an entry: tool name matches count for more than prose overlap."""
    tools = [t.lower() for t in entry_tools(entry)]
    if tool and tool.lower() not in tools:
        return 0.0
    haystack = tokenize(f"{entry.get('name', '')} {entry.get('description', '')}")
    haystack |= tokenize(" ".join(tools))
    if not wanted:
        return 1.0
    overlap = len(wanted & haystack)
    boost = 2.0 if wanted & set(tools) else 0.0
    return overlap + boost


def search(index: list[dict], args: argparse.Namespace) -> list[tuple[float, dict]]:
    """Filter, score and rank index entries; best first."""
    wanted = tokenize(args.query or "")
    hits = [
        (score(e, wanted, args.tool), e)
        for e in index
        if matches_filters(e, args.technique, args.edam)
    ]
    hits = [(s, e) for s, e in hits if s > 0]
    hits.sort(key=lambda pair: (-pair[0], str(pair[1].get("slug"))))
    return hits[: args.k]


def format_hit(rank: int, entry: dict, leaf_dir: str) -> str:
    """One compact, greppable block per candidate skill."""
    tools = ", ".join(entry_tools(entry)[:6])
    desc = " ".join(str(entry.get("description") or "").split())
    stages = entry.get("stages") or []
    scope = f"stages: {' -> '.join(str(s) for s in stages)}" if stages else (
        f"tier: {entry.get('license_tier') or '-'}")
    return (
        f"{rank}. {entry.get('slug')}\n"
        f"   {desc}\n"
        f"   tools: {tools or '-'} | techniques: "
        f"{', '.join(entry.get('techniques') or []) or '-'} | {scope}\n"
        f"   read: {leaf_dir}/{entry.get('slug')}/SKILL.md"
    )


def build_parser() -> argparse.ArgumentParser:
    """CLI for the retrieval entry point."""
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--query", default="", help="free text describing the task")
    p.add_argument("--collection", default=str(COLLECTION_ROOT))
    p.add_argument("--target", choices=sorted(TARGETS), default="skills",
                   help="which corpus to search: single skills, or composite workflows")
    p.add_argument("--technique", help="exact technique tag, e.g. LC-MS")
    p.add_argument("--tool", help="exact tool name, e.g. SIRIUS")
    p.add_argument("--edam", help="substring of an EDAM operation/topic IRI")
    p.add_argument("-k", type=int, default=10, help="how many candidates to print")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    collection = Path(args.collection).resolve()
    hits = search(load_index(collection, args.target), args)
    if not hits:
        print("no match — loosen the filters or reword --query")
        return 1
    where = read_dir(collection, args.target)
    for rank, (_, entry) in enumerate(hits, 1):
        print(format_hit(rank, entry, where))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sample = [
            {"slug": "peak-align", "name": "Peak alignment",
             "description": "Align LC-MS peaks across samples",
             "tools": ["XCMS"], "techniques": ["LC-MS"], "license_tier": "open"},
            {"slug": "formula-id", "name": "Formula prediction",
             "description": "Predict molecular formulas from MS2",
             "tools": ["SIRIUS"], "techniques": ["LC-MS"], "license_tier": "open"},
        ]
        ns = build_parser().parse_args(["--query", "align peaks across samples"])
        assert search(sample, ns)[0][1]["slug"] == "peak-align"
        ns = build_parser().parse_args(["--tool", "SIRIUS"])
        got = search(sample, ns)
        assert len(got) == 1 and got[0][1]["slug"] == "formula-id"
        ns = build_parser().parse_args(["--technique", "GC-MS"])
        assert search(sample, ns) == []

        # A workflow row names its tools `member_tools` and carries stages.
        flows = [{"slug": "untargeted", "name": "Untargeted pipeline",
                  "description": "End-to-end untargeted LC-MS/MS annotation",
                  "member_tools": ["MZmine", "SIRIUS"], "techniques": ["LC-MS"],
                  "stages": ["preprocess", "annotate"]}]
        ns = build_parser().parse_args(["--target", "workflows", "--tool", "MZmine"])
        assert search(flows, ns)[0][1]["slug"] == "untargeted"
        assert "stages: preprocess -> annotate" in format_hit(1, flows[0], "workflows")
        print("search_skills.py smoke check OK", file=sys.stderr)
        raise SystemExit(0)
    raise SystemExit(main())
