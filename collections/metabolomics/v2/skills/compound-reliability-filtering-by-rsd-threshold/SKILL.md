---
name: compound-reliability-filtering-by-rsd-threshold
description: Use when apply this filter after batch correction of compound/internal-standard
  ratios when you have pooled study quality control (SQC) samples and need to determine
  which compounds are sufficiently reproducible for downstream reporting. Use it specifically
  when the nonReportableRSD threshold (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# compound-reliability-filtering-by-rsd-threshold

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter metabolomics compounds based on Relative Standard Deviation (RSD) of pooled quality-control (QC) samples to exclude unreliable analytes before reporting. This is a core reliability gate in batch-corrected mass spectrometry data that removes compounds with excessive measurement variability in QC replicates.

## When to use

Apply this filter after batch correction of compound/internal-standard ratios when you have pooled study quality control (SQC) samples and need to determine which compounds are sufficiently reproducible for downstream reporting. Use it specifically when the nonReportableRSD threshold (e.g., 30%) has been set in doAnalysis and you are deciding which compounds in rowData$use should be marked TRUE (reliable) or FALSE (unreliable).

## When NOT to use

- When you have no pooled QC samples or replicates; RSD calculation requires variance in QC sample measurements.
- When the input data has not been batch-corrected; filtering on raw (unbatched) RSD may retain systematic batch-dependent noise.
- When your goal is exploratory discovery rather than reporting; filtering before univariate/multivariate analysis may remove valid signals with high biological variance.

## Inputs

- SummarizedExperiment object (post-doAnalysis with batch-corrected ratio assay)
- rowData table containing RSDQC values and compound reliability metrics
- nonReportableRSD threshold parameter (numeric, e.g., 30 for 30%)

## Outputs

- SummarizedExperiment with updated rowData$use column (TRUE/FALSE per compound)
- Subset SummarizedExperiment containing only reliable compounds
- Report annotations indicating which compounds failed RSD thresholds

## How to apply

After running doAnalysis with your chosen parameters (e.g., removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE), mzQuality automatically calculates the Relative Standard Deviation of batch-corrected ratios for each compound using QC replicates (RSDQC). Compounds are flagged for exclusion if RSDQC exceeds the nonReportableRSD threshold (default 30%). This decision combines three metrics: (1) RSDQC value itself, (2) background signal percentage (vs. the backgroundPercentage threshold, e.g., 40%), and (3) presence of the compound in QC samples. The package stores the decision in the rowData 'use' column; you can override these flags manually or use the automated selection by subsetting exp[rowData(exp)$use, ]. The rationale is that compounds with high RSD in QC samples indicate poor batch correction or inherent analytical noise, making them unfit for quantitative reporting.

## Related tools

- **mzQuality** (R package that performs doAnalysis with RSDQC calculation and rowData$use assignment; implements the nonReportableRSD filtering logic automatically.) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container for storing compound assays, rowData (compound metadata including RSDQC and use flags), and colData.)
- **mzQualityDashboard** (Interactive Shiny application layered on mzQuality for users who prefer GUI-based filtering without direct R code.) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, backgroundPercentage=40, nonReportableRSD=30); exp_filtered <- exp[rowData(exp)$use, exp$use]
```

## Evaluation signals

- Verify that rowData(exp)$use contains only TRUE for compounds with RSDQC ≤ nonReportableRSD threshold and FALSE for compounds exceeding it (or failing combined background/presence filters).
- Check that the subset exp[rowData(exp)$use, ] returns a valid SummarizedExperiment with fewer rows (compounds) than the input.
- Confirm that createReports output Reports subdirectory contains compound lists stratified by confidence level (High Confidence, Caution, Low SNR, Not Reported) and that Not Reported compounds match those with use=FALSE.
- Validate that batch-corrected ratio_corrected assay values for flagged compounds show visibly higher within-QC variance (higher SD of QC sample values) compared to retained compounds.
- Ensure that when nonReportableRSD is lowered (more stringent), the count of use=TRUE compounds decreases monotonically.

## Limitations

- RSDQC filtering assumes that QC sample replicates represent true analytical variability; if QC samples are not truly representative of the matrix, the threshold may be incorrectly set.
- Only one sample type can be used for calculating concentrations in the current version of mzQuality; filtering decisions based on RSD do not account for sample-type-specific variability.
- The combined filtering logic (RSDQC + background% + presence in QC) is not fully decomposed in the output; it is difficult to distinguish which metric caused a compound to be marked use=FALSE without examining rowData directly.
- Compounds with low absolute abundance may have naturally high RSD and be filtered even if they are genuine analytes; the threshold does not adapt to dynamic range.

## Evidence

- [intro] mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's.: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's."
- [readme] It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in doAnalysis.: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
- [other] doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using Compound/Internal Standard ratio.: "doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers"
- [readme] mzQuality adds a column called use in both the rowData and colData slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is reliable for reporting based on the set thresholds.: "mzQuality adds a column called use in both the rowData and colData slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is reliable for"
- [other] Apply qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 thresholds to define acceptable analyte reliability and measurement variability.: "Apply qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 thresholds to define acceptable analyte reliability and measurement variability."
