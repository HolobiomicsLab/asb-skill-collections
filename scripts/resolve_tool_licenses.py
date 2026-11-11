"""Resolve each tool record's own licence and repository, and write tool_licenses.json.

`enrich_tools_index.py` reads that file and refuses to tier a tool without it, so
this script is where a tool's licence is allowed to come from. Precision comes
before coverage: a wrong licence shown as `open` is worse than `unknown`.

Sources, in order of precedence (governance/LICENSE_TIERS.md, "Where a tool
licence is allowed to come from"):

- `reviewed`        governance/tool_licences_reviewed.yaml, checked by hand. A
                    name it lists is never looked up anywhere else.
- `self_published`  the tool is the subject of a corpus paper, so that paper's
                    repository is the tool's. Offline.
- `registry`        a package of the same name in a registry declared in
                    governance/tool_registries.yaml, accepted only when
                    `scripts/tool_identity.py` judges, from the record's own
                    evidence in its collection, that the package is the tool.

The registry declares the licence string; `scripts/tool_licence_text.py` reads
it without inventing a version. Anything unresolved stays `unknown`, which is a
true statement, and the reason it was withheld is reported.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

import yaml
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts import reviewed_tool_licences as reviewed_map
from scripts.license_tier import (UNESTABLISHED_DETECTIONS, load_map, tier_for_license,
                                  tool_license, warn_legacy_tool_licenses)
from scripts.tool_identity import build_context, collection_word_share, judge, repo_key
from scripts.tool_licence_text import read_licence
from scripts.repository_licence import (DETECTION_REPOSITORY_FILE, agrees, gnu_family, raw_urls,
                                        repository_name, repository_readme,
                                        repository_statement)
from scripts.tool_registry_sources import Fetcher, Registry, RegistryRefused, normalize

_GOVERNANCE = pathlib.Path(__file__).resolve().parent.parent / "governance"
_REGISTRIES = _GOVERNANCE / "tool_registries.yaml"
_COMMON_WORDS = _GOVERNANCE / "tool_name_common_words.txt"

DETECTION_REVIEWED = "reviewed-map"
DETECTION_SELF_PUBLISHED_FALLBACK = "self-published"


def load_registry_config(path=None) -> dict:
    """The whole registry governance document."""
    return yaml.safe_load(pathlib.Path(path or _REGISTRIES).read_text(encoding="utf-8")) or {}


def load_registries(path=None) -> list:
    """Registry definitions from governance/tool_registries.yaml."""
    return load_registry_config(path).get("registries") or []


def excluded_pairs(config) -> set:
    """``{(tool_slug, registry_id)}`` a human reviewed and rejected."""
    return {(e.get("tool"), e.get("registry")) for e in (config.get("excluded_matches") or [])}


def load_common_words(path=None) -> frozenset:
    """English words that are also package names; see the file's header."""
    p = pathlib.Path(path or _COMMON_WORDS)
    if not p.is_file():
        return frozenset()
    return frozenset(normalize(line) for line in p.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.startswith("#"))


# --------------------------------------------------------------------------- #
# The introducing paper                                                       #
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
    if not paper or tool_license(paper) is None:
        return None
    block = tool_license(paper) or {}
    detection = block.get("detection")
    licence = block.get("spdx")
    if detection in UNESTABLISHED_DETECTIONS or not licence:
        return None
    reading = read_licence(licence)
    tier = reading["tier"] or tier_for_license(licence)
    return {"license": licence, "license_tier": tier, "license_raw": licence,
            "license_detection": detection, "license_evidence": paper.get("repo_url"),
            "repo_url": paper.get("repo_url"), "route": "self_published",
            "matched": paper.get("name")}


# --------------------------------------------------------------------------- #
# Registry candidates                                                         #
# --------------------------------------------------------------------------- #

_CODE_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org")
_REPO_ROOT = re.compile(
    r"(https?://(?:www\.)?(?:" + "|".join(h.replace(".", r"\.") for h in _CODE_HOSTS) +
    r")/[^/\s,;]+/[^/\s,;#?]+?)(?:\.git)?(?:/(?:-/)?(?:issues|pulls|tree|blob|wiki)\b.*)?/?$",
    re.I)


