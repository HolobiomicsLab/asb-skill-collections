# Workflow Challenge: `coll_cosmic_workflow`


> SIRIUS is a Java-based software framework for LC-MS/MS metabolite analysis that integrates multiple web service components including CSI:FingerID, CANOPUS, and MSNovelist. The paper documents the framework architecture and confirms that the Build and Publish CI workflow for the SIRIUS release branch executes successfully.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 1 reported result: The Build and Publish workflow for sirius-ms/sirius is configured to run on the release branch and is accessible via a status badge in the README. Reconstructs 4 described mechanisms (described in the paper but not separately evaluated there): SIRIUS is implemented as a Java-based software framework designed to accept LC-MS/MS data as input for downstream analysis. CSI:FingerID is a SIRIUS web service component that processes spectrum queries as part of the integrated LC-MS/MS analysis framework. CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation. MSNovelist is offered as a web service component within the SIRIUS framework alongside CSI:FingerID and CANOPUS for scientific analysis.

## Research questions

- How does SIRIUS ingest and parse LC-MS/MS data into a structured representation within its Java framework?
- How does the CSI:FingerID web service accept a parsed mass spectrum query and return a molecular fingerprint prediction?
- What is the mechanism by which CANOPUS accepts a fingerprint or spectrum query and returns a structured compound-class annotation result?
- How does the MSNovelist web service endpoint accept a query input and return de-novo generated candidate structures?
- Does the GitHub Actions 'Build and Publish' workflow on the release branch of the sirius-ms/sirius repository execute successfully and produce a passing build status?

## Methods overview

Load raw LC-MS/MS data files into SIRIUS Java framework Parse and extract spectral metadata (precursor m/z, retention time, collision energy, fragment assignments) Construct hierarchical spectrum objects with indexed MS1 and MS/MS data Validate spectral quality (non-zero ion counts, valid mass ranges, metadata completeness) Validation: All input spectra successfully parsed with no missing mandatory metadata fields and ion counts verified as non-zero Prepare MS/MS spectrum metadata and fragment peak list Format spectrum query according to CSI:FingerID API specification Submit HTTP POST request to CSI:FingerID web service endpoint Parse JSON response to extract fingerprint prediction and confidence metrics Validation: Verify response JSON contains fingerprint prediction data with non-empty bit vector or scored features Prepare fingerprint or spectrum input in CANOPUS-compatible format Submit query to CANOPUS web service endpoint Retrieve structured compound-class annotation response Parse and validate annotation fields (class, confidence) Validation: Response contains predicted compound class and confidence score fields Format query with molecular m/z and optional MS/MS spectrum data Submit query to MSNovelist web service REST endpoint Retrieve and parse JSON response containing ranked candidate structures Serialize candidates with scores and metadata to output file Validation: Verify that output file contains at least one ranked candidate structure with valid SMILES notation and associated score Access the sirius-ms/sirius repository via GitHub and locate the release branch. Review the distribute.yaml workflow configuration to identify build triggers and pipeline stages. Trigger the workflow by creating a release tag or pushing to the release branch according to distribute.yaml trigger conditions. Monitor the GitHub Actions interface until the workflow run completes. Validation: Confirm the workflow run status displays 'passed' and the README build badge shows a passing status indicator (green badge with 'passing' or 'success' label).

**Domain:** cheminformatics

**Techniques:** in-silico-fragmentation, machine-learning, metabolite-identification, deep-learning, database-annotation, high-resolution-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** SIRIUS is licensed under AGPL v3. _[grounded: sirius_system]_
- **(finding)** The current version of SIRIUS is 6.3.7. _[grounded: sirius_system]_
- **(finding)** SIRIUS is a java-based software framework. _[grounded: sirius_system]_
- **(finding)** SIRIUS is used for the analysis of LC-MS/MS data of metabolites. _[grounded: sirius_system]_
- **(finding)** SIRIUS methods are offered to the scientific community as freely available resources. _[grounded: sirius_system]_
- **(finding)** Redistribution of SIRIUS methods in whole or in part for commercial purposes is prohibited. _[grounded: sirius_system]_
- **(finding)** SIRIUS web services are hosted by the Böcker group. _[grounded: sirius_system]_
- **(finding)** SIRIUS web services are for academic research and education use only. _[grounded: sirius_system]_
- **(finding)** CSI:FingerID is one of the SIRIUS web services. _[grounded: sirius_system]_
- **(finding)** CANOPUS is one of the SIRIUS web services. _[grounded: sirius_system]_
- **(finding)** MSNovelist is one of the SIRIUS web services. _[grounded: sirius_system]_
- **(finding)** Bright Giant GmbH provides licenses and services for non-academic SIRIUS users. _[grounded: sirius_system]_
- **(finding)** Users of SIRIUS tools are asked to cite corresponding papers in resulting publications. _[grounded: sirius_system]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Commercial redistribution of methods is prohibited

