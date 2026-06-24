---
name: coefficient-of-variation-threshold-analysis
description: 'Use when you have per-feature CV values from quality control analysis
  of NMR or MS metabolomic data and need to: (1) establish whether your dataset meets
  FDA reproducibility standards for downstream biomarker discovery or quantification;
  (2) benchmark data quality against regulatory thresholds;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - MWASTools
  - R (≥3.3)
  - Bioconductor
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly
  pipeline'
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

# coefficient-of-variation-threshold-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluates the reproducibility and quality of NMR metabolomic features by computing cumulative distributions of coefficient of variation (CV) values and assessing compliance with FDA regulatory thresholds (CV < 0.30 for biomarker discovery, CV < 0.15 for quantification). This skill validates data quality across high-throughput metabolic profiling datasets.

## When to use

Apply this skill when you have per-feature CV values from quality control analysis of NMR or MS metabolomic data and need to: (1) establish whether your dataset meets FDA reproducibility standards for downstream biomarker discovery or quantification; (2) benchmark data quality against regulatory thresholds; (3) report the proportion of features meeting predefined CV cutoffs to justify inclusion/exclusion decisions in association studies.

## When NOT to use

- CV values have not yet been computed; use the upstream quality control (QC) analysis step first to derive per-feature CVs from replicate or technical replicate measurements.
- The study does not require FDA regulatory compliance or does not use metabolomic data; CV thresholds are specific to metabolite biomarker discovery and quantification workflows.
- Input is already a filtered feature table rather than raw CV distributions; this skill operates on unfiltered CV value distributions to evaluate data quality before feature selection.

## Inputs

- Per-feature coefficient of variation (CV) values (numeric vector or table from QC analysis)
- Feature metadata (feature name, chemical shift or m/z, metabolite ID where available)

## Outputs

- Contingency table with feature counts and percentages for CV < 0.15, 0.15 ≤ CV < 0.30, and CV ≥ 0.30
- Summary statistics: proportion meeting each FDA threshold
- Distribution plot (histogram or empirical CDF) with threshold lines at CV = 0.15 and 0.30
- Validation report confirming reproducibility against FDA benchmarks

## How to apply

Load pre-computed per-feature CV values (output from MWASTools or equivalent QC pipeline). Calculate the empirical cumulative distribution of CV across all metabolic features. Compute the proportion of features with CV < 0.30 and CV < 0.15, comparing against the regulatory benchmarks (target: ≥99% at 0.30, ≥92% at 0.15). Generate both a summary contingency table (count and percentage of features in each CV category) and a visualization (histogram or empirical CDF) with threshold lines overlaid at CV = 0.15 and 0.30. Validate that computed percentages match the reported thresholds; discrepancies warrant investigation of outlier features or QC preprocessing steps.

## Related tools

- **MWASTools** (R package providing integrated quality control analysis, including computation of per-feature CV values and threshold-based reproducibility assessment for metabolite-phenotype association studies) — https://github.com/AndreaRMICL/MWASTools
- **R (≥3.3)** (Statistical computing environment used to implement CV distribution calculations, thresholding, and visualization)
- **Bioconductor** (Provides data structures and statistical methods for managing and analyzing high-dimensional biological data including metabolomic feature tables)

## Examples

```
# Load pre-computed CV values and assess FDA compliance
cv_data <- read.csv('metabo_SE_cv_values.csv', row.names=1)
threshold_30 <- sum(cv_data$CV < 0.30) / nrow(cv_data) * 100
threshold_15 <- sum(cv_data$CV < 0.15) / nrow(cv_data) * 100
print(paste('Proportion CV<0.30:', round(threshold_30, 1), '%'))
print(paste('Proportion CV<0.15:', round(threshold_15, 1), '%'))
plot(ecdf(cv_data$CV), main='CV Distribution', xlab='Coefficient of Variation'); abline(v=c(0.15, 0.30), col=c('blue','red'), lty=2)
```

## Evaluation signals

- Proportions of features with CV < 0.30 and CV < 0.15 match the reported benchmarks (99% and 92% respectively, or close to them within rounding tolerance).
- Distribution plot clearly displays both threshold lines and shows the shape of the empirical CDF; visual inspection confirms that the marked threshold proportions align with the histogram/CDF curve.
- Contingency table row sums equal the total number of features, and column proportions sum to 100%, indicating complete feature coverage with no missing or double-counted values.
- No features in the dataset have CV values below 0 or above 1 (CV is a normalized measure); outliers or implausible CV values are flagged.
- The computed percentages are consistent across repeated calculations (reproducibility check) and across different subsets of features (e.g., aromatic vs. aliphatic regions in NMR) to detect batch or region-specific quality issues.

## Limitations

- CV thresholds are calibrated for FDA biomarker discovery and quantification; regulatory standards may vary by jurisdiction or application domain, and this skill does not automatically adapt thresholds.
- The skill assumes that CV values have been computed from valid technical replicate or QC measurements; if the underlying QC design is flawed (e.g., insufficient replicates, systematic drift), CV estimates will be biased and threshold interpretation unreliable.
- FDA thresholds (CV < 0.30 for discovery, CV < 0.15 for quantification) are global cutoffs and do not account for metabolite-specific factors such as abundance-dependent noise, resonance overlap in NMR spectra, or ionization efficiency in MS; features just above a threshold may still be analytically useful.
- The skill evaluates reproducibility only; it does not assess accuracy, systematic bias, or matrix effects, which are separate quality dimensions required for full method validation.

## Evidence

- [other] FDA coefficient of variation thresholds: "What proportion of NMR metabolic features meet the FDA coefficient of variation (CV) thresholds of <0.30 for biomarker discovery and <0.15 for quantification?"
- [other] Cumulative distribution and threshold-based assessment: "Calculate the cumulative distribution of CV values and determine the percentage of features meeting each FDA threshold (CV < 0.30 and CV < 0.15)"
- [other] Reporting structure and validation: "Generate a summary table reporting the count and proportion of features in each CV category. 4. Produce a distribution plot (histogram or empirical CDF) showing CV values with threshold lines marked"
- [abstract] Quality control analysis in MWASTools: "Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation"
- [other] Confirmed finding from task: "99% of metabolic features exhibit CV < 0.30 and 92% exhibit CV < 0.15, confirming reproducibility of the NMR dataset according to FDA thresholds."
