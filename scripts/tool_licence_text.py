"""Read a licence string declared by a package registry into SPDX and a tier.

Registries declare licences in several grammars: SPDX expressions (`MIT`,
`GPL-3.0-or-later OR BSD-2-Clause`), the R `DESCRIPTION` grammar
(`GPL (>= 2)`, `GPL-2 | GPL-3`, `MIT + file LICENSE`), PyPI trove classifiers
(`GNU General Public License v2 (GPLv2)`) and free text (`Apache 2.0`).

The reading follows three rules, each of which an earlier substring classifier
broke:

- A version is never invented. `GPLv2+` is `GPL-2.0-or-later`, `LGPL 2.1 or later`
  is `LGPL-2.1-or-later`. An explicit version without "or later" is recorded as
  `-only`, which is what SPDX's own deprecated ids (`GPL-2.0`) mean.
- An unversioned family name (`GPL`, `LGPL`, `AGPL`, `BSD`) yields a tier only
  when every member of the family has the same tier in
  governance/license_tiers.yaml, and the recorded licence is then the string the
  source wrote, never a guessed SPDX id.
- A non-commercial or no-derivatives licence never lands in `open`. A string
  that mentions non-commercial use and is not recognised stays unread.

Anything this module cannot read returns `tier=None`, which the resolver turns
into `unknown`. It never falls back to `restricted`: an unread string is not an
established licence.
"""
from __future__ import annotations

import re

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.license_tier import load_map

TIER_OPEN = "open"
TIER_NONCOMMERCIAL = "noncommercial"
TIER_RESTRICTED = "restricted"

# The R placeholder for a licence held in a file the registry does not serve.
FILE_REF = "LicenseRef-file-LICENSE"

# Families whose unversioned name still has one tier: every version of each is
# listed as `open` in governance/license_tiers.yaml (GPL-2.0 and GPL-3.0; LGPL-2.0,
# 2.1 and 3.0; AGPL-3.0; BSD-2-Clause and BSD-3-Clause). `Apache` and `Artistic`
# are absent on purpose: their 1.x versions are not in the tier map.
UNVERSIONED_FAMILIES = {"gpl": "GPL", "lgpl": "LGPL", "agpl": "AGPL", "bsd": "BSD"}

# Statements that are not a licence id but have one reading: the work is not
# under copyright, or R's "Unlimited" (no restriction on use).
NO_RESTRICTION_STATEMENTS = {"public domain": "Public Domain", "unlimited": "Unlimited",
                             "ncbi-pd": "NCBI-PD"}

_VERSIONS = {"gpl": {"1", "2", "3"}, "lgpl": {"2", "2.1", "3"}, "agpl": {"1", "3"}}

