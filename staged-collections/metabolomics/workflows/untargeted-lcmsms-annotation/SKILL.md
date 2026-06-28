---
name: untargeted-lcmsms-annotation-workflow
description: 'Use when you have untargeted LC-MS/MS data (mzML) and want an annotated
  feature table — preprocessing, blank/QC filtering, feature-based molecular networking,
  spectral library matching, SIRIUS de novo annotation, optional taxonomy-aware re-weighting,
  and a fused master table. This is the canonical metabopipe-style annotation pipeline.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 7
  member_skills:
  - peak-detection-and-mass-alignment
  - mass-spectrometry-feature-detection-validation
  - lcms-peak-detection-and-alignment
  - spectral-feature-table-generation
  - cross-sample-feature-alignment
  - blank-sample-feature-filtering
  - feature-table-blank-intensity-detection
  - background-ion-contaminant-removal
  - feature-table-quality-control
  - background-ion-blank-comparison
  - molecular-networking-construction
  - molecular-family-graph-construction
  - spectral-similarity-network-generation
  - spectral-library-molecular-networking
  - gnps-molecular-network-integration
  - graph-based-metabolite-similarity-assessment
  - spectral-library-matching-annotation
  - spectral-library-matching
  - spectral-library-matching-with-cosine-similarity
  - mass-spectrometry-library-ranking
  - spectral-library-annotation-matching
  - sirius-spectral-request-construction
  - web-service-api-integration
  - spectrum-query-formatting
  - spectral-fingerprint-web-service-query
  - molecular-fingerprint-parsing
  - taxonomic-weighting-in-annotation
  - metabolite-annotation-taxonomic-integration
  - metabolite-annotation-scoring
  - metabolite-annotation-network-architecture
  - feature-metadata-annotation
  - feature-network-construction-from-mass-spectrometry
  - sample-centric-metabolite-annotation
  - feature-table-consensus-aggregation
  - unannotated-feature-characterization
  - feature-table-integration-and-normalization
  member_tools:
  - MZmine2
  - Optimus
  - OpenMS
  - R
  - MZmine3
  - Jupyter Notebook
  - FBMN-STATS
  - ENPKG
  - MZmine
  - MEMO
  - MSThunder
  - Windows
  - GNPS
  - MSConvert
  - CSI:FingerID
  - SIRIUS
  - CANOPUS
  - Docker
  - tima (Taxonomically Informed Metabolite Annotation)
  - LOTUS
  - GNPS-FBMN
  - msFeaST
  - jupyter-notebook
  - msFeaST Dashboard bundle
  coverage_gaps: []
  derived_from_workflows:
  - coll_ms2deepscore
  - coll_ramclust_cq
  - coll_xcms_cq
  - coll_inventa_cq
  - coll_nmr2struct
  - spec2vec_grounded
  - spec2vec_pkg_oalarge
  - coll_bioactivity_based_molecular_networking_cq
  - coll_concise_cq
  - coll_redu_cq
  - coll_deepmsprofiler_cq
  - coll_cardinal_cq
  - coll_dures_cq
  - coll_fbmn_stats_cq
  - coll_idsl_ipa_cq
  - coll_metabodirect
  - coll_multiomicsintegrator_cq
  - coll_peakqc_cq
  - coll_tardis
  - coll_vimms
  - coll_lipidin_cq
  - coll_molnetenhancer
  - coll_ms2rescore_immunopeptidome_rescoring_cq
  - coll_npclassscore_cq
  - coll_rapidmass_cq
  - coll_tardis_cq
  - coll_esp_cq
  - coll_graphormer_rt_cq
  - coll_lipidmatch_cq
  - coll_corems
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Untargeted LC-MS/MS Metabolomite Annotation (FBMN + SIRIUS)

## Summary

End-to-end untargeted LC-MS/MS annotation: raw mzML in, an evidence-grounded master feature table out, combining molecular networking, library matching and SIRIUS.


## When to use

Use when you have untargeted LC-MS/MS data (mzML) and want an annotated feature table — preprocessing, blank/QC filtering, feature-based molecular networking, spectral library matching, SIRIUS de novo annotation, optional taxonomy-aware re-weighting, and a fused master table. This is the canonical metabopipe-style annotation pipeline.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw mzML -> aligned feature table + MS2 exports (GNPS-FBMN mgf + SIRIUS mgf)

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf/gnps-fbmn, mgf/sirius

**Candidate leaf skills:** `peak-detection-and-mass-alignment` (primary), `mass-spectrometry-feature-detection-validation`, `lcms-peak-detection-and-alignment`, `spectral-feature-table-generation`, `cross-sample-feature-alignment`

**Tools (primary):** MZmine2, Optimus, OpenMS

**Other candidate tools:** mzRAPP, MZmine 2, R, XCMS, enviPat, Skyline, R (with mzRAPP library), ISFrag, CAMERA, JPA, MS-Convert

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.1c01644, 10.1021/acs.jnatprod.7b00737, 10.1093/bioinformatics/btab231/6214530, 10.3390/metabo12030212

### Stage 2 — qc_filter  [OPTIONAL]

**Goal:** (optional) remove blank / background / low-quality features before annotation

**EDAM operation:** operation_3695

**Inputs:** feature-table · **Outputs:** feature-table

**Candidate leaf skills:** `blank-sample-feature-filtering` (primary), `feature-table-blank-intensity-detection`, `background-ion-contaminant-removal`, `feature-table-quality-control`, `background-ion-blank-comparison`

**Tools (primary):** R, MZmine3, Jupyter Notebook, FBMN-STATS

