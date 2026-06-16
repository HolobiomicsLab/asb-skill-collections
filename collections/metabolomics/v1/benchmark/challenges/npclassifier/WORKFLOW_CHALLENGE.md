# Workflow Challenge: `coll_npclassifier_workflow`


> NP Classifier is a natural product classification system providing programmatic access via a /classify API endpoint that accepts SMILES strings and returns predictions through TensorFlow Serving.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The NP Classifier implements a RESTful API architecture for molecular classification. The system exposes two key endpoints: a /classify endpoint that accepts SMILES strings as query parameters for programmatic classification requests, and a /model/metadata endpoint that provides model metadata through TensorFlow Serving. The underlying models are deployed in a dockerized environment and require specific layer naming conventions: input layers named 'input_2048' and 'input_4096', and an output layer named 'output'. The workflow describes a Keras model conversion process that produces HDF5 TF2 models with these specified layer names to ensure compatibility with the serving infrastructure.

## Research questions

- Does the /classify API endpoint accept a SMILES string parameter and return a properly structured classification response?
- Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names when queried on the running Dockerized NP-Classifier server?
- What are the required layer names that a converted Keras model must expose after transformation to HDF5 TensorFlow 2.3.0 format for use in the NP Classifier pipeline?

## Methods overview

Verify Docker containers (NP-Classifier server and TensorFlow Serving) are running and healthy. Construct HTTP GET request to /classify endpoint with valid SMILES string parameter. Execute request and capture HTTP response (status code, headers, body). Parse JSON response body and validate structure contains 'output' field. Confirm input layer names 'input_2048' and 'input_4096' are present in response metadata or model schema. Validation: HTTP status is 200, response is valid JSON, and all required layer names match specification. Launch the NP-Classifier Docker Compose stack to start TensorFlow Serving. Issue an HTTP GET request to the /model/metadata REST endpoint exposed by TensorFlow Serving. Parse the JSON response and extract input/output layer metadata. Validate that input layers are exactly named 'input_2048' and 'input_4096' and output layer is named 'output'. Validation: metadata response contains all three expected layer names with correct spelling and format. Clone the NP-Classifier GitHub repository to obtain the model conversion script and pre-trained model artifacts. Execute the get_models.sh script from Classifier/models_folder/models to download and convert Keras models to HDF5 TF2 format using TensorFlow 2.3.0. Load the resulting HDF5 model into a TensorFlow 2.3.0 environment and programmatically inspect all layer objects. Extract and validate layer names, confirming exact matches for 'input_2048', 'input_4096', and 'output'. Validation: layer name inspection must report all three required layers with exact spelling and no additional input or output layers deviating from the specification.

**Domain:** bioinformatics

**Techniques:** machine-learning, deep-learning

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** NP Classifier is typically deployed locally.
- **(finding)** Docker and docker-compose are required to bring up the NP Classifier.
- **(finding)** NP Classifier models are downloaded via a shell script located at Classifier/models_folder/models/get_models.sh.
- **(finding)** Python must be installed to convert keras models into HDF5 TF2 models. _[grounded: TOOL_TENSORFLOW]_
- **(finding)** TensorFlow version 2.3.0 must be installed to convert keras models into HDF5 TF2 models. _[grounded: TOOL_TENSORFLOW]_
- **(finding)** A Docker network named nginx-net must be created before building the dockerized server.
- **(finding)** The dockerized server is built using the make server-compose command.
- **(finding)** Model metadata can be checked at the /model/metadata endpoint via TensorFlow Serving. _[grounded: TOOL_TENSORFLOW]_
- **(finding)** If model input names change, the code must be updated accordingly.
- **(finding)** Input layer names should be "input_2048" and "input_4096". _[grounded: COMP_INPUT_2048]_
- **(finding)** The output layer name should be "output". _[grounded: COMP_OUTPUT_LAYER]_
- **(finding)** NP Classifier can be used programmatically via the /classify API endpoint with SMILES notation. _[grounded: API_CLASSIFY]_
- **(finding)** A cached flag can be provided as a parameter to the /classify endpoint to retrieve cached results and improve performance.

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- TensorFlow version 2.3.0 is required to convert keras models into HDF5 TF2 models

## Steps

### Step `task_001`
- Title: Reproduce the /classify API endpoint response for a SMILES query
- Task kind: `reproduction`
- Task: Send a SMILES string to the running NP-Classifier /classify endpoint and verify the classification response is returned with the expected JSON structure (input layers 'input_2048' and 'input_4096', output layer 'output').
- Inputs:
  - SMILES string for chemical compound (e.g., 'CC(C)Cc1ccc(cc1)C(C)C(O)=O' or similar valid SMILES)
  - Running NP-Classifier server with TensorFlow Serving backend deployed via Docker Compose
- Expected outputs:
  - JSON response object containing classification results with output field and metadata confirming input/output layer names
- Tools: docker, docker-compose, TensorFlow Serving, Python
- Landmark output files: http_status_code.txt, response_headers.json, classification_response.json
- Primary expected artifact: `classification_response.json`

### Step `task_002`
- Title: Reproduce the /model/metadata API response via TensorFlow Serving passthrough
- Task kind: `reproduction`
- Task: Query the /model/metadata endpoint on a running Dockerized NP-Classifier server and verify that TensorFlow Serving returns complete model metadata including input layer names ('input_2048', 'input_4096') and output layer name ('output'). Save the metadata response as a JSON file.
- Inputs:
  - Running NP-Classifier Docker container with TensorFlow Serving endpoint
- Expected outputs:
  - Model metadata JSON response containing input and output layer names
- Tools: docker, docker-compose, TensorFlow Serving
- Landmark output files: tf_serving_response.json
- Primary expected artifact: `model_metadata.json`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the Keras model conversion step producing a HDF5 TF2 model with named input/output layers
- Task kind: `component_reconstruction`
- Task: Using the get_models.sh script and TensorFlow 2.3.0, convert Keras classification models to HDF5 TF2 format and verify that the resulting model exposes input layers named 'input_2048' and 'input_4096', plus an output layer named 'output'.
- Inputs:
  - NP-Classifier repository from github.com/mwang87/NP-Classifier
  - TensorFlow 2.3.0 installed environment
- Expected outputs:
  - HDF5 TF2 model file with verified layer names (input_2048, input_4096, output)
  - Verification report listing confirmed layer names and structural compliance
- Tools: docker, get_models.sh, TensorFlow 2.3.0, Python
- Landmark output files: converted_model.h5, layer_names.json, model_verification_report.txt
- Primary expected artifact: `model_verification_report.txt`

## Final expected outputs

- `Model metadata JSON response containing input and output layer names` (type: file, tolerance: hash)
- `HDF5 TF2 model file with verified layer names (input_2048, input_4096, output)` (type: file, tolerance: hash)
- `Verification report listing confirmed layer names and structural compliance` (type: file, tolerance: hash)

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
  "workflow_id": "coll_npclassifier_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003"
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
    }
  },
  "final_outputs": {
    "Model metadata JSON response containing input and output layer names": "<locator>",
    "HDF5 TF2 model file with verified layer names (input_2048, input_4096, output)": "<locator>",
    "Verification report listing confirmed layer names and structural compliance": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
