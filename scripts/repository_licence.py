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
README_FILES = ("README.md", "README.rst", "README", "README.txt")
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


# A permissive licence file that adds terms of its own is not that licence (bmxp:
# "MIT License (Dual License)", free for academic and non-profit use, a separate
# commercial licence for redistribution). The added terms are looked for only
# outside the licence's canonical wording, because the canonical texts of some
# families use the same words (the Unlicense: "commercial or non-commercial").
# The canonical spans below are removed from the normalised text; what remains is
# the heading, the added clauses and any trailing notes. Copyright lines are
# dropped first, so a holder named "Academic Medical Center" is not a term.
_MIT_GRANT = re.compile(r"permission is hereby granted, free of charge, to any person obtaining a copy")
_CANONICAL = {
    "MIT": [r"permission is hereby granted, free of charge, to any person obtaining a copy of this "
            r"software.{0,800}?subject to the following conditions:?",
            r"the above copyright notice and this permission notice shall be included in all "
            r"copies or substantial portions of the software\.?",
            r"the software is provided \"?as is\"?,? without warranty of any kind.{0,1500}?"
            r"(?:other dealings in the software|use or other dealings)\.?"],
    "BSD": [r"redistribution and use in source and binary forms, with or without modification, "
            r"are permitted provided that the following conditions are met:?",
            r"redistributions of source code must retain [^.]*\.",
            r"redistributions in binary form must reproduce [^.]*\.",
            r"neither the name [^.]*\.",
            r"the names? of [^.]{0,200}(?:may|must) not be used to endorse [^.]*\.",
            r"this software is provided by .{0,300}?\"?as is\"?.{0,2000}?possibility of such damage\.?"],
    "Apache": [r"apache license,? version 2\.0.{0,20000}?end of terms and conditions",
               r"appendix: how to apply the apache license.{0,2000}?limitations under the license\.?",
               r"licensed under the apache license,? version 2\.0.{0,1000}?limitations under the "
               r"license\.?"],
    "Unlicense": [r"this is free and unencumbered software released into the public domain"
                  r".{0,4000}?(?:unlicense\.org/?>?|$)"],
}
_ADDED_TERMS = re.compile(
    r"dual[- ]licen|non-?commercial|academic|non-?profit|commercial licen|commercial use|"
    r"commercial purposes|research purposes|educational purposes|industrial|permission of|"
    r"contact us")
# Plain words that commercial use is excluded or needs a separate licence.
_COMMERCIAL_EXCLUDED = re.compile(
    r"separate commercial licen|commercial licen[cs]e (?:is |must be )?(?:required|needed|obtained)"
    r"|(?:commercial (?:use|purposes|users?|redistribution)|redistribution)[^.]{0,80}"
    r"(?:requires?|requiring|needs?|must obtain)[^.]{0,40}licen"
    r"|commercial (?:use|purposes)[^.]{0,40}(?:not (?:permitted|allowed)|prohibited|excluded)")


def _permissive_family(t: str, distinct: list[str]) -> str | None:
    """The permissive family whose added terms must be checked, or None."""
    if len(distinct) > 1:
        return None
    lic = distinct[0] if distinct else None
    if lic == "MIT" or (lic is None and _MIT_GRANT.search(t)):
        return "MIT"
    if lic is None and _BSD.search(t):
        return "BSD"
    if lic and lic.startswith("BSD-"):
        return "BSD"
    if lic in ("Apache-2.0", "Unlicense", "CC0-1.0"):
        return lic.split("-")[0]
    return None


def added_terms(text: str, family: str) -> str | None:
    """The text outside a permissive licence's canonical wording, when it adds terms."""
    kept = "\n".join(line for line in (text or "").splitlines()
                     if not re.match(r"^\W*(?:copyright\b|\(c\)|\u00a9)", line.strip(), re.I))
    t = _norm(kept)
    if family == "CC0":
        # A Creative Commons text uses these words itself; only a heading above it counts.
        title = re.search(r"creative commons legal code|cc0 1\.0 universal", t)
        outside = t[:title.start()] if title else ""
    else:
        outside = t
        for pattern in _CANONICAL[family]:
            outside = re.sub(pattern, " ", outside)
    outside = " ".join(outside.split())
    return outside if _ADDED_TERMS.search(outside) else None


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
    family = _permissive_family(t, distinct)
    if family:
        extra = added_terms(text, family)
        if extra:
            if _COMMERCIAL_EXCLUDED.search(extra) or _NONCOMMERCIAL.search(extra):
                return {"license": NONCOMMERCIAL_FILE, "tier": "noncommercial",
                        "reason": "permissive-with-noncommercial-terms"}
            return {"license": None, "tier": None, "reason": "permissive-with-added-terms"}
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


