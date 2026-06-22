---
name: batch-spectral-record-processing
description: Use when you have acquired MS/MS spectra in .msp format (e.g., from MassBank or experimental acquisition) and need to transform them into a structured library format compatible with automated annotation tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MetaboAnnotatoR
  - R
  - MassBank
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Batch spectral record processing

## Summary

Convert MS/MS spectra from library files (e.g., .msp format) into metabolite annotation database entries by applying peak-picking, occurrence scoring, and ionization-mode classification. This skill enables high-throughput transformation of raw spectral data into structured, reusable fragment libraries for metabolite identification.

## When to use

You have acquired MS/MS spectra in .msp format (e.g., from MassBank or experimental acquisition) and need to transform them into a structured library format compatible with automated annotation tools. This is the entry point when building or updating fragment databases for untargeted LC-MS metabolomics, particularly when working with All-ion fragmentation (AIF) datasets.

## When NOT to use

- Spectra are already in vendor-specific binary formats (e.g., .raw, .d) without prior centroiding — use raw data conversion and feature detection tools (e.g., xcms) first.
- Input is a pre-built feature table or annotated result set — use this skill only for library/database generation, not for annotation of experimental data.
- Spectra lack ionization-mode or adduct-type metadata — the function requires this information to correctly assign positive/negative suffixes.

## Inputs

- MS/MS spectral records in .msp file format (MassBank-compatible or equivalent)
- Noise threshold and marker peak intensity parameters (configurable)
- Ionization mode metadata (adduct type annotations in spectral headers)

## Outputs

- .csv library entries with columns for m/z, intensity, and occurrence scores
- Separate output files per ionization mode with '_pos' or '_neg' filename suffix
- Processed library entries ready for use in annotateRC or other annotation workflows

## How to apply

Load the .msp spectral library file into MetaboAnnotatoR's mspToLib function, which parses individual MS/MS spectral records and applies configurable peak-picking with user-defined noise thresholds and marker peak intensity cutoffs. For each spectrum, the function detects fragment peaks, assigns occurrence scores to quantify peak reproducibility or intensity rank, and classifies the ionization mode (positive or negative) based on adduct type annotations in the spectral metadata. Output filenames are automatically suffixed with mode indicators (e.g., '_pos', '_neg'). Write all resulting .csv library entries to a designated output directory. Validation involves confirming that all spectra were parsed, each output file contains the expected columns (m/z, intensity, occurrence scores), and ionization-mode assignments match the adduct annotations in the input metadata.

## Related tools

- **MetaboAnnotatoR** (Primary R package providing mspToLib function for batch spectral record parsing, peak-picking, and library entry generation) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher required) for executing mspToLib and managing .csv output workflows)
- **MassBank** (Public MS/MS spectral database providing .msp-format records for library generation (optional source))

## Examples

```
library(MetaboAnnotatoR); mspToLib(mspfile="MassBank_example.msp", output_dir="./library_output", noise_threshold=5, marker_peak_threshold=10)
```

## Evaluation signals

- All input .msp records are parsed without errors; output .csv count matches expected spectrum count.
- Each output .csv contains valid m/z and intensity columns; occurrence scores are numeric and fall within expected range (e.g., 0–1 or 0–100 depending on normalization).
- Ionization-mode suffixes ('_pos' or '_neg') correctly reflect adduct type detected in input spectral metadata; no misclassified modes.
- Output filenames follow expected pattern (basename + mode suffix + '.csv'); no duplicate or truncated entries.
- Downstream annotation using annotateRC successfully matches output library entries against experimental features without format errors.

## Limitations

- Requires input spectra to be in centroid mode; raw profile-mode data must be converted prior to this step.
- Peak-picking thresholds (noise, marker peak intensity) must be empirically optimized for each spectral data source; defaults may not suit all ionization methods or instrumental configurations.
- Ionization-mode assignment depends on accurate adduct metadata in the .msp header; missing or incorrect adduct annotations will produce misclassified output files.
- Batch processing does not include cross-spectrum deduplication or quality filtering; redundant or low-quality spectra will be carried into the library unless pre-filtered.

## Evidence

- [other] mspToLib function converts MS/MS spectra from .msp files into MetaboAnnotatoR library entries: "The mspToLib function reads MS/MS spectra from .msp files, applies peak-picking with configurable noise and marker peak thresholds, assigns occurrence scores to detected peaks, and outputs library"
- [intro] MS/MS spectrum format and metadata requirements: "MS/MS spectrum of D-Pantothenic Acid [M+H]+ adduct from MassBank, accession code: MSBNK-RIKEN-PR100295"
- [readme] Intended use of mspToLib in the MetaboAnnotatoR vignette suite: "Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format)."
- [readme] Centroid mode requirement for raw data: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [other] Workflow step: parse spectral records and generate library entries: "Execute mspToLib with default parameters to parse the MSP spectral records and generate individual .csv entries."