def pick_repo_url(values):
    """The repository among a registry's declared URLs, canonicalised, or None.

    Registries mix a project homepage, an issue tracker and a git remote into the
    same fields. CAMERA declares a lab web page as `URL` and
    `.../CAMERA/issues/new` as `BugReports`; the answer to "where do I read the
    source" is the second one with its tracker path removed.
    """
    for value in values:
        for candidate in re.split(r"[,\s]+", str(value).strip()):
            match = _REPO_ROOT.match(candidate.rstrip("/"))
            if match:
                return match.group(1)
    return next((str(v).split(",")[0].strip() for v in values if v), None)


def _read_registry_licence(registry, record) -> dict:
    """One reading of the record's licence statement(s); disagreeing statements are unread."""
    readings = [read_licence(s, registry.spec["license_format"]
                             if registry.spec["license_format"] != "pypi_info" else "spdx_or_text")
                for s in registry.licence_strings(record)]
    read = [r for r in readings if r["tier"]]
    if not read:
        return readings[0] if readings else {"raw": None, "license": None, "tier": None,
                                             "reason": "no-licence-field"}
    if len({r["tier"] for r in read}) > 1:
        return {"raw": " | ".join(str(r["raw"]) for r in read), "license": None, "tier": None,
                "reason": "statements-disagree"}
    return read[0]


def _introducing_hint(record, ctx, tool_yaml) -> bool:
    """Whether the record looks like it carries the tool's own paper or repository.

    Used only to decide whether to ask a per-name registry (bio.tools) at all:
    its answer is then accepted only on a shared repository or DOI.
    """
    return ctx.is_subject


def registry_candidates(record, ctx, tool_yaml, registries, common_words, excluded) -> list:
    """Every same-name package in the declared registries, with its identity verdict."""
    names = [n for n in (record.get("name"), record.get("slug")) if n]
    code = ctx.code_evidence()
    out = []
    for registry in registries:
        if (record.get("slug"), registry.id) in excluded:
            out.append({"registry": registry.id, "excluded": True})
            continue
        allow = True
        if registry.spec["index_shape"] == "per_name":
            ask = registry.spec.get("ask_when")
            # bio.tools costs one request per name and adds no ecosystem; it is not
            # asked about a record an earlier registry has already resolved. PyPI is
            # always asked when the record has Python evidence, because a second
            # ecosystem with another licence must make the record unknown (K3).
            if ask == "introducing_hint" and any(
                    c.get("verdict") and c["verdict"].accept and c["reading"]["tier"] for c in out):
                continue
            if ask == "code_python":
                allow = bool(code.get("python"))
            elif ask == "introducing_hint":
                allow = _introducing_hint(record, ctx, tool_yaml)
            else:
                allow = False
        for canonical, pkg in registry.lookup(names, allow_request=allow):
            verdict = judge(registry, canonical, pkg, ctx, common_words)
            reading = _read_registry_licence(registry, pkg)
            out.append({"registry": registry.id, "registry_obj": registry, "canonical": canonical,
                        "record": pkg, "verdict": verdict, "reading": reading})
    _share_identity(out)
    return out


def _repo_keys(c) -> set:
    return {k for k in (repo_key(v) for v in c["registry_obj"].repo_values(c["record"])) if k}


def _share_identity(candidates) -> None:
    """Accept a package that declares the same repository as one already accepted on
    strong evidence: two registries listing one repository describe one tool.

    bio.tools may establish bedtools from a shared repository while the Bioconda
    package of the same repository has no corroboration of its own; the Bioconda
    record then declares the licence the package ships under now.
    """
    anchors = [c for c in candidates if c.get("verdict") and c["verdict"].accept
               and any(k["kind"] in ("repository", "publication", "code")
                       for k in c["verdict"].corroboration)]
    for c in candidates:
        if not c.get("verdict") or c["verdict"].accept or c["verdict"].contradiction and any(
                k["kind"] in ("ecosystem", "data-package") for k in c["verdict"].contradiction):
            continue
        if c["verdict"].reason in ("data-package", "registry-flags-restricted-use"):
            continue
        for anchor in anchors:
            shared = sorted(_repo_keys(c) & _repo_keys(anchor))
            if shared:
                c["verdict"].accept = True
                c["verdict"].reason = "corroborated"
                c["verdict"].corroboration = [{"kind": "repository", "value": shared[0],
                                               "via": anchor["registry"]}]
                break


