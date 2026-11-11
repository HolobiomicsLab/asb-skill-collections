"""Decide whether a registry package is the tool a record names.

An exact name match is not identity. The same name denotes a dimension-reduction
method and a genome mappability package, a language model and a Bioconductor
package, a particle-physics code and a microbial one. Identity is therefore
judged per record, in its collection, from the record's own evidence:

- the record's evidence spans, the version it quotes, and the titles of the
  papers it was extracted from (`local text`);
- the repositories and DOIs it carries;
- the names and descriptions of the skills that cite it (`skill text`).

Three kinds of corroboration are read from that evidence (`corroboration`):

- `repository`  a repository or homepage the package declares is one the record
                names (its `source_repos`, or a URL in its spans);
- `publication` a DOI the registry lists for the tool is one of the record's;
- `code`        the record uses the name as a package of the registry's own
                ecosystem: `library(x)`, `x::f`, `BiocManager::install("x")`,
                `R package x` for R; `import x`, `pip install x`, `Python package x`
                for Python; `conda install x` for conda.

and two weaker signals:

- `domain`      the vocabulary of the record's local text overlaps the package
                description (binary cosine over identity-free tokens, at the
                threshold measured in docs/design/registry-match-corroboration-2026-11-07.md);
- the collection's domain: a curated life-science registry carries the domain
  constraint only for a life-science collection.

The rule, as `judge()` applies it, is stated in governance/LICENSE_TIERS.md.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.corroborate_registry_match import STOPWORDS, domain_signal
from scripts.repository_licence import readme_restriction
from scripts.tool_registry_sources import normalize

# Selected on the labelled set of 94 Bioconductor and Bioconda matches; see
# docs/design/registry-match-corroboration-2026-11-07.md. The `corroborated`
# verdict had precision 1.0 on both splits at this threshold.
DOMAIN_THRESHOLD = 0.021713

# Names this short collide across registries too often for a name match plus
# silence to count as identity: `bart`, `grid`, `mist` and `umap` are all four.
SHORT_NAME_LENGTH = 4

_CODE_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org", "sourceforge.net")
# Hosts whose root or package pages say nothing about which project is meant.
_GENERIC_HOSTS = ("bioconductor.org", "cran.r-project.org", "pypi.org", "anaconda.org",
                  "bioconda.github.io", "doi.org", "dx.doi.org", "zenodo.org", "r-project.org",
                  "python.org", "readthedocs.io", "github.io")
_URL = re.compile(r"https?://[^\s)\]>'\"`,;]+", re.I)


def repo_key(url) -> str | None:
    """Comparable key for a repository or homepage URL, or None when it identifies nothing.

    Code hosts compare on owner and repository; other hosts on host and path,
    and a bare host is not a key (`https://www.bioconductor.org` names no tool).
    """
    text = str(url or "").strip().strip("\"'<>[](),;").rstrip("/.")
    text = re.sub(r"^git\+", "", text)
    m = re.match(r"^(?:https?://)?(?:www\.)?([^/\s,;]+)(/[^?#\s,;]*)?", text, re.I)
    if not m:
        return None
    host, path = m.group(1).lower(), (m.group(2) or "").rstrip("/")
    if host in _CODE_HOSTS:
        parts = [p for p in path.split("/") if p]
        if len(parts) < 2:
            return None
        repo = re.sub(r"\.git$", "", parts[1].lower())
        return f"{host}/{parts[0].lower()}/{repo}"
    if any(host == g or host.endswith("." + g) for g in _GENERIC_HOSTS) or not path:
        return None
    return f"{host}{path.lower()}"


def _name_pattern(names) -> str:
    """Alternation of the names, bounded so `scan` does not match inside `scanpy`."""
    # Separators are interchangeable (`memory_profiler` is PyPI's `memory-profiler`),
    # but a separator is never invented or dropped: `py-graphviz` is not `pygraphviz`.
    escaped = sorted({re.sub(r"\\\s+|\\ ", r"[\\s_-]?",
                             re.sub(r"\\[-.]|_", "[-_.]", re.escape(str(n).strip())))
                      for n in names if n and str(n).strip()}, key=len, reverse=True)
    return r"(?<![\w.\-])(?:" + "|".join(escaped) + r")(?![\w\-])"


def _ecosystem_patterns(names, r_case_sensitive=False) -> dict[str, list[re.Pattern]]:
    n = _name_pattern(names)
    q = r"[\"'`*]*"
    # R package names are case-sensitive: `library(MeTEor)` does not load CRAN's
    # `meteor`. When the caller asks for it, R code must spell the package exactly.
    rc = 0 if r_case_sensitive else re.I
    # Prose may capitalise a lower-case package name ("the R package Splatter"),
    # but a name with its own capitals must appear as written: CRAN's `acoRn` is
    # not the `acorn` a genomics paper installs from GitHub.
    rp = rc if any(str(name)[1:] != str(name)[1:].lower() for name in names) else re.I
    return {
        "r": [
            re.compile(rf"\b(?:library|require|requireNamespace|suppressPackageStartupMessages\(\s*library)\s*\(\s*{q}{n}{q}\s*[,)]", rc),
            re.compile(rf"\b(?:install\.packages|BiocManager::install|biocLite|remotes::install_cran|pak::pkg_install)\s*\([^)]*{q}{n}{q}", rc),
            re.compile(rf"{n}:::?[A-Za-z.][\w.]*\s*\(", rc),
            re.compile(rf"\bR[\s-]+(?:package|library)\s+(?:called\s+|named\s+)?{q}{n}", rp),
            re.compile(rf"{n}{q}\s+(?:R|Bioconductor|CRAN)[\s-]+(?:package|library)\b", rp),
            re.compile(rf"\b(?:Bioconductor|CRAN)\s+(?:package\s+)?{q}{n}", rp),
            re.compile(rf"{n}\s*\((?:an?\s+)?(?:R|Bioconductor)\s+package", rp),
            re.compile(rf"bioconductor\.org/packages/(?:(?:release|devel)/bioc/html/)?{n}", rc),
            re.compile(rf"cran\.r-project\.org/(?:web/)?package(?:s/|=){n}", rc),
        ],
        "python": [
            re.compile(rf"\bimport\s+{n}(?:\s+as\s+\w+)?\s*(?:$|[\n;,])", re.I | re.M),
            re.compile(rf"\bfrom\s+{n}(?:\.\w+)*\s+import\b", re.I),
            # Only flags that take no value may sit between `install` and the name:
            # in `pip install -r requirements.txt` nothing after `-r` is a package.
            re.compile(rf"\bpip3?\s+install\s+(?:(?:-U|--upgrade|--user|-q|--quiet|--pre|"
                       rf"--no-cache-dir|--no-deps)\s+)*{q}{n}", re.I),
            re.compile(rf"\bPython\s+(?:package|library|module)\s+(?:called\s+|named\s+)?{q}{n}", re.I),
            re.compile(rf"{n}{q}\s+(?:Python|PyPI)\s+(?:package|library|module)\b", re.I),
            re.compile(rf"pypi\.org/project/{n}", re.I),
            re.compile(rf"{n}\s*\((?:a\s+)?Python(?:\s+package)?\)", re.I),
        ],
        "conda": [
            re.compile(rf"\b(?:conda|mamba|micromamba)\s+install\b[^\n]*?(?:bioconda::)?{n}", re.I),
            re.compile(rf"\bbioconda::{n}", re.I),
        ],
    }


def spelled_alike(canonical, names) -> bool:
    """Whether the package name is one of the record's names up to case and separators.

    `Trim Galore` is `trim-galore` and `scikit_learn` is `scikit-learn`; `pygraphviz`
    is not `py-graphviz`, which the normalised lookup reaches only by removing a
    hyphen from the package's own name.
    """
    def key(s):
        return re.sub(r"[\s_.\-]+", "-", str(s or "").strip().lower()).strip("-")
    package = key(canonical)
    for n in names:
        if not n:
            continue
        # Equal up to case and separators, or the record's name with its separators
        # dropped (`IQ-TREE` is Bioconda's `iqtree`, `Diffu Stats` Bioconductor's
        # `diffuStats`). A package that adds a separator the name lacks is another
        # string (`py-graphviz` against `pygraphviz`).
        if package == key(n) or package == key(n).replace("-", ""):
            return True
    return False


def python_usage(ctx, name) -> str | None:
    """A snippet where the record uses ``name`` as a Python module, beyond imports."""
    n = _name_pattern([name])
    for pattern in (rf"[`:]~?{n}\.[A-Za-z_]\w*`",
                    rf"(?<![\w.\-]){n}\.py\b",
                    rf"\bpython3?\s+-m\s+{n}"):
        for text in (ctx.local_text, ctx.skill_text):
            m = re.search(pattern, text, re.I)
            if m:
                return " ".join(text[max(0, m.start() - 40):m.end() + 40].split())
    return None


@dataclass
class RecordContext:
    """What a single tool record says about itself, in its collection."""

    collection: str
    life_science: bool
    names: list[str]
    local_text: str
    skill_text: str
    repos: set[str] = field(default_factory=set)
    dois: set[str] = field(default_factory=set)
    # Share of the collection's skills whose text holds each word; see specific_overlap().
    word_share: dict = field(default_factory=dict)
    # Set when the record shows that the tool is the subject of its citing paper:
    # the repositories named after the tool, and whether a title opens with it.
    subject_repos: set = field(default_factory=set)
    subject_title: bool = False

    @property
    def is_subject(self) -> bool:
        return bool(self.subject_repos) or self.subject_title

    def all_text(self) -> str:
        return self.local_text + "\n" + self.skill_text

    def code_evidence(self, extra_names=(), only=None) -> dict[str, list[str]]:
        """``{ecosystem: [snippets]}`` where the record uses the name as that ecosystem's package.

        With ``only``, the record must use exactly that package name, and R code
        must spell it with its case.
        """
        # A name holding `::` is a namespace path (Perl's `Getopt::Long`), not a
        # package name; matched as one it reads as R code (`x::f`).
        names = [only] if only else list(self.names) + list(extra_names)
        names = [n for n in names if n and "::" not in str(n)]
        if not names:
            return {}
        out: dict[str, list[str]] = {}
        for ecosystem, patterns in _ecosystem_patterns(names, bool(only)).items():
            for pattern in patterns:
                for text in (self.local_text, self.skill_text):
                    m = pattern.search(text)
                    if m:
                        start = max(0, m.start() - 40)
                        out.setdefault(ecosystem, []).append(
                            " ".join(text[start:m.end() + 40].split()))
                        break
                if ecosystem in out:
                    break
        return out


_WORD = re.compile(r"[a-z][a-z0-9]+")


def _stem(word: str) -> str:
    """Plural and simple verb endings off, so `pipelines` meets `pipeline`."""
    for suffix in ("ies", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)] + ("y" if suffix == "ies" else "")
    return word


def words(text: str) -> set[str]:
    return {_stem(w) for w in _WORD.findall(str(text).lower())}


def collection_word_share(skills) -> dict:
    """``{word: share of skills whose name or description holds it}`` for one collection."""
    counts: dict[str, int] = {}
    for skill in skills:
        for w in words(f"{skill.get('name') or ''} {skill.get('description') or ''}"):
            counts[w] = counts.get(w, 0) + 1
    n = max(1, len(skills))
    return {w: c / n for w, c in counts.items()}


# Verbs a title uses when the tool it opens with is its subject: "X enables ...".
_SUBJECT_VERBS = ("is", "are", "enables", "allows", "provides", "offers", "uses", "identifies",
                  "improves", "reveals", "integrates", "infers", "predicts", "maps", "detects",
                  "performs", "accelerates", "facilitates", "achieves", "delivers", "supports",
                  "characterizes", "characterises", "quantifies", "models", "learns", "leverages")


def title_has_subject(title, name) -> bool:
    """Whether a paper title opens with the tool name as its subject.

    `VEGA is an interpretable generative model ...`, `STEM enables mapping ...`,
    `Seurat: ...`, `MS-DIAL - ...`. A title that merely mentions the tool later on
    does not count.
    """
    title, name = str(title or "").strip(), str(name or "").strip()
    key = normalize(name)
    if len(key) < 3:
        return False
    head = re.split(r"[:\u2013\u2014]|\s-\s|,", title, maxsplit=1)[0]
    if normalize(head) == key:
        return True
    verbs = "|".join(_SUBJECT_VERBS)
    return re.match(rf"^\s*{re.escape(name)}\s+(?:{verbs})\b", title, re.I) is not None


def subject_evidence(names, repos, titles) -> tuple[set, bool]:
    """(repositories named after the tool, whether a title opens with it)."""
    keys = {normalize(n) for n in names if len(normalize(n)) >= 3}
    named = {r for r in repos if normalize(r.rsplit("/", 1)[-1]) in keys}
    return named, any(title_has_subject(t, n) for t in titles for n in names)


def build_context(collection, life_science, record, tool_yaml, citing_skills,
                  word_share=None) -> RecordContext:
    """The record's own evidence, gathered from its index row, its yaml and its citing skills."""
    tool_yaml = tool_yaml or {}
    spans = [str(s) for s in tool_yaml.get("evidence_spans") or []]
    titles = [str(d.get("title")) for d in tool_yaml.get("derived_from") or []
              if isinstance(d, dict) and d.get("title")]
    version = tool_yaml.get("version_used")
    local = "\n".join(spans + titles + ([str(version)] if version else []))
    skill_parts = []
    for skill in citing_skills:
        skill_parts.append(str(skill.get("name") or ""))
        skill_parts.append(str(skill.get("description") or ""))
    repos = {k for k in (repo_key(u) for u in tool_yaml.get("source_repos") or []) if k}
    repos |= {k for k in (repo_key(u) for u in _URL.findall(local)) if k}
    dois = {str(d).lower() for d in record.get("dois") or []}
    dois |= {str(d.get("doi")).lower() for d in tool_yaml.get("derived_from") or []
             if isinstance(d, dict) and d.get("doi")}
    names = [n for n in (record.get("name"), record.get("slug")) if n]
    own = {k for k in (repo_key(u) for u in tool_yaml.get("source_repos") or []) if k}
    subject_repos, subject_title = subject_evidence(names, own, titles)
    return RecordContext(collection=collection, life_science=life_science, names=names,
                         local_text=local, skill_text="\n".join(skill_parts),
                         repos=repos, dois=dois, word_share=word_share or {},
                         subject_repos=subject_repos, subject_title=subject_title)