# Exact strings after cleaning (lower case, single spaces, no trailing "license").
# Only forms seen in Bioconductor, Bioconda, CRAN, PyPI and bio.tools, and only
# those with one reading.
_EXACT = {
    "mit": "MIT", "expat": "MIT", "mit/expat": "MIT", "mit (mit)": "MIT",
    "apache-2.0": "Apache-2.0", "apache 2.0": "Apache-2.0", "apache 2": "Apache-2.0",
    "apache-2": "Apache-2.0", "apache2": "Apache-2.0", "apache v2.0": "Apache-2.0",
    "apache v2": "Apache-2.0", "apache_2_0": "Apache-2.0", "apache 2.0 license": "Apache-2.0",
    "apache-2.0 license": "Apache-2.0", "apache software 2.0": "Apache-2.0",
    "apache software license 2.0": "Apache-2.0", "apache, version 2.0": "Apache-2.0",
    "apache version 2.0": "Apache-2.0", "apache (== 2.0)": "Apache-2.0", "apache (== 2)": "Apache-2.0",
    "apache (>= 2)": "Apache-2.0", "apache (>= 2.0)": "Apache-2.0",
    "apache software license (apache 2.0)": "Apache-2.0",
    "apache software license (apache-2.0)": "Apache-2.0",
    "bsd-3-clause": "BSD-3-Clause", "bsd 3-clause": "BSD-3-Clause", "bsd-3": "BSD-3-Clause",
    "bsd 3": "BSD-3-Clause", "bsd3": "BSD-3-Clause", "bsd_3_clause": "BSD-3-Clause",
    "bsd 3 clause": "BSD-3-Clause", "3-clause bsd": "BSD-3-Clause", "new bsd": "BSD-3-Clause",
    "modified bsd": "BSD-3-Clause", "revised bsd": "BSD-3-Clause", "bsd-3-clause license": "BSD-3-Clause",
    "bsd 3-clause license": "BSD-3-Clause", "bsd-3 clause": "BSD-3-Clause",
    "bsd-2-clause": "BSD-2-Clause", "bsd 2-clause": "BSD-2-Clause", "bsd-2": "BSD-2-Clause",
    "bsd2": "BSD-2-Clause", "bsd_2_clause": "BSD-2-Clause", "bsd 2 clause": "BSD-2-Clause",
    "2-clause bsd": "BSD-2-Clause", "simplified bsd": "BSD-2-Clause", "bsd 2-clause license": "BSD-2-Clause",
    "bsd-3-clause-clear": "BSD-3-Clause-Clear",
    "mpl-2.0": "MPL-2.0", "mpl 2.0": "MPL-2.0", "mozilla public license 2.0": "MPL-2.0",
    "mozilla public license 2.0 (mpl 2.0)": "MPL-2.0", "mozilla public 2.0": "MPL-2.0",
    "artistic-2.0": "Artistic-2.0", "artistic 2.0": "Artistic-2.0", "artistic_2": "Artistic-2.0",
    "artistic-2.0-only": "Artistic-2.0", "artistic license 2.0": "Artistic-2.0",
    "the artistic license, version 2.0": "Artistic-2.0", "artistic, version 2.0": "Artistic-2.0",
    "isc": "ISC", "isc license (iscl)": "ISC", "unlicense": "Unlicense", "the unlicense": "Unlicense",
    "the unlicense (unlicense)": "Unlicense", "zlib": "Zlib", "bsl-1.0": "BSL-1.0",
    "boost software license 1.0": "BSL-1.0", "epl-1.0": "EPL-1.0", "epl-2.0": "EPL-2.0",
    "eclipse public license 2.0": "EPL-2.0", "eclipse public license 1.0": "EPL-1.0",
    "afl-3.0": "AFL-3.0", "0bsd": "0BSD", "ncsa": "NCSA", "wtfpl": "WTFPL", "ms-pl": "MS-PL",
    "mulanpsl-2.0": "MulanPSL-2.0",
    "cc0": "CC0-1.0", "cc0-1.0": "CC0-1.0", "cc0 1.0": "CC0-1.0", "cc0 1.0 universal": "CC0-1.0",
    "cc0 1.0 universal (cc0 1.0) public domain dedication": "CC0-1.0",
    "perl_5": "Artistic-1.0-Perl OR GPL-1.0-or-later", "perl 5": "Artistic-1.0-Perl OR GPL-1.0-or-later",
    "artistic-1.0-perl": "Artistic-1.0-Perl", "psf-2.0": "PSF-2.0", "python-2.0": "Python-2.0",
}

# Creative Commons, written out or abbreviated. Group 1 is the clause list, group 2
# the version. Clauses decide the tier, so they are parsed rather than guessed.
_CC = re.compile(
    r"^(?:cc|creative commons)[\s\-_]*"
    r"((?:(?:attribution|by|non[\s\-]?commercial|nc|share[\s\-]?alike|sa|no[\s\-]?derivatives|"
    r"noderivs|nd|international|public)[\s\-_/]*)+)"
    r"(?:licen[cs]e[\s,]*)?(?:v(?:ersion)?\.?\s*)?(\d(?:\.\d)?)?(?:\s*international)?(?:\s*licen[cs]e)?$")

_NC_WORDS = re.compile(r"non[\s\-]?commercial|\bnc\b|academic|research use only|not for commercial", re.I)

