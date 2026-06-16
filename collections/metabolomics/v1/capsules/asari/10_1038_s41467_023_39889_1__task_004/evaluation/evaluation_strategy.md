# Evaluation Strategy

## Direct Checks

- verify that the asari package repository (github:shuzhao-li-lab/asari) contains peak quality filter implementation with METRIC_SNR, METRIC_PEAKSHAPE, and PARAM_MIN_PEAK_HEIGHT parameters in the peaks module or configuration
- file_exists: full_Feature_table.tsv in test dataset or example output directory
- file_exists: filtered feature table output after applying peak quality thresholds
- row_count_equals: filtered feature table row count is less than or equal to full_Feature_table.tsv row count
- verify that filtered feature table row count demonstrates appropriate reduction relative to unfiltered table (multiple defensible approaches for 'appropriate'—threshold-dependent)
- script_runs: asari peak quality filter function accepts METRIC_SNR (>2), METRIC_PEAKSHAPE goodness_fitting, and PARAM_MIN_PEAK_HEIGHT (default 1e5 with >20% prominence) as parameters without error
- output_matches_reference: filtered feature table structure preserves expected columns from unfiltered full_Feature_table.tsv

## Expert Review

- verify that METRIC_SNR threshold of >2 is scientifically defensible for metabolomics LC-MS peak quality
- verify that METRIC_PEAKSHAPE goodness_fitting metric is an appropriate measure of Gaussian fit quality for chromatographic peaks
- verify that PARAM_MIN_PEAK_HEIGHT default of 1e5 with >20% prominence threshold is reasonable for the instrument sensitivity and sample complexity assumed in test/example datasets
- assess whether row count reduction magnitude is consistent with expected filtering stringency for the thresholds applied
