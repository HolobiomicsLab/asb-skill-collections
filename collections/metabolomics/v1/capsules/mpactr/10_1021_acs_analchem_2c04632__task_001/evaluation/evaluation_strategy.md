# Evaluation Strategy

## Direct Checks

- verify file exists in mums2/mpactr repository: vignette or documentation describing filter_summary() applied to 'mispicked' filter output structure
- script_runs: R code loading mpactr library, importing cultures_peak_table.csv and cultures_metadata.csv via example_path(), applying filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum"), then calling filter_summary() on the result
- output_matches_reference: verify returned object contains exactly two named lists with keys 'passed_ions' and 'failed_ions' (or equivalent), robust to column ordering within each list
- file_format_is: both passed_ions and failed_ions outputs are data tables (data.frame or data.table class)
- row_count_equals: verify row counts in passed_ions and failed_ions tables are non-negative integers and sum to total number of ions in input peak table

## Expert Review

- verify structure and field names of passed_ions and failed_ions tables match the vignette specification for the 'mispicked' filter (requires domain knowledge of expected ion metadata fields)
- assess whether filter_summary() output correctly identifies ions that failed vs. passed the mispicked-ion detection logic as documented in the vignette
