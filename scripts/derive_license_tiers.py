"""Resolve each corpus entry's tool license via the GitHub license API and write
license_tier (+ raw access.license) into corpus.yaml. Network; cache-backed.

The OA axis (access.type) is NOT changed here — only access.license (raw SPDX) is
filled and license_tier added. No resolvable license -> restricted (by design).
"""
from __future__ import annotations

import base64
import json
import pathlib
import re
import urllib.error
import urllib.request

import yaml
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))


from scripts.license_tier import (SUBJECT_PAPER, SUBJECT_TOOL, UNESTABLISHED_DETECTIONS,
                                  licence_subject, load_map, tier_for_license)

_GH_API = "https://api.github.com/repos/{}/{}/license"
_LICENSE_FILE_RE = re.compile(r"^(licen[sc]e|copying|notice)(\.[\w.-]+)?$", re.I)

# Ordered: most specific first; noncommercial BEFORE generic CC-BY.
_TEXT_RULES = [
    ("AGPL-3.0",     ["affero general public"]),
    ("LGPL-3.0",     ["lesser general public", "library general public"]),
    ("GPL-3.0",      ["gnu general public"]),               # tier-equivalent across GPL versions
    ("Apache-2.0",   ["apache license"]),
    ("MPL-2.0",      ["mozilla public license"]),
    ("MIT",          ["mit license", "permission is hereby granted, free of charge"]),
    ("BSD-3-Clause", ["redistribution and use in source and binary"]),
    ("ISC",          ["isc license"]),
    ("Unlicense",    ["this is free and unencumbered software released into the public domain"]),
    ("CC-BY-NC-4.0", ["attribution-noncommercial", "cc by-nc"]),  # high-confidence CC-BY-NC phrases only; ambiguous "noncommercial" mentions fall through to file-present-unclassified
    ("CC-BY-4.0",    ["creative commons attribution", "creativecommons.org/licenses/by/", "cc by"]),
]


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


def classify_license_text(text: str):
    """SPDX-ish id from license text, or None."""
    if not text:
        return None
    low = " ".join(text.lower().split())
    for spdx, needles in _TEXT_RULES:
        if any(n in low for n in needles):
            return spdx
    return None


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


def _gh_contents(owner, repo, token):
    """Root filenames via the GitHub contents API; [] on 404/error."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/contents", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return [item.get("name", "") for item in json.loads(r.read())]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise


def _gh_file(owner, repo, path, token):
    """Raw file text via the contents API (base64), or '' on failure."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        return base64.b64decode(data.get("content", "")).decode("utf-8", "replace")
    except Exception:
        return ""


_R_DESCRIPTION = "DESCRIPTION"
_R_LICENSE_FIELD = re.compile(r"^License:\s*(.+)$", re.M)
# `MIT + file LICENSE` -> `MIT`; `GPL (>= 2)` -> `GPL`. The suffix points at a
# stub file and the qualifier is a version floor; neither changes which licence
# it is.
_R_FILE_SUFFIX = re.compile(r"\s*\+\s*file\s+\S+\s*$", re.IGNORECASE)
_R_VERSION_QUALIFIER = re.compile(r"\s*\(([^)]*)\)\s*$")
# `GPL (>= 2)` is "version 2 or later", which SPDX spells `GPL-2.0-or-later`.
# Dropping the floor and mapping the bare family would record the wrong version.
_R_VERSION_FLOOR = re.compile(r">=\s*(\d+(?:\.\d+)?)")
_R_VERSIONED_FAMILIES = {"gpl": "GPL", "lgpl": "LGPL", "agpl": "AGPL"}


def spdx_from_r_description(text: str, _map=None) -> str | None:
    """SPDX id from an R package's DESCRIPTION `License:` field, or None.

    R keeps the licence in DESCRIPTION, not LICENSE: `usethis::use_mit_license()`
    writes a LICENSE containing only YEAR and COPYRIGHT HOLDER, which no text
    classifier can read. A field naming only a file (`License: file LICENSE`)
    declares nothing and returns None rather than a guess.
    """
    match = _R_LICENSE_FIELD.search(text or "")
    return spdx_from_r_license_field(match.group(1), _map) if match else None


