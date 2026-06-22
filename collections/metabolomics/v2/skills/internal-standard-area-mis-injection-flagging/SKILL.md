---
name: internal-standard-area-mis-injection-flagging
description: Use when after building a SummarizedExperiment object containing LC-MS peak areas and internal standard assignments, when you need to identify study samples with anomalous Internal Standard signal (indicating syringe failure, capillary clogging, or injection system malfunction) before applying.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality is a user-friendly R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# internal-standard-area-mis-injection-flagging

## Summary

Detect and flag mis-injected study samples in metabolomics LC-MS data by testing whether Internal Standard peak areas fall outside expected ranges, identifying technical failures that compromise quantitation reliability.

## When to use

After building a SummarizedExperiment object containing LC-MS peak areas and internal standard assignments, when you need to identify study samples with anomalous Internal Standard signal (indicating syringe failure, capillary clogging, or injection system malfunction) before applying batch correction or concentration calculations.

## When NOT to use

- Input samples have no assigned internal standards or lack Internal Standard peak area measurements.
- All study samples have uniform Internal Standard areas (no variance to detect outliers).
- You are analyzing only QC or calibration-line samples; mis-injection testing is specific to Study Samples.

## Inputs

- SummarizedExperiment object with assay containing Internal Standard peak areas
- colData with sample type annotations (Study Sample vs. QC vs. Calibration Line)
- rowData mapping compounds to assigned internal standards

## Outputs

- SummarizedExperiment with colData$use column marked FALSE for flagged mis-injected samples
- Metadata annotations in colData identifying detected outliers and mis-injection status

## How to apply

Invoke doAnalysis with removeOutliers=TRUE on a SummarizedExperiment containing study samples with assigned internal standards. The function calculates the median Internal Standard area across all study samples in each batch, then tests each study sample's Internal Standard area against this batch median using statistical outlier detection (Rosner Test). Samples flagged as outliers (with extremely low or high Internal Standard areas) are marked with metadata annotations in the colData slot, indicating potential mis-injection. These flagged samples should be excluded from downstream analyses (via the 'use' column in colData) or investigated manually. The rationale is that internal standards are spiked at constant amounts; deviation signals instrumental failure rather than biological variation.

## Related tools

- **mzQuality** (Implements doAnalysis function for outlier detection and flagging of mis-injected study samples using Internal Standard areas) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor object class used to store peak areas, sample metadata, and outlier flags in colData and rowData slots)
- **mzQualityDashboard** (Interactive Shiny application providing visualization and manual curation of flagged mis-injected samples) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers = TRUE, useWithinBatch = TRUE); flagged_samples <- exp$use == FALSE; exp_filtered <- exp[, exp$use]
```

## Evaluation signals

- Flagged study samples (colData$use = FALSE) have Internal Standard areas > 2–3 standard deviations from batch median.
- Rosner Test p-value for flagged samples is < 0.05, confirming statistical significance of the outlier.
- Samples with extremely low Internal Standard areas (< 10% of batch median) correspond to known injection system failures or manual notes in the lab notebook.
- After filtering flagged samples, batch-corrected assays (ratio_corrected) show reduced variance in QC sample ratios (RSDQC improvement).
- Manual inspection of chromatograms or instrument logs confirms technical anomalies (e.g., syringe blockage, column pressure spike) on flagged injection dates.

## Limitations

- Mis-injection detection relies on Internal Standard area alone; if the internal standard itself is unstable or co-elutes with matrix, false positives may occur.
- The method assumes all study samples receive the same injection volume and internal standard amount; variable internal standard addition will confound outlier detection.
- In batches with very few study samples (n < 5), the batch median is unreliable and the Rosner Test may lack statistical power.
- Outlier flagging is applied only to Study Samples; QC samples are tested separately using Compound/Internal Standard ratios, not raw Internal Standard areas.

## Evidence

- [intro] Study Samples are tested for mis-injections using their Internal Standard areas.: "Furthermore, Study Samples are tested for mis-injections using their Internal Standard areas."
- [intro] The doAnalysis function with removeOutliers=TRUE flags QC and study sample outliers.: "Invoke doAnalysis with parameters removeOutliers=TRUE to flag QC sample outliers based on Compound/Internal Standard ratios"
- [intro] Output includes metadata marking detected outliers and mis-injected samples.: "Generate output SummarizedExperiment containing the 'ratio_corrected' assay with batch-corrected compound/internal-standard ratios and metadata annotations marking detected outliers and mis-injected"
- [other] Selection is based on Rosner Test for statistical outliers in QC samples.: "For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples."
- [other] The 'use' column in colData and rowData indicates reliability for reporting.: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
