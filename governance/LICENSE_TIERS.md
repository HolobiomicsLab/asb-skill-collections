# License tiers

`license_tier` answers a consumer question — *what may I do with the tool this skill
grounds on?* — and is **separate** from the paper open-access axis (`access.type`),
which answers *may we redistribute the source?*

## What the tier does and does not govern

Three different questions get confused with one another. Only the third is what
`license_tier` answers.

| Question | Governed by | Bearing on this collection |
|---|---|---|
| May we **describe** a tool in a skill? | Not the tool's licence. A tool's name, purpose, input/output types, and the fact that a paper used it are facts, and facts are not copyrightable. | None. Every tool is describable, proprietary ones included — otherwise no review article could exist. |
| May we **redistribute** the tool's code, wrapper or config? | The tool's licence, fully. | Only if we vendor those bytes. This collection ships prose and references, so it does not. |
| May a consumer **run** the tool for their purpose? | The tool's licence, fully. | This is what `license_tier` advises on. |

The consequence worth stating plainly: **an unlicensed tool is not thereby freely
usable, and it is not thereby un-describable either.** Absent a licence, default
copyright reserves all rights, and GitHub's terms grant other users only viewing and
forking within GitHub — no redistribution, no derivative works. That makes "no
licence" the *most* restrictive state for redistribution, not a permissive one. It
places no restriction at all on naming the tool and saying what it does.

So the tier is **downstream-use advice attached to a record**, never an admission
gate. A skill is never excluded because the tool it describes is proprietary or
unlicensed. Vendoring is what the tier gates.

## The tiers

| Tier | Meaning | Examples |
|---|---|---|
| `open` | Commercial use OK | MIT, Apache-2.0, BSD, MPL-2.0, CC-BY/CC0, **GPL/AGPL/LGPL** |
| `noncommercial` | Academic / noncommercial only | CC-BY-NC-*, PolyForm-Noncommercial, "academic use free, commercial by permission" |
| `restricted` | Established, and it constrains | CC-BY-ND, proprietary vendor EULA, declared all-rights-reserved |
| `unknown` | **No tool-level evidence found** | not looked up; lookup failed; a LICENSE file that no classifier could identify |

Copyleft maps to `open`: it governs derivative *distribution*, not whether a consumer
may use the tool commercially. Canonical SPDX→tier map: `governance/license_tiers.yaml`.
A licence string that is present but unrecognised falls back to `restricted`, unless
its text contains a noncommercial keyword → `noncommercial`.

### `unknown` is not `restricted`

`restricted` is a **verdict**: a licence was established and it constrains reuse.
`unknown` is an **open question**: nothing about the tool's own licence was
established. They have different remedies — a `restricted` tool needs a lawyer or a
vendor conversation, an `unknown` tool needs a lookup — so a consumer that cannot
tell them apart cannot act on either.

This is the same distinction `source_reuse` already draws between `None` (unknown,
blocks and reports loudly) and `none` (a known refusal). The tool axis previously
collapsed it, defaulting every unresolved tool to `restricted`; that made 257 of 909
tools indistinguishable from a genuine proprietary verdict, and made the catalogue
look far more resolved than it was.

**Why a tier value rather than a `--strict`-style flag.** The state belongs to the
record, not to the run. A flag would make the same catalogue mean different things
depending on how it was invoked, and every consumer would have to be told which mode
produced the file it is reading. A value is visible to everyone, is diffable, and
lets each consumer choose its own strictness. `--strict` also already means
"promotion mode" in `release_gate.py`; a second meaning there would be its own bug.

### Non-profit and commercial use

| Tier | Non-profit / academic | Commercial | Redistribution by us |
|---|---|---|---|
| `open` | permitted | permitted | permitted (respect copyleft on derivatives) |
| `noncommercial` | permitted | **not permitted** without a separate licence | link-only |
| `restricted` | per the licence | per the licence — usually a vendor EULA | link-only |
| `unknown` | describing and using are unaffected | verify before relying on it | **never vendor** — treat as all-rights-reserved |

Both `noncommercial` and `restricted` tiers are **link-only** in shipped grounding
bundles (referenced, never embedded). Beyond that, they differ:

- **`noncommercial`** additionally triggers a **blocking runtime acknowledgment**
  (commercial use is forbidden without a separate license; the consumer must
  explicitly confirm a permitted purpose before the skill is applied).
- **`restricted`** instead carries a **non-blocking soft note**: "licence established
  and it constrains reuse — check it before commercial use or redistribution."