def name_is_weak(name, common_words) -> bool:
    """True when the name alone cannot carry identity: very short, or an English word."""
    key = normalize(name)
    return len(key) <= SHORT_NAME_LENGTH or key in common_words


# Words every life-science description uses. For a weak name, an overlap made
# only of these says the package is about biology, not that it is this tool:
# `EPIC` (immune deconvolution) and the Bioconda `epic` (a ChIP-seq peak caller)
# share `seq` and nothing else.
GENERIC_DOMAIN_TOKENS = frozenset("""
    seq sequencing sequence sequences sequenced rna dna cell cells single gene genes genome
    genomes genomic genomics read reads high different biological input output files file
    python program programs fast accurate large efficient default generate end one level full
    computational protein proteins sample samples biology bioinformatics tool toolkit
    distinguish quality short long
    """.split())
MIN_SPECIFIC_OVERLAP = 2


# A word held by this share of a collection's skills or more says what the
# collection is about, not what one tool does (`metagenome` in metagenomics).
COMMON_IN_COLLECTION = 0.02
# Likewise for a word held by this share of the registry's package descriptions.
COMMON_IN_REGISTRY = 0.01
MIN_SKILL_OVERLAP = 2
MIN_SKILL_OVERLAP_WEAK_NAME = 3


def specific_overlap(ctx, registry_text, identity_values, registry_share=None) -> list[str]:
    """Words shared by the citing skills and the package description that are specific.

    Excluded: stopwords, identity words (a name cannot corroborate itself), the
    generic life-science vocabulary, any word held by COMMON_IN_COLLECTION of the
    collection's skills or more, and any word held by COMMON_IN_REGISTRY of the
    registry's package descriptions or more.
    """
    registry_share = registry_share or {}
    identity = set()
    for value in identity_values:
        identity |= words(value)
        identity.add(normalize(value))
    shared = words(ctx.skill_text) & words(registry_text)
    return sorted(w for w in shared
                  if w not in identity and w not in STOPWORDS and w not in GENERIC_DOMAIN_TOKENS
                  and len(w) > 2 and ctx.word_share.get(w, 0.0) < COMMON_IN_COLLECTION
                  and registry_share.get(w, 0.0) < COMMON_IN_REGISTRY)


