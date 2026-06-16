# Evaluation Strategy

## Direct Checks

- verify that inputs include a two-condition ATAC-seq dataset from GEO/SRA with accession number and sample metadata
- verify file_exists for output differential TF occupancy results table (.tsv format)
- verify file_exists for output summary plot (.pdf or .png format)
- verify that .tsv output contains at least the following fields: TF name, condition 1 occupancy score, condition 2 occupancy score, differential occupancy metric, and statistical significance (p-value or adjusted p-value)
- verify row_count_equals for .tsv output is greater than 0 (at least one TF detected)
- verify that all numeric fields in .tsv (occupancy scores, p-values) are in valid ranges: occupancy scores between 0–1 or normalized scale, p-values between 0–1
- verify script_runs: TOBIAS pipeline commands execute without error on the input dataset (bias correction, footprint scoring, BINDetect modules complete successfully)
- verify that plot (.pdf/.png) displays at least one visualization comparing differential TF occupancy between the two conditions (e.g., scatter plot, bar chart, or heatmap), parameter-sensitive to visualization design choices and no canonical answer for plot layout

## Expert Review

- assess whether the selection of the two-condition ATAC-seq dataset and experimental design are appropriate for testing differential TF occupancy
- assess whether the TOBIAS pipeline parameters (bias correction thresholds, footprint scoring windows, BINDetect statistical model) are reasonable and justified for the chosen dataset
- assess whether the differential TF occupancy results are biologically plausible and consistent with known TF biology and the experimental conditions
- assess whether the summary plot effectively communicates the main findings and is suitable for publication or presentation
