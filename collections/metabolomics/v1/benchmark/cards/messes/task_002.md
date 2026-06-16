# SciTask Card: Reconstruct the matrix Directive resolution engine including collate and fields_to_headers behaviour

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T14:01:04.089933+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_messes/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- DOI: `10.3390/metabo11030163`
- GitHub: `MoseleyBioinformaticsLab/MESSES`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Techniques: `quality-control`, `database-annotation`

## Research Question
How does the matrix directive handler resolve a matrix-type record from conversion directives against input JSON to produce a list of dictionaries, including support for headers, collation, field exclusion, sorting, filtering, and custom code?

## Connected Finding
The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields; collate records by a grouping field; map record fields to dictionary keys via headers; exclude fields with exclusion_headers; convert values to strings with values_to_str; or execute custom Python code for complex transformations.

## Task Description
Implement a matrix directive handler that resolves matrix-type records from a conversion directives file against input JSON data, producing a list of dictionaries with support for headers, collation, field mapping, exclusion, value stringification, sorting, filtering, and custom code execution.

## Inputs
- Conversion directives file specifying matrix-type record transformation rules
- Input JSON data containing records to be transformed

## Expected Outputs
- List of dictionaries representing resolved matrix-type records with mapped headers and applied transformations

## Expected Output File

- `matrix_records.json`

## Landmark Outputs

- `parsed_directives.json`
- `filtered_records.json`
- `collated_records.json`
- `sorted_records.json`

## Tools
- Python
- jsonschema

## Skills
- json-schema-validation-and-mapping
- conversion-directive-parsing
- record-field-transformation-and-collation
- custom-code-execution-in-data-pipeline
- multi-key-sorting-and-filtering

## Workflow Description
1. Parse the conversion directives file to extract the matrix-type directive configuration, including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code sub-fields. 2. Load the input JSON data and locate the source records to be transformed. 3. Apply field-to-header mapping using the fields_to_headers configuration to construct output dictionary keys from specified input fields. 4. Filter records according to the test condition (if provided) and exclusion_headers criteria to retain only qualifying records. 5. Collate grouped records using the collate directive, aggregating multiple source records into single output dictionaries where applicable. 6. Convert specified fields to string representation using values_to_str to standardize output data types. 7. Sort the resulting list of dictionaries according to sort_by field(s) in sort_order (ascending or descending). 8. Execute any custom transformation code provided in the code sub-field to apply user-defined logic to the output records. 9. Validation: verify the output contains the expected number of records, all specified headers are present in each dictionary, and data types match the conversion directives configuration.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history provided in the discussion section
- Source material was synthesized at 2026-06-15 but no concrete reference documentation, specification document, or code examples for the matrix directive handler are present in the provided section text

## Domain Knowledge
- Matrix directives in MESSES are designed to transform flat or nested JSON records into tabular representations by mapping input fields to output headers and supporting record collation, filtering, and custom transformations.
- The collate sub-field groups multiple records by a common key, aggregating them into single output dictionaries to produce summary or flattened representations.
- The fields_to_headers mapping establishes the transformation rule binding input field paths to output dictionary keys, enabling flexible schema adaptation.
- Custom code execution via the code sub-field allows arbitrary Python transformations on individual records after collation, sorting, and filtering are applied.
- The test sub-field filters records using a boolean condition expression, and exclusion_headers removes records containing specified header values, providing multi-stage record selection.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does the matrix directive handler resolve a matrix-type record from conversion directives against input JSON to produce a list of dictionaries, including support for headers, collation, field exclusion, sorting, filtering, and custom code?: 'The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table. By'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields; collate records by a grouping field; map record fields to dictionary keys via headers; exclude fields with exclusion_headers; convert values to strings with values_to_str; or execute custom Python code for complex transformations.: 'The "headers" field will create a new dictionary for every record in the indicated table, but sometimes you might need to pull data from multiple records into a single new dictionary, and the'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Conversion directives file specifying matrix-type record transformation rules: 'The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Input JSON data containing records to be transformed: 'The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] List of dictionaries representing resolved matrix-type records with mapped headers and applied transformations: 'To support the JSON-to-JSON conversion a relatively simple set of directives were developed'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Python: 'MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] jsonschema: 'utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history provided in the discussion section: '_No changelog found._'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] Source material was synthesized at 2026-06-15 but no concrete reference documentation, specification document, or code examples for the matrix directive handler are present in the provided section text: 'Synthesized at: 2026-06-15T14:01:02+00:00'

## Evaluation Strategy
### Direct Checks
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

### Expert Review
- assess correctness of matrix-to-dictionary transformation logic: verify that the mapping from input JSON record fields to output dictionary headers follows the fields_to_headers directive specification faithfully
- assess soundness of collate strategy: verify that field merging or combination respects data semantics and does not produce information loss or corruption
- assess robustness of conditional filtering: verify that test sub-field expressions correctly identify which input records should be included/excluded in output
- assess code execution safety and correctness: review embedded code sub-field execution for correctness, side effects, and alignment with documented behavior

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Parse matrix-type conversion directives to extract configuration parameters (headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, code).
2. Load input JSON and apply field-to-header mapping to construct output dictionaries with specified key names.
3. Filter records using test condition and exclusion_headers criteria to retain qualifying records.
4. Collate grouped records using the collate directive to aggregate multiple source records into single outputs.
5. Convert specified fields to string representation and sort results by specified fields in configured order.
6. Execute custom transformation code to apply user-defined logic to final records.
7. Validation: confirm output record count matches expected cardinality, all headers are present in each dictionary, data types conform to directives, and no records fail test or exclusion criteria.
8. References: source article (DOI: 10.3390/metabo11030163)

## Workflow Ports

**Inputs:**

- `directives_file` — Conversion directives file with matrix-type configuration ← `task_001/resolved_json`
- `input_json` — Input JSON data containing source records

**Outputs:**

- `matrix_records` — List of dictionaries with resolved matrix-type records

**Used:** `urn:asb:port:task_001/resolved_json`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:MoseleyBioinformaticsLab__MESSES`
- **Synthesized at:** 2026-06-15T14:07:59+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
