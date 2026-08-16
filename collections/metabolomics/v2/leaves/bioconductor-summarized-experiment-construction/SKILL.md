---
name: bioconductor-summarized-experiment-construction
description: 'Use when after successfully reading and validating a tab-delimited metabolomics
  file (containing mandatory columns: aliquot, compound, area, type, injection_time,
  batch) using readData, and before applying batch correction, outlier detection,
  or other QC filters.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - readData
  - mzQualityDashboard
  - mzrtsim
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
- doi: 10.1021/acs.analchem.5c01213
  title: ''
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bioconductor-summarized-experiment-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert a validated tab-delimited metabolomics data frame into a Bioconductor SummarizedExperiment object with automatically computed assays (primary compound areas, internal standard areas, and compound/IS ratios) and structured metadata. This skill bridges raw data import and downstream quality control analysis in mzQuality workflows.

## When to use

After successfully reading and validating a tab-delimited metabolomics file (containing mandatory columns: aliquot, compound, area, type, injection_time, batch) using readData, and before applying batch correction, outlier detection, or other QC filters. Use this skill when you have a data frame with metabolite measurements indexed by sample and compound identifiers, and need to construct a structured object that preserves both assay data and sample/feature metadata.

## When NOT to use

- Data is already in SummarizedExperiment format (use directly or convert via coercion instead)
- Input file has missing or incorrectly formatted mandatory columns—run readData validation first and correct before calling buildExperiment
- No internal standard (secondary assay) is defined or available; ratio assay computation will fail silently or produce NA values

## Inputs

- data frame from readData() with validated columns: aliquot, compound, area, type, injection_time, batch
- column name specifying compound/feature identifier (string)
- column name specifying aliquot/sample identifier (string)
- column name for primary assay values, typically peak area (string)
- column name for secondary assay values, typically internal standard area (string)

## Outputs

- SummarizedExperiment object with three assays: primary compound areas, internal standard areas, and computed compound/IS ratios
- rowData slot containing compound metadata (indexed by feature name)
- colData slot containing sample metadata including batch, injection_time, and sample type
- assay slot with three named matrices: primaryAssay, secondaryAssay, and ratio

## How to apply

Call buildExperiment() on the validated data frame returned by readData(), specifying the compoundColumn (feature identifier, e.g., 'compound'), aliquotColumn (sample identifier, e.g., 'aliquot'), primaryAssay (e.g., 'area' for compound peak area), and secondaryAssay (e.g., 'area' for internal standard peak area when type='IS'). The function automatically deduces rowData from unique compounds and colData from unique samples, infers batch and injection_time metadata, and computes the compound/internal standard ratio assay by dividing primary by secondary assay values for each sample. Verify the resulting SummarizedExperiment contains three assays (primaryAssay, secondaryAssay, ratio), rowData indexed by compound with metadata columns, and colData indexed by aliquot with sample type, batch, and injection metadata.

## Related tools

- **mzQuality** (R package providing buildExperiment() function to construct SummarizedExperiment from validated metabolomics data frames) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor S4 class used internally by mzQuality to store assay data and associated metadata in structured rowData and colData slots) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **readData** (mzQuality function that reads tab-delimited files and validates mandatory columns before passing to buildExperiment) — https://github.com/hankemeierlab/mzQuality
- **mzQualityDashboard** (Interactive Shiny application wrapping mzQuality's buildExperiment for users without R programming experience) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path))
```

## Evaluation signals

- Resulting object is a valid SummarizedExperiment with class 'SummarizedExperiment' (check via class() in R)
- Three named assays are present: verify via names(assays(exp)) returns at least [primaryAssay, secondaryAssay, ratio]
- Ratio assay values are correctly computed as primary/secondary for each sample; spot-check a few cells: assays(exp)$ratio[i,j] ≈ assays(exp)$primaryAssay[i,j] / assays(exp)$secondaryAssay[i,j]
- rowData contains one row per unique compound with no duplicate feature names; nrow(rowData(exp)) equals number of unique compounds in input
- colData contains one row per unique sample with batch and injection_time metadata; nrow(colData(exp)) equals number of unique aliquots in input
- No NA values appear in ratio assay where both primary and secondary assay values are non-zero and non-missing

## Limitations

- buildExperiment requires all mandatory columns (aliquot, compound, area, type, injection_time, batch) to be present and correctly formatted; missing or misspelled columns will cause function failure—use readData() for validation first
- Ratio assay computation assumes secondary assay (internal standard) is always present for every sample; samples missing internal standard measurements will produce NA in ratio assay
- Function does not perform batch correction or outlier detection; these are separate downstream steps (doAnalysis) applied after object construction
- Large datasets (105+ compounds × 500+ samples) may consume significant memory as assays are stored as dense matrices; sparse matrix support is not documented

## Evidence

- [other] buildExperiment deduces rowData and colData slots from compoundColumn and aliquotColumn, uses primaryAssay and secondaryAssay as compound and Internal Standard areas respectively, and automatically calculates the compound/Internal Standard ratio for each sample, storing it in the ratio assay.: "buildExperiment deduces rowData and colData slots from compoundColumn and aliquotColumn, uses primaryAssay and secondaryAssay as compound and Internal Standard areas respectively, and automatically"
- [intro] The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [other] To read your data, you can use the `readData` function. This function will read in your data and check for any missing or incorrect columns.: "To read your data, you can use the `readData` function. This function will read in your data and check for any missing or incorrect columns."
- [readme] Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format. Finally, the function `buildExperiment` will convert the data into a SummarizedExperiment object.: "Finally, the function `buildExperiment` will convert the data into a SummarizedExperiment object. This is the object that mzQuality uses to perform all calculations and analyses"
- [readme] path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path)): "exp <- buildExperiment(readData(path))"
