"""Resolve a pre-print's posting licence from DOI registries.

Pre-print servers let the author choose the posting licence, so a pre-print is NOT
automatically CC-BY: bioRxiv/medRxiv offer CC-BY, CC-BY-NC, CC-BY-ND, CC-BY-NC-ND,
CC0 and "no reuse allowed", and arXiv's default grants no reuse rights at all.
Assuming CC-BY would admit source text this project has no right to redistribute.
See governance/OPEN_ACCESS_POLICY.md, section "Pre-prints".

Pre-print-ness is read from the registry's own declaration -- Crossref's
`type: posted-content` and DataCite's `resourceTypeGeneral: Preprint` -- never from
a DOI prefix. A prefix identifies a registrant, not a work type (10.1101 is Cold
Spring Harbor, covering bioRxiv, medRxiv *and* CSHL journals), and prefix lists go
stale the moment a server re-registers. Any server registered with either registry
therefore resolves with no change to this module.

An unrecognised or absent licence resolves to an explicit loud status, never to a
permissive or restrictive default. Callers must treat every status other than
`resolved` as blocking.
"""
from __future__ import annotations

import argparse
import glob as globlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

import yaml

from scripts.license_tier import load_map, source_reuse_for_license, tier_for_license

CROSSREF_WORK_URL = "https://api.crossref.org/works/{doi}"
DATACITE_DOI_URL = "https://api.datacite.org/dois/{doi}"
SERVERS_MAP = pathlib.Path(__file__).resolve().parent.parent / "governance" / "preprint_servers.yaml"
USER_AGENT = "asb-skill-collections/1.0 (https://github.com/HolobiomicsLab/asb-skill-collections)"
REQUEST_TIMEOUT_S = 20
ABSENT_STATUS = (403, 404, 410)
RETRYABLE_STATUS = (429, 500, 502, 503, 504)
MAX_ATTEMPTS = 4
BACKOFF_BASE_S = 2.0

STATUS_RESOLVED = "resolved"
STATUS_UNKNOWN_LICENCE = "unknown_licence"
STATUS_NO_LICENCE_DECLARED = "no_licence_declared"
STATUS_NOT_A_PREPRINT = "not_a_preprint"
STATUS_UNRESOLVED = "unresolved"

_CC_LICENSE_RE = re.compile(r"creativecommons\.org/licenses/(?P<code>[a-z][a-z-]*)/(?P<version>\d+(?:\.\d+)?)", re.I)
_CC_ZERO_RE = re.compile(r"creativecommons\.org/publicdomain/zero/(?P<version>\d+(?:\.\d+)?)", re.I)
_ARXIV_DEFAULT_RE = re.compile(r"arxiv\.org/licenses/nonexclusive-distrib/(?P<version>\d+(?:\.\d+)?)", re.I)

# A trailing server-side version marker, e.g. `...433248v2` or `...530140v1.abstract`.
# Requires a digit before the `v` so a real DOI segment like `.v2` (figshare) is kept.
_VERSION_SUFFIX_RE = re.compile(r"(?<=\d)v\d+(?:\.[A-Za-z][\w-]*)?$")


@dataclass(frozen=True)
class PreprintLicense:
    """The outcome of resolving one DOI. `status` is authoritative."""

    doi: str
    status: str
    doi_used: str | None = None
    registry: str | None = None
    license_url: str | None = None
    spdx: str | None = None
    source_reuse: str | None = None
    license_tier: str | None = None

    @property
    def admissible_as_open_access(self) -> bool:
        """Only a resolved, full-reuse licence may carry an open `access.type`."""
        return self.status == STATUS_RESOLVED and self.source_reuse == "full"


def spdx_from_license_url(url: str) -> str | None:
    """Map a licence URL to an SPDX id; None when the URL is not recognised."""
    if not url:
        return None
    zero = _CC_ZERO_RE.search(url)
    if zero:
        return f"CC0-{zero['version']}"
    arxiv = _ARXIV_DEFAULT_RE.search(url)
    if arxiv:
        return f"arXiv-{arxiv['version']}"
    creative = _CC_LICENSE_RE.search(url)
    if creative:
        return f"CC-{creative['code'].upper()}-{creative['version']}"
    return None


def strip_version_suffix(doi: str) -> str:
    """Drop a trailing `vN` / `vN.fragment` marker scraped from a landing-page URL."""
    return _VERSION_SUFFIX_RE.sub("", (doi or "").strip())


def retry_delay(attempt: int, retry_after: str | None) -> float:
    """Seconds to wait before the next attempt, honouring a server's Retry-After."""
    if retry_after and retry_after.strip().isdigit():
        return float(retry_after.strip())
    return BACKOFF_BASE_S * (2 ** (attempt - 1))


