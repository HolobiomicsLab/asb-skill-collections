---
name: fda-repeatability-compliance-assessment
description: Use when you have completed NMR data quality control analysis and possess per-feature CV values, and you need to formally assess whether the metabolomic dataset meets FDA regulatory standards for downstream biomarker discovery or quantitative assays.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
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

# FDA repeatability compliance assessment

## Summary

Quantifies the proportion of NMR metabolic features meeting FDA coefficient of variation (CV) thresholds for biomarker discovery (CV < 0.30) and quantification (CV < 0.15), establishing whether a metabolomic dataset exhibits acceptable reproducibility. This skill validates dataset quality against regulatory benchmarks.

## When to use

Apply this skill when you have completed NMR data quality control analysis and possess per-feature CV values, and you need to formally assess whether the metabolomic dataset meets FDA regulatory standards for downstream biomarker discovery or quantitative assays. Use specifically when reproducibility claims must be validated or when gatekeeping on data quality before phenotype association studies.

## When NOT to use

- Input is raw NMR spectra or peak intensity data, not pre-computed CV values; run QC analysis first.
- CV values have already been filtered or subset; this skill requires the complete, unfiltered CV distribution.
- Your study uses different reproducibility standards (e.g., industry-specific or non-FDA thresholds); FDA thresholds are fixed and non-negotiable here.

## Inputs

- Per-feature coefficient of variation (CV) values from NMR QC analysis (numeric vector or table)
- Feature metadata (feature identifiers, chemical shift assignments, optional)

## Outputs

- Summary table: feature counts and proportions meeting CV < 0.30 and CV < 0.15 thresholds
- Distribution plot (histogram or empirical CDF) with FDA threshold reference lines
- Compliance report: percentage of features in each CV category, validation against expected benchmarks

## How to apply

Load pre-computed per-feature CV values from quality control output. Calculate the empirical cumulative distribution of CV across all metabolic features. Determine the count and percentage of features with CV < 0.30 and separately CV < 0.15, using these FDA thresholds as fixed decision boundaries. Generate a distribution plot (histogram or empirical CDF) with vertical reference lines at both thresholds to visualize compliance. Produce a summary table reporting feature counts and proportions in each CV category. Validate that computed proportions match expected benchmarks (99% at 0.30, 92% at 0.15 for high-quality datasets); substantial deviations indicate data quality issues requiring investigation before downstream analysis.

## Related tools

- **MWASTools** (R package providing integrated QC analysis pipeline; CV computation and threshold-based feature filtering are core functionalities) — https://github.com/AndreaRMICL/MWASTools
- **R** (Statistical computing environment for loading CV data, computing cumulative distributions, generating summary tables and plots)

## Examples

```
# Load MWASTools and compute FDA compliance in R
library(MWASTools); CV_data <- read.csv('feature_cv_values.csv'); compliance <- data.frame(threshold=c(0.30, 0.15), n_pass=c(sum(CV_data$CV < 0.30), sum(CV_data$CV < 0.15)), pct_pass=c(100*mean(CV_data$CV < 0.30), 100*mean(CV_data$CV < 0.15))); plot(ecdf(CV_data$CV), main='FDA Compliance: CV Distribution', xlab='Coefficient of Variation'); abline(v=c(0.15, 0.30), col=c('red', 'orange'), lty=2)
```

## Evaluation signals

- Computed percentages at CV < 0.30 and CV < 0.15 thresholds match expected values (99% and 92% respectively for high-quality NMR datasets).
- Distribution plot correctly displays all features on the CV axis with reference lines at 0.15 and 0.30; no CV values outside the valid numeric range [0, ∞).
- Summary table row totals equal the total number of features in input; proportions sum to 100% within rounding.
- Features classified as meeting both thresholds (CV < 0.15) form a subset of those meeting the discovery threshold (CV < 0.30); no logical contradictions.
- Documented exceptions or deviations from benchmarks are traced to specific features and investigated for systematic QC failures (e.g., low signal-to-noise).

## Limitations

- FDA thresholds (0.30 and 0.15) are fixed decision points; this skill does not accommodate alternative reproducibility standards or context-specific adjustments.
- Compliance assessment is univariate—does not capture multivariate reproducibility or feature-to-feature correlations that may affect quantification robustness.
- High CV in a subset of features (e.g., low-intensity metabolites) may still pass the overall threshold; individual feature-level investigation is required for assay optimization.
- CV values must be pre-computed from replicate NMR acquisitions; this skill assumes appropriate experimental design (e.g., QC samples run in replicate) was already executed.

## Evidence

- [other] Research question and finding from task_002: "What proportion of NMR metabolic features meet the FDA coefficient of variation (CV) thresholds of <0.30 for biomarker discovery and <0.15 for quantification? 99% of metabolic features exhibit CV <"
- [other] Workflow definition for compliance assessment: "Load the pre-computed per-feature CV values (output from quality control analysis). Calculate the cumulative distribution of CV values and determine the percentage of features meeting each FDA"
- [abstract] MWASTools QC capabilities from article abstract: "Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation"
- [intro] QC analysis workflow step: "quality control (QC) analysis; metabolite-phenotype association models adjusted for epidemiological confounders"