## Steps

### Step `task_001`
- Title: Reconstruct the LC-MS/MS metabolite analysis pipeline entry point in SIRIUS
- Task kind: `component_reconstruction`
- Task: Ingest LC-MS/MS spectral data into the SIRIUS Java framework and produce a parsed, structured representation of input spectra suitable for downstream analysis. Output the loaded and validated spectral data object(s) in SIRIUS-native format.
- Inputs:
  - Raw LC-MS/MS data file(s) in mzML, mzXML, or vendor instrument format
- Expected outputs:
  - Parsed and structured spectral data representation in SIRIUS-native format with validated MS1 and MS/MS hierarchies
- Tools: SIRIUS

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the CSI:FingerID web-service dispatch for molecular fingerprint prediction
- Task kind: `component_reconstruction`
- Task: Submit a parsed spectrum query (with precursor m/z, ionization mode, and MS/MS fragment peaks) to the CSI:FingerID web service endpoint and retrieve the molecular fingerprint prediction response.
- Inputs:
  - Parsed MS/MS spectrum data (precursor m/z, ionization mode, fragment peak list with m/z and intensity)
- Expected outputs:
  - Molecular fingerprint prediction response from CSI:FingerID web service (structured JSON or table format containing fingerprint bits and confidence scores)
- Tools: CSI:FingerID, SIRIUS
- Landmark output files: spectrum_request_payload.json, csi_fingerid_response.json
- Primary expected artifact: `fingerprint_prediction.json`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the CANOPUS web-service dispatch for compound class prediction
- Task kind: `component_reconstruction`
- Task: Submit a molecular fingerprint or spectrum query to the CANOPUS web service and retrieve the structured compound-class annotation result.
- Inputs:
  - Molecular fingerprint or MS/MS spectrum (in format accepted by CANOPUS web service)
- Expected outputs:
  - Structured compound-class annotation result from CANOPUS (JSON or tabular format containing predicted classes and confidence scores)
- Tools: SIRIUS, CANOPUS
- Primary expected artifact: `canopus_annotation_result.json`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the MSNovelist web-service dispatch for de-novo structure generation
- Task kind: `component_reconstruction`
- Task: Submit a molecular feature query to the MSNovelist web service and retrieve a structured set of de-novo generated candidate structures.
- Inputs:
  - Molecular ion mass (monoisotopic m/z) and optional MS/MS fragmentation spectrum
- Expected outputs:
  - Structured file containing ranked list of de-novo generated candidate structures with scores and metadata
- Tools: SIRIUS, MSNovelist
- Landmark output files: query_payload.json, msnovelist_response.json
- Primary expected artifact: `msnovelist_candidates.json`

### Step `task_005`
- Depends on: `task_001`
- Title: Reproduce the Build and Publish CI workflow execution status for the SIRIUS release branch
- Task kind: `reproduction`
- Task: Trigger the GitHub Actions 'Build and Publish' workflow (distribute.yaml) on the release branch of sirius-ms/sirius and verify that the build completes successfully and the repository README displays a passing build badge.
- Inputs:
  - sirius-ms/sirius GitHub repository URL and access credentials
- Expected outputs:
  - Screenshot or JSON report of GitHub Actions workflow run showing passing status
  - README badge screenshot or URL confirming build badge displays passing status
- Tools: SIRIUS, GitHub Actions
- Landmark output files: distribute.yaml, workflow_run_logs.txt, readme_badge.png
- Primary expected artifact: `workflow_run_status.json`

## Final expected outputs

- `Structured compound-class annotation result from CANOPUS (JSON or tabular format containing predicted classes and confidence scores)` (type: file, tolerance: hash)
- `Structured file containing ranked list of de-novo generated candidate structures with scores and metadata` (type: file, tolerance: hash)
- `Screenshot or JSON report of GitHub Actions workflow run showing passing status` (type: file, tolerance: hash)
- `README badge screenshot or URL confirming build badge displays passing status` (type: file, tolerance: hash)

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

- **Orchestration planning:** dynamic

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
  "workflow_id": "coll_cosmic_workflow",
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
    "Structured compound-class annotation result from CANOPUS (JSON or tabular format containing predicted classes and confidence scores)": "<locator>",
    "Structured file containing ranked list of de-novo generated candidate structures with scores and metadata": "<locator>",
    "Screenshot or JSON report of GitHub Actions workflow run showing passing status": "<locator>",
    "README badge screenshot or URL confirming build badge displays passing status": "<locator>"
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
