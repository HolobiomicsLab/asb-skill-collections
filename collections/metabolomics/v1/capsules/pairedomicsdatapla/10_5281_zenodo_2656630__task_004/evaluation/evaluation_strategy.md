# Evaluation Strategy

## Direct Checks

- verify file exists: project JSON document input
- verify file_format_is: input is valid JSON
- script_runs: validation script executes without error on test inputs
- output_matches_reference: validation script identifies all URL fields containing whitespace in a test JSON document with known whitespace-containing URLs, no false negatives
- output_matches_reference: validation script produces no false positives on a test JSON document with valid URLs (no whitespace)
- contains_substring: validation output includes flagged URL field name(s) and the problematic value(s) containing spaces

## Expert Review

- Confirm URL field schema is correctly identified in the project JSON structure
- Confirm whitespace character definition (space, tab, newline, etc.) aligns with platform requirements
- Confirm error/warning message is actionable for end users submitting project data