_R_QUALIFIER = re.compile(r"\(\s*(>=|==|>)\s*v?(\d+(?:\.\d+)?)\s*\)")
_FAMILY = re.compile(
    r"^(agpl|lgpl|gpl)\s*(?:version\s*|ver\.?\s*|v\.?\s*|-)?\s*(\d(?:\.\d)?)?(?:\.0)?\s*"
    r"(\+|or later|or-later|-or-later|or any later version|or newer|or greater|-only|only)?$")


def _clean(text: str) -> str:
    """Lower case, single spaces, with the noise words that carry no meaning removed."""
    s = " ".join(str(text).replace("‐", "-").split()).strip().strip("'\"`").strip()
    s = s.lower()
    s = re.sub(r"^the\s+", "", s)
    for long, short in (("gnu affero general public", "agpl"), ("affero general public", "agpl"),
                        ("gnu library or lesser general public", "lgpl"),
                        ("library or lesser general public", "lgpl"),
                        ("gnu lesser general public", "lgpl"), ("lesser general public", "lgpl"),
                        ("gnu library general public", "lgpl"), ("library general public", "lgpl"),
                        ("gnu general public", "gpl"), ("general public", "gpl"),
                        ("gnu gpl", "gpl"), ("gnu lgpl", "lgpl"), ("gnu agpl", "agpl")):
        s = s.replace(long, short)
    s = re.sub(r"\s+licen[cs]e\b", "", s)
    s = re.sub(r"^licen[cs]e\s*:\s*", "", s)
    s = re.sub(r"\s+", " ", s).strip(" ,;.")
    return s


def _family_reading(s: str) -> str | None:
    """SPDX id, or an unversioned family marker `family:<name>`, for a GPL-family atom."""
    s = s.replace("gplv", "gpl v").replace("lgplv", "lgpl v").replace("agplv", "agpl v")
    # A redundant parenthetical repeating the family, as PyPI classifiers write it:
    # "gpl v2 (gplv2)". Kept only when it reads the same as the outside.
    paren = re.match(r"^(.*?)\s*\(([^()]*)\)$", s)
    if paren and not _R_QUALIFIER.search(s):
        outer, inner = _family_reading(paren.group(1)), _family_reading(paren.group(2))
        if outer and (inner is None or inner == outer or inner.startswith("family:")
                      and outer.split("-")[0].lower() == inner.split(":")[1].lower()):
            return outer
        if outer is None and inner and paren.group(1) in ("gpl", "lgpl", "agpl"):
            return inner
        return None
    qualifier = _R_QUALIFIER.search(s)
    later = False
    if qualifier:
        if qualifier.group(1) == ">":
            return None
        later = qualifier.group(1) == ">="
        s = _R_QUALIFIER.sub(" ", s).strip() + " " + qualifier.group(2)
        s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*>=\s*(\d)", r" \1+", s)
    m = _FAMILY.match(s.strip())
    if not m:
        return None
    family, version, suffix = m.group(1), m.group(2), (m.group(3) or "").strip()
    if not version:
        if later or suffix:
            return None
        return f"family:{UNVERSIONED_FAMILIES[family]}"
    version = version[:-2] if version.endswith(".0") else version
    if version not in _VERSIONS[family]:
        return None
    later = later or suffix in ("+", "or later", "or-later", "-or-later", "or any later version",
                                "or newer", "or greater")
    spdx_version = version if "." in version else version + ".0"
    return f"{family.upper()}-{spdx_version}-{'or-later' if later else 'only'}"


def _cc_reading(s: str) -> str | None:
    m = _CC.match(s)
    if not m:
        return None
    clauses = m.group(1)
    version = m.group(2)
    nc = bool(re.search(r"non[\s\-]?commercial|\bnc\b", clauses))
    nd = bool(re.search(r"no[\s\-]?derivatives|noderivs|\bnd\b", clauses))
    sa = bool(re.search(r"share[\s\-]?alike|\bsa\b", clauses))
    by = bool(re.search(r"attribution|\bby\b", clauses)) or nc or nd or sa
    if not by or not version:
        return None
    version = version if "." in version else version + ".0"
    parts = ["CC", "BY"] + (["NC"] if nc else []) + (["SA"] if sa else []) + (["ND"] if nd else [])
    return "-".join(parts) + "-" + version