def unversioned_family(file_licence) -> str | None:
    """`GPL`, `LGPL`, `AGPL` or `BSD` when the repository names the family alone."""
    keys = _keys(file_licence)
    if len(keys) != 1:
        return None
    key = next(iter(keys))
    return key.split(":", 1)[1] if key.startswith("family:") else None


def gnu_family(registry_licence, file_licence) -> str | None:
    """`GPL`, `LGPL` or `AGPL` when both are that GNU family and differ only in version."""
    reg, rep = _keys(registry_licence), _keys(file_licence)
    if len(reg) != 1 or len(rep) != 1:
        return None
    a, b = next(iter(reg)), next(iter(rep))
    if a == b or a.startswith("family:") or b.startswith("family:"):
        return None
    fa, fb = a.split("-")[0], b.split("-")[0]
    return fa if fa == fb and fa in ("GPL", "LGPL", "AGPL") else None


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


def _raw_base(repo_url) -> str | None:
    urls = raw_urls(repo_url)
    return urls[0][1].rsplit("/", 1)[0] + "/" if urls else None


def _get_text(fetcher, url) -> str | None:
    key = "repofile-" + re.sub(r"[^A-Za-z0-9.]+", "_", url.split("://", 1)[1])
    data = fetcher.get(url, key, MAX_FILE_BYTES, paced=True)
    return None if data is None else data.decode("utf-8", "replace")


def repository_name(repo_url) -> str | None:
    """The repository part of a GitHub or GitLab address."""
    m = re.match(r"^(?:https?://)?(?:www\.)?(?:github\.com|gitlab\.com)/[^/\s]+/([^/\s#?]+?)"
                 r"(?:\.git)?/?$", str(repo_url or "").strip())
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# The README                                                                  #
# --------------------------------------------------------------------------- #

# A sentence that restricts use of the tool itself. The patterns are about use or
# licensing, never a bare "commercial": "free for academic and educational
# purposes", "academic use only", "commercial use requires a licence", "a license
# is needed", "for research purposes only", an industrial licence.
_KIND = r"(?:academic|non-?commercial|research|educational|education|non-?profit|scientific)"
# Kinds joined by a conjunction or written together ("academic research and
# training"). Training and teaching count only after another kind: "only for
# training" in a README about a neural network names a model's training step.
_KINDS = _KIND + r"(?:(?:(?:,| and| or| &|/) ?| )(?:" + _KIND[3:-1] + r"|training|teaching))*"
_README_RESTRICTION = re.compile(
    r"free (?:of charge )?for (?:all |any )?" + _KINDS + r" (?:use|users|purposes|institutions)"
    r"|\b" + _KINDS + r" (?:use|purposes) only"
    r"|(?:only|solely|exclusively) (?:for|to) " + _KINDS + r"(?: (?:use|users|purposes))?"
    r"|restricted to " + _KINDS + r"(?: (?:use|users|purposes|institutions))?"
    r"|\bfor " + _KINDS + r" only\b"
    r"|not (?:be )?(?:for|used for|intended for) (?:any )?commercial (?:use|purposes)"
    r"|commercial use is (?:not permitted|prohibited|forbidden|not allowed)"
    r"|commercial (?:use|users?|purposes|applications?|entities|companies)[^.]{0,80}"
    r"(?:requires?|need|must (?:obtain|contact|purchase)|contact us|licen[cs]e is)"
    r"|(?:a|separate|commercial) licen[cs]e (?:is|must be|needs to be|has to be) "
    r"(?:needed|required|obtained)"
    r"|for research purposes only"
    r"|industrial[^.]{0,100}licen[cs]e")
# A sentence about something the tool depends on, not the tool. Such sentences are
# skipped: "Note that NetMHCpan, a dependency, is free for academic use only".
_ABOUT_ANOTHER = re.compile(
    r"dependenc|third[- ]party|depends on|is required (?:to run|by)|"
    r"you (?:will )?(?:also )?need to (?:download|install|obtain|register)|"
    r"(?:must|should|needs? to) be (?:downloaded|installed|obtained) separately|"
    r"(?:its|their) own licen|licen[cs]ed by (?:its|their)")


