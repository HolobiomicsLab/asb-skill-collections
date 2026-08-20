---
name: data-format-conversion-to-application-schema
description: Use when you have m/z peak lists (positive and negative mode) and sample
  metadata from peak-picking software (e.g., XCMS with MetaboAnalyst export, MSnbase,
  or MetaboLights format) and need to load them into MetaboShiny for compound identification,
  statistical analysis, or machine learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3370
  tools:
  - MetaboShiny
  - R
  - XCMS
  - MSnbase
  techniques:
  - mass-spectrometry
  license_tier: open
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

# data-format-conversion-to-application-schema

## Summary

Convert raw or intermediate mass spectrometry peak data and sample metadata into the canonical input schema required by MetaboShiny for downstream metabolomics analysis. This skill bridges diverse upstream peak-picking formats (XCMS, MSnbase, MetaboLights) into a unified, validated structure.

## When to use

You have m/z peak lists (positive and negative mode) and sample metadata from peak-picking software (e.g., XCMS with MetaboAnalyst export, MSnbase, or MetaboLights format) and need to load them into MetaboShiny for compound identification, statistical analysis, or machine learning. The trigger is the availability of three separate files: positive peaklist, negative peaklist, and metadata table with sample identifiers and experimental covariates.

## When NOT to use

- Raw instrumental data files (mzML, netCDF, .raw) are available—use XCMS or MSnbase first to extract peak lists before this skill.
- Peak data is already in MetaboAnalyst export format with embedded metadata—MetaboShiny accepts this directly without conversion.
- Sample identifiers in peaklist column headers exactly match metadata 'sample' column without any prefix or suffix—no regex adjustment is needed.

## Inputs

- Positive m/z peaklist file (CSV/TSV with m/z, intensity, and optional retention time columns)
- Negative m/z peaklist file (CSV/TSV with m/z, intensity, and optional retention time columns)
- Metadata table (CSV/TSV with 'sample', 'individual', and at least one experimental group column)
- Optional regex string to adjust peaklist column names to metadata sample identifiers

## Outputs

- Merged peak data and metadata in MetaboShiny canonical format
- Validated R data structure (or intermediate serialized form) ready for data normalization
- Confirmation of successful conversion (green tick mark in UI or validation log)

## How to apply

Load the positive and negative peaklist CSV/TSV files and the metadata table into R as data frames. Validate that peaklists contain required columns (m/z values, peak intensities, retention time where applicable) with numerical values within expected mass range (typically 50–2000 m/z) and intensities as positive numbers. Validate that the metadata table contains a 'sample' column with identifiers matching peaklist column names (after optional regex adjustment), an 'individual' column (to distinguish repeat samples from the same subject), and at least one experimental group or condition column. Transform the peaklists and metadata into the canonical format by ensuring consistent sample name mapping, column naming (e.g., 'm/z', 'intensity', 'retention_time' in peaklists), and structure expected by MetaboShiny's data loader. Use the optional regex field in MetaboShiny's file import step to strip filename prefixes from peaklist column headers if they do not exactly match metadata sample identifiers. Output the merged and validated data structure, confirmed by a green tick mark in the file import panel, which signals successful format conversion and readiness for the normalization step.

## Related tools

- **MetaboShiny** (Target application that ingests the converted peak and metadata format; provides file import UI with validation and regex adjustment for sample name harmonization) — https://github.com/joannawolthuis/MetaboShiny
- **XCMS** (Upstream peak-picking tool that can export data in MetaboAnalyst-like format, which can be converted to MetaboShiny canonical format)
- **MSnbase** (Alternative upstream peak-picking tool whose output can be converted to MetaboShiny input format)
- **R** (Programming language used to load, validate, and transform peaklist and metadata data frames into canonical format)

## Examples

```
library(MetaboShiny); start_metshi(inBrowser=T); # Then: 1. Enter project name. 2. Set ppm tolerance (e.g., 5 ppm). 3. Upload positive peaklist CSV, negative peaklist CSV, and metadata CSV. 4. (optional) Enter regex to strip prefixes from peaklist column names. 5. Click merge arrow to convert and validate format.
```

## Evaluation signals

- All sample identifiers in peaklist column headers match entries in metadata 'sample' column after optional regex transformation (no unmatched samples).
- All peaklist files contain required columns with numerical data types and values within expected ranges (m/z: 50–2000, intensities: positive numbers).
- Metadata table contains non-null 'sample', 'individual', and at least one experimental group/condition column with no missing critical identifiers.
- File import UI displays a green tick mark after clicking the merge arrow, indicating successful format conversion and readiness for normalization.
- Row and column counts in merged output match the union of samples and m/z features from input peaklists, with no data loss or duplication.

## Limitations

- MetaboShiny does not accept raw instrumental data; peak lists must be pre-extracted using XCMS, MSnbase, or equivalent peak-picking software.
- Sample identifier matching is case-sensitive and requires exact string alignment after regex transformation; inconsistent naming conventions will cause sample loss.
- Missing values handling is deferred to the data normalization step; conversion only validates presence of required columns, not imputation.
- The skill assumes positive and negative peaklists are separate files; merged polarity data in a single file may require pre-splitting.
- Retention time is optional but recommended; analyses may have reduced specificity without it, particularly for isotope pattern matching and adduct annotation.

## Evidence

- [readme] MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase.: "MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase."
- [readme] For example input files (positive and negative peaklists + metadata) please see the examples folder.: "For example input files (positive and negative peaklists + metadata) please see the `examples` folder."
- [readme] MetaboShiny, unless using the MetaboAnalyst format, requires an additional metadata table. This should minimally have a 'sample' column that contains the same sample identifiers used in the peak table files, an 'individual' column (since multiple samples can come from one individual in time series data) and at least one column on experimental group or something alike.: "MetaboShiny, unless using the MetaboAnalyst format, requires an additional metadata table. This should minimally have a 'sample' column that contains the same sample identifiers used in the peak"
- [readme] (optional) Input a regex string to to adjust peaklist names to metadata sample names - the match is removed from each name.: "(optional) Input a regex string to to adjust peaklist names to metadata sample names - the match is removed from each name."
- [readme] Once step 5 is completed (green tick mark), continue to the Data normalization step.: "Once step 5 is completed (green tick mark), continue to the Data normalization step."
- [readme] You can find examples of three different accepted data formats (MetaboAnalyst-like, MetaboShiny native and Metabolights) in the inst/examples folder.: "You can find examples of three different accepted data formats (MetaboAnalyst-like, MetaboShiny native and Metabolights) in the inst/examples folder."
