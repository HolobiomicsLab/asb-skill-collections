# Evaluation Strategy

## Direct Checks

- verify file 'preferred_Feature_table.tsv' exists in pipeline output directory
- verify file 'full_Feature_table.tsv' exists in pipeline output directory
- verify file '_mass_grid_mapping.csv' exists in pipeline output directory
- verify file 'cmap.pickle' exists in pipeline output directory
- verify file 'Annotated_empiricalCompounds.json' exists in pipeline output directory
- file_format_is 'preferred_Feature_table.tsv' TSV with tab-delimited rows
- file_format_is 'full_Feature_table.tsv' TSV with tab-delimited rows
- file_format_is '_mass_grid_mapping.csv' CSV with comma-delimited rows
- file_format_is 'cmap.pickle' binary pickle format (bytes match pickle magic number)
- file_format_is 'Annotated_empiricalCompounds.json' valid JSON (parseable by standard JSON parser)
- row_count_equals 'preferred_Feature_table.tsv' at least 1 (header row present)
- row_count_equals 'full_Feature_table.tsv' at least 1 (header row present)
- row_count_equals '_mass_grid_mapping.csv' at least 1 (header row present)
- script_runs: asari pipeline execution completes without fatal errors on centroided mzML input, robust to minor version variations in dependencies

## Expert Review

- Verify that feature identifiers in preferred_Feature_table.tsv correspond to valid mass tracks in _mass_grid_mapping.csv
- Verify that Annotated_empiricalCompounds.json contains plausible compound annotations with mass-to-charge ratios consistent with input data m/z range
- Verify that cmap.pickle deserializes to a valid mass grid object with expected internal structure (dictionary or object with mass alignment metadata)
- Verify that full_Feature_table.tsv contains superset of features in preferred_Feature_table.tsv with expected quality/filtering differences
