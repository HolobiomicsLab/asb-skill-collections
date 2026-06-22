---
name: data-serialization-format-interoperability
description: Use when you have a new or draft file format specification (e.g., mzPeak) with multiple independent language implementations, and you need to verify that all readers agree on the structured data they extract before recommending the format for production use.
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
  - arrow (R)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-serialization-format-interoperability

## Summary

Validate that independent implementations of a file format specification (Rust, Python/pyarrow, R/arrow) produce field-level agreement when reading identical input files, ensuring correctness and interoperability across language ecosystems. This skill is essential when adopting or validating a nascent data format across multiple analytical platforms.

## When to use

You have a new or draft file format specification (e.g., mzPeak) with multiple independent language implementations, and you need to verify that all readers agree on the structured data they extract before recommending the format for production use. This is most critical when the format is work-in-progress or when stakeholders plan to use it across heterogeneous computational stacks (e.g., Rust pipelines alongside R or Python).

## When NOT to use

- The file format specification is already stable and widely adopted with years of field validation; interoperability testing is redundant.
- You have only one implementation available; field-level cross-implementation comparison is not possible.
- The input files are not canonical test specimens but real user data with known quality issues; use curated reference files instead.

## Inputs

- mzPeak file (test specimen)
- Rust mzPeak reader implementation
- Python/pyarrow mzPeak reader implementation
- R/arrow mzPeak reader implementation

## Outputs

- CSV export from Rust reader (spectrum table)
- CSV export from Python/pyarrow reader (spectrum table)
- CSV export from R/arrow reader (spectrum table)
- Field-level consistency report (agreement/divergence summary)

## How to apply

Load the same test mzPeak file using each implementation (Rust library reader, Python/pyarrow, R/arrow), exporting the resulting spectrum table to a common serialization format (CSV or TSV). Compare the three outputs field-by-field: verify field names match exactly, confirm data types are consistent, check that row counts are identical, and inspect numerical values for exact agreement or acceptable floating-point tolerance. Generate a consistency report documenting field-level agreement status, any detected divergences (field naming, type mismatches, missing rows, numerical drift), and an overall validation status. Use this report to identify which implementation(s) deviate from the specification or each other, and trace the cause (spec ambiguity, implementation bug, or format version mismatch).

## Related tools

- **Rust mzPeak library** (Read and export mzPeak files to CSV; provides reference implementation with read/write support) — https://github.com/HUPO-PSI/mzPeak
- **pyarrow** (Enable Python implementation to read mzPeak files (Parquet-based format)) — https://arrow.apache.org/docs/python/index.html
- **arrow (R)** (Enable R implementation to read mzPeak files) — https://arrow.apache.org/docs/r/
- **OpenMS** (Reference mass spectrometry data processing framework; format stewardship)

## Examples

```
# Load mzPeak with Rust and export to CSV
cargo run --release --bin mzpeak -- read test.mzpeak --format csv > rust_output.csv
# Load with Python/pyarrow
python -c "import pyarrow.parquet as pq; df = pq.read_table('test.mzpeak/spectra_metadata.parquet').to_pandas(); df.to_csv('python_output.csv', index=False)"
# Load with R/arrow
Rscript -e "library(arrow); df <- read_parquet('test.mzpeak/spectra_metadata.parquet'); write.csv(df, 'r_output.csv', row.names=FALSE)"
# Compare outputs
diff -u <(sort rust_output.csv) <(sort python_output.csv) <(sort r_output.csv)
```

## Evaluation signals

- All three CSV exports have identical field names (no name mismatches or missing columns across implementations)
- Row counts are identical across all three exports; no spectrum records are dropped or duplicated by any reader
- Numerical values in data fields agree exactly or within a pre-specified floating-point tolerance (e.g., ≤ 1e-6 relative error for m/z and intensity) across all three implementations
- Data types (integer, float, string, etc.) are consistent across all three outputs for each field
- The consistency report flags zero divergences, or clearly documents which divergences are acceptable (e.g., known spec ambiguities) and which are implementation bugs

## Limitations

- This skill validates only read operations; Python and R implementations currently support read-only access, so write-path interoperability cannot be tested with those tools.
- The mzPeak format is documented as work-in-progress with no stability guarantee, so field-level agreement may evolve as the specification matures; test results are valid only for the specification version tested.
- Test coverage depends on the comprehensiveness of the test mzPeak file; edge cases (null m/z values, zero run stripping, chunked vs. point layout data arrays) may not be detected if absent from the specimen.
- Floating-point numerical comparisons require careful handling of representation; byte-level identity is not expected across platforms or implementations, but semantic agreement (e.g., within mass accuracy tolerance) must be verified.

## Evidence

- [other] research_question_cross_impl: "Do the Rust, Python/pyarrow, and R/arrow implementations of mzPeak file readers produce field-level agreement when loading the same input file?"
- [other] workflow_three_exports: "Load the test mzPeak file using the Rust library reader and export the resulting spectrum table to CSV format. 2. Load the identical mzPeak file using the Python/pyarrow implementation and export the"
- [other] workflow_field_comparison: "Compare the three CSV outputs field-by-field to identify any discrepancies in field names, data types, row counts, and numerical values."
- [other] workflow_report_gen: "Generate a consistency report documenting field-level agreement, any divergences detected, and validation status across all three implementations."
- [readme] python_read_only: "The Python codebase does not support writing at this time although this is subject to change in the future"
- [readme] r_read_only: "which is also a complete re-implementation using the [`arrow`] for _reading_ only at this time"
- [readme] work_in_progress_status: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
- [readme] parquet_based_format: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP]"
