# Evaluation Strategy

## Direct Checks

- verify that the cluster assignment file exists and is readable
- verify file_format_is cluster assignment output (e.g. TSV, CSV, or JSON with spectrum identifiers and cluster labels)
- verify field_present: cluster assignment file contains at least two columns/fields: spectrum identifier and cluster label
- verify row_count_equals: cluster assignment file contains one row per input spectrum (row count matches input spectrum count)
- verify contains_substring: cluster assignment file contains valid cluster identifiers (numeric or alphanumeric labels, no nulls or 'None' values for assigned spectra)
- verify script_runs: density-based clustering implementation (DBSCAN or equivalent) executes without errors on sparse distance matrix input
- verify output_matches_reference: cluster assignments are reproducible (byte-for-byte or robust to parameter choices, depending on implementation determinism)

## Expert Review

- assess whether cluster assignments are biologically/chemically meaningful by comparing against known spectrum families or reference spectral libraries, if available
- assess whether the density threshold parameters (e.g. eps, min_samples for DBSCAN) are appropriately justified and documented
- assess whether cluster quality metrics (silhouette score, Davies-Bouldin index, or domain-specific measures) meet expected thresholds for mass spectrometry data