def _evidence_from_candidate(c) -> dict:
    registry, pkg = c["registry_obj"], c["record"]
    repo = pick_repo_url(registry.repo_values(pkg))
    return {"license": c["reading"]["license"], "license_tier": c["reading"]["tier"],
            "license_raw": c["reading"]["raw"],
            "license_detection": registry.spec["detection"],
            "license_evidence": registry.address(c["canonical"], pkg),
            "repo_url": repo if repo and repo_key(repo) else None,
            "route": f"registry:{registry.id}", "matched": c["canonical"],
            "identity": {"rule": c["verdict"].reason,
                         "corroboration": c["verdict"].corroboration}}


def choose(candidates) -> tuple[dict | None, str]:
    """(evidence, reason) from the judged candidates of one record."""
    judged = [c for c in candidates if not c.get("excluded")]
    if not judged:
        return None, "reviewed-exclusion" if candidates else "no-registry-match"
    accepted = [c for c in judged if c["verdict"].accept]
    if not accepted:
        return None, "identity:" + judged[0]["verdict"].reason
    readable = [c for c in accepted if c["reading"]["tier"]]
    if not readable:
        return None, "licence-unread:" + str(accepted[0]["reading"]["reason"])
    if len(readable) > 1 and len({c["reading"]["license"] for c in readable}) > 1:
        keys = [_repo_keys(c) for c in readable]
        same_entity = all(keys[0] & k for k in keys[1:])
        decisive = [c for c in readable if c["verdict"].corroboration
                    and c["verdict"].reason == "corroborated"]
        if same_entity:
            # One tool in several registries: the first declared registry wins,
            # the others are kept for the reviewer.
            evidence = _evidence_from_candidate(readable[0])
            evidence["superseded"] = [{"route": f"registry:{c['registry']}",
                                       "license": c["reading"]["license"],
                                       "license_evidence": c["registry_obj"].address(
                                           c["canonical"], c["record"])}
                                      for c in readable[1:]]
            return evidence, "resolved"
        if len(decisive) == 1:
            readable = decisive
        else:
            return None, "several-packages-differ:" + ",".join(
                f"{c['registry']}={c['reading']['license']}" for c in readable)
    chosen = readable[0]
    if chosen["registry_obj"].scope == "general":
        # A same-name package that was not contradicted but declares another licence
        # makes the record unknown: bio.tools still lists bedtools as GPL-2.0 while
        # the Bioconda package has been MIT since 2.28, and neither can be preferred
        # without evidence that the package is the tool.
        others = [c for c in judged if c is not chosen and c["reading"]["tier"]
                  and c["reading"]["license"] != chosen["reading"]["license"]
                  and not any(k["kind"] in ("ecosystem", "data-package")
                              for k in c["verdict"].contradiction)]
        if others:
            return None, "registries-disagree:" + ",".join(
                f"{c['registry']}={c['reading']['license']}" for c in [chosen] + others)
    return _evidence_from_candidate(chosen), "resolved"


THIRD_PARTY = frozenset({"bioconda", "biotools"})
R_DECLARED = frozenset({"bioconductor", "cran"})


def confirm(evidence, fetcher, tool_name=None, readme=True) -> tuple[dict | None, str]:
    """(evidence, outcome): the repository's licence file, then its README.

    A record that would be recorded `open` is withheld when the repository's README
    restricts use of the tool in plain words (USAT: an LGPL-2.1 file, and a README
    that says "Free for all academic and educational purposes. A license is needed
    ... for any industrial and any other purposes"): the tool's own statements then
    contradict each other, as MassCube's do.
    """
    out, outcome = _confirm_file(evidence, fetcher, tool_name)
    if not (readme and out and out.get("license_tier") == "open"):
        return out, outcome
    found = repository_readme(out.get("repo_url"), fetcher)
    if found and found["sentence"]:
        return None, f"withheld-readme-restriction:{found['sentence']}"
    if found and out.get("confirmation") is not None:
        out["confirmation"]["readme"] = found["file"]
    return out, outcome


