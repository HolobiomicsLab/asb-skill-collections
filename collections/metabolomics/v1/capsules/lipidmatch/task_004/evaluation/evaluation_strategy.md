# Evaluation Strategy

## Direct Checks

- verify file exists: LipidMatch repository cloned from github:GarrettLab-UF__LipidMatch contains executable scripts for library integration
- verify file_format_is: user-authored .csv lipid library conforms to format specification documented in LipidMatch manual (exact column names and order required)
- verify script_runs: library integration script executes without errors when passed valid .csv file as input
- verify file_exists: integrated library file is generated in expected output location after script execution
- verify contains_substring: output matching run results file contains at least one custom lipid entry from the integrated .csv library among candidate matches (requires exact lipid identifier match)

## Expert Review

- Confirm that the custom lipid entries correctly appear as valid candidates in the matching output (chemical accuracy of integration and ranking)
- Validate that library integration did not corrupt or duplicate entries from the original in-silico library
