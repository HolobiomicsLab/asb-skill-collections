# Evaluation Strategy

## Direct Checks

- verify that github:rjdossan/M2S repository is accessible and contains Matlab source code files
- verify that M2S package includes a main entry point or documented pipeline script for feature matching
- script_runs: execute M2S pipeline on two synthetic or provided LC-MS feature datasets (CSV or compatible format) without errors
- verify that pipeline execution produces a named output file (e.g., matched_features table, alignment results, or correspondence matrix)
- file_format_is: output file is tabular (CSV, Excel, or Matlab table) with at least three columns: feature_1_ID, feature_2_ID, and match_score or similarity metric
- row_count_equals: output table contains at least one matched feature pair (row_count ≥ 1), robust to dataset size
- verify output structure contains identifiable references to input features from both datasets

## Expert Review

- Assess whether matching algorithm (mass tolerance, retention time window, scoring method) is appropriate for untargeted LC-MS metabolomics and documented in code comments or README
- Evaluate whether matched feature pairs are chemically plausible given m/z and retention time deltas reported in output
- Review whether pipeline handles edge cases (missing RT values, duplicate features, m/z calibration drift) gracefully
