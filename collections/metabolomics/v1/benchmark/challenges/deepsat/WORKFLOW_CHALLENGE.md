# Workflow Challenge: `coll_deepsat_workflow`


> SMART 3 is a system that retrieves model metadata from TensorFlow Serving and provides an API for programmatic spectroscopic classification.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reconstructs 2 described mechanisms (described in the paper but not separately evaluated there): The SMART 3 system queries model metadata via an HTTP GET call to the /model/metadata endpoint on a TensorFlow Serving instance, from which model input names must be extracted and verified, as changes to these input names require corresponding code updates. The /api/smart3/search endpoint accepts peaks as a JSON list of dictionaries with 1H and 13C as headers for programmatic classification requests.

## Research questions

- How does the SMART 3 system query the TensorFlow Serving instance to retrieve and validate model metadata, and what information about input names must be extracted?
- How should peak data be formatted and submitted to the DeepSAT SMART 3 classification API endpoint to obtain predictions?

## Methods overview

Construct an HTTP GET request to the TensorFlow Serving /model/metadata endpoint. Execute the request and retrieve the JSON response from the server. Parse the returned JSON to extract model input tensor names and validate required response fields (signature, inputs, outputs). Write the extracted input names and validation results to a structured JSON output file. Validation: Confirm that the response structure is valid JSON, contains all expected top-level fields, and input names are non-empty strings matching the expected NMR spectroscopic dimensions (1H, 13C). Query the /model/metadata endpoint via TensorFlow Serving to retrieve and validate the current model input schema. Format NMR peak data as a JSON list of dictionaries with 1H and 13C keys. Submit a POST request to /api/smart3/search with the formatted JSON payload. Parse and extract classification predictions from the returned JSON response. Validation: HTTP response code is 200 (or documented success code), and response JSON contains expected prediction fields with valid numeric or categorical values.

**Domain:** bioinformatics

**Techniques:** deep-learning, machine-learning

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Model metadata can be checked by passing through tensorflow serving at the /model/metadata URL. _[grounded: tool_tensorflow_serving]_
- **(finding)** If the model input names change, the code must be updated accordingly.
- **(finding)** SMART 3 provides an API at /api/smart3/search for programmatic classification. _[grounded: component_smart3]_
- **(finding)** Peak data can be input to the SMART 3 API as a JSON list of dictionaries with 1H and 13C as headers. _[grounded: component_smart3]_
- **(finding)** DeepSAT source code is available on github under the user mwang87. _[grounded: system_deepsat]_

## Steps

### Step `task_001`
- Title: Reconstruct the TensorFlow Serving model metadata retrieval step in DeepSAT/SMART 3
- Task kind: `component_reconstruction`
- Task: Query the TensorFlow Serving /model/metadata endpoint for SMART 3 to retrieve and parse model input names, then validate that the response structure matches expected fields. Output the extracted metadata as a JSON file.
- Inputs:
  - TensorFlow Serving instance URL and endpoint path (/model/metadata)
- Expected outputs:
  - Parsed model metadata including input names and response validation status as JSON
- Tools: tensorflow serving
- Landmark output files: raw_metadata_response.json, extracted_input_names.json
- Primary expected artifact: `model_metadata.json`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the SMART 3 classification API call via /api/smart3/search
- Task kind: `component_reconstruction`
- Task: Implement a programmatic POST request to the DeepSAT SMART 3 Classification API endpoint (/api/smart3/search), submitting a JSON list of peak dictionaries with 1H and 13C NMR headers, and capture the structured prediction response.
- Inputs:
  - NMR peak data with 1H and 13C chemical shift headers
- Expected outputs:
  - Structured JSON response containing classification predictions and metadata from the API
- Tools: tensorflow serving
- Landmark output files: model_metadata.json, nmr_peaks_payload.json
- Primary expected artifact: `smart3_api_response.json`

## Final expected outputs

- `Structured JSON response containing classification predictions and metadata from the API` (type: file, tolerance: hash)

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

- **Abstraction level:** implicit

- **Orchestration planning:** static

- **Data transport:** streaming

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_deepsat_workflow",
  "agent_order": [
    "task_001",
    "task_002"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Structured JSON response containing classification predictions and metadata from the API": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
