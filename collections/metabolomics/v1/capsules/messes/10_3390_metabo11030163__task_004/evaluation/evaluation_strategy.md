# Evaluation Strategy

## Direct Checks

- verify that the input IC-FTMS measurement example dataset is present in the documentation (file_exists or contains_substring check)
- verify that the expected output JSON for collate='assignment' is explicitly shown in the Collate section of the documentation (contains_substring check)
- script_runs: execute the matrix directive with collate='assignment' on the documented example input without errors
- output_matches_reference: the resulting list of dictionaries byte-for-byte matches the expected output JSON cited in the Collate section
- verify that output is valid JSON (format_is check)

## Expert Review

- assess whether the semantic meaning of the assignment collation is correctly implemented (e.g., correct grouping/assignment logic applied to the example data)
- confirm that the output structure and field assignments match the intent of the collate='assignment' directive as documented
