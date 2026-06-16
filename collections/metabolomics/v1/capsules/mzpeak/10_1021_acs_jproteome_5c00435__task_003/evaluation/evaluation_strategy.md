# Evaluation Strategy

## Direct Checks

- verify file exists at github:mobiusklein__mzpeak_prototyping/R/ subdirectory
- verify arrow R package is installed and loadable
- verify a valid mzPeak file artifact is available as input (file_exists and file_format_is mzPeak)
- script_runs: R read operation completes without error
- output_matches_reference: returned tabular artifact contains at least one named column representing spectrum data (field_present)
- verify output is a structured table format (data.frame or arrow Table equivalent)
- row_count_equals or value_in_range: tabular output contains ≥1 row of spectrum records

## Expert Review

- verify that the tabular representation correctly preserves all essential spectrum metadata (m/z, intensity, retention time if applicable)
- confirm that the arrow R implementation faithfully deserializes mzPeak binary structure without data loss or corruption
- assess whether the column naming and data types are semantically consistent with mzPeak specification
