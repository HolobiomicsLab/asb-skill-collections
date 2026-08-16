---
name: tabular-data-field-comparison
description: Use when you have multiple independent implementations of the same data
  format reader (e.g., Rust, Python, R versions) and need to verify they produce identical
  or equivalent output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - Python
  - pyarrow
  - R
  - Rust mzPeak library
  - R arrow
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is a separate Python implementation in `python/`
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tabular Data Field Comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare structured tabular outputs (CSV, Parquet) exported from independent implementations of the same file reader to detect field-level discrepancies in names, types, row counts, and numerical values. This skill validates implementation interoperability and identifies divergences in data interpretation across language/library variants.

## When to use

Apply this skill when you have multiple independent implementations of the same data format reader (e.g., Rust, Python, R versions) and need to verify they produce identical or equivalent output. Use it to validate that a newly written reader implementation (in one language) produces the same spectrum table structure and numerical content as an existing trusted implementation.

## When NOT to use

- Input is a single implementation or vendor output; comparison requires at least two independent readers.
- Field definitions or data types are intentionally different across implementations by design (e.g., different precision levels for intentional lossy compression).
- Input file format is already validated or certified by a reference standard; this skill is for early-stage interoperability testing, not final certification.

## Inputs

- mzPeak file (ZIP archive containing Parquet files)
- Three or more independent reader implementations (Rust library, Python pyarrow implementation, R arrow implementation)

## Outputs

- CSV export of spectrum metadata table from each implementation
- CSV export of spectrum signal data table from each implementation
- Consistency report documenting field-level agreement and discrepancies
- Validation status summary (pass/fail per implementation pair)

## How to apply

Load the same input file (e.g., an mzPeak archive) sequentially using each independent implementation—Rust, Python/pyarrow, and R/arrow—and export the resulting spectrum metadata or signal tables to CSV format for easy textual comparison. Compare the three CSV outputs systematically: first check schema agreement (field names, declared data types, row counts match), then validate numerical equality field-by-field, paying attention to floating-point precision and integer representation. Generate a structured consistency report documenting which fields agree, which diverge, and whether divergences are due to implementation bugs, format interpretation differences, or acceptable numerical tolerances. Use field-level agreement as the primary validation criterion, since row count and schema matching alone are insufficient to confirm correctness.

## Related tools

- **Rust mzPeak library** (Primary read/write implementation used to load test file and export reference spectrum table) — https://github.com/HUPO-PSI/mzPeak
- **pyarrow** (Python Parquet reader for loading mzPeak table files and exporting to CSV) — https://arrow.apache.org/docs/python/index.html
- **R arrow** (R Parquet reader for loading mzPeak table files and exporting to CSV) — https://arrow.apache.org/docs/r/
- **OpenMS** (Reference mass spectrometry toolkit; mzPeak name held in trust by OpenMS Inc.)

## Evaluation signals

- Field names match exactly across all three CSV exports (including order and case sensitivity).
- Data types inferred from CSV content (integer, float, string, null) agree across implementations for each column.
- Row counts are identical across all three CSV outputs.
- Numerical values in floating-point columns agree within an acceptable precision tolerance (e.g., within machine epsilon or a domain-specific threshold like 1e-6 relative error).
- No spurious nulls or NaN values appear in one implementation but not others (unless intentional per format design, such as null marking for zero-run-stripped regions).

## Limitations

- The mzPeak format is work-in-progress with no stability guarantee at this point; field definitions or semantics may change.
- Python and R implementations support reading only; if testing write capability, only Rust can produce reference outputs.
- Floating-point precision differences (e.g., f32 vs. f64 representation) may introduce small numerical divergences that are valid but require tolerance tuning.
- The skill does not validate semantic correctness (e.g., whether a m/z value makes physical sense); it only checks consistency across implementations.

## Evidence

- [other] Do the Rust, Python/pyarrow, and R/arrow implementations of mzPeak file readers produce field-level agreement when loading the same input file?: "Do the Rust, Python/pyarrow, and R/arrow implementations of mzPeak file readers produce field-level agreement when loading the same input file?"
- [other] Compare the three CSV outputs field-by-field to identify any discrepancies in field names, data types, row counts, and numerical values.: "Compare the three CSV outputs field-by-field to identify any discrepancies in field names, data types, row counts, and numerical values."
- [other] Three independent mzPeak reader implementations exist: a Rust library, a Python implementation using pyarrow, and an R implementation using arrow, all capable of reading mzPeak files.: "Three independent mzPeak reader implementations exist: a Rust library, a Python implementation using pyarrow, and an R implementation using arrow, all capable of reading mzPeak files."
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak.: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the PyData stack.: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
