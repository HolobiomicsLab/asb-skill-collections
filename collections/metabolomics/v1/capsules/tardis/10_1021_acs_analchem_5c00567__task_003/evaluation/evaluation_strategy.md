# Evaluation Strategy

## Direct Checks

- verify file_exists: output directory contains per-metric CSV files named 'AUC.csv', 'Max Intensity.csv', 'SNR.csv', 'peak_cor.csv', and 'pop.csv' (or 'points over the peak.csv')
- verify file_format_is: each per-metric CSV file is valid comma-separated format with row_count_equals at least 1 data row plus header
- verify output_matches_reference: QC feature table tibble structure contains columns for target identifiers and average metric values across QC runs
- verify script_runs: tardisPeaks() function executes without error when called with screening_mode=FALSE on vignette dataset after RT adjustment for targets 1577 and 1583
- verify field_present: output tibble contains expected columns corresponding to metrics (AUC, Max Intensity, SNR, peak_cor, pop)
- verify row_count_equals: number of rows in output tibble matches number of unique targets in vignette target list

## Expert Review

- Verify that QC feature table tibble values (average metrics per target) are scientifically plausible given typical LC–MS metabolomics data ranges and peak quality thresholds
- Assess whether per-metric CSV files contain sufficient detail and consistency to support targeted metabolomics quality assessment workflows
- Review RT adjustment procedure applied to targets 1577 and 1583 for correctness relative to xcms retention time correction methodology
