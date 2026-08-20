#!/usr/bin/env python3
"""skill_map — embedding-space coverage + centrality map of a skill collection.

Reads a collection's leaf embedding cache and answers three questions a curator
needs before authoring the next super-skill:

  * COVERAGE  — what fraction of leaves is bound by at least one super-skill
    (workflow), and which regions of the skill space no super-skill reaches yet.
  * ISLANDS   — clusters of leaves that are FAR from every covered leaf, i.e.
    exactly where the next super-skills (or prunes) should go. Defined relative
    to coverage so it is percolation-free: only the uncovered frontier is
    clustered, never the whole dense space.
  * CENTRALITY — hubs (leaves many others call a nearest neighbour) and core
    (leaves closest to the global centroid): the load-bearing "key skills".

Emits ``skill_map_report.json`` (schema mirrors ``curation_report.json``).
Descriptive by default; ``--strict`` exits 1 only on a real integrity failure
(a cache that matches none of the index).

Two disciplines this file keeps (from the 2026-06-17 overfit audit):
  * ``None`` != ``0`` — a missing cache or no super-skills is reported
    ``not_applicable``/loudly, never a silent "0 islands / 100% covered".
  * No domain vocabulary (generalize-or-stop rule 5) — every path, slug and DOI
    comes from the collection on disk; none is written into this file.

Coverage %, hubs and core are exact and clustering-independent; only island
GROUPING uses a heuristic (mutual-kNN components of the uncovered frontier).

Dependencies: numpy + pyyaml. Run under
``uv run --with numpy --with pyyaml`` where those are not on the base interpreter.

Usage:
  python skill_map.py <collection_dir> [--cache PATH] [--workflows PATH]
      [--report PATH] [--knn N] [--island-sim F] [--link-sim F] [--top N]
      [--coords] [--strict] [--quiet]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - depends on how the repo was installed
    raise SystemExit("skill_map needs numpy: pip install -e '.[analysis]'")
import yaml

# Nearest neighbours per leaf for the kNN graph + hub in-degree.
DEFAULT_KNN = 15
# A leaf is on the "uncovered frontier" (island candidate) when its best cosine
# to ANY covered leaf is below this — no super-skill reaches its neighbourhood.
DEFAULT_ISLAND_SIM = 0.55
# Within that frontier, two leaves join the same island when their mutual-kNN
# cosine clears this. Only the sparse frontier is clustered, so it cannot
# percolate the way clustering the whole dense space would.
DEFAULT_LINK_SIM = 0.72
# How many hub / core / method-dense entries to list.
DEFAULT_TOP = 15
# An island smaller than this is noise, not a coverage gap worth an entry.
MIN_ISLAND_SIZE = 5
# One island holding more than this fraction of all leaves means the frontier
# clustering percolated (thresholds too loose) — flagged, never left silent.
PERCOLATION_FRAC = 0.15
_EPS = 1e-9


def finding(check: str, severity: str, target: str, detail: str) -> dict:
    """One structural problem with the map. severity is 'fail' or 'warn'."""
    return {"check": check, "severity": severity, "target": target, "detail": detail}


def norm_doi(doi: str) -> str:
    """Lower-case a DOI and drop any resolver prefix (for grouping)."""
    d = str(doi).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d


def default_cache_path(collection_dir: str) -> str:
    """The cache path build_leaf_embedding_cache.py writes for a collection."""
    name = os.path.basename(os.path.normpath(collection_dir))
    return os.path.join(collection_dir, ".cache", f"leafemb_{name}.npz")


def load_index(collection_dir: str) -> list:
    """Load the leaf skills_index.json for a collection."""
    with open(os.path.join(collection_dir, "skills_index.json")) as fh:
        return json.load(fh)


def load_cache(path: str):
    """Return (emb float32[N,D], slugs list[str]) from an .npz, or (None, None)."""
    if not os.path.exists(path):
        return None, None
    data = np.load(path, allow_pickle=True)
    return data["emb"].astype(np.float32), [str(s) for s in data["slug"]]


def align_to_index(emb, cache_slugs: list, index_slugs: list):
    """Keep only cached rows whose slug is in the index; L2-normalise them.

    Returns (X, slugs) restricted+reordered to the intersection, so a stale slug
    left in the cache after a purge never inflates the map.
    """
    wanted = set(index_slugs)
    keep = [i for i, s in enumerate(cache_slugs) if s in wanted]
    sub = emb[keep]
    norms = np.linalg.norm(sub, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (sub / norms).astype(np.float32), [cache_slugs[i] for i in keep]


def knn_graph(X, k: int):
    """Return (knn_idx[N,k], knn_sim[N,k]) sorted nearest-first per row.

    Cosine == dot product for L2-normalised X. The diagonal is masked so a leaf
    is never its own neighbour.
    """
    k = min(k, X.shape[0] - 1)
    sim = X @ X.T
    np.fill_diagonal(sim, -2.0)  # below any real cosine [-1,1] -> self never a neighbour
    idx = np.argpartition(-sim, k, axis=1)[:, :k]
    picked = np.take_along_axis(sim, idx, axis=1)
    order = np.argsort(-picked, axis=1)
    return np.take_along_axis(idx, order, axis=1), np.take_along_axis(picked, order, axis=1)


class _DSU:
    """Minimal union-find for connected components."""

    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def mutual_knn_components(knn_idx, knn_sim, threshold: float) -> list:
    """Connected components of the mutual-kNN graph above a cosine threshold.

    An edge (i, j) is kept only when each is in the other's kNN and the cosine
    clears the threshold — symmetric, deterministic, no extra dependency.
    Returned largest-first.
    """
    n = len(knn_idx)
    neighbours = [set(int(j) for j in row) for row in knn_idx]
    dsu = _DSU(n)
    for i in range(n):
        for pos in range(len(knn_idx[i])):
            j = int(knn_idx[i][pos])
            if knn_sim[i][pos] >= threshold and i in neighbours[j]:
                dsu.union(i, j)
    groups = defaultdict(list)
    for i in range(n):
        groups[dsu.find(i)].append(i)
    return sorted(groups.values(), key=len, reverse=True)


def hub_in_degree(knn_idx) -> Counter:
    """How many leaves call each leaf a nearest neighbour (kNN in-degree)."""
    counts = Counter()
    for row in knn_idx:
        for j in row:
            counts[int(j)] += 1
    return counts


def core_closeness(X):
    """Cosine of every leaf to the global centroid (domain-core score)."""
    centroid = X.mean(0)
    centroid /= np.linalg.norm(centroid) + _EPS
    return X @ centroid


def exemplar(members: list, X, slugs: list) -> str:
    """Slug of the leaf nearest a group's centroid (its representative)."""
    centroid = X[members].mean(0)
    centroid /= np.linalg.norm(centroid) + _EPS
    sims = X[members] @ centroid
    return slugs[members[int(np.argmax(sims))]]


