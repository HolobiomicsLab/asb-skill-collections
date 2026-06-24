---
name: cross-language-implementation-compatibility
description: Use when when a new file format specification has multiple language implementations
  and you need to validate that all implementations correctly interpret the specification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - Python
  - pyarrow
  - R
  - Rust mzPeak library
  - Python/pyarrow mzPeak reader
  - R/arrow mzPeak reader
  - Apache Arrow
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

# cross-language-implementation-compatibility

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that independent implementations of a file format reader (in Rust, Python/pyarrow, and R/arrow) produce field-level agreement when loading identical input files. This skill ensures interoperability and correctness of format specifications across language ecosystems before standardization.

## When to use

When a new file format specification has multiple language implementations and you need to validate that all implementations correctly interpret the specification. Use this skill if you have access to the same input file, multiple independent reader implementations, and require confidence that the format spec is unambiguous and implementations are correct before release or standardization.

## When NOT to use

- Input file is in a different format (mzML, mzXML, NetCDF) — this skill is specific to mzPeak files.
- Only one language implementation is available — the skill requires at least two independent implementations to test agreement.
- Implementations are known to intentionally differ (e.g., one uses lossy compression while another does not) — this skill assumes all implementations should produce identical output from identical input.

## Inputs

- mzPeak file (Parquet-based archive format)
- Rust mzPeak reader library
- Python/pyarrow mzPeak reader
- R/arrow mzPeak reader

## Outputs

- CSV export from Rust implementation (spectrum table)
- CSV export from Python/pyarrow implementation (spectrum table)
- CSV export from R/arrow implementation (spectrum table)
- Cross-implementation consistency report (field-level agreement documentation)

## How to apply

Load the same mzPeak input file using each of the three independent implementations (Rust library, Python/pyarrow implementation, and R/arrow implementation), exporting the resulting spectrum table to CSV format for each. Compare the three CSV outputs field-by-field, checking field names, data types, row counts, and numerical values for exact agreement. Generate a consistency report that documents field-level agreement, any divergences detected (including which implementation(s) differ), and overall validation status. Use this report to identify whether divergences stem from specification ambiguity, implementation bugs, or acceptable encoding differences (e.g., numerical precision in floating-point representation).

## Related tools

- **Rust mzPeak library** (Primary reader implementation for mzPeak format; includes read/write capabilities and serves as reference implementation) — https://github.com/HUPO-PSI/mzPeak
- **Python/pyarrow mzPeak reader** (Read-only independent implementation of mzPeak reader using PyData stack; enables cross-language validation) — https://github.com/HUPO-PSI/mzPeak
- **R/arrow mzPeak reader** (Read-only independent implementation of mzPeak reader using Arrow for R; enables cross-language validation) — https://github.com/HUPO-PSI/mzPeak
- **Apache Arrow** (Underlying columnar data format and runtime for both Python and R implementations) — https://arrow.apache.org/
- **OpenMS** (Proteomics toolkit referenced for context on mass spectrometry data handling) — https://www.openms.de/

## Evaluation signals

- Field names match exactly across all three CSV exports (no missing, renamed, or extra columns)
- Data types inferred from CSV exports are consistent (e.g., numeric vs. string vs. boolean for corresponding fields)
- Row counts are identical across all three exports (same number of spectra loaded)
- Numerical values agree field-by-field, accounting for acceptable floating-point precision differences (e.g., within machine epsilon for 32-bit or 64-bit floats)
- Consistency report explicitly documents which fields/rows/implementations agree or diverge, enabling root-cause analysis of any failures

## Limitations

- The skill validates agreement at the field level but does not validate correctness against external ground truth (e.g., whether a peak centroid value is physically accurate).
- Floating-point comparison requires careful tolerance handling; the skill may need to accommodate acceptable numerical divergence due to platform differences or compiler optimizations.
- Python and R implementations are read-only; they cannot be used to validate round-trip fidelity (write then read).
- The skill assumes all three implementations are available and operational; missing or broken implementations prevent validation.
- Format is in work-in-progress status with no stability guarantee; implementations may change, invalidating previous consistency reports.

## Evidence

- [other] Three independent mzPeak reader implementations exist: a Rust library, a Python implementation using pyarrow, and an R implementation using arrow, all capable of reading mzPeak files.: "Three independent mzPeak reader implementations exist: a Rust library, a Python implementation using pyarrow, and an R implementation using arrow, all capable of reading mzPeak files."
- [other] Load the test mzPeak file using the Rust library reader and export the resulting spectrum table to CSV format. Load the identical mzPeak file using the Python/pyarrow implementation and export the spectrum table to CSV format. Load the identical mzPeak file using the R/arrow implementation and export the spectrum table to CSV format. Compare the three CSV outputs field-by-field to identify any discrepancies in field names, data types, row counts, and numerical values.: "Load the test mzPeak file using the Rust library reader and export the resulting spectrum table to CSV format. Load the identical mzPeak file using the Python/pyarrow implementation and export the"
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak.: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the PyData stack.: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the"
- [readme] There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only at this time.: "There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only at this time."
- [other] Generate a consistency report documenting field-level agreement, any divergences detected, and validation status across all three implementations.: "Generate a consistency report documenting field-level agreement, any divergences detected, and validation status across all three implementations."
- [readme] NOTE: This is a **work in progress**, no stability is guaranteed at this point.: "NOTE: This is a **work in progress**, no stability is guaranteed at this point."
