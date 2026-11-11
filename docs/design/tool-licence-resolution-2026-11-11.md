# Tool licence resolution, 11 November 2026

Intent INT-ASB-050: give the tool records of the ten released collections a licence
that is the tool's own, with the source it was read from, or `unknown`. A wrong
licence shown as `open` is worse than `unknown`, so precision comes before coverage.
The rule is stated in `governance/LICENSE_TIERS.md` ("Where a tool licence is allowed
to come from"); this note records why it has its shape and what it does to the ten
collections.

## What was wrong

The resolver of 21 August matched a tool name exactly against Bioconductor and
Bioconda and took the licence string through a substring classifier. Run on the ten
released collections it resolved 1,150 of 7,398 records, and a sample of 40 held two
wrong tools and three doubtful ones:

- the dimension-reduction method UMAP resolved to Bioconda's `umap`, a genome
  mappability tool (188 skill citations over seven collections);
- the language model BERT (agentic-ai) to Bioconductor's `BERT`, a batch-effect tool;
- the particle-physics GAMBIT (astronomy) to Bioconda's `gambit`, a microbial typer;
- `msigdb` is a data package for a database, `singularity` the legacy container line.

Licence strings were mapped to the wrong version (`GPLv2` and `GPLv2+` to GPL-3.0,
`LGPL 2.1 or later` to LGPL-3.0, bare `GPL` to GPL-3.0), one non-commercial licence
read as CC-BY-4.0 and `open`, and 347 name matches stayed unread (`BSD-3`, `Apache
2.0`, `GPL-2 | GPL-3`, `file LICENSE`). The most cited tools (R, Python, Seurat,
scikit-learn, PyTorch, NumPy, ggplot2) are in neither registry, and a PyPI-first
lookup returns the Python `devtools`, `shiny` and `docker` for the R packages and the
container engine.

## The identity rule

A name match is accepted only when the record's own evidence supports it. The
evidence is read per record, in its collection, because the same name denotes
different tools in different collections: `Umap` in genomics is the mappability tool
and `UMAP` in transcriptomics is the method, and the rule resolves each in its place.

Strong evidence is a repository or homepage the package declares that the record
also names, a DOI bio.tools lists for the tool that the record carries, or code that
uses the name as a package of the registry's ecosystem. Weaker evidence is
vocabulary: the domain signal measured on 7 November (cosine over identity-free
tokens of the record's spans and citing-paper titles against the package
description, threshold 0.021713), and words shared by the citing skills and the
package description.

The previous design accepted any curated-registry match a reviewer had not excluded,
on the argument that a life-science registry carries the domain constraint
structurally. That holds for a collection about the life sciences and for a
distinctive name; it fails for both traps measured here:

- outside the life sciences (BERT, GAMBIT), so a curated registry there needs strong
  evidence;
- for a short or English-word name (UMAP, cooler, singularity), and for distinctive
  names that only collide after normalisation (`CoLoRMap` and `colormap`, `DiSCo`
  and `disco`, `MetAlign` and `metalign`), so every match now needs some
  corroboration.

Vocabulary is filtered before it counts. A one-word overlap such as `seq` or
`sequence` says that a package is about biology, not that it is this tool: `EPIC`
(immune-cell deconvolution) and Bioconda's `epic` (a ChIP-seq peak caller) share
`seq` and nothing else. Words are therefore discounted when they are generic
life-science vocabulary, common in the collection's skills (2% or more), or common in
the registry's descriptions (1% or more).

For an ambiguous name the reviewed map takes precedence, and applies a context only
through machine-checkable keys (`any_terms`, `none_terms`, `ecosystems`,
`collections`) when exactly one context matches. A context described by a sentence
alone leaves every record unknown. This is the safer of the two options the brief
offered: a free-text `when` cannot be checked by a program, and guessing which
sentence fits a record is the error the rule exists to prevent.

## Measured effect

Run on 11 November 2026 on copies of the small files of the ten released collections
(registry snapshots of that day; the reviewed map held the five entries it ships with:
scikit-learn, NumPy, pandas, R and UMAP, the last ambiguous). Resolved means a tier
other than `unknown`; skill citations are the `used_by_skills` links of the records.

| Collection | Records | Resolved | reviewed | Bioconductor | Bioconda | CRAN | PyPI | bio.tools | Unknown | Tiers of resolved | Skill citations covered |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| proteomics | 163 | 22 | 4 | 4 | 1 | 2 | 1 | 10 | 141 | noncommercial 1, open 21 | 460/1920 (24.0%) |
| genomics | 867 | 192 | 5 | 10 | 131 | 14 | 3 | 29 | 675 | noncommercial 1, open 191 | 4605/12412 (37.1%) |
| metagenomics | 717 | 171 | 4 | 7 | 96 | 13 | 5 | 46 | 546 | noncommercial 2, open 169 | 4189/10314 (40.6%) |
| metabarcoding | 203 | 31 | 4 | 2 | 20 | 2 | 0 | 3 | 172 | open 31 | 889/3053 (29.1%) |
| multi-omics | 211 | 28 | 5 | 6 | 7 | 6 | 0 | 4 | 183 | open 28 | 797/3040 (26.2%) |
| astronomy | 415 | 17 | 5 | 0 | 0 | 0 | 11 | 1 | 398 | open 17 | 597/5845 (10.2%) |
| agentic-ai | 215 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | 210 | open 5 | 69/2813 (2.5%) |
| transcriptomics | 2086 | 423 | 6 | 83 | 115 | 86 | 43 | 90 | 1663 | noncommercial 1, open 422 | 19447/46090 (42.2%) |
| epigenomics | 532 | 104 | 6 | 18 | 22 | 11 | 1 | 46 | 428 | open 104 | 3258/8510 (38.3%) |
| metabolomics | 1989 | 259 | 6 | 44 | 64 | 49 | 23 | 73 | 1730 | noncommercial 4, open 255 | 13120/39075 (33.6%) |
| total | 7398 | 1252 | 49 | 174 | 456 | 183 | 88 | 302 | 6146 | noncommercial 9, open 1243 | 47431/133072 (35.6%) |

Of the 1,150 records the previous resolver resolved, 546 are still resolved (517 with
the same licence and source, 16 with the licence string now read correctly, such as
`GPL-3.0` becoming `GPL-3.0-only` or `GPL`, and 13 from another source, among them
UMAP from the reviewed map) and 604 are withheld:

| Reason | Records |
|---|---:|
| distinctive name, no corroboration in the record's evidence | 362 |
| short or English-word name, no corroboration | 206 |
| Bioconductor data, annotation or workflow package | 17 |
| curated registry outside the life-science collections | 10 |
| licence string unread (`Artistic-2.0 + file LICENSE`, `Custom OSS`) | 6 |
| a general registry and a same-name package declare different licences | 2 |
| reviewed map: the name means the mappability tool here (`Umap`, genomics) | 1 |

Most of the 568 identity withdrawals are probably correct tools whose records carry
too little text to corroborate them (bedtools, Bowtie, Trimmomatic, sambamba in some
collections); they are the price of refusing CoLoRMap and DiSCo, which a name-only
acceptance resolved to the wrong package, and MetAlign, metid and EPIC, which an overlap
of one generic word did. The reviewed map is the route
back for the most cited of them. Without the reviewed exclusions of
`tool_registries.yaml`, the rule refuses all five of them on its own.

Across the ten collections, every entity (one `license_evidence` address) carries one
licence (`scripts/check_tool_licence_consistency.py`); three names resolve to two
entities in different collections: `plotly` (CRAN in metabolomics, PyPI elsewhere, by
the code each record shows), and `OrthoFinder` and `Racon` (Bioconda in one collection,
bio.tools in another, with the same licence).

Network: two requests to Bioconductor (r-universe, a three-record probe and the bulk
list, 2.4 MB), one to CRAN (`packages.rds`, 12.8 MB), the Bioconda `channeldata.json` reused from the run of the
same day, 144 PyPI requests (124 answers, 20 not found, 23.0 MB) and 1,502 bio.tools
requests (56.5 MB), every answer cached. No request was refused.

## Second pass: the subject of the paper, and the repository's own licence

A hand check of the resolved records found two further errors.

An import name is not a distribution name. The VEGA paper's `import vega` resolved to
PyPI's `vega` (a Jupyter widget) and STEM's `from STEM.model import *` to PyPI's `stem`
(a Tor controller). When a record shows that the tool is the subject of its citing
paper (a source repository named after the tool, or a title opening with it), a
package is now accepted only if it declares that repository or lists that paper.
Bioconductor is exempt when the repository has the same name or none is declared,
because its packages move between accounts. Against the run with the lead's reviewed
map of 143 entries, the rule withholds 16 earlier resolutions: PyPI 11 (VEGA, STEM,
SIMILE, candl, gallifrey, GWpy, ctmm, gssnng, MaCroDNA, SenePy, DeepRTAlign), Bioconda 3
(fpa, VirSorter, Leafcutter) and CRAN 2 (LUCIDus, Mpath). GWpy is probably a false refusal:
its paper cites GitHub and PyPI declares GitLab under the same owner and name.

A registry licence string is often not the tool's. Every registry resolution with a
GitHub or GitLab repository is now checked against that repository's licence file,
with what the file may change set by who wrote the registry entry (table in
`governance/LICENSE_TIERS.md`). On the ten collections (registry snapshots and raw
files of 11 November 2026):

| Source | Confirmed | Replaced | Withheld, contradiction | Kept without confirmation | Withheld, unconfirmed |
|---|---:|---:|---:|---:|---:|
| Bioconductor | 110 | 0 | 0 | 40 | 0 |
| CRAN | 93 | 0 | 0 | 34 | 0 |
| PyPI | 52 | 3 | 1 | 10 | 0 |
| Bioconda | 286 | 7 | 0 | 0 | 75 |
| bio.tools | 239 | 16 | 0 | 0 | 47 |

Resolutions went from 1,633 to 1,492 and skill citations covered from 49.4% to 47.3%.
Three replacements change the tier from `open` to `noncommercial` (medaka, MINI-EX,
REDItools); the other 23 stay `open`. MassCube is withheld because PyPI says CC-BY-NC-4.0 and the
repository Apache-2.0. Network for the pass: 1,807 raw GitHub requests (801 files,
1,006 not found, 7.6 MB), one GitLab request and 45 bio.tools requests, every answer
cached, none refused.

## Limits

- The domain signal was measured on 94 metabolomics matches. The filters added
  here (specific words, collection and registry shares) were set by inspecting the
  ten collections, not on a held-out labelled set; the hand-checked sample of 120
  is the test of them.
- The English-word list is Webster's Second International (1934) intersected with
  the registry names; it holds rare words (`limma`), which only costs coverage.
- Code evidence is read from the record's spans and the citing skills'
  descriptions. A skill that describes two tools may lend one tool's code to the
  other; the ecosystem contradiction rule refuses such a match when the code names
  the other ecosystem, but not when it names the same one.
- PyPI and CRAN are consulted only with code or repository evidence, so the most
  cited general-purpose libraries resolve only through the reviewed map.
- The repository read of `derive_license_tiers.py` (`classify_license_text`,
  `r_license_aliases`) still maps bare `GPL` to GPL-3.0 for corpus papers' own
  repositories. The tool resolver no longer uses it.