def read_atom(text: str) -> str | None:
    """One licence term to an SPDX id, `family:<NAME>`, `statement:<text>`, or None."""
    s = _clean(text)
    if not s:
        return None
    if s in ("file license", "file licence", "file"):
        return FILE_REF
    if s in NO_RESTRICTION_STATEMENTS:
        return f"statement:{NO_RESTRICTION_STATEMENTS[s]}"
    if s in _EXACT:
        return _EXACT[s]
    known = {k.lower(): k for k in (load_map().get("spdx") or {})}
    if s in known and s not in UNVERSIONED_FAMILIES:
        return known[s]
    if s in UNVERSIONED_FAMILIES:
        return f"family:{UNVERSIONED_FAMILIES[s]}"
    if s in ("bsd license", "bsd licence", "bsd-style", "bsd style"):
        return "family:BSD"
    cc = _cc_reading(s)
    if cc:
        return cc
    # A trailing parenthetical that repeats the licence, as trove classifiers and
    # recipe authors write it: "Mozilla Public License 2.0 (MPL 2.0)".
    paren = re.match(r"^(.*?)\s*\(([^()]*)\)$", s)
    if paren and not _R_QUALIFIER.search(s) and not re.match(r"^(a?l?gpl)", s):
        outer, inner = read_atom(paren.group(1)), read_atom(paren.group(2))
        if outer and outer == inner:
            return outer
    deprecated = re.match(r"^(a?l?gpl)-(\d\.\d)(\+)?$", s)
    if deprecated:
        family, version, plus = deprecated.groups()
        if version.rstrip("0").rstrip(".") in _VERSIONS[family] or version in _VERSIONS[family]:
            return f"{family.upper()}-{version}-{'or-later' if plus else 'only'}"
    spdx_versioned = re.match(r"^(a?l?gpl)-(\d\.\d)-(only|or-later)$", s)
    if spdx_versioned:
        return f"{spdx_versioned.group(1).upper()}-{spdx_versioned.group(2)}-{spdx_versioned.group(3)}"
    if re.match(r"^(a?l?gpl)", s):
        family = _family_reading(s)
        if family:
            return family
    return None


def atom_tier(atom: str | None, _map=None) -> str | None:
    """Tier of one read atom, or None when the tier map does not settle it."""
    if not atom or atom == FILE_REF:
        return None
    if atom.startswith("statement:"):
        return TIER_OPEN
    if atom.startswith("family:"):
        # Every member of these families is `open` in the tier map; see
        # UNVERSIONED_FAMILIES. Checked here so that a change to the map breaks a test.
        return TIER_OPEN
    m = _map or load_map()
    table = {k.lower(): v for k, v in (m.get("spdx") or {}).items()}
    key = atom.lower()
    if key in table:
        return table[key]
    base = re.sub(r"-(only|or-later)$", "", key)
    for candidate in (base, base + "-only", base + "-or-later"):
        if candidate in table:
            return table[candidate]
    # An "or later" grant of any GNU licence lets the user take the latest version,
    # which the tier map lists as open.
    if re.match(r"^(a?l?gpl)-\d\.\d-or-later$", key):
        return TIER_OPEN
    if key.startswith("cc-by-nc"):
        return TIER_NONCOMMERCIAL
    if key.startswith("cc-by-nd"):
        return TIER_RESTRICTED
    return None


_ORDER_AND = {TIER_OPEN: 0, TIER_RESTRICTED: 1, TIER_NONCOMMERCIAL: 2}


def _split(text: str, license_format: str) -> tuple[str, list[str]]:
    """('OR'|'AND'|'ONE', parts). R alternatives are `|`; SPDX uses OR and AND."""
    t = str(text).strip()
    while t.startswith("(") and t.endswith(")") and t.count("(") == 1:
        t = t[1:-1].strip()
    if "|" in t:
        return "OR", [p for p in t.split("|") if p.strip()]
    if re.search(r"\s+OR\s+", t):
        if re.search(r"\s+AND\s+", t):
            return "MIXED", [t]
        return "OR", re.split(r"\s+OR\s+", t)
    if re.search(r"\s+AND\s+", t):
        return "AND", re.split(r"\s+AND\s+", t)
    return "ONE", [t]


