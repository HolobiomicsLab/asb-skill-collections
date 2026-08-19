---
name: ms2lda-substructure-discovery-workflow
description: 'Use when you want to discover shared substructures (Mass2Motifs) across
  a corpus of MS2 spectra via LDA topic modeling — convert MS/MS spectra into a bag-of-fragments
  document corpus, run MS2LDA (Latent Dirichlet Allocation) to infer recurring fragmentation
  motifs, annotate motifs against MotifDB / Spec2Vec embeddings, and map motifs back
  onto molecular-network features for substructure-level annotation of an untargeted
  LC-MS/MS dataset.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - mass-spectrometry-file-format-parsing
  - fragment-ion-peak-detection-and-normalization
  - mass-spectrometry-peak-filtering-and-noise-reduction
  - spectral-noise-filtering-and-artifact-removal
  - spectral-noise-filtering-and-quality-control
  - probabilistic-topic-modeling-mass-spectrometry
  - mass2motif-parameter-optimization
  - lda-model-training-convergence
  - latent-dirichlet-allocation-topic-inference
  - mass-binning-and-tokenization-for-topic-modeling
  - mass2motif-annotation-guidance-via-spectral-embeddings
  - motifdb-reference-library-querying
  - mass2motif-annotation-mapping
  - spectral-similarity-scoring-and-ranking
  - motif-metadata-annotation
  - mass2motif-substructure-mapping
  - ms2lda-motif-to-network-mapping
  - molecular-network-annotation-integration
  - mass-spectral-network-annotation
  - substructure-annotation-integration
  - json-structured-report-generation
  - mass2motif-network-construction
  - ms2lda-motif-mapping
  - ms2lda-substructure-assignment
  member_tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - MS2LDA.Preprocessing.generate_corpus
  - ProteoWizard Library and Tools
  - pwiz
  - Latent Dirichlet Allocation (LDA)
  - Spec2Vec
  - MAG
  - MotifDB
  - MassQL
  - LDA (Latent Dirichlet Allocation)
  - pyMolNetEnhancer
  - RMolNetEnhancer
  - GNPS
  - Cytoscape
  - MAG (Automated Mass2Motif Annotation Guidance)
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

# MS2LDA Substructure Discovery (MS2 corpus -> Mass2Motifs -> network-mapped substructures)

## Summary

MS2 spectra in, substructure-annotated features out: bag-of-fragments corpus construction, MS2LDA topic modeling into Mass2Motifs, motif annotation against MotifDB/Spec2Vec, and propagation of motif labels onto a GNPS molecular network.


## When to use

Use when you want to discover shared substructures (Mass2Motifs) across a corpus of MS2 spectra via LDA topic modeling — convert MS/MS spectra into a bag-of-fragments document corpus, run MS2LDA (Latent Dirichlet Allocation) to infer recurring fragmentation motifs, annotate motifs against MotifDB / Spec2Vec embeddings, and map motifs back onto molecular-network features for substructure-level annotation of an untargeted LC-MS/MS dataset.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw MS2 spectra (mgf/mzML/msp) -> cleaned, intensity-normalized bag-of-fragments corpus

**EDAM operation:** operation_3632

**Inputs:** mgf, mzML · **Outputs:** corpus-json

**Candidate leaf skills:** `mass-spectrometry-file-format-parsing` (primary), `fragment-ion-peak-detection-and-normalization`, `mass-spectrometry-peak-filtering-and-noise-reduction`, `spectral-noise-filtering-and-artifact-removal`, `spectral-noise-filtering-and-quality-control`

**Tools (primary):** MS2LDA, MS2LDA.Preprocessing.load_and_clean, Python, Conda, MS2LDA.Preprocessing.generate_corpus, ProteoWizard Library and Tools, pwiz


**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jproteome.9b00640, 10.1073/pnas.1608041113

### Stage 2 — lda_modeling

**Goal:** bag-of-fragments corpus -> Mass2Motifs (LDA topic model over spectral documents)

**EDAM operation:** operation_3644

**Inputs:** corpus-json · **Outputs:** motifset-json

**Candidate leaf skills:** `probabilistic-topic-modeling-mass-spectrometry` (primary), `mass2motif-parameter-optimization`, `lda-model-training-convergence`, `latent-dirichlet-allocation-topic-inference`, `mass-binning-and-tokenization-for-topic-modeling`

**Tools (primary):** MS2LDA, Latent Dirichlet Allocation (LDA), Python, Spec2Vec

**Other candidate tools:** MS2LDA.modeling, MotifDB, MS2LDA.Preprocessing.load_and_clean, Conda, MS2LDA.Preprocessing.generate_corpus

**Grounding:** 1 KB(s); DOIs: 10.1073/pnas.1608041113

### Stage 3 — motif_annotation

**Goal:** Mass2Motifs -> putative substructure annotations (MotifDB + Spec2Vec embedding match)

**EDAM operation:** operation_3629

**Inputs:** motifset-json · **Outputs:** annotated-motifset-json

**Candidate leaf skills:** `mass2motif-annotation-guidance-via-spectral-embeddings` (primary), `motifdb-reference-library-querying`, `mass2motif-annotation-mapping`, `spectral-similarity-scoring-and-ranking`, `motif-metadata-annotation`

**Tools (primary):** MS2LDA, MAG, Python, Spec2Vec, MotifDB, MassQL, LDA (Latent Dirichlet Allocation)

**Other candidate tools:** MAG (Automated Mass2Motif Annotation Guidance), MAG (Mass2Motif Annotation Guidance), MS2LDAViz

**Grounding:** 2 KB(s); DOIs: 10.1073/pnas.1608041113, 10.5281/zenodo.15688609

### Stage 4 — network_mapping

**Goal:** annotated Mass2Motifs + GNPS molecular network -> motif-enriched network nodes

**EDAM operation:** operation_3778

**Inputs:** annotated-motifset-json, mgf/gnps-fbmn · **Outputs:** graphml

**Candidate leaf skills:** `mass2motif-substructure-mapping` (primary), `ms2lda-motif-to-network-mapping`, `molecular-network-annotation-integration`, `mass-spectral-network-annotation`, `substructure-annotation-integration`

**Tools (primary):** pyMolNetEnhancer, Python, RMolNetEnhancer, GNPS, MS2LDA, Cytoscape

**Other candidate tools:** MS2LDA (ms2lda.org)

**Grounding:** 1 KB(s); DOIs: 10.3390/metabo9070144

### Stage 5 — report

**Goal:** consolidate motifs + annotations + motif-enriched network into a substructure discovery report

**EDAM operation:** operation_3434

**Inputs:** annotated-motifset-json, graphml · **Outputs:** tsv

**Candidate leaf skills:** `json-structured-report-generation` (primary), `mass2motif-network-construction`, `ms2lda-motif-mapping`, `ms2lda-substructure-assignment`

**Tools (primary):** MS2LDA, MAG, Python, MAG (Automated Mass2Motif Annotation Guidance), Spec2Vec, MotifDB

**Other candidate tools:** Latent Dirichlet Allocation (LDA), pyMolNetEnhancer, RMolNetEnhancer, GNPS, Cytoscape

**Grounding:** 2 KB(s); DOIs: 10.1073/pnas.1608041113, 10.3390/metabo9070144

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
