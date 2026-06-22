---
name: cumulative-distribution-visualization
description: 'Use when when you have per-feature quality metrics (such as CV values from NMR or MS reproducibility analysis) and need to: (1) confirm that a specified proportion of features meet regulatory thresholds (e.g., 99% < 0.30, 92% < 0.15 for CV);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MWASTools
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cumulative-distribution-visualization

## Summary

Visualize the empirical cumulative distribution of a continuous quality metric (e.g., coefficient of variation) across features to assess reproducibility against regulatory thresholds. This skill enables rapid validation of whether a dataset meets predefined FDA or domain-specific quality gates.

## When to use

When you have per-feature quality metrics (such as CV values from NMR or MS reproducibility analysis) and need to: (1) confirm that a specified proportion of features meet regulatory thresholds (e.g., 99% < 0.30, 92% < 0.15 for CV); (2) visually communicate the distribution of reproducibility across the entire metabolome; or (3) validate dataset suitability for downstream association studies before proceeding to metabolite-phenotype modeling.

## When NOT to use

- Input is already an aggregated or summarized CV distribution rather than per-feature values; use the summary directly instead of re-computing.
- Quality control analysis has not yet been performed on the raw spectra; run QC preprocessing (phasing, baseline correction, normalization) before computing CV values.
- Your goal is to identify outlier features for removal rather than to validate overall dataset reproducibility; use a different filtering or outlier-detection skill.

## Inputs

- per-feature coefficient of variation (CV) values (numeric vector or table column)
- pre-computed QC analysis output from NMR or MS platform
- FDA or domain-specific threshold definitions (e.g., 0.30, 0.15)

## Outputs

- empirical cumulative distribution plot (histogram or CDF curve with threshold annotations)
- summary table reporting count and proportion of features in each CV category
- validation report confirming observed percentages match expected thresholds

## How to apply

Load pre-computed per-feature CV (or equivalent QC metric) values from quality control analysis output. Calculate the empirical cumulative distribution function (CDF) and compute the proportion of features below each FDA threshold (typically CV < 0.30 for biomarker discovery and CV < 0.15 for quantification). Generate a distribution plot (histogram with threshold lines or empirical CDF curve) marking the cutoff values at 0.15 and 0.30 on the x-axis. Overlay or report the observed percentages (e.g., 99% at 0.30, 92% at 0.15) and verify these match expected or previously reported values. Use this visualization to either flag reproducibility concerns if thresholds are not met or provide confidence in dataset quality for downstream MWAS modeling.

## Related tools

- **MWASTools** (R package that provides integrated quality control analysis module to compute and report per-feature CV values, which serve as input to cumulative distribution visualization) — https://github.com/AndreaRMICL/MWASTools
- **R** (Statistical computing environment in which CDF calculations, threshold filtering, and visualization (via base R or ggplot2) are performed)

## Examples

```
# R example: cv_data <- read.csv('metabo_SE_QC_CV.csv'); prop_030 <- mean(cv_data$CV < 0.30); prop_015 <- mean(cv_data$CV < 0.15); plot(ecdf(cv_data$CV), main='CV Distribution', xlab='Coefficient of Variation'); abline(v=c(0.15, 0.30), col=c('blue','red'), lty=2)
```

## Evaluation signals

- Observed percentages of features meeting each FDA threshold (e.g., 99% < 0.30, 92% < 0.15) match expected or previously published values for the same dataset.
- Cumulative distribution plot displays smooth monotonic increase from 0 to 1, with clear annotation of threshold lines at 0.15 and 0.30.
- Summary table reports exact counts and proportions for all CV categories; counts sum to total number of features analyzed.
- No CV values are negative or exceed 1.0 (or dataset-specific bounds); all input data passed basic validity checks.
- Threshold lines visually intersect the CDF curve at the reported percentages, confirming internal consistency between plot and numeric results.

## Limitations

- Cumulative distribution visualization assumes CV values are already computed from replicate measurements; it does not validate the QC analysis that produced them.
- Thresholds (0.30, 0.15) are FDA guidelines for NMR/MS metabolomics but may not apply to other metabolite profiling platforms or study designs; users must verify appropriateness for their context.
- The skill reports marginal univariate distributions of CV and does not account for potential correlations between feature reproducibility and chemical class, concentration range, or spectral region.
- Visualization alone does not identify why specific features fail thresholds (e.g., instrumental drift, peak overlap, low signal); downstream investigation of failed features is needed.

## Evidence

- [other] Finding: 99% of metabolic features exhibit CV < 0.30 and 92% exhibit CV < 0.15, confirming reproducibility of the NMR dataset according to FDA thresholds.: "99% of metabolic features exhibit CV < 0.30 and 92% exhibit CV < 0.15, confirming reproducibility of the NMR dataset according to FDA thresholds"
- [other] Workflow step: Calculate the cumulative distribution of CV values and determine the percentage of features meeting each FDA threshold (CV < 0.30 and CV < 0.15).: "Calculate the cumulative distribution of CV values and determine the percentage of features meeting each FDA threshold (CV < 0.30 and CV < 0.15)"
- [other] Workflow step: Produce a distribution plot (histogram or empirical CDF) showing CV values with threshold lines marked at 0.15 and 0.30.: "Produce a distribution plot (histogram or empirical CDF) showing CV values with threshold lines marked at 0.15 and 0.30"
- [abstract] MWASTools functionality: Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation spectroscopy (STOCSY).: "Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools"
- [other] Workflow task: Load the pre-computed per-feature CV values (output from quality control analysis).: "Load the pre-computed per-feature CV values (output from quality control analysis)"
