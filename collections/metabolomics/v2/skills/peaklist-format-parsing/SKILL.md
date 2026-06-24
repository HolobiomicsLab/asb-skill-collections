---
name: peaklist-format-parsing
description: Use when you have raw or semi-processed m/z peak detection output from
  LC-MS/MS instruments (typically from XCMS, MSnbase, or other peak-picking tools)
  in one of several known formats (MetaboAnalyst-like, MetaboShiny native, or Metabolights)
  and need to ingest them into MetaboShiny for compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboShiny
  - R
  - XCMS
  techniques:
  - LC-MS
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

# peaklist-format-parsing

## Summary

Parse and validate mass spectrometry peaklist files (positive and negative mode m/z peak files) and associated metadata into canonical formats accepted by MetaboShiny. This skill bridges raw peak detection output into a standardized tabular structure required for downstream metabolomics analysis.

## When to use

You have raw or semi-processed m/z peak detection output from LC-MS/MS instruments (typically from XCMS, MSnbase, or other peak-picking tools) in one of several known formats (MetaboAnalyst-like, MetaboShiny native, or Metabolights) and need to ingest them into MetaboShiny for compound identification and statistical analysis. The trigger is the presence of separate positive and negative polarity peaklist files plus a sample metadata table that must be merged and validated before normalization.

## When NOT to use

- Peaklist input is already in MetaboShiny's native format and has been previously loaded and saved by MetaboShiny itself — proceed directly to loading the saved project.
- You have only raw mzML or netCDF instrument files without peak detection applied — first run XCMS or MSnbase peak picking before attempting peaklist parsing.
- Metadata table lacks required 'sample' and 'individual' columns or does not have at least one experimental group column — metadata must be reconstructed before parsing.

## Inputs

- Positive mode m/z peaklist file (CSV, TSV, or tabular format with m/z, intensity, and retention time columns)
- Negative mode m/z peaklist file (same format as positive mode)
- Metadata table (CSV or TSV with 'sample', 'individual', and experimental grouping columns)

## Outputs

- Validated positive peaklist (data frame or CSV with standardized column structure)
- Validated negative peaklist (data frame or CSV with standardized column structure)
- Validated metadata table (data frame or CSV with required columns aligned to peaklist sample names)

## How to apply

Load the positive and negative peaklist files and metadata file from your input directory (MetaboShiny provides examples in its `inst/examples` folder). Validate that each peaklist contains required columns: m/z values, peak intensities, and retention time where applicable, with numerical values within expected ranges for your instrument (e.g., m/z typically 50–2000 Da for metabolomics). Validate the metadata file structure: confirm presence of a 'sample' column matching peaklist sample identifiers, an 'individual' column (for time-series or repeated-measures designs), and at least one experimental group or condition column. Transform both peaklists and metadata into R data frames or CSV files matching MetaboShiny's input specification. If sample names in peaklists differ from metadata, use a regex string (provided during file import in MetaboShiny) to adjust peaklist names before merging. Output the validated and parsed peaklists (separate positive and negative CSV/data frame pairs) and metadata table ready for the file import step.

## Related tools

- **MetaboShiny** (Target application that ingests and processes the parsed peaklists and metadata for compound identification, normalization, and statistical analysis) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Programming environment for loading, validating, and transforming peaklist and metadata files into canonical tabular formats)
- **XCMS** (Upstream peak detection tool that generates m/z peaklists in MetaboAnalyst-compatible format suitable for parsing by this skill)

## Evaluation signals

- Peaklist data frames contain exactly the required columns (m/z, intensity, retention time) with no missing values in critical fields; all numerical values fall within expected instrument ranges (e.g., m/z > 0, intensity > 0).
- Metadata table contains 'sample', 'individual', and at least one experimental group column; all entries in the 'sample' column are unique and match peaklist sample identifiers exactly after regex adjustment.
- After merging peaklist and metadata, the number of samples in the merged object equals the number of rows in the metadata file and the union of positive + negative peaklist samples.
- MetaboShiny file import step (step 5 in Load data files) completes successfully with a green checkmark, indicating the merged format is accepted.
- Pre- and post-normalization peak value distributions can be plotted for randomly selected m/z values and samples, confirming data structure integrity.

## Limitations

- MetaboShiny does not accept raw peak data directly; preprocessing with XCMS, MSnbase, or equivalent is mandatory before parsing.
- Sample identifiers in peaklists and metadata must be reconcilable via exact match or regex substitution; arbitrary or undocumented naming conventions in peaklists may cause merge failure.
- The skill assumes peaklists and metadata are complete and internally consistent; rows with missing sample identifiers or duplicate identifiers in either file will cause validation or merge errors.
- Retention time columns are optional but recommended; their absence may affect downstream compound matching accuracy in MetaboShiny if the database search relies on RT information.

## Evidence

- [other] MetaboShiny requires input data preparation in two forms: m/z peak files (positive and negative peaklists) and a metadata file: "MetaboShiny requires input data preparation in two forms: m/z peak files (positive and negative peaklists) and a metadata file"
- [readme] MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase.: "MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase."
- [readme] MetaboShiny, unless using the MetaboAnalyst format, requires an additional metadata table. This should minimally have a 'sample' column that contains the same sample identifiers used in the peak table files, an 'individual' column (since multiple samples can come from one individual in time series data) and at least one column on experimental group or something alike.: "This should minimally have a 'sample' column that contains the same sample identifiers used in the peak table files, an 'individual' column (since multiple samples can come from one individual in"
- [readme] For example input files (positive and negative peaklists + metadata) please see the examples folder.: "For example input files (positive and negative peaklists + metadata) please see the examples folder."
- [readme] 4a. (optional) Input a regex string to to adjust peaklist names to metadata sample names - the match is removed from each name.: "Input a regex string to to adjust peaklist names to metadata sample names - the match is removed from each name."
- [readme] After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples: "After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples"
