#!/usr/bin/env python
"""Ingest community-deposited supplementary information into a paper KB.

Reads ``supplements/<doi-slug>/manifest.yaml`` (schema ``asb-supplements/1.0``,
see ``supplements/SPEC.md``), resolves each entry (a local OA ``file:`` or a
``url:`` download link), extracts text, and ingests it into the paper's
Perspicacité KB as labeled documents so it grounds the generated skills/cards.

Resolution rules (mirrors the server's local-doc ingest in Perspicacité):
  * ``.pdf``                       -> uploaded raw; the server's pdf_parser extracts text
  * ``.xlsx`` / ``.xls``           -> flattened to text client-side (openpyxl)
  * ``.csv`` / ``.tsv`` / ``.txt`` / ``.md`` / ``.json`` / ``.rst`` / ``.html``
                                   -> wrapped with a labeled header, uploaded as text
  * other binary                   -> skipped with a warning

Idempotent: each ingested entry is recorded in ``<doi>/.ingested.json`` keyed by
sha256 (files) or url, and skipped on re-run unless ``--force``.

Requires the Perspicacité server on :8002 (override with ``--base``). Run
``validate_supplements.py`` first — this script re-checks the license gate but
assumes a valid manifest.

Usage:
    python scripts/ingest_supplements.py supplements/<doi-slug>            # default KB asb-paper-<doi-slug>
    python scripts/ingest_supplements.py <doi-slug> --kb asb-paper-foo
    python scripts/ingest_supplements.py <doi-slug> --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import yaml

SUP_ROOT = Path(__file__).resolve().parent.parent / "supplements"
DEFAULT_BASE = "http://127.0.0.1:8002"
_OA_FILE_LICENSES = {"cc-by", "cc-by-sa", "cc0", "public-domain", "cc-by-4.0", "cc-by-sa-4.0"}
_TEXT_SUFFIXES = {".csv", ".tsv", ".txt", ".md", ".json", ".rst", ".html", ".htm", ".xml"}


def doi_slug(doi: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", doi.lower()).strip("-")


def _norm(v: str) -> str:
    return re.sub(r"\s+", "", str(v or "").strip().lower())


def _slug(s: str, n: int = 48) -> str:
    return (re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-") or "item")[:n]


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------- io
def http_get_bytes(url: str, timeout: float = 120.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "asb-supplements-ingest"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def post_multipart(base: str, kb: str, filename: str, data: bytes,
                   content_type: str, timeout: float = 300.0) -> dict:
    """POST one file to /api/kb/<kb>/local-files as multipart/form-data."""
    boundary = f"----asbsup{uuid.uuid4().hex}"
    pre = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode()
    post = f"\r\n--{boundary}--\r\n".encode()
    body = pre + data + post
    req = urllib.request.Request(
        f"{base}/api/kb/{kb}/local-files", data=body, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def poll_job(base: str, job_id: str, timeout: float = 300.0) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(2)
        try:
            req = urllib.request.Request(f"{base}/api/jobs/{job_id}", method="GET")
            with urllib.request.urlopen(req, timeout=30) as r:
                st = json.load(r)
        except Exception:  # noqa: BLE001
            continue
        state = st.get("status") or st.get("state")
        if state in ("completed", "done", "finished", "success"):
            return st
        if state in ("failed", "error"):
            return st
    return {"status": "timeout"}


def ensure_kb(base: str, kb: str, desc: str) -> None:
    body = json.dumps({"name": kb, "description": desc}).encode()
    req = urllib.request.Request(f"{base}/api/kb", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=60).read()
    except urllib.error.HTTPError as e:
        if e.code not in (400, 409):
            raise


# ---------------------------------------------------------------- extraction
def xlsx_to_text(raw: bytes) -> str:
    import io

    import openpyxl  # noqa: PLC0415
    wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
    out: list[str] = []
    for ws in wb.worksheets:
        out.append(f"## sheet: {ws.title}")
        for row in ws.iter_rows(values_only=True):
            cells = ["" if c is None else str(c) for c in row]
            if any(cells):
                out.append("\t".join(cells))
    return "\n".join(out)


def build_payload(entry: dict, raw: bytes, src_suffix: str, doi: str) -> tuple[str, bytes, str] | None:
    """Return (filename, bytes, content_type) to upload, or None to skip."""
    label = entry.get("label", "supplement")
    kind = entry.get("kind", "other")
    lic = entry.get("license", "unknown")
    prov = entry.get("provenance", "")
    base_name = f"sup__{_slug(label)}"
    header = (
        f"# Supplementary information: {label}\n\n"
        f"- source_doi: {doi}\n- kind: {kind}\n- license: {lic}\n"
        f"- provenance: {prov}\n- asb_supplement: true\n\n---\n\n"
    )
    suf = src_suffix.lower()
    if suf == ".pdf":
        # upload raw; server extracts text. Header can't be prepended to a PDF.
        return f"{base_name}.pdf", raw, "application/pdf"
    if suf in (".xlsx", ".xls"):
        try:
            text = xlsx_to_text(raw)
        except Exception as e:  # noqa: BLE001
            print(f"    !! xlsx extract failed ({e}); skipping", file=sys.stderr)
            return None
        return f"{base_name}.md", (header + text).encode("utf-8"), "text/markdown"
    if suf in _TEXT_SUFFIXES:
        text = raw.decode("utf-8", errors="replace")
        return f"{base_name}.md", (header + text).encode("utf-8"), "text/markdown"
    print(f"    !! unsupported suffix {suf!r} for '{label}'; deposit text/csv/pdf instead", file=sys.stderr)
    return None


# --------------------------------------------------------------------- driver
def resolve_dir(target: str) -> Path:
    p = Path(target)
    if p.is_dir():
        return p
    cand = SUP_ROOT / target
    if cand.is_dir():
        return cand
    raise SystemExit(f"no supplement dir: {target} (looked at {p} and {cand})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", help="supplements/<doi-slug> dir or just <doi-slug>")
    ap.add_argument("--kb", default=None, help="paper KB slug (default asb-paper-<doi-slug>)")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--force", action="store_true", help="re-ingest already-recorded entries")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sdir = resolve_dir(args.target)
    mpath = sdir / "manifest.yaml"
    if not mpath.is_file():
        raise SystemExit(f"no manifest.yaml in {sdir}")
    doc = yaml.safe_load(mpath.read_text(encoding="utf-8"))
    doi = str(doc.get("doi", "")).strip()
    slug = doi_slug(doi) if doi else sdir.name
    kb = args.kb or f"asb-paper-{slug}"

    ledger_path = sdir / ".ingested.json"
    ledger = {}
    if ledger_path.is_file():
        try:
            ledger = json.loads(ledger_path.read_text())
        except Exception:  # noqa: BLE001
            ledger = {}

    if not args.dry_run:
        ensure_kb(args.base, kb, f"Paper KB for {doi} (with deposited supplements)")

    entries = doc.get("entries") or []
    print(f"== {sdir.name}: {len(entries)} entry(ies) -> KB {kb} ==")
    n_ok = n_skip = n_fail = 0
    for i, e in enumerate(entries):
        label = e.get("label", f"entry[{i}]")
        lic = _norm(e.get("license"))
        if e.get("file"):
            fpath = (sdir / str(e["file"])).resolve()
            try:
                fpath.relative_to(sdir.resolve())
            except ValueError:
                print(f"  [{i}] {label}: SKIP (path escapes dir)")
                n_fail += 1
                continue
            if not fpath.exists():
                print(f"  [{i}] {label}: SKIP (file missing: {e['file']})")
                n_fail += 1
                continue
            if lic and lic not in _OA_FILE_LICENSES:
                print(f"  [{i}] {label}: SKIP (deposited file non-OA license {e.get('license')!r}; use url:)")
                n_fail += 1
                continue
            raw = fpath.read_bytes()
            suffix = fpath.suffix
            key = _sha256_bytes(raw)
        elif e.get("url"):
            url = str(e["url"]).strip()
            key = url
            if key in ledger and not args.force:
                print(f"  [{i}] {label}: already ingested (url) — skip")
                n_skip += 1
                continue
            if args.dry_run:
                print(f"  [{i}] {label}: would FETCH {url}")
                continue
            try:
                raw = http_get_bytes(url)
            except Exception as ex:  # noqa: BLE001
                print(f"  [{i}] {label}: FETCH FAILED ({ex})")
                n_fail += 1
                continue
            # infer suffix from url path
            suffix = Path(urllib.request.urlparse(url).path).suffix or ".txt"
            if lic and lic not in _OA_FILE_LICENSES:
                print(f"  [{i}] {label}: non-OA url -> Tier-2 private KB only")
        else:
            print(f"  [{i}] {label}: SKIP (no file/url)")
            n_fail += 1
            continue

        if key in ledger and not args.force:
            print(f"  [{i}] {label}: already ingested — skip")
            n_skip += 1
            continue

        payload = build_payload(e, raw, suffix, doi)
        if payload is None:
            n_fail += 1
            continue
        fname, data, ctype = payload
        if args.dry_run:
            print(f"  [{i}] {label}: would UPLOAD {fname} ({len(data)} bytes, {ctype})")
            continue

        try:
            resp = post_multipart(args.base, kb, fname, data, ctype)
        except Exception as ex:  # noqa: BLE001
            print(f"  [{i}] {label}: UPLOAD FAILED ({ex})")
            n_fail += 1
            continue
        job = resp.get("job_id")
        st = poll_job(args.base, job, timeout=300.0) if job else resp
        chunks = (st.get("result") or {}).get("added_chunks") if isinstance(st, dict) else None
        state = st.get("status") or st.get("state") if isinstance(st, dict) else "?"
        print(f"  [{i}] {label}: {state} (chunks={chunks}) <- {fname}")
        if state in ("completed", "done", "finished", "success"):
            ledger[key] = {"label": label, "kb": kb, "file": fname,
                           "chunks": chunks, "sha256": key if e.get("file") else None}
            n_ok += 1
        else:
            n_fail += 1

    if not args.dry_run:
        ledger_path.write_text(json.dumps(ledger, indent=1))
    print(f"\n== done: {n_ok} ingested, {n_skip} skipped, {n_fail} failed ==")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
