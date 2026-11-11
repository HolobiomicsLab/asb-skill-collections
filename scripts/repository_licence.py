"""Confirm a registry's licence against the tool repository's own licence statement.

Bioconductor, CRAN and PyPI metadata are written by the package authors. A
Bioconda recipe and a bio.tools entry are written by someone else, and their
licence strings are often not the tool's: bio.tools still lists bedtools as
GPL-2.0 and MUON as GPL-3.0 (both repositories say otherwise), and Bioconda lists
STAR and Kraken2 as GPL-3.0-or-later while both repositories carry an MIT licence.
A tool's licence may only come from the tool (governance/LICENSE_TIERS.md), so a
registry resolution with a repository on a code host is checked against the
licence file that repository serves.

The file is fetched anonymously as raw content (raw.githubusercontent.com, or
gitlab.com's raw path), never through an API. The classifier is conservative: it
recognises a licence only from its canonical title or grant wording, and a file
it cannot read, or one that holds more than one licence, is unread.

A licence file alone cannot say whether a GNU licence is "only" or "or later":
the text of the licence is the same. The reading then carries the version and no
suffix (`GPL-3.0`), as the reviewed map writes it, unless the file also holds the
notice "either version N of the License, or (at your option) any later version".
"""
from __future__ import annotations

import re
import urllib.parse

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.tool_licence_text import atom_tier, read_licence
from scripts.tool_registry_sources import normalize

DETECTION_REPOSITORY_FILE = "repository-licence-file"
LICENCE_FILES = ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING", "COPYING.txt",
                 "LICENCE", "LICENCE.txt")
MAX_FILE_BYTES = 400_000

NONCOMMERCIAL_FILE = "LicenseRef-repository-noncommercial"


def _norm(text: str) -> str:
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(re.sub(r"[#*>`_=|]+", " ", text).lower().split())


# A GNU licence is recognised only from its heading, "GNU GENERAL PUBLIC LICENSE"
# with "Version N" on the same or the next line, never from a sentence in the
# body: the LGPL-2.1 text itself speaks of "the ordinary GNU General Public
# License, version 2".
_GNU_HEADING = re.compile(
    r"^[\s#*_>]*GNU\s+(AFFERO\s+|LESSER\s+|LIBRARY\s+)?GENERAL\s+PUBLIC\s+LICEN[CS]E[\s#*_>,]*"
    r"\n?[\s#*_>]*Version\s+(\d(?:\.\d)?)", re.I | re.M)
_GNU_FAMILY = {"affero": "AGPL", "lesser": "LGPL", "library": "LGPL", "": "GPL"}
# The "or any later version" notice counts only outside the licence's own
# appendix, "How to Apply These Terms", which prints it as a template.
_LATER = re.compile(r"either version (\d(?:\.\d)?) of the license, or \(at your option\) any later version")
_APPENDIX = re.compile(r"how to apply these terms to your new (?:programs|libraries)")
_SPDX_LINE = re.compile(r"SPDX-License-Identifier:\s*([^\n`]+)")
_MIT = re.compile(r"permission is hereby granted, free of charge, to any person obtaining a copy "
                  r"of this software.{0,400}the above copyright notice and this permission notice "
                  r"shall be included")
_BSD = re.compile(r"redistribution and use in source and binary forms, with or without "
                  r"modification, are permitted provided that the following conditions are met")
_APACHE = re.compile(r"apache license,? version 2\.0")
_MPL = re.compile(r"mozilla public license,? (?:version|v\.?) ?2\.0")
_ARTISTIC = re.compile(r"the artistic license 2\.0")
_CC0 = re.compile(r"cc0 1\.0 universal")
_UNLICENSE = re.compile(r"this is free and unencumbered software released into the public domain")
_CC = re.compile(r"(?:creative commons )?attribution(-noncommercial)?(-sharealike|-noderivatives|"
                 r"-noderivs)? (\d\.\d) international")
_DUAL = re.compile(r"dual[- ]licen[cs]ed|licen[cs]ed under (?:either|both)|"
                   r"(?:under|by) (?:the terms of )?either (?:the )?[a-z0-9 .-]{2,60} or (?:the )?"
                   r"|at your (?:choice|choosing)|you may (?:choose|elect)")
