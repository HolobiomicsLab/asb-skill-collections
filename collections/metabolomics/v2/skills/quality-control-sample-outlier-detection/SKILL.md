---
name: quality-control-sample-outlier-detection
description: Use when you have a SummarizedExperiment object containing pooled quality
  control samples with measured compound and internal standard peak areas.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  techniques:
  - mass-spectrometry
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-sample-outlier-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated detection and flagging of statistical outliers in pooled quality control (QC) samples using Compound/Internal Standard ratios in metabolomics mass spectrometry data. This skill identifies unreliable QC measurements that deviate significantly from the expected distribution, enabling informed decisions about sample retention or exclusion before batch correction and downstream analysis.

## When to use

Apply this skill when you have a SummarizedExperiment object containing pooled quality control samples with measured compound and internal standard peak areas. Use it if QC sample consistency is critical for validating batch correction or if you need to flag potentially mis-injected or degraded QC aliquots before calculating correction factors.

## When NOT to use

- If no pooled quality control samples are present in the experiment—outlier detection requires QC replicates to establish a reference distribution.
- If internal standard areas are missing or unreliable—the skill depends on accurate IS measurements to compute robust ratios.
- If you intend to apply QC-based batch correction before outlier removal—flagged outliers should be excluded from the correction reference pool, not corrected and then removed.

## Inputs

- SummarizedExperiment object with assay containing compound peak areas and internal standard areas
- colData containing sample type annotations (e.g., 'QC', 'Study Sample')
- rowData containing compound and internal standard identifiers

## Outputs

- SummarizedExperiment with updated colData containing 'use' column (TRUE/FALSE per sample)
- Metadata annotations marking detected outliers in QC samples
- Intermediate ratio assay (Compound/Internal Standard) used for outlier calculation

## How to apply

Invoke doAnalysis with removeOutliers=TRUE on a SummarizedExperiment containing QC sample data. The function calculates the Compound/Internal Standard ratio for each QC sample, then applies the Rosner test to identify statistical outliers based on deviation from the central distribution of these ratios. Set the outlier detection sensitivity (if exposed in parameters) according to your tolerance for false positives vs. detection power. The function returns the input experiment with a 'use' column added to colData, marking each QC sample TRUE (reliable) or FALSE (outlier flagged). Examine the flagged samples visually using compoundPlot or aliquotPlot to confirm outliers reflect genuine technical problems (e.g., crystal formation, evaporation, mis-injection) before proceeding to batch correction. Only QC samples with use=TRUE should be used as references for within-batch normalization.

## Related tools

- **mzQuality** (Primary implementation package; doAnalysis function performs Rosner test-based outlier detection on QC Compound/IS ratios) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Data container; stores assays, rowData, and colData with outlier flags)
- **mzQualityDashboard** (Interactive visualization interface for inspecting flagged outliers and their ratios) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers = TRUE, useWithinBatch = TRUE)
```

## Evaluation signals

- colData(exp)$use contains exactly two values (TRUE/FALSE); all non-QC samples retain TRUE by default; only QC samples may be FALSE.
- The number of flagged QC outliers is reasonable relative to the total QC sample count (typically <5% of QC samples flagged under normal conditions).
- Compound/Internal Standard ratios of FALSE-flagged samples visually deviate from the central cluster when plotted (compoundPlot or pcaPlot output shows separation).
- Flagged outliers correlate with documented technical events (e.g., batch entry notes, instrumental maintenance logs, obvious evaporation or precipitation).
- Subsetting exp[, exp$use] removes the flagged QC samples and improves the consistency of ratio_corrected assay values across remaining study samples.

## Limitations

- Outlier detection depends on the Rosner test's assumptions; small QC sample sets (<10 replicates) may have reduced statistical power to detect true outliers.
- Internal Standard areas must be measured reliably; if IS response is itself unstable or missing, ratio-based detection will fail or flag spurious outliers.
- The skill detects statistical outliers but cannot distinguish between genuine analytical failures (mis-injection, hardware malfunction) and real biological variation in pooled QC; manual inspection is required to confirm.
- Only one sample type can be used for calculating concentrations in the current version, which may limit retrospective re-analysis if mixed-type QC pools are used.

## Evidence

- [intro] The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio.: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio."
- [other] doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using Compound/Internal Standard ratio: "doAnalysis with parameters removeOutliers=TRUE to flag QC sample outliers based on Compound/Internal Standard ratios"
- [readme] For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples.: "For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples."
- [readme] mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is reliable for reporting based on the set thresholds.: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value"
