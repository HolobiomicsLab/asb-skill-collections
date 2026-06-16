# Workflow Challenge: `coll_messes_workflow`


> MESSES is a Python package that converts tabular experimental metadata into structured JSON formats and supports transformation between JSON representations and specialized domain formats. The package demonstrates mechanisms for extracting tagged tabular data, validating against schemas, and converting between formats using customizable directives.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MESSES (Metadata from Experimental SpreadSheets Extraction System) facilitates conversion of tabular data into JSON and other formats through three primary commands: extract converts tagged tabular data into intermediate JSON form, validate checks JSON data against the experiment description specification and optional user-provided schemas, and convert transforms JSON to other formats using conversion directives. The convert command employs directive-driven transformations that support str directives for building string values through override, code evaluation, record selection, or iteration with filtering and sorting; matrix directives for generating lists of dictionaries through field mapping, record collation, and custom code execution; and generic JSON-to-JSON conversion. The system processes directives defined in JSON or tagged tabular form, where table columns marked with #<table_name>.id denote record identifiers and columns marked with #.<field_name> denote record fields. Conversion results were demonstrated on metabolomics datasets: the collate directive grouped measurement records by assignment field to consolidate intensity values across samples for each metabolite, and the for_each directive with filtering and sorting concatenated multiple sample preparation protocol descriptions into a single summary field.

## Research questions

