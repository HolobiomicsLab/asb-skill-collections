---
name: metabolomics-data-validation
description: Use when you have raw or semi-processed m/z peak lists (positive and
  negative ion mode) and a sample metadata table, and you need to confirm they meet
  MetaboShiny's structural and semantic requirements before loading them into the
  normalization pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0091
  tools:
  - MetaboShiny
  - R
  - XCMS
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

# metabolomics-data-validation

## Summary

Validate and standardize m/z peak files and metadata tables to conform to MetaboShiny's input specification before downstream analysis. This skill ensures data integrity and prevents processing failures by verifying file formats, required columns, numerical ranges, and sample identifier consistency.

## When to use

Apply this skill when you have raw or semi-processed m/z peak lists (positive and negative ion mode) and a sample metadata table, and you need to confirm they meet MetaboShiny's structural and semantic requirements before loading them into the normalization pipeline. Use it as the first step after peak detection and before any batch correction or feature filtering.

## When NOT to use

- Input data has already been loaded and validated by MetaboShiny's file import dialog (skip to normalization step).
- Raw instrument output files (mzML, mzXML, NetCDF) — use XCMS or MSnbase for peak detection first.
- Data is already in a committed MetaboShiny project save state — load existing dataset instead.

## Inputs

- positive mode m/z peaklist file (CSV/TSV with m/z, intensity, retention time columns)
- negative mode m/z peaklist file (CSV/TSV with m/z, intensity, retention time columns)
- sample metadata table (CSV/TSV with sample, individual, batch, group, concentration columns)
- example reference files from MetaboShiny repository inst/examples folder

## Outputs

- validated positive peaklist data frame (R object or CSV)
- validated negative peaklist data frame (R object or CSV)
- validated metadata data frame (R object or CSV)
- validation report (list of passed/failed checks, sample ID mappings)

## How to apply

Load positive and negative peaklist files and the metadata file into R. Validate peaklist structure by confirming each file contains required columns (m/z values, peak intensities, retention time where applicable) and checking that numerical values fall within expected mass spectrometry ranges. Validate metadata structure by confirming presence of a 'sample' column with identifiers matching peaklist sample names, an 'individual' column (for time-series or multi-sample designs), and at least one experimental group or batch column. Cross-check that all sample identifiers in peaklists appear in metadata (and vice versa, or document exclusions). Transform peaklists and metadata into R data frames matching MetaboShiny's canonical format. Output the validated objects as CSV files or R RDS objects ready for the data normalization step.

## Related tools

- **MetaboShiny** (Shiny web application that ingests and processes validated peaklists and metadata; defines input format specification) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Programming environment for loading, parsing, validating, and transforming peaklist and metadata files into canonical R data structures)
- **XCMS** (Recommended upstream tool for peak detection and export to MetaboAnalyst-compatible or MetaboShiny-native peaklist format)

## Evaluation signals

- All peaklist files contain m/z, intensity, and retention time columns with numeric, non-missing values in expected ranges (e.g., m/z > 0, intensity ≥ 0).
- Metadata table contains 'sample', 'individual', and at least one experimental group/batch column; all sample identifiers are unique and match across peaklist and metadata files (after regex adjustment if applied).
- No samples are present in peaklists but missing from metadata (or exclusions are documented); conversely, no samples in metadata lack corresponding peaklist data.
- Data frames are successfully loaded into R without type coercion warnings or missing value errors; can be written to CSV without loss of structure.
- Validated outputs conform to example formats from inst/examples folder (MetaboAnalyst-like, MetaboShiny native, or Metabolights format as appropriate).

## Limitations

- Validation does not detect biological implausibility (e.g., unrealistic m/z ranges for small molecules) — requires domain knowledge to interpret.
- Metadata validation assumes 'sample', 'individual', and group columns exist; custom metadata schemas may require manual adjustment or documentation.
- If peaklist names do not match metadata sample identifiers exactly, a regex pattern must be provided to reconcile them; incorrect regex will cause validation to fail silently.
- Validation assumes positive and negative mode files are provided separately; merged or multi-mode files may require preprocessing before validation.
- The skill does not impute missing metadata fields; sparse or incomplete metadata will be reported but not auto-corrected.

## Evidence

- [other] MetaboShiny requires input data preparation in two forms: m/z peak files (positive and negative peaklists) and a metadata file, with example input files available in the examples folder of the repository.: "MetaboShiny requires input data preparation in two forms: m/z peak files (positive and negative peaklists) and a metadata file, with example input files available in the examples folder"
- [other] Validate peaklist format: check that each file contains required columns (m/z values, peak intensities, and retention time where applicable) and that numerical values are within expected ranges.: "check that each file contains required columns (m/z values, peak intensities, and retention time where applicable) and that numerical values are within expected ranges"
- [readme] MetaboShiny, unless using the MetaboAnalyst format, requires an additional metadata table. This should minimally have a 'sample' column that contains the same sample identifiers used in the peak table files, an 'individual' column (since multiple samples can come from one individual in time series data) and at least one column on experimental group or something alike.: "This should minimally have a 'sample' column that contains the same sample identifiers used in the peak table files, an 'individual' column, and at least one column on experimental group"
- [readme] MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase.: "MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method"
- [other] Transform peaklists and metadata into the canonical format ingested by MetaboShiny using R data structures (data frames or lists).: "Transform peaklists and metadata into the canonical format ingested by MetaboShiny using R data structures (data frames or lists)"
