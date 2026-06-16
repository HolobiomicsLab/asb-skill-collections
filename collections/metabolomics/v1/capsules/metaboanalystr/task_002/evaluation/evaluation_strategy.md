# Evaluation Strategy

## Direct Checks

- verify that MetaboAnalystR package can be loaded and executed against a public LC-MS dataset (e.g., from MetaboLights or MassIVE accession)
- file_exists: check that the output feature table artifact is generated (expected format: CSV, TSV, or R data frame)
- row_count_equals or row_count_in_range: verify the feature table contains at least one feature (row > 0) and at least one sample (column > 0)
- field_present: confirm the output table contains columns for feature identifiers, sample identifiers, and intensity or abundance values
- value_in_range: check that peak intensity summary statistics (mean, median, min, max, standard deviation) are non-negative and finite
- script_runs: verify that the end-to-end LC-MS workflow script executes without fatal errors on the selected public dataset

## Expert Review

- assess whether the feature table dimensions and intensity distributions are reasonable for the chosen LC-MS dataset (e.g., consistent with dataset documentation or comparable published analyses)
- evaluate whether peak intensity summary statistics and feature recovery align with expected metabolomic signal characteristics (no anomalously sparse or saturated distributions)
