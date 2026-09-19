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

### Fixed
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
