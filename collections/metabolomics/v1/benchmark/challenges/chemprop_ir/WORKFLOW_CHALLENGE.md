# Workflow Challenge: `coll_chemprop_ir_workflow`


> This work describes the chemprop-IR architecture, an extension of chemprop that integrates new spectral features for infrared spectral prediction using message passing neural networks.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reconstructs 2 described mechanisms (described in the paper but not separately evaluated there): The chemprop-IR architecture is an extension of chemprop that incorporates new spectral features for infrared spectral predictions using message passing neural networks. chemprop-IR is an extension of chemprop that incorporates new spectral features designed specifically for infrared spectral predictions using message passing neural networks.

## Research questions

- How does the chemprop-IR architecture extend the base chemprop message passing neural network with new spectral features?
- What are the spectral features that chemprop-IR implements to extend the base chemprop architecture for infrared spectral prediction tasks?

## Methods overview

Clone and load the base chemprop message passing neural network architecture from the official repository. Design and implement the spectral features module as a PyTorch extension layer that augments chemprop's learned molecular representations. Integrate the spectral features module into the chemprop model definition, ensuring proper tensor shape alignment and gradient flow. Instantiate the chemprop-IR model with the spectral features module and verify successful compilation. Execute a forward pass on a sample molecule (SMILES or graph tensor) to verify model execution and output tensor generation. Validation: model instantiates without errors, forward pass completes successfully, and output tensor shape matches the spectral prediction dimension. Retrieve and parse the chemprop-IR repository to locate the spectral features component implementation. Study the feature construction logic and API to understand input requirements and output format. Instantiate the spectral feature extraction module with test molecular inputs. Execute feature extraction on example molecules and collect output tensors. Validation: Confirm that extracted features have the correct dimensionality, data type (float tensor), and non-null values consistent with the chemprop-IR architecture specification.

**Domain:** cheminformatics

**Techniques:** deep-learning, graph-neural-network, machine-learning, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The chemprop-IR architecture is an extension of chemprop with new spectral features. _[grounded: chemprop_IR_system]_
- **(finding)** Message passing neural networks are used for spectral predictions in this repository.
- **(finding)** The repository is available at github:gfm-collab__chemprop-IR. _[grounded: chemprop_IR_system]_
- **(finding)** The document was synthesized on 2026-06-15T10:08:50+00:00.
- **(finding)** Detailed information on base chemprop functionality is available in README_chemprop. _[grounded: chemprop_base]_

## Steps

### Step `task_001`
- Title: Reconstruct the chemprop-IR MPNN architecture as an extension of chemprop base
- Task kind: `component_reconstruction`
- Task: Reconstruct the chemprop-IR model architecture by extending the base chemprop message passing neural network with a new spectral features module. Verify the extended model can be instantiated and execute a forward pass on a sample molecule.
- Inputs:
  - chemprop base model code and architecture definition from github.com/chemprop/chemprop
  - sample molecular input (SMILES string or graph representation)
- Expected outputs:
  - instantiated chemprop-IR model with spectral features module successfully compiled
  - forward pass output tensor from sample molecule verification
- Tools: chemprop, chemprop-IR
- Landmark output files: chemprop_base_architecture.txt, spectral_features_module.py, chemprop_ir_model_summary.txt, forward_pass_output_shape.txt
- Primary expected artifact: `chemprop_ir_model_verification.log`

### Step `task_002`
- Depends on: `task_001`
- Title: Implement the spectral feature extraction step within the chemprop-IR pipeline
- Task kind: `component_reconstruction`
- Task: Extract and construct spectral features from molecular structures using the chemprop-IR spectral features component. Produce a feature extraction module that accepts molecular inputs (SMILES or molecular graphs) and outputs the named spectral features as implemented in the chemprop-IR repository.
- Inputs:
  - chemprop-IR repository code and README from github.com/chemprop/chemprop
  - Test molecular structures (SMILES strings or molecular graph objects)
- Expected outputs:
  - Spectral features tensor or feature matrix extracted from test molecules
  - Feature extraction module code or validated implementation script
  - Verification report confirming feature shape, data type, and completeness
- Tools: chemprop, chemprop-IR
- Landmark output files: spectral_features_component.py, feature_extraction_test.py, test_features_output.pt, feature_verification.txt
- Primary expected artifact: `spectral_features_extracted.pt`

## Final expected outputs

- `Spectral features tensor or feature matrix extracted from test molecules` (type: file, tolerance: hash)
- `Feature extraction module code or validated implementation script` (type: file, tolerance: hash)
- `Verification report confirming feature shape, data type, and completeness` (type: file, tolerance: hash)

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

- **Composition modularity:** hierarchical

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
  "workflow_id": "coll_chemprop_ir_workflow",
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
    "Spectral features tensor or feature matrix extracted from test molecules": "<locator>",
    "Feature extraction module code or validated implementation script": "<locator>",
    "Verification report confirming feature shape, data type, and completeness": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