def _get_json(url: str) -> dict | None:
    """One attempt. None when the record is absent; raises on anything else."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_S) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in ABSENT_STATUS:
            return None
        raise


def fetch_json(url: str) -> dict | None:
    """GET a JSON document, retrying transient failures.

    A rate-limited or briefly unavailable registry must not be mistaken for a DOI
    that does not exist: the first would silently mark a resolvable pre-print
    `unresolved`, and a bulk audit would report absence where there was only 429.
    Only ABSENT_STATUS means "no record".
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return _get_json(url)
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_STATUS or attempt == MAX_ATTEMPTS:
                raise
            time.sleep(retry_delay(attempt, exc.headers.get("Retry-After")))
        except (urllib.error.URLError, TimeoutError):
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(retry_delay(attempt, None))
    return None


def _first_recognised_spdx(urls: list[str]) -> tuple[str | None, str | None]:
    """Return the first (url, spdx) pair whose URL maps to a known SPDX id."""
    for url in urls:
        spdx = spdx_from_license_url(url)
        if spdx:
            return url, spdx
    return (urls[0] if urls else None), None


def _classify(doi: str, doi_used: str, registry: str, urls: list[str]) -> PreprintLicense:
    """Turn a registry's declared licence URLs into a typed outcome."""
    if not urls:
        return PreprintLicense(doi, STATUS_NO_LICENCE_DECLARED, doi_used, registry)
    url, spdx = _first_recognised_spdx(urls)
    if not spdx:
        return PreprintLicense(doi, STATUS_UNKNOWN_LICENCE, doi_used, registry, url)
    reuse = source_reuse_for_license(spdx)
    if reuse is None:
        return PreprintLicense(doi, STATUS_UNKNOWN_LICENCE, doi_used, registry, url, spdx)
    return PreprintLicense(doi, STATUS_RESOLVED, doi_used, registry, url, spdx, reuse, tier_for_license(spdx))


def load_servers(path: pathlib.Path | None = None) -> dict:
    """Load the server-API + licence-token map (governance/preprint_servers.yaml)."""
    return yaml.safe_load((path or SERVERS_MAP).read_text(encoding="utf-8")) or {}


def _declared_servers(message: dict, servers: dict) -> list[str]:
    """Server slugs the registry itself names for this work, restricted to known ones."""
    names = [str(i.get("name", "")).strip().lower() for i in (message.get("institution") or [])]
    return [name for name in names if name in servers]


def _probe_server_api(server: str, doi: str, original: str, fetch) -> PreprintLicense | None:
    """Ask a pre-print server for its own licence token when the registry has none."""
    config = load_servers()
    payload = fetch(config["servers"][server]["detail_url"].format(doi=doi))
    records = (payload or {}).get("collection") or []
    if not records:
        return None
    token = str(records[-1].get("license") or "").strip().lower()
    spdx = (config.get("license_tokens") or {}).get(token)
    if not spdx:
        return PreprintLicense(original, STATUS_UNKNOWN_LICENCE, doi, f"{server}_api", token or None)
    reuse = source_reuse_for_license(spdx)
    if reuse is None:
        return PreprintLicense(original, STATUS_UNKNOWN_LICENCE, doi, f"{server}_api", token, spdx)
    return PreprintLicense(original, STATUS_RESOLVED, doi, f"{server}_api", token, spdx, reuse, tier_for_license(spdx))


def _probe_crossref(doi: str, original: str, fetch) -> PreprintLicense | None:
    """Crossref declares a pre-print as type `posted-content`.

    Crossref's `license` array is sometimes absent, or points at a server FAQ page
    rather than a licence deed. When it yields nothing usable, fall back to the
    server the registry itself names in `institution[]` -- never to a DOI prefix.
    """
    payload = fetch(CROSSREF_WORK_URL.format(doi=urllib.parse.quote(doi, safe="/")))
    if not payload:
        return None
    message = payload.get("message") or {}
    if message.get("type") != "posted-content":
        return PreprintLicense(original, STATUS_NOT_A_PREPRINT, doi, "crossref")
    urls = [entry.get("URL") for entry in (message.get("license") or []) if entry.get("URL")]
    outcome = _classify(original, doi, "crossref", urls)
    if outcome.status == STATUS_RESOLVED:
        return outcome
    for server in _declared_servers(message, load_servers().get("servers") or {}):
        recovered = _probe_server_api(server, doi, original, fetch)
        if recovered is not None:
            return recovered
    return outcome


def _probe_datacite(doi: str, original: str, fetch) -> PreprintLicense | None:
    """DataCite declares a pre-print as resourceTypeGeneral `Preprint` (arXiv lives here)."""
    payload = fetch(DATACITE_DOI_URL.format(doi=urllib.parse.quote(doi, safe="/")))
    if not payload:
        return None
    attributes = (payload.get("data") or {}).get("attributes") or {}
    if (attributes.get("types") or {}).get("resourceTypeGeneral") != "Preprint":
        return PreprintLicense(original, STATUS_NOT_A_PREPRINT, doi, "datacite")
    urls = [r.get("rightsUri") for r in (attributes.get("rightsList") or []) if r.get("rightsUri")]
    return _classify(original, doi, "datacite", urls)


