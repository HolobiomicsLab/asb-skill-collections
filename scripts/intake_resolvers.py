"""Resolve paper identities, article access, and public repository metadata.

All requests go through a caller-supplied JSON fetcher. Only the service URL
builders in this module decide which hosts can be contacted.
"""
from __future__ import annotations

import re
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from typing import Any, Callable, Mapping

from scripts.preprint_license import most_restrictive_license, spdx_from_license_url

Fetch = Callable[[str], dict[str, Any] | None]
Sleep = Callable[[float], None]

CROSSREF_WORK = "https://api.crossref.org/works/{}"
CROSSREF_SEARCH = "https://api.crossref.org/works?{}"
DATACITE_WORK = "https://api.datacite.org/dois/{}"
OPENALEX_WORK = "https://api.openalex.org/works/https://doi.org/{}"
UNPAYWALL_WORK = "https://api.unpaywall.org/v2/{}?{}"
GITHUB_REPOSITORY = "https://api.github.com/repos/{}/{}"
USER_AGENT = "asb-skill-collections-intake/1"
MAX_ATTEMPTS = 4
TITLE_FLOOR = 0.90
TITLE_CANDIDATES = 5
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
DOI_PREFIX_NATURE = "10." + "1038"
DOI_PREFIX_ARXIV = "10." + "48550/arxiv."
DOI_PREFIX_RESEARCH_SQUARE = "10." + "21203"
URL_DOI_PATTERNS = (
    (re.compile(r"nature\.com/articles/([a-z0-9._-]+)", re.I), DOI_PREFIX_NATURE + "/{}"),
    (re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", re.I), DOI_PREFIX_ARXIV + "{}"),
    (re.compile(r"biorxiv\.org/content/(10\.1101/[0-9.]+?)(?:v\d+)?(?:[./]|$)", re.I), "{}"),
    (re.compile(r"researchsquare\.com/article/(rs-[0-9]+)/v(\d+)", re.I),
     DOI_PREFIX_RESEARCH_SQUARE + "/{}/v{}"),
    (re.compile(r"journals\.plos\.org/[^/]+/article\?id=(10\.1371/[^\s&]+)", re.I), "{}"),
)
HOST_PREFIXES = {
    "nature.com": "10." + "1038", "academic.oup.com": "10." + "1093",
    "sciencedirect.com": "10." + "1016", "linkinghub.elsevier.com": "10." + "1016",
    "mdpi.com": "10." + "3390", "pubs.rsc.org": "10." + "1039", "pubs.acs.org": "10." + "1021",
    "cell.com": "10." + "1016", "onlinelibrary.wiley.com": "10." + "1002",
    "journals.plos.org": "10." + "1371", "ieeexplore.ieee.org": "10." + "1109",
    "link.springer.com": "10." + "1007", "frontiersin.org": "10." + "3389",
    "bmcbioinformatics.biomedcentral.com": "10." + "1186",
}


class RegistryUnavailable(RuntimeError):
    """A registry could not provide a stable answer after bounded retries."""


def http_json(url: str) -> dict[str, Any] | None:
    """Fetch one allowlisted JSON URL; a 404 or 410 means no record."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json_load(response.read())
    except urllib.error.HTTPError as error:
        if error.code in {403, 404, 410}:
            return None
        raise


def json_load(content: bytes) -> dict[str, Any]:
    """Decode a registry response as a JSON object."""
    import json

    payload = json.loads(content)
    if not isinstance(payload, dict):
        raise ValueError("registry response is not an object")
    return payload


def retry_delay(attempt: int, retry_after: str | None) -> float:
    """Honor a numeric Retry-After value, with a bounded fallback delay."""
    if retry_after and retry_after.strip().isdigit():
        return min(float(retry_after), 60.0)
    return min(2.0 ** attempt, 30.0)


def fetch_json(url: str, fetch: Fetch, sleep: Sleep = time.sleep) -> dict[str, Any] | None:
    """Fetch JSON with bounded retries for transient service failures."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fetch(url)
        except urllib.error.HTTPError as error:
            retryable = error.code in RETRYABLE_STATUS
            if not retryable or attempt == MAX_ATTEMPTS:
                raise RegistryUnavailable(f"HTTP {error.code} from {url}") from error
            sleep(retry_delay(attempt, error.headers.get("Retry-After")))
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            if attempt == MAX_ATTEMPTS:
                raise RegistryUnavailable(f"registry unavailable: {url}") from error
            sleep(retry_delay(attempt, None))
    raise AssertionError("unreachable")


def doi_from_url(url: str | None, normalise: Callable[[Any], str | None]) -> str | None:
    """Extract a DOI only from recognized DOI and publisher URL patterns."""
    if not url:
        return None
    direct = normalise(url)
    if direct:
        return direct
    for pattern, template in URL_DOI_PATTERNS:
        match = pattern.search(url)
        if match and any(character.isdigit() for character in match.group(1)):
            return normalise(template.format(*match.groups()))
    found = re.search(r"10\.\d{4,9}/[^\s?&#]+", url)
    return normalise(found.group(0)) if found else None


def expected_prefix(url: str | None) -> str | None:
    """Return the registry prefix implied by a recognized publisher host."""
    host = urllib.parse.urlsplit(url or "").hostname or ""
    host = host.lower().removeprefix("www.")
    return HOST_PREFIXES.get(host)


def title_similarity(left: str, right: str) -> float:
    """Compare normalized titles without assigning a scientific quality score."""
    def clean(value: str) -> str:
        return re.sub(r"[^a-z0-9 ]+", " ", value.lower()).strip()

    return SequenceMatcher(None, clean(left), clean(right)).ratio()


def _crossref_metadata(message: dict[str, Any], normalise: Callable[[Any], str | None]) -> dict[str, Any]:
    titles = message.get("title") or []
    dates = (message.get("published") or message.get("issued") or {}).get("date-parts") or []
    return {
        "doi": normalise(message.get("DOI")), "title": titles[0] if titles else None,
        "year": dates[0][0] if dates and dates[0] else None,
        "type": message.get("type"), "repository": _crossref_repository(message),
        "relation": message.get("relation") or {}, "license_urls": _crossref_licenses(message),
        "registry": "crossref",
    }


def _crossref_licenses(message: dict[str, Any]) -> list[str]:
    return [item.get("URL") for item in message.get("license") or []
            if isinstance(item, dict) and isinstance(item.get("URL"), str)]


def _crossref_repository(message: dict[str, Any]) -> str | None:
    candidates = [item.get("URL") for item in message.get("link") or []
                  if isinstance(item, dict)] + [message.get("URL")]
    return next((url for url in candidates if github_repository(url)), None)


def _datacite_metadata(payload: dict[str, Any], normalise: Callable[[Any], str | None]) -> dict[str, Any]:
    attributes = (payload.get("data") or {}).get("attributes") or {}
    titles = attributes.get("titles") or []
    resource_type = (attributes.get("types") or {}).get("resourceTypeGeneral")
    rights = [item.get("rightsUri") for item in attributes.get("rightsList") or []
              if isinstance(item, dict) and isinstance(item.get("rightsUri"), str)]
    return {
        "doi": normalise(attributes.get("doi") or (payload.get("data") or {}).get("id")),
        "title": titles[0].get("title") if titles else None,
        "year": attributes.get("publicationYear"), "type": resource_type,
        "repository": attributes.get("url") if github_repository(attributes.get("url")) else None,
        "related": attributes.get("relatedIdentifiers") or [],
        "license_urls": rights, "registry": "datacite",
    }


def _openalex_metadata(payload: dict[str, Any], normalise: Callable[[Any], str | None]) -> dict[str, Any]:
    locations = [payload.get("primary_location") or {}] + (payload.get("locations") or [])
    repository = next((location.get("landing_page_url") for location in locations
                       if github_repository(location.get("landing_page_url"))), None)
    return {"doi": normalise(payload.get("doi")), "title": payload.get("title"),
            "year": payload.get("publication_year"), "type": payload.get("type"),
            "repository": repository, "registry": "openalex", "license_urls": []}


def github_repository(url: Any) -> tuple[str, str] | None:
    """Return an owner/repository pair for a canonical public GitHub URL."""
    if not isinstance(url, str):
        return None
    parsed = urllib.parse.urlsplit(url.strip())
    if parsed.scheme != "https" or (parsed.hostname or "").lower() != "github.com":
        return None
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2 or any(part in {".", ".."} for part in parts):
        return None
    owner, name = parts
    return owner, name.removesuffix(".git")


def published_doi(metadata: dict[str, Any], normalise: Callable[[Any], str | None]) -> str | None:
    """Find a registry-declared published version of a preprint."""
    relations = metadata.get("relation") or {}
    for key in ("is-preprint-of", "has-preprint"):
        for item in relations.get(key) or []:
            if str(item.get("id-type", "doi")).lower() == "doi":
                if doi := normalise(item.get("id")):
                    return doi
    for item in metadata.get("related") or []:
        if item.get("relationType") in {"IsVersionOf", "IsPreviousVersionOf"}:
            if item.get("relatedIdentifierType") == "DOI":
                if doi := normalise(item.get("relatedIdentifier")):
                    return doi
    return None


def declared_published_doi(message: Mapping[str, Any], normalise: Callable[[Any], str | None]) -> str | None:
    """Read Crossref's preprint-to-publication relation before generic metadata."""
    for relation in (message.get("relation") or {}).get("is-preprint-of") or []:
        if str(relation.get("id-type", "doi")).lower() == "doi":
            if doi := normalise(relation.get("id")):
                return doi
    return None


class Resolver:
    """Small, fixed-host resolver used by issue intake."""

    def __init__(self, fetch: Fetch = http_json, sleep: Sleep = time.sleep,
                 normalise: Callable[[Any], str | None] | None = None):
        self.fetch = fetch
        self.sleep = sleep
        self.normalise = normalise

    def get(self, url: str) -> dict[str, Any] | None:
        """Fetch one URL through the injected transport."""
        return fetch_json(url, self.fetch, self.sleep)

    def by_doi(self, doi: str) -> dict[str, Any] | None:
        """Resolve Crossref first, then DataCite, then OpenAlex."""
        quoted = urllib.parse.quote(doi, safe="")
        payload = self.get(CROSSREF_WORK.format(quoted))
        if payload and isinstance(payload.get("message"), dict):
            published = declared_published_doi(payload["message"], self.normalise)
            if published and published != doi:
                metadata = _crossref_metadata(payload["message"], self.normalise)
                metadata["published_doi"] = published
                return metadata
            return _crossref_metadata(payload["message"], self.normalise)
        payload = self.get(DATACITE_WORK.format(quoted))
        if payload and isinstance(payload.get("data"), dict):
            return _datacite_metadata(payload, self.normalise)
        payload = self.get(OPENALEX_WORK.format(quoted))
        return _openalex_metadata(payload, self.normalise) if payload else None

    def by_title(self, title: str, prefix: str | None) -> dict[str, Any] | None:
        """Resolve a title only when one sufficiently similar result is clear."""
        query = urllib.parse.urlencode({"query.bibliographic": title, "rows": TITLE_CANDIDATES,
                                        "select": "DOI,title"})
        payload = self.get(CROSSREF_SEARCH.format(query))
        items = ((payload or {}).get("message") or {}).get("items") or []
        matches = [(title_similarity(title, (item.get("title") or [""])[0]), item)
                   for item in items if item.get("title")]
        if prefix:
            preferred = [match for match in matches
                         if str(match[1].get("DOI", "")).lower().startswith(prefix + "/")]
            if preferred:
                matches = preferred
        if not matches:
            return None
        score, best = max(matches, key=lambda match: match[0])
        tied = [match for match in matches if match[0] == score]
        if score < TITLE_FLOOR or len(tied) != 1:
            return None
        return self.by_doi(self.normalise(best["DOI"]))

    def access(self, doi: str, email: str | None) -> dict[str, Any]:
        """Resolve access without treating lookup failure as closed access."""
        if not email:
            return _unresolved_access("email is required for Unpaywall")
        query = urllib.parse.urlencode({"email": email})
        try:
            payload = self.get(UNPAYWALL_WORK.format(urllib.parse.quote(doi, safe=""), query))
        except RegistryUnavailable as error:
            return _unresolved_access(str(error))
        if payload is None:
            return self._unresolved_access("Unpaywall has no record")
        return _access_metadata(payload)

    def registry_license(self, metadata: dict[str, Any]) -> dict[str, Any] | None:
        """Extract declared article rights without querying a proposed URL."""
        url, spdx, reuse = most_restrictive_license(metadata.get("license_urls") or [])
        if not spdx and not url:
            return None
        return {"spdx": spdx, "url": url, "source_reuse": reuse,
                "registry": metadata.get("registry")}

    def repository(self, url: str | None) -> dict[str, Any] | None:
        """Resolve public GitHub metadata and code licence independently."""
        identity = github_repository(url)
        if not identity:
            return None
        payload = self.get(GITHUB_REPOSITORY.format(*identity))
        if not payload or payload.get("private") is True:
            return {"status": "gone", "code_license": None, "repository": url}
        if "status" in payload and "full_name" not in payload:
            return {"status": payload["status"], "code_license": payload.get("code_license"),
                    "repository": payload.get("repository") or url}
        full_name = payload.get("full_name") or "/".join(identity)
        return {"status": "moved" if full_name.lower() != "/".join(identity).lower() else "exists",
                "code_license": (payload.get("license") or {}).get("spdx_id"),
                "repository": payload.get("html_url") or url,
                "archived": payload.get("archived")}


def _access_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    best = payload.get("best_oa_location") or {}
    license_name = best.get("license")
    if license_name and license_name.startswith("http"):
        license_name = spdx_from_license_url(license_name) or license_name
    reuse = _classify_reuse(license_name)
    verified_via = "unpaywall_best_oa_location" if best else "unpaywall"
    return {"type": payload.get("oa_status") or ("closed" if payload.get("is_oa") is False else "unknown"),
            "license": license_name, "is_oa": payload.get("is_oa"),
            "oa_status": payload.get("oa_status"), "source_reuse": reuse,
            "verified_via": verified_via, "error": None}


def _classify_reuse(license_name: str | None) -> str:
    if not license_name:
        return "none"
    from scripts.license_tier import source_reuse_for_license

    reuse = source_reuse_for_license(license_name)
    if reuse is not None:
        return {"full": "permissive", "limited": "restricted", "none": "none"}[reuse]
    lowered = license_name.lower()
    if any(marker in lowered for marker in ("-nc", "-nd")):
        return "restricted"
    return "permissive" if lowered in {"cc0", "cc-by", "cc-by-sa", "public-domain", "pd"} else "other"


def _unresolved_access(error: str) -> dict[str, Any]:
    return {"type": "unknown", "license": None, "is_oa": None, "source_reuse": "unknown",
            "verified_via": "unresolved", "error": error}
