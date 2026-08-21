---
name: quality-metrics-summarization
description: Use when after running QC analysis on NMR or MS metabolomic data and
  obtaining per-feature CV values, use this skill to validate that the dataset meets
  FDA thresholds (CV < 0.30 for discovery, CV < 0.15 for quantification) and to report
  the proportion of features meeting each threshold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MWASTools
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
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

# quality-metrics-summarization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute and report cumulative distributions of quality control metrics (e.g., coefficient of variation) across metabolomic features to validate dataset reproducibility against regulatory thresholds. This skill aggregates pre-computed per-feature QC values into interpretable summary statistics and visualizations that confirm fitness for downstream analysis.

## When to use

After running QC analysis on NMR or MS metabolomic data and obtaining per-feature CV values, use this skill to validate that the dataset meets FDA thresholds (CV < 0.30 for discovery, CV < 0.15 for quantification) and to report the proportion of features meeting each threshold. This is a validation gate before proceeding to association modeling.

## When NOT to use

- Input is raw NMR or MS spectra (not yet processed through QC analysis)
- Per-feature CV values have not yet been computed or are missing
- The analysis goal is to identify individual features requiring reanalysis rather than to summarize overall dataset reproducibility

## Inputs

- Pre-computed per-feature CV values (numeric vector or table, output from MWASTools QC analysis)
- FDA regulatory thresholds (CV < 0.30 for discovery, CV < 0.15 for quantification)

## Outputs

- Summary table: feature counts and proportions meeting each CV threshold
- Distribution plot: histogram or empirical CDF of CV values with threshold lines at 0.15 and 0.30
- Validation report: confirmation that observed percentages match expected thresholds

## How to apply

Load pre-computed per-feature CV values from QC output. Calculate the empirical cumulative distribution function (CDF) of CV and determine what proportion of features fall below each FDA threshold (0.30 and 0.15). Generate a summary table reporting feature counts and proportions in each CV category. Produce a distribution plot (histogram or empirical CDF) overlaid with vertical threshold lines at CV = 0.15 and 0.30. Validate that computed percentages match reported expectations (e.g., 99% < 0.30, 92% < 0.15) to confirm reproducibility and quality before advancing to metabolite-phenotype association models.

## Related tools

- **MWASTools** (R package that performs QC analysis and outputs per-feature CV values; used to load and aggregate QC metrics for threshold-based validation) — github.com/AndreaRMICL/MWASTools
- **R** (Statistical environment used to compute empirical CDF, calculate proportions, and generate summary tables and distribution plots)

## Examples

```
# In R using MWASTools output: cv_data <- read.csv('cv_values.csv'); prop_030 <- sum(cv_data$CV < 0.30) / nrow(cv_data); prop_015 <- sum(cv_data$CV < 0.15) / nrow(cv_data); cat('Proportion < 0.30:', prop_030, '\nProportion < 0.15:', prop_015, '\n'); hist(cv_data$CV, breaks=50, main='CV Distribution', xlab='Coefficient of Variation'); abline(v=c(0.15, 0.30), col=c('blue', 'red'), lty=2)
```

## Evaluation signals

- Computed percentages at CV thresholds (0.30 and 0.15) match reported expectations (99% and 92%, respectively)
- Sum of feature counts across all CV categories equals total number of features in the dataset
- Distribution plot displays both threshold lines (0.15 and 0.30) and reflects the empirical shape of the CV distribution
- Summary table contains non-negative integers for feature counts and proportions that sum to 100% (or 1.0 as decimal)
- No missing or undefined CV values in the input data; all features have valid numeric CV measurements

## Limitations

- Summary is descriptive only; does not identify which specific features are outliers or fail thresholds — separate investigation needed
- Thresholds (0.30, 0.15) are FDA recommendations; applicability may vary by regulatory context or assay platform (NMR vs. MS)
- Does not account for potential batch effects or platform-specific CV distributions that might differ across cohorts or experimental runs

## Evidence

- [intro] FDA threshold interpretation and task objective: "What proportion of NMR metabolic features meet the FDA coefficient of variation (CV) thresholds of <0.30 for biomarker discovery and <0.15 for quantification?"
- [other] Core workflow for metrics summarization: "Calculate the cumulative distribution of CV values and determine the percentage of features meeting each FDA threshold (CV < 0.30 and CV < 0.15). Generate a summary table reporting the count and"
- [other] Visualization and validation requirement: "Produce a distribution plot (histogram or empirical CDF) showing CV values with threshold lines marked at 0.15 and 0.30. Validate that reported percentages (99% at 0.30 threshold, 92% at 0.15"
- [other] Input data type: "Load the pre-computed per-feature CV values (output from quality control analysis)."
- [abstract] MWASTools QC capability: "Key functionalities of the package include: quality control (QC) analysis; metabolite-phenotype association models"
