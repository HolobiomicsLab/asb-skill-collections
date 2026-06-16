#!/usr/bin/env python
"""Validate community-deposited supplementary-information manifests.

Offline by default (schema + license gate + file-presence/sha256). Pass
``--check-links`` to additionally probe each ``url:`` entry (network).

Enforces ``supplements/SPEC.md`` (schema ``asb-supplements/1.0``) and the
license gate from ``CONTENT_POLICY.md`` §3/§4:

  * a DEPOSITED ``file:`` is redistributed in this public repo, so its license
    MUST be OA/permissive (cc-by, cc-by-sa, cc0, public-domain);
  * a ``url:`` download link is only a pointer (not redistribution), so any
    license is allowed — but a non-OA ``url`` ingests Tier-2 (private KB) only.

Usage:
    python scripts/validate_supplements.py                      # all manifests
    python scripts/validate_supplements.py supplements/<doi>    # one dir
    python scripts/validate_supplements.py --check-links        # + probe urls

Exit code is non-zero if any manifest has an ERROR.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

SCHEMA_ID = "asb-supplements/1.0"
SUP_ROOT = Path(__file__).resolve().parent.parent / "supplements"

_KINDS = {
    "si-pdf", "si-table", "protocol", "extended-data",
    "dataset-readme", "repo-wiki", "other",
}
# Licenses that permit redistributing the file in this public repo (CONTENT_POLICY §3/§4).
_OA_FILE_LICENSES = {"cc-by", "cc-by-sa", "cc0", "public-domain", "cc-by-4.0", "cc-by-sa-4.0"}
# Any string here is accepted as a *recorded* license for url entries.
_KNOWN_LICENSES = _OA_FILE_LICENSES | {
    "cc-by-nc", "cc-by-nc-sa", "cc-by-nc-nd", "cc-by-nd",
    "publisher-si", "all-rights-reserved", "unknown",
}
_ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)


def _norm_lic(v: str) -> str:
    return re.sub(r"\s+", "", str(v or "").strip().lower())


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 16), b""):
            h.update(blk)
    return h.hexdigest()


def _probe_url(url: str, timeout: float = 20.0) -> tuple[bool, str]:
    """Best-effort reachability check; returns (ok, detail)."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method,
                                         headers={"User-Agent": "asb-supplements-validator"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                code = getattr(r, "status", r.getcode())
                if 200 <= code < 400:
                    return True, f"{method} {code}"
        except urllib.error.HTTPError as e:
            if e.code in (403, 405) and method == "HEAD":
                continue  # some hosts block HEAD; try GET
            return False, f"{method} HTTP {e.code}"
        except Exception as e:  # noqa: BLE001
            if method == "HEAD":
                continue
            return False, f"{type(e).__name__}: {e}"
    return False, "unreachable"


def validate_manifest(mpath: Path, check_links: bool) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings) for one manifest.yaml."""
    errs: list[str] = []
    warns: list[str] = []
    try:
        doc = yaml.safe_load(mpath.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"YAML parse error: {e}"], []
    if not isinstance(doc, dict):
        return ["manifest is not a mapping"], []

    if doc.get("schema") != SCHEMA_ID:
        errs.append(f"schema must be '{SCHEMA_ID}' (got {doc.get('schema')!r})")
    doi = str(doc.get("doi", "")).strip()
    if not doi:
        errs.append("missing required field: doi")
    elif not _DOI_RE.match(doi):
        warns.append(f"doi {doi!r} does not look like a DOI (10.xxxx/...)")

    entries = doc.get("entries")
    if not isinstance(entries, list) or not entries:
        errs.append("entries must be a non-empty list")
        return errs, warns

    seen_keys: set[str] = set()
    for i, e in enumerate(entries):
        tag = f"entry[{i}]"
        if not isinstance(e, dict):
            errs.append(f"{tag}: not a mapping")
            continue
        lbl = e.get("label")
        if lbl:
            tag = f"entry[{i}] '{lbl}'"
        # kind
        if e.get("kind") not in _KINDS:
            errs.append(f"{tag}: kind must be one of {sorted(_KINDS)} (got {e.get('kind')!r})")
        # exactly one of file/url
        has_file, has_url = bool(e.get("file")), bool(e.get("url"))
        if has_file == has_url:
            errs.append(f"{tag}: exactly ONE of 'file' or 'url' is required")
        # label
        if not lbl:
            errs.append(f"{tag}: missing required field: label")
        # license
        lic = _norm_lic(e.get("license"))
        if not lic:
            errs.append(f"{tag}: missing required field: license")
        elif lic not in _KNOWN_LICENSES:
            warns.append(f"{tag}: unrecognized license {e.get('license')!r} (treated as non-OA)")
        # depositor_orcid
        orcid = str(e.get("depositor_orcid", "")).strip()
        if not orcid:
            errs.append(f"{tag}: missing required field: depositor_orcid")
        elif not _ORCID_RE.match(orcid):
            errs.append(f"{tag}: depositor_orcid {orcid!r} is not a valid ORCID (0000-0000-0000-0000)")
        if not e.get("provenance"):
            warns.append(f"{tag}: no 'provenance' note (recommended)")

        # ---- license gate ----
        if has_file:
            if lic and lic not in _OA_FILE_LICENSES:
                errs.append(
                    f"{tag}: deposited file has non-OA license {e.get('license')!r}; "
                    f"only {sorted(_OA_FILE_LICENSES)} may be redistributed here — "
                    f"use a 'url:' download link instead")
            fpath = (mpath.parent / str(e["file"])).resolve()
            # contain within the doi dir (no path traversal)
            try:
                fpath.relative_to(mpath.parent.resolve())
            except ValueError:
                errs.append(f"{tag}: file {e['file']!r} escapes the supplement directory")
                fpath = None
            if fpath is not None:
                if not fpath.exists():
                    errs.append(f"{tag}: file not found: {e['file']}")
                else:
                    key = _sha256(fpath)
                    if e.get("sha256") and _norm_lic(e["sha256"]) != key:
                        errs.append(f"{tag}: sha256 mismatch (manifest {e['sha256']!r} != actual {key})")
                    if key in seen_keys:
                        warns.append(f"{tag}: duplicate file content (sha256 already seen)")
                    seen_keys.add(key)
        elif has_url:
            url = str(e["url"]).strip()
            if not url.lower().startswith(("http://", "https://")):
                errs.append(f"{tag}: url must be http(s): {url!r}")
            elif url in seen_keys:
                warns.append(f"{tag}: duplicate url")
            else:
                seen_keys.add(url)
            if lic and lic not in _OA_FILE_LICENSES:
                warns.append(f"{tag}: non-OA url license {e.get('license')!r} → ingests Tier-2 (private KB) only")
            if check_links and url.lower().startswith(("http://", "https://")):
                ok, detail = _probe_url(url)
                (warns if ok else errs).append(f"{tag}: link {'ok' if ok else 'DEAD'} ({detail})")
    return errs, warns


def discover(targets: list[str]) -> list[Path]:
    if targets:
        out = []
        for t in targets:
            p = Path(t)
            if p.is_file() and p.name == "manifest.yaml":
                out.append(p)
            elif p.is_dir() and (p / "manifest.yaml").is_file():
                out.append(p / "manifest.yaml")
            else:
                print(f"!! no manifest.yaml at {t}", file=sys.stderr)
        return out
    if not SUP_ROOT.is_dir():
        return []
    return sorted(SUP_ROOT.glob("*/manifest.yaml"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("targets", nargs="*", help="supplement dir(s) or manifest.yaml; default = all")
    ap.add_argument("--check-links", action="store_true", help="probe each url: entry (network)")
    args = ap.parse_args()

    manifests = discover(args.targets)
    if not manifests:
        print("No manifests found (supplements/<doi>/manifest.yaml). Nothing to validate.")
        return 0

    total_err = 0
    for m in manifests:
        errs, warns = validate_manifest(m, args.check_links)
        rel = m.parent.name
        status = "FAIL" if errs else ("WARN" if warns else "OK")
        print(f"[{status}] {rel}/manifest.yaml")
        for w in warns:
            print(f"    warn: {w}")
        for er in errs:
            print(f"    ERROR: {er}")
        total_err += len(errs)

    print(f"\n{len(manifests)} manifest(s); {total_err} error(s).")
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
