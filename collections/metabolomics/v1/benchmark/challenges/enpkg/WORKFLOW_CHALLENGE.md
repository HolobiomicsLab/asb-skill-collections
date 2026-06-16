# Workflow Challenge: `coll_enpkg_workflow`


> ENPKG is a computational workflow for processing and integrating data into knowledge graphs through installation, setup, and execution stages. The workflow transforms raw input into annotated outputs ready for knowledge-graph integration.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The ENPKG full workflow describes a structured process comprising three primary operational stages: installation, setup, and execution. The workflow guide covers installation and environment setup procedures as foundational steps, followed by end-to-end pipeline execution that processes sample datasets and produces annotated outputs suitable for knowledge-graph integration.

## Research questions

- What are the conda and pip dependencies and installation procedures required to establish a functional ENPKG environment?
- What is the complete computational workflow executed by ENPKG from raw input data to final knowledge-graph-ready annotated outputs?

## Methods overview

Clone the enpkg/enpkg_full repository to a local working directory. Extract the conda environment specification (environment.yml or equivalent) from the repository. Create and activate a new conda environment using the declared dependency manifest. Install all pinned Python packages and external dependencies via conda and pip. Validation: Verify all declared packages are present at the correct pinned versions and that core ENPKG modules can be imported without error. References: source article (DOI: 10.1021/acscentsci.3c00800) Install ENPKG full workflow from repository and configure the computational environment with all required dependencies. Prepare and validate input dataset (spectral data and sample metadata) in the workflow's expected directory structure. Execute the ENPKG orchestrator, which automatically chains feature detection, spectral matching, molecular networking, and knowledge-graph annotation. Monitor execution logs and verify successful completion of all pipeline stages. Validation: Confirm that all expected output files (annotated features, knowledge-graph triples, spectral matches) exist, are non-empty, conform to output schema, and contain molecular annotations with confidence scores for test dataset samples. References: source article (DOI: 10.1021/acscentsci.3c00800)

**Domain:** cheminformatics

**Techniques:** machine-learning, database-annotation, dereplication, molecular-networking, deep-learning, in-silico-fragmentation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** ENPKG is a computational workflow for which a scientific paper exists.
- **(finding)** The ENPKG workflow guide covers installation, setup, and execution. _[grounded: enpkg_full_system]_
- **(finding)** The ENPKG full workflow is a computational workflow that can be explored by users. _[grounded: enpkg_full_system]_
- **(finding)** The ENPKG scientific paper contains insights and methodologies that power the workflow.

## Steps

### Step `task_001`
- Title: Reconstruct the ENPKG full workflow installation and environment setup
- Task kind: `component_reconstruction`
- Task: Reconstruct and verify the conda/pip environment for the ENPKG full workflow by installing all declared dependencies, producing a validated and reproducible computational runtime.
- Inputs:
  - enpkg/enpkg_full GitHub repository URL
- Expected outputs:
  - Installed conda environment with all ENPKG dependencies at pinned versions
  - Environment verification report listing all installed packages and versions
- Tools: ENPKG
- Landmark output files: environment.yml, conda_env_packages.txt, pip_freeze_output.txt
- Primary expected artifact: `env_verification_report.txt`

### Step `task_002`
- Title: Reconstruct the end-to-end ENPKG pipeline execution on a sample dataset
- Task kind: `component_reconstruction`
- Task: Execute the complete ENPKG full workflow on the provided example or test dataset, producing all final annotated output files ready for knowledge-graph integration and natural products annotation.
- Inputs:
  - ENPKG repository (enpkg_full) with installation instructions and example dataset
  - Example or test dataset (raw spectral data and sample metadata files)
- Expected outputs:
  - Annotated feature table with molecular identifications and confidence scores
  - Knowledge-graph output files in standardized format (RDF triples or equivalent)
  - Spectral library matches and molecular network visualization outputs
- Tools: ENPKG
- Landmark output files: input_manifest.txt, feature_detection_results.csv, molecular_network.graphml, spectral_matches.tsv, annotated_features_final.csv, knowledge_graph.rdf

## Final expected outputs

- `Installed conda environment with all ENPKG dependencies at pinned versions` (type: file, tolerance: hash)
- `Environment verification report listing all installed packages and versions` (type: file, tolerance: hash)
- `Annotated feature table with molecular identifications and confidence scores` (type: file, tolerance: hash)
- `Knowledge-graph output files in standardized format (RDF triples or equivalent)` (type: file, tolerance: hash)
- `Spectral library matches and molecular network visualization outputs` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

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
  "workflow_id": "coll_enpkg_workflow",
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
    "Installed conda environment with all ENPKG dependencies at pinned versions": "<locator>",
    "Environment verification report listing all installed packages and versions": "<locator>",
    "Annotated feature table with molecular identifications and confidence scores": "<locator>",
    "Knowledge-graph output files in standardized format (RDF triples or equivalent)": "<locator>",
    "Spectral library matches and molecular network visualization outputs": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
