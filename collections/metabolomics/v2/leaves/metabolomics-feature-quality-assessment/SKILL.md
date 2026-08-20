---
name: metabolomics-feature-quality-assessment
description: Use when after drift correction and before missing value imputation when
  your LC-MS peak table contains features with variable detection rates across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - notame
  - R
  - missForest
  - doParallel
  - Biobase
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- The implementation we use (from the missForest package) can be parallelized
- Load the libraries (doParallel is used for parallel processing)
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-feature-quality-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and flag low-quality molecular features in LC-MS metabolomics data using detection rates and quality metrics to ensure downstream statistical and multivariate analyses are performed on reliable features. This skill applies quality thresholds defined in the notame workflow to systematically exclude features with extensive missing values or poor reproducibility before imputation and batch correction.

## When to use

Apply this skill after drift correction and before missing value imputation when your LC-MS peak table contains features with variable detection rates across samples. Use it when you need to distinguish between genuine metabolite signals and artifacts or noise, particularly when features show inconsistent detection patterns (e.g., missing in >50% of samples) or fail reproducibility checks on quality control (QC) samples.

## When NOT to use

- Feature table already pre-filtered by the peak-picking software (MS-DIAL or equivalent); applying additional quality flagging may over-filter.
- Analysis goal is exploratory or discovery-focused where you wish to retain all features for hypothesis generation, even marginal ones.
- Study has very small sample size (<10 per group) where aggressive feature filtering may eliminate true but under-sampled signals.

## Inputs

- MetaboSet object with expression matrix (exprs) and feature metadata
- Sample metadata and group assignments
- QC (quality control) sample replicates within the peak table

## Outputs

- MetaboSet object with flag column(s) in feature metadata indicating low-detection or low-quality status
- Summary statistics of flagged features (count, detection rates, quality metric distributions)
- Visualization of feature detection across samples and QC reproducibility

## How to apply

First, use flag_detection to identify features based on their detection frequency across samples, flagging those with extensive missing values according to your experimental design thresholds. Second, apply flag_quality to evaluate features against quality metrics such as QC sample reproducibility and signal intensity distributions, as defined by Broadhurst et al. criteria. Set seed numbers for reproducibility when flagging decisions depend on stochastic processes. Features flagged at this stage are marked in the MetaboSet object but typically retained; decide post-hoc whether to remove flagged features entirely or exclude them from specific downstream analyses (e.g., keep low-quality features out of multivariate models but include them in univariate tests). The rationale is that low-quality features introduce noise and reduce statistical power, while systematic flagging enables transparent, reproducible filtering decisions.

## Related tools

- **notame** (Provides flag_detection and flag_quality functions to systematically assess and flag low-quality features in MetaboSet objects) — https://github.com/hanhineva-lab/notame
- **Biobase** (Supplies the ExpressionSet class upon which MetaboSet is built, enabling structured feature and sample metadata storage)
- **R** (Statistical environment for executing flagging functions and generating quality assessment visualizations)

## Examples

```
metaboset_flagged <- flag_detection(metaboset, min_detection = 0.5); metaboset_flagged <- flag_quality(metaboset_flagged)
```

## Evaluation signals

- Feature metadata now contains logical or binary flag columns (e.g., 'detected', 'quality_pass') with no NA values
- Detection rate distribution for flagged features shows clear separation from non-flagged features (e.g., flagged features <50% detection, non-flagged >70%)
- QC sample reproducibility metrics (e.g., RSD or ICC) for flagged features show notably higher variance than non-flagged features
- Flagged feature count and percentages are reported; typically 10–40% of initial features flagged depending on data quality and threshold stringency
- Subsequent statistical models run on non-flagged features show improved stability, lower p-value inflation, and more reproducible effect sizes than models including all features

## Limitations

- Flagging thresholds are semi-arbitrary and study-dependent; no universally optimal detection rate or quality cutoff exists across all metabolomics experiments. Results are sensitive to the choice of QC sample frequency and homogeneity.
- Low-quality flags do not automatically remove features; decision to exclude flagged features must be made post-hoc and justified in methods and results sections.
- Studies with few QC samples or no technical replicates cannot reliably estimate reproducibility metrics, limiting the power of quality flagging to distinguish noise from true signal.
- Missing value patterns are not fully accounted for during flagging; features with systematic missingness tied to batch or condition may be unfairly flagged if detection is calculated naively across all samples without stratification.

## Evidence

- [other] flag_detection and quality thresholds: "```flag_detection``` is used to flag features based on detection"
- [other] Quality metrics framework: "Identifying and flagging (or removing) low-quality molecular features using quality metrics defined by Broadhurst et al."
- [other] Workflow position and rationale: "Next, flag all the features with extensive amounts of missing values"
- [other] Contaminant and quality flagging functions: "```flag_contaminants``` is used to flag contaminants
  - flag_quality  [section=other; evidence='```flag_quality``` is used to flag features based on the other quality metrics"
- [readme] Purpose in preprocessing pipeline: "Identifying and flagging (or removing) low-quality molecular features using quality metrics defined by Broadhurst et al."