def _confirm_file(evidence, fetcher, tool_name=None) -> tuple[dict | None, str]:
    """(evidence, outcome) after checking a registry licence against the repository.

    Who wrote the registry's licence field decides what the repository may change:

    - Bioconda, bio.tools (written by a third party): the repository's licence
      file wins when it is read (`replaced`); without one the record is unknown
      (`withheld-unconfirmed`), because a third-party string is not the tool's
      own statement.
    - PyPI (the authors' metadata, often careless): a file of the same tier with
      another licence replaces it; a file of another tier makes the record unknown
      (`withheld-contradiction`), because the authors' two statements contradict
      each other (MassCube: PyPI says CC BY-NC 4.0, the repository Apache-2.0);
      no readable file keeps the PyPI licence (`kept-unconfirmed`).
    - Bioconductor, CRAN (the DESCRIPTION file is the declared licence): the
      registry licence is kept. Only the repository's DESCRIPTION is read, and only
      a tier contradiction with it withholds. A LICENSE file may carry terms for a
      bundled component (xcms) and never overrides the declaration.

    A permissive licence file that adds terms of its own (bmxp: "MIT License (Dual
    License)", a separate commercial licence for redistribution) withholds the
    record for every source unless the file is read as `noncommercial` and the
    registry was written by a third party (`withheld-added-terms`).

    A replacement reads only a repository named like the package or the record
    (`withheld-repository-name`), and two GNU statements of one family that differ
    only in version give the unversioned family (`family-fallback`).

    `confirmed` means the file agrees in family and version.
    """
    registry = evidence["route"].split(":", 1)[1]
    statement = repository_statement(evidence.get("repo_url"), fetcher,
                                     description_only=registry in R_DECLARED)
    if statement and statement["reason"].startswith("permissive-with") and not (
            statement["tier"] and registry in THIRD_PARTY):
        return None, (f"withheld-added-terms:{registry}={evidence['license']}"
                      f"|repository={statement['license'] or 'unread'}")
    read = bool(statement and statement["tier"])
    if read and agrees(evidence["license"], statement["license"]):
        evidence["confirmation"] = {"status": "confirmed", "file": statement["file"],
                                    "file_license": statement["license"]}
        return evidence, "confirmed"
    if read:
        differs = {"file": statement["file"], "file_license": statement["license"],
                   "file_tier": statement["tier"], "registry_license": evidence["license"],
                   "registry_license_raw": evidence.get("license_raw"),
                   "registry_tier": evidence["license_tier"],
                   "registry_evidence": evidence.get("license_evidence")}
        same_tier = statement["tier"] == evidence["license_tier"]
        if registry in R_DECLARED or (registry == "pypi" and not same_tier):
            if not same_tier:
                return None, (f"withheld-contradiction:{registry}={evidence['license']}"
                              f"|repository={statement['license']}")
            evidence["confirmation"] = dict(differs, status="kept-registry-declares")
            return evidence, "kept-registry-declares"
        # A replacement must read the tool's own repository: its name is the
        # package's or the record's (bootRangespaper holds a paper's scripts, the
        # tool is elsewhere). A repository that moved under the same name passes.
        name = repository_name(evidence.get("repo_url"))
        if normalize(name) not in {normalize(evidence.get("matched")), normalize(tool_name)} - {""}:
            return None, f"withheld-repository-name:{name}"
        out = dict(evidence)
        family = gnu_family(evidence["license"], statement["license"])
        if family:
            # Two GNU statements of one family that differ only in version (FastTree:
            # a GPL-3 text, source headers "version 2 or later"): the family is what
            # both support.
            out.update(license=family, license_tier=read_licence(family)["tier"],
                       license_raw=family, license_detection=DETECTION_REPOSITORY_FILE,
                       license_evidence=statement["file"])
            out["confirmation"] = dict(differs, status="family-fallback")
            return out, "family-fallback"
        out.update(license=statement["license"], license_tier=statement["tier"],
                   license_raw=statement["license"],
                   license_detection=DETECTION_REPOSITORY_FILE,
                   license_evidence=statement["file"])
        out["confirmation"] = dict(differs, status="replaced")
        return out, "replaced"
    why = statement["reason"] if statement else (
        "no-code-host-repository" if not raw_urls(evidence.get("repo_url")) else "no-licence-file")
    if registry in THIRD_PARTY:
        return None, f"withheld-unconfirmed:{why}"
    evidence["confirmation"] = {"status": "kept-unconfirmed", "reason": why,
                                "file": (statement or {}).get("file")}
    return evidence, "kept-unconfirmed"


