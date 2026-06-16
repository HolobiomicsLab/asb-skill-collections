# Workflow Challenge: `coll_nextflow4msdial_workflow`


> Nextflow4MS-DIAL is a reproducible Nextflow workflow for processing LC-HRMS metabolomics data through a containerized MS-DIAL to MSFLO pipeline, with support for Docker and Singularity container backends.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The Nextflow4MS-DIAL workflow implements a containerized sequential pipeline that processes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO. The workflow is designed to support multiple container execution mechanisms: Docker-based container execution for standard environments and Singularity-based container execution for high-performance computing environments. This containerized approach enables reproducible metabolomics data processing across different computational infrastructures.

## Research questions

- What is the sequential pipeline architecture of the containerized MS-DIAL to MSFLO workflow, and how does it process .mzML input files within Nextflow?
- Does the Nextflow4MS-DIAL workflow execute successfully using Docker containerization on publicly available .mzML LC-MS metabolomics data?
- Does the Nextflow4MS-DIAL workflow successfully execute on a Singularity container backend with public LC-MS .mzML data?

## Methods overview

Select containerization backend (Docker or Singularity) based on target compute environment. Load and validate .mzML input files in Nextflow execution context. Execute MS-DIAL in containerized environment to detect peaks and identify features. Stream MS-DIAL outputs into MSFLO module running in same container orchestration. Collect and export final MSFLO processed feature table and annotation artifacts. Validation: Verify MSFLO output files exist and contain expected feature annotations. Verify Nextflow ≥22.10.0 installation and clone the Nextflow4MS-DIAL repository Obtain a public .mzML LC-MS metabolomics dataset and configure workflow input parameters Enable Docker container backend and configure containerized MS-DIAL and MSFLO environment Execute the Nextflow workflow pipeline, processing .mzML data through MS-DIAL feature detection and alignment, then MSFLO post-processing Monitor execution logs and validate that workflow completes without error and produces expected output files (feature tables, aligned matrices, annotations) Validation: Nextflow exits with status code 0, all pipeline stages report completion, and output directory contains non-empty feature table and annotation files matching expected schema Clone the Nextflow4MS-DIAL repository from the public GitHub source. Verify Nextflow ≥22.10.0 installation and Singularity container runtime availability. Obtain or select a public .mzML LC-MS metabolomics dataset from a public repository (MetaboLights, MassIVE, PRIDE). Configure Nextflow workflow profile to use Singularity as the container executor backend. Execute the MS-DIAL → MSFLO containerized processing pipeline on the input .mzML data via nextflow run. Validation: Confirm workflow completion via execution report, verify presence of MS-DIAL feature tables and MSFLO output files, and check that no fatal errors or task failures are reported in the Nextflow log.

**Domain:** metabolomics

**Techniques:** feature-detection, metabolite-identification, spectral-library-matching, database-annotation, quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Nextflow4MS-DIAL is a reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL. _[grounded: sys_nextflow4ms_dial]_
- **(finding)** Nextflow version 22.10.0 or greater is required. _[grounded: tool_nextflow]_
- **(finding)** The workflow enables processing of .mzML LC-MS metabolomics data with MS-DIAL. _[grounded: tool_ms_dial]_
- **(finding)** Both Docker and Singularity containerization are supported by the workflow. _[grounded: tool_docker]_
- **(finding)** The workflow processes .mzML data through MS-DIAL to MSFLO. _[grounded: tool_ms_dial]_
- **(finding)** Nextflow4MS-DIAL adheres to Semantic Versioning. _[grounded: sys_nextflow4ms_dial]_
- **(finding)** The changelog format is based on Keep a Changelog.

## Steps

### Step `task_001`
- Title: Reconstruct the MS-DIAL to MSFLO containerized processing pipeline for .mzML LC-MS metabolomics data
- Task kind: `component_reconstruction`
- Task: Reconstruct and containerize the MS-DIAL → MSFLO sequential processing pipeline as a fixed Nextflow workflow architecture that accepts .mzML LC-MS metabolomics input files and produces MSFLO output artifacts, supporting both Docker and Singularity execution environments.
- Inputs:
  - .mzML LC-MS metabolomics data files
- Expected outputs:
  - MSFLO-processed metabolomics feature table and annotations
- Tools: Nextflow ≥22.10.0, MS-DIAL, MSFLO, Docker, Singularity
- Landmark output files: nextflow.config, main.nf, ms_dial_peaks.txt, msflo_features.csv

### Step `task_002`
- Depends on: `task_001`
- Title: Implement Docker-based container execution of the Nextflow4MS-DIAL workflow on a sample .mzML dataset
- Task kind: `component_reconstruction`
- Task: Configure and execute the Nextflow4MS-DIAL workflow using Docker containerization on a publicly available .mzML LC-MS dataset, verifying successful workflow completion and presence of expected output files.
- Inputs:
  - Public .mzML LC-MS metabolomics dataset (e.g., from MassIVE, MetaboLights, or GitHub test data)
  - Nextflow4MS-DIAL source code repository and configuration files
- Expected outputs:
  - Workflow execution log confirming all stages completed without error
  - MS-DIAL processed feature table and aligned LC-HRMS data matrices
  - MSFLO annotation and summary output files
- Tools: Nextflow ≥22.10.0, Nextflow, MS-DIAL, Docker, MSFLO
- Landmark output files: workflow_config.nf, ms-dial_feature_table.csv, aligned_features_msflo.csv, msflo_annotations.txt
- Primary expected artifact: `nextflow_execution_log.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement Singularity-based container execution of the Nextflow4MS-DIAL workflow for HPC environments
- Task kind: `component_reconstruction`
- Task: Configure and execute the Nextflow4MS-DIAL workflow using Singularity container backend on a publicly available .mzML LC-MS metabolomics dataset, verifying successful completion and presence of expected MS-DIAL and MSFLO output files.
- Inputs:
  - Public .mzML LC-MS metabolomics dataset (e.g. from MetaboLights, MassIVE, or PRIDE accession)
  - Nextflow4MS-DIAL repository source code
- Expected outputs:
  - MS-DIAL processed feature table and metadata files
  - MSFLO-formatted output file(s)
  - Nextflow execution log and completion report
- Tools: Nextflow ≥22.10.0, MS-DIAL, MSFLO, Singularity
- Landmark output files: ms-dial_features.txt, msflo_output.csv, .nextflow.log
- Primary expected artifact: `nextflow_execution_report.html`

## Final expected outputs

- `Workflow execution log confirming all stages completed without error` (type: file, tolerance: hash)
- `MS-DIAL processed feature table and aligned LC-HRMS data matrices` (type: file, tolerance: hash)
- `MSFLO annotation and summary output files` (type: file, tolerance: hash)
- `MS-DIAL processed feature table and metadata files` (type: file, tolerance: hash)
- `MSFLO-formatted output file(s)` (type: file, tolerance: hash)
- `Nextflow execution log and completion report` (type: file, tolerance: hash)

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

- **Abstraction level:** concrete

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
  "workflow_id": "coll_nextflow4msdial_workflow",
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
    "Workflow execution log confirming all stages completed without error": "<locator>",
    "MS-DIAL processed feature table and aligned LC-HRMS data matrices": "<locator>",
    "MSFLO annotation and summary output files": "<locator>",
    "MS-DIAL processed feature table and metadata files": "<locator>",
    "MSFLO-formatted output file(s)": "<locator>",
    "Nextflow execution log and completion report": "<locator>"
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
