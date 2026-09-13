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

### Changed
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
- Vendor the `asb-contribute` feedback helper with its standalone shared PII configuration so installed units can run it without repository gate dependencies.

### Added
- Shared index-closure and helper-containment checks for shipped units, with
  an offline CLI and release-gate integration across every declared helper.

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
