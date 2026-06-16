# Evaluation Strategy

## Direct Checks

- verify file_exists: output directory contains 'Plots' subdirectory
- verify file_exists: output directory contains 'Reports' subdirectory
- verify file_format_is: all files in Plots subdirectory are image files (PNG, PDF, or similar graphics format)
- verify file_format_is: all files in Reports subdirectory are tab-delimited text files (.txt or .tsv)
- verify script_runs: createReports() function executes without error when called with parameters makeSummaryReport=TRUE, makeCompoundReport=TRUE, backgroundPercent=40, cautionRSD=15, nonReportableRSD=30, assays='area'
- verify row_count_equals: summary report and compound report files are non-empty (contain at least header row plus one data row)

## Expert Review

- Verify that generated plots are visually coherent and match documented mzQuality output styles for quality control visualization
- Verify that report content appropriately reflects the specified RSD thresholds (cautionRSD=15, nonReportableRSD=30) in flagging or categorizing compounds