_R_FILE = re.compile(r"\s*\+\s*file\s+licen[cs]e\s*$", re.I)


def _read_part(part: str) -> tuple[str | None, str | None]:
    """(atom, note) for one alternative, applying the R `+ file LICENSE` rule."""
    p = part.strip()
    p = re.sub(r"\s+WITH\s+[\w.\-]+$", "", p)
    if _R_FILE.search(p):
        base = read_atom(_R_FILE.sub("", p))
        # R requires `+ file LICENSE` for MIT and the BSD templates, where the file
        # only names the copyright holder. For the GNU licences it may add only
        # the terms those licences permit (attribution). Anywhere else the file
        # may carry any restriction, so the part is unread.
        if base in ("MIT", "BSD-2-Clause", "BSD-3-Clause") or (
                base and (base.startswith(("GPL-", "LGPL-", "AGPL-")) or base in (
                    "family:GPL", "family:LGPL", "family:AGPL"))):
            return base, "file-LICENSE-template"
        return None, "file-LICENSE-may-restrict"
    return read_atom(p), None


def read_licence(raw, license_format: str = "spdx_or_text", _map=None) -> dict:
    """Read a registry licence string.

    Returns ``{raw, license, tier, reason}``. ``license`` is what a record should
    show: an SPDX expression, or the source's own words for an unversioned family
    or a no-restriction statement. ``tier`` is None when the string is not read,
    and ``reason`` says why.
    """
    out = {"raw": raw, "license": None, "tier": None, "reason": None}
    if raw is None or not str(raw).strip():
        out["reason"] = "empty"
        return out
    text = " ".join(str(raw).split())
    if len(text) > 200:
        out["reason"] = "free-text"
        return out
    # A name that stands for a compound licence, such as Perl's.
    expanded = _EXACT.get(_clean(text))
    op, parts = _split(expanded if expanded and " OR " in expanded else text, license_format)
    if op == "MIXED":
        out["reason"] = "mixed-operators"
        return out
    atoms = [_read_part(p) for p in parts]
    tiers = [atom_tier(a, _map) for a, _ in atoms]
    # A part that speaks of non-commercial use must read as non-commercial, or not
    # at all: an unrecognised academic-only clause must never surface as open.
    for (atom, _), tier, part in zip(atoms, tiers, parts):
        if _NC_WORDS.search(part) and tier not in (None, TIER_NONCOMMERCIAL):
            out["reason"] = "non-commercial-wording"
            return out
    if op in ("ONE", "AND"):
        if any(t is None for t in tiers):
            out["reason"] = "unread"
            return out
        tier = max(tiers, key=lambda t: _ORDER_AND[t])
    else:
        read = [t for t in tiers if t is not None]
        if TIER_OPEN in read:
            tier = TIER_OPEN
        elif read and len(read) == len(tiers):
            tier = min(read, key=lambda t: _ORDER_AND[t])
        else:
            out["reason"] = "unread"
            return out
    shown = [_display(a, p) for (a, _), p in zip(atoms, parts)]
    joiner = " OR " if op == "OR" else " AND "
    families = any(a and (a.startswith("family:") or a.startswith("statement:")) for a, _ in atoms)
    if families and op == "ONE":
        # Record the source's own words for an unversioned family: a guessed
        # SPDX id would invent a version the source never stated.
        out["license"] = _R_FILE.sub("", text).strip() if license_format == "r_description_field" else text
    else:
        out["license"] = joiner.join(shown)
    out["tier"] = tier
    out["reason"] = "read"
    return out


def _display(atom: str | None, part: str) -> str:
    if atom is None:
        return FILE_REF if re.search(r"file\s+licen[cs]e", part, re.I) else "LicenseRef-unread"
    if atom.startswith("family:") or atom.startswith("statement:"):
        return atom.split(":", 1)[1]
    return atom
