---
name: relative-standard-deviation-calculation-qc-replicates
description: Use when you have a peak table from XCMS preprocessing with intensity measurements for the same set of metabolites across multiple QC replicate injections (samples marked SampleType='LQC'), and you need to filter out EICs with poor reproducibility before evaluating peak quality or training a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MetaClean
  - XCMS
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- getEvalObj is called to extract the relevant data from the three objects provided by ther user and store them in an object of class evalObj
- It is an R package and can be easily incorporated
- MetaClean is a package for building classifiers to identify low quality integrations in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package `caret`) for building a predictive model.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  dedup_kept_from: coll_metaclean_cq
schema_version: 0.2.0
---

# relative-standard-deviation-calculation-qc-replicates

## Summary

Calculate relative standard deviation (RSD) of peak intensities across quality control (QC) replicates to assess reproducibility of extracted ion chromatograms in untargeted LC-MS metabolomics. RSD is used as a filtering criterion to exclude low-reproducibility EICs prior to peak quality metric calculation and machine learning classifier training.

## When to use

You have a peak table from XCMS preprocessing with intensity measurements for the same set of metabolites across multiple QC replicate injections (samples marked SampleType='LQC'), and you need to filter out EICs with poor reproducibility before evaluating peak quality or training a classifier to detect low-quality integrations.

## When NOT to use

- QC replicate samples are not available in the dataset; RSD calculation requires at least 2 QC replicate measurements per EIC.
- Peak table has already been pre-filtered or normalized by external methods that alter intensity distributions, as this may invalidate RSD-based filtering assumptions.
- Analysis goal is to preserve all detected features regardless of reproducibility, such as in discovery screening for rare metabolites.

## Inputs

- Peak table from XCMS peakTable() output with intensity measurements
- Covariate or phenotype file identifying QC sample column names (SampleType='LQC')
- RSD threshold percentage (default 0.3 or 30%)

## Outputs

- Filtered peak table containing only EICs with RSD ≤ threshold
- RSD values for each retained EIC

## How to apply

Extract the intensity columns corresponding to QC replicate samples from the peak table. For each EIC (row), compute the mean and standard deviation of intensity values across the QC replicates, then calculate RSD as (standard deviation / mean) × 100. Compare each EIC's RSD to a user-specified threshold (default 0.3, or 30%). Retain only EICs with RSD ≤ threshold; exclude those exceeding the threshold. This filtering is applied before calculating the 12 peak-quality metrics or training machine learning classifiers, as a way to reduce noise from poorly reproducible chromatographic integrations.

## Related tools

- **MetaClean** (R package that implements the rsdFilter() function for optional RSD-based filtering of EICs prior to peak quality evaluation) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (Generates the peak table input from which EIC intensities are extracted for RSD calculation)
- **R** (Programming language; rsdFilter() is implemented as an R function within MetaClean)

## Examples

```
rsdFilter(peakTable = peak_table, eicColumn = 'EICNo', qcSampleNames = c('LQC_rep1', 'LQC_rep2', 'LQC_rep3'), rsdThreshold = 0.3)
```

## Evaluation signals

- All retained EICs have RSD ≤ the specified threshold; all filtered-out EICs have RSD > threshold.
- The number and proportion of filtered-out EICs are consistent with the expected distribution of reproducibility in the dataset.
- Comparison of peak quality metric distributions or classifier performance before and after RSD filtering shows improvement in signal-to-noise or reproducibility metrics.
- Visual inspection of box plots or violin plots of RSD values shows a clear separation between retained and removed EICs at the threshold cutoff.
- RSD values for QC replicates are recalculated independently and agree with stored RSD values (within numerical precision).

## Limitations

- RSD threshold is user-specified and may require optimization for different LC-MS platforms, metabolite classes, or sample preparation protocols.
- Calculation assumes intensity values are normally distributed or can be approximated by mean and standard deviation; highly skewed or multimodal distributions may violate this assumption.
- RSD filtering discards potentially valid rare metabolites or features with inherently low reproducibility, which may be biologically relevant in some contexts.
- The method assumes QC replicate samples are truly technical replicates with identical preparation and injection; confounding biological or technical variation in QC samples will inflate RSD estimates.

## Evidence

- [methods] the user can optionally filter out EICs by RSD % using the rsdFilter() function: "the user can optionally filter out EICs by RSD % using the rsdFilter() function."
- [other] Call rsdFilter() with peak table, QC sample names, and RSD threshold to remove poor-reproducibility EICs: "Call rsdFilter() with the peak table, EIC column name, vector of QC sample column names, and RSD threshold (default 0.3)."
- [other] Validation requires confirming retained EICs meet RSD cutoff and removed EICs exceed it: "Confirm that all retained EICs have RSD ≤ threshold and that all filtered-out EICs have RSD > threshold."
- [other] Filtering step removes EICs prior to peak quality metric calculation: "removes extracted ion chromatograms (EICs) based on a relative standard deviation (RSD) percentage threshold specified by the user prior to subsequent peak quality metric calculation and classifier"
- [methods] RSD filtering is an optional preprocessing step in the MetaClean workflow: "(Optional) RSD Filtering"
