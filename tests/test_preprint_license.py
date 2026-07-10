"""Pre-print licence resolution must never guess.

The rule this guards: a pre-print is admissible only when its *actual* posting
licence permits the intended reuse. Every failure mode -- unknown licence, no
licence declared, registry unreachable -- must surface as a loud status, never as
a permissive default and never as a restrictive default that hides a lookup bug.
"""

import ast
import pathlib
import sys
import urllib.error

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import preprint_license as pl
from scripts.license_tier import load_map, source_reuse_for_license

CC_BY = "https://creativecommons.org/licenses/by/4.0/"
CC_BY_NC_ND = "http://creativecommons.org/licenses/by-nc-nd/4.0/"
CC_BY_ND = "https://creativecommons.org/licenses/by-nd/4.0/legalcode"
CC_ZERO = "http://creativecommons.org/publicdomain/zero/1.0/"
ARXIV_DEFAULT = "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"


def crossref(work_type: str, license_urls: list[str], institution: str | None = None) -> dict:
    message = {"type": work_type, "license": [{"URL": u} for u in license_urls]}
    if institution:
        message["institution"] = [{"name": institution}]
    return {"message": message}


def server_api(token: str | None) -> dict:
    return {"collection": [{"license": token}] if token is not None else []}


def datacite(resource_type: str, rights_uris: list[str]) -> dict:
    rights = [{"rightsUri": u} for u in rights_uris]
    return {"data": {"attributes": {"types": {"resourceTypeGeneral": resource_type}, "rightsList": rights}}}


def fetch_from(routes: dict):
    """A hermetic fetch: returns a canned payload per URL substring, else None (404)."""

    def _fetch(url: str):
        for fragment, payload in routes.items():
            if fragment in url:
                return payload
        return None

    return _fetch


def crossref_only(payload):
    return fetch_from({"api.crossref.org": payload})


def datacite_only(payload):
    return fetch_from({"api.datacite.org": payload})


# --- Positive: fires across four distinct sciences, on both registries ---------

@pytest.mark.parametrize(
    "science,doi,fetch,expected_spdx",
    [
        # biology (bioRxiv, Crossref)
        ("biology", "10.1101/2020.01.01.000001", crossref_only(crossref("posted-content", [CC_BY])), "CC-BY-4.0"),
        # clinical medicine (medRxiv, Crossref)
        ("clinical", "10.1101/2020.03.24.20042937", crossref_only(crossref("posted-content", [CC_BY_ND])), "CC-BY-ND-4.0"),
        # chemistry (ChemRxiv, Crossref)
        ("chemistry", "10.26434/chemrxiv-2024-1zk33", crossref_only(crossref("posted-content", [CC_BY_NC_ND])), "CC-BY-NC-ND-4.0"),
        # astrophysics (arXiv, DataCite) -- a science with no presence in this repo
        ("astrophysics", "10.48550/arxiv.2502.05114", datacite_only(datacite("Preprint", [CC_ZERO])), "CC0-1.0"),
    ],
)
def test_resolves_on_every_science_and_registry(science, doi, fetch, expected_spdx):
    result = pl.resolve_preprint_license(doi, fetch=fetch)
    assert result.status == pl.STATUS_RESOLVED, science
    assert result.spdx == expected_spdx, science


def test_only_full_reuse_licences_are_admissible_as_open_access():
    admissible = pl.resolve_preprint_license("d/1", fetch=crossref_only(crossref("posted-content", [CC_BY])))
    assert admissible.admissible_as_open_access

    for url in (CC_BY_NC_ND, CC_BY_ND, ARXIV_DEFAULT):
        blocked = pl.resolve_preprint_license("d/1", fetch=crossref_only(crossref("posted-content", [url])))
        assert not blocked.admissible_as_open_access, url


def test_arxiv_default_licence_grants_no_reuse():
    result = pl.resolve_preprint_license("d/1", fetch=datacite_only(datacite("Preprint", [ARXIV_DEFAULT])))
    assert result.status == pl.STATUS_RESOLVED
    assert result.source_reuse == "none"
    assert not result.admissible_as_open_access


# --- Negative: stays loud on every not-applicable / unresolvable input ---------

def test_journal_article_is_not_a_preprint_and_is_not_open():
    result = pl.resolve_preprint_license("d/1", fetch=crossref_only(crossref("journal-article", [CC_BY])))
    assert result.status == pl.STATUS_NOT_A_PREPRINT
    assert not result.admissible_as_open_access


def test_unrecognised_licence_url_is_loud_not_defaulted():
    result = pl.resolve_preprint_license("d/1", fetch=crossref_only(crossref("posted-content", ["https://example.org/bespoke"])))
    assert result.status == pl.STATUS_UNKNOWN_LICENCE
    assert result.source_reuse is None
    assert not result.admissible_as_open_access


