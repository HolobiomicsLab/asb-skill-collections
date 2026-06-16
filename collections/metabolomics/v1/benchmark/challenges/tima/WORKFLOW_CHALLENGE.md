# Workflow Challenge: `coll_tima_workflow`


> The tima R package implements a taxonomically informed annotation workflow with automated build validation and containerized deployment.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 2 reported results: The tima package has an active R-CMD-check workflow configured on GitHub that validates the package build and check status. A Docker image for tima is available at the repository adafede/tima-r on Docker Hub. Reconstructs 1 described mechanism (described in the paper but not separately evaluated there): The tima package implements a taxonomically informed annotation workflow that builds on initial work published at https://doi.org/10.3389/fpls.2019.01329, with improvements made since the original publication.

## Research questions

- What is the complete end-to-end workflow architecture of the TIMA (Taxonomically Informed annotation) system as implemented in the tima R package?
- Does the tima R package install successfully from the r-universe repository and pass its R-CMD-check test suite?
- Does the tima Docker container (adafede/tima-r) successfully pull and launch without errors?

## Methods overview

Install tima R package from the official GitHub repository (taxonomicallyinformedannotation/tima) or use Docker image. Load example metabolomics dataset (e.g., mass spectrometry feature table or raw instrument data) into R environment. Execute the canonical tima workflow pipeline as illustrated in package documentation, which integrates spectral matching, chemical similarity, and taxonomic context for metabolite annotation. Generate annotated feature table with metabolite identities, chemical classes, and taxonomic predictions ranked by confidence. Validation: Confirm all workflow stages complete without error, annotated features table contains expected columns (metabolite ID, annotation, confidence score), and output files match example dataset expectations. Configure R environment to recognize the r-universe TIMA repository as a package source Invoke install.packages() targeting the TIMA package from the configured repository Execute library(tima) to load the package into the active R session and capture load status Run R-CMD-check on the installed package to validate structural integrity and test suite compliance Validation: Installation succeeds with exit code 0, package loads without warnings or errors, and R-CMD-check reports all NOTE/WARNING/ERROR categories as zero or explicitly non-blocking Retrieve the TIMA Docker image (adafede/tima-r) from Docker Hub. Instantiate and launch the container. Invoke the tima entry point with a help or version flag to confirm availability and correct operation. Validation: Verify that the container starts without errors and the tima help/version command exits with status code 0 and produces non-empty output.

**Domain:** bioinformatics

**Techniques:** database-annotation, machine-learning, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The tima project's initial work is described in a publication available at https://doi.org/10.3389/fpls.2019.01329. _[grounded: SYS-TIMA]_
- **(finding)** Many improvements have been made to tima since the initial publication. _[grounded: SYS-TIMA]_
- **(finding)** The tima project is in an experimental lifecycle stage. _[grounded: SYS-TIMA]_
- **(finding)** A Docker image for tima is available. _[grounded: SYS-TIMA]_
- **(finding)** The tima package has a Zenodo DOI identifier 10.5281/zenodo.5797920. _[grounded: SYS-TIMA]_

## Steps

### Step `task_001`
- Title: Reconstruct the TIMA annotation workflow as described in the README
- Task kind: `component_reconstruction`
- Task: Install the tima R package (or Docker image) and execute the canonical taxonomically informed annotation workflow against a publicly deposited example dataset to reconstruct the end-to-end TIMA pipeline. Produce annotated output files demonstrating successful workflow execution.
- Inputs:
  - tima R package source code or Docker image
  - Example metabolomics dataset (public repository or local file compatible with tima)
- Expected outputs:
  - Annotated metabolite feature table with taxonomic and chemical annotations
  - Workflow execution log demonstrating successful completion of tima pipeline steps
  - Annotation summary report with metabolite identities and confidence metrics
- Tools: R
- Landmark output files: tima_installation.log, raw_data_loaded.rds, feature_table_processed.csv, spectral_matches.csv, taxonomic_annotations.csv, annotated_features.csv
- Primary expected artifact: `annotated_features.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the tima R package installation and basic execution via r-universe
- Task kind: `reproduction`
- Task: Install the TIMA R package from the r-universe repository and verify successful installation and package integrity by confirming it loads without errors and passes the R-CMD-check suite.
- Inputs:
  - r-universe repository URL for TIMA
- Expected outputs:
  - Installation log confirming successful package installation
  - Package load confirmation with no error messages
  - R-CMD-check report with all tests passing
- Tools: R
- Landmark output files: installation_output.log, package_load_test.Rout
- Primary expected artifact: `cmd_check_results.txt`

### Step `task_003`
- Title: Reproduce the tima Docker image build and smoke-test execution
- Task kind: `reproduction`
- Task: Pull the TIMA Docker image from adafede/tima-r and verify container startup and availability of the tima entry point via a help or version command.
- Inputs:
  - Docker Hub repository URL: https://hub.docker.com/r/adafede/tima-r/
- Expected outputs:
  - Docker image successfully pulled and container launched; tima entry point responds to help or version command with non-error output
- Tools: R
- Landmark output files: docker_pull.log, container_startup.log, tima_entry_point_test.out

## Final expected outputs

- `Installation log confirming successful package installation` (type: file, tolerance: hash)
- `Package load confirmation with no error messages` (type: file, tolerance: hash)
- `R-CMD-check report with all tests passing` (type: file, tolerance: hash)
- `Docker image successfully pulled and container launched; tima entry point responds to help or version command with non-error output` (type: file, tolerance: hash)

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
  "workflow_id": "coll_tima_workflow",
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
    "Installation log confirming successful package installation": "<locator>",
    "Package load confirmation with no error messages": "<locator>",
    "R-CMD-check report with all tests passing": "<locator>",
    "Docker image successfully pulled and container launched; tima entry point responds to help or version command with non-error output": "<locator>"
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