**Other candidate tools:** ThermoRawFileParser, Python, PCPFM (Python-Centric Pipeline for Metabolomics), Asari, GetFeatistics, XCMS, MS-Dial, metDataModel

**Grounding:** 3 KB(s); DOIs: 10.1038/s41596-024-01046-3, 10.1371/journal.pcbi.1011912, 10.1515/jib-2025-0047

### Stage 3 — network

**Goal:** MS2 spectra -> molecular family graph (modified cosine; GNPS-style components)

**EDAM operation:** operation_3214

**Inputs:** mgf/gnps-fbmn · **Outputs:** graphml, tsv

**Candidate leaf skills:** `molecular-networking-construction` (primary), `molecular-family-graph-construction`, `spectral-similarity-network-generation`, `spectral-library-molecular-networking`, `gnps-molecular-network-integration`, `graph-based-metabolite-similarity-assessment`

**Tools (primary):** ENPKG, MZmine, MEMO

**Other candidate tools:** nplinker, Python, pytest, GNPS, MZmine2, Optimus, Cytoscape, MSHub, mineMS2, igraph, R, MSnbase

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.jnatprod.7b00737, 10.1021/acscentsci.3c00800, 10.1038/s41587-020-0700-3, 10.1186/s13321-025-01051-y …

### Stage 4 — library_match

**Goal:** MS2 spectra -> spectral library annotations (cosine match to reference libraries)

**EDAM operation:** operation_3631

**Inputs:** mgf/gnps-fbmn · **Outputs:** tsv

**Candidate leaf skills:** `spectral-library-matching-annotation` (primary), `spectral-library-matching`, `spectral-library-matching-with-cosine-similarity`, `mass-spectrometry-library-ranking`, `spectral-library-annotation-matching`

**Tools (primary):** MSThunder, Windows, GNPS, MSConvert

**Other candidate tools:** microbeMASST, metadataMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, GNPS_MASST, GNPS libraries, Fast Search API, MZmine, MASSBANK, DrugBANK, meRgeION2, RChemMass, MS2Compound, CFM-id, mssearchr, R, NIST API, ANN-SoLo, Python, Anaconda, Git, MSBERT, PyTorch, matchms, Spec2Vec, nplinker, pytest

**Grounding:** 8 KB(s); DOIs: 10.1016/j.enceco.2025.07.022, 10.1021/acs.analchem.2c04343, 10.1021/acs.analchem.4c02426, 10.1021/acs.jproteome.8b00359 …

### Stage 5 — sirius

**Goal:** MS2 spectra -> formula + structure + class (SIRIUS / CSI:FingerID / CANOPUS)

**EDAM operation:** operation_3860

**Inputs:** mgf/sirius · **Outputs:** tsv

**Candidate leaf skills:** `sirius-spectral-request-construction` (primary), `web-service-api-integration`, `spectrum-query-formatting`, `spectral-fingerprint-web-service-query`, `molecular-fingerprint-parsing`

**Tools (primary):** CSI:FingerID, SIRIUS, CANOPUS

**Other candidate tools:** MSNovelist, ClassyFire

**Grounding:** 1 KB(s); DOIs: 10.1038/s41587-021-01045-9

### Stage 6 — taxonomy_propagate  [OPTIONAL]

**Goal:** (optional) taxonomy-aware re-weighting / propagation of annotations

**EDAM operation:** —

**Inputs:** tsv, tsv, metadata · **Outputs:** tsv

**Candidate leaf skills:** `taxonomic-weighting-in-annotation` (primary), `metabolite-annotation-taxonomic-integration`, `metabolite-annotation-scoring`, `metabolite-annotation-network-architecture`

**Tools (primary):** R, Docker, tima (Taxonomically Informed Metabolite Annotation), LOTUS, SIRIUS, GNPS-FBMN

**Other candidate tools:** tima (R package), GNPS, Spectra (R package), MrnAnnoAlgo3 (MetDNA3), MrnAnnoAlgo3, MetDNA3

**Grounding:** 4 KB(s); DOIs: 10.1038/nbt.3597, 10.1038/s41467-025-63536-6, 10.1038/s41592-019-0344-8, 10.3389/fpls.2019.01329

### Stage 7 — fusion

**Goal:** consolidate networking + library + SIRIUS (+ taxonomy) into one master table

**EDAM operation:** operation_3434

**Inputs:** feature-table, graphml, tsv · **Outputs:** tsv

**Candidate leaf skills:** `feature-metadata-annotation` (primary), `feature-network-construction-from-mass-spectrometry`, `sample-centric-metabolite-annotation`, `feature-table-consensus-aggregation`, `unannotated-feature-characterization`, `feature-table-integration-and-normalization`

**Tools (primary):** msFeaST, jupyter-notebook, msFeaST Dashboard bundle

**Other candidate tools:** networkx, treelib, mass2chem, metDataModel, Python 3, asari, khipu, ENPKG, MZmine, enpkg_mn_isdb_taxo, enpkg_sirius_canopus, enpkg_meta_analysis, SIRIUS, Open Tree of Life, Wikidata, NPClassifier, ChEMBL, Python, DEIMoS, numpy, ProteoWizard msconvert, MZmine2, MZmine3, timaR, Ion Identity, Inventa, ISFrag, R, XCMS

**Grounding:** 7 KB(s); DOIs: 10.1021/acs.analchem.1c01644, 10.1021/acs.analchem.1c05017, 10.1021/acs.analchem.2c05810, 10.1021/acscentsci.3c00800 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