def parse_workflow_coverage(workflows_dir: str) -> list:
    """Return [(workflow_name, {leaf_slug, ...}), ...] from workflows/*/workflow.yaml.

    Reads the leaf slugs each super-skill binds (``steps[].skills[]``). A
    workflow that binds no leaves is skipped, not counted as empty coverage.
    """
    out = []
    for wf in sorted(glob.glob(os.path.join(workflows_dir, "*", "workflow.yaml"))):
        try:
            doc = yaml.safe_load(open(wf)) or {}
        except yaml.YAMLError:
            continue
        steps = doc.get("steps") if isinstance(doc, dict) else None
        if not isinstance(steps, list):
            continue  # top-level list/scalar, or steps not a list -> no coverage
        skills = set()
        for step in steps:
            if not isinstance(step, dict):
                continue
            slug_list = step.get("skills")
            for slug in slug_list if isinstance(slug_list, list) else []:
                if isinstance(slug, str):
                    skills.add(slug)
        if skills:
            out.append((os.path.basename(os.path.dirname(wf)), skills))
    return out


def covered_indices(aligned_slugs: list, workflow_sets: list) -> set:
    """Indices of leaves bound by at least one super-skill."""
    pos = {s: i for i, s in enumerate(aligned_slugs)}
    covered = set()
    for _, skills in workflow_sets:
        covered.update(pos[s] for s in skills if s in pos)
    return covered


def coverage_distance(X, covered: set):
    """Best cosine from each leaf to any covered leaf (None if none covered)."""
    if not covered:
        return None
    cov = X[sorted(covered)]
    return (X @ cov.T).max(axis=1)


def _leaf_list(leaf: dict, field: str) -> list:
    """A leaf's list-valued field, or [] if absent/malformed (never a string).

    A string is iterable, so treating a string field as a list would silently
    count it per-character; callers must never do that.
    """
    val = leaf.get(field)
    return val if isinstance(val, list) else []


def _top_counts(members: list, index_by_slug: dict, slugs: list, field: str, n: int) -> list:
    """Most common values of a list-valued leaf field across a group."""
    counter = Counter()
    for m in members:
        for val in _leaf_list(index_by_slug[slugs[m]], field):
            counter[val] += 1
    return [v for v, _ in counter.most_common(n)]


