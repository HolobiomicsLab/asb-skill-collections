# Workflow Challenge: `coll_idslmint_workflow`


> IDSL_MINT is a mass spectrometry data processing framework constructed upon transformer models following the 'Attention is All You Need' paradigm for interpreting mass spectra.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 1-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

IDSL_MINT, developed by the Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME), is a mass spectrometry data processing framework that builds upon transformer-based architectures as described in the 'Attention is All You Need' framework. The paper describes the underlying transformer-based mechanism for mass spectra interpretation that forms the foundation of IDSL_MINT's approach to metabolomics data processing.

## Research questions

- How is the transformer model architecture from 'Attention is All You Need' adapted and implemented within IDSL_MINT to process mass spectrometry data?

## Methods overview

Define a multi-head self-attention layer with learnable query, key, value projections and output projection. Implement a feed-forward network with ReLU activation and two linear transformations. Stack transformer encoder blocks with residual connections, layer normalization, and dropout. Add sinusoidal positional encoding to spectrum embeddings to preserve order information. Instantiate the complete transformer model in PyTorch with specified hyperparameters. Convert representative mass spectrum (m/z and intensity) into a tensor of shape (sequence_length, embedding_dimension). Execute model.eval() and perform a forward pass on the input spectrum tensor. Validation: Verify that the output tensor has correct shape, contains no NaN/Inf values, and model parameters are learnable.

**Domain:** metabolomics

**Techniques:** deep-learning, machine-learning, metabolite-identification, in-silico-fragmentation, spectral-library-matching, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** IDSL_MINT is a mass spectrometry data processing framework developed by the Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME). _[grounded: IDSL_MINT_system]_
- **(finding)** IDSL_MINT's approach for mass spectrometry data processing is constructed upon transformer models. _[grounded: IDSL_MINT_system]_
- **(finding)** IDSL_MINT is powered by RDKit. _[grounded: IDSL_MINT_system]_
- **(finding)** IDSL_MINT uses PyTorch. _[grounded: IDSL_MINT_system]_
- **(finding)** IDSL_MINT is developed by Sadjad Fakouri Baygi. _[grounded: IDSL_MINT_system]_

## Steps

### Step `task_001`
- Title: Reconstruct the transformer-based mass spectra interpretation pipeline in IDSL_MINT
- Task kind: `component_reconstruction`
- Task: Implement the core transformer model architecture used by IDSL_MINT for processing mass spectrometry data in PyTorch. Verify that the model can be instantiated and execute a forward pass on a representative input spectrum.
- Inputs:
  - Transformer architecture specification (embedding dimension, number of attention heads, number of encoder layers, feed-forward hidden dimension, dropout rate)
  - Representative mass spectrum input (m/z and intensity pairs formatted as a tensor)
- Expected outputs:
  - PyTorch model instance in evaluation mode, successfully initialized
  - Forward pass output tensor with validated shape and numerical content
  - Model instantiation and forward pass execution log (including input/output shapes and timing)
- Tools: PyTorch, RDKit, Python
- Landmark output files: model_architecture.py, model_checkpoint.pt, forward_pass_output.tensor
- Primary expected artifact: `execution_log.txt`

## Final expected outputs

- `PyTorch model instance in evaluation mode, successfully initialized` (type: file, tolerance: hash)
- `Forward pass output tensor with validated shape and numerical content` (type: file, tolerance: hash)
- `Model instantiation and forward pass execution log (including input/output shapes and timing)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_idslmint_workflow",
  "agent_order": [
    "task_001"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "PyTorch model instance in evaluation mode, successfully initialized": "<locator>",
    "Forward pass output tensor with validated shape and numerical content": "<locator>",
    "Model instantiation and forward pass execution log (including input/output shapes and timing)": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
