# Evaluation Strategy

## Direct Checks

- verify that the implementation accepts a conversion directives file (JSON or tagged-tabular format) as input
- verify that the implementation reads and parses the str-type directive record without errors
- verify that the implementation resolves str-type record fields against an input JSON object
- verify that override sub-field, when present, takes precedence over code sub-field in str directive resolution
- verify that code sub-field is executed (if override is absent) and produces a scalar or string output
- verify that record_id sub-field, when present, filters or identifies the target record correctly
- verify that for_each sub-field, when present, iterates over an array or collection in the input JSON
- verify that test sub-field, when present, evaluates to a boolean and gates application of the directive
- verify that sort_by and sort_order sub-fields, when both present, sort output results accordingly (robust to parameter choices for sort key selection)
- verify that delimiter sub-field, when present, joins or splits string output using the specified delimiter
- verify that fields sub-field, when present, selects or maps only specified field names in the output record
- verify that the implementation produces a named output artifact (file, record, or structured result) matching the expected_outputs specification

## Expert Review

- verify that the precedence and interaction logic among override, code, record_id, for_each, and test sub-fields aligns with the intended semantics of the Conversion Directives Engine
- verify that edge cases (missing sub-fields, empty arrays, null values, type mismatches) are handled gracefully and produce defensible outputs
- verify that the str handler correctly integrates with other value_type handlers within the broader Conversion Directives Engine
