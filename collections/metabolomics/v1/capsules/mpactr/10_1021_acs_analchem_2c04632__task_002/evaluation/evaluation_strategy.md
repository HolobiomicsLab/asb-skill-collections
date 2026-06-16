# Evaluation Strategy

## Direct Checks

- verify file exists: cultures_peak_table.csv (from mpactr package example_path)
- verify file exists: cultures_metadata.csv (from mpactr package example_path)
- script_runs: R script that loads mpactr library, imports cultures datasets via import_data(), applies filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum"), filter_group(group_to_remove = "Solvent_Blank"), and filter_cv(cv_threshold = 0.2) sequentially, then calls qc_summary() on the resulting object
- output_matches_reference: returned data.table has field names matching vignette description (exact field names require expert review of vignette)
- value_in_range: row count of qc_summary() output data.table is positive and less than or equal to number of unique compounds in filtered input

## Expert Review

- verify that qc_summary() output data.table field structure and semantics (compound ID column, pass/fail status columns per filter) align with published vignette documentation
- confirm that pass/fail status values are consistent with the three filter criteria (mispicked, group, CV threshold 0.2) applied in sequence
- validate that the row count reflects correct filtering logic: compounds should only appear if they survive all three filters or are properly marked as failed at each stage
