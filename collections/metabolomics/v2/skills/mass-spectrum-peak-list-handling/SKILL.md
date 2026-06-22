---
name: mass-spectrum-peak-list-handling
description: Use when you have raw or preprocessed electron ionization (EI) mass spectral data that must be stored in, retrieved from, or validated against the MSP file format (used by NIST MS Search and similar spectral library tools).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mssearchr
  - R
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users
- enhance the capabilities of R users for conducting library searches
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  dedup_kept_from: coll_mspepsearchr_cq
schema_version: 0.2.0
---

# mass-spectrum-peak-list-handling

## Summary

Parse, validate, and write mass spectral peak lists in MSP (NIST MS Search) format, ensuring compliance with MSP specification conventions for precursor m/z, peak intensities, metadata annotations, and delimiter formatting. This skill enables reproducible round-trip I/O of spectral databases for downstream library search and comparison workflows.

## When to use

You have raw or preprocessed electron ionization (EI) mass spectral data that must be stored in, retrieved from, or validated against the MSP file format (used by NIST MS Search and similar spectral library tools). Apply this skill when you need to: (1) ingest an existing MSP spectral library into an R data structure for programmatic analysis; (2) construct new MSP records from peak lists and metadata; (3) ensure round-trip fidelity (read → parse → modify → write → re-read) of spectral records; or (4) validate that exported spectra conform to MSP header field and peak list conventions.

## When NOT to use

- Input spectral data is already in a different standardized format (mzML, mzXML, NetCDF) and does not require MSP export for NIST API or MS Search compatibility.
- Peak lists have already been aggregated, binned, or merged into a feature table (e.g., for statistical comparison); this skill reconstructs individual spectra, not summary matrices.
- Spectral ionization method is not electron ionization (EI); mssearchr is designed for EI mass spectral databases.

## Inputs

- MSP (NIST MS Search) spectral library file (plain text)
- Peak list records with precursor m/z, peak m/z–intensity pairs, and metadata annotations
- R data frame or list of spectrum objects (for writing)

## Outputs

- In-memory R data structure (list or data frame) of parsed spectrum objects
- MSP-formatted text file with header fields, peak lists, and metadata
- Validation report comparing original and round-trip parsed fields

## How to apply

Load an MSP spectral library file using mssearchr's MSP parser, which deserializes the file into an in-memory R data structure (list or data frame of spectrum objects). Extract and validate key spectral fields from each record: precursor m/z, peak list (m/z–intensity pairs), and metadata annotations (name, formula, CAS number, etc.). Inspect peak list format compliance with MSP specification—peaks must follow the delimiter and range conventions expected by NIST tools. Write the parsed spectra back to a new MSP file using mssearchr's MSP writer, enforcing format compliance with MSP specification (header field order, peak list delimiters, and conventions). Verify output file structure by reading the newly written MSP file back and comparing parsed fields (precursor m/z, peak counts, metadata) to the original input records; exact field-by-field equivalence confirms correct serialization.

## Related tools

- **mssearchr** (Implements MSP file parser and writer; provides read/write methods for serializing and deserializing spectrum objects in MSP format) — https://github.com/AndreySamokhin/mssearchr
- **R** (Host language for mssearchr; provides data structures (lists, data frames) to hold parsed spectra and metadata)

## Examples

```
# R: Parse MSP file, validate, and write back
library(mssearchr)
spectra <- read.msp('library.msp')
write.msp(spectra, 'library_output.msp')
spectra_verify <- read.msp('library_output.msp')
# Compare spectra and spectra_verify for field equivalence
```

## Evaluation signals

- Round-trip fidelity: parsed fields from re-read output match original input fields exactly (precursor m/z, peak count, metadata strings).
- MSP format compliance: output file header fields appear in correct order, peak list delimiters (space, tab, newline) match MSP specification, and no truncation or corruption of metadata occurs.
- Peak list integrity: all peaks from input are present in output; no spurious peaks are introduced; m/z and intensity values are preserved within numerical precision.
- Field validation: extracted precursor m/z is numeric and plausible (typically 50–2000); peak intensities are non-negative; metadata annotations (name, formula) are non-empty strings.
- Schema consistency: output MSP records conform to expected header structure (Name:, Precursor m/z:, Num Peaks:, etc.) as defined by NIST MSP specification.

## Limitations

- mssearchr is designed specifically for electron ionization (EI) spectral databases; applicability to other ionization methods (ESI, APCI, MALDI) is not documented.
- No changelog is available for the package, limiting transparency on format version support and backward compatibility.
- Round-trip validation depends on exact field matching; numerical precision differences in m/z or intensity values may cause validation to fail even if practical equivalence is acceptable.

## Evidence

- [other] The mssearchr package implements reading and writing capabilities for msp files as part of its toolkit for mass spectral database operations.: "The mssearchr package implements reading and writing capabilities for msp files"
- [other] MSP parser loads spectral library files into in-memory R data structures and MSP writer ensures format compliance.: "Load an MSP spectral library file using mssearchr's MSP parser into an in-memory R data structure (list or data frame of spectrum objects)"
- [other] Validation requires extracting and comparing key spectral fields from records.: "Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations)"
- [other] Output verification via round-trip comparison ensures correctness.: "Verify output file structure by reading it back and comparing parsed fields to the original input records"
- [readme] mssearchr provides tools for reading and writing MSP files.: "reading/writing *msp* files"