def domain_support(domain, ctx, registry_share, weak) -> bool:
    """Whether the local-text domain signal is enough to carry the name.

    The measured signal (cosine over the record's own text) is necessary. On top
    of it, a weak name needs two shared words that are specific: not generic
    life-science vocabulary, not common in the collection's skills, not common
    in the registry's descriptions. A distinctive name needs one specific word:
    `MetAlign` (mass spectra) and the Bioconda `metalign` (metagenomes) share only
    `alignment`, which many Bioconda packages use, and the metabolomics `metid`
    shares only `lc` and `ms` with Bioconductor's `MetID`.
    """
    if domain["verdict"] != "corroborated":
        return False
    overlap = domain["overlap_tokens"]
    specific = [t for t in overlap if t not in GENERIC_DOMAIN_TOKENS
                and registry_share.get(_stem(t), 0.0) < COMMON_IN_REGISTRY
                and ctx.word_share.get(_stem(t), 0.0) < COMMON_IN_COLLECTION]
    if weak:
        return len(specific) >= MIN_SPECIFIC_OVERLAP
    return len(specific) >= 1


@dataclass
class Verdict:
    accept: bool
    reason: str
    corroboration: list = field(default_factory=list)
    contradiction: list = field(default_factory=list)


def subject_exception_repos(registry, record, ctx: RecordContext) -> list[str] | None:
    """Whether a Bioconductor package is let through by name, and what to check.

    Bioconductor names are unique and curated, and its packages move between
    accounts (GuangchuangYu/clusterProfiler is now YuLab-SMU/clusterProfiler), so
    when the record is the subject of its paper, a repository of the same name is
    not a contradiction there ([]: nothing to check). A package that declares no
    repository is let through only if the paper's repository is that R package:
    the caller reads its DESCRIPTION (resolve_tool_licenses.check_subject_exception)
    and gets the repositories to read. MetNet, a Java tool whose paper's repository
    is simeoni-biolab/MetNet, is not Bioconductor's `MetNet`, which declares none.
    Returns None when the exception does not apply.
    """
    if registry.id != "bioconductor" or not ctx.is_subject:
        return None
    package_repos = {k for k in (repo_key(v) for v in registry.repo_values(record)) if k}
    own = ctx.subject_repos or ctx.repos
    if package_repos & own or registry.dois(record) & ctx.dois:
        return None
    if not package_repos:
        return sorted(own)
    names = {k.rsplit("/", 1)[-1] for k in own}
    return [] if any(k.rsplit("/", 1)[-1] in names for k in package_repos) else None