def test_preprint_with_no_declared_licence_is_loud():
    result = pl.resolve_preprint_license("d/1", fetch=crossref_only(crossref("posted-content", [])))
    assert result.status == pl.STATUS_NO_LICENCE_DECLARED
    assert not result.admissible_as_open_access


def test_absent_from_both_registries_is_unresolved():
    result = pl.resolve_preprint_license("d/1", fetch=fetch_from({}))
    assert result.status == pl.STATUS_UNRESOLVED
    assert not result.admissible_as_open_access


def test_network_failure_is_unresolved_never_clean():
    def exploding_fetch(url):
        raise urllib.error.URLError("registry unreachable")

    result = pl.resolve_preprint_license("d/1", fetch=exploding_fetch)
    assert result.status == pl.STATUS_UNRESOLVED
    assert not result.admissible_as_open_access


def test_empty_doi_is_unresolved():
    assert pl.resolve_preprint_license("", fetch=fetch_from({})).status == pl.STATUS_UNRESOLVED


# --- DOI normalisation is two-sided: strips a version marker, keeps a real segment ---

def test_landing_page_version_suffix_is_stripped_only_on_retry():
    seen = []

    def fetch(url):
        seen.append(url)
        return crossref("posted-content", [CC_BY]) if url.endswith("000001") else None

    result = pl.resolve_preprint_license("10.1101/2020.01.01.000001v3.abstract", fetch=fetch)
    assert result.status == pl.STATUS_RESOLVED
    assert result.doi_used == "10.1101/2020.01.01.000001"
    assert any("v3.abstract" in url for url in seen), "the DOI as recorded must be tried first"


def test_a_real_dot_v_segment_is_never_stripped():
    assert pl.strip_version_suffix("10.6084/m9.figshare.28876751.v2") == "10.6084/m9.figshare.28876751.v2"


def test_exact_doi_wins_when_it_resolves():
    result = pl.resolve_preprint_license("10.6084/m9.figshare.28876751.v2",
                                         fetch=crossref_only(crossref("posted-content", [CC_BY])))
    assert result.doi_used == "10.6084/m9.figshare.28876751.v2"


# --- Server-API fallback, routed by the registry's declared institution --------

def test_server_api_recovers_a_licence_crossref_does_not_declare():
    fetch = fetch_from({"api.crossref.org": crossref("posted-content", [], institution="bioRxiv"),
                        "api.biorxiv.org": server_api("cc_by_nc_nd")})
    result = pl.resolve_preprint_license("d/1", fetch=fetch)
    assert result.status == pl.STATUS_RESOLVED
    assert result.registry == "biorxiv_api"
    assert result.spdx == "CC-BY-NC-ND-4.0"
    assert not result.admissible_as_open_access


def test_server_api_recovers_when_crossref_points_at_a_faq_page():
    faq = "https://www.biorxiv.org/about/FAQ#license"
    fetch = fetch_from({"api.crossref.org": crossref("posted-content", [faq], institution="bioRxiv"),
                        "api.biorxiv.org": server_api("cc_by")})
    result = pl.resolve_preprint_license("d/1", fetch=fetch)
    assert result.status == pl.STATUS_RESOLVED
    assert result.admissible_as_open_access


def test_author_reserved_all_rights_is_a_known_refusal_not_an_unknown():
    fetch = fetch_from({"api.crossref.org": crossref("posted-content", [], institution="bioRxiv"),
                        "api.biorxiv.org": server_api("cc_no")})
    result = pl.resolve_preprint_license("d/1", fetch=fetch)
    assert result.status == pl.STATUS_RESOLVED
    assert result.spdx == "NoReuse-1.0"
    assert result.source_reuse == "none"
    assert not result.admissible_as_open_access


def test_unknown_server_token_stays_loud():
    fetch = fetch_from({"api.crossref.org": crossref("posted-content", [], institution="bioRxiv"),
                        "api.biorxiv.org": server_api("some_new_token")})
    result = pl.resolve_preprint_license("d/1", fetch=fetch)
    assert result.status == pl.STATUS_UNKNOWN_LICENCE
    assert result.source_reuse is None


def test_an_unknown_institution_never_triggers_a_server_call():
    called = []

    def fetch(url):
        called.append(url)
        return crossref("posted-content", [], institution="Some Unlisted Server") if "crossref" in url else None

    result = pl.resolve_preprint_license("d/1", fetch=fetch)
    assert result.status == pl.STATUS_NO_LICENCE_DECLARED
    assert not any("biorxiv" in url for url in called)