def reconcile(self_published, registry, _map=None) -> tuple:
    """(evidence, conflict) from the introducing-paper route and the registry route.

    Where both fire, the registry wins on the licence string: a package declares
    its own licence, a repository read infers one from whatever LICENSE file sits
    at the root (`sneumann/xcms`: DESCRIPTION says `GPL (>= 2)`, the LICENSE file
    classifies as LGPL-3.0 because it carries terms for a bundled component).
    A disagreement in *tier* is a contradiction, so the tool resolves to nothing.
    """
    if not self_published or not registry:
        return self_published or registry, None
    tier_a = self_published.get("license_tier") or tier_for_license(self_published["license"], _map)
    tier_b = registry.get("license_tier") or tier_for_license(registry["license"], _map)
    if tier_a != tier_b:
        return None, {"self_published": self_published, "registry": registry}
    evidence = dict(registry)
    if not evidence.get("repo_url"):
        evidence["repo_url"] = self_published.get("repo_url")
    if self_published["license"] != registry["license"]:
        evidence["superseded"] = {"license": self_published["license"],
                                  "license_detection": self_published["license_detection"]}
    return evidence, None


def _reviewed_evidence(reading, reason, entry) -> dict:
    return {"license": reading.get("license"), "license_tier": reading.get("license_tier"),
            "license_raw": reading.get("license"), "license_detection": DETECTION_REVIEWED,
            "license_evidence": reading.get("evidence_url"),
            "repo_url": reading.get("repo_url") or entry.get("repo_url"),
            "route": "reviewed", "matched": reading.get("entity") or entry.get("entity"),
            "entry_kind": reading.get("entry_kind"),
            "identity": {"rule": reason, "verified": str(entry.get("verified"))}}


# --------------------------------------------------------------------------- #
# A collection                                                                #
# --------------------------------------------------------------------------- #

def collection_domain(collection_dir) -> str:
    """The collection's domain slug, from collection.yaml or the directory layout."""
    d = pathlib.Path(collection_dir)
    descriptor = d / "collection.yaml"
    if descriptor.is_file():
        doc = yaml.safe_load(descriptor.read_text(encoding="utf-8")) or {}
        slug = str(doc.get("slug") or "")
        if slug:
            return slug.split("/")[0]
    if re.match(r"^v\d+$", d.name):
        return d.parent.name
    return d.name


