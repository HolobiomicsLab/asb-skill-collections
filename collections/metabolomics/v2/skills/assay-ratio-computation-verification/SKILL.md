---
name: assay-ratio-computation-verification
description: Use when after calling buildExperiment on metabolomics data to construct a SummarizedExperiment object, before performing batch correction, outlier detection, or other QC calculations that depend on ratio assay values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality is a user-friendly R package
- mzQuality requires a specific format for the input data.
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
---

# assay-ratio-computation-verification

## Summary

Verify that the ratio assay (compound area divided by internal standard area) is correctly computed in a SummarizedExperiment object, including validation of default behavior when no secondary assay is provided. This skill ensures the mathematical correctness of the normalized compound/internal standard ratios before downstream QC analyses.

## When to use

After calling buildExperiment on metabolomics data to construct a SummarizedExperiment object, before performing batch correction, outlier detection, or other QC calculations that depend on ratio assay values. Essential when verifying the behavior of internal standard normalization, especially when testing edge cases such as missing or unspecified secondary assay columns.

## When NOT to use

- When the input is already a SummarizedExperiment object without need for re-construction—use existing assay slots directly instead.
- When only raw compound areas are needed and internal standard normalization is not intended for the downstream analysis.
- When secondary assay (internal standard) data are not available or present in the dataset—skip ratio verification and work with primary assay only.

## Inputs

- tab-delimited metabolomics data file (TSV format)
- data frame from readData function with mandatory columns for compounds, samples, and assay values
- optionally: column name specification for primary and secondary assays

## Outputs

- SummarizedExperiment object with validated 'ratio' assay
- element-wise comparison report confirming ratio = primary / secondary (or primary if secondary absent)
- validation boolean or summary table confirming all ratios are computed correctly

## How to apply

Load metabolomics data using readData, which validates column integrity and format. Call buildExperiment on the resulting data frame, optionally specifying column mappings for compounds (features), samples (aliquots), primary assay (compound area), and secondary assay (internal standard area). Extract the 'ratio' assay from the returned SummarizedExperiment object. For cases where secondaryAssay is not provided, verify that the ratio assay equals the primary assay values element-wise (confirming an implicit divisor of 1). For cases where secondaryAssay is specified, verify that each ratio value equals the primary assay divided by the corresponding secondary assay value across all compound–sample pairs. Compare using exact equality or tolerance-based checks depending on numerical precision requirements.

## Related tools

- **mzQuality** (R package that constructs SummarizedExperiment objects and computes ratio assays from metabolomics data; provides buildExperiment and readData functions used to load and structure data) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor data structure class that stores assay matrices (including 'ratio'), row metadata (compound data), and column metadata (sample data); the core object format for mzQuality)
- **R** (Language in which mzQuality is implemented; used to execute readData, buildExperiment, and verification code)

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); combined <- readData(path); exp <- buildExperiment(combined); ratio_assay <- assay(exp, "ratio"); primary_assay <- assay(exp, "area"); all.equal(ratio_assay, primary_assay)
```

## Evaluation signals

- When secondaryAssay is not specified, verify that all ratio assay values match primary assay values element-wise (confirms divisor defaults to 1).
- When secondaryAssay is specified, verify that ratio[i,j] == primary[i,j] / secondary[i,j] for all compounds i and samples j (within numerical tolerance).
- Confirm that the SummarizedExperiment object contains a 'ratio' key in the assays() slot.
- Verify that rowData includes compound metadata and colData includes sample metadata with correct dimensions matching the ratio assay matrix.
- Check that no NA or infinite values appear in the ratio assay unless explicitly expected (e.g., division by zero in secondary assay).

## Limitations

- In the current version of mzQuality, only one sample type can be used for calculating concentrations, which may constrain multi-type studies.
- The ratio computation assumes the secondary assay (internal standard area) values are positive and non-zero; division by zero or missing values in secondary assay are not explicitly documented.
- Ratio verification depends on exact floating-point arithmetic; numerical precision differences between software or platforms may introduce small discrepancies requiring tolerance-based comparison rather than exact equality.

## Evidence

- [other] Task 005 finding on default secondary assay behavior: "When secondaryAssay is not provided to buildExperiment, its value defaults to 1, which negates the Internal Standard effect, making the ratio assay equal to the primary assay values."
- [other] Task 001 finding on ratio computation method: "The function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay (or"
- [other] Task 001 workflow on SummarizedExperiment construction: "Call buildExperiment on the resulting data frame, specifying column mappings for aliquots (samples), compounds (features), and assay values (area under the curve). Inspect the returned"
- [readme] README example of buildExperiment usage: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format. Finally, the function"
- [readme] README on doAnalysis workflow including ratio calculation: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards,"
