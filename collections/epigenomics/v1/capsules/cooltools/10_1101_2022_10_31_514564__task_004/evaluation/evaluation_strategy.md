# Evaluation Strategy

## Direct Checks

- verify file_exists: input cooler file (deposited dataset or public accession with cis contact table) can be loaded
- verify script_runs: logbin_expected function executes without error on a precomputed expected_cis table
- verify file_format_is: output file is TSV (tab-separated values) with .tsv extension
- verify field_present: output TSV contains at least two columns (e.g., separation distance and smoothed P(s) value)
- verify row_count_equals: output TSV has at least one data row (no canonical answer on exact row count due to log-binning parameter sensitivity)
- verify contains_substring: output TSV header or metadata indicates data is log-binned (robust to various column naming conventions)
- verify output_matches_reference: if cooltools repository contains a worked example or integration test for logbin_expected, output structure and numeric precision match the reference output (byte-for-byte match not required; robust to floating-point representation)

## Expert Review

- Verify that the smoothed P(s) curve values are mathematically plausible for cis contact decay (monotonic decrease or expected decay pattern consistent with Hi-C biology)
- Assess whether log-binning spacing and smoothing parameters (if exposed in function signature) are appropriate for genomic distance scales
- Evaluate whether the API documentation or function signature in the cooltools repository clarifies which parameters are unstable and may change in future releases
