---
name: feature-based-molecular-networking-and-propagation-workflow
description: 'Use when you have untargeted LC-MS/MS MS2 data and want to spread a
  handful of confident annotations across whole molecular families — build a feature-based
  molecular network, seed it with spectral-library and SIRIUS/CANOPUS annotations,
  then propagate compound classes and analogue annotations across network components
  (MolNetEnhancer / network annotation propagation) so unannotated nodes inherit chemically-plausible
  identities.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 6
  member_skills:
  - peak-detection-and-mass-alignment
  - cross-sample-feature-alignment
  - lcms-peak-detection-and-alignment
  - spectral-feature-table-generation
  - mass-spectrometry-feature-detection-validation
  - spectral-similarity-network-generation
  - molecular-family-graph-construction
  - metabolomic-spectral-annotation-and-molecular-family-clustering
  - molecular-family-grouping-analysis
  - metabolomic-molecular-family-networking-gnps
  - spectral-library-matching-annotation
  - spectral-library-matching
  - spectral-library-molecular-networking
  - mass-spectrometry-library-ranking
  - chemical-ontology-mapping
  - spectral-feature-chemical-assignment
  - consensus-classification-reconciliation
  - structural-annotation-integration
  - chemical-classification-scheme-validation
  - graph-based-feature-annotation
  - chemical-class-metadata-integration
  - molecular-network-node-annotation
  - molecular-network-attribute-enrichment
  - molecular-network-annotation-integration
  - feature-metadata-annotation
  - feature-consolidation-across-batches
  - untargeted-metabolomics-dataset-integration
  - lcms-feature-table-construction
  - feature-annotation-consolidation
  member_tools:
  - MZmine2
  - Optimus
  - OpenMS
  - GNPS
  - Cytoscape
  - MSThunder
  - Windows
  - MSConvert
  - SIRIUS
  - NPClassifier
  - CANOPUS
  - ClassyFire
  - ConCISE
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - MS2LDA
  - msFeaST
  - jupyter-notebook
  - msFeaST Dashboard bundle
  coverage_gaps: []
  derived_from_workflows:
  - coll_molnetenhancer
  - coll_npclassscore_cq
  - spec2vec_grounded
  - coll_ms2deepscore
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Feature-Based Molecular Networking with Annotation Propagation

## Summary

MS2 in, a network-propagated annotation table out: molecular networking, seed annotation, chemical-class assignment, and topology-driven propagation of annotations and classes across molecular families.


## When to use

Use when you have untargeted LC-MS/MS MS2 data and want to spread a handful of confident annotations across whole molecular families — build a feature-based molecular network, seed it with spectral-library and SIRIUS/CANOPUS annotations, then propagate compound classes and analogue annotations across network components (MolNetEnhancer / network annotation propagation) so unannotated nodes inherit chemically-plausible identities.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw mzML -> aligned feature table + MS2 exports (GNPS-FBMN mgf + SIRIUS mgf)

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf/gnps-fbmn, mgf/sirius

**Candidate leaf skills:** `peak-detection-and-mass-alignment` (primary), `cross-sample-feature-alignment`, `lcms-peak-detection-and-alignment`, `spectral-feature-table-generation`, `mass-spectrometry-feature-detection-validation`

**Tools (primary):** MZmine2, Optimus, OpenMS

**Other candidate tools:** ISFrag, R, XCMS, CAMERA, JPA, MS-Convert, mzRAPP, MZmine 2, enviPat, Skyline, R (with mzRAPP library)

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.1c01644, 10.1021/acs.jnatprod.7b00737, 10.1093/bioinformatics/btab231/6214530, 10.3390/metabo12030212

### Stage 2 — network

**Goal:** MS2 spectra -> molecular family graph (modified cosine; GNPS-style components)

**EDAM operation:** operation_3214

**Inputs:** mgf/gnps-fbmn · **Outputs:** graphml, tsv

**Candidate leaf skills:** `spectral-similarity-network-generation` (primary), `molecular-family-graph-construction`, `metabolomic-spectral-annotation-and-molecular-family-clustering`, `molecular-family-grouping-analysis`, `metabolomic-molecular-family-networking-gnps`

