---
name: numerical-equivalence-testing
description: Use when you need to confirm that omitting an optional input parameter (such as secondaryAssay in buildExperiment) produces the expected mathematical result—specifically, when a default value should neutralize a transformation (e.
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

# numerical-equivalence-testing

## Summary

Verify that two numerical assays or derived quantities are element-wise identical or functionally equivalent by comparing their values across all observations. This skill is essential when testing default parameter behaviors or validating that mathematical transformations (e.g., division by 1) leave data unchanged.

## When to use

Apply this skill when you need to confirm that omitting an optional input parameter (such as secondaryAssay in buildExperiment) produces the expected mathematical result—specifically, when a default value should neutralize a transformation (e.g., an internal standard divisor of 1 making the ratio assay equal to the primary assay). Use it to validate assumptions about default behavior before proceeding with downstream analyses that depend on those defaults.

## When NOT to use

- Input data already has a secondary assay explicitly specified; equivalence testing is not meaningful when both numerator and denominator are intentionally distinct.
- The expected behavior is that ratio assay should differ from primary assay (e.g., when internal standard normalization is the intended operation).
- Assays contain missing or NaN values that would invalidate direct element-wise comparison without imputation or masking logic.

## Inputs

- tab-delimited metabolomics data file (e.g., example.tsv from mzQuality package)
- SummarizedExperiment object with primary assay and optional secondary assay slots

## Outputs

- validation report confirming element-wise equality across compound–sample pairs
- boolean matrix or logical summary indicating which assay pairs pass equivalence test

## How to apply

Load the input data using readData (which performs basic integrity checks on column structure), then call buildExperiment without the optional secondary assay parameter to generate a SummarizedExperiment object. Extract the 'ratio' assay from the resulting experiment object and the primary assay values separately. Perform element-wise comparison across all compound–sample pairs to verify that ratio values equal primary assay values, confirming that the default internal standard divisor of 1 has negated the normalization effect. Generate a validation report documenting the equality check outcome for all observations.

## Related tools

- **mzQuality** (Provides buildExperiment function to construct SummarizedExperiment objects and readData for input validation; hosts example.tsv test dataset used to validate ratio assay default behavior.) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container object that stores compound (rowData) and sample (colData) metadata alongside multiple assays (ratio, primary, ratio_corrected) enabling slot-based extraction and comparison.) — https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html
- **R** (Programming environment in which readData, buildExperiment, and element-wise assay extraction and comparison operations are executed.)

## Examples

```
path <- system.file('extdata', 'example.tsv', package = 'mzQuality'); exp <- buildExperiment(readData(path)); all.equal(assay(exp, 'ratio'), assay(exp, 'primary'))
```

## Evaluation signals

- All ratio assay values are numerically identical (or differ only by floating-point rounding error ≤ machine epsilon) to primary assay values across all compound–sample pairs.
- Validation report documents the count and percentage of observations passing equivalence test, with 100% pass rate indicating correct default behavior.
- No NaN, Inf, or missing values appear in the comparison result when input data is complete; presence of such values flags data quality issues.
- Repeating the test with an explicitly specified secondaryAssay parameter = 1 produces identical outcome, confirming equivalence of default and explicit divisor.
- Element-wise difference matrix (ratio - primary) contains only zeros or values within machine epsilon tolerance (e.g., < 1e-15 for double precision).

## Limitations

- Floating-point arithmetic may introduce rounding errors; exact equality testing must account for machine epsilon tolerance rather than strict zero difference.
- This validation assumes the primary assay contains no missing or NaN values; presence of such values will cause element-wise comparison to produce NA or FALSE results that mask the true default behavior.
- The secondaryAssay default value of 1 is specific to mzQuality's buildExperiment function; other tools or functions may have different or no defaults, making the equivalence test inapplicable.
- Test is limited to the specific case where secondaryAssay is omitted entirely; partial or conditional specification of secondary assay parameters may not follow the documented default.

## Evidence

- [other] Default internal standard divisor behavior: "When secondaryAssay is not provided to buildExperiment, its value defaults to 1, which negates the Internal Standard effect, making the ratio assay equal to the primary assay values."
- [other] Workflow for validation testing: "Load the example.tsv file from the mzQuality package using readData function, which performs basic checks on column integrity. Call buildExperiment on the resulting data frame without specifying a"
- [other] Validation report generation: "Generate a validation report confirming equality across all compound–sample pairs."
- [readme] buildExperiment function and SummarizedExperiment usage: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [readme] Data import and integrity checking: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format."
