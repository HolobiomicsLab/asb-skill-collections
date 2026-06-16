# Workflow Challenge: `coll_seacr_workflow`


> SEACR is a peak-calling tool described in literature for processing CUT&RUN bedGraph data, but the paper provides no concrete documentation of its implementation, executable components, or end-to-end operation.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 1-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This benchmark documents SEACR, a peak-calling mechanism designed to process bedGraph inputs from CUT&RUN experiments. However, the source material contains no detailed description of SEACR's shell and R script components, their executable status, or their integration for end-to-end operation. No mechanism documentation or implementation details are available in the provided text, limiting characterization of the tool's architecture and usage.

## Research questions

- What are the core computational components (shell and R scripts) that comprise the SEACR tool, and can they be executed end-to-end on typical CUT&RUN bedGraph input to produce peaked-regions output?

## Methods overview

Clone the SEACR repository from FredHutch GitHub. Verify presence of shell and R scripts and confirm executable permissions. Prepare or obtain a minimal valid CUT&RUN bedGraph test file. Run SEACR end-to-end on the test bedGraph input. Validate that peaked-regions output file is produced and contains valid genomic coordinates and peak annotations. Validation: Confirm repository cloning succeeds, all shell and R scripts exist with executable permissions set, and SEACR produces a non-empty peaked-regions file with proper BED-like format (chromosome, start, end, plus metadata columns).

**Domain:** bioinformatics

## Steps

### Step `task_001`
- Title: Reconstruct the SEACR peak-calling tool from its public GitHub repository
- Task kind: `component_reconstruction`
- Task: Clone the SEACR repository from GitHub, verify presence and executability of shell and R scripts, and validate end-to-end functionality by running the tool on a minimal CUT&RUN bedGraph input file to produce a peaked-regions output.
- Inputs:
  - GitHub repository URL: github:FredHutch__SEACR
  - Minimal CUT&RUN bedGraph test file with chromosome, start, end, and signal columns
- Expected outputs:
  - Peaked-regions output file from SEACR in BED or bedGraph format containing genomic coordinates and peak statistics
  - Verification log confirming cloned repository structure, script executability, and successful end-to-end run completion
- Tools: git, SEACR
- Landmark output files: repo_structure_manifest.txt, script_permissions_check.log, test_bedgraph_prepared.bedGraph, seacr_peaks.bed
- Primary expected artifact: `seacr_peaks.bed`

## Final expected outputs

- `Peaked-regions output file from SEACR in BED or bedGraph format containing genomic coordinates and peak statistics` (type: file, tolerance: hash)
- `Verification log confirming cloned repository structure, script executability, and successful end-to-end run completion` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** ad_hoc

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
  "workflow_id": "coll_seacr_workflow",
  "agent_order": [
    "task_001"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Peaked-regions output file from SEACR in BED or bedGraph format containing genomic coordinates and peak statistics": "<locator>",
    "Verification log confirming cloned repository structure, script executability, and successful end-to-end run completion": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