**Tools (primary):** MZmine2, Optimus, GNPS, Cytoscape

**Other candidate tools:** nplinker, Python, pytest, antiSMASH, BiG-SCAPE, MIBiG, MS2LDA, PALS (Pathway Activity Level Scoring), GNPS (Global Natural Products Social Molecular Networking), MS2LDA (Mass2Motif Latent Dirichlet Allocation), PALS Viewer, conda, pip, BigScape

**Grounding:** 6 KB(s); DOIs: 10.1021/acs.jnatprod.7b00737, 10.1101/2024.10.11.617756, 10.1186/1471-2105-6-225, 10.1186/s40168-022-01444-3 …

### Stage 3 — seed_annotate

**Goal:** MS2 spectra -> seed spectral-library annotations to propagate from

**EDAM operation:** operation_3631

**Inputs:** mgf/gnps-fbmn · **Outputs:** tsv

**Candidate leaf skills:** `spectral-library-matching-annotation` (primary), `spectral-library-matching`, `spectral-library-molecular-networking`, `mass-spectrometry-library-ranking`

**Tools (primary):** MSThunder, Windows, GNPS, MSConvert

**Other candidate tools:** microbeMASST, metadataMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, GNPS_MASST, GNPS libraries, Fast Search API, MZmine, MASSBANK, DrugBANK, meRgeION2, RChemMass, MS2Compound, CFM-id, mssearchr, R, NIST API, MSHub, Python, Anaconda, Git, MSBERT, PyTorch, matchms, Spec2Vec

**Grounding:** 7 KB(s); DOIs: 10.1016/j.enceco.2025.07.022, 10.1021/acs.analchem.2c04343, 10.1021/acs.analchem.4c02426, 10.1021/jasms.5c00322 …

### Stage 4 — class_annotate

**Goal:** MS2 spectra -> molecular formula + chemical class (SIRIUS / CANOPUS / NPClassifier)

**EDAM operation:** operation_3860

**Inputs:** mgf/sirius · **Outputs:** tsv

**Candidate leaf skills:** `chemical-ontology-mapping` (primary), `spectral-feature-chemical-assignment`, `consensus-classification-reconciliation`, `structural-annotation-integration`, `chemical-classification-scheme-validation`

**Tools (primary):** SIRIUS, NPClassifier, GNPS, CANOPUS, ClassyFire, ConCISE

**Other candidate tools:** Fiehn Labs ClassyFire Batch

**Grounding:** 1 KB(s); DOIs: 10.3390/metabo12121275

### Stage 5 — propagate

**Goal:** spread seed annotations + chemical classes across molecular families

**EDAM operation:** operation_3434

**Inputs:** graphml, tsv, tsv · **Outputs:** tsv

**Candidate leaf skills:** `graph-based-feature-annotation` (primary), `chemical-class-metadata-integration`, `molecular-network-node-annotation`, `molecular-network-attribute-enrichment`, `molecular-network-annotation-integration`

**Tools (primary):** pyMolNetEnhancer, Python, RMolNetEnhancer, GNPS, MS2LDA, Cytoscape

**Other candidate tools:** ms2lda.org, MS2LDA (ms2lda.org)

**Grounding:** 1 KB(s); DOIs: 10.3390/metabo9070144

### Stage 6 — consolidate

**Goal:** consolidate network family + seed + class + propagated annotations into one table

**EDAM operation:** operation_3434

**Inputs:** feature-table, graphml, tsv · **Outputs:** tsv

**Candidate leaf skills:** `feature-metadata-annotation` (primary), `feature-consolidation-across-batches`, `untargeted-metabolomics-dataset-integration`, `lcms-feature-table-construction`, `feature-annotation-consolidation`

**Tools (primary):** msFeaST, jupyter-notebook, msFeaST Dashboard bundle

**Other candidate tools:** R (>=), LargeMetabo, R, Matlab, M2S, Centwave, FeatureFinderMetabo, ADAP, ProteoWizard, MsFeatures, xcms, faahKO

**Grounding:** 5 KB(s); DOIs: 10.1021/ac051437y, 10.1021/acs.analchem.1c02687, 10.1021/acs.analchem.1c03592, 10.1093/bib/bbac455 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
