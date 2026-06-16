# Evaluation Strategy

## Direct Checks

- verify file exists in github:mobiusklein__mzpeak_prototyping repository: a sample mzPeak file suitable for cross-reader testing
- script_runs: Rust reader executable successfully loads the sample mzPeak file and outputs a structured record (JSON, Arrow IPC, or Parquet)
- script_runs: Python/pyarrow reader successfully loads the same sample mzPeak file and outputs a tabular structure (DataFrame or Arrow Table)
- script_runs: R/arrow reader successfully loads the same sample mzPeak file and outputs a tabular structure (data.frame or Arrow Table)
- field_present: all three output tables contain identical column names (robust to row ordering)
- row_count_equals: Rust, Python, and R readers produce tables with matching row counts for the same input file
- output_matches_reference: spectrum record fields (m/z values, intensities, retention time, scan metadata) are byte-for-byte identical across all three readers, or expert review documents acceptable tolerance and root causes for any divergence

## Expert Review

- Evaluate whether small numerical differences (floating-point precision) in m/z or intensity fields across the three readers are acceptable given IEEE 754 standards and the format specification
- Assess whether any missing or extra fields in one reader relative to the others represent implementation bugs, format ambiguities, or intentional design choices
- Determine whether differences in metadata field ordering, naming conventions, or data-type encoding (e.g., integer vs. float for scan number) indicate true interoperability issues or benign representation choices