def find_islands(X, slugs, index_by_slug, covered, island_sim, link_sim, knn):
    """Cluster the uncovered frontier (leaves far from all coverage) into islands.

    Returns None when coverage is unknown (no super-skills) — islands are then
    undefined, not zero. Only the frontier is clustered, so it never percolates.
    """
    dist = coverage_distance(X, covered)
    if dist is None:
        return None
    frontier = [i for i in range(len(slugs)) if dist[i] < island_sim]
    if len(frontier) < 2:
        return []
    sub_idx, sub_sim = knn_graph(X[frontier], knn)
    islands = []
    for comp in mutual_knn_components(sub_idx, sub_sim, link_sim):
        if len(comp) < MIN_ISLAND_SIZE:
            continue
        members = [frontier[m] for m in comp]  # map back to global indices
        islands.append({
            "size": len(members),
            "exemplar": exemplar(members, X, slugs),
            "top_techniques": _top_counts(members, index_by_slug, slugs, "techniques", 2),
            "top_tools": _top_counts(members, index_by_slug, slugs, "tools", 4),
        })
    return sorted(islands, key=lambda r: r["size"], reverse=True)


def pca_2d(X):
    """Top-2 principal-component coordinates (numpy-only, for a 2-D map)."""
    centered = X - X.mean(0)
    _, components = np.linalg.eigh(centered.T @ centered)
    top2 = components[:, -2:][:, ::-1]
    return centered @ top2


def _coverage_block(slugs: list, covered: set, workflow_sets: list) -> dict:
    """Coverage summary; not_applicable when no super-skill binds any leaf."""
    if not workflow_sets:
        return {"status": "not_applicable", "covered": 0, "total": len(slugs),
                "pct": None, "n_workflows": 0}
    total = len(slugs)
    return {"status": "ok", "covered": len(covered), "total": total,
            "pct": round(100.0 * len(covered) / total, 1) if total else None,
            "n_workflows": len(workflow_sets)}


def analyse(index: list, X, slugs: list, workflow_sets, knn: int,
            island_sim: float, link_sim: float, top: int, with_coords: bool) -> dict:
    """Compute the full map over aligned embeddings. Pure — no filesystem."""
    index_by_slug = {r["slug"]: r for r in index if r.get("slug")}
    knn_idx, _ = knn_graph(X, knn)
    covered = covered_indices(slugs, workflow_sets)
    indeg = hub_in_degree(knn_idx)
    closeness = core_closeness(X)
    islands = find_islands(X, slugs, index_by_slug, covered, island_sim, link_sim, knn)

    hubs = [{"slug": slugs[i], "in_degree": indeg[i]} for i, _ in indeg.most_common(top)]
    core = [{"slug": slugs[i], "closeness": round(float(closeness[i]), 4)}
            for i in np.argsort(-closeness)[:top]]
    doi_leaves = Counter()
    for s in slugs:
        for doi in _leaf_list(index_by_slug[s], "dois"):
            doi_leaves[norm_doi(doi)] += 1

    out = {
        "n_leaves_index": len(index),
        "n_aligned": len(slugs),
        "coverage": _coverage_block(slugs, covered, workflow_sets),
        "islands_status": "not_applicable" if islands is None else "ok",
        "islands": islands or [],
        "hubs": hubs,
        "core": core,
        "method_dense_papers": [{"doi": d, "leaves": c} for d, c in doi_leaves.most_common(top)],
    }
    if with_coords:
        coords = pca_2d(X)
        out["coords"] = {slugs[i]: [round(float(coords[i, 0]), 4), round(float(coords[i, 1]), 4)]
                         for i in range(len(slugs))}
    return out


def map_findings(body: dict) -> list:
    """Non-fatal signals: missing embeddings degrade retrieval; a giant island
    means the frontier clustering percolated (thresholds too loose)."""
    findings = []
    n, n_index = body.get("n_aligned", 0), body.get("n_leaves_index", 0)
    if n_index and n < n_index:
        findings.append(finding("alignment", "warn", "<cache>",
                                f"{n_index - n} indexed leaves have no embedding "
                                "(they fall back to keyword retrieval)"))
    islands = body.get("islands") or []
    if n and islands and islands[0]["size"] > PERCOLATION_FRAC * n:
        findings.append(finding("percolation", "warn", islands[0]["exemplar"],
                                f"largest island holds {islands[0]['size']}/{n} leaves; "
                                "tighten --island-sim/--link-sim (island split unreliable)"))
    cov = body.get("coverage") or {}
    if cov.get("status") == "ok" and cov.get("n_workflows") and cov.get("covered") == 0:
        findings.append(finding("coverage", "warn", "<workflows>",
                                f"{cov['n_workflows']} super-skills bind no leaf present in "
                                "the index (dangling slug references?)"))
    return findings


