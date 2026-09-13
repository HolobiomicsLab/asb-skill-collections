---
name: metadata-structure-checking
description: Use when after loading a metadata file but before merging it with positive
  and negative mode m/z peaklists. Apply this skill when you have a candidate metadata
  table (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboShiny
  - R
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-structure-checking

## Summary

Validate that a metadata file conforms to MetaboShiny's required structure and column schema before integration with m/z peak data. This upstream quality check ensures sample identifiers, batch information, and experimental metadata are present and correctly formatted to prevent downstream integration failures.

## When to use

After loading a metadata file but before merging it with positive and negative mode m/z peaklists. Apply this skill when you have a candidate metadata table (e.g., CSV, TSV) and need to confirm it matches MetaboShiny's input specification—specifically, the presence of 'sample', 'individual', and experimental group columns—to proceed with the file import step.

## When NOT to use

- The metadata file already has been validated and integrated into a MetaboShiny project; re-checking is redundant.
- You are working with MetaboAnalyst export format, which embeds metadata and peak data together—use the unified file import path instead.
- Sample identifiers in your metadata do not correspond to any peaklist file names; resolve naming conflicts first before structure checking.

## Inputs

- Raw metadata file (CSV, TSV, or R data.frame)
- Example metadata files from MetaboShiny examples folder (for reference schema)

## Outputs

- Validated metadata R data.frame
- Validated metadata CSV file (canonical format for MetaboShiny)
- Validation report (presence/absence of required columns, null counts, sample identifier match status)

## How to apply

Load the metadata file into R as a data frame and inspect its structure. Verify the presence of three mandatory columns: (1) 'sample' containing identifiers that match peaklist sample names, (2) 'individual' to track repeated measures or time series, and (3) at least one column representing experimental group or treatment. Check that all entries are non-null and that sample identifiers are unique or appropriately duplicated (if multiple samples per individual are expected). If batch information or concentration data are relevant to your study design, confirm those columns exist with valid values. Transform the metadata into a data frame or list structure conformable to MetaboShiny's ingestion format, then output it as CSV or an R object for the subsequent merge step. Use the example metadata files in the repository's examples folder as reference for acceptable structure and column naming.

## Related tools

- **MetaboShiny** (Target application that ingests validated metadata; defines schema requirements and merge logic) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Scripting environment for loading, inspecting, and transforming metadata data.frames)

## Examples

```
# In R: load and validate metadata
metadata <- read.csv('metadata.csv', row.names=1)
all(c('sample', 'individual', 'group') %in% colnames(metadata))
all(!is.na(metadata$sample)) && length(unique(metadata$sample)) == nrow(metadata)
```

## Evaluation signals

- All three mandatory columns ('sample', 'individual', experimental group) are present with no null values.
- Sample identifiers in the metadata column exactly match (or can be reconciled with) sample names in the m/z peaklist files after optional regex adjustment.
- Data types are correct: sample and individual identifiers are character/string; numerical fields (concentration, batch IDs) are numeric or integer.
- The validated metadata can be successfully merged with positive and negative peaklist data without errors during the file import step in MetaboShiny.
- Example metadata files from the repository can be loaded and validated using the same workflow without raising schema errors.

## Limitations

- MetaboShiny requires 'individual' column even for cross-sectional (non-repeated-measures) studies; if not present, it must be constructed (e.g., one individual per sample).
- The metadata file must be tab- or comma-delimited; format errors (e.g., embedded newlines, inconsistent delimiters) will cause parsing failures and are not automatically detected by schema checks alone.
- Sample name reconciliation relies on exact string matching or user-provided regex rules; partial mismatches between metadata sample IDs and peaklist file names will result in orphaned samples or m/z values.
- Metadata column names are case-sensitive; variations like 'Sample' vs 'sample' will not be recognized as the required 'sample' column.

## Evidence

- [readme] Required columns specification: "MetaboShiny, unless using the MetaboAnalyst format, requires an additional metadata table. This should minimally have a 'sample' column that contains the same sample identifiers used in the peak"
- [readme] Examples and reference location: "Examples of metadata formats are also present in the [inst/examples](./inst/examples) folder."
- [readme] Integration step and validation trigger: "5. Click on the arrow to merge peak data and metadata and convert them to a format that will serve as the input for the analyses."
- [readme] Optional regex reconciliation for sample naming: "4a. (optional) Input a regex string to to adjust peaklist names to metadata sample names - the match is removed from each name."
- [other] Source task finding on metadata validation: "Load the metadata file from the examples folder and validate its structure: confirm presence of required sample identifiers, batch information, and other metadata fields expected by MetaboShiny."