- **`unknown`** carries a different non-blocking note: "no tool-level licence
  evidence — verify before redistributing." It does not block, because the absence of
  evidence is not a prohibition on use; it does forbid vendoring, because absence of a
  grant is not a grant.

## A tool's licence may only come from the tool

A licence claim on a tool record must rest on evidence about **that tool**: its own
repository, its own `DESCRIPTION`/`pyproject`, its own LICENSE file, its own
distribution page.

It may **never** be inherited from a paper that uses the tool. That inheritance was
the mechanism behind issue #42: every tool tier in the metabolomics catalogue was the
licence of a citing paper, aggregated most-restrictively across citations, which
recorded CAMERA (GPL) as Apache-2.0 because a paper using CAMERA is Apache-2.0, and
scikit-learn (BSD) as `noncommercial` because one preprint mentioning it is
CC-BY-NC-ND. Both directions are wrong and neither was visible, because the record
did not say whose licence it was.

`scripts/license_tier.py::licence_subject` exists to make the subject explicit, and
`tools_index.json` records `license_subject` on every entry. A `-paper` detection is
evidence about a paper and yields `unknown` on the tool axis. Enforced by
`scripts/check_tools_index.py`.

### Not every catalogue entry is software

The catalogue is assembled by extraction from papers, so an entry may be a software
package, a vendor instrument, a proprietary application, or a fragment a paper
happened to name. `entry_kind` says which, from the vocabulary in
`governance/tool_entry_kinds.yaml`:

| `entry_kind` | What it is | Tier |
|---|---|---|
| `software` | A tool with a licence to find | resolved, or `unknown` while it is not |
| `vendor_product` | An instrument or a proprietary application | `restricted` |
| `artefact` | An extraction defect: a module path, a bare URL, a function call, a sentence fragment | `unknown` |

**Instruments and vendor software are legitimate entries and legitimate to use.** A
lab uses the instrument it owns and the software it licensed; nothing here
discourages that. What they are not is redistributable, and there is no repository
to resolve an SPDX id from — so they take `restricted`, whose meaning is exactly
"use is governed by an agreement rather than an open licence", and not `unknown`,
which would claim a lookup is outstanding when none is possible.

Artefacts stay in the catalogue because skills reference their slugs and removing a
row would break that. Labelling them stops them counting as unresolved licence work.
An entry of `governance/tool_licences_reviewed.yaml` sets `entry_kind` for the names it
lists, and a reviewer's kind outranks the vocabulary.

The distinction is what makes the `unknown` count mean something. Of 909 entries: 195
`open`, 20 `restricted`, 1 `noncommercial`, and 693 `unknown` — of which 39 are
artefacts, leaving **654 pieces of software genuinely awaiting a licence lookup**.

Vendor terms are matched as whole words, never inside a token: `Thermo Xcalibur` is a
vendor product and `ThermoRawFileParser` is Apache-2.0 open source. Proprietary
applications that carry no vendor word are a curated list, because a name alone
cannot say whether software is proprietary and guessing either way is worse than a
reviewed entry — Skyline, ProteoWizard and msconvert are deliberately absent from it.
The vocabulary is measured against the 196 tools whose licences were resolved from
their own repositories: none of them may classify as anything but `software`, and
`tests/test_classify_tool_entries.py` fails if a carelessly added term makes one.

### Where a tool licence is allowed to come from

`scripts/resolve_tool_licenses.py` writes `tool_licenses.json`, and that file is the
only thing `enrich_tools_index.py` will tier a tool from. Precision comes before
coverage: a wrong licence shown as `open` is worse than `unknown`. Sources, in order
of precedence, all evidence about the tool itself:

| Route | Evidence | Network |
|---|---|---|
| `reviewed` | `governance/tool_licences_reviewed.yaml`: a name checked by hand against the tool's own licence statement. A name listed there is never looked up anywhere else, so a reviewer's "leave unknown" holds. | no |
| `self_published` | The tool is the subject of a paper already in the corpus, matched on exact name equality, never substring, so that paper's repository is the tool's. | no |
| `registry` | A package of the same name in a registry declared in `governance/tool_registries.yaml`, accepted only when the record's own evidence supports the identity (below). | yes, cached |

The registries are Bioconductor and Bioconda (`scope: life_science`) and CRAN, PyPI and
bio.tools (`scope: general`).

#### A name match is not identity