def build_report(collection_dir: str, body: dict | None, status: str, findings: list) -> dict:
    """Assemble skill_map_report.json (body is None when not analysable)."""
    report = {
        "schema": "asbb-skill-map-report/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collection_dir": collection_dir,
        "overall_status": status,
        "findings": findings,
    }
    if body is not None:
        report.update(body)
    return report


def print_summary(report: dict) -> None:
    """Human one-screen summary of the map."""
    print(f"skill_map: {report['collection_dir']} -> {report['overall_status'].upper()}")
    if "n_aligned" not in report:
        for f in report["findings"]:
            print(f"  [{f['severity']}] {f['target']}: {f['detail']}")
        return
    cov = report["coverage"]
    cov_str = ("n/a (no super-skills bind any leaf)" if cov["status"] == "not_applicable"
               else f"{cov['covered']}/{cov['total']} ({cov['pct']}%) by {cov['n_workflows']} super-skills")
    print(f"  leaves aligned: {report['n_aligned']}/{report['n_leaves_index']}")
    print(f"  coverage: {cov_str}")
    if report["islands_status"] == "not_applicable":
        print("  islands: n/a (coverage unknown)")
    else:
        print(f"  islands (uncovered clusters >= {MIN_ISLAND_SIZE}): {len(report['islands'])}")
        for isl in report["islands"][:10]:
            print(f"    n={isl['size']:4d}  {isl['exemplar']}  "
                  f"techs={isl['top_techniques']} tools={isl['top_tools']}")
    print("  top hub skills:")
    for h in report["hubs"][:5]:
        print(f"    in-deg={h['in_degree']:3d}  {h['slug']}")
    print("  domain-core skills:")
    for c in report["core"][:5]:
        print(f"    {c['closeness']:.3f}  {c['slug']}")
    for f in report["findings"]:
        print(f"  [{f['severity']}] {f['target']}: {f['detail']}")


def run(collection_dir: str, cache_path: str, workflows_dir: str, knn: int,
        island_sim: float, link_sim: float, top: int, with_coords: bool) -> dict:
    """Load, analyse and assemble the report for one collection."""
    index = load_index(collection_dir)
    if not isinstance(index, list) or not all(isinstance(r, dict) for r in index):
        f = finding("index", "fail", "skills_index.json",
                    "not a JSON list of leaf objects (cannot map the skill space)")
        return build_report(collection_dir, None, "fail", [f])
    emb, cache_slugs = load_cache(cache_path)
    if emb is None:
        f = finding("cache", "warn", cache_path, "no embedding cache found "
                    "(it is a release asset; run build_leaf_embedding_cache.py)")
        return build_report(collection_dir, None, "not_applicable", [f])
    X, slugs = align_to_index(emb, cache_slugs, [r["slug"] for r in index if r.get("slug")])
    if not slugs:
        f = finding("alignment", "fail", cache_path,
                    "no cached slug matches the index (wrong collection cache?)")
        return build_report(collection_dir, None, "fail", [f])

    workflow_sets = parse_workflow_coverage(workflows_dir) if os.path.isdir(workflows_dir) else []
    body = analyse(index, X, slugs, workflow_sets, knn, island_sim, link_sim, top, with_coords)
    findings = map_findings(body)
    if not os.path.isdir(workflows_dir):
        findings.append(finding("coverage", "warn", workflows_dir,
                                "no workflows/ dir (coverage + islands not evaluated)"))
    status = "warn" if findings else "pass"
    return build_report(collection_dir, body, status, findings)


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill_map.py",
        description="Embedding-space coverage + centrality map of a skill collection.")
    parser.add_argument("collection_dir", help="Collection dir, e.g. collections/<slug>/v<N>")
    parser.add_argument("--cache", default=None,
                        help="Embedding .npz (default: <collection>/.cache/leafemb_<name>.npz)")
    parser.add_argument("--workflows", default=None,
                        help="Super-skill workflows dir (default: <collection>/workflows)")
    parser.add_argument("--report", default=None,
                        help="Where to write skill_map_report.json "
                             "(default: <collection>/skill_map_report.json)")
    parser.add_argument("--knn", type=int, default=DEFAULT_KNN)
    parser.add_argument("--island-sim", type=float, default=DEFAULT_ISLAND_SIM,
                        help="Leaf is an island candidate when its best cosine to any "
                             f"covered leaf is below this (default {DEFAULT_ISLAND_SIM}).")
    parser.add_argument("--link-sim", type=float, default=DEFAULT_LINK_SIM,
                        help=f"Frontier clustering linkage cosine (default {DEFAULT_LINK_SIM}).")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP)
    parser.add_argument("--coords", action="store_true",
                        help="Add PCA-2D coordinates per leaf (for a 2-D map).")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on a FAIL finding (cache matches none of the index).")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.collection_dir):
        print(f"error: not a directory: {args.collection_dir}", file=sys.stderr)
        return 2
    cache_path = args.cache or default_cache_path(args.collection_dir)
    workflows_dir = args.workflows or os.path.join(args.collection_dir, "workflows")

    try:
        report = run(args.collection_dir, cache_path, workflows_dir, args.knn,
                     args.island_sim, args.link_sim, args.top, args.coords)
    except FileNotFoundError as exc:
        print(f"error: missing collection file: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: malformed skills_index.json: {exc}", file=sys.stderr)
        return 2
    out = args.report or os.path.join(args.collection_dir, "skill_map_report.json")
    try:
        with open(out, "w") as fh:
            json.dump(report, fh, indent=2)
    except OSError as exc:
        print(f"error: cannot write report to {out}: {exc}", file=sys.stderr)
        return 2
    if not args.quiet:
        print_summary(report)
        print(f"  report: {out}")

    return 1 if (args.strict and report["overall_status"] == "fail") else 0