# A sentence that says the tool itself, or its binary, is closed or carries further
# restrictions. It withholds even when the cause is a dependency (MZA: "the software
# binary depends on other software libraries which place further restrictions on
# its use and redistribution"); only a sentence that calls the dependency optional
# is skipped.
_TOOL_RESTRICTED = re.compile(
    r"closed[- ]source (?:code|binar)"
    r"|(?:this|the|its|our) (?:software|tool|program|binar(?:y|ies)|package|code|executable)s? "
    r"(?:is|are) (?:proprietary|closed[- ]source)"
    r"|under a proprietary licen"
    r"|(?:further|additional) restrictions on (?:its|their|the) (?:use|redistribution)"
    r"|agree to comply with the (?:restrictions|licen[cs]e agreements)")
# The same words in a comparison describe other software ("an open alternative to
# closed-source software").
_COMPARISON = re.compile(r"alternative to|replacement for|unlike|instead of|compared (?:to|with)"
                         r"|replac(?:e|es|ing) ")


# A licence term that limits the field of use of the software itself: dsb's
# alternative terms, "THE SOFTWARE SHALL NOT BE USED IN THE TREATMENT OR DIAGNOSIS
# OF HUMAN SUBJECTS". A second licence for a bundled component (xcms) holds no
# such sentence and is not read as one.
_FIELD_OF_USE = re.compile(
    r"shall not be used (?:in|for)\b"
    r"|(?:must|may|shall|can) not be used (?:in|for) (?:the )?(?:treatment|diagnos|clinical|"
    r"medical|commercial|patient)")


def field_of_use(text: str) -> str | None:
    """The first sentence of a licence file that limits the use of the software itself.

    A GNU or Apache text speaks of non-commercial distribution in its own terms
    (GPL-2.0, section 3c), so in such a file only an explicit field-of-use sentence
    counts.
    """
    standard = bool(_GNU_HEADING.search(text or "") or _APACHE.search(_norm(text or "")))
    for sentence in readme_sentences(text):
        low = sentence.lower()
        if _FIELD_OF_USE.search(low) or not standard and (_NONCOMMERCIAL.search(low) or (
                _README_RESTRICTION.search(low) and not _ABOUT_ANOTHER.search(low))):
            return sentence[:300]
    return None


def repository_licence_text(repo_url, fetcher) -> dict | None:
    """``{file, text}`` for the first licence file the repository serves, or None."""
    for name, url in raw_urls(repo_url)[:-1]:
        text = _get_text(fetcher, url)
        if text is not None:
            return {"file": url, "text": text}
    return None


def readme_sentences(text: str) -> list[str]:
    """The README's sentences, with code blocks and markup removed."""
    text = re.sub(r"```.*?```", " ", text or "", flags=re.S)
    text = re.sub(r"<[^>]{1,200}>|\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)|!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    parts = re.split(r"(?<=[.!?])\s+|\n\s*\n|\n\s*(?:[-*+]|\d+[.)])\s+|\n\s*#+\s*", text)
    return [" ".join(re.sub(r"[#*>`_|]+", " ", p).split()) for p in parts if p.strip()]


def readme_restriction(text: str) -> str | None:
    """The first README sentence that restricts use of the tool itself, or None."""
    sentences = readme_sentences(text)
    for i, sentence in enumerate(sentences):
        low = sentence.lower().replace("\u2019", "'")
        if _TOOL_RESTRICTED.search(low) and not _COMPARISON.search(low) and not re.search(
                r"\boptional", low):
            return sentence[:300]
        if not _README_RESTRICTION.search(low) or _ABOUT_ANOTHER.search(low):
            continue
        # "For research use only. Not for use in diagnostic procedures." is a
        # regulatory disclaimer about clinical use, not a licence term.
        near = " ".join(sentences[i:i + 2]).lower()
        if re.search(r"research use only", low) and re.search(r"diagnos|clinical", near):
            continue
        return sentence[:300]
    return None


def repository_readme(repo_url, fetcher) -> dict | None:
    """``{file, sentence}`` for the first README present, or None when there is none."""
    base = _raw_base(repo_url)
    if not base:
        return None
    for name in README_FILES:
        url = base + urllib.parse.quote(name)
        text = _get_text(fetcher, url)
        if text is not None:
            return {"file": url, "sentence": readme_restriction(text)}
    return None


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
        return _get_text(fetcher, url)

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
