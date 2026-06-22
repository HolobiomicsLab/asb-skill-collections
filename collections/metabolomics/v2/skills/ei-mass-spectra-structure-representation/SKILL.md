---
name: ei-mass-spectra-structure-representation
description: Use when you have raw or archived MSP spectral library files and need to load them into R for library searching, spectral matching, or batch reprocessing. Specifically, when you must extract precursor m/z values, peak intensity pairs, and spectrum metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - mssearchr
  - R
  - NIST API
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

# ei-mass-spectra-structure-representation

## Summary

Parse electron ionization mass spectral data from MSP (NIST MS Search) files into structured R data objects, extracting and validating precursor m/z, peak lists, and metadata annotations for downstream library search and spectral comparison workflows.

## When to use

You have raw or archived MSP spectral library files and need to load them into R for library searching, spectral matching, or batch reprocessing. Specifically, when you must extract precursor m/z values, peak intensity pairs, and spectrum metadata (e.g., compound name, formula, CAS number) in a format compatible with Identity (EI Normal) or Similarity (EI Simple) matching algorithms.

## When NOT to use

- Spectral data is already in memory as an R data frame or list of spectrum objects—no parsing needed.
- Input is in a non-MSP format (e.g., mzML, mzXML, NetCDF)—use format-specific parsers instead.
- You only need to perform spectral matching without reconstructing or validating file structure.

## Inputs

- MSP spectral library file (text format with NIST MS Search structure)
- Precursor m/z values
- Peak list (m/z–intensity pairs)
- Spectrum metadata (name, formula, CAS, etc.)

## Outputs

- R data structure (list or data frame) of spectrum objects
- Parsed spectrum records with validated fields
- MSP-compliant output file (if written back)
- Comparison report (input vs. parsed field agreement)

## How to apply

Use the mssearchr MSP parser to load an MSP file into an in-memory R data structure (list or data frame of spectrum objects). Extract and validate key spectral fields from each record: precursor m/z, peak m/z–intensity pairs, and header metadata. Ensure compliance with MSP specification format conventions (delimiters, header field order, peak list structure). After processing, verify correctness by reading the output file back and comparing parsed fields against the original input records to detect parsing errors or format drift.

## Related tools

- **mssearchr** (MSP file parser and writer; implements precursor m/z and peak extraction; provides Identity (EI Normal) and Similarity (EI Simple) matching algorithms for validating parsed spectra) — https://github.com/AndreySamokhin/mssearchr
- **R** (Host environment for mssearchr; provides data structures (lists, data frames) to store parsed spectrum objects)
- **NIST API** (Optional downstream tool for library search validation; mssearchr can call nistms$.exe to cross-check parsed spectra against NIST reference library)

## Examples

```
library(mssearchr); spec_list <- parse_msp('reference_library.msp'); validated_spec <- validate_spectra(spec_list); write_msp(validated_spec, 'output_library.msp')
```

## Evaluation signals

- Parsed precursor m/z values match header entries in the original MSP file exactly.
- Peak list m/z and intensity pairs are extracted without loss or truncation; row counts and numeric ranges match input.
- Metadata fields (compound name, formula, CAS number, etc.) are correctly assigned to their corresponding spectrum records.
- Output MSP file written by mssearchr writer passes round-trip validation: re-reading and comparing field values shows zero discrepancies with input records.
- No parsing errors or format-compliance warnings are raised; error logs and audit trails confirm successful header and peak-list validation.

## Limitations

- No changelog available; version compatibility and breaking changes are not documented.
- Parsing success depends on strict adherence to MSP format specification; non-standard or malformed MSP files may fail or be truncated.
- The skill is specific to electron ionization (EI) mass spectra; other ionization modes (ESI, APCI, etc.) may not be supported.
- Large MSP files (millions of spectra) may incur memory overhead in R; batch or streaming processing strategies are not mentioned.

## Evidence

- [readme] reading/writing *msp* files: "reading/writing *msp* files"
- [other] Load an MSP spectral library file using mssearchr's MSP parser into an in-memory R data structure (list or data frame of spectrum objects).: "Load an MSP spectral library file using mssearchr's MSP parser into an in-memory R data structure (list or data frame of spectrum objects)."
- [other] Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations).: "Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations)."
- [other] Write the parsed spectra back to a new MSP file using mssearchr's MSP writer, ensuring format compliance with MSP specification (header fields, peak list format, delimiter conventions).: "Write the parsed spectra back to a new MSP file using mssearchr's MSP writer, ensuring format compliance with MSP specification (header fields, peak list format, delimiter conventions)."
- [other] Verify output file structure by reading it back and comparing parsed fields to the original input records.: "Verify output file structure by reading it back and comparing parsed fields to the original input records."
- [readme] The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases.: "The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases."
