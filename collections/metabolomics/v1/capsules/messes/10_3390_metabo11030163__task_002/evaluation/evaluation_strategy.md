# Evaluation Strategy

## Direct Checks

- verify file exists in repository MoseleyBioinformaticsLab/messes containing matrix directive handler implementation
- verify script_runs: execute matrix directive handler on a test JSON input with headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code sub-fields defined
- verify output_matches_reference: output is a list of dictionaries (Python list[dict] type or JSON array of objects)
- verify field_present: each output dictionary contains keys derived from fields_to_headers mapping
- verify contains_substring: implementation handles exclusion_headers parameter to filter specified fields from output
- verify contains_substring: implementation handles sort_by and sort_order parameters to reorder output list (multiple defensible sort strategies acceptable)
- verify contains_substring: implementation handles values_to_str parameter to convert non-string values to strings where specified
- verify contains_substring: implementation handles collate parameter to combine or merge field values according to directive specification
- verify contains_substring: implementation evaluates test sub-field condition (if present) against input record before including in output (no canonical answer — test expression language must match library's evaluation framework)
- verify contains_substring: implementation executes code sub-field (if present) to transform or compute values before population in output dictionary (no canonical answer — code execution context varies by library design)

## Expert Review

- assess correctness of matrix-to-dictionary transformation logic: verify that the mapping from input JSON record fields to output dictionary headers follows the fields_to_headers directive specification faithfully
- assess soundness of collate strategy: verify that field merging or combination respects data semantics and does not produce information loss or corruption
- assess robustness of conditional filtering: verify that test sub-field expressions correctly identify which input records should be included/excluded in output
- assess code execution safety and correctness: review embedded code sub-field execution for correctness, side effects, and alignment with documented behavior
