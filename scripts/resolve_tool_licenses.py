"""Resolve each tool's own licence and repository, and write tool_licenses.json.

`enrich_tools_index.py` reads that file and refuses to tier a tool without it, so
this script is where a tool's licence is allowed to come from. Two routes, both
requiring evidence about the tool itself (issue #43):

- `self_published`  the tool is the subject of a paper already in the corpus, so
                    that paper's repository is the tool's repository and the
                    licence resolved from it is the tool's licence. Offline.
- `registry`        the tool's name matches a package in a curated life-science
                    registry (governance/tool_registries.yaml). Network, cached.

Where both fire they are compared. The registry wins a disagreement over the
licence string, because a package declares its own licence and a repository read
only infers one. A disagreement in *tier* is a contradiction rather than an
override: the tool resolves to nothing and is reported. Anything unresolved stays
`unknown`, which is a true statement.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

import yaml
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.derive_license_tiers import classify_license_text, spdx_from_r_license_field
from scripts.license_tier import (SUBJECT_TOOL, UNESTABLISHED_DETECTIONS, licence_subject,
                                  load_map, tier_for_license)

_REGISTRIES = pathlib.Path(__file__).resolve().parent.parent / "governance" / "tool_registries.yaml"
_USER_AGENT = "asb-skill-collections tool-licence-resolver"


def normalize(text) -> str:
    """Lower-case alphanumerics only: the comparison key for names."""
    return re.sub(r"[^a-z0-9]", "", str(text or "").lower())


def load_registries(path=None) -> list:
    """Registry definitions from governance/tool_registries.yaml."""
    return load_registry_config(path).get("registries") or []


def load_registry_config(path=None) -> dict:
    """The whole registry governance document."""
    return yaml.safe_load(pathlib.Path(path or _REGISTRIES).read_text(encoding="utf-8")) or {}


def excluded_pairs(config) -> set:
    """``{(tool_slug, registry_id)}`` a human reviewed and rejected.

    Name collisions that no current signal separates from correct matches; each
    carries a reason in governance/tool_registries.yaml. Held as data so the
    rejection is reviewable and the resolver stays free of tool names.
    """
    return {(e.get("tool"), e.get("registry")) for e in (config.get("excluded_matches") or [])}


# --------------------------------------------------------------------------- #
# Route A -- the tool is the subject of a corpus paper                         #
# --------------------------------------------------------------------------- #

def introducing_paper(tool, papers) -> dict | None:
    """The corpus paper that introduces this tool, or None.

    Matched on exact normalized name equality, never substring: `XCMS Online` and
    `XCMS` are different tools, and a substring rule would merge them.
    """
    target = normalize(tool.get("name"))
    if not target:
        return None
    for doi in tool.get("dois") or []:
        paper = papers.get(doi)
        if paper and normalize(paper.get("name")) == target:
            return paper
    return None


def self_published_evidence(tool, papers) -> dict | None:
    """Licence evidence from the repository of the paper that introduces the tool.

    Only accepted when the corpus entry's licence is about the *tool* -- a paper
    whose licence came from Crossref describes the publication, and inheriting it
    is the defect issue #42 fixed.
    """
    paper = introducing_paper(tool, papers)
    if not paper or licence_subject(paper) != SUBJECT_TOOL:
        return None
    detection = paper.get("license_detection")
    licence = (paper.get("access") or {}).get("license")
    if detection in UNESTABLISHED_DETECTIONS or not licence:
        return None
    return {"license": licence, "license_detection": detection,
            "repo_url": paper.get("repo_url"), "route": "self_published",
            "matched": paper.get("name")}


# --------------------------------------------------------------------------- #
# Route B -- the tool is a package in a curated life-science registry           #
# --------------------------------------------------------------------------- #

def fetch_json(url, cache_dir, key):
    """GET url as JSON, memoised on disk so re-runs are offline and deterministic."""
    cache = pathlib.Path(cache_dir) / f"{key}.json"
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read())
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return None
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(payload), encoding="utf-8")
    return payload


def registry_names(registry, cache_dir) -> dict:
    """``{normalized_name: canonical_name}`` for one registry, or {} if unreachable."""
    payload = fetch_json(registry["index_url"], cache_dir, f"{registry['id']}-index")
    if payload is None:
        return {}
    if registry["index_shape"] == "packages_map":
        payload = list((payload.get("packages") or {}).keys())
    return {normalize(n): n for n in payload if normalize(n)}


def registry_record(registry, canonical, cache_dir) -> dict | None:
    """The registry's metadata for one package."""
    if registry["index_shape"] == "packages_map":
        index = fetch_json(registry["index_url"], cache_dir, f"{registry['id']}-index") or {}
        return (index.get("packages") or {}).get(canonical)
    url = registry["package_url"].format(name=urllib.parse.quote(canonical))
    return fetch_json(url, cache_dir, f"{registry['id']}-{normalize(canonical)}")


def spdx_from_registry(value, license_format, _map=None) -> str | None:
    """Registry licence string to an SPDX id, or None when it is not recognised.

    None rather than the `restricted` fallback on purpose: a licence we could not
    read is not a licence we established, and `tier_for_license` would turn LGPL
    prose into a verdict.
    """
    if not value or not str(value).strip():
        return None
    if license_format == "r_description_field":
        return spdx_from_r_license_field(str(value), _map)
    text = str(value).strip()
    known = {k.lower(): k for k in ((_map or load_map()).get("spdx") or {})}
    return known.get(text.lower()) or classify_license_text(text)


