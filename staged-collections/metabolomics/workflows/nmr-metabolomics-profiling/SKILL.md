---
name: nmr-metabolomics-profiling-workflow
description: 'Use when you have NMR metabolomics data (1D/2D spectra or FIDs) and
  want a quantified, identified metabolite profile — spectral preprocessing (phase/baseline/referencing,
  binning), metabolite identification by chemical shift, quantification, and group
  statistics.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - NMR
  stage_count: 4
  member_skills:
  - nmr-spectral-preprocessing-and-phasing
  - nmr-workflow-pipeline-execution
  - nmr-spectra-preprocessing
  - metabolite-dataset-preprocessing
  - metabolite-peak-assignment-from-nmr
  - nmr-metabolite-identity-confirmation
  - nmr-chemical-shift-interval-matching
  - hmdb-metabolite-query-and-retrieval
  - nmr-peak-deconvolution
  - compound-abundance-quantification-from-flow
  - nmr-peak-table-generation
  - univariate-statistical-testing-for-metabolomics
  - multiple-testing-correction-metabolomics
  - group-comparison-statistics
  - multicontrast-statistical-testing-lipidomics
  member_tools:
  - R
  - Bioconductor
  - MWASTools
  - TopSpin 3.2
  - Bruker Avance III 600 MHz
  - SAND
  - NMRPipe
  - NMRBox
  - PRIMA-Panel
  - PyTorch
  - NumPy
  - Pandas
  - SciPy
  - NMRformer
  - openpyxl
  - XlsxWriter
  - Python
  - PyQt5
  - Human Metabolome Database (HMDB)
  - ROIAL-NMR
  - mcfNMR
  - spec2csv
  - omu (omu_summary function)
  - assign_hierarchy
  - omu_summary
  - omu_anova
  - count_fold_changes
  - transform_samples
  - LargeMetabo
  - Marker_Identify
  - e1071
  - FSelector
  - mixOmics
  - siggenes
  - lipidr
  - limma
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# NMR Metabolomics Profiling

## Summary

End-to-end NMR metabolomics: from raw spectra to identified, quantified metabolites and group-wise statistical comparison.


## When to use

Use when you have NMR metabolomics data (1D/2D spectra or FIDs) and want a quantified, identified metabolite profile — spectral preprocessing (phase/baseline/referencing, binning), metabolite identification by chemical shift, quantification, and group statistics.


## When NOT to use

- The data is not NMR.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess_nmr

**Goal:** NMR spectral preprocessing (phase, baseline, referencing, binning)

**EDAM operation:** operation_3215

**Inputs:** nmr-spectrum · **Outputs:** feature-table

**Candidate leaf skills:** `nmr-spectral-preprocessing-and-phasing` (primary), `nmr-workflow-pipeline-execution`, `nmr-spectra-preprocessing`, `metabolite-dataset-preprocessing`

**Tools:** R, Bioconductor, MWASTools, TopSpin 3.2, Bruker Avance III 600 MHz, SAND, NMRPipe, NMRBox, PRIMA-Panel

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.3c03078, 10.1021/acs.analchem.4c04938, 10.1093/bioinformatics/btx477

### Stage 2 — identification

**Goal:** identify metabolites by chemical shift matching

**EDAM operation:** operation_3803

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-peak-assignment-from-nmr` (primary), `nmr-metabolite-identity-confirmation`, `nmr-chemical-shift-interval-matching`, `hmdb-metabolite-query-and-retrieval`

**Tools:** PyTorch, NumPy, Pandas, SciPy, NMRformer, R, Bioconductor, MWASTools, TopSpin 3.2, openpyxl, XlsxWriter, Python, PyQt5, Human Metabolome Database (HMDB), ROIAL-NMR

**Grounding:** 3 KB(s); DOIs: 10.1002/nbm.70131, 10.1021/acs.analchem.4c05632, 10.1093/bioinformatics/btx477

### Stage 3 — quantification

**Goal:** quantify metabolites from NMR signals

**EDAM operation:** operation_3799

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `nmr-peak-deconvolution` (primary), `compound-abundance-quantification-from-flow`, `nmr-peak-table-generation`

**Tools:** SAND, NMRPipe, NMRBox, mcfNMR, spec2csv

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.3c03078, 10.1021/acs.analchem.4c01652

### Stage 4 — statistics

**Goal:** multivariate + differential analysis of NMR profiles

**EDAM operation:** operation_3659

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `univariate-statistical-testing-for-metabolomics` (primary), `multiple-testing-correction-metabolomics`, `group-comparison-statistics`, `multicontrast-statistical-testing-lipidomics`

**Tools:** R, omu (omu_summary function), assign_hierarchy, omu_summary, omu_anova, count_fold_changes, transform_samples, MWASTools, Bioconductor, LargeMetabo, Marker_Identify, e1071, FSelector, mixOmics, siggenes, lipidr, limma

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.jproteome.0c00082, 10.1093/bib/bbac455, 10.1093/bioinformatics/btx477, 10.1128/mra.00129-19

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
