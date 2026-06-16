# Evaluation Strategy

## Direct Checks

- verify file exists: parser implementation in messes repository (github:MoseleyBioinformaticsLab/messes)
- verify file_format_is: parser accepts tabular input with export tags matching pattern #<table_name>.id and #.<field_name>
- verify script_runs: parser execution on tagged tabular test file without errors
- verify output_matches_reference: generated JSON structure conforms to nested schema consumed by directive resolvers (byte-for-byte matching against reference conversion or schema validation)
- verify field_present: output JSON contains expected nested fields corresponding to input table and field tags
- verify format_is: output is valid JSON (parseable by standard JSON parser)

## Expert Review

- assess correctness of tag interpretation logic: does parser correctly map export tags (#<table_name>.id, #.<field_name>) to nested JSON hierarchy
- assess completeness of conversion: does generated JSON structure preserve all information from tagged input and match directives engine consumption expectations
- assess handling of edge cases: nested tables, missing tags, malformed tags, duplicate field names
