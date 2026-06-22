---
name: qc-replicate-identification-and-grouping
description: Use when you have a QC-annotated LC-MS feature table (CSV or data frame format with sample metadata) and need to isolate QC replicate measurements prior to computing quality metrics such as D-Ratio or performing signal drift correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R ≥4.1.2
  - R
  - 'OUKS (Step 4: Correction.R)'
  - MetCorR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC Replicate Identification and Grouping

## Summary

Systematically identify and extract quality control (QC) sample replicates from LC-MS metabolomic feature tables to enable computation of batch effect metrics and signal drift assessment. This is a prerequisite step for D-Ratio calculation and QC-based correction in untargeted metabolomics workflows.

## When to use

Apply this skill when you have a QC-annotated LC-MS feature table (CSV or data frame format with sample metadata) and need to isolate QC replicate measurements prior to computing quality metrics such as D-Ratio or performing signal drift correction. Specifically use it in the early Correction phase (step 4 of OUKS) before quality assessment or in Filtering (step 6) when D-Ratio filtering is applied.

## When NOT to use

- Input feature table contains no QC-annotated samples (metadata does not include 'QC' label or equivalent).
- QC replicates are insufficient in number (< 3 replicates) to estimate reliable within-group variance.
- Feature table is already filtered, normalized, or aggregated; use raw intensity values prior to Correction step instead.

## Inputs

- QC-annotated LC-MS feature intensity table (CSV or R data frame)
- Sample metadata table with QC label assignments
- Feature identifiers (m/z, retention time, or compound name)

## Outputs

- Grouped QC replicate feature intensity data frame (features × QC sample replicates)
- QC sample indices or row numbers for cross-referencing with full feature table
- QC subset feature table (CSV or R object) ready for variance/drift analysis

## How to apply

Load the QC-annotated feature intensity table into R as a data frame or matrix, with sample identifiers (rows) and feature m/z × RT values (columns). Extract and index all rows whose sample metadata column (e.g., 'class' or 'sample_type') equals the QC label (typically 'QC'). Verify that QC replicates are present in multiple injections across the analytical batch (e.g., at sequence start, middle, and end) to capture temporal drift patterns. Group replicate intensities by feature identifier so that subsequent variance, correlation, or D-Ratio calculations can be performed on pooled QC measurements. Export or retain this grouped QC subset as a separate data frame with feature IDs and their replicate intensity vectors for downstream metric computation.

## Related tools

- **R** (Primary scripting environment for QC sample subsetting, grouping, and data frame manipulation) — https://cloud.r-project.org/
- **OUKS (Step 4: Correction.R)** (Implements QC identification and D-Ratio metric computation immediately downstream of this grouping step) — https://github.com/plyush1993/OUKS
- **MetCorR** (Receives grouped QC samples to fit GAM-based signal drift correction models on QC replicates across run order and batch) — https://github.com/plyush1993/MetCorR

## Examples

```
# R code snippet from OUKS Step 4 (Correction.R) pattern:
qc_samples <- feature_table[metadata$class == "QC", ]
qc_intensities <- qc_samples[, grep("^mz_", colnames(qc_samples))]
# Export for D-Ratio computation:
write.csv(qc_intensities, "QC_grouped_replicates.csv", row.names = TRUE)
```

## Evaluation signals

- QC subset contains only rows whose sample metadata matches the QC label (e.g., 'class == "QC"'); spot-check first and last rows of output to confirm correct filtering.
- Number of QC replicates per feature is consistent and ≥ 3; inspect the shape of the output data frame (e.g., nrow should equal number of QC samples, ncol should equal number of features).
- Feature identifiers and intensity values are preserved without duplication or loss; compare sum of intensities before and after grouping to confirm no data loss.
- Temporal ordering of QC replicates is retained (if relevant for drift assessment); verify that run order or injection sequence is logged alongside grouped intensities.
- Output format matches the input schema expected by downstream D-Ratio or MetCorR functions (e.g., data frame with feature IDs and replicate intensity columns).

## Limitations

- If QC samples are injected only once at the beginning or end of a batch (not distributed throughout), drift detection and correction will be unreliable.
- Presence of missing values or imputation artifacts in QC replicates can inflate within-group variance estimates; inspect for missing intensity patterns before grouping.
- QC label assignment must be consistent and correctly spelled in metadata; mismatches or typos (e.g., 'QC' vs. 'qc' vs. 'quality_control') will cause QC samples to be missed.
- No automated validation of QC replicate chemical or instrumental consistency; identical QC composition and identical LC-MS parameters are assumed but not verified by this step alone.

## Evidence

- [other] Identify QC sample replicates and extract their feature intensity values: "Identify QC sample replicates and extract their feature intensity values."
- [other] QC-annotated feature table in Correction step: "Load the QC-annotated feature table (CSV or data frame format) into R."
- [other] D-Ratio metric depends on QC group extraction: "Calculate the D-Ratio for each feature as the ratio of between-group variance to within-group variance (or mean intensity in QC replicates to pooled standard deviation across all samples)"
- [readme] QC samples used in MetCorR GAM fitting: "Fitting GAMs on QC samples..."