An exact name match does not establish that a package is the tool a paper meant.
Bioconda's `umap` is a genome mappability tool, not the dimension-reduction method;
Bioconductor's `BERT` reduces batch effects and is not the language model; Bioconda's
`gambit` types microbes and is not the particle-physics code; PyPI's `docker` is a
Python SDK, and PyPI's `devtools` and `shiny` are not the R packages. Identity is
therefore judged per record, in its collection (`scripts/tool_identity.py`), from the
record's own evidence: its evidence spans, the version it quotes, the titles of the
papers it was extracted from, its repositories and DOIs, and the names and
descriptions of the skills that cite it. The same name can be two different tools in
two collections, and the rule allows that.

Evidence counts as **strong** when the package's repository or homepage is one the
record names, when a DOI bio.tools lists for the tool is one of the record's, or when
the record uses the name as a package of the registry's ecosystem (`library(x)`,
`x::f`, `BiocManager::install("x")`, `R package x`; `import x`, `pip install x`,
`Python package x`; `conda install x`). A match is accepted as follows:

1. A Bioconductor data, annotation or workflow package is never the tool: it wraps a
   dataset named like the tool (MSigDB). When the record shows that the tool is the
   subject of its citing paper (a repository among its `source_repos` named after the
   tool, or a paper title opening with the tool as its subject: `X: ...`, `X is ...`,
   `X enables ...`), a package is the tool only if it declares that repository or lists
   that paper; otherwise the match is contradicted. Bioconductor is the one exception:
   its names are unique and curated and its packages move between accounts
   (GuangchuangYu/clusterProfiler became YuLab-SMU/clusterProfiler), so a repository of
   the same name, or none declared, is not a contradiction there. An import name is not a
   distribution name: `import vega` in the VEGA paper is not PyPI's `vega`, a Jupyter
   widget, and `from STEM.model import *` is not PyPI's `stem`, a Tor controller.
2. A contradiction refuses the match unless the package's repository or publication is
   the record's: code evidence for another ecosystem (`library(x)` against a Python
   package, `import x` against an R one, an R package against a Bioconda package of the
   bare name, which Bioconda would have prefixed).
3. A general registry needs strong evidence: CRAN and PyPI a shared repository or
   code evidence, bio.tools a shared repository or publication. PyPI is asked only
   about names with Python evidence, and bio.tools only about records that carry what
   looks like the tool's own paper or repository.
4. A curated registry in a collection outside `life_science_collections` (astronomy
   and agentic-ai today, and any new domain until it is listed) needs strong evidence.
5. In a life-science collection, a weak name (four characters or fewer, or a word of
   `governance/tool_name_common_words.txt`) needs strong evidence, the measured domain
   signal (docs/design/registry-match-corroboration-2026-11-07.md) with two shared words
   that are specific (not generic life-science vocabulary, not common in the
   collection's skills, not common in the registry's descriptions), or three specific
   words shared by the citing skills and the package description.
6. Any other name needs strong evidence, the domain signal with one specific shared
   word, or two specific words shared by the citing skills and the package
   description. Silence is not identity: `CoLoRMap` (long-read correction) and
   Bioconda's `colormap` (matplotlib colours) share a normalised name and nothing
   else.
7. R code must spell the package with its case: `library(MeTEor)` does not load CRAN's
   `meteor`.
8. Two packages that declare the same repository are one tool, and a package that
   declares the repository of a package accepted on strong evidence is accepted too;
   the first declared registry then gives the licence and the others are kept as
   `superseded`. Otherwise, when packages from several registries are accepted for
   one record and declare different licences, the record stays `unknown` unless
   exactly one of them rests on strong evidence (decision K3: a name present in two
   ecosystems with different licences and nothing to tell them apart is not
   resolved). A general registry's answer is also withheld when a same-name package
   that was not contradicted declares another licence: bio.tools still lists bedtools
   as GPL-2.0, the package has been MIT since 2.28.

The measured effect of the rule on the ten released collections is in
`docs/design/tool-licence-resolution-2026-11-11.md`. The reviewed exclusions of
`tool_registries.yaml` remain as data.

#### Confirming the licence against the repository

Bioconductor, CRAN and PyPI metadata are written by the package authors. A Bioconda
recipe and a bio.tools entry are written by someone else, and their licence strings
are often not the tool's: bio.tools lists MUON as GPL-3.0 and bedtools as GPL-2.0, and
Bioconda lists STAR and Kraken2 as GPL-3.0-or-later, while each repository carries a
different licence file. Every registry resolution whose package declares a repository
on GitHub or GitLab is therefore checked against that repository's own licence file
(`scripts/repository_licence.py`), read anonymously as raw content, never through an
API: `LICENSE`, `LICENSE.txt`, `LICENSE.md`, `COPYING`, `COPYING.txt`, `LICENCE`,
`LICENCE.txt`, then the `License:` field of `DESCRIPTION`.