def candidate_names(tool) -> list:
    """Names to try against a registry index, most canonical first."""
    names = [tool.get("slug"), tool.get("name")]
    return [n for n in names if n]


_CODE_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org")
_REPO_ROOT = re.compile(
    r"(https?://(?:www\.)?(?:" + "|".join(h.replace(".", r"\.") for h in _CODE_HOSTS) +
    r")/[^/\s,;]+/[^/\s,;#?]+?)(?:\.git)?(?:/(?:issues|pulls|tree|blob|wiki)\b.*)?/?$",
    re.I)


def pick_repo_url(values):
    """The repository among a registry's declared URLs, canonicalised, or None.

    Registries mix a project homepage, an issue tracker and a git remote into the
    same fields, and the field here is called `repo_url`. CAMERA declares a lab web
    page as `URL` and `.../CAMERA/issues/new` as `BugReports`; the answer to "where
    do I read the source" is the second one with its tracker path removed.
    """
    for value in values:
        for candidate in re.split(r"[,\s]+", str(value).strip()):
            match = _REPO_ROOT.match(candidate.rstrip("/"))
            if match:
                return match.group(1)
    return next((str(v).split(",")[0].strip() for v in values if v), None)


def registry_evidence(tool, registries, indexes, cache_dir, _map=None, excluded=()) -> dict | None:
    """Licence evidence from the first curated registry that carries this package."""
    for registry in registries:
        if (tool.get("slug"), registry["id"]) in excluded:
            continue
        index = indexes.get(registry["id"]) or {}
        canonical = next((index[normalize(n)] for n in candidate_names(tool)
                          if normalize(n) in index), None)
        if not canonical:
            continue
        record = registry_record(registry, canonical, cache_dir) or {}
        spdx = spdx_from_registry(record.get(registry["license_field"]),
                                  registry["license_format"], _map)
        if not spdx:
            continue
        values = [record.get(f) for f in registry["repo_fields"] if record.get(f)]
        return {"license": spdx, "license_detection": registry["detection"],
                "repo_url": pick_repo_url(values), "route": f"registry:{registry['id']}",
                "matched": canonical}
    return None


# --------------------------------------------------------------------------- #
# Reconciliation                                                               #
# --------------------------------------------------------------------------- #

def reconcile(self_published, registry, _map=None) -> tuple:
    """(evidence, conflict) from the two routes.

    Where both fire, the registry wins. A registry states the licence the package
    declares for itself; the repository route reads a LICENSE file, and for a
    packaged tool that file is often narrower than the package. `sneumann/xcms`
    is the case in point: DESCRIPTION says `GPL (>= 2)`, GitHub reports
    NOASSERTION, and the LICENSE file classifies as LGPL-3.0 because it carries
    terms for a bundled component. The same reasoning already sits in
    governance/license_tiers.yaml, which is why `r_license_aliases` exists.

    A disagreement in *tier* is not an override but a contradiction: the two
    sources would give a consumer materially different advice, so the tool
    resolves to nothing and the conflict is reported.
    """
    if not self_published or not registry:
        return self_published or registry, None
    if tier_for_license(self_published["license"], _map) != \
            tier_for_license(registry["license"], _map):
        return None, {"self_published": self_published, "registry": registry}
    evidence = dict(registry)
    if not evidence.get("repo_url"):
        evidence["repo_url"] = self_published.get("repo_url")
    if self_published["license"] != registry["license"]:
        evidence["superseded"] = {"license": self_published["license"],
                                  "license_detection": self_published["license_detection"]}
    return evidence, None


def resolve(collection_dir, cache_dir, registries=None) -> dict:
    """Write tool_licenses.json for a collection and return a summary."""
    d = pathlib.Path(collection_dir)
    tools = json.loads((d / "tools_index.json").read_text(encoding="utf-8"))
    corpus = yaml.safe_load((d / "corpus.yaml").read_text(encoding="utf-8"))
    papers = {p["doi"]: p for p in corpus.get("papers", []) if p.get("doi")}
    config = load_registry_config()
    registries = registries if registries is not None else (config.get("registries") or [])
    excluded = excluded_pairs(config)
    tier_map = load_map()
    indexes = {r["id"]: registry_names(r, cache_dir) for r in registries}

    resolved, conflicts = {}, {}
    for tool in tools:
        evidence, conflict = reconcile(
            self_published_evidence(tool, papers),
            registry_evidence(tool, registries, indexes, cache_dir, tier_map, excluded),
            tier_map)
        if conflict:
            conflicts[tool["slug"]] = conflict
        elif evidence:
            resolved[tool["slug"]] = evidence

    (d / "tool_licenses.json").write_text(
        json.dumps(dict(sorted(resolved.items())), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    routes: dict[str, int] = {}
    for e in resolved.values():
        routes[e["route"]] = routes.get(e["route"], 0) + 1
    return {"tools": len(tools), "resolved": len(resolved),
            "reviewed_exclusions": len(excluded),
            "cross_checked": sum(1 for e in resolved.values() if "superseded" in e),
            "conflicts": conflicts, "routes": dict(sorted(routes.items())),
            "index_sizes": {k: len(v) for k, v in indexes.items()}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collection", required=True,
                    help="collection dir with tools_index.json and corpus.yaml")
    ap.add_argument("--cache", default=".cache/tool-registries",
                    help="where registry responses are memoised (default: .cache/tool-registries)")
    args = ap.parse_args(argv)
    print(json.dumps(resolve(args.collection, args.cache), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
