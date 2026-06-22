---
name: mass-spectrometry-file-standardization
description: Use when you have raw or semi-processed mass-spectrometry peak data from XCMS, MSnbase, or other peak-picking tools in non-standard formats (MetaboAnalyst-like, Metabolights, vendor-specific), and you need to load them into MetaboShiny for compound identification, normalization, and statistical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboShiny
  - R
  - XCMS
  - MSnbase
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
---

# mass-spectrometry-file-standardization

## Summary

Reconstruct and validate mass-spectrometry peak files (m/z peaklists in positive and negative ionization modes) and associated metadata into canonical formats accepted by MetaboShiny, ensuring structural consistency, numerical validity, and sample-to-metadata linkage before downstream analysis.

## When to use

You have raw or semi-processed mass-spectrometry peak data from XCMS, MSnbase, or other peak-picking tools in non-standard formats (MetaboAnalyst-like, Metabolights, vendor-specific), and you need to load them into MetaboShiny for compound identification, normalization, and statistical analysis. Use this skill when positive and negative mode peaklists exist as separate files and a sample metadata table (with batch, concentration, or experimental grouping information) must be reconciled with peak intensity matrices.

## When NOT to use

- Peak data are already in MetaboShiny native format or have been previously imported and saved in a MetaboShiny project (load the saved project instead via the Project tab in Settings).
- Raw mass-spectrometry spectrum files (mzML, mzXML, raw vendor formats) have not yet been processed through peak-picking; use XCMS or MSnbase first to generate m/z peaklists.
- Metadata identifiers do not match any sample names in the peaklist files and no regex transformation can reconcile them (manual rename or data curation required before this skill).

## Inputs

- Positive-mode m/z peak file (CSV with m/z, intensity, retention time columns)
- Negative-mode m/z peak file (CSV with m/z, intensity, retention time columns)
- Metadata file (CSV with 'sample', 'individual', and experimental group/phenotype columns)
- Example input templates (from MetaboShiny inst/examples folder)

## Outputs

- Validated positive-mode peaklist (R data frame or CSV)
- Validated negative-mode peaklist (R data frame or CSV)
- Validated metadata table (R data frame or CSV)
- Merged peak-metadata object (ready for MetaboShiny import)

## How to apply

Load positive and negative peaklist files (CSV or equivalent) from your peak-picking output or the MetaboShiny examples folder using R. Validate that each peaklist contains required columns: m/z values, peak intensities, and retention time (if applicable), and verify numerical ranges are physically plausible for your mass spectrometer (e.g., m/z > 0, intensity ≥ 0). In parallel, load the metadata file and confirm it has a 'sample' column with identifiers matching peaklist column names, an 'individual' column (for time-series or repeated-measure designs), and at least one experimental grouping or phenotype column. Transform both peaklists and metadata into R data frames or lists matching MetaboShiny's canonical structure (as shown in the examples folder). Output validated objects as CSV files or R serialized objects ready for MetaboShiny's file import dialog, where you will specify project name, mass spectrometer ppm tolerance, and a regex pattern (if needed) to align peaklist sample names to metadata sample identifiers.

## Related tools

- **MetaboShiny** (Target application for standardized input; provides file import dialog and canonical format specification via examples folder) — https://github.com/joannawolthuis/MetaboShiny
- **XCMS** (Upstream peak-picking tool that produces m/z peaklists compatible with MetaboShiny (with MetaboAnalyst export option))
- **MSnbase** (Alternative upstream peak-picking tool that produces m/z peaklists compatible with MetaboShiny)
- **R** (Environment for loading, validating, and transforming peaklist and metadata files into canonical format)

## Examples

```
library(MetaboShiny); pos_peaks <- read.csv('examples/positive_peaklist.csv'); neg_peaks <- read.csv('examples/negative_peaklist.csv'); metadata <- read.csv('examples/metadata.csv'); # Validate sample name match and load into MetaboShiny via browser UI with project name, ppm tolerance, and regex pattern as needed.
```

## Evaluation signals

- Each m/z value in positive and negative peaklists is numeric, > 0, and within expected instrument range (e.g., 50–1500 m/z for typical LC-MS).
- Peak intensities are numeric and ≥ 0; no negative or null values in required columns.
- All sample identifiers in peaklist column headers exactly match (after regex adjustment, if applied) identifiers in the metadata 'sample' column.
- Metadata contains no null values in 'sample', 'individual', or grouping columns; at least one experimental variable is present.
- Output files load without error into MetaboShiny's file import dialog (File Import panel, step 5: arrow merge button returns green tick mark).

## Limitations

- MetaboShiny does not accept raw peak data; upstream peak-picking (XCMS, MSnbase, or equivalent) is mandatory; this skill applies only to post-picking standardization.
- Metadata sample identifiers must be inferable from peaklist column names via exact match or regex substitution; completely non-aligned identifiers require manual curation outside this workflow.
- Three specific input formats are validated (MetaboAnalyst-like, MetaboShiny native, Metabolights); other custom formats may require additional custom parsing not covered in the examples.
- The skill addresses only structural validation and format alignment; it does not address batch effects, missing values, or distributional issues—those are handled downstream in the Data Normalization step.

## Evidence

- [readme] MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase.: "MetaboShiny does not accept raw peak data. We suggest using either XCMS (with the MetaboAnalyst export option) or another method of choice such as MSnbase."
- [other] MetaboShiny requires input data preparation in two forms: m/z peak files (positive and negative peaklists) and a metadata file, with example input files available in the examples folder.: "For example input files (positive and negative peaklists + metadata) please see the `examples` folder."
- [readme] Metadata must include sample identifiers, individual column, and experimental grouping.: "MetaboShiny, unless using the MetaboAnalyst format, requires an additional metadata table. This should minimally have a 'sample' column that contains the same sample identifiers used in the peak"
- [readme] File import step includes regex adjustment and data merging.: "4a. (optional) Input a regex string to to adjust peaklist names to metadata sample names - the match is removed from each name. 4b. Upload your metadata and positive and negative mode m/z peak files."
- [readme] Validation via file import completion.: "Once step 5 is completed (green tick mark), continue to the [Data normalization](#data-normalization) step."
