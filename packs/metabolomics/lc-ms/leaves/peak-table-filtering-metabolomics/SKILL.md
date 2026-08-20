---
name: peak-table-filtering-metabolomics
description: Use when after generating a peak table from XCMS peakTable() output in an untargeted LC-MS metabolomics workflow, if your experimental design includes quality control (QC) samples (SampleType='LQC') and you want to exclude noisy or unstable EICs before building a peak quality classifier.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MetaClean
  - XCMS
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01738-3
  all_source_dois:
  - 10.1007/s11306-020-01738-3
  - 10.1186/1471-2105-15-s11-s5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-filtering-metabolomics

## Summary

Filter extracted ion chromatograms (EICs) from XCMS peak tables by relative standard deviation (RSD) in quality control samples prior to peak quality metric calculation and machine learning classifier training. This optional preprocessing step removes EICs with excessive variability in replicate QC injections, improving downstream peak quality assessment.

## When to use

After generating a peak table from XCMS peakTable() output in an untargeted LC-MS metabolomics workflow, if your experimental design includes quality control (QC) samples (SampleType='LQC') and you want to exclude noisy or unstable EICs before building a peak quality classifier. Use this when RSD values in QC replicates are available and you have a priori knowledge of an acceptable variability threshold (default 0.3 or 30%).

## When NOT to use

- Input peak table lacks quality control (QC) replicates — RSD cannot be computed without replicate measurements in consistent samples.
- EIC intensity values are already normalized or log-transformed in a way incompatible with RSD calculation on original scale.
- Your experimental design does not include replicate QC injections or samples with SampleType='LQC' are not documented in the covariate file.

## Inputs

- XCMS peakTable() output (data.frame with peak intensities across samples)
- Peak table with EIC identifier column
- Covariate file or metadata table with SampleType annotations (e.g., 'LQC' for quality control samples)
- Vector of quality control sample column names
- RSD threshold (numeric, default 0.3)

## Outputs

- Filtered peak table containing only EICs with RSD ≤ threshold
- Subset of original EICs (rows removed if RSD > threshold)

## How to apply

Load the XCMS peak table and add an EIC identifier column. Identify quality control sample column names from the covariate file (samples annotated with SampleType='LQC'). Call rsdFilter() with the peak table, the EIC column name, the vector of QC sample column names, and your chosen RSD threshold (expressed as a fraction; default 0.3 represents 30% RSD). The function computes the RSD of each EIC across QC replicates and retains only those with RSD ≤ the specified threshold. Output is a filtered peak table ready for subsequent peak quality metric calculation and classifier training.

## Related tools

- **XCMS** (Peak detection and alignment tool that produces the peakTable() output; rsdFilter is applied downstream of XCMS preprocessing)
- **MetaClean** (Parent R package containing rsdFilter() function; integrates RSD filtering as an optional preprocessing step before peak quality metric calculation and classifier training) — https://github.com/KelseyChetnik/MetaClean
- **R** (Programming language in which rsdFilter() is implemented and executed)

## Examples

```
rsdFilter(peakTable = pqm_data, eicColumn = 'EICNo', qcSamples = c('LQC_1', 'LQC_2', 'LQC_3'), rsdThreshold = 0.3)
```

## Evaluation signals

- All retained EICs have RSD ≤ threshold; all removed EICs have RSD > threshold (exact agreement with threshold criterion).
- Row count of filtered table ≤ row count of input table (filtering removes rows, never adds).
- No NA or infinite RSD values in retained EICs; check that QC sample columns are non-empty and numeric.
- Summary statistics (mean, median, min, max RSD) of retained EICs cluster below the threshold; summary stats of removed EICs cluster above.
- Filtered peak table preserves all original column structure and sample columns (no columns are dropped, only rows).

## Limitations

- Requires replicate QC samples in the experimental design; single-injection QC samples cannot be used to compute RSD.
- RSD threshold is user-specified and data-dependent; no automated threshold selection is provided. Threshold choice must be justified by QC variability distribution.
- Filtering is applied before peak quality metric calculation, which may remove weak signal EICs even if they are detected and integrate well. The trade-off between noise removal and feature retention depends on the chosen RSD cutoff.
- RSD is sensitive to low-abundance EICs; very faint peaks may exhibit high RSD even if integration is consistent relative to their signal strength.

## Evidence

- [methods] rsdFilter() function overview and purpose: "the user can optionally filter out EICs by RSD % using the rsdFilter() function."
- [other] rsdFilter() inputs and execution workflow: "Call rsdFilter() with the peak table, EIC column name, vector of QC sample column names, and RSD threshold (default 0.3)."
- [other] rsdFilter() output specification: "Output the filtered peak table containing only EICs with RSD below the threshold."
- [other] Validation logic for rsdFilter() correctness: "Confirm that all retained EICs have RSD ≤ threshold and that all filtered-out EICs have RSD > threshold."
- [intro] Integration with XCMS and MetaClean workflow: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
- [readme] MetaClean package scope and design: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
