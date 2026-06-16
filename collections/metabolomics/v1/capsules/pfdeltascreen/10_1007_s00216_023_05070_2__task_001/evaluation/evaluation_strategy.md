# Evaluation Strategy

## Direct Checks

- verify file exists at github:JonZwe__PFAScreen (PFAScreen repository)
- verify script_runs: execute pyOpenMS feature detection module on a centroided mzML input file without errors
- verify output_matches_reference: feature list output contains required columns (m/z, retention time, intensity)
- verify file_format_is: output feature list is in a structured format (CSV, featureXML, or pandas DataFrame serialization)
- verify row_count_equals: feature list contains at least one detected feature (row_count > 0) for non-empty input mzML
- verify value_in_range: detected m/z values fall within physically plausible range (50–2000 m/z, parameter-sensitive to instrument and sample)
- verify value_in_range: retention time values are non-negative and monotonically increasing or clustered (parameter-sensitive to LC gradient)
- verify value_in_range: intensity values are positive numbers (>0)

## Expert Review

- assess whether pyOpenMS centroid detection parameters (peak picking, feature linking thresholds) are appropriate for the analyte class and instrument resolution reported in the article
- assess whether detected feature m/z accuracy and retention time precision meet expected HRMS performance for PFAS screening
- assess whether feature list completeness (number and identity of true features) is reasonable by comparison to literature or reference standards for similar LC-HRMS PFAS methods
