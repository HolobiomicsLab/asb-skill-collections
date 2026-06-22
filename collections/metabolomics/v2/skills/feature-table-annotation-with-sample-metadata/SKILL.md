---
name: feature-table-annotation-with-sample-metadata
description: Use when your input is a feature intensity table (CSV or R data frame) with features as columns and samples as rows, and you have accompanying sample metadata (batch identifiers, QC/study sample labels, run order, sample phenotypes, collection dates).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3336
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - OUKS (Omics Untargeted Key Script)
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
---

# feature-table-annotation-with-sample-metadata

## Summary

Annotate metabolomic feature tables with sample-level metadata (e.g., QC labels, batch, run order, phenotype) to enable stratified quality assessment, signal drift correction, and batch effect removal during LC-MS untargeted metabolomics processing. This skill bridges raw feature intensity matrices with experimental design information required for QC-aware correction and filtering.

## When to use

Your input is a feature intensity table (CSV or R data frame) with features as columns and samples as rows, and you have accompanying sample metadata (batch identifiers, QC/study sample labels, run order, sample phenotypes, collection dates). You need to link these two sources before applying QC-based correction (step 4 in OUKS) or before stratified filtering (step 6). The metadata should encode sample types (e.g., 'QC' vs. case/control) and technical variables (run order, batch) that explain systematic variation.

## When NOT to use

- Input is already a single integrated R object with metadata columns embedded (e.g., output from a prior OUKS step); re-merging risks duplication or inconsistency.
- Sample metadata is incomplete or contradictory (e.g., QC samples labeled as different batches, missing run order); resolve metadata quality before annotation.
- Feature table and metadata have no common sample identifier; annotation will fail or produce silent misalignment.

## Inputs

- Feature intensity table (CSV or R data frame): rows=samples, columns=metabolic features, values=intensity or area under curve
- Sample metadata table (CSV or R data frame): rows=samples, columns include sample identifier, 'class' (QC/study sample type), 'batch' (batch/cohort), 'order' (run sequence)

## Outputs

- Merged annotated feature table (R data frame): features as columns, samples as rows, with metadata columns (class, batch, order, etc.) appended or linked by row name
- Optional: validated metadata mapping file (CSV) documenting sample ID correspondence and completeness check results

## How to apply

Load the feature intensity table (CSV format) and the corresponding metadata table (containing sample identifiers matching row names in the feature table, plus columns for 'class' indicating sample type, 'batch' for batch/cohort assignments, and 'order' for run sequence). Merge the two by sample identifier into a unified R data frame, ensuring all samples in the intensity table have a corresponding metadata row and vice versa. Validate the merge by checking for missing values in critical metadata fields (especially 'class' and batch indicators). Store the merged data frame or pass it directly to downstream OUKS steps (e.g., step 4 Correction.R or step 6 Filtering.R). The metadata enables algorithms like QC-GAM (used in MetCorR step 4) to fit signal drift models using QC replicates and to stratify feature filtering by batch and sample type in step 6. Rationale: QC-annotated metabolomics requires explicit labeling of QC replicates and batch structure so that quality metrics (e.g., D-Ratio) and correction models can distinguish biological signal from technical drift without confounding study samples.

## Related tools

- **R** (Scripting language for loading, merging, and validating feature tables and metadata; used in OUKS steps 1–9) — https://cran.r-project.org/index.html
- **OUKS (Omics Untargeted Key Script)** (Nine-step untargeted metabolomics pipeline; steps 4 (Correction) and 6 (Filtering) consume annotated feature tables with metadata) — https://github.com/plyush1993/OUKS
- **MetCorR** (QC-based signal drift correction using GAMs; accepts intensity data and metadata (order, batch, class, qc_label) to fit correction models) — https://github.com/plyush1993/MetCorR

## Examples

```
# Load and merge in R
intensity <- read.csv('features.csv', row.names=1)
metadata <- read.csv('metadata.csv', row.names=1)
merged <- cbind(intensity, metadata)
# Or pass separately to MetCorR:
out <- MetCorR(method=2, int_data=intensity, order=metadata$order, class=metadata$class, batch=metadata$batch, qc_label='QC')
```

## Evaluation signals

- No row misalignment: verify row names or sample IDs in merged table match both original feature table and metadata table; use `all.equal(rownames(intensity), rownames(metadata))` in R.
- Metadata completeness: all rows have non-missing values in critical columns ('class', 'batch', 'order'); check with `sapply(metadata, function(x) sum(is.na(x))) == 0`.
- QC label consistency: verify that samples labeled 'QC' in the class column form a coherent technical replicate set (e.g., same batch, distributed across run order); unexpected QC assignments indicate annotation error.
- Feature table dimensions preserved: merged table retains all original features and samples; confirm `nrow(merged) == nrow(intensity)` and `ncol(merged) >= ncol(intensity) + ncol(metadata) - 1` (accounting for shared ID column).
- Downstream compatibility: pass merged table to MetCorR::MetCorR() or OUKS step 4/6 scripts; successful execution without 'sample not found' or dimension mismatch errors confirms correct annotation.

## Limitations

- Metadata structure is not validated against OUKS expectations; if 'class' column uses non-standard labels (e.g., 'QC_sample' vs. 'QC'), downstream QC-GAM algorithms may fail silently or mislabel QC samples.
- No explicit guidance in the article on handling missing or duplicate sample identifiers in metadata; the user must manually audit the merge.
- The article does not specify acceptable batch size thresholds or minimum number of QC replicates per batch; small or unbalanced QC distributions may compromise correction model fitting in step 4.
- The OUKS project is marked as 'Inactive'; support and maintenance are not guaranteed, and metadata schema may differ between versions.

## Evidence

- [other] Load the QC-annotated feature table (CSV or data frame format) into R. Identify QC sample replicates and extract their feature intensity values.: "Load the QC-annotated feature table (CSV or data frame format) into R. Identify QC sample replicates and extract their feature intensity values."
- [other] D-Ratio metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering is applied.: "OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering"
- [readme] run correction (method = 2 uses both run order and batch); MetCorR function accepts int_data, order, class, batch, qc_label parameters.: "out <- MetCorR( method = 2, int_data = example_intensity, order = example_meta$order, class = example_meta$class, batch = example_meta$batch, qc_label = "QC" )"
- [other] Nine step LC-MS untargeted metabolomic profiling data processing; step 4 Correction uses D-Ratio metric, RLA-plot, correlogram, 2-factors PCA; step 6 Filtering uses D-Ratio filtering.: "comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox; "4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA; "6. Filtering": D-Ratio filtering was"
- [readme] Datasets in .csv format are available for reproducibility from corresponding folders. Metadata table is also provided.: "[Datasets](https://github.com/plyush1993/OUKS/tree/main/Datasets%20(csv)) in .csv and [other files]... [`Metadata`](https://github.com/plyush1993/OUKS/blob/main/Datasets%20(csv)/metadata.csv) table"
