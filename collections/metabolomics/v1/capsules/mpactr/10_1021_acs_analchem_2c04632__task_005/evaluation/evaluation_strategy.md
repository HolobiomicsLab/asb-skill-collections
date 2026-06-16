# Evaluation Strategy

## Direct Checks

- file_exists: cultures_peak_table.csv in the mpactr package or accessible via example_path()
- file_exists: cultures_metadata.csv in the mpactr package or accessible via example_path()
- script_runs: R script that loads mpactr library, imports cultures dataset via import_data(example_path("cultures_peak_table.csv")), and executes filter_mispicked_ions() twice with copy_object=FALSE and copy_object=TRUE respectively
- output_matches_reference: comparison table contains exactly 2 rows (one per condition: copy_object=FALSE, copy_object=TRUE)
- output_matches_reference: comparison table contains columns for condition, original_object_row_count, result_object_row_count, and object_identity_match (boolean)
- value_in_range: row counts are positive integers matching the dimensions of the cultures dataset after filtering
- format_is: output is a structured table (data.frame, tibble, or CSV) with named columns and consistent data types

## Expert Review

- verify that the observed divergence in row counts between copy_object=FALSE and copy_object=TRUE conditions aligns with documented R6 reference semantics behavior (in-place modification vs. shallow copy behavior)
- confirm that object identity (via identical() or address comparison) shows expected pattern: copy_object=FALSE should modify original in-place; copy_object=TRUE should preserve original while modifying assigned result