def resolve(collection_dir, cache_dir, registries=None, *, domain=None, reviewed=None,
            common_words=None, config=None, offline=False, fetcher=None, report=None,
            confirm_registry=True) -> dict:
    """Write tool_licenses.json for a collection and return a summary."""
    d = pathlib.Path(collection_dir)
    tools = json.loads((d / "tools_index.json").read_text(encoding="utf-8"))
    corpus_path = d / "corpus.yaml"
    corpus = yaml.safe_load(corpus_path.read_text(encoding="utf-8")) if corpus_path.is_file() else {}
    corpus_papers = (corpus or {}).get("papers", []) if isinstance(corpus, dict) else []
    warn_legacy_tool_licenses(corpus_papers, corpus_path)
    papers = {p["doi"]: p for p in corpus_papers if p.get("doi")}
    skills_path = d / "skills_index.json"
    skills = {s["slug"]: s for s in json.loads(skills_path.read_text(encoding="utf-8"))} \
        if skills_path.is_file() else {}

    config = config if config is not None else load_registry_config()
    specs = registries if registries is not None else (config.get("registries") or [])
    fetcher = fetcher or Fetcher(cache_dir, offline=offline)
    regs = [Registry(spec, fetcher) for spec in specs]
    excluded = excluded_pairs(config)
    words = common_words if common_words is not None else load_common_words()
    doc = reviewed if reviewed is not None else reviewed_map.load()
    by_name = reviewed_map.index(doc)
    domain = domain or collection_domain(d)
    life_science = domain in set(config.get("life_science_collections") or [])
    tier_map = load_map()
    word_share = collection_word_share(list(skills.values()))

    resolved, withheld, conflicts, outcomes = {}, {}, {}, []
    try:
        for tool in tools:
            slug = tool["slug"]
            tool_yaml_path = d / "tools" / f"{slug}.yaml"
            tool_yaml = yaml.safe_load(tool_yaml_path.read_text(encoding="utf-8")) \
                if tool_yaml_path.is_file() else {}
            citing = [skills[s] for s in tool.get("used_by_skills") or [] if s in skills]
            ctx = build_context(domain, life_science, tool, tool_yaml, citing, word_share)
            outcome = {"slug": slug, "name": tool.get("name"), "citations": len(citing)}
            entry = by_name.get(normalize(tool.get("name"))) or by_name.get(normalize(slug))
            if entry is not None:
                reading, reason = reviewed_map.apply(entry, ctx)
                if reading is not None:
                    evidence = _reviewed_evidence(reading, reason, entry)
                    resolved[slug] = evidence
                    outcome.update(status="resolved" if evidence["license_tier"] != "unknown"
                                   else "reviewed-unknown", reason=reason, evidence=evidence)
                else:
                    withheld[slug] = reason
                    outcome.update(status="withheld", reason=reason)
                outcomes.append(outcome)
                continue
            candidates = registry_candidates(tool, ctx, tool_yaml, regs, words, excluded)
            registry_ev, reason = choose(candidates)
            confirmation = None
            if registry_ev and confirm_registry:
                outcome["confirmation_source"] = registry_ev["route"].split(":", 1)[1]
                outcome["registry_reading"] = {k: registry_ev.get(k) for k in (
                    "matched", "license", "license_tier", "license_evidence", "repo_url")}
                registry_ev, confirmation = confirm(registry_ev, fetcher, tool.get("name"))
                if registry_ev is None:
                    reason = confirmation
            evidence, conflict = reconcile(self_published_evidence(tool, papers), registry_ev,
                                           tier_map)
            if confirmation:
                outcome["confirmation"] = confirmation
            if conflict:
                conflicts[slug] = conflict
                withheld[slug] = "routes-disagree-on-tier"
                outcome.update(status="withheld", reason="routes-disagree-on-tier")
            elif evidence:
                resolved[slug] = evidence
                outcome.update(status="resolved", reason=evidence.get("identity", {}).get(
                    "rule", evidence["route"]), evidence=evidence)
            else:
                withheld[slug] = reason
                outcome.update(status="withheld" if reason != "no-registry-match" else "no-match",
                               reason=reason)
            outcome["candidates"] = [
                {"registry": c["registry"], "excluded": True} if c.get("excluded") else
                {"registry": c["registry"], "package": c["canonical"],
                 "address": c["registry_obj"].address(c["canonical"], c["record"]),
                 "accept": c["verdict"].accept, "rule": c["verdict"].reason,
                 "corroboration": c["verdict"].corroboration,
                 "contradiction": c["verdict"].contradiction,
                 "licence_raw": c["reading"]["raw"], "licence": c["reading"]["license"],
                 "tier": c["reading"]["tier"]}
                for c in candidates]
            outcomes.append(outcome)
    except RegistryRefused as exc:
        raise SystemExit(f"stopped: {exc}") from exc

    (d / "tool_licenses.json").write_text(
        json.dumps(dict(sorted(resolved.items())), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    if report:
        pathlib.Path(report).write_text(json.dumps(outcomes, indent=1, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
    routes: dict[str, int] = {}
    tiers: dict[str, int] = {}
    for e in resolved.values():
        routes[e["route"]] = routes.get(e["route"], 0) + 1
        tiers[e["license_tier"]] = tiers.get(e["license_tier"], 0) + 1
    confirmations: dict[str, int] = {}
    for o in outcomes:
        if o.get("confirmation"):
            key = o["confirmation"].split(":")[0]
            confirmations[key] = confirmations.get(key, 0) + 1
    reasons: dict[str, int] = {}
    for r in withheld.values():
        key = r.split(":")[0] if not r.startswith("identity:") else r
        reasons[key] = reasons.get(key, 0) + 1
    return {"domain": domain, "life_science": life_science, "tools": len(tools),
            "resolved": sum(1 for e in resolved.values() if e["license_tier"] != "unknown"),
            "routes": dict(sorted(routes.items())), "tiers": dict(sorted(tiers.items())),
            "withheld": dict(sorted(reasons.items())),
            "confirmation": dict(sorted(confirmations.items())),
            "reviewed_exclusions": len(excluded),
            "conflicts": conflicts,
            "index_sizes": {r.id: r.bulk_size() for r in regs},
            "requests": fetcher.requests, "bytes": fetcher.bytes}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collection", required=True,
                    help="collection dir with tools_index.json, tools/ and skills_index.json")
    ap.add_argument("--cache", default=".cache/tool-registries",
                    help="where registry responses are memoised (default: .cache/tool-registries)")
    ap.add_argument("--domain", help="collection domain (default: from collection.yaml or the path)")
    ap.add_argument("--offline", action="store_true",
                    help="read the cache only; a name not in it is not looked up")
    ap.add_argument("--report", help="write every record's outcome and candidates to this JSON file")
    args = ap.parse_args(argv)
    summary = resolve(args.collection, args.cache, domain=args.domain, offline=args.offline,
                      report=args.report)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
