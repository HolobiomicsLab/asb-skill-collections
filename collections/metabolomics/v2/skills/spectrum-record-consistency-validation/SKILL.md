---
name: spectrum-record-consistency-validation
description: Use when when you have a mass spectrometry data file (such as mzPeak) that has been read by two or more independent implementations (e.g., Rust, Python/pyarrow, R/arrow) and need to verify that all implementations produce identical spectrum metadata, data types, row counts, and numerical values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - OpenMS
  - Python
  - pyarrow
  - R
  - Rust mzPeak library
  - Python pyarrow
  - R arrow
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
---

# spectrum-record-consistency-validation

## Summary

Validates field-level agreement in spectrum records across independent implementations of a mass spectrometry file format reader by exporting identical input files through multiple language stacks and comparing CSV outputs. This skill ensures that format specifications are correctly and consistently realized across Rust, Python, and R implementations.

## When to use

When you have a mass spectrometry data file (such as mzPeak) that has been read by two or more independent implementations (e.g., Rust, Python/pyarrow, R/arrow) and need to verify that all implementations produce identical spectrum metadata, data types, row counts, and numerical values. This is critical when validating a new or evolving format specification across multiple language ecosystems, or when verifying that a format migration or conversion is lossless across tool chains.

## When NOT to use

- The input file format is not supported by all three implementations (e.g., if one reader does not support writing or only reads a subset of the schema).
- You are comparing implementations that are intentionally designed to produce different outputs (e.g., lossy vs. lossless modes, different precision levels by design).
- The goal is to validate semantic correctness or biological accuracy rather than format compliance; this skill checks format consistency, not scientific validity.

## Inputs

- mzPeak file (test input file readable by all implementations)
- Rust mzPeak reader library
- Python pyarrow-based mzPeak reader
- R arrow-based mzPeak reader

## Outputs

- CSV export from Rust reader (spectrum table)
- CSV export from Python/pyarrow reader (spectrum table)
- CSV export from R/arrow reader (spectrum table)
- Consistency report documenting field-level agreement, divergences, and validation status

## How to apply

Load the same input mzPeak file using each independent reader implementation (Rust library, Python/pyarrow, R/arrow) and export the resulting spectrum tables to CSV format for deterministic comparison. Compare the three CSV outputs field-by-field, checking for agreement in field names, data types, row counts, and numerical values. Document any discrepancies (missing fields, type mismatches, row count divergences, or numerical precision differences) in a structured consistency report. The validation succeeds when all three implementations produce identical field sets, types, and row counts; numerical divergences should be inspected for acceptable floating-point rounding error (typically ≤1 ULP for 32-bit or 64-bit floats) versus genuine algorithmic or schema deviation. Use this skill to catch both specification ambiguities (where different implementers reasonably interpret the spec differently) and implementation bugs (where a single language version deviates from the others).

## Related tools

- **Rust mzPeak library** (Primary reference implementation for reading and writing mzPeak files; used to export CSV for comparison) — https://github.com/HUPO-PSI/mzPeak
- **Python pyarrow** (Parquet reader used in Python implementation of mzPeak reader; exports spectrum data to CSV) — https://arrow.apache.org/docs/python/index.html
- **R arrow** (Parquet reader used in R implementation of mzPeak reader; exports spectrum data to CSV) — https://arrow.apache.org/docs/r/
- **OpenMS** (Trusted holder of mzPeak format specification; reference for format semantics)

## Evaluation signals

- All three CSV exports have identical field names and are present in the same order.
- All three CSV exports have identical data types for each column (string, float32, float64, int32, etc.).
- All three CSV exports have identical row counts for each spectrum record.
- Numerical values in floating-point columns agree to within expected rounding error (≤1 ULP for the declared precision); integer columns must match exactly.
- The consistency report explicitly documents any divergences detected and either validates them as acceptable (e.g., documented precision differences) or flags them as non-compliant with the specification.

## Limitations

- The skill assumes all three implementations are available and functional; if one implementation is incomplete (e.g., the .NET or JavaScript versions are separately hosted and may have different maturity), they cannot be included in the comparison.
- Python and R implementations currently support reading only, not writing; if the input is modified or regenerated, only the Rust implementation can reliably write it back to mzPeak format for re-validation.
- The skill depends on deterministic CSV export (field order, precision formatting, line endings); non-determinism in export (e.g., floating-point to string conversion rounding, row ordering in edge cases) may cause false divergence signals.
- The mzPeak format is documented as work-in-progress with no stability guarantee; specification changes between implementations may be legitimate, not bugs, if the implementations predate specification updates.
- Null or missing value handling, sparse arrays (e.g., zero-run-stripped spectra), and optional nested structures (packed parallel tables) require careful field-by-field inspection; schema differences in how optional fields are represented may not be visually obvious in CSV.

## Evidence

- [other] Do the Rust, Python/pyarrow, and R/arrow implementations of mzPeak file readers produce field-level agreement when loading the same input file?: "Do the Rust, Python/pyarrow, and R/arrow implementations of mzPeak file readers produce field-level agreement when loading the same input file?"
- [other] Compare the three CSV outputs field-by-field to identify any discrepancies in field names, data types, row counts, and numerical values.: "Compare the three CSV outputs field-by-field to identify any discrepancies in field names, data types, row counts, and numerical values."
- [other] Generate a consistency report documenting field-level agreement, any divergences detected, and validation status across all three implementations.: "Generate a consistency report documenting field-level agreement, any divergences detected, and validation status across all three implementations."
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files"
- [readme] There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`], and the R implementation in `R/`, which is also a complete re-implementation using the [`arrow`] for _reading_ only: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`], and the R implementation in `R/`, which is also a complete"
