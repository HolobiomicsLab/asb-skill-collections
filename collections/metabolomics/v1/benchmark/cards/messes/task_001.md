# SciTask Card: Reconstruct the str Directive resolution engine for the Conversion Directives Engine

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T14:01:04.089933+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_messes/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- DOI: `10.3390/metabo11030163`
- GitHub: `MoseleyBioinformaticsLab/MESSES`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Techniques: `quality-control`, `database-annotation`

## Research Question
How does the str directive handler resolve a record from input JSON by reading conversion directive specifications that include override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters?

## Connected Finding
The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific record and extracts fields; for_each iterates over all records with optional test filtering and delimiter-separated concatenation; sort_by and sort_order control record ordering before selection or iteration.

## Task Description
Implement the str directive handler within the Conversion Directives Engine that reads conversion directives from JSON/tagged-tabular input and resolves a single str-type record against an input JSON document, supporting override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields sub-directive parameters. Produce a Python module with unit tests demonstrating correct directive resolution.

## Inputs
- Conversion directives JSON file with str-type directive definition
- Input JSON document to be resolved against conversion directives

## Expected Outputs
- Resolved JSON document with str-type records populated according to directive specifications
- Unit test suite (Python) validating str directive handler for override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters

## Expected Output File

- `str_directive_handler.py`

## Landmark Outputs

- `directives_parsed.json`
- `resolved_records.json`
- `test_results.txt`

## Tools
- Python
- jsonschema

## Skills
- json-schema-validation
- directive-engine-implementation
- conditional-record-resolution
- string-concatenation-with-delimiters
- field-mapping-and-transformation
- unit-test-design-for-data-processing

## Workflow Description
1. Parse conversion directives JSON file to extract str-type directive definition with all sub-fields (override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields). 2. Load the target input JSON document against which the directive will be resolved. 3. Evaluate conditional test sub-directive (if present) to determine whether to apply the str directive; skip resolution if test condition fails. 4. If for_each is specified, iterate over the designated array or object collection in the input JSON; otherwise apply directive once to the root or specified record_id target. 5. For each iteration, apply code transformation (if present) to resolve dynamic values, then concatenate selected field values using the specified delimiter and output to the resolved str field. 6. If sort_by and sort_order sub-directives are present, sort the concatenated or iterated results accordingly. 7. If override sub-directive is true, replace existing str field values; otherwise preserve existing values and only populate missing fields. 8. Write resolved JSON output to file and validate against input schema.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog provided for the mwtab library or MESSES package to document specific implementation details, version history, or API stability of the str directive handler.

## Domain Knowledge
- Conversion directives are JSON-formatted rule specifications that transform intermediate JSON documents into target formats; str-type directives specifically concatenate field values into string outputs using delimiter-separated fields.
- The for_each sub-directive enables iteration over arrays or object collections within the input JSON, allowing the same str transformation to be applied across multiple records.
- Conditional resolution via the test sub-directive allows str directives to be applied only when specific logical conditions on the input JSON are satisfied, preventing invalid or irrelevant string construction.
- The override boolean parameter determines whether existing str field values in the input JSON are preserved (override=false) or replaced entirely (override=true) with directive-computed values.
- The code sub-directive supports dynamic value resolution through programmatic transformation functions, enabling str concatenation to reference computed or derived field values in addition to literal input fields.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Resolved JSON document with str-type records populated according to directive specifications, Unit test suite (Python) validating str directive handler for override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does the str directive handler resolve a record from input JSON by reading conversion directive specifications that include override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters?: 'Every record must have a "value_type" field, and the value of this field determines the other required and meaningful fields the record can have. The allowed values for the "value_type" field are'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific record and extracts fields; for_each iterates over all records with optional test filtering and delimiter-separated concatenation; sort_by and sort_order control record ordering before selection or iteration.: 'The str type produces a single string value for the record. The value can be built from a single record in the table or by iterating over all of them, and the records can be sorted and filtered'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Conversion directives JSON file with str-type directive definition: 'The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Input JSON document to be resolved against conversion directives: 'The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Resolved JSON document with str-type records populated according to directive specifications: 'The convert command of MESSES supports converting JSON data to another JSON format or another supported format'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Unit test suite (Python) validating str directive handler for override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters: 'The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Python: 'MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] jsonschema: 'utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] No changelog provided for the mwtab library or MESSES package to document specific implementation details, version history, or API stability of the str directive handler.: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
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

### Expert Review
- verify that the precedence and interaction logic among override, code, record_id, for_each, and test sub-fields aligns with the intended semantics of the Conversion Directives Engine
- verify that edge cases (missing sub-fields, empty arrays, null values, type mismatches) are handled gracefully and produce defensible outputs
- verify that the str handler correctly integrates with other value_type handlers within the broader Conversion Directives Engine

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Parse conversion directives JSON to extract str-type definition with all sub-fields.
2. Load input JSON document and locate target records by record_id or root scope.
3. Evaluate test condition (if present) to gate directive application.
4. Iterate over for_each collection (if specified) or apply once to target record.
5. Apply code transformation (if present) and resolve field references.
6. Concatenate resolved field values using specified delimiter.
7. Apply sort_by and sort_order transformations (if specified).
8. Apply override logic to determine whether to replace or preserve existing str values.
9. Validation: Confirm resolved JSON output contains str fields populated per directive specification, test sub-directive conditions respected, for_each iteration complete, and override behavior matches expected state.
10. References: source article (DOI: 10.3390/metabo11030163)

## Workflow Ports

**Inputs:**

- `directives_json` — Conversion directives JSON file with str-type definition
- `input_json` — Input JSON document to resolve

**Outputs:**

- `resolved_json` — Resolved JSON with str records populated
- `test_suite` — Unit tests for str directive handler

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:MoseleyBioinformaticsLab__MESSES`
- **Synthesized at:** 2026-06-15T14:07:59+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
