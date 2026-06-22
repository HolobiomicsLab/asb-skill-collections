---
name: replicate-consistency-assessment
description: Use when after NMR or MS data acquisition and preprocessing (phasing, baseline correction) when you have a SummarizedExperiment object containing assay intensity matrix with QC sample columns designated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Bioconductor
  - MWASTools
  - R / Bioconductor
  techniques:
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# replicate-consistency-assessment

## Summary

Compute coefficient of variation (CV) across quality control (QC) replicates to quantify the reproducibility of individual metabolic features in high-throughput NMR or MS assays. This metric identifies which features have stable, reliable signal intensity across technical replicates, informing downstream filtering and association analysis.

## When to use

Apply this skill after NMR or MS data acquisition and preprocessing (phasing, baseline correction) when you have a SummarizedExperiment object containing assay intensity matrix with QC sample columns designated. Use it to establish a reproducibility threshold before filtering features for metabolite-phenotype association modeling, particularly when QC samples are available and epidemiological confounding adjustment is planned.

## When NOT to use

- Input assay already contains only features pre-filtered by vendor QC software (CV filtering already performed upstream).
- No QC replicate samples are available in the study design; CV computation requires at least 2–3 technical replicates per QC pool.
- Assay data are already aggregated or summarized (e.g., feature presence/absence table); CV requires raw or normalized intensity values.

## Inputs

- SummarizedExperiment object (metabo_SE) with assay matrix of metabolite intensities
- Column annotations identifying QC sample replicates within the assay
- Preprocessed NMR or MS signal matrix (post-phasing, baseline correction)

## Outputs

- Named numeric vector (metabo_CV) of coefficient-of-variation values, one per feature
- Feature-level reproducibility metrics for filtering and QC reporting
- Optional: Boolean feature mask or filtered assay object with low-CV features retained

## How to apply

Extract the subset of assay matrix columns corresponding to QC samples (e.g., 10 QC replicates). For each metabolite feature (row), calculate the mean and standard deviation of signal intensity across the QC sample columns. Compute CV as the ratio sd/mean for each feature. Store results in a named numeric vector with feature names as vector names. Features with CV below a study-defined threshold (commonly ≤ 0.2–0.3 in NMR metabolomics) are retained for association analysis; high-CV features are flagged as unreliable and often excluded to improve statistical power and reduce noise in downstream models.

## Related tools

- **MWASTools** (R package providing integrated quality control (QC) analysis workflow, including CV computation and feature reproducibility filtering for metabolomics association studies) — https://github.com/AndreaRMICL/MWASTools
- **R / Bioconductor** (Computational environment and framework for SummarizedExperiment object manipulation, vector operations, and statistical QC workflows)

## Examples

```
metabo_CV <- QC_CV(metabo_SE, qc_cols = c('QC_1', 'QC_2', ..., 'QC_10')); filtered_features <- names(metabo_CV)[metabo_CV <= 0.2]
```

## Evaluation signals

- metabo_CV vector length equals the total number of metabolite features in the input assay matrix.
- All CV values are non-negative and unitless (dimensionless ratio of sd to mean); check for NaN or Inf entries arising from zero or near-zero mean intensities.
- CV values should show expected distribution (e.g., median ≤ 0.25 for well-controlled NMR; outliers > 0.5 indicate unstable features).
- Feature subsetting based on CV threshold (e.g., retaining features with CV ≤ 0.2) reduces feature count by 10–40% in typical metabolomics QC; verify count consistency with quality expectations.
- Named vector structure: confirm feature names match original assay row names; spot-check a few CV values by manual calculation (sd/mean) on raw QC intensity subset.

## Limitations

- CV is undefined or inflated when feature mean intensity is near zero; features with low absolute signal intensity may have artificially high CV despite acceptable absolute repeatability (consider signal-to-noise ratio thresholds as alternative or complement).
- CV threshold selection is study- and platform-dependent; NMR typically permits stricter CV (≤ 0.2), while targeted MS or dilute samples may require relaxed thresholds (≤ 0.3–0.4); no universal cutoff is provided in the article.
- QC pool composition (single pooled control vs. multiple QC pools) affects interpretation; CV computed within a single QC pool reflects technical variability only, not between-pool biological or batch drift.
- Small QC sample size (n < 5) reduces precision of CV estimate; article uses n = 10 QC replicates, which provides stable estimation.

## Evidence

- [other] Extract the 10 QC sample columns; compute mean and sd per feature across QC samples; calculate CV as sd/mean.: "Extract the 10 QC sample columns from the metabo_SE SummarizedExperiment assay matrix. 2. For each metabolite feature (row), calculate the mean and standard deviation across the 10 QC samples. 3."
- [other] QC_CV function output is a named numeric vector of CV values per feature, used to quantify signal reproducibility.: "The QC_CV function calculates the coefficient of variation (sd/mean) for each NMR signal across the QC samples, producing a metabo_CV output vector that quantifies signal reproducibility."
- [other] MWASTools package provides integrated quality control analysis within MWAS pipeline.: "Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation"
- [other] QC analysis is a core workflow step in multivariate metabolomics analysis.: "quality control (QC) analysis; metabolite-phenotype association models"