- How does the str directive handler resolve a record from input JSON by reading conversion directive specifications that include override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters?
- How does the matrix directive handler resolve a matrix-type record from conversion directives against input JSON to produce a list of dictionaries, including support for headers, collation, field exclusion, sorting, filtering, and custom code?
- How does the parser convert a tagged tabular file (using export tags like #<table_name>.id and #.<field_name>) into the nested JSON structure required by the directive resolvers?
- When a matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by assignment and merge their sample intensity data into a single dictionary?
- When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records, does the output match the expected concatenated summary string?

## Methods overview

Parse conversion directives JSON to extract str-type definition with all sub-fields. Load input JSON document and locate target records by record_id or root scope. Evaluate test condition (if present) to gate directive application. Iterate over for_each collection (if specified) or apply once to target record. Apply code transformation (if present) and resolve field references. Concatenate resolved field values using specified delimiter. Apply sort_by and sort_order transformations (if specified). Apply override logic to determine whether to replace or preserve existing str values. Validation: Confirm resolved JSON output contains str fields populated per directive specification, test sub-directive conditions respected, for_each iteration complete, and override behavior matches expected state. References: source article (DOI: 10.3390/metabo11030163) Parse matrix-type conversion directives to extract configuration parameters (headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, code). Load input JSON and apply field-to-header mapping to construct output dictionaries with specified key names. Filter records using test condition and exclusion_headers criteria to retain qualifying records. Collate grouped records using the collate directive to aggregate multiple source records into single outputs. Convert specified fields to string representation and sort results by specified fields in configured order. Execute custom transformation code to apply user-defined logic to final records. Validation: confirm output record count matches expected cardinality, all headers are present in each dictionary, data types conform to directives, and no records fail test or exclusion criteria. References: source article (DOI: 10.3390/metabo11030163) Parse tagged tabular file headers to extract export tag directives Build hierarchical JSON object by mapping table names, record identifiers, and field names to nested structure Validate tag syntax compliance and uniqueness constraints Output nested JSON structure for downstream Conversion Directives Engine consumption Validation: parsed JSON structure contains all tagged columns in correct hierarchy with no duplicate record identifiers within each table References: source article (DOI: 10.3390/metabo11030163) Load the IC-FTMS example dataset in JSON format from MESSES documentation Parse and configure a matrix conversion directive with collate='assignment' parameter Execute MESSES convert command to apply the directive and generate output list of dictionaries Compare output structure and content against documented expected output in Collate section Validation: verify that the produced list of dictionaries exactly matches the expected JSON structure documented in the Collate section reference References: source article (DOI: 10.3390/metabo11030163) Load the documented example JSON input containing the protocol table. Apply str directive with for_each=True and test='type=sample_prep' to filter protocol records. Sort filtered records by 'id' field in ascending order. Concatenate sorted record values using space delimiter to generate SAMPLEPREP_SUMMARY. Validation: Compare generated SAMPLEPREP_SUMMARY string character-for-character against the expected output documented in the For Each section. References: source article (DOI: 10.3390/metabo11030163)

**Domain:** metabolomics

**Techniques:** quality-control, database-annotation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MESSES is a Python package that facilitates the conversion of tabular data into other formats. _[grounded: MESSES_system]_
- **(finding)** MESSES was initially created to pull mass spectrometry and nuclear magnetic resonance experimental data into a database. _[grounded: MESSES_system]_
- **(finding)** The convert command transforms JSON format to the JSON version of supported formats and then to the final niche format. _[grounded: convert_command]_
- **(finding)** The convert command supports simple JSON-to-JSON conversion through the "generic" sub-command. _[grounded: convert_command]_
- **(finding)** The str directive produces a single string value for the record. _[grounded: str_directive]_
- **(finding)** The matrix directive produces a list of dictionaries (aka an array of objects) for the record. _[grounded: matrix_directive]_
- **(finding)** The section type can produce anything for the whole table.
- **(finding)** The extract command supports turning tabular data into JSON by adding a layer of tags on top of the data. _[grounded: MESSES_system]_
- **(finding)** The validate command supports validating JSON data largely through utilizing JSON Schema. _[grounded: MESSES_system]_
- **(finding)** The validate command performs validation beyond the capabilities of JSON Schema.
- **(finding)** The Metabolomics Standards Initiative is an international community effort launched in 2005 by the Metabolomics Society.
- **(finding)** The MSI established consensus-based reporting standards for metabolomics data to ensure experimental results are transparent, reproducible, and reusable.
- **(finding)** The Schymanski 2014 paper on MSI confidence levels is the most widely cited and used version of the system.
- **(finding)** The Sumner guidelines describe 4 levels of MSI confidence assignment.
- **(finding)** The Jeon 2013 publication describes 4 levels of MSI confidence, more concrete than the original paper.
- **(finding)** The Schymanski 2014 paper describes 5 levels of MSI confidence with level 2a and 2b.
- **(finding)** The Schrimpe-Rutledge 2016 publication describes 5 levels of MSI confidence.
- **(finding)** The override field in conversion directives allows direct specification of a string value. _[grounded: override_field]_
- **(finding)** The code field in conversion directives allows Python code to be delivered directly to eval(). _[grounded: code_field]_
- **(finding)** The for_each field in str directives allows looping over all records in a table.
- **(finding)** The delimiter field in str directives specifies how to separate strings built from each record.
- **(finding)** The test field in str directives filters records based on field equality conditions.
- **(finding)** The sort_by field in str directives allows sorting input JSON records before building the value.
- **(finding)** The matrix directive creates a list of dictionaries by looping over all records in the indicated table. _[grounded: matrix_directive]_
- **(finding)** The collate field in matrix directives groups record data into dictionaries based on a specified field value. _[grounded: collate_field]_
- **(finding)** The fields_to_headers field changes matrix directive behavior to copy all fields from input records as is into the dictionary. _[grounded: matrix_directive]_
- **(finding)** The exclusion_headers field in matrix directives allows excluding specific fields from being added.
- **(finding)** The values_to_str field in matrix directives can convert all field values to strings.
- **(finding)** The required field in conversion directives indicates if a directive is required, stopping the program on error if true.
- **(finding)** The default field in conversion directives provides a string value to default to if the directive cannot be built and is not required.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- JSON Schema validation can be turned off with options, and users can provide their own JSON schema

## Steps

### Step `task_001`
- Title: Reconstruct the str Directive resolution engine for the Conversion Directives Engine
- Task kind: `component_reconstruction`
- Task: Implement the str directive handler within the Conversion Directives Engine that reads conversion directives from JSON/tagged-tabular input and resolves a single str-type record against an input JSON document, supporting override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields sub-directive parameters. Produce a Python module with unit tests demonstrating correct directive resolution.
- Inputs:
  - Conversion directives JSON file with str-type directive definition
  - Input JSON document to be resolved against conversion directives
- Expected outputs:
  - Resolved JSON document with str-type records populated according to directive specifications
  - Unit test suite (Python) validating str directive handler for override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters
- Tools: Python, jsonschema
- Landmark output files: directives_parsed.json, resolved_records.json, test_results.txt
- Primary expected artifact: `str_directive_handler.py`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the matrix Directive resolution engine including collate and fields_to_headers behaviour
- Task kind: `component_reconstruction`
- Task: Implement a matrix directive handler that resolves matrix-type records from a conversion directives file against input JSON data, producing a list of dictionaries with support for headers, collation, field mapping, exclusion, value stringification, sorting, filtering, and custom code execution.
- Inputs:
  - Conversion directives file specifying matrix-type record transformation rules
  - Input JSON data containing records to be transformed
- Expected outputs:
  - List of dictionaries representing resolved matrix-type records with mapped headers and applied transformations
- Tools: Python, jsonschema
- Landmark output files: parsed_directives.json, filtered_records.json, collated_records.json, sorted_records.json
- Primary expected artifact: `matrix_records.json`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement tagged-tabular-to-JSON conversion for Conversion Directives input parsing
- Task kind: `component_reconstruction`
- Task: Implement a parser that accepts tagged tabular input (using export tags like #<table_name>.id and #.<field_name>) and converts it to nested JSON structures compatible with the Conversion Directives Engine resolver.
- Inputs:
  - Tagged tabular file (CSV or TSV format) with export tags in column headers
- Expected outputs:
  - Nested JSON object with table-record-field hierarchy matching tagged column structure
- Tools: Python
- Landmark output files: tag_mapping.csv, record_index.json
- Primary expected artifact: `parsed_nested_structure.json`

### Step `task_004`
- Depends on: `task_001`
- Title: Reproduce the IC-FTMS collate matrix directive output from the example dataset
- Task kind: `reproduction`
- Task: Apply a matrix directive with collate='assignment' to the IC-FTMS measurement example dataset documented in the MESSES documentation and verify that the resulting list of dictionaries matches the expected output JSON shown in the Collate section.
- Inputs:
  - IC-FTMS measurement example dataset in JSON format from MESSES documentation
- Expected outputs:
  - List of dictionaries produced by matrix directive with collate='assignment' matching documented expected output
- Tools: Python, jsonschema
- Landmark output files: input_dataset.json, conversion_directive_spec.json, collated_output.json
- Primary expected artifact: `collated_output.json`

### Step `task_005`
- Depends on: `task_004`
- Title: Reproduce the SAMPLEPREP_SUMMARY for_each str directive output from the protocol example dataset
- Task kind: `reproduction`
- Task: Apply a str directive with for_each=True, test='type=sample_prep', sort_by=['id'], sort_order='ascending', and delimiter=' ' to a protocol table in JSON, producing a concatenated SAMPLEPREP_SUMMARY string that matches the documented expected output.
- Inputs:
  - Documented example input JSON with protocol table containing sample_prep type records
- Expected outputs:
  - Concatenated SAMPLEPREP_SUMMARY string matching the expected output in the For Each section of the documentation
- Tools: Python
- Landmark output files: filtered_protocol_records.json, sorted_protocol_records.json
- Primary expected artifact: `sampleprep_summary.txt`

## Final expected outputs

- `List of dictionaries representing resolved matrix-type records with mapped headers and applied transformations` (type: file, tolerance: hash)
- `Nested JSON object with table-record-field hierarchy matching tagged column structure` (type: file, tolerance: hash)
- `Concatenated SAMPLEPREP_SUMMARY string matching the expected output in the For Each section of the documentation` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_messes_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "List of dictionaries representing resolved matrix-type records with mapped headers and applied transformations": "<locator>",
    "Nested JSON object with table-record-field hierarchy matching tagged column structure": "<locator>",
    "Concatenated SAMPLEPREP_SUMMARY string matching the expected output in the For Each section of the documentation": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
