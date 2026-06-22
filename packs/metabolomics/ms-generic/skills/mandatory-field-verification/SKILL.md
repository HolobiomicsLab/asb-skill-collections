---
name: mandatory-field-verification
description: Use when after generating mzPeak files from prototype implementations (Rust, Python, R, or .NET) or after format conversion, and before integrating files into a mass spectrometry data repository or sharing them with collaborators. Use it when specification compliance is a hard requirement (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - Rust mzPeak library
  - pyarrow
  - Apache Arrow (R)
  - mzPeak-specification (HUPO-PSI)
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mandatory-field-verification

## Summary

Validate that mzPeak file outputs conform to all mandatory fields and structural requirements defined in the published specification by systematically comparing parsed file contents against the normative schema. This skill ensures compliance before downstream consumption or publication.

## When to use

Apply this skill after generating mzPeak files from prototype implementations (Rust, Python, R, or .NET) or after format conversion, and before integrating files into a mass spectrometry data repository or sharing them with collaborators. Use it when specification compliance is a hard requirement (e.g., HUPO-PSI submission, multi-platform interoperability testing, or benchmark comparison).

## When NOT to use

- The input file is not mzPeak format (e.g., mzML, mzXML, NetCDF) — use format conversion first.
- The specification version is unknown or the file was generated against a different, undocumented specification version — conformance is version-specific.
- Only reading or visualizing spectrum data without reference to the specification — schema validation is a separate concern from data exploration.

## Inputs

- mzPeak specification document (Markdown source or published HTML from https://hupo-psi.github.io/mzPeak-specification/)
- mzPeak file (uncompressed ZIP archive containing Parquet tables and mzpeak_index.json)
- JSON Schema files from schema/ directory defining mandatory field structure

## Outputs

- Compliance report documenting mandatory field presence/absence
- List of non-conforming fields or structural deviations
- Overall specification conformance status (pass/fail)
- Parsed mzPeak file structure (tables, columns, metadata)

## How to apply

Begin by retrieving the canonical mzPeak specification from https://hupo-psi.github.io/mzPeak-specification/ and extracting the list of mandatory fields and required structural elements from the specification document (organized under docs/foundations/, docs/layouts/, and docs/schemas/). Obtain or generate a test mzPeak file using the Rust implementation's write functionality or format conversion tools. Parse the mzPeak archive (an uncompressed ZIP containing Parquet files: mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, and optional chromatograms_*.parquet) using the Rust library's reading functionality to examine the internal structure, schema, and field contents of each Parquet table. Cross-reference all mandatory fields from the specification (e.g., spectrum-level metadata, packed parallel table structures, zero-run-stripped point layout or chunked layout encoding, null marking for sparse m/z arrays) against the parsed file. Document which mandatory fields are present, which are absent, and whether structural elements (e.g., JSON metadata segments in Parquet headers, controlled vocabulary terms, packed parallel group hierarchies) match the normative schema. Generate a compliance report summarizing the overall conformance status and any deviations.

## Related tools

- **Rust mzPeak library** (Read and parse mzPeak files to access internal Parquet structure and metadata for field extraction and validation) — https://github.com/HUPO-PSI/mzPeak
- **OpenMS** (Reference implementation and format conversion tool for generating or validating mzPeak outputs)
- **pyarrow** (Python library for programmatically reading and inspecting Parquet tables within mzPeak archives) — https://arrow.apache.org/docs/python/index.html
- **Apache Arrow (R)** (R library for reading and introspecting mzPeak Parquet file structures) — https://arrow.apache.org/docs/r/
- **mzPeak-specification (HUPO-PSI)** (Authoritative source document defining all mandatory fields, structural elements, and controlled vocabulary terms) — https://github.com/HUPO-PSI/mzPeak-specification

## Evaluation signals

- All mandatory fields listed in the specification (e.g., spectrum-level metadata, m/z and intensity arrays, scan metadata) are present and non-null in the parsed file.
- Parquet schema matches the JSON Schema definitions in the specification's schema/ directory for each table (spectra_metadata.parquet, spectra_data.parquet, etc.).
- mzpeak_index.json correctly enumerates all Parquet files present in the ZIP archive with controlled vocabulary terms matching the specification.
- Packed parallel table structures are correctly formed (e.g., spectrum scan, precursor, and selected ion groups are properly nested and may be null at appropriate levels).
- Zero-run-stripped point layout or chunked layout encoding is applied as declared in file metadata, with validity buffers and null-marked m/z values consistent with the stored data.
- File-level metadata (JSON documents in Parquet metadata segments) conform to the specification's JSON Schemas for file description, instrumentation, and software.

## Limitations

- The specification is a working draft (HUPO-PSI recommendation in draft status) and may undergo breaking changes; compliance is tied to a specific specification version.
- This skill validates structural and mandatory field presence but does not assess semantic correctness (e.g., whether m/z values are physically plausible or whether controlled vocabulary terms are semantically appropriate).
- Python and R implementations currently support reading only; compliance testing of files generated by read-only implementations will always pass trivially. Write-capable implementations (Rust primary, .NET, TypeScript) must be used for round-trip validation.
- No changelog is currently provided in the specification document, making it difficult to track which fields became mandatory or optional across versions.
- The project is explicitly marked as 'work in progress' with 'no stability guaranteed at this point', so compliance against the current specification may not future-proof the file.

## Evidence

- [other] Does the Rust implementation of mzPeak produce files that conform to all mandatory fields and structural elements defined in the published mzPeak specification?: "Does the Rust implementation of mzPeak produce files that conform to all mandatory fields and structural elements defined in the published mzPeak specification?"
- [other] Retrieve the draft mzPeak specification document from the HUPO-PSI living specification repository at https://hupo-psi.github.io/mzPeak-specification/ and extract the list of mandatory fields and required structural elements.: "Retrieve the draft mzPeak specification document from the HUPO-PSI living specification repository at https://hupo-psi.github.io/mzPeak-specification/ and extract the list of mandatory fields and"
- [other] Parse the mzPeak file using the Rust library (reading functionality) to examine its internal structure and field contents.: "Parse the mzPeak file using the Rust library (reading functionality) to examine its internal structure and field contents."
- [other] Cross-check all mandatory fields and structural elements from the specification against the parsed file contents.: "Cross-check all mandatory fields and structural elements from the specification against the parsed file contents."
- [other] Generate a compliance report documenting which mandatory fields are present, which are absent, and overall specification conformance status.: "Generate a compliance report documenting which mandatory fields are present, which are absent, and overall specification conformance status."
- [readme] mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run.: "mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run."
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] **NOTE**: This is a **work in progress**, no stability is guaranteed at this point.: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
- [readme] mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents.: "mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents."
- [readme] The spectra_metadata.parquet and chromatograms_metadata.parquet store multiple schemas in parallel. In these Parquet files, the root schema is made up of several branched 'group' or 'struct' (Parquet vs. Arrow nomenclature) that may be null at any level.: "The spectra_metadata.parquet and chromatograms_metadata.parquet store multiple schemas in parallel. In these Parquet files, the root schema is made up of several branched 'group' or 'struct' (Parquet"