def _selftest() -> None:
    """Smoke check on synthetic embeddings — no filesystem, no domain vocabulary."""
    rng = np.random.default_rng(0)
    dim = 32
    centres = np.eye(3, dim)  # three well-separated clusters
    slugs, rows, index = [], [], []
    for cl in range(3):
        for k in range(6):
            slug = f"c{cl}_{k}"
            slugs.append(slug)
            rows.append(centres[cl] + 0.01 * rng.standard_normal(dim))
            index.append({"slug": slug, "tools": [f"tool{cl}"], "techniques": [f"tech{cl}"],
                          "dois": ["10.1/x"], "description": f"cluster {cl} leaf {k}"})
    emb = np.asarray(rows, dtype=np.float32)
    X, aligned = align_to_index(emb, slugs, [r["slug"] for r in index])
    assert aligned == slugs

    # One super-skill covers cluster 0 -> clusters 1 & 2 are the uncovered frontier.
    wf = [("w0", {f"c0_{k}" for k in range(6)})]
    body = analyse(index, X, aligned, wf, knn=5, island_sim=0.5, link_sim=0.5, top=5, with_coords=True)
    assert body["coverage"]["covered"] == 6, body["coverage"]
    techs = {t for isl in body["islands"] for t in isl["top_techniques"]}
    assert techs == {"tech1", "tech2"}, techs        # covered cluster is NOT an island
    assert len(body["hubs"]) == 5 and len(body["core"]) == 5
    assert len(body["coords"]) == len(slugs)

    # None != 0: no super-skills -> coverage + islands not_applicable, not 0.
    empty = analyse(index, X, aligned, [], knn=5, island_sim=0.5, link_sim=0.5, top=5, with_coords=False)
    assert empty["coverage"]["status"] == "not_applicable"
    assert empty["islands_status"] == "not_applicable" and empty["islands"] == []

    # Full coverage -> a known-but-empty frontier (0 islands), distinct from unknown.
    wf_all = [("w", set(slugs))]
    full = analyse(index, X, aligned, wf_all, knn=5, island_sim=0.5, link_sim=0.5, top=5, with_coords=False)
    assert full["islands_status"] == "ok" and full["islands"] == []

    # Missing cache -> whole map not_applicable (loud), never a clean empty map.
    rep = build_report("d", None, "not_applicable", [finding("cache", "warn", "x", "missing")])
    assert rep["overall_status"] == "not_applicable" and "n_aligned" not in rep

    # Alignment warn: an indexed leaf with no embedding is flagged.
    assert map_findings({"n_aligned": 9, "n_leaves_index": 10})[0]["severity"] == "warn"
    # Percolation warn: one island swallowing most leaves is never left silent.
    perc = map_findings({"n_aligned": 100, "n_leaves_index": 100,
                         "islands": [{"size": 40, "exemplar": "x"}]})
    assert any(f["check"] == "percolation" for f in perc), perc
    print("skill_map self-test: OK")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        _selftest()
    else:
        sys.exit(main())
