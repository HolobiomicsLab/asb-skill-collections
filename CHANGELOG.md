# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

This repo ships **two** things on **two** tag schemes, both noted per release:
- the **Python distribution** `asb-skill-collections` (the `asbb` CLI + `asb-mcp`
  server) — tagged `vX.Y.Z`, installed from a checkout in v0 and published to
  PyPI from v1 (design decision 5: the CLI without the corpus it reads is not a
  working install);
- the **skill collections** (e.g. metabolomics) — tagged `<slug>-v<N>`, deposited
  to Zenodo / HuggingFace.

## [Unreleased]

### Added
- Build-capsules deposit path, `scripts/capsules_deposit.py`: `refresh` rewrites the
  descriptive files of an existing pack against the collection as it is now and copies the
  build zips after checking their size and sha256; `archive` writes one deterministic zip per
  record with the build zips stored unchanged, since Zenodo accepts at most 100 files per
  record by default; `plan` checks the pack offline and writes `deposit-plan.json`, refusing a
  screen failure or deny hit on a zipped build, a zip that disagrees with `MANIFEST.json`, a
  build that is not an included paper of the collection, metadata the deposit API would reject,
  creators that differ from the release list, a stale collection DOI, a private repository URL
  and a local path; `create` makes a first-release draft from the owner's terminal and never
  publishes and records the draft beside the plan so a rerun refuses unless `--again` is
  given; `record-doi` (with `--published`) writes an optional `capsules` block on the released version's row of
  `collections.yaml`, which `check_collections_manifest.py` validates, `regen_catalogue.py`
  carries as `capsules_doi`, the documentation site and the README collections table show, and a
  later patch release keeps. No capsules record is published.
- Four contribution routes at the point of use (INT-ASB-051, lot A): this skill is wrong
  or could be better; a skill is missing: request it, or propose yours; a paper is not
  referenced: propose it; something technical failed: report it. Each lands on the issue
  tracker of this public registry, since the domain repositories are private. The issue
  chooser gains `config.yml` (blank issues kept, links to the contribute and paper pages and
  to the security policy) and puts the four routes first: `1-skill-feedback.md` and
  `3-propose-paper.md` (renamed from `skill-feedback.md` and `propose-paper.md`), and two new
  templates, `2-request-skill.md` and `4-technical-fault.md`. `scripts/skill_feedback.py`
  holds one closed list of kinds (`defect`, `drift`, `enhancement`, `efficiency`, `gap`,
  `composition`; the earlier site kinds are read as these) and one set of labels
  (`usage-feedback`, `needs-triage`, `propose` for new work, `auto-report` when a script or a
  form drafted it), used by `scripts/make_improvement_report.py`, the templates and the site,
  and renders the paper and technical-fault routes. `scripts/router_shape.py` renders a
  `## Report and contribute` section in the router and the workflow router of a generated
  collection, naming the collection, and can ship `bin/report_issue.py`,
  a standard-library helper generated from `skill_feedback.py` and `pii_config.py`
  (`--sync-report-helper`) that prints the redacted report and a bounded prefilled address
  and never posts. `asbb report <route>` runs the same helper. An empty search names routes
  2 and 3. The site's paper form writes the fields `scripts/intake_issue.py` reads and offers
  only the released collections, with no default. `scripts/check_release_surface.py` and
  `router_shape.py --check` reject a stale contribution section and accept a router without
  one, so the ten released collections pass unchanged. `.github/CONTRIBUTING.md`, `README.md`,
  `AGENTS.md`, `CLAUDE.md` and `docs/CONTRIBUTION_LOOP.md` name the four routes; texts that sent
  the public to a domain repository or to Discussions are corrected.
