---
name: untargeted-metabolomics-data-quality-assessment
description: Use when after imputation and signal drift correction (OUKS steps 3–4),
  when you have a QC-annotated feature intensity table with replicated QC samples
  and need to assess which features have stable, reproducible signals before filtering
  and statistical testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - R ≥4.1.2
  - R
  - OUKS
  - MetCorR
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- '[![](https://img.shields.io/badge/R≥4.1.2-5fb9ed.svg?style=flat&logo=r&logoColor=white?)](https://cran.r-project.org/index.html)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-metabolomics-data-quality-assessment

## Summary

Evaluate feature reliability in QC-annotated LC-MS metabolomic feature tables by computing the D-Ratio quality metric, which quantifies signal stability as the ratio of between-group variance to within-group variance across QC replicates. This metric identifies and removes unreliable features before downstream statistical analysis.

## When to use

After imputation and signal drift correction (OUKS steps 3–4), when you have a QC-annotated feature intensity table with replicated QC samples and need to assess which features have stable, reproducible signals before filtering and statistical testing. Use this skill when technical variation must be distinguished from biological variation to ensure only high-confidence features enter downstream analysis.

## When NOT to use

- Input data lacks QC replicates or QC sample annotations—D-Ratio requires multiple QC measurements to calculate within-group variance.
- Feature table has already been filtered for quality—redundant calculation if D-Ratio filtering has been applied upstream.
- Analysis uses targeted metabolomics with a priori known features and no missing value imputation—D-Ratio is designed for untargeted LC-MS workflows where feature reliability is uncertain.

## Inputs

- QC-annotated feature intensity table (CSV or R data frame with samples as rows, features as columns)
- Sample metadata including QC sample class labels and sample order
- Feature identifiers (m/z, retention time, feature name, or index)

## Outputs

- Per-feature D-Ratio scores (numeric vector or data frame with feature IDs and D-Ratio values)
- D-Ratio table exported as CSV file for downstream filtering

## How to apply

Load the QC-annotated feature intensity table (CSV or R data frame) and identify all QC sample replicates by their sample class label. For each feature, extract intensity values from QC replicates and calculate the D-Ratio as the ratio of between-group variance (or mean intensity in QC replicates) to within-group variance (pooled standard deviation across all samples, including QC and biological samples). Compile per-feature D-Ratio scores into a data frame indexed by feature identifier (m/z, retention time, or feature ID). Export the D-Ratio table to CSV. The resulting D-Ratio scores serve as input to the subsequent Filtering step (OUKS step 6), where a threshold (typically defined by the analyst or data-driven cutoff) is applied to remove features with D-Ratio values below the quality threshold, retaining only reproducible features.

## Related tools

- **R** (Programming environment for loading feature tables, calculating D-Ratio variance components, and exporting results) — https://cran.r-project.org/index.html
- **OUKS** (Complete untargeted metabolomics workflow; step 4 (Correction) implements D-Ratio computation; step 6 (Filtering) applies D-Ratio thresholds) — https://github.com/plyush1993/OUKS
- **MetCorR** (QC-based signal drift correction using GAMs; recommended to run before D-Ratio assessment to remove batch and run-order effects) — https://github.com/plyush1993/MetCorR

## Examples

```
# Load feature table and metadata; calculate D-Ratio per feature in OUKS step 4
# Example R snippet from OUKS workflow:
# data <- read.csv('features_qc_annotated.csv', row.names=1)
# qc_samples <- data[metadata$class == 'QC', ]
# d_ratio <- apply(data, 2, function(x) mean(qc_samples[,colnames(data)==names(x)]) / sd(x))
# d_ratio_table <- data.frame(feature_id=names(d_ratio), D_Ratio=d_ratio)
# write.csv(d_ratio_table, 'D_Ratio_results.csv')
```

## Evaluation signals

- D-Ratio values are positive, finite numbers; no NaN or infinite values indicate computational errors or missing QC replicates.
- Features with high D-Ratio scores (e.g., > median or > user-defined threshold) exhibit lower relative standard deviation in QC replicates compared to biological samples, confirming technical stability.
- D-Ratio table has one row per feature and matches the dimensionality of the input feature table; feature ordering is preserved or explicitly aligned.
- Downstream Filtering step (OUKS step 6) successfully applies D-Ratio thresholds to remove low-quality features, reducing feature count while retaining biologically plausible metabolites.
- RLA plots (Relative Log Abundance plots) or correlogram output from OUKS step 4 (Correction) show improved data distribution after D-Ratio-based filtering, indicating removal of noisy features.

## Limitations

- D-Ratio assumes QC replicates are truly representative of the feature pool; if QC samples are prepared differently or contain contamination, D-Ratio may misclassify features.
- The metric depends on adequate replication; studies with very few QC replicates (< 3) may produce unstable variance estimates, leading to unreliable D-Ratio scores.
- D-Ratio does not account for features with genuine zero values (true absence) vs. missing values or below-detection-limit signals; imputation strategy upstream (OUKS step 3) affects the distribution of intensity values and thus D-Ratio calculation.
- No published sensitivity analysis or benchmarking study is provided in the article or README to recommend optimal D-Ratio thresholds; threshold selection is data-dependent and currently requires expert judgment or exploratory analysis.
- OUKS project is marked as inactive; ongoing maintenance and support for edge cases or new metabolomics standards are not guaranteed.

## Evidence

- [other] OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data: "OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering"
- [other] D-Ratio calculated as ratio of between-group variance to within-group variance: "Calculate the D-Ratio for each feature as the ratio of between-group variance to within-group variance (or mean intensity in QC replicates to pooled standard deviation across all samples), following"
- [other] Workflow: load QC-annotated table, identify replicates, calculate D-Ratio per feature, compile into data frame, export to CSV: "1. Load the QC-annotated feature table (CSV or data frame format) into R. 2. Identify QC sample replicates and extract their feature intensity values. 3. Calculate the D-Ratio for each feature as the"
- [readme] "4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA: ""4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA"
- [readme] "6. Filtering": D-Ratio filtering was added.: ""6. Filtering": D-Ratio filtering was added."
- [readme] R ≥4.1.2 requirement: "The only requirements are to be familiar with the basic syntax of the R language, PC with Internet connection and Windows OS (desirable), [RStudio](https://www.rstudio.com/products/rstudio/download/)"