def test_server_without_a_record_falls_back_to_the_registry_outcome():
    fetch = fetch_from({"api.crossref.org": crossref("posted-content", [], institution="bioRxiv"),
                        "api.biorxiv.org": server_api(None)})
    assert pl.resolve_preprint_license("d/1", fetch=fetch).status == pl.STATUS_NO_LICENCE_DECLARED


def test_every_server_token_maps_to_a_known_source_reuse_value():
    """A token whose SPDX has no source_reuse row would resolve to a silent unknown."""
    config = pl.load_servers()
    for token, spdx in config["license_tokens"].items():
        assert source_reuse_for_license(spdx, load_map()) is not None, f"{token} -> {spdx} has no source_reuse row"


# --- Licence URL parsing ------------------------------------------------------

@pytest.mark.parametrize("url,spdx", [
    (CC_BY, "CC-BY-4.0"),
    (CC_BY_NC_ND, "CC-BY-NC-ND-4.0"),
    (CC_ZERO, "CC0-1.0"),
    (ARXIV_DEFAULT, "arXiv-1.0"),
    ("https://opensource.org/licenses/MIT", None),
    ("", None),
])
def test_spdx_from_license_url(url, spdx):
    assert pl.spdx_from_license_url(url) == spdx


def test_unknown_spdx_has_no_source_reuse_entry():
    """None means unknown; it must not collapse onto the known refusal 'none'."""
    assert source_reuse_for_license("Totally-Made-Up-1.0", load_map()) is None
    assert source_reuse_for_license("arXiv-1.0", load_map()) == "none"


# --- A rate-limited registry is not an absent DOI ------------------------------

def test_absent_and_retryable_statuses_are_disjoint():
    assert not set(pl.ABSENT_STATUS) & set(pl.RETRYABLE_STATUS)


def test_retry_delay_honours_retry_after_then_backs_off():
    assert pl.retry_delay(1, "7") == 7.0
    assert pl.retry_delay(1, None) == pl.BACKOFF_BASE_S
    assert pl.retry_delay(3, None) > pl.retry_delay(2, None)
    assert pl.retry_delay(2, "not-a-number") == pl.retry_delay(2, None)


def test_fetch_json_retries_a_rate_limit_then_succeeds(monkeypatch):
    attempts = []

    def flaky(url):
        attempts.append(url)
        if len(attempts) < 3:
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {"Retry-After": "0"}, None)
        return {"ok": True}

    monkeypatch.setattr(pl, "_get_json", flaky)
    monkeypatch.setattr(pl.time, "sleep", lambda _s: None)
    assert pl.fetch_json("https://example.org/x") == {"ok": True}
    assert len(attempts) == 3


def test_fetch_json_gives_up_loudly_rather_than_reporting_absence(monkeypatch):
    def always_limited(url):
        raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)

    monkeypatch.setattr(pl, "_get_json", always_limited)
    monkeypatch.setattr(pl.time, "sleep", lambda _s: None)
    with pytest.raises(urllib.error.HTTPError):
        pl.fetch_json("https://example.org/x")


def test_a_rate_limited_registry_never_yields_a_clean_answer(monkeypatch):
    """The whole point: 429 must surface as unresolved, never as not_a_preprint."""
    def always_limited(url):
        raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)

    monkeypatch.setattr(pl, "_get_json", always_limited)
    monkeypatch.setattr(pl.time, "sleep", lambda _s: None)
    result = pl.resolve_preprint_license("d/1", fetch=pl.fetch_json)
    assert result.status == pl.STATUS_UNRESOLVED
    assert not result.admissible_as_open_access


# --- Generality guards --------------------------------------------------------

def _string_constants(module_path: pathlib.Path):
    """Every string literal in a module, excluding docstrings (and comments)."""
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    docstrings = {ast.get_docstring(tree)}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            docstrings.add(ast.get_docstring(node))
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value not in docstrings]


def test_no_doi_literals_in_scripts():
    """A DOI literal in general code is an overfit to one paper. Keep them in tests."""
    import re
    doi_shape = re.compile(r"\b10\.\d{4,9}/")
    offenders = []
    for script in sorted((pathlib.Path(__file__).parent.parent / "scripts").glob("*.py")):
        offenders += [f"{script.name}: {s}" for s in _string_constants(script) if doi_shape.search(s)]
    assert not offenders, f"DOI literals belong in tests/, not general code: {offenders}"


def test_preprint_detection_never_dispatches_on_a_doi_prefix():
    """Pre-print-ness comes from the registry's declared type, not a registrant prefix."""
    source = (pathlib.Path(__file__).parent.parent / "scripts" / "preprint_license.py")
    for literal in _string_constants(source):
        assert not literal.startswith("10."), f"prefix dispatch re-entered via {literal!r}"