_NONCOMMERCIAL = re.compile(
    r"(?:for|only for|solely for|limited to) (?:academic|non-?commercial|research)(?: and "
    r"(?:academic|non-?commercial|research))*(?: research)? (?:use|purposes)(?: only)?"
    r"|non-?commercial (?:use|purposes) only|not for commercial use|commercial use is "
    r"(?:not permitted|prohibited|forbidden)|may not be used for (?:any )?commercial purposes")


def classify_file(text: str) -> dict:
    """``{license, tier, reason}`` for a licence file's text; ``tier`` None when unread."""
    t = _norm(text or "")
    if not t:
        return {"license": None, "tier": None, "reason": "empty"}
    spdx = _SPDX_LINE.search(text or "")
    if spdx:
        # The file states its licence as an SPDX expression; read it as written.
        reading = read_licence(" ".join(spdx.group(1).split()))
        if reading["tier"]:
            return {"license": reading["license"], "tier": reading["tier"], "reason": "read"}
    found = []
    for m in _GNU_HEADING.finditer(text or ""):
        family = _GNU_FAMILY[(m.group(1) or "").strip().lower()]
        version = m.group(2)
        version = version if "." in version else version + ".0"
        found.append(f"{family}-{version}")
    if _APACHE.search(t):
        found.append("Apache-2.0")
    if _MPL.search(t):
        found.append("MPL-2.0")
    if _ARTISTIC.search(t):
        found.append("Artistic-2.0")
    if _CC0.search(t):
        found.append("CC0-1.0")
    if _UNLICENSE.search(t):
        found.append("Unlicense")
    if _MIT.search(t):
        found.append("MIT")
    bsd = _BSD.search(t)
    if bsd:
        tail = t[bsd.end():bsd.end() + 2500]
        clauses = sum(bool(re.search(p, tail)) for p in (
            r"redistributions of source code must retain",
            r"redistributions in binary form must reproduce",
            r"(?:neither the name|the names? of .{0,120}(?:may|must) not be used to endorse)"))
        if re.search(r"all advertising materials", tail):
            return {"license": None, "tier": None, "reason": "bsd-advertising-clause"}
        if clauses in (2, 3) and re.search(r"redistributions of source code must retain", tail):
            found.append("BSD-3-Clause" if clauses == 3 else "BSD-2-Clause")
        else:
            return {"license": None, "tier": None, "reason": "bsd-clauses-unclear"}
    cc = _CC.search(t)
    if cc:
        parts = ["CC", "BY"] + (["NC"] if cc.group(1) else []) + (
            ["SA"] if cc.group(2) == "-sharealike" else ["ND"] if cc.group(2) else [])
        found.append("-".join(parts) + "-" + cc.group(3))
    distinct = sorted(set(found))
    if len(distinct) == 2 and _DUAL.search(t) and not any(
            d.startswith("CC-BY-NC") for d in distinct):
        # A file that offers a choice in plain words ("dual licensed under ... or ...").
        tiers = [atom_tier(d) for d in distinct]
        if all(tiers):
            return {"license": " OR ".join(distinct),
                    "tier": "open" if "open" in tiers else tiers[0], "reason": "read"}
    if _NONCOMMERCIAL.search(t) and not any(d.startswith("CC-BY-NC") for d in distinct):
        if distinct:
            return {"license": None, "tier": None, "reason": "several-licences"}
        return {"license": NONCOMMERCIAL_FILE, "tier": "noncommercial",
                "reason": "noncommercial-wording"}
    if len(distinct) != 1:
        return {"license": None, "tier": None,
                "reason": "several-licences" if distinct else "unrecognised"}
    licence = distinct[0]
    family = licence.split("-")[0]
    if family in ("GPL", "LGPL", "AGPL"):
        appendix = _APPENDIX.search(t)
        later = _LATER.search(t[:appendix.start()] if appendix else t)
        if later and (later.group(1).split(".")[0] == licence.split("-")[1].split(".")[0]):
            licence = f"{licence}-or-later"
    tier = atom_tier(licence)
    if tier is None:
        return {"license": None, "tier": None, "reason": "not-in-tier-map"}
    return {"license": licence, "tier": tier, "reason": "read"}


