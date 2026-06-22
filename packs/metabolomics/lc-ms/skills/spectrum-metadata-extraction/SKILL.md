---
name: spectrum-metadata-extraction
description: Use when when you have raw mass spectrometry data from diverse instrument vendors (Thermo, Sciex, etc.) and need to harmonize and standardize spectrum-level metadata—including scan information, precursor m/z and charge, and ion selection parameters—into a queryable, vendor-agnostic tabular schema.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - R
  - Rust mzPeak library
  - pyarrow
  - arrow (R package)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is also an R implementation in `R/`
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

# spectrum-metadata-extraction

## Summary

Extract and structure spectrum-level metadata (descriptions, scans, precursors, selected ions) from mass spectrometry data into a Parquet-backed tabular format using the mzPeak specification. This skill enables standardized metadata capture and interoperability across different MS instrument vendors and data pipelines.

## When to use

When you have raw mass spectrometry data from diverse instrument vendors (Thermo, Sciex, etc.) and need to harmonize and standardize spectrum-level metadata—including scan information, precursor m/z and charge, and ion selection parameters—into a queryable, vendor-agnostic tabular schema prior to downstream spectral analysis, identification, or cross-platform data sharing.

## When NOT to use

- If you need read/write capabilities for metadata modification in Python or R—only the Rust implementation supports writing; Python and R implementations support reading only.
- If your MS data is already in a finalized, vendor-locked binary format and you require lossless round-trip conversion without access to the mzPeak Rust toolchain.
- If spectrum-level metadata is minimal or absent (e.g., centroid-only data with no precursor information), as the packed parallel table structure assumes hierarchical metadata is available.

## Inputs

- Raw mass spectrometry data files (mzML, vendor proprietary formats: Thermo .raw, Sciex .wiff, etc.)
- Instrument metadata (vendor, model, configuration parameters)
- Spectrum list with scan numbers and precursor information

## Outputs

- spectra_metadata.parquet file (Parquet table within mzPeak archive)
- Structured tabular metadata with columns: spectrum_index, scan_number, precursor_mz, precursor_charge, selected_ion_mz, precursor_isolation_window_lower_mz, precursor_isolation_window_upper_mz, and optional vendor-specific fields
- mzpeak_index.json (archive manifest)

## How to apply

Load the raw MS data (mzML, proprietary vendor formats, or other MS archive) using the appropriate language-specific mzPeak reader (Rust for full read/write, Python or R arrow implementation for read-only access). Extract spectrum-level fields including spectrum descriptions, scan indices, precursor m/z, precursor charge, selected ion windows, and any instrument-specific metadata using the packed parallel table structure defined in spectra_metadata.parquet. Map vendor-specific terms to controlled vocabulary terms where feasible (using HUPO-PSI CV recommendations) and serialize the result into Parquet format within the mzPeak archive. Validate that all required columns are present and non-null for critical fields (spectrum index, scan number, precursor m/z) and verify that the row count matches the number of spectra in the source data.

## Related tools

- **Rust mzPeak library** (Primary implementation for reading and writing mzPeak files and converting existing MS formats into mzPeak with full metadata extraction) — https://github.com/HUPO-PSI/mzPeak
- **pyarrow** (Python backend for reading and parsing Parquet-encoded spectrum metadata from mzPeak archives) — https://arrow.apache.org/docs/python/index.html
- **arrow (R package)** (R backend for reading and extracting spectrum metadata from mzPeak Parquet tables) — https://arrow.apache.org/docs/r/
- **OpenMS** (Complementary MS data processing framework for validation and manipulation of spectrum metadata) — https://www.openms.de/

## Evaluation signals

- All spectrum records are present in spectra_metadata.parquet with row count matching source data spectrum count
- Critical metadata columns (spectrum_index, scan_number, precursor_mz, precursor_charge) are non-null for MS/MS spectra and properly typed (integers for indices/charges, floats for m/z values)
- Precursor isolation windows (lower_mz, upper_mz) satisfy the invariant: lower_mz < precursor_mz < upper_mz for all records
- Controlled vocabulary terms (e.g., polarity, activation method) match HUPO-PSI CV or are traceable to external ontologies
- mzpeak_index.json correctly lists spectra_metadata.parquet and validates against the mzPeak JSON Schema

## Limitations

- The R and Python implementations support read-only access to metadata; modifications require the Rust implementation.
- Metadata extraction fidelity depends on vendor format documentation; proprietary or undocumented vendor fields may be lost during conversion.
- The packed parallel table structure assumes hierarchical metadata is present; sparse or degenerate metadata (e.g., missing precursors for all scans) will result in many null values and reduced storage efficiency.
- mzPeak specification is in work-in-progress status with no stability guarantee at this point; schema changes in future versions may require re-extraction of existing archives.

## Evidence

- [readme] Spectrum level metadata and file-level metadata. Includes spectrum descriptions, scans, precursors, and selected ions using packed parallel tables.: "Spectrum level metadata and file-level metadata. Includes spectrum descriptions, scans, precursors, and selected ions using packed parallel tables."
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak: "including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak"
- [readme] There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`]: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
- [readme] There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`] for _reading_ only at this time.: "complete re-implementation using the [`arrow`] for _reading_ only at this time"
- [readme] mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents.: "descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents"
- [readme] **NOTE**: This is a **work in progress**, no stability is guaranteed at this point.: "This is a **work in progress**, no stability is guaranteed at this point."
