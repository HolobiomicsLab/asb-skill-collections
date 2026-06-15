---
name: batch-corrected-data-extraction
description: Use when after batch correction has been applied to metabolomics data using pooled SQC samples, and you need to retrieve the corrected ratios (compound / internal standard) for quality metrics calculation, internal standard recommendation, concentration estimation, or statistical modelling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3196
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality is a user-friendly R package
- mzQuality requires a specific format for the input data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
---

# batch-corrected-data-extraction

## Summary

Extract batch-corrected compound/internal-standard ratios and their metadata from a SummarizedExperiment object after pooled study quality control (SQC) sample-based batch correction. This skill enables downstream analyses requiring normalized, drift-corrected abundance data.

## When to use

After batch correction has been applied to metabolomics data using pooled SQC samples, and you need to retrieve the corrected ratios (compound / internal standard) for quality metrics calculation, internal standard recommendation, concentration estimation, or statistical modelling. Specifically triggered when the SummarizedExperiment contains 'ratio_corrected' assays and you require access to the corrected values along with their batch-correction metadata.

## When NOT to use

- Input SummarizedExperiment has not yet undergone batch correction (e.g., only raw or unnormalized ratios are available).
- You require uncorrected (raw) ratio values for comparing batch-corrected vs. uncorrected performance.
- Analysis goal is to assess or evaluate the batch-correction method itself rather than use corrected data for downstream tasks.

## Inputs

- SummarizedExperiment object with batch-corrected assays (ratio_corrected slot)
- rowData containing compound metadata and assigned internal standards
- colData containing sample metadata and batch annotations

## Outputs

- Matrix of batch-corrected compound/internal-standard ratios (compounds × samples)
- Subset matrices filtered by sample type (e.g., QC samples only)
- Batch-correction metadata (internal standard assignments, batch labels)

## How to apply

Load the batch-corrected SummarizedExperiment object that was produced by mzQuality's batch-correction step (typically via `doAnalysis`). The corrected ratios are stored in the 'ratio_corrected' assay slot. Extract the assay matrix using standard SummarizedExperiment accessors (e.g., `assay(exp, 'ratio_corrected')`), which will contain compounds as rows and samples (QC, study samples, aliquots) as columns. Access the batch-correction metadata stored in `rowData()` and `colData()` slots to understand which internal standard was used per compound and which samples belong to which batch. Filter or subset the extracted data by sample type (e.g., QC samples only) as needed for downstream calculations such as relative standard deviation (RSD) computation or concentration modelling.

## Related tools

- **mzQuality** (Performs batch correction using pooled SQC samples and stores corrected ratios in SummarizedExperiment assay slots.) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Container object that stores batch-corrected assays, rowData (compound metadata), and colData (sample metadata).) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny interface for visualizing and extracting batch-corrected data without requiring programmatic access.) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
# Extract batch-corrected ratios from SummarizedExperiment
exp <- doAnalysis(exp = exp)
corrected_ratios <- assay(exp, 'ratio_corrected')
qc_corrected <- corrected_ratios[, exp$sample_type == 'QC']
head(qc_corrected)
```

## Evaluation signals

- Extracted 'ratio_corrected' assay matrix has same dimensions (compounds × samples) as the input SummarizedExperiment.
- All corrected ratio values are numeric and within expected ranges (no NaN or Inf unless expected from missing data).
- rowData includes internal standard assignments for each compound; colData includes batch labels consistent with SQC-based correction.
- QC sample subsets (filtered by colData sample type) show reduced variance in corrected ratios compared to raw ratios, confirming batch correction was applied.
- Metadata in rowData and colData traces back to original input data, confirming no information loss during extraction.

## Limitations

- Batch correction in mzQuality relies on pooled SQC samples; if SQC samples are absent, biased, or insufficient in number, corrected ratios may not be reliable.
- The skill requires that batch correction has already been performed; it cannot recover or infer corrected values if the input SummarizedExperiment only contains raw ratios.
- Only one internal standard per compound is assigned; if multiple internal standards are needed or if the assigned standard is unsuitable, the corrected ratios may not be optimal for all downstream analyses.

## Evidence

- [other] Load the batch-corrected SummarizedExperiment object containing QC sample ratios (compound / internal standard) and their batch-correction metadata.: "Load the batch-corrected SummarizedExperiment object containing QC sample ratios (compound / internal standard) and their batch-correction metadata."
- [other] mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound.: "mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound"
- [intro] batch-correction using pooled study quality control samples (SQC): "batch-correction using pooled study quality control samples (SQC)"
- [intro] Internally, mzQuality uses Bioconductors' SummarizedExperiment object to store the data.: "Internally, mzQuality uses Bioconductors' SummarizedExperiment object to store the data."
- [readme] All calculations will be added to the assay, rowData and colData slots of the experiment, or overwrite the values if they are already present.: "All calculations will be added to the assay, rowData and colData slots of the experiment, or overwrite the values if they are already present."
