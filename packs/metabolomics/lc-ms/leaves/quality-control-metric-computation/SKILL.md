---
name: quality-control-metric-computation
description: Use when after feature integration and imputation when you have QC-annotated
  LC-MS feature intensity data (CSV or data frame format) with replicate QC samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - OUKS step 4 (Correction.R)
  - OUKS step 6 (Filtering.R)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# quality-control-metric-computation

## Summary

Compute the D-Ratio quality metric for LC-MS metabolomic features using QC sample replicates to assess feature reliability and signal consistency. The D-Ratio quantifies the ratio of between-group variance to within-group variance, enabling downstream filtering of unreliable features in the Correction step of untargeted metabolomics workflows.

## When to use

Apply this skill after feature integration and imputation when you have QC-annotated LC-MS feature intensity data (CSV or data frame format) with replicate QC samples. Use it to generate per-feature quality scores before the Filtering step (step 6), especially when technical variation and signal drift need to be characterized in metabolomic profiling studies.

## When NOT to use

- Input lacks QC sample replicates or QC annotations — D-Ratio requires replicate QC measurements to estimate within-group variance.
- Feature table has already been filtered by quality metrics — applying D-Ratio computation post-filtering on a reduced feature set may bias the variance estimates.
- Study design includes only single QC injections per batch — insufficient replication to reliably estimate pooled standard deviation.

## Inputs

- QC-annotated feature intensity table (CSV or R data frame)
- Sample metadata with QC replicate identifiers
- Feature identifiers and their corresponding intensity vectors

## Outputs

- D-Ratio data frame (feature ID × D-Ratio score)
- D-Ratio CSV export file for downstream filtering

## How to apply

Load the QC-annotated feature table into R and identify all QC sample replicates by their sample class label. For each feature, extract the intensity values from QC replicates and calculate the D-Ratio as the ratio of mean intensity in QC replicates to pooled standard deviation across all samples (or equivalently, between-group variance to within-group variance). Compile the per-feature D-Ratio values into a data frame indexed by feature identifier. Export the D-Ratio table to CSV format for downstream use in the Filtering step, where D-Ratio thresholds are applied to remove features with low quality scores.

## Related tools

- **R** (Computing environment for D-Ratio calculation and data frame manipulation) — https://cloud.r-project.org/
- **OUKS step 4 (Correction.R)** (Implements D-Ratio metric computation within the nine-step LC-MS workflow) — https://github.com/plyush1993/OUKS/blob/main/Scripts%20(R)/4.%20Correction.R
- **OUKS step 6 (Filtering.R)** (Applies D-Ratio thresholds to filter unreliable features post-computation) — https://github.com/plyush1993/OUKS/blob/main/Scripts%20(R)/6.%20Filtering.R

## Examples

```
# Load feature table and metadata in R; extract QC replicates and compute D-Ratio
qc_samples <- metadata[metadata$class == "QC", ]
for (feature in colnames(feature_table)) {
  qc_intensity <- feature_table[rownames(feature_table) %in% qc_samples$sample_id, feature]
  d_ratio[feature] <- mean(qc_intensity) / sd(feature_table[[feature]])
}
write.csv(d_ratio, "D-Ratio_metrics.csv")
```

## Evaluation signals

- D-Ratio values are numeric, non-negative, and assigned to every feature in the input table with no missing values
- QC replicate samples produce lower D-Ratio variance than technical replicates across the full sample set, indicating consistent QC signal
- D-Ratio distribution shows expected separation: high-quality features (D-Ratio > threshold) retain signal, low-quality features (D-Ratio < threshold) are enriched in noise or artifacts
- CSV export preserves feature identifiers and D-Ratio scores in consistent row order matching the input feature table
- Downstream Filtering step (step 6) successfully removes features below the D-Ratio cutoff without errors or data loss

## Limitations

- D-Ratio computation assumes QC replicates are representative of biological and technical variance across all samples; poor QC design (e.g., QC replicates do not span full batch) may yield biased estimates.
- D-Ratio is sensitive to missing values in QC replicates; if imputation was performed (step 3), artificially reduced variance in imputed QC values may inflate D-Ratio scores.
- No guidance provided in the article on parameter selection or D-Ratio threshold cutoff for filtering — threshold determination is left to practitioner discretion.
- D-Ratio does not account for feature-specific factors such as ionization efficiency or chromatographic behavior; a single threshold may not be optimal across all chemical classes.

## Evidence

- [other] OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering is applied to remove unreliable features.: "OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering"
- [other] Calculate the D-Ratio for each feature as the ratio of between-group variance to within-group variance (or mean intensity in QC replicates to pooled standard deviation across all samples), following the OUKS step 4 (Correction) metric definition.: "Calculate the D-Ratio for each feature as the ratio of between-group variance to within-group variance (or mean intensity in QC replicates to pooled standard deviation across all samples)"
- [readme] "4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA: ""4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA"
- [readme] comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox"
- [readme] The only requirements are to be familiar with the basic syntax of the R language, PC with Internet connection and Windows OS (desirable), RStudio and R (≥ 4.1.2).: "The only requirements are to be familiar with the basic syntax of the R language, PC with Internet connection and Windows OS (desirable), RStudio and R (≥ 4.1.2)."
