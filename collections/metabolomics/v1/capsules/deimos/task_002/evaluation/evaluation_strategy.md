# Evaluation Strategy

## Direct Checks

- verify file example_alignment.h5 exists in repository or deposited dataset
- verify deimos.alignment function is callable from deimos package after installation
- verify output aligned table file_format_is HDF5 or pandas DataFrame serializable format
- verify aligned output contains expected columns matching input feature tables (robust to column order)
- script_runs: Python script loading example_alignment.h5, calling deimos.alignment with reference-based method, and writing aligned output without errors
- verify output row_count_equals or approximately matches expected feature count (parameter-sensitive to alignment tolerance parameters)
- verify aligned features contain at least the common dimensions (m/z, drift_time, retention_time) from input tables

## Expert Review

- assess whether reference-based alignment correctly matched homologous features across the two input feature tables
- evaluate alignment quality by examining mass accuracy and dimensional correspondence of matched features
- verify that alignment method choice (reference-based vs. other approaches) was appropriate for the example datasets
- assess whether the aligned output preserves intensity and other quantitative metadata without loss or corruption
