"""Resolve each corpus entry's tool license via the GitHub license API and write
license_tier (+ raw access.license) into corpus.yaml. Network; cache-backed.

The OA axis (access.type) is NOT changed here — only access.license (raw SPDX) is
filled and license_tier added. No resolvable license -> restricted (by design).
"""
from __future__ import annotations

import json
import pathlib
import re
import urllib.error
import urllib.request

import yaml

from scripts.license_tier import tier_for_license

_GH_API = "https://api.github.com/repos/{}/{}/license"


def parse_repo(repo_url: str):
    """Extract (owner, repo) from a GitHub URL or 'owner/repo'; None if not GitHub."""
    if not repo_url:
        return None
    s = repo_url.strip().rstrip(";,. ")
    m = re.search(r"github\.com[/:]([^/]+)/([^/#?]+?)(?:\.git)?(?:[/#?].*)?$", s)
    if m:
        return m.group(1), m.group(2)
    m = re.fullmatch(r"([\w.-]+)/([\w.-]+)", s)
    return (m.group(1), m.group(2)) if m else None


def _gh_fetch(owner: str, repo: str, token: str | None) -> str | None:
    """Return the repo's SPDX id via the GitHub license API, or None (404/none)."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(_GH_API.format(owner, repo), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    spdx = (data.get("license") or {}).get("spdx_id")
    return None if spdx in (None, "NOASSERTION") else spdx


def tier_for_repo(repo_url, token=None, cache=None, _fetch=_gh_fetch):
    """(tier, spdx) for a repo URL. No repo or no license -> ('restricted', None)."""
    pr = parse_repo(repo_url)
    if not pr:
        return ("restricted", None)
    key = f"{pr[0]}/{pr[1]}"
    if cache is not None and key in cache:
        spdx = cache[key]
    else:
        spdx = _fetch(pr[0], pr[1], token)
        if cache is not None:
            cache[key] = spdx
    return (tier_for_license(spdx or ""), spdx)


def apply_to_corpus(corpus_path, token, cache=None, _fetch=_gh_fetch) -> dict:
    """Write license_tier + access.license into every corpus entry. Returns {tier:count}."""
    path = pathlib.Path(corpus_path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    summary: dict[str, int] = {}
    for p in doc.get("papers", []):
        if p.get("license_locked"):
            t = p.get("license_tier", "restricted")
            summary[t] = summary.get(t, 0) + 1
            continue
        tier, spdx = tier_for_repo(p.get("repo_url"), token=token, cache=cache, _fetch=_fetch)
        p["license_tier"] = tier
        p.setdefault("access", {})
        p["access"]["license"] = spdx
        summary[tier] = summary.get(tier, 0) + 1
    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return summary


def _load_cache(p):
    cp = pathlib.Path(p)
    return json.loads(cp.read_text()) if cp.is_file() else {}


def main(argv=None) -> int:
    import argparse
    import os
    import subprocess
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--cache", default=".license-cache.json")
    args = ap.parse_args(argv)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        try:
            token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip() or None
        except Exception:
            token = None
    cache = _load_cache(args.cache)
    summary = apply_to_corpus(args.corpus, token, cache=cache)
    pathlib.Path(args.cache).write_text(json.dumps(cache, indent=2))
    print(json.dumps({"corpus": args.corpus, "tiers": summary, "authenticated": bool(token)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