def judge(registry, canonical, record, ctx: RecordContext, common_words) -> Verdict:
    """Whether package ``canonical`` of ``registry`` is the tool ``ctx`` names.

    The rule, in order:

    1. A Bioconductor data package is never the tool (it names a dataset).
       When the record shows that the tool is the subject of its citing paper
       (a repository named after the tool, or a title opening with it), a package
       is the tool only if it declares that repository or lists that paper; for
       Bioconductor, a repository of the same name or none declared suffices.
    2. A contradiction always refuses unless the package's repository or
       publication is the record's own: code evidence for another ecosystem
       (`library(x)` against a Python package, `import x` against an R one, an
       R package against a Bioconda package of the bare name, which Bioconda
       would have prefixed), or, without strong evidence, a domain mismatch.
    3. A general registry (CRAN, PyPI, bio.tools) needs strong evidence: the
       repository, the publication or, for CRAN and PyPI, code evidence in the
       registry's own ecosystem.
    4. A curated life-science registry (Bioconductor, Bioconda) in a collection
       outside the life sciences needs strong evidence too.
    5. In a life-science collection, a weak name (four characters or fewer, or
       an English word) needs strong evidence, a corroborated domain signal
       with two specific shared words (domain_support()), or
       MIN_SKILL_OVERLAP_WEAK_NAME specific words shared by the citing skills
       and the package description (specific_overlap()).
    6. Any other name needs strong evidence, a corroborated domain signal with
       one specific shared word, or MIN_SKILL_OVERLAP specific words shared by
       the citing skills and the package description.
    """
    strong, contra = [], []
    package_repos = {k for k in (repo_key(v) for v in registry.repo_values(record)) if k}
    shared = sorted(package_repos & ctx.repos)
    if shared:
        strong.append({"kind": "repository", "value": shared[0]})
    shared_dois = sorted(registry.dois(record) & ctx.dois)
    if shared_dois:
        strong.append({"kind": "publication", "value": shared_dois[0]})
    code = ctx.code_evidence([canonical])
    ecosystem = registry.ecosystem
    # Code corroborates a package only when it names that package as the registry
    # spells it: `conda install pygraphviz` is not Bioconda's `py-graphviz`.
    exact = ctx.code_evidence(only=canonical)
    if ecosystem in ("r", "python") and exact.get(ecosystem):
        strong.append({"kind": "code", "value": exact[ecosystem][0]})
    if ecosystem == "conda" and (exact.get("conda") or exact.get("python")):
        found = exact.get("conda") or exact.get("python")
        strong.append({"kind": "code", "value": found[0]})
    decisive = any(s["kind"] in ("repository", "publication") for s in strong)

    if registry.is_data_package(record):
        return Verdict(False, "data-package", strong, [{"kind": "data-package"}])
    if registry.restricts_use(record):
        # The licence field is then not the whole story; leave it to a reviewer.
        return Verdict(False, "registry-flags-restricted-use", strong, [])
    if readme_restriction(registry.text(record)):
        # The package's own description limits who may use it (KEGGREST: an
        # Artistic-2.0 client, "Only for academic use by academic users", because
        # the service it calls is). The licence field is then not the whole story.
        return Verdict(False, "registry-text-restricts-use", strong, [])

    # The registry matched only after punctuation was removed from a different
    # string (`pygraphviz` and Bioconda's `py-graphviz`, the wrapper of another
    # project): only the repository or the publication can say it is the tool.
    if not spelled_alike(canonical, ctx.names) and not decisive:
        return Verdict(False, "name-differs-needs-repository", strong, [{
            "kind": "spelling", "value": f"package {canonical!r}; record {', '.join(ctx.names)}"}])

    # The paper that cites the tool is about it, so the tool is that paper's code.
    # A package is then the tool only if it declares that repository (or lists that
    # paper): an import name is not a distribution name. `import vega` in the VEGA
    # paper is not PyPI's `vega`, the Jupyter widget of vega/ipyvega.
    if ctx.is_subject:
        same = bool(package_repos & (ctx.subject_repos or ctx.repos)) or bool(shared_dois)
        if not same and subject_exception_repos(registry, record, ctx) is not None:
            same = True
        if not same:
            return Verdict(False, "contradicted", strong, [{
                "kind": "subject-repository",
                "value": "record is the subject of its paper ("
                         + (", ".join(sorted(ctx.subject_repos)) or "title") + "); package declares "
                         + (", ".join(sorted(package_repos)) or "no repository")}])

    other = {"r": "python", "python": "r"}.get(ecosystem)
    if other and code.get(other) and not code.get(ecosystem):
        contra.append({"kind": "ecosystem", "value": f"{other}: {code[other][0]}"})
    elif ecosystem == "r" and not exact.get("r"):
        # A name present in both ecosystems (MuData: scverse's Python `mudata`, and
        # a Bioconductor package of the same name). An R package without R code is
        # contradicted when the record uses the name as a Python module in a way
        # the import patterns do not see: a documentation role naming one of its
        # classes ({class}`~mudata.MuData`), a `name.py` file, `python -m name`.
        usage = python_usage(ctx, canonical)
        if usage:
            contra.append({"kind": "ecosystem", "value": f"python: {usage}"})
    if ecosystem == "conda" and code.get("r") and not (code.get("conda") or code.get("python")):
        contra.append({"kind": "ecosystem", "value": f"r: {code['r'][0]}"})

    domain = domain_signal(ctx.local_text, registry.text(record),
                           list(ctx.names) + [canonical], DOMAIN_THRESHOLD)
    domain_summary = {"kind": "domain", "value": domain["verdict"], "score": domain["score"],
                      "overlap": domain["overlap_tokens"][:8]}
    skill_words = specific_overlap(ctx, registry.text(record), list(ctx.names) + [canonical],
                                   registry.word_share(words))
    skill_summary = {"kind": "skill-domain", "value": "corroborated" if len(skill_words) >=
                     MIN_SKILL_OVERLAP else "insufficient", "overlap": skill_words[:8]}

    if contra and not decisive:
        return Verdict(False, "contradicted", strong, contra)
    if registry.scope == "general":
        kinds = {s["kind"] for s in strong}
        if registry.id == "biotools":
            ok = bool(kinds & {"repository", "publication"})
        else:
            ok = bool(kinds & {"repository", "code"})
        return Verdict(ok, "corroborated" if ok else "general-registry-needs-corroboration", strong, contra)
    if not ctx.life_science:
        return Verdict(bool(strong), "corroborated" if strong else "outside-life-science-needs-corroboration",
                       strong, contra)
    if strong:
        return Verdict(True, "corroborated", strong, contra)
    weak = any(name_is_weak(n, common_words) for n in [canonical] + list(ctx.names))
    share = registry.word_share(words)
    if weak:
        if domain_support(domain, ctx, share, weak=True):
            return Verdict(True, "domain-corroborated", [domain_summary], contra)
        if len(skill_words) >= MIN_SKILL_OVERLAP_WEAK_NAME:
            return Verdict(True, "skill-domain-corroborated", [skill_summary], contra)
        return Verdict(False, "weak-name-needs-corroboration", strong,
                       contra + [domain_summary, skill_summary])
    if domain_support(domain, ctx, share, weak=False):
        return Verdict(True, "domain-corroborated", [domain_summary], contra)
    if skill_summary["value"] == "corroborated":
        return Verdict(True, "skill-domain-corroborated", [skill_summary], contra)
    return Verdict(False, "uncorroborated", strong, contra + [domain_summary, skill_summary])