- Tool licence resolution fit to ship (INT-ASB-050). `scripts/resolve_tool_licenses.py`
  now judges every registry match per record, in its collection, from the record's own
  evidence (`scripts/tool_identity.py`): a short or English-word name, a match outside the
  life-science collections, and any match in CRAN, PyPI or bio.tools need corroboration
  (the package's repository, a shared DOI, or `library(x)` / `import x` style use), and a
  silent name match is no longer identity. Licence strings are read by
  `scripts/tool_licence_text.py` with the R `DESCRIPTION` grammar and an explicit table,
  never inventing a version and never reading a non-commercial licence as open.
  `governance/tool_licences_reviewed.yaml` is a reviewed map that takes precedence over
  every registry; `governance/tool_name_common_words.txt` lists the English words that are
  also package names. Every resolved record carries `license_evidence`, the address its
  licence was read from. `scripts/check_tool_licence_consistency.py` checks that one entity
  carries one licence across collections. Rule and measured effect:
  `docs/design/tool-licence-resolution-2026-11-11.md`.
- Every registry resolution is checked against the licence file of the repository the
  package declares (`scripts/repository_licence.py`, raw content from GitHub or GitLab,
  never an API), with what the file may change set by who wrote the registry entry.
  A Bioconda or bio.tools licence is replaced by the file (detection
  `repository-licence-file`) and is unknown without one. A PyPI licence is replaced by a
  file of the same tier and withheld against a file of another tier. A Bioconductor or
  CRAN licence is kept and withheld only when the repository DESCRIPTION gives another
  tier. A file that offers a choice of licences is read as an SPDX `OR`. A permissive
  licence file that adds terms of its own is not read as that licence, and a README
  sentence that restricts use of the tool (academic use only, a licence needed for
  industrial use) withholds a record that would otherwise be open. A replacement reads
  only a repository named like the tool, and two GNU statements that differ only in
  version give the unversioned family, as does a third party's version that the
  repository does not state. A package whose registry description restricts use
  (KEGGREST, academic use only) is not matched. The tier map reads a bare `GPL`, `LGPL`
  or `AGPL` as open. When the record shows that the tool is the subject of its citing paper, a
  package must declare that paper's repository: an import name is not a distribution
  name (`import vega` is not PyPI's `vega`).
- Identity and README checks from the fourth audit and the census. Code corroborates a
  package only when it names the package as the registry spells it, and a package that
  adds a separator the record's name lacks (`py-graphviz` against `pygraphviz`) needs
  the repository or the publication. An R package without R code is contradicted when
  the record uses the name as a Python module (MuData). A Bioconductor package that
  declares no repository passes the subject-of-paper rule only when the paper's
  repository holds that R package (MetNet). A README sentence that the tool's code or
  binary is closed-source or under further restrictions withholds (MZA), more wordings
  of academic-only use are read (CalibraCurve), and an R licence field that names
  `file LICENSE` withholds when the file limits the field of use (dsb). The reviewed map
  adds CANOPUS and MSNovelist as SIRIUS web services, noncommercial. SIRIUS, ZODIAC and COSMIC are
  recorded as academic use only in the mass spectrometry collections (AGPL-3.0 text, a licence
  for other users), on the collection owner's reading.
- `enrich_tools_index.py --licence-only` writes the licence fields, `entry_kind`,
  `repo_url`, `source_paper_repos` and `license_evidence` and leaves the skill-tool links
  byte-identical.

### Changed
- `scripts/pack_capsules.py` packs only builds of papers that the released corpus includes and
  lists the others under `not_released` in `MANIFEST.json`. It names the private
  AgenticScienceBuilder pipeline in the record description and links it only with
  `--pipeline-public`. The screen rewrites a GitHub URL of a private repository (the
  pipeline and every registry domain repository) to the bare `owner/name`, counts it as
  `private_urls_rewritten` in `SCREEN.json`, fails a build on a residual one, and fails a JSON
  document that no longer parses. Benchmark rows keep the sorted key order of `capsules.jsonl`.
- `check_tools_index.py` reports resolved and unknown tool counts for each collection,
  fails when a record claims a licence and `tool_licenses.json` is absent, when a registry
  or reviewed tier names no `license_evidence`, and when the tier or address drifts from
  the resolution.
- `repo_url` of an unresolved tool is empty: the collector no longer copies the first
  citing paper's repository into it (it stays in `source_repos`).
- Registry matches that the previous resolver accepted on name alone, such as Bioconda's
  genome mappability `umap` for the dimension-reduction method, Bioconductor's `BERT` for
  the language model and Bioconda's `gambit` for the particle-physics code, are withheld.
- Selector: the package default returns to `asb-keyword` 1.0.0, so
  `asb_skill_collections/asb_skill_index.py`, the script template and the
  released collections carry the same selector. Selector 1.1.0 lost against
  1.0.0 on the 326 benchmark-card labels (expected Hit@1 lower by 0.036 to
  0.080 in the four arms) and on known-item retrieval in eight collections
  (name-query hit@1 0.643 to 0.857 against 0.940 to 0.997). The measurements,
  and the variants that did not beat 1.0.0, are in `docs/selection.md`.
- `scripts/router_shape.py --scripts-only --keep-selector` refreshes the wrapper
  of `bin/search_skills.py` around the selector a unit already ships, so a patch
  release can change what a search prints without changing the ranking of a
  released collection. A semantic wrapper without a marked selector block is
  left as it is instead of stopping the refresh. `docs/selection.md` records the
  known-item check that kept selector 1.0.0 in the released collections.
- Router generator (`scripts/router_shape.py`): the leaf router and the workflow
  router, which now has a generator (`write_workflow_router`), give
  `python3 "${CLAUDE_SKILL_DIR}/../../bin/search_skills.py"` commands that run
  from any directory. Claude Code fills in `${CLAUDE_SKILL_DIR}` with the
  router's absolute directory, so the command runs as printed; the router tells
  a host that leaves the variable to replace it. The leaf router points to the
  workflow and tool searches, offers `--technique` only when the index has
  tags, defines all four licence tiers (`unknown` included), asks for the
  skill's DOI and tier in the answer, and opens its description with the
  domain trigger ("Use for any <domain> how-to question ..., before answering
  from memory"), without workflow slugs.
- Search script template (`scripts/templates/search_skills.py`): a skill hit
  prints its tier and first source DOI on its first line, a tool hit its tier
  and recorded licence; the scoring explanation moves to `--json` only (the
  text output of a ten-hit search halves). A search that matches nothing exits
  0 and says what to try next. Refresh a released tree with
  `python scripts/router_shape.py --scripts-only <collection>` followed by
  `python scripts/router_shape.py --routers-only --rewrite <collection>`; this
  changes `bin/search_skills.py` (its wrapper; the selector stays 1.0.0),
  `skills/_router/SKILL.md` and `workflows/_workflow_router/SKILL.md` only.
  `--routers-only --rewrite` renders both routers of a shaped unit. The released
  collections are unchanged; their routers still print
  `python bin/search_skills.py`, relative to the collection root.
  `AGENTS.md`, `README.md`, `CLAUDE.md` and `docs/partial-install.md` now
  describe the released layout: one advertised router, `bin/search_skills.py`,
  leaves with `provenance.source_papers`, no binder or `commands/` inside a
  collection, receipts under `receipts/<cut-id>/` in the domain repository.
- Complete step 2 of the per-domain split: released content leaves this master,
  which retains the `asb_skill_collections` tooling package, scripts, tests,
  governance, docs-site, catalogue, release registry and validation workflows.
  The legacy epigenomics, transcriptomics and metabolomics v1 trees are recorded
  in `collections.yaml`. Marketplace entries now use `git-subdir` sources in
  `asb-skills-metabolomics`: v3 for the full collection and the v2-derived packs
  at the same pinned commit. The master's former v2 copy had diverged from the
  domain v2 in description wording and `evidence_spans` fields in 5,858 leaves;
  the registry pins the domain copy.
- Move the metabolomics v3 registry row and marketplace pin to
  `metabolomics-v3.0.1` (10.5281/zenodo.24093587). The v3.0.0 deposit
  (10.5281/zenodo.24054446) is listed under `superseded` in that row.
- Describe the ten registered domains in `README.md`, `CLAUDE.md`,
  `CITATION.cff`, `.github/copilot-instructions.md` and the maintainer docs: a
  release table read from `collections.yaml`, and pointers to the registry in
  place of single-release statements.

- Align the contribution, release and intake documents with the ten-domain
  layout: content paths are paths in the domain checkout, the removed tag and
  mirror workflows are marked historical, the release order in
  `docs/domain-onboarding.md` follows `scripts/release_domain.py`, and the
  eight metabolomics pack entries of the marketplace are pinned at the v3.0.1
  commit (the `packs/` tree is byte-identical to the v3.0.0 commit).

### Fixed
- The capsule screen applies the quotation policy to every field that carries text of the
  paper, recognised by its place in the document: quote properties by local name (so
  `asbval:evidence_quote` counts), the items of `passages_used` and `substring_hits`, plain
  evidence snippets, and the paper payload of a dataset preview. Before, six key names and
  Markdown block quotes were covered, and the passages retrieved from papers that are not
  open shipped in the local packs. Text is kept, capped under one budget per DOI across the
  members of a build, or removed with an anchor; a second pass reads the output and leaves out
  a build that holds text it should not. Full retention is for CC-BY, CC-BY-SA, CC0 and public
  domain; the NC and ND variants of Creative Commons are capped (a prefix test gave them
  full retention). A drive letter counts as a path only before a home directory, which stops
  the rewrite of mathematics such as `X:\mathbb`.
- Capsule tables and guides say what the files hold. The validation label is derived from the
  claim entries and lowered when the summary of `validation.json` disagrees, which the row
  states. The evaluation listing is described as structurally complete definitions, not as
  runnable benchmarks, and carries checks by kind, unresolved references and input assets
  with a hash or a download hint. Each entry of `artifact_provenance.json` says whether its
  file ships. `build_manifest.json` drops the branch name and dirty flag of its Git entries.
  The record README and the pack README gain a field dictionary generated from one table,
  the screen counters, the licence layers and the citation; the dataset card has no
  placeholder and takes `--capsules-doi`.
- Build-capsules records now describe only what they hold. `capsules.jsonl`, its optional
  Parquet twin and `benchmark-manifest.json` exclude builds without a zip; the manifest and
  deposit plan distinguish considered, packed and left-out builds and capsules; `plan`
  refuses stale table rows; and its uploaded README describes the public record instead of
  the local pack. Capsule metadata expresses the public tooling repository as a
  `references` related identifier, and Zenodo metadata validation checks the list shapes
  accepted by the deposit API.
- The capsule screen (`scripts/capsule_screen.py`) rewrites and checks JSON, JSONL, JSON-LD
  and YAML documents on their decoded strings (values and mapping keys) and serializes them
  afterwards. Run on the serialized text, an email match took the `n` of a `\n` escape, a
  path match took the backslash of a `\"` escape or ran through a `\n` into the next line,
  and a drive pattern matched serialization artefacts such as a YAML line continuation after
  `r:` or an escaped `b:\"`; builds were left out as `invalid_json_after_rewrite` or
  `residual_paths_rewritten`. Markdown, plain text, CSV and TSV are still screened as text,
  and deny-list patterns are still counted on the final text. A YAML document whose comments
  hold something to screen is serialized rather than kept.
- The capsule screen redacts a phone-shaped number only with a cue (an international
  prefix, a parenthesised area code that is not a year, or a telephone or fax label shortly
  before it). The earlier rule redacted any three digit groups separated by a space, a dot
  or a hyphen, which replaced masses, axis ticks and parts of identifiers in the packs;
  right after a label, groupings the earlier shape missed (`04 92 07 61 00`) are now covered.
- The path rule of the capsule screen is stated once. A machine path is a root marker
  followed by path characters; `/home/`, `/root/` and `/tmp/` count only where an absolute
  path starts (`test/tmp/` is left alone, `-I/home/...` is rewritten), and `/home/` and
  `/root/` are new in the rule. The residual check stays wider than the rewrite, so a root
  marker the rewrite cannot handle leaves the build out, but it no longer fails on a mention
  that ends at the marker (`in the /tmp/ directory`) or on a placeholder
  (`/tmp/<name>`). YAML sets, ordered pairs and binary values are screened or checked, and two
  keys that become the same key once screened fail the document.
- Bind `nhs_number` to its label like the other clinical identifiers, treat a
  bounded set of documented template e-mail local parts (`your@…`,
  `firstname.lastname@…`) as notation, and add an exact, per-pattern allowlist
  for documented example values (the two canonical SSN placeholders) and
  owner-read spans (one de-identified public-dataset sample label, decision of
  2026-10-29). The candidate gates of 2026-09-20 had stopped transcriptomics,
  epigenomics, agentic-ai and proteomics on `pii_dual_use` for a Bloom-filter
  bit budget, two benchmark-table cells, a README usage line and a paper's own
  example record. `pii_config` moves to `2026-10-29.1`; the four domains re-run
  through the strict gate with it pass (`release_verified: true`, cut ids
  unchanged: `c0107b2c545e`, `576c19e25af0`, `d7359e4dd5f0`, `b5a519a80508`).

### Added
- Record the releases of agentic-ai, astronomy, genomics, metabarcoding,
  metagenomics, multi-omics and proteomics (v1) and of epigenomics and
  transcriptomics (v2) in `collections.yaml`, each with its domain concept DOI,
  version DOI, commit and tree digest, and add a marketplace entry for each,
  pinned to its registry commit. The epigenomics and transcriptomics v1 trees
  stay as legacy rows.
- Add an optional explicit build root to the cut collector and pass the candidate driver's build root through to it.
- Add the deterministic S6 same-paper duplicate report and S4–S6 candidate assembly driver with pinned source, stage and output receipts.
- Add the S8 local candidate landing command with verified-gate preconditions, candidate branches and non-release marketplace metadata.
- Let S8 append candidates to tracked marketplaces that already list released collection versions, with rollback-safe restoration.
- Add the deterministic S3 cut-to-candidate collector, its release-creators
  source, and a public-safe three-output fixture with policy-aligned quote
  trimming and router-shaped output tests.
- Add the deterministic S4 corpus-record join and Decision 7 P1 access map,
  with duplicate and unmatched receipts plus fixture coverage.
- Add the deterministic S5 index bootstrap and six-check candidate gate runner,
  with stamped indexes, retained check output and fixture coverage.
- Add the data-driven release-surface check (`scripts/check_release_surface.py`,
  rules in `scripts/release_surface_rules.yaml`: the sentences retracted on 2026-09-13 and
  the metabolomics/v2 identifiers, P6) as the seventh candidate check of the gate runner.
- Ship an RO-Crate with every released capsule and make `validate.yml` gate 8
  blocking. The 417 capsules of `metabolomics/v1`, `epigenomics/v1` and
  `transcriptomics/v1` now carry the `ro-crate-metadata.json` their build wrote,
  imported only from a build whose shipped files are byte-identical
  (`release_capsule_truth.py --import-crates-from`) and pruned to what the capsule
  holds: entities for files promotion left behind are dropped with their
  references, every held file is described and listed in `hasPart`, and 12,425
  absolute `/outputs/` paths become `urn:asb:build:` locators. The build crates
  claim Workflow Run Profile 0.5 without its `mainEntity`, so the release copy
  keeps only the RO-Crate 1.1 claim. Promotion keeps and prunes the crate, and
  gate 8 holds each capsule to `crate_problems`, failing on any problem and on
  finding no released capsule rather than passing over zero files. The crates add
  23 MB uncompressed, 1.9 MB compressed.
- Let `asbb install` take a selection of skills in place of a pack name (#70):
  `--skills slug[,slug...]`, `--skills-file` (one slug per line) or
  `--query TEXT --top N`, which reuses the offline selector of `asbb search`.
  The pack build derives the selection with a slug list as membership and
  installs it as a managed unit named by `--name` or
  `<collection>-subset-<8 hex digits>`; uninstall and `--dry-run` work as for
  packs. Measured on 2026-10-31 with `HOME` in a temporary directory, a 10-skill
  selection writes 20 files and 145,561 bytes (the install receipt records the
  destination path, so the total varies with the length of `HOME`).
  `docs/partial-install.md` gives the full collection (6,870 files) and the
  lc-ms pack (2,627 files) measured the same way. `build_packs --check` still
  reports 0 of the 8 declared packs differing.
- Add `asbb fetch`, which downloads chosen leaves from GitHub at a ref without a
  checkout, checks them against the remote `skills_index.json`, prints each
  licence tier and writes `PROVENANCE.json` with the URL and SHA-256 of every
  file; a ref with a `..` segment is refused before any network read (#70).
  Tests: 15 in `tests/test_asbb_subset.py`, 12 in `tests/test_asbb_fetch.py`
  and one more in `tests/test_build_packs.py`.
- Add `scripts/zenodo_deposit.py` (#69). It builds a deterministic release zip
  of a collection, prints the deposit plan offline and creates a new-version
  draft on Zenodo that keeps the metadata the draft inherits. It never calls the
  publish action; publishing stays a manual step. Tokens are read from
  `ZENODO_TOKEN` or `ZENODO_SANDBOX_TOKEN` and never printed.
  `docs/RELEASE_DEPOSIT.md` gives the procedure; 36 tests in
  `tests/test_zenodo_deposit.py`.
- Add `assets/brand/`: the ASB logo in nine files (light and dark logo, mark,
  wordmark, favicon, collections lockup, a 512 px PNG) with `BRAND.md` (#68).
- Add `docs/STATUS.md`, which keeps the verification caveats of the previous
  README grouped by surface with their last-verified dates (#68).

### Changed
- Make CI gate 1 (LinkML) blocking once its schema is resolvable. It now
  validates every `collection.yaml` closed against `SkillCollection` in
  `asb-schema` >= 0.3.0, the first version that declares the ten keys the
  released manifests carry, and it runs outside `continue-on-error`. While that
  package is not installable, or an older one resolves, the step says it did not
  run and exits 0. The four released manifests validate against a locally built
  0.3.0 wheel; `asb-schema` is not on PyPI yet, so CI still reports that the gate
  did not run.
- Make `router` the default offline selector rule and give it a relevance-bearing
  tie-break inside an equal-score block: candidates are ordered by how many query
  terms reached their `name`, then by how much of the `name` those terms are,
  with slug then collection as the deterministic fallback. On 326 benchmark-card
  labels `router` leads the previous `package` default by +0.126 Hit@1 on the
  5,859-row corpus under a relevance-neutral tie policy (95% CI
  [+0.070, +0.182]), and the title tie-break adds a further +0.019 there and
  +0.041 on the 1,478-row installed unit while cutting the rank-1 tie rate from
  51.2% to 12.6% and from 47.2% to 7.7% respectively. `package` stays available
  for one release via `--selector package` / `ASB_SELECTOR_RULE=package` and
  keeps its historical score/slug order unchanged. See `docs/selection.md`.
- Restructure the README (395 to 235 lines) around install, use, contents,
  citation and governance (#68). Private companion repositories are named
  without links, and links to the private AgenticScienceBuilder repository are
  removed from the README, `docs/REGISTRY.md`, the metabolomics v2 `ABOUT.md`
  and `.zenodo.json`, `CITATION.cff` and `pyproject.toml`.
  `scripts/check_advertised_counts.py` reports 139 advertised count claims
  matching the on-disk census.

### Fixed
- Recover missing leaf DOI provenance from the canonical build manifest without replacing DOI provenance already present in the leaf.
- Raise the content gate policy to 1.3: strict verbatim caps now use only known
  paper-text licence evidence; tool-subject and unknown text licences follow
  access-only caps, with the unknown class reported separately.
- Make the release gate own and fully account for evidence-quote parsing,
  including colon-bearing labels, multiline blocks and embedded quotes; apply
  verbatim caps to every non-text-reuse-permissive DOI (licence tier, else
  `access.source_reuse`, else the paper licence the v1 corpora record under
  `access.license`) with normalized DOI identity; distinguish Git SSH and
  R-slot syntax from real email addresses (a two-letter last label is always
  an email); propagate the `unknown` licence tier without collapsing or
  raising; and refresh the vendored `pii_config.py` of metabolomics v2.
- Make generated skill descriptions and routers carry their unit's own contract:
  approved description openings are normalised without duplication, domain
  wording comes from the collection slug (or stays neutral), and router apply /
  grounding instructions describe sampled leaf metadata and only the grounding
  assets that the unit ships, while the released v2 router remains byte-stable.
- Scope all 16,583 validation assertion IDs in the three v1 collections to
  their source paper, preserving each existing local suffix. The 82 indicium
  records now use `asbval:assertion/paper/<URL-escaped DOI>/<local suffix>`;
  all IDs are distinct across records. Source identity comes from the exact
  workflow/build provenance join for 78 records and four caller-confirmed paper
  DOIs, using ASB's production normalization and scope helpers. Assertion
  contents, serialization and the 24 records without assertions are unchanged.
  `scripts/migrate_v1_assertion_ids.py` reproduces the migration, the three
  receipts are regenerated, and `tests/test_v1_assertion_ids.py` guards source
  identity and uniqueness. Supply the four confirmed metabolomics identities
  with repeated `--confirmed-doi COLLECTION/RECORD=DOI` arguments:
  `metabolomics/featurefindermetab=10.1074/mcp.m113.031278`,
  `metabolomics/mzmine2=10.1186/1471-2105-11-395`,
  `metabolomics/np_analyst=10.1021/acscentsci.1c01108`, and
  `metabolomics/sirius=10.1038/s41592-019-0344-8`.
- Name real ontology terms in the 16,583 validation assertions of the three v1
  collections (82 `indicium/*.jsonld` files: 14,912 `ClaimAssessment`, 1,374
  `SkillTriageAssertion`, 297 `ScopeDriftAssertion`). They carried
  `sepio:credibility_status` with SEPIO_0000338–0000341 and 0000301–0000303, and
  `eco:evidence_type`; in the SEPIO release of 2023-06-13 none of those codes is a
  status (0000340 is an annotation property, the others do not exist), so every
  such triple expanded to an IRI no ontology defines. Each record now carries
  `sepio:0000183` (evidence direction) — 0000403 supporting, 0000404 disputing,
  0000405 inconclusive — and claim assessments `ro:0002558` (has evidence) with
  ECO_0000501 (evidence used in automatic assertion); the context declares `ro`.
  The direction is derived from the verdict each record already held
  (`asbval:supported_raw`, `asbval:triage_status`), which stays unchanged, and all
  16,583 legacy codes agreed with it. `partial` and uncertain verdicts both map to
  inconclusive. This matches ASB's validation bridge 0.2.0. The three receipts are
  regenerated and verify; `metabolomics/v2` carries no such records.
  `tests/test_v1_validation_assertion_terms.py` holds the records to the terms.
- Record `collection_dir` and `corpus_path` in `gate_report.json` relative to the
  checkout that holds the collection, not as absolute paths. The receipt ships inside
  the collection, so the four regenerated receipts published the gate machine's home
  directory and worktree name, including in `collections/metabolomics/v2`, whose tree
  on `main` carried no such path. Verification never reads either field. The four
  receipts are regenerated and verify; `tests/test_release_gate_recorded_paths.py`
  holds the rule and the shipped receipts to it.
- Derive the collection's grounding map through the rule its packs already use.
  `kb_bundle.json` feeds `perspicacite_kb_bind.py`, which clones every `repo_urls`
  entry; the entries came from tool records that held the repository of *some*
  paper citing the tool (issue #42). The unit builder was fixed and never run over
  the collection, so the release was about to ship two answers: the `metabolomics`
  plugin and the technique packs handing different repositories for one identical
  skill. Re-derived over all 5,859 skills: 306 → 360 distinct repositories, 16,768
  → 6,110 pointers, and skills with no repository 316 → 15. First, three papers
  whose `corpus.yaml` row carried `repo_url: ''` are recorded, which is what keeps
  55 skills from emptying — `10.1186/s13321-020-00449-0` (rMSIcleanup),
  `10.1021/acs.jproteome.5c00435` (mzPeak) and `10.1186/s13321-023-00738-4`
  (DeepSAT), all three Crossref-verified against public repositories. The 15 that
  remain empty are one paper, `BitterMasS`, for which no public repository was
  found; an honest absence rather than another paper's code.
- Write unit `plugin.json` the way the tree carries it. The bundle writer was
  corrected to `ensure_ascii=False`; the manifest writer three lines below it was
  not, so it escaped the em dash and `Perspicacité` in every description it wrote.
  The eight advertised technique packs have shipped `\u2014` / `\u00e9` in their
  marketplace descriptions since packaged grounding landed, `origin/main` included.
  Both writers now agree with the tree, and the nine manifests are re-encoded — the
  documents parse identically either way, so no description changes.
- Bind a payload file whose name happens to be `__pycache__`. The receipt skipped
  any path with that name in any component, which is right for a cache directory
  and wrong for a regular file: such a file would ship unbound, outside the
  receipt, for the sake of its name. The skip now matches cache directories and
  their contents only. No tracked path is affected today — the hole was
  theoretical — and it rides with the regeneration the two items above require
  rather than costing a fourth receipt rewrite of its own.
- Ship the link-only grounding guard the repository has carried since
  2026-06-23. `bin/perspicacite_kb_bind.py` is a build-time copy of
  `scripts/perspicacite_kb_bind.py` and is the file an installed unit actually
  runs; nothing compared the two. `5f79a87db` added `link_only` /
  `build_local_manifest`, which refuse to embed a `noncommercial` or
  `restricted` skill's sources and return a link-only manifest instead, and
  re-vendored none of the nine copies. All nine — the collection and the eight
  packs — still shipped the pre-guard binder, which clones every `repo_urls`
  entry unconditionally, while 1,440 of the collection's 5,859 bundle records
  (1,279 `restricted`, 161 `noncommercial`) now carry the `license_tier` the
  guard reads. The copies are refreshed and a test compares every vendored copy
  that shares a filename with a repository source — the binder and
  `scripts/pii_config.py` today — so a helper change can no longer land in the
  repository without reaching the consumer. Unit assets authored in place are
  outside it: `bin/search_skills.py` and `bin/semantic_search.py` are generated
  by `scripts/router_shape.py`, and `workflows/bin/semantic_search.py` is the
  historical copy `docs/selection.md` documents as outside that unification.
- Stop erasing the repository of a skill that has no papers. `resolve_repo_urls`
  exists so a skill is never handed another paper's repository (issue #42), and
  it derives from the skill's DOIs — which leaves a skill with no DOIs with
  nothing. The corpus has one, `masster` (`provenance_tier: repository`), whose
  declared repository is its own source and not somebody else's; deriving the
  `lc-ms` pack in R7 both added that leaf to the pack for the first time and
  shipped it with an empty grounding map. A record with no papers now keeps its
  declared `repo_urls`; a record with papers is still re-derived and its declared
  list still ignored.
- Write unit `kb_bundle.json` the way every other producer writes it.
  `build_grounding_bundle.py` used the `json.dumps` default `ensure_ascii=True`
  while `build_packs.py` and `skill_index.py` write `ensure_ascii=False`, so
  running the repository's own `scripts/build_all_grounding.sh` over a tree
  another producer had written re-escaped every non-ASCII tool name — 85 rows
  across six packs, changing no content.
- An installed unit that is moved on disk stays usable and stays removable. Every
  bound entry now names its asset root relative to its own directory alongside the
  absolute path, and its documented first step resolves from the entry rather than
  from a path fixed at install time. `uninstall --dest` and `install --dest`
  naming the new location recognise the moved unit as the same unit instead of
  refusing it, so removal no longer requires aiming an uninstall at a directory
  that no longer exists — which emptied the manifest and orphaned the copy.
- Remove twelve stale rows from four technique packs' skill indexes and KB
  bundles, using their declared v2 parent index; correct the pack table and
  router count metadata without changing leaves.
- Re-derive the eight technique packs from `collections/metabolomics/v2` instead
  of carrying the hand-made 2026-06-22 split forward. The packs were internally
  consistent with their own indexes and had drifted from the collection: the
  `masster` leaf added the next day never reached `lc-ms` (2,616 of 2,617 LC-MS
  skills, and six sites advertising the lower number while the collection
  advertised the higher one for the same technique); `provenance_tier`,
  `tool_license` and `grounding_tier` were absent from all 4,949 copied leaves,
  and `provenance_tier`, `grounding_tier` and `tools_used` from every row of
  both pack indexes; and the packaged grounding map still pointed at
  repositories belonging to other papers (issue #42), fixed in the unit builder
  and never re-run over the packs. Pack leaves are now byte copies of the
  collection leaf of the same slug and both indexes are the collection's own
  rows filtered to the pack's members.
- Stop advertising a LinkML gate that has never run. `validate.yml` gate 1 called
  `linkml-validate --schema asb_skill_bundle.yaml`, a file that ships in the
  sibling `asb-schema` package and exists nowhere in this repository, so every
  run printed `FAIL: LinkML validation failures` once per collection and exited
  1 — and `continue-on-error: true` turned that into a green Validate. Measured
  on the last green run on `main` (2026-09-05): four failures, all
  `File 'asb_skill_bundle.yaml' does not exist`, job conclusion `success`. The
  step now resolves its schema (checkout, then an installed `asb-schema`),
  checks that the `linkml-validate` CLI is on PATH, and emits a `::warning::`
  saying `GATE 1 DID NOT RUN` instead of failing where nobody looks.
  `docs/REGISTRY.md`, `docs/RELEASE_TRAIN_v0.md` — which listed the gate as
  blocking — the PR template and `governance/CONTENT_POLICY.md` no longer
  assert that `collection.yaml` is schema-validated. Against `asb-schema` v0.2
  the four manifests carry seven fields its `SkillCollection` class does not
  declare (ten for `metabolomics/v2`) and no missing required slot, so turning
  the gate on is a schema decision for the maintainers, not a switch.
- Say what the RO-Crate gate measured. No collection ships an
  `ro-crate-metadata.json`, so `validate.yml` gate 8 validated zero files and
  printed `PASS: RO-Crate validation OK (0 crates checked)` — which reads in the
  PR checks exactly like an enforced gate that passed, and it is
  `continue-on-error` besides. It now emits a `::warning::` and says it did not
  run, the way gate 9 already does, and `docs/REGISTRY.md`,
  `docs/RELEASE_TRAIN_v0.md`, the PR template and `governance/CONTENT_POLICY.md`
  no longer assert that a crate is present and valid. The `ro_crate_path` field
  itself is dropped from all four manifests and from the generator that wrote it
  unconditionally: a manifest a consumer reads should not name a file the release
  does not ship, and the schema `asb_skill_collection.yaml` declares the slot
  optional, so nothing requires it. Shipping real crates would make gate 8
  enforceable and is v1 work. The gate's own warning is corrected with the field:
  it told the reader that four manifests still declared `ro_crate_path`, which
  stopped being true in the same change that dropped them.
- Make a promoted capsule's own documents describe the capsule, not the build.
  Dropping `ro_crate_path` from the manifests left the same claim standing one
  layer down, in the two documents a consumer actually opens. 417 benchmark cards
  ended with "See the `ro-crate-metadata.json` in this capsule for full
  provenance" (336 in `metabolomics/v1`, 44 in `epigenomics/v1`, 37 in
  `transcriptomics/v1`) and the release ships exactly 417 capsules, none of which
  contains that file. The obvious repair — point the card at
  `artifact_provenance.json`, which every capsule does carry — was measured before
  it was taken, and it was not enough: those 417 manifests were promoted from the
  build unchanged and declared **2,085 artefact paths of which 0 existed** in the
  released capsule, so the redirect would have landed on a dead index. ASB's own
  `validate_capsule_provenance` reports each of them as a dangling path; it had
  never been run against a promoted collection. Both documents are now re-stated
  against what the release carries: the card links to the capsule's provenance
  file (417 of 417 links resolve), and the manifest lists the artefacts that are
  present, every file the capsule holds, and — rather than silently dropping them
  — the build artefacts the release does not promote. The rule lives in one place
  (`scripts/release_capsule_truth.py`), `scripts/promote_benchmark_layer.py`
  applies it while promoting so the next run cannot undo it, and a new
  `validate.yml` gate holds the tree to it. `metabolomics/v2`, the public
  collection, ships no capsules and is unchanged. Generating real crates (the
  option that would make gate 8 enforceable) remains v1 work.
- Stop binding compiled-bytecode caches into a release receipt. The gate
  snapshots the tree it finds on disk, so the two `__pycache__` files that
  running `collections/metabolomics/v2/bin/`'s own search scripts leaves behind
  were bound as if the release shipped them. Measured on the shipped tree: a
  strict run passed here and bound three cache entries, and that receipt then
  failed `--verify` against `git archive` of the same commit — the state of
  every checkout and of the Zenodo deposition. The receipt now records the
  release rather than the machine that generated it, and a consumer who runs
  the collection's scripts no longer invalidates their own receipt.
- Aim the licence and provenance tier gates at the packs as well as the
  collection. `check_license_tiers` read `corpus.yaml` unconditionally and so
  raised `FileNotFoundError` on every pack, which is why the tiers a consumer
  installs were never checked; a pack ships no corpus of its own, and its pass
  line now says so rather than reporting a half-run gate as OK.
- Vendor the `asb-contribute` feedback helper with its standalone shared PII configuration so installed units can run it without repository gate dependencies.

### Added
- Shared index-closure and helper-containment checks for shipped units, with
  an offline CLI and release-gate integration across every declared helper.
- `packs/<domain>/packs.yaml` (schema `asb-pack-map/1.0`) declares pack
  membership as data: one technique tag per pack, selecting
  `tag in skills_index[slug].techniques`. Nothing recorded this before.
- `scripts/build_packs.py` re-derives every declared pack from that map, with
  `--check` (report drift, write nothing) and `--dry-run`. `build(build(t))`
  equals `build(t)`; `bin/`, `commands/`, `skills/`, `.claude-plugin/` and
  `GROUNDING.md` are not touched.
- A pack-to-collection check in `scripts/unit_closure.py`, reading the
  generator's own rule and comparison so the gate cannot pass a tree the
  generator would change. It reports a selected leaf the pack does not ship, a
  shipped leaf the rule does not select, and a copy whose bytes are not its
  original's, naming the front-matter key when one was lost. Index closure alone
  stays green on a pack that lost a leaf and pruned its own rows. Wired into the
  release gate and into CI.
- CI now runs the existing advertised-count guard over the repository. It would
  not have caught the stale LC-MS count — the pack really did hold 2,616 leaves
  — but it is what keeps the six corrected sites honest now that the derivation
  gate makes the two numbers one number.

## [Patch releases of the ten collections] - 2026-11-10

Each released collection has a patch release: `v1.0.1` for agentic-ai, astronomy,
genomics, metabarcoding, metagenomics, multi-omics and proteomics, `v2.0.1` for
epigenomics and transcriptomics, `v3.0.2` for metabolomics. Each is a new version
of the Zenodo record of its collection (the concept DOI is unchanged) and becomes
the current row of `collections.yaml`; the replaced release is listed under
`superseded` in that row.

What changes in a collection: the leaf router and the workflow router give search
commands that run from any directory and say when to use them, and
`bin/search_skills.py` prints the licence tier and the source DOI of each hit.
The ranking is the one each collection was released with (selector 1.0.0). Skill,
tool, workflow and paper counts are unchanged.

| Domain | Release | Version DOI |
|---|---|---|
| agentic-ai | `agentic-ai-v1.0.1` | [10.5281/zenodo.24122112](https://doi.org/10.5281/zenodo.24122112) |
| astronomy | `astronomy-v1.0.1` | [10.5281/zenodo.24122111](https://doi.org/10.5281/zenodo.24122111) |
| epigenomics | `epigenomics-v2.0.1` | [10.5281/zenodo.24122116](https://doi.org/10.5281/zenodo.24122116) |
| genomics | `genomics-v1.0.1` | [10.5281/zenodo.24122105](https://doi.org/10.5281/zenodo.24122105) |
| metabarcoding | `metabarcoding-v1.0.1` | [10.5281/zenodo.24122109](https://doi.org/10.5281/zenodo.24122109) |
| metabolomics | `metabolomics-v3.0.2` | [10.5281/zenodo.24122117](https://doi.org/10.5281/zenodo.24122117) |
| metagenomics | `metagenomics-v1.0.1` | [10.5281/zenodo.24122106](https://doi.org/10.5281/zenodo.24122106) |
| multi-omics | `multi-omics-v1.0.1` | [10.5281/zenodo.24122110](https://doi.org/10.5281/zenodo.24122110) |
| proteomics | `proteomics-v1.0.1` | [10.5281/zenodo.24122102](https://doi.org/10.5281/zenodo.24122102) |
| transcriptomics | `transcriptomics-v2.0.1` | [10.5281/zenodo.24122113](https://doi.org/10.5281/zenodo.24122113) |

## [agentic-ai-v1.0.0] - 2026-11-09

Release of the agentic-ai collection (v1) from the private domain repository
`asb-skills-agentic-ai`, deposited as
[10.5281/zenodo.24093110](https://doi.org/10.5281/zenodo.24093110) (concept DOI
10.5281/zenodo.24093109). 668 skills, 215 tools, 2 workflows
and 29 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [astronomy-v1.0.0] - 2026-11-09

Release of the astronomy collection (v1) from the private domain repository
`asb-skills-astronomy`, deposited as
[10.5281/zenodo.24093095](https://doi.org/10.5281/zenodo.24093095) (concept DOI
10.5281/zenodo.24093094). 1,671 skills, 415 tools, 2 workflows
and 100 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [epigenomics-v2.0.0] - 2026-11-09

Release of the epigenomics collection (v2) from the private domain repository
`asb-skills-epigenomics`, deposited as
[10.5281/zenodo.24093107](https://doi.org/10.5281/zenodo.24093107) (concept DOI
10.5281/zenodo.24093106). 2,295 skills, 532 tools, 2 workflows
and 92 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [genomics-v1.0.0] - 2026-11-09

Release of the genomics collection (v1) from the private domain repository
`asb-skills-genomics`, deposited as
[10.5281/zenodo.24093085](https://doi.org/10.5281/zenodo.24093085) (concept DOI
10.5281/zenodo.24093084). 3,246 skills, 867 tools, 2 workflows
and 137 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [metabarcoding-v1.0.0] - 2026-11-09

Release of the metabarcoding collection (v1) from the private domain repository
`asb-skills-metabarcoding`, deposited as
[10.5281/zenodo.24093089](https://doi.org/10.5281/zenodo.24093089) (concept DOI
10.5281/zenodo.24093088). 803 skills, 203 tools, 2 workflows
and 29 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [metagenomics-v1.0.0] - 2026-11-09

Release of the metagenomics collection (v1) from the private domain repository
`asb-skills-metagenomics`, deposited as
[10.5281/zenodo.24093087](https://doi.org/10.5281/zenodo.24093087) (concept DOI
10.5281/zenodo.24093086). 2,754 skills, 717 tools, 2 workflows
and 117 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [multi-omics-v1.0.0] - 2026-11-09

Release of the multi-omics collection (v1) from the private domain repository
`asb-skills-multi-omics`, deposited as
[10.5281/zenodo.24093092](https://doi.org/10.5281/zenodo.24093092) (concept DOI
10.5281/zenodo.24093090). 787 skills, 211 tools, 2 workflows
and 29 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [proteomics-v1.0.0] - 2026-11-09

Release of the proteomics collection (v1) from the private domain repository
`asb-skills-proteomics`, deposited as
[10.5281/zenodo.24093114](https://doi.org/10.5281/zenodo.24093114) (concept DOI
10.5281/zenodo.24093113). 558 skills, 163 tools, 2 workflows
and 28 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [transcriptomics-v2.0.0] - 2026-11-09

Release of the transcriptomics collection (v2) from the private domain repository
`asb-skills-transcriptomics`, deposited as
[10.5281/zenodo.24093100](https://doi.org/10.5281/zenodo.24093100) (concept DOI
10.5281/zenodo.24093099). 11,256 skills, 2,086 tools, 2 workflows
and 450 papers. The registry row in `collections.yaml` pins the commit and tree digest.

## [metabolomics-v3.0.1] - 2026-11-09

Patch release of metabolomics v3, published from the domain repository
`HolobiomicsLab/asb-skills-metabolomics` as
[10.5281/zenodo.24093587](https://doi.org/10.5281/zenodo.24093587). It keeps the
collection path `collections/metabolomics/v3` and replaces v3.0.0 as the v3 row
of `collections.yaml`.

It remaps EDAM operation and topic annotations (tier T2), adds EDAM topic facets
and the technique tags CE-MS and direct infusion. The counts are unchanged:
11,830 skills, 1,989 tools, 20 workflows, 477 papers.

## [metabolomics-v3.0.0] — 2026-11-09

Consolidated rebuild on the class-A pipeline: **11,830 skills** across **1,989
tools**, distilled from **477 published method papers (journal articles and
preprints)**, with **20 composite workflows** recomposed from the v2 collection.
The release was published from the domain repository
`HolobiomicsLab/asb-skills-metabolomics` as
[10.5281/zenodo.24054446](https://doi.org/10.5281/zenodo.24054446).

## [0.2.0] — 2026-06-29

First release of the installable tooling and of composite workflow super-skills.
Dates finalize at tag time.

### Added
- **21 composite workflow super-skills** in `metabolomics/v2` (e.g.
  `untargeted-lcmsms-annotation`, `lipidomics-lcms-annotation`,
  `sirius-denovo-structure-elucidation`, `pathway-functional-analysis`), each a
  DAG of leaf skills grounded in 3–8 source DOIs, with a `_workflow_router`.
- **`asbb` CLI** — offline, key-free `search` / `get` over a checkout or
  `ASB_COLLECTIONS_ROOT` (`--target skills|workflows|tools`).
- **`asb-mcp` MCP skill-server** — `search`/`get` for skills, workflows, and
  tools from any MCP agent (behind the `[mcp]` extra).
- **Installable `asb-skill-collections` package** — `uv pip install -e .` from a
  checkout — and a dormant `publish-pypi.yml` (PyPI Trusted Publishing, no stored
  token) held back to v1.
- **Leaf embedding-cache builder** for semantic search, shipped via the release
  deposition.
- **Repository-OA tier** documented in governance (`repo-oa` / `repo-permissive`
  / `repo-copyleft`): software tools are admitted on the openness of their code
  repository, not the paper's reuse license.
- **`docs/NEXT_WAVE.md`** — backlog for the next ASB generation wave.

### Changed
- Metabolomics `v2` corpus: **5,866 → 5,859 skills** — purged 7 over-aggregated
  "meta-leaf" artifacts (>25 tools each); added a >25-tools-per-leaf guard to
  prevent reintroduction.
- Distributed package reorganized: the installable surface moved
  `scripts/` → `asb_skill_collections/`. `scripts/` keeps the path-invoked CI/dev
  tools (not distributed).
- Releases now mint a **new version under a stable Zenodo concept-DOI** instead of
  a fresh concept-DOI each time.

### Fixed
- Skill-frontmatter parser dropped any skill whose evidence spans contained a
  `---` line; **recovered 2 skills**.
- sdist no longer bundles the full skill corpus (**37 MB → ~108 KB**).
- Improvement-report anonymizer: bounded the email regex (ReDoS on long inputs)
  and closed a secret-leak for underscore-glued key names.
