---
name: coefficient-of-variation-computation
description: Use when you have loaded raw NMR or MS metabolomic abundance data into a SummarizedExperiment object and need to assess feature reproducibility before downstream association modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Bioconductor
  - MWASTools
  - ncGTW
  - xcms
  techniques:
  - NMR
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
- doi: 10.1093/bioinformatics/btaa037
  title: ''
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  - build: coll_ncgtw_cq
    doi: 10.1093/bioinformatics/btaa037
    title: ncGTW
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  - 10.1093/bioinformatics/btaa037
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# coefficient-of-variation-computation

## Summary

Compute coefficient of variation (CV) for each metabolic feature across samples in a metabolomic SummarizedExperiment object to quantify reproducibility and identify low-variance, high-quality features. This step is foundational for quality control filtering in metabolome-wide association studies.

## When to use

Apply this skill when you have loaded raw NMR or MS metabolomic abundance data into a SummarizedExperiment object and need to assess feature reproducibility before downstream association modeling. CV computation is triggered when the goal is to retain only metabolites with stable, reproducible signal levels across your sample cohort—particularly important in multivariate or epidemiological designs where confounding and batch effects must be controlled.

## When NOT to use

- Do not compute CV on already-filtered or pre-aggregated feature tables where individual sample replicates are not available; CV requires within-group variance across samples.
- Do not apply CV filtering if your experimental design intentionally uses features with high biological heterogeneity (e.g., disease biomarkers expected to vary widely); CV thresholding assumes low technical variation is desirable.
- Do not use CV computation on log-transformed or standardized abundance data without first back-transforming to original scale, as CV on transformed data may not reflect true reproducibility.

## Inputs

- SummarizedExperiment object containing metabolomic abundance data (assay matrix with features × samples)
- numeric matrix of metabolite abundances with samples as columns and features as rows

## Outputs

- numeric vector of coefficient of variation values, one per metabolic feature
- SummarizedExperiment object with CV values stored in rowData metadata

## How to apply

For each metabolic feature in the SummarizedExperiment assay matrix, calculate the coefficient of variation as the ratio of standard deviation to mean abundance across all samples. CV is unitless and expressed as a decimal (e.g., CV = 0.30 means 30% variation). The computed CV vector is typically stored as a column in the feature metadata (rowData) of the SummarizedExperiment. This metric quantifies feature reproducibility: lower CV values indicate more stable, reproducible metabolite measurements. The CV values then serve as the basis for downstream CV_filter thresholding to remove non-reproducible features and improve data quality before association testing.

## Related tools

- **MWASTools** (R package providing integrated pipeline for CV computation and CV_filter quality control within metabolome-wide association studies) — https://github.com/AndreaRMICL/MWASTools
- **Bioconductor** (Framework providing SummarizedExperiment class and data structures for storing and manipulating metabolomic feature metadata including CV values)
- **R** (Programming language required to run MWASTools and compute CV statistics (R >= 3.3))

## Evaluation signals

- CV vector length equals the number of features (rows) in the input SummarizedExperiment; no features are missing or duplicated.
- All CV values are non-negative and expressed as decimals (typically 0 to 1 or 0 to 10 depending on scaling); check for NaN, Inf, or negative values which indicate computational errors or empty features.
- CV distribution is right-skewed with median CV < mean CV, reflecting that most metabolites have moderate reproducibility with a tail of high-variance outlier features.
- Features with zero mean abundance or zero variance produce CV = 0 or NaN respectively; these should be handled or flagged explicitly before downstream filtering.
- Downstream CV_filter(metabo_SE, metabo_CV, CV_th = 0.30) successfully subsets the SummarizedExperiment using the computed CV vector, retaining only features where CV ≤ threshold and reducing feature count proportionally.

## Limitations

- CV is undefined or unstable for features with mean abundance near zero; requires explicit handling of zero-mean or near-zero-mean features (common in sparse metabolomic data).
- CV assumes samples are independent replicates; if data include technical replicates or nested designs, CV should be computed within-group and summarized appropriately to avoid inflated variation estimates.
- CV does not account for batch effects, instrument drift, or time-dependent systematic variation; preprocessing (e.g., drift correction in TopSpin or normalization) may be needed before CV computation to isolate true biological/technical reproducibility.
- CV threshold selection (e.g., CV_th = 0.30) is heuristic and dataset-dependent; no universal threshold is provided in the article; users must validate thresholds against quality metrics or reference standards for their specific NMR/MS platform and biological context.

## Evidence

- [other] CV_filter(metabo_SE, metabo_CV, CV_th = 0.30) retains only metabolic features with coefficient of variation below 0.30, removing non-reproducible features from the metabolic matrix to produce a filtered SummarizedExperiment object.: "CV_filter(metabo_SE, metabo_CV, CV_th = 0.30) retains only metabolic features with coefficient of variation below 0.30, removing non-reproducible features"
- [intro] quality control (QC) analysis; metabolite-phenotype association models: "quality control (QC) analysis; metabolite-phenotype association models"
- [other] compute coefficient of variation (CV) for each feature across samples: "compute coefficient of variation (CV) for each feature across samples"
- [other] Apply threshold filter retaining only features where CV ≤ 0.30 to remove high-variance, low-reproducibility metabolites.: "Apply threshold filter retaining only features where CV ≤ 0.30 to remove high-variance, low-reproducibility metabolites"
- [intro] Assuming that R (>=3.3) and Bioconductor have been correctly installed: "Assuming that R (>=3.3) and Bioconductor have been correctly installed"