def classify_description(text: str) -> dict:
    """The `License:` field of an R DESCRIPTION file, read with the R grammar."""
    m = re.search(r"^License:\s*(.+(?:\n[ \t]+.+)*)", text or "", re.M)
    if not m:
        return {"license": None, "tier": None, "reason": "no-license-field"}
    reading = read_licence(" ".join(m.group(1).split()), "r_description_field")
    return {"license": reading["license"], "tier": reading["tier"], "reason": reading["reason"]}


# --------------------------------------------------------------------------- #
# Comparison                                                                  #
# --------------------------------------------------------------------------- #

def _keys(expression) -> set[str]:
    """Family-and-version keys of an expression's parts: `GPL-3.0-or-later` is `GPL-3`."""
    out = set()
    for part in re.split(r"\s+(?:OR|AND)\s+", str(expression or "")):
        p = part.strip()
        while p.startswith("(") and p.endswith(")") and p.count("(") == 1:
            p = p[1:-1].strip()
        reading = read_licence(p)
        lic = reading["license"] or p
        if reading["tier"] is None and not reading["license"]:
            continue
        m = re.match(r"^(A?L?GPL)-(\d(?:\.\d)?)", lic)
        if m:
            version = m.group(2)
            version = version[:-2] if version.endswith(".0") else version
            out.add(f"{m.group(1)}-{version}")
            continue
        low = normalize(lic)
        family = {"gpl": "GPL", "lgpl": "LGPL", "agpl": "AGPL", "bsd": "BSD", "bsdlicense": "BSD",
                  "gnugeneralpubliclicensegpl": "GPL"}.get(low)
        out.add(f"family:{family}" if family else lic)
    return out


def agrees(registry_licence, file_licence) -> bool:
    """Whether a registry's licence and the repository's agree in family and version.

    `GPL-3.0-or-later` agrees with a file read as `GPL-3.0`; an unversioned `GPL`
    agrees with any GPL file; `BSD` agrees with BSD-2-Clause or BSD-3-Clause.
    """
    reg, rep = _keys(registry_licence), _keys(file_licence)
    if reg & rep:
        return True
    for one, other in ((reg, rep), (rep, reg)):
        for r in one:
            if r.startswith("family:"):
                family = r.split(":", 1)[1]
                if any(x == r or x.startswith(family + "-") for x in other):
                    return True
    return False


# --------------------------------------------------------------------------- #
# Fetching                                                                    #
# --------------------------------------------------------------------------- #

def raw_urls(repo_url) -> list[tuple[str, str]]:
    """``[(file name, raw URL)]`` for a repository on GitHub or GitLab, else []."""
    m = re.match(r"^(?:https?://)?(?:www\.)?(github\.com|gitlab\.com)/([^/\s]+)/([^/\s#?]+?)"
                 r"(?:\.git)?/?$", str(repo_url or "").strip())
    if not m:
        return []
    host, owner, repo = m.groups()
    names = list(LICENCE_FILES) + ["DESCRIPTION"]
    if host == "github.com":
        base = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/"
    else:
        base = f"https://gitlab.com/{owner}/{repo}/-/raw/HEAD/"
    return [(n, base + urllib.parse.quote(n)) for n in names]


def repository_statement(repo_url, fetcher, description_only=False) -> dict | None:
    """``{license, tier, reason, file}`` from the repository, or None when nothing was found.

    Licence files are tried in order and the first one present is classified.
    When none is present, or it cannot be read (an R package's LICENSE holds only
    the year and the copyright holder), the DESCRIPTION file's `License:` field is
    read instead.
    """
    urls = raw_urls(repo_url)
    if not urls:
        return None

    def get(url):
        key = "repofile-" + re.sub(r"[^A-Za-z0-9.]+", "_", url.split("://", 1)[1])
        data = fetcher.get(url, key, MAX_FILE_BYTES, paced=True)
        return None if data is None else data.decode("utf-8", "replace")

    found = None
    for name, url in ([] if description_only else urls[:-1]):
        text = get(url)
        if text is not None:
            found = dict(classify_file(text), file=url)
            break
    if found and found["tier"]:
        return found
    text = get(urls[-1][1])
    if text is not None:
        described = dict(classify_description(text), file=urls[-1][1])
        if described["tier"] or not found:
            return described
    return found