def spdx_from_r_license_field(value: str, _map=None) -> str | None:
    """SPDX id from the *value* of an R `License:` field, or None.

    Split out because registries serve the field on its own -- r-universe returns
    `GPL (>= 2) + file LICENSE` with no surrounding DESCRIPTION to search.
    """
    if not value:
        return None
    field = _R_FILE_SUFFIX.sub("", value.strip())
    qualifier = _R_VERSION_QUALIFIER.search(field)
    declared = _R_VERSION_QUALIFIER.sub("", field).strip()
    if not declared or declared.lower().startswith("file "):
        return None
    family = _R_VERSIONED_FAMILIES.get(declared.lower())
    floor = _R_VERSION_FLOOR.search(qualifier.group(1)) if qualifier else None
    if family and floor:
        version = floor.group(1)
        return f"{family}-{version if '.' in version else version + '.0'}-or-later"
    aliases = (_map or load_map()).get("r_license_aliases") or {}
    for name, spdx in aliases.items():
        if name.lower() == declared.lower():
            return spdx
    return None


def detect_license(owner, repo, token, _fetch_api=_gh_fetch, _contents=_gh_contents, _fetch_file=_gh_file):
    """(license_id, source) where source ∈ {github-api, license-file, r-description, file-present-unclassified, none}."""
    spdx = _fetch_api(owner, repo, token)
    if spdx:
        return (spdx, "github-api")
    names = _contents(owner, repo, token)
    lic_files = [n for n in names if _LICENSE_FILE_RE.match(n)]
    if lic_files:
        cls = classify_license_text(_fetch_file(owner, repo, lic_files[0], token))
        if cls:
            return (cls, "license-file")
    # Last resort, and only for what the text could not settle: an R package's
    # real declaration lives in DESCRIPTION.
    if _R_DESCRIPTION in names:
        cls = spdx_from_r_description(_fetch_file(owner, repo, _R_DESCRIPTION, token))
        if cls:
            return (cls, "r-description")
    return (None, "file-present-unclassified") if lic_files else (None, "none")


def tier_for_repo(repo_url, token=None, cache=None, _detect=detect_license):
    """(tier, license_id, source) for a repo URL. No repo or no license -> ('restricted', None, 'none')."""
    pr = parse_repo(repo_url)
    if not pr:
        return ("restricted", None, "none")
    key = f"{pr[0]}/{pr[1]}"
    if cache is not None and key in cache:
        lic, src = cache[key]["id"], cache[key]["source"]
    else:
        lic, src = _detect(pr[0], pr[1], token)
        if cache is not None:
            cache[key] = {"id": lic, "source": src}
    return (tier_for_license(lic or ""), lic, src)


def apply_to_corpus(corpus_path, token, cache=None, _detect=detect_license) -> dict:
    """Write license_tier + access.license + license_detection into every corpus entry. Returns {tier:count}."""
    path = pathlib.Path(corpus_path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    summary: dict[str, int] = {}
    for p in doc.get("papers", []):
        # An entry with no repository is not this script's question, and writing
        # `restricted` / `none` over it destroys whatever the *paper* licence
        # resolver established from the registry (`resolve_paper_license.py`).
        # Both write the same fields; only one of them has evidence per entry.
        if p.get("license_locked") or not str(p.get("repo_url") or "").strip():
            t = p.get("license_tier", "restricted")
            summary[t] = summary.get(t, 0) + 1
            continue
        tier, lic, src = tier_for_repo(p.get("repo_url"), token=token, cache=cache, _detect=_detect)
        # A lookup that found nothing must not erase one that did. The licence
        # *value* is what matters, not the detection label beside it: in
        # metabolomics/v1 the recorded licences carry `license_detection: null`
        # because they came from Unpaywall rather than from a repository, and a
        # guard keyed only on the label wiped nineteen of them.
        recorded = (p.get("access") or {}).get("license")
        # This script reads a repository, so it may only speak about the tool.
        # Writing over a licence that describes the *paper* substitutes one axis
        # for the other, and nothing downstream can tell that it happened.
        if licence_subject(p) == SUBJECT_PAPER:
            kept = p.get("license_tier") or "restricted"
            summary[kept] = summary.get(kept, 0) + 1
            continue
        if lic is None and (recorded
                            or p.get("license_detection") not in UNESTABLISHED_DETECTIONS):
            kept = p.get("license_tier", "restricted")
            summary[kept] = summary.get(kept, 0) + 1
            continue
        p["license_tier"] = tier
        p.setdefault("access", {})["license"] = lic
        p["license_detection"] = src
        p["license_subject"] = SUBJECT_TOOL
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
    ap.add_argument("--cache", default=".license-cache-v2.json")
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