def _doi_candidates(doi: str) -> list[str]:
    """The DOI as recorded, then a version-stripped retry if that differs."""
    exact = (doi or "").strip()
    stripped = strip_version_suffix(exact)
    return [exact] if stripped == exact else [exact, stripped]


def resolve_preprint_license(doi: str, fetch=fetch_json) -> PreprintLicense:
    """Resolve one DOI's posting licence. Never guesses; see module docstring."""
    if not (doi or "").strip():
        return PreprintLicense(doi, STATUS_UNRESOLVED)
    try:
        for candidate in _doi_candidates(doi):
            for probe in (_probe_crossref, _probe_datacite):
                outcome = probe(candidate, doi, fetch)
                if outcome is not None:
                    return outcome
    except (urllib.error.URLError, OSError, ValueError):
        return PreprintLicense(doi, STATUS_UNRESOLVED)
    return PreprintLicense(doi, STATUS_UNRESOLVED)


def _corpus_entries(patterns: list[str]):
    """Yield (path, paper) for every entry in every matching corpus file."""
    for pattern in patterns:
        for path in sorted(globlib.glob(pattern)):
            document = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8")) or {}
            for paper in document.get("papers") or []:
                yield path, paper


def _load_cache(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def audit(patterns: list[str], cache_path: pathlib.Path, fetch=fetch_json) -> list[dict]:
    """Resolve every corpus DOI and report the pre-prints among them."""
    cache = _load_cache(cache_path)
    findings = []
    for path, paper in _corpus_entries(patterns):
        doi = str(paper.get("doi") or "").strip()
        if not doi:
            continue
        if doi not in cache:
            cache[doi] = resolve_preprint_license(doi, fetch).__dict__
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
        record = cache[doi]
        if record["status"] == STATUS_NOT_A_PREPRINT:
            continue
        access = paper.get("access") or {}
        findings.append({
            "corpus": path, "doi": doi, "entry_status": paper.get("status"),
            "access_type": access.get("type"), "recorded_license": access.get("license"),
            "preprint_status": record["status"], "preprint_spdx": record["spdx"],
            "source_reuse": record["source_reuse"],
        })
    return findings


def _print_audit(findings: list[dict]) -> int:
    """Print the audit table; return the count of entries needing a decision."""
    unresolved = [f for f in findings if f["preprint_status"] == STATUS_UNRESOLVED]
    preprints = [f for f in findings if f["preprint_status"] != STATUS_UNRESOLVED]
    not_full = [f for f in preprints if f["source_reuse"] != "full"]
    for finding in preprints:
        print(f"  {finding['doi']:44} {str(finding['preprint_spdx']):18} reuse={str(finding['source_reuse']):8} "
              f"access.type={finding['access_type']} status={finding['entry_status']}")
    print(f"\npre-prints: {len(preprints)}   not-full-reuse: {len(not_full)}   unresolved: {len(unresolved)}")
    for finding in unresolved:
        print(f"  UNRESOLVED (blocking): {finding['doi']} in {finding['corpus']}")
    return len(not_full) + len(unresolved)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--doi", help="resolve a single DOI and print the outcome")
    parser.add_argument("--corpus", nargs="*", default=["collections/*/v*/corpus.yaml"],
                        help="glob(s) of corpus.yaml files to audit")
    parser.add_argument("--cache", default=".cache/preprint_licenses.json")
    parser.add_argument("--strict", action="store_true", help="exit 1 if any pre-print is not full-reuse or unresolved")
    parser.add_argument("--smoke", action="store_true", help="run the module's self-check and exit")
    args = parser.parse_args(argv)

    if args.smoke:
        return _smoke()
    if args.doi:
        print(json.dumps(resolve_preprint_license(args.doi).__dict__, indent=2))
        return 0
    needing_decision = _print_audit(audit(args.corpus, pathlib.Path(args.cache)))
    return 1 if (args.strict and needing_decision) else 0


def _smoke() -> int:
    assert spdx_from_license_url("https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode") == "CC-BY-NC-ND-4.0"
    assert spdx_from_license_url("http://creativecommons.org/publicdomain/zero/1.0/") == "CC0-1.0"
    assert spdx_from_license_url("http://arxiv.org/licenses/nonexclusive-distrib/1.0/") == "arXiv-1.0"
    assert spdx_from_license_url("https://example.org/my-licence") is None
    assert strip_version_suffix("registrant/2021.02.28.433248v2").endswith("433248")
    assert strip_version_suffix("registrant/figshare.28876751.v2").endswith(".v2")
    assert source_reuse_for_license("CC-BY-4.0", load_map()) == "full"
    assert source_reuse_for_license("CC-BY-NC-ND-4.0", load_map()) == "limited"
    assert source_reuse_for_license("Some-Unknown-1.0", load_map()) is None
    print("PASS: preprint_license smoke check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
