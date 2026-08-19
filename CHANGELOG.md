# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

This repo ships **two** things on **two** tag schemes, both noted per release:
- the **Python distribution** `asb-skill-collections` (the `asbb` CLI + `asb-mcp`
  server) — tagged `vX.Y.Z`, published to PyPI;
- the **skill collections** (e.g. metabolomics) — tagged `<slug>-v<N>`, deposited
  to Zenodo / HuggingFace.

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
- **pip-installable `asb-skill-collections` package** (wheel ~108 KB) and
  `publish-pypi.yml` (PyPI Trusted Publishing, no stored token).
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
