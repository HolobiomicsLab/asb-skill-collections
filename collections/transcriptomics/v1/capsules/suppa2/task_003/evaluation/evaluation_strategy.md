# Evaluation Strategy

## Direct Checks

- verify that github:comprna__SUPPA repository is accessible and contains a diffSplice subcommand implementation
- verify file_format_is: input PSI matrix files are tab-separated or comma-separated text files with events as rows and conditions as columns
- verify file_format_is: input transcript expression files follow expected format (e.g., tab-separated with transcript identifiers and expression values)
- verify file_exists: output differential splicing results table is produced with .txt or .tsv extension
- verify field_present: output table contains at least 'dpsi' column (delta PSI values)
- verify field_present: output table contains at least 'p-value' or 'pvalue' column
- verify row_count_equals: output table contains one row per input splicing event (exact match to input event count)
- verify script_runs: diffSplice subcommand executes without fatal errors on minimal test input (PSI matrix + expression files)

## Expert Review

- statistical validity: assess whether the differential splicing statistical test (method for computing dpsi and p-value) is appropriate for paired/unpaired conditions and handles missing/zero values correctly
- biological plausibility: review whether computed dpsi values and p-values align with expected effect sizes and significance thresholds for known alternative splicing events
- uncertainty quantification: if SUPPA2 claims uncertainty-aware analysis, verify that confidence intervals or error estimates are present in output or documented in method
