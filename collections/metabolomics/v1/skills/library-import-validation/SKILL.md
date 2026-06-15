---
name: library-import-validation
description: Use when you have raw .msp spectral library files (e.g., from MassBank or custom sources) and need to convert them into a structured CSV library format for use in metabolite annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnnotatoR
  - R
  - BiocManager
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
---

# Library Import and Validation

## Summary

Validate that MS/MS spectral libraries imported from .msp files or other sources are correctly converted into appropriately formatted and annotated CSV library entries with proper ionisation mode designation and peak-picking thresholds applied. This skill ensures spectral databases are ready for metabolite annotation workflows.

## When to use

You have raw .msp spectral library files (e.g., from MassBank or custom sources) and need to convert them into a structured CSV library format for use in metabolite annotation. Apply this skill when you need to verify that spectra are correctly parsed, peaks are filtered by noise and intensity thresholds, and files are organised by ionisation mode (positive/negative) before performing feature annotation.

## When NOT to use

- Input is already in CSV or tabular format — use direct ingestion instead of conversion.
- Spectral data is in a format other than .msp (e.g., mzML, mzXML) — those require different parsers.
- You need to curate or modify peak annotations after import — defer peak-picking until after library validation.

## Inputs

- .msp spectral library file (e.g., MassBank_example.msp)
- Peak-picking parameter specification (noise threshold, marker peaks score, marker peaks threshold)
- Output directory path for CSV library entries

## Outputs

- Per-spectrum CSV library entries named with ionisation mode suffixes (e.g., *_positive.csv, *_negative.csv)
- Organised directory structure grouping CSV files by mode
- Annotated CSV columns containing m/z, intensity, and occurrence scores for filtered peaks

## How to apply

Use the mspToLib function in MetaboAnnotatoR to read the .msp library file and convert each spectrum record into an individual CSV entry stored in a user-defined output directory. Apply default peak-picking parameters: noise threshold of 0.005, marker peaks score of 0.9, and marker peaks threshold of 0.1 to filter peaks above background and assign occurrence scores. Each output CSV file should be named with a mode-specific suffix ('positive' or 'negative') corresponding to the ionisation mode of the spectrum. After conversion, verify that the CSV entries contain complete spectral annotations (m/z, intensity, peak counts) and that the directory structure reflects the correct mode organisation. Spot-check a sample of converted spectra against the original .msp records to confirm accurate peak filtering and metadata transfer.

## Related tools

- **MetaboAnnotatoR** (Provides mspToLib function to convert .msp spectral records into CSV library entries with configurable peak-picking and mode-based file naming) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Execution environment for MetaboAnnotatoR functions; version 4.5.0 or higher required)
- **BiocManager** (Dependency manager for installing Bioconductor packages required by MetaboAnnotatoR)

## Examples

```
mspToLib(mspFile='MassBank_example.msp', outputDir='./csv_libraries', noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)
```

## Evaluation signals

- Output CSV files are created for each spectrum with correct ionisation mode suffix in filename
- Spot-check of CSV content confirms presence of m/z, intensity, and occurrence score columns with no missing values for peaks above noise and marker peak thresholds
- Peak count and intensity distributions in CSV entries match the filtered peaks in original .msp records (peaks below noise=0.005 and mpeaksThres=0.1 are absent)
- Directory structure groups CSV files correctly by mode (positive vs. negative ionisation), with no mode misclassification
- All spectra from the input .msp file are represented in the output directory with no missing or duplicate entries

## Limitations

- The mspToLib function requires .msp input format; other spectral file formats (mzML, mzXML, NetCDF) are not supported by this function and require alternative converters.
- Peak occurrence scores are assigned only to peaks meeting both the noise threshold (0.005) and marker peaks threshold (0.1); weak peaks below these cutoffs are discarded and cannot be recovered post-import.
- No changelog or version history is documented in the package, limiting traceability of changes to the conversion algorithm across releases.
- Ionisation mode designation must be present or inferrable in the .msp file metadata; spectra with missing or ambiguous mode information may fail to generate correctly named output files.

## Evidence

- [other] The mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file name: "The mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file"
- [other] Occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters: "occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)"
- [readme] Generation of Metabolite fragment database entry from MS/MS spectra from public databases in .msp format: "Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format)"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [other] the fragment libraries need to be specified: "the fragment libraries need to be specified"
