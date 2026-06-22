---
name: metabolite-feature-quality-control
description: Use when you have a metabolomic SummarizedExperiment object with replicate QC (quality control) samples and need to remove non-reproducible metabolic features before phenotype association modeling. Use it specifically when your workflow requires FDA-compliant reproducibility thresholds (CV < 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MWASTools
  - Bioconductor
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
---

# metabolite-feature-quality-control

## Summary

Assess reproducibility of metabolomic features by computing coefficient of variation (CV) across quality control samples and filtering features that fail FDA thresholds for biomarker discovery (CV < 0.30) or quantification (CV < 0.15). This skill ensures only reliable, low-variance metabolites are retained for downstream association analysis.

## When to use

Apply this skill when you have a metabolomic SummarizedExperiment object with replicate QC (quality control) samples and need to remove non-reproducible metabolic features before phenotype association modeling. Use it specifically when your workflow requires FDA-compliant reproducibility thresholds (CV < 0.30 for discovery, CV < 0.15 for quantification) or when you need to document what proportion of your feature set meets these standards.

## When NOT to use

- Input metabolomic dataset lacks replicate QC samples — CV cannot be computed without within-QC variability
- Features have already been filtered or preprocessed by an external QC pipeline — applying redundant filtering may remove informative signal
- Study design uses single-injection samples without technical replicates — CV estimates will be unreliable

## Inputs

- SummarizedExperiment object (metabo_SE) with metabolite abundances and QC sample identifiers
- Assay matrix containing raw metabolite intensity values across samples

## Outputs

- Coefficient of variation vector (metabo_CV) with CV values per feature
- Filtered SummarizedExperiment object (metabo_SE) retaining only CV-passing features
- Summary table reporting count and proportion of features in each CV category
- Distribution plot (histogram or empirical CDF) with FDA threshold lines marked

## How to apply

First, extract QC sample columns from the metabolomic SummarizedExperiment assay matrix and compute coefficient of variation (CV = sd/mean) for each metabolite feature across these QC replicates using the QC_CV function, producing a named CV vector. Second, calculate the cumulative distribution of CV values and report the percentage of features meeting each FDA threshold (< 0.30 and < 0.15) to document reproducibility. Third, apply the CV_filter function with a chosen threshold (typically CV_th = 0.30) to subset the SummarizedExperiment, retaining only features below the threshold and removing high-variance metabolites. Validate that the reported percentages match your computed values (e.g., 99% < 0.30, 92% < 0.15) and generate a distribution plot with threshold lines marked to visualize the filtering decision.

## Related tools

- **MWASTools** (R package providing QC_CV and CV_filter functions for computing and applying CV thresholds to metabolomic SummarizedExperiment objects) — https://github.com/AndreaRMICL/MWASTools
- **R** (Programming environment for loading SummarizedExperiment objects and executing MWASTools functions (>=3.3 required))
- **Bioconductor** (Framework providing SummarizedExperiment class and infrastructure for metabolomic data representation)

## Examples

```
metabo_CV <- QC_CV(metabo_SE); metabo_SE_filtered <- CV_filter(metabo_SE, metabo_CV, CV_th = 0.30); prop_pass_030 <- sum(metabo_CV < 0.30) / length(metabo_CV); prop_pass_015 <- sum(metabo_CV < 0.15) / length(metabo_CV)
```

## Evaluation signals

- Reported percentages of features meeting FDA thresholds (99% < 0.30, 92% < 0.15) match independently computed values from the CV distribution
- Filtered SummarizedExperiment object contains only features with CV ≤ threshold; verify no features above threshold remain in assay matrix
- Distribution plot shows bimodal or expected unimodal CV distribution with threshold lines correctly positioned at 0.15 and 0.30
- Feature count decreases predictably: applying CV_th = 0.30 removes ~1% of features; applying CV_th = 0.15 removes ~8% of features relative to unfiltered set
- No missing values or NaN entries in metabo_CV vector; all feature names from input SummarizedExperiment are present in output CV vector

## Limitations

- CV computation is sensitive to low absolute abundances (features with mean near zero produce inflated CV estimates); consider log-transformation or lower abundance thresholds
- FDA thresholds (0.30 and 0.15) are population-specific; coefficients vary by analytical platform (NMR vs. MS), sample matrix, and instrument tuning and should be validated in your own QC cohort
- Filtering by CV alone does not account for biological relevance; low-variance features may be uninformative metabolites whereas higher-variance features may still carry phenotype association signal
- Small QC sample sets (< 5 replicates) produce unstable CV estimates; the original study used 10 QC samples

## Evidence

- [other] QC_CV function computes coefficient of variation for metabolites: "The QC_CV function calculates the coefficient of variation (sd/mean) for each NMR signal across the QC samples, producing a metabo_CV output vector that quantifies signal reproducibility."
- [other] FDA reproducibility thresholds for biomarker discovery and quantification: "99% of metabolic features exhibit CV < 0.30 and 92% exhibit CV < 0.15, confirming reproducibility of the NMR dataset according to FDA thresholds."
- [other] CV_filter function removes non-reproducible features: "CV_filter(metabo_SE, metabo_CV, CV_th = 0.30) retains only metabolic features with coefficient of variation below 0.30, removing non-reproducible features from the metabolic matrix to produce a"
- [abstract] Quality control analysis is a key MWASTools functionality: "Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation"
- [intro] NMR platform for metabolomic data acquisition: "<sup>1</sup>H NMR plasma spectra were acquired on a Bruker Avance III 600 MHz spectrometer"