The file classifier recognises a licence only from its canonical title or grant
wording: MIT, BSD-2-Clause and BSD-3-Clause by their clauses, Apache-2.0, MPL-2.0,
GPL, LGPL and AGPL with the version in the title, Artistic-2.0, CC0, the Unlicense,
the Creative Commons licences by their clauses, and a custom text as `noncommercial`
only when it says in plain words that use is non-commercial or academic only. A file
that holds two licences (a bundled component's terms appended) is unread. A licence
text cannot say whether a GNU licence is "only" or "or later", so the reading is the
version without a suffix (`GPL-3.0`, as the reviewed map writes it) unless the file
also holds the "or (at your option) any later version" notice.

A file that offers a choice in plain words ("dual licensed under GPL-3.0 or BSD-3-Clause",
Jellyfish) is read as an SPDX `OR` expression, as is a file that says so on an
`SPDX-License-Identifier` line.

Who wrote the registry's licence field decides what the repository may change:

| Registry | Repository agrees | Repository differs, same tier | Repository differs in tier | Nothing readable |
|---|---|---|---|---|
| Bioconda, bio.tools (third party) | registry licence, `confirmed` | the file's licence, `replaced` | the file's licence, `replaced` | `unknown`, withheld as `withheld-unconfirmed:<why>` |
| PyPI (the authors) | registry licence, `confirmed` | the file's licence, `replaced` | `unknown`, withheld as `withheld-contradiction:pypi=<a>\|repository=<b>` | registry licence, `kept-unconfirmed` |
| Bioconductor, CRAN (the authors' DESCRIPTION) | registry licence, `confirmed` | registry licence, `kept-registry-declares` | `unknown`, withheld as `withheld-contradiction` | registry licence, `kept-unconfirmed` |

For Bioconductor and CRAN only the repository's `DESCRIPTION` is read. A `LICENSE`
file there may carry the terms of a bundled component (xcms) and never overrides the
declared licence. A replaced record carries detection `repository-licence-file`,
`license_evidence` the file read, and the registry's reading under `confirmation`
(`registry_license`, `registry_tier`, `registry_evidence`). MassCube is the measured
PyPI contradiction: PyPI says CC-BY-NC-4.0, the repository Apache-2.0.

Three further checks apply on top of the table.

- **A permissive file that adds terms is not that licence.** For MIT, BSD, Apache-2.0,
  the Unlicense and CC0, the classifier removes the licence's canonical wording (for
  MIT the grant sentence, the notice condition and the warranty disclaimer; for BSD the
  opening sentence, the standard clauses and the disclaimer; for Apache the licence
  text to "END OF TERMS AND CONDITIONS", its appendix and the short notice; for the
  Unlicense its whole text; for CC0 everything from its title on) and drops copyright
  lines. If what remains speaks of a dual licence, non-commercial, academic, non-profit
  or educational use, research purposes, industrial use, a commercial licence or
  commercial use, the permission of the authors or "contact us", the file is not read
  as the plain licence: it is `noncommercial` when it says in plain words that
  commercial use is excluded or needs a separate licence (bmxp: "redistribution
  requires obtaining a separate commercial license"), and unread otherwise. Such a
  file withholds the record as `withheld-added-terms`, except that a third-party
  registry's licence is replaced by a `noncommercial` reading. GNU and Creative
  Commons texts are not checked, because their own wording uses these words.
- **The README.** For a record that would be recorded `open`, the repository's README
  (`README.md`, `README.rst`, `README`, `README.txt`) is read the same way. A sentence
  that restricts use of the tool itself ("free for all academic and educational
  purposes", "academic use only", "not for commercial use", "commercial use requires
  a licence", "a license is needed", "for research purposes only", an industrial
  licence) withholds the record for every source as `withheld-readme-restriction`,
  with the sentence quoted (USAT: an LGPL-2.1 file, and a README that says a licence
  is needed for industrial use). A sentence about a dependency or a third-party tool
  is skipped when it says so, and "For research use only" next to a sentence on
  diagnostic or clinical use is a regulatory disclaimer, not a licence term. A README
  that mentions another tool's restriction without saying so still withholds the
  record; unknown is the safe side.
- **Guards on a replacement.** The repository read must be named like the matched
  package or the record (`withheld-repository-name`: the bio.tools repository of
  bootRanges, `bootRangespaper`, holds the paper's scripts). Two GNU statements of one
  family that differ only in version give the unversioned family, `GPL`, `LGPL` or
  `AGPL`, read as open, with both strings kept under `confirmation`
  (`family-fallback`: FastTree, Bioconda GPL-2.0-or-later and a GPL version 3 text).
  Different families (GPL against LGPL) keep the repository file's licence. A
  replacement that makes the tier more restrictive is recorded from the repository.

What none of this sees: a restriction stated only on a project website or in source
file headers, and a repository that moved, whose old copy keeps its old statement
(EpiNano's bio.tools repository is the old location and still passes the name guard).

#### Reading the licence string

`scripts/tool_licence_text.py` reads what the registry declares, with an explicit table
and the R `DESCRIPTION` grammar (`GPL (>= 2)`, `GPL-2 | GPL-3`, `MIT + file LICENSE`,
`file LICENSE`):

- A version is never invented. `GPLv2+` is `GPL-2.0-or-later`; an explicit version
  without "or later" is `-only`, as SPDX's own deprecated ids (`GPL-2.0`) mean.
- An unversioned family (`GPL`, `LGPL`, `AGPL`, `BSD`) gets a tier only because every
  member of the family is `open` in `license_tiers.yaml`, and the record then keeps the
  source's words (`GPL`), not a guessed SPDX id. `Apache` and `Artistic` without a
  version stay unread: their 1.x versions are not in the tier map.
- `+ file LICENSE` is read as the template it is for MIT and the BSD licences, and as
  the attribution terms the GNU licences permit; after any other licence the file may
  restrict, so the string is unread. `file LICENSE` alone is unread.
- Alternatives (`|`, `OR`) take the most permissive alternative that was read;
  conjunctions (`AND`) need every part read and take the most restrictive.
- Non-commercial and no-derivatives licences never land in `open`: a Creative Commons
  licence is parsed by its clauses, and any other string that speaks of non-commercial
  or academic use is unread.
- An unread string is `unknown`, never the `restricted` fallback.

The raw string stays in `tool_licenses.json` as `license_raw`.

#### What a resolved record carries

Every resolved record carries `license_detection` (`reviewed-map`, `bioconductor-package`,
`bioconda-package`, `cran-package`, `pypi-package`, `biotools-entry`,
`repository-licence-file`, or a repository detection for the introducing paper) and `license_evidence`, the address the licence
was read from: the registry's package page or the reviewed entry's `evidence_url`. Both
are written into `tools_index.json` and `tools/<slug>.yaml`. `repo_url` is the tool's own
repository, from the reviewed map or the registry, and is empty on an unresolved tool;
the repositories of the papers that cite a tool stay in `source_paper_repos` (decision
K1).

`check_tools_index.py` fails if `tools_index.json` drifts from the resolution it was
derived from, if a tool carries a tier with no entry behind it, if `tool_licenses.json`
is absent while a record claims a resolved licence, or if a registry or reviewed tier
names no `license_evidence`; its line for each collection reports the resolved and
unknown counts, so a collection that ends all `unknown` is visible. No gate makes a
network call. `scripts/check_tool_licence_consistency.py` checks across collections that
one entity (one `license_evidence` address) carries one licence.

Licence enrichment runs with `enrich_tools_index.py --licence-only`, which leaves the
skill-tool links (`used_by_skills`, `tools_used`) byte-identical (decision K2). The
pipeline step is documented in `docs/domain-onboarding.md`.

## The source-reuse axis

`license_tier` answers *"what may I do with the tool?"*. It does **not** answer
*"what may we do with the source text?"* — and the two disagree. CC-BY-ND permits
commercial use of a tool (so it is not `noncommercial`) while forbidding derivative
text (so it is not `open`). Reading a paper's licence through the tool tier would
call such a source open, which is the mistake the blanket "pre-prints are always
CC-BY" rule made.

The second canonical table, `source_reuse` in `license_tiers.yaml`, answers the
source question. Reach it via `scripts/license_tier.py::source_reuse_for_license`.

| Value | Meaning | Examples |
|---|---|---|
| `full` | Redistribute, quote at length, derive — the open-access bar | CC-BY, CC-BY-SA, CC0 |
| `limited` | Some grant, but not full reuse; link-only | CC-BY-NC-*, CC-BY-ND-* |
| `none` | No reuse rights granted | arXiv `nonexclusive-distrib` |
| *(absent)* | **Unknown** — blocks admission, reported loudly | any unlisted licence |

An unlisted licence returns `None`, never a default. `None` (unknown) and `none`
(a known refusal) are different answers and must not be collapsed: one means we
failed to establish the rights, the other means the rights were withheld. Only
`full` admits a source at an open `access.type`. See
`scripts/preprint_license.py` and `governance/OPEN_ACCESS_POLICY.md` § Pre-prints.
