# Evaluation Strategy

## Direct Checks

- verify file standard_data.csv exists in github:castratton__uafR repository
- verify standard_data.csv contains column 'Match.Factor'
- verify standard_data.csv contains column 'Compound.Name'
- verify row_count_equals for compounds with Match.Factor >= 65 against COND-mf65 output
- verify row_count_equals for compounds with Match.Factor >= 80 against COND-mf80 output
- verify row_count_equals for compounds with Match.Factor >= 90 against COND-mf90 output
- verify output table contains exactly three rows (one per threshold: 65, 80, 90)
- verify output table contains columns for threshold value and retained compound count
- verify retained_count(>=90) <= retained_count(>=80) <= retained_count(>=65) (monotonic decrease with stricter threshold)
- script_runs: R script applying Match.Factor filters to standard_data.csv and producing comparison table executes without error

## Expert Review

- assess whether the Match.Factor thresholds (65, 80, 90) are scientifically appropriate and well-justified for mass spectrometry compound identification quality control
- evaluate whether the comparison table format and labeling are clear and suitable for presenting filtering results
