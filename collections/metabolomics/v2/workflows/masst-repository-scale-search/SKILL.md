---
name: masst-repository-scale-search-workflow
description: 'Use when you have a spectrum or feature of interest and want to know
  where else it occurs across all public metabolomics data — query preparation, repository-scale
  fastMASST search, specialized microbe/plant/food MASST for ecological context, and
  co-occurrence analysis.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 4
  member_skills:
  - usi-spectrum-retrieval-and-loading
  - spectral-data-loading-from-repository
  - usi-namespace-parsing
  - usi-string-parsing-and-resolution
  - usi-spectrum-identifier-encoding
  - spectral-database-query-execution
  - spectral-match-result-consolidation
  - mass-spectrometry-database-search
  - mass-spectrometry-reference-database-integration
  - spectral-match-interpretation
  - domain-specific-spectrum-search-implementation
  - masst-output-visualization
  - multi-domain-search-result-aggregation
  - metadata-harmonization-across-sources
  - metabolite-metadata-integration
  - sample-centric-metabolite-annotation
  - tandem-mass-spectrometry-metadata-standardization
  - ms-ms-spectral-library-matching
  - compound-database-matching
  member_tools:
  - spectrum_utils
  - Python
  - matplotlib
  - GNPS public library
  - ProteomeXchange (PXD datasets)
  - MASST
  - GNPS
  - MASST+
  - CLUSTERING+
  - PAIRING+
  - microbeMASST
  - metadataMASST
  - GNPS_MASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - MZmine
  - msFeaST
  - pandas
  - jupyter-notebook
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# MASST Repository-Scale Spectral Search (Reverse Metabolomics)

## Summary

End-to-end reverse metabolomics: take one molecule and find its public-dataset footprint with MASST, then add ecological context and co-occurrence interpretation.


## When to use

Use when you have a spectrum or feature of interest and want to know where else it occurs across all public metabolomics data — query preparation, repository-scale fastMASST search, specialized microbe/plant/food MASST for ecological context, and co-occurrence analysis.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — spectrum_prep

**Goal:** prepare a query MS/MS spectrum / USI for search

**EDAM operation:** operation_3215

**Inputs:** mgf · **Outputs:** tsv

**Candidate leaf skills:** `usi-spectrum-retrieval-and-loading` (primary), `spectral-data-loading-from-repository`, `usi-namespace-parsing`, `usi-string-parsing-and-resolution`, `usi-spectrum-identifier-encoding`

**Tools (primary):** spectrum_utils, Python, matplotlib, GNPS public library, ProteomeXchange (PXD datasets)

**Other candidate tools:** NumPy, GNPS Molecular Networking, MassBank, MetaboLights, Metabolomics Workbench, MS2LDA, GNPS Spectral Libraries, ProteoXchange Repository, QR Code Generation Library, USI Resolver and Displayer

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.9b04884, 10.1101/2020.05.09.086066

### Stage 2 — masst_search

**Goal:** repository-scale spectral search (fastMASST)

**EDAM operation:** operation_3631

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `spectral-database-query-execution` (primary), `spectral-match-result-consolidation`, `mass-spectrometry-database-search`, `mass-spectrometry-reference-database-integration`, `spectral-match-interpretation`

**Tools (primary):** MASST, GNPS, MASST+, CLUSTERING+, PAIRING+

**Other candidate tools:** metadataMASST, microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, Fast Search API, GNPS_MASST, GNPS Molecular Networking, MZmine

**Grounding:** 3 KB(s); DOIs: 10.1038/s41538-022-00137-3, 10.1038/s41564-023-01575-9, 10.1038/s41587-023-01985-4

### Stage 3 — specialized_masst  [OPTIONAL]

**Goal:** (optional) ecological context via microbe/plant/food MASST

**EDAM operation:** operation_3631

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `domain-specific-spectrum-search-implementation` (primary), `masst-output-visualization`, `multi-domain-search-result-aggregation`, `metadata-harmonization-across-sources`

**Tools (primary):** microbeMASST, metadataMASST, GNPS_MASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, Fast Search API, MZmine


**Grounding:** 2 KB(s); DOIs: 10.1038/s41538-022-00137-3, 10.1038/s41564-023-01575-9

### Stage 4 — cooccurrence

**Goal:** co-occurrence / reverse-metabolomics interpretation

**EDAM operation:** operation_3659

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-metadata-integration` (primary), `sample-centric-metabolite-annotation`, `tandem-mass-spectrometry-metadata-standardization`, `ms-ms-spectral-library-matching`, `compound-database-matching`

**Tools (primary):** msFeaST, pandas, jupyter-notebook

**Other candidate tools:** ENPKG, MZmine, enpkg_mn_isdb_taxo, enpkg_sirius_canopus, enpkg_meta_analysis, SIRIUS, Open Tree of Life, Wikidata, NPClassifier, ChEMBL, matchms, pubchempy, RDKit, Python, masscube, TandemMatch, Mirador, PeakQC, Spectra, MetFrag, R, PubChem, COCONUT

**Grounding:** 6 KB(s); DOIs: 10.1021/acscentsci.3c00800, 10.1021/jasms.4c00146, 10.1038/s41467-025-60640-5, 10.1093/bioinformatics/btae584 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
