# Evaluation Strategy

## Direct Checks

- verify file exists: input multi-batch interpolated feature table (e.g., CSV, TSV, or HDF5 format)
- verify file_format_is: input feature table conforms to expected shape (rows=samples, columns=features)
- script_runs: pycombat batch_correct function executes without errors on input table using by_batch parameter
- verify file_exists: output corrected feature table (same format as input)
- row_count_equals: corrected table row count matches input table row count (samples preserved)
- row_count_equals: corrected table column count matches input table column count (features preserved)
- verify output_matches_reference: inter-batch variance (e.g., sum-of-squares or Silhouette distance) for selected features is lower in corrected table than uncorrected table; solution_space: multiple defensible variance metrics (PCA-based, PERMANOVA, homogeneity index) are valid
- value_in_range: variance reduction magnitude is quantitatively reported as a numeric score or percentage; parameter-sensitive: depends on feature and batch selection

## Expert Review

- inspect corrected feature table for biological plausibility: verify that batch correction does not artificially inflate or eliminate true biological signal (e.g., case-control or treatment effects should remain detectable post-correction)
- assess choice of selected features for variance reduction analysis: confirm that features are representative (e.g., not cherry-picked) and that the selection strategy is justified
- evaluate appropriateness of inter-batch variance metric: confirm that the chosen metric (e.g., between-batch dispersion, homogeneity index) is statistically sound for the experimental design
