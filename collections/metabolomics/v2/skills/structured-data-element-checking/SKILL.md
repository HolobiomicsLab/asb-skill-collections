---
name: structured-data-element-checking
description: Use when you have generated or received a mass spectrometry data file
  in a structured format (e.g., mzPeak, Parquet-based archive) and need to verify
  it conforms to the published specification before use in analysis pipelines, sharing
  with collaborators, or publishing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - Rust mzpeak library
  - pyarrow
  - arrow (R package)
  - mzPeak specification (living document)
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mzpeak
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00435
  all_source_dois:
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structured Data Element Checking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a structured data file (e.g., mzPeak archive or Parquet table) contains all mandatory fields and structural elements required by a published specification. This ensures compliance before downstream processing or publication.

## When to use

You have generated or received a mass spectrometry data file in a structured format (e.g., mzPeak, Parquet-based archive) and need to verify it conforms to the published specification before use in analysis pipelines, sharing with collaborators, or publishing. This is especially critical when the file was produced by a new or prototype implementation.

## When NOT to use

- The input file is already known to be compliant (e.g., produced by a certified reference implementation and previously validated).
- The specification document does not exist or is not publicly available; compliance checking requires a normative reference.
- The task is to *correct* non-compliant files rather than *detect* non-compliance; that requires transformation, not validation.

## Inputs

- mzPeak archive file (ZIP containing Parquet tables and JSON metadata)
- Published specification document (Markdown or HTML, containing mandatory field list and schema constraints)
- File format specification (JSON Schema or equivalent normative definition)

## Outputs

- Compliance report (text or JSON) documenting pass/fail for each mandatory field
- List of absent mandatory fields (if any)
- Schema mismatch report (field types, column names, structural deviations)
- Overall specification conformance status (pass/fail)

## How to apply

Retrieve the canonical specification document (e.g., from https://hupo-psi.github.io/mzPeak-specification/ for mzPeak) and extract the exhaustive list of mandatory fields and required structural elements (e.g., for mzPeak: `mzpeak_index.json`, `spectra_metadata.parquet`, `spectra_data.parquet`, and their required schema columns). Open the data file using a language-native library that supports both reading and structural introspection (e.g., Rust `mzpeak` crate, Python `pyarrow`, or R `arrow` package). Programmatically parse the file's root schema and metadata layers to enumerate all present fields and sub-structures. Cross-check each mandatory element against the parsed inventory, recording presence/absence and schema conformance. Generate a compliance report that documents pass/fail status for each mandatory field, noting any missing elements or schema mismatches.

## Related tools

- **Rust mzpeak library** (Read and parse mzPeak archives; introspect file schema and metadata structure for compliance verification) — https://github.com/HUPO-PSI/mzPeak
- **pyarrow** (Read and inspect Parquet table schemas and contents in Python; extract mandatory field inventory) — https://arrow.apache.org/docs/python/index.html
- **arrow (R package)** (Read and inspect Parquet table schemas in R; verify structural conformance) — https://arrow.apache.org/docs/r/
- **mzPeak specification (living document)** (Authoritative reference for mandatory fields, structural elements, and schema constraints) — https://hupo-psi.github.io/mzPeak-specification/

## Evaluation signals

- All mandatory fields listed in the specification are present in the parsed file with correct data types.
- The file contains all required Parquet tables (`mzpeak_index.json`, `spectra_metadata.parquet`, `spectra_data.parquet`) and optional tables (e.g., `spectra_peaks.parquet`) are correctly declared in the index.
- Packed parallel table structures (struct/group columns in `spectra_metadata.parquet` and `chromatograms_metadata.parquet`) match the specification's branching schema; all required sub-fields are present or correctly nullable.
- File-level metadata stored in Parquet metadata segments can be parsed as valid JSON documents conforming to the JSON Schemas in the specification's `schema/` directory.
- Compliance report shows 100% pass rate for mandatory elements and documents any optional or vendor-specific extensions separately.

## Limitations

- The mzPeak format is described as 'work in progress' with 'no stability guarantee'; mandatory field lists or schemas may change between specification versions, requiring re-validation after specification updates.
- Python and R implementations support *reading only*; compliance checking of write operations requires the Rust implementation or conversion to Rust for full coverage.
- Zero run stripping and null marking techniques for profile data may not be detected by schema alone; semantic validation of m/z spacing reconstruction or peak model fidelity requires additional computational checks beyond structural compliance.
- The specification is maintained as a living document; there is no published changelog, so practitioners must monitor the repository for breaking changes to mandatory field definitions.

## Evidence

- [other] Does the Rust implementation of mzPeak produce files that conform to all mandatory fields and structural elements defined in the published mzPeak specification?: "Does the Rust implementation of mzPeak produce files that conform to all mandatory fields and structural elements defined in the published mzPeak specification?"
- [other] Cross-check all mandatory fields and structural elements from the specification against the parsed file contents.: "Cross-check all mandatory fields and structural elements from the specification against the parsed file contents."
- [readme] The spectra_metadata.parquet and chromatograms_metadata.parquet store multiple schemas in parallel. In these Parquet files, the root schema is made up of several branched 'group' or 'struct' (Parquet vs. Arrow nomenclature) that may be null at any level.: "The spectra_metadata.parquet and chromatograms_metadata.parquet store multiple schemas in parallel. In these Parquet files, the root schema is made up of several branched 'group' or 'struct'"
- [readme] mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents.: "mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents."
- [readme] Components of an mzPeak archive: mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, spectra_peaks.parquet (optional), chromatograms_metadata.parquet, chromatograms_data.parquet: "Components of an mzPeak archive: - `mzpeak_index.json`: Definition of the files present in the archive - `spectra_metadata.parquet`: Spectrum level metadata - `spectra_data.parquet`: Spectrum signal"
