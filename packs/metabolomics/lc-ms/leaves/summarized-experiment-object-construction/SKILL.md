---
name: summarized-experiment-object-construction
description: Use when when you have imported a tab-delimited metabolomics file (via readData or similar) containing columns for compound identifiers, sample/aliquot names, peak areas (primary assay), internal standard areas (secondary assay), and sample type classifications, and you need to organize these into.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - readData
  techniques:
  - LC-MS
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

# SummarizedExperiment Object Construction

## Summary

Convert a tab-delimited metabolomics data frame into a SummarizedExperiment object by mapping user-specified columns to compound names, sample identifiers, and assay values (primary and secondary). The function automatically computes a compound/internal standard ratio assay, storing all data in a structured Bioconductor container suitable for downstream quality control analyses.

## When to use

When you have imported a tab-delimited metabolomics file (via readData or similar) containing columns for compound identifiers, sample/aliquot names, peak areas (primary assay), internal standard areas (secondary assay), and sample type classifications, and you need to organize these into a single analytical object before performing batch correction, outlier detection, or concentration calculations.

## When NOT to use

- Input is already a SummarizedExperiment object — proceed directly to doAnalysis or filtering steps.
- Input data lacks mandatory columns for compound identifiers or sample names — first validate and preprocess using readData to ensure column integrity.
- Column mappings are ambiguous or unmapped — buildExperiment requires explicit specification of column roles; resolve ambiguities before invocation.

## Inputs

- data frame with validated columns (from readData output)
- column name mappings for aliquots, compounds, primary assay values, and optional secondary assay values

## Outputs

- SummarizedExperiment object with rowData (compound metadata), colData (sample metadata), and assays (primary assay, secondary assay, and computed ratio assay)

## How to apply

Call buildExperiment on the data frame returned by readData, specifying column mappings for aliquots (sample names), features or compounds (compound identifiers), and assay values (area under the curve or peak intensity). The function validates column integrity, maps the primary assay (e.g., compound area) and optionally a secondary assay (e.g., internal standard area), then automatically computes a 'ratio' assay by dividing the primary by secondary values (or defaults the secondary assay to 1 if not provided, making the ratio equal to the primary assay). The resulting SummarizedExperiment object stores compound metadata in rowData, sample metadata in colData, and both the original and derived assays in the assays slot, enabling immediate downstream filtering and analysis via doAnalysis.

## Related tools

- **mzQuality** (Package providing buildExperiment function and downstream quality control workflows) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor S4 container class for storing assay data, row metadata (features), and column metadata (samples))
- **readData** (Upstream function that reads tab-delimited or Sciex OS text files and performs basic column validation and data integrity checks before handoff to buildExperiment) — https://github.com/hankemeierlab/mzQuality

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path))
```

## Evaluation signals

- Presence and correct structure of rowData slot: confirm compound identifiers and metadata are indexed by row.
- Presence and correct structure of colData slot: confirm sample/aliquot identifiers and sample types are indexed by column.
- Presence of at least three assays: primary assay, secondary assay (or vector of 1s if not provided), and 'ratio' assay with values equal to primary ÷ secondary (element-wise).
- Ratio assay identity check: when secondaryAssay is not provided, verify that ratio assay values are identical to primary assay values (element-wise comparison across all compound–sample pairs).
- Dimensions consistency: verify that nrow(SummarizedExperiment) equals number of unique compounds and ncol(SummarizedExperiment) equals number of unique samples.

## Limitations

- In the current version of mzQuality, only one sample type can be used for calculating concentrations, a limitation that will be addressed in a future version.
- buildExperiment requires explicit column mappings; missing or incorrectly named columns will cause the function to fail — validation should be performed by readData before invocation.
- If secondaryAssay column is not provided, the internal standard effect is negated by defaulting to 1, which may not be appropriate for all experimental designs.

## Evidence

- [intro] buildExperiment function with column mappings: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [other] Automatic ratio computation from primary and secondary assays: "the function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay"
- [other] Secondary assay defaults to 1 when not provided: "When secondaryAssay is not provided to buildExperiment, its value defaults to 1, which negates the Internal Standard effect, making the ratio assay equal to the primary assay values"
- [readme] SummarizedExperiment as core analytical object: "Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data."
- [readme] readData performs upstream validation: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format."
- [readme] buildExperiment converts validated data to SummarizedExperiment: "Finally, the function `buildExperiment` will convert the data into a SummarizedExperiment object. This is the object that mzQuality uses to perform all calculations and analyses and is used"
