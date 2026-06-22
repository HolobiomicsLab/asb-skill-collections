---
name: file-format-validation
description: Use when after writing parsed spectra to a new MSP file using mssearchr's MSP writer, or when integrating MSP files from external sources into an R analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0121
  tools:
  - mssearchr
  - R
  - Rust mzPeak library
  - pyarrow
  - arrow (R)
  - JSON Schema validators (various)
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
- doi: 10.1021/acs.jproteome.5c00435
  title: ''
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users
- enhance the capabilities of R users for conducting library searches
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  - build: coll_mzpeak_cq
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mspepsearchr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00322
  all_source_dois:
  - 10.1021/jasms.5c00322
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-validation

## Summary

Validate that parsed spectral data conforms to MSP file format specification by reading back written records and comparing key fields (precursor m/z, peaks, metadata, delimiters) to the original input. This ensures round-trip fidelity and prevents downstream errors in spectral database operations.

## When to use

After writing parsed spectra to a new MSP file using mssearchr's MSP writer, or when integrating MSP files from external sources into an R analysis pipeline. Validation is essential when round-trip integrity (read→parse→write→read) is required, or when downstream spectral matching (Identity or Similarity algorithms) depends on accurate peak lists and metadata annotations.

## When NOT to use

- Input file is already validated by a trusted upstream tool or database.
- MSP file is read-only reference data from a curated public repository (e.g., NIST).
- Validation overhead is prohibitive and data loss is acceptable (e.g., exploratory analysis only).

## Inputs

- MSP spectral library file (original)
- MSP spectral library file (newly written)
- Original parsed spectrum objects (list or data frame)

## Outputs

- Validation report (pass/fail per spectrum)
- Field-by-field comparison results (precursor m/z, peaks, metadata)
- Format compliance status (header fields, peak list format, delimiters)

## How to apply

Load the newly written MSP file back into R using mssearchr's MSP parser to reconstruct spectrum objects. Extract key spectral fields from the re-parsed records: precursor m/z, peak list (m/z and intensity pairs), and metadata annotations (e.g., name, formula, CAS number). Compare these fields element-wise to the original input records, checking for exact numeric equality on m/z and intensity values, string equality on metadata, and structural compliance with MSP specification conventions (header field ordering, peak delimiter format, line termination). Flag discrepancies in peak counts, missing annotations, or malformed delimiters as format violations that indicate writer or parser errors.

## Related tools

- **mssearchr** (MSP file parser and writer; provides read and write functions to reconstruct and serialize spectrum objects for validation) — https://github.com/AndreySamokhin/mssearchr
- **R** (Runtime environment for executing mssearchr functions and performing field-by-field comparisons)

## Evaluation signals

- Field-by-field equality: precursor m/z values match exactly (or within machine tolerance) between original and re-parsed records
- Peak list integrity: all peaks in the original input appear in the re-parsed file with identical m/z and intensity values
- Metadata preservation: string fields (name, formula, CAS, etc.) are unchanged after round-trip
- Structure compliance: MSP format conventions (header field order, peak delimiter style, line endings) match MSP specification
- Record count: number of spectra written equals number of spectra successfully re-parsed without truncation or duplication

## Limitations

- Validation depends on correct implementation of mssearchr's MSP parser and writer; bugs in either will propagate to validation results.
- Numeric precision loss (e.g., floating-point rounding) may cause false negatives if tolerance thresholds are too strict.
- MSP specification is loosely defined; validation cannot catch semantic errors in metadata (e.g., incorrect chemical formula) only syntactic ones.
- No changelog available for mssearchr; version-specific format changes or regressions cannot be tracked without external versioning.

## Evidence

- [other] Verify output file structure by reading it back and comparing parsed fields to the original input records.: "Verify output file structure by reading it back and comparing parsed fields to the original input records."
- [other] Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations).: "Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations)."
- [other] Write the parsed spectra back to a new MSP file using mssearchr's MSP writer, ensuring format compliance with MSP specification (header fields, peak list format, delimiter conventions).: "Write the parsed spectra back to a new MSP file using mssearchr's MSP writer, ensuring format compliance with MSP specification (header fields, peak list format, delimiter conventions)."
- [readme] reading/writing *msp* files: "reading/writing *msp* files"
