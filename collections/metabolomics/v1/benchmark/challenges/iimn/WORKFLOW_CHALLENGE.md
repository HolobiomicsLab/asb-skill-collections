# Workflow Challenge: `coll_iimn_workflow`


> mzmine is an open-source mass spectrometry data processing software designed to provide a user-friendly and extensible platform for the complete MS analysis workflow. The project includes CI/CD automation via GitHub Actions and supports multiple chromatography and imaging modalities.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

mzmine is an open-source software for mass spectrometry data processing that aims to provide a flexible and easily extendable platform covering the entire MS data analysis workflow. The software supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), and MS imaging modalities (e.g., MALDI) across most MS instruments. The project maintains a Development Build Release GitHub Actions workflow (dev_build_release.yml) for continuous integration and delivery, and is built on JDK version 25 and JavaFX version 24.

## Research questions

- How does mzmine route input mass spectrometry data to the appropriate processing module based on the declared data type?
- Does the mzmine GitHub Actions workflow 'dev_build_release.yml' successfully complete and produce a passing build artifact?

## Methods overview

Clone or inspect the mzmine GitHub repository to locate the main entry point and module initialization code. Identify the data-type classification system (enum, interface, or metadata field) used to label input as LC, GC, IMS, or MS Imaging. Trace conditional branching logic (if/switch statements, factory methods, or service registries) that maps each data type to its processing module. Extract dispatch conditions, parameter validation checks, and fallback or error-handling behavior. Synthesize the routing logic as a control-flow diagram, decision tree, or pseudocode with all pathways and triggering criteria. Validation: Verify that the reconstructed routing logic accounts for all four supported data types (LC, GC, IMS, MS Imaging) and correctly documents the dispatch conditions reported in mzmine documentation. Access mzmine/mzmine GitHub repository and identify dev_build_release.yml workflow Trigger the workflow via GitHub Actions API with specified branch reference Poll GitHub Actions API for workflow run status until completion Retrieve and parse build logs to confirm successful compilation Download build artifact(s) and verify file integrity and completeness Validation: Workflow status is 'success', build logs contain no fatal errors, and artifact files are present and accessible for download

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** mzmine is an open-source software for mass spectrometry data processing. _[grounded: mzmine_system]_
- **(finding)** mzmine aims to provide a user-friendly, flexible and easily extendable software. _[grounded: mzmine_system]_
- **(finding)** mzmine provides a complete set of modules covering the entire MS data analysis workflow. _[grounded: mzmine_system]_
- **(finding)** mzmine supports liquid chromatography (LC). _[grounded: mzmine_system]_
- **(finding)** mzmine supports gas chromatography (GC). _[grounded: mzmine_system]_
- **(finding)** mzmine supports ion mobility spectrometry (IMS). _[grounded: mzmine_system]_
- **(finding)** mzmine supports MS imaging such as MALDI. _[grounded: mzmine_system]_
- **(finding)** mzmine supports most MS instruments. _[grounded: mzmine_system]_
- **(finding)** The project is written using JDK version 25.
- **(finding)** The project uses JavaFX version 24. _[grounded: tool_javafx]_

## Steps

### Step `task_001`
- Title: Reconstruct the module dispatch routing for LC, GC, IMS, and MS Imaging input types in mzmine
- Task kind: `component_reconstruction`
- Task: Reconstruct the conditional routing logic that dispatches mass spectrometry input data to the appropriate processing module (LC Support, GC Support, IMS Support, or MS Imaging Support) based on declared data type, as defined in the mzmine architecture. Document the dispatch mechanism and decision criteria as a structured control flow.
- Inputs:
  - mzmine source code repository (github.com/mzmine/mzmine)
- Expected outputs:
  - Control-flow diagram or pseudocode documenting the conditional routing logic for LC, GC, IMS, and MS Imaging module dispatch
  - Data-type classification schema and dispatch decision criteria
- Tools: mzmine, JDK 25, JavaFX 24
- Landmark output files: module_dispatch_code_excerpt.java, data_type_enum.java, routing_control_flow.txt
- Primary expected artifact: `routing_dispatch_logic.md`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the automated development build and release artifact produced by GitHub Actions for mzmine
- Task kind: `reproduction`
- Task: Trigger the GitHub Actions workflow 'dev_build_release.yml' in the public mzmine/mzmine repository and confirm that a passing build artifact is successfully produced.
- Inputs:
  - mzmine/mzmine public GitHub repository URL and branch name (dev or main)
- Expected outputs:
  - GitHub Actions workflow run completion status report (pass/fail) and downloadable build artifact file(s)
  - Build artifact log or summary confirming successful compilation with JDK 25 and JavaFX 24 dependencies
- Tools: mzmine, JDK 25, JavaFX 24
- Landmark output files: workflow_run_log.txt, build_status_report.json
- Primary expected artifact: `mzmine_build_artifact.zip`

## Final expected outputs

- `GitHub Actions workflow run completion status report (pass/fail) and downloadable build artifact file(s)` (type: file, tolerance: hash)
- `Build artifact log or summary confirming successful compilation with JDK 25 and JavaFX 24 dependencies` (type: file, tolerance: hash)

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
  "workflow_id": "coll_iimn_workflow",
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
    "GitHub Actions workflow run completion status report (pass/fail) and downloadable build artifact file(s)": "<locator>",
    "Build artifact log or summary confirming successful compilation with JDK 25 and JavaFX 24 dependencies": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
