# Evaluation Strategy

## Direct Checks

- verify file_exists for input feature table artifact (CSV, TSV, or JSON format)
- verify file_format_is correct for output imputed table (same format as input)
- verify row_count_equals: output table has same number of features as input table
- verify field_present: output table contains all original feature columns
- script_runs: ARCH-IMPUTE impute command executes without error on input table with specified interpolation_ratio parameter
- output_matches_reference: for each feature in output table, verify that all zero/missing values are replaced with (interpolation_ratio × minimum non-zero observed value for that feature) — requires sampling verification on representative features (no canonical answer for which features to spot-check; multiple defensible random sampling strategies acceptable)
- value_in_range: all imputed values in output table are greater than zero and less than or equal to (interpolation_ratio × maximum observed value per feature)
- verify contains_substring: output artifact filename or metadata indicates imputation was applied with the specified interpolation_ratio value

## Expert Review

- evaluate whether interpolation_ratio parameter value is scientifically reasonable for metabolomics missing-value imputation (typical metabolomics practice uses ratios between 0.1 and 0.5 of minimum non-zero values)
- assess whether replacement strategy (ratio × minimum non-zero) is appropriate for the metabolomics context and preserves statistical properties needed for downstream analysis
- confirm that imputation method does not introduce artificial patterns or bias in feature abundance distributions
