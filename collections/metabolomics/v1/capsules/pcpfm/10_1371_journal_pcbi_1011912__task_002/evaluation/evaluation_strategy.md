# Evaluation Strategy

## Direct Checks

- verify that the blank_masking command is documented in the repository (github:shuzhao-li-lab__PythonCentricPipelineForMetabolomics) with parameter blank_intensity_ratio
- verify file_exists for a sample feature table artifact suitable as input to blank_masking
- script_runs: execute blank_masking on the sample feature table with a specified blank_intensity_ratio value
- verify output_matches_reference: the filtered feature table contains only features whose max intensity in unknown samples exceeds (blank_intensity_ratio × max intensity in blank samples)
- verify row_count_equals: count of features in output is less than or equal to count in input (no features added by filtering)
- verify field_present in output feature table: intensity columns for both blank and unknown sample groups are preserved

## Expert Review

- assess whether the blank_intensity_ratio threshold choice is defensible for the metabolomics study design and blank sample composition
- verify that the filtering logic correctly interprets 'features whose intensity in unknown samples does not exceed the ratio threshold relative to blank samples' (i.e., removal criterion is intensity_unknown ≤ blank_intensity_ratio × intensity_blank)
