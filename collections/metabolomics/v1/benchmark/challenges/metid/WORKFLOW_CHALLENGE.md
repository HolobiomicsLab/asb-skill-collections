# Workflow Challenge: `coll_metid_workflow`


> Met-ID automates metabolite identification in mass spectrometry imaging by handling derivatizing matrices that produce non-standard ions. The software is designed with extensibility to support any derivatizing matrix beyond the in-house FMP-10 reagent.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Met-ID addresses the challenge of automating metabolite identification in mass spectrometry imaging, a task traditionally performed manually by experts. The software is designed to handle derivatizing matrices such as FMP-10 that produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode. A key design feature is the extensibility of Met-ID to support any derivatizing matrix, not limited to FMP-10. The repository maintains an automated CI pipeline tracked via GitHub Actions, as indicated by the workflow badge linked to main.yml.

## Research questions

- How does Met-ID compute expected adduct ions for metabolites when using derivatizing matrices like FMP-10, beyond the standard [M+H]+ and [M-H]- ions?
- Does the Met-ID GitHub repository's CI workflow (main.yml) execute successfully and pass all automated checks as indicated by the badge?
- Is Met-ID extensible to register and apply derivatizing matrices beyond FMP-10 to produce correct adduct annotations?

## Methods overview

Load and validate metabolite SMILES string; parse matrix identifier to retrieve or initialize adduct ionization ruleset. Construct molecular graph using RDKit; calculate exact molecular weight of the unmodified metabolite. For each matrix-specific adduct rule, compute the expected m/z by adding matrix mass and applying charge state (proton gain/loss). Compile predicted adduct table with ion formula, mass shift, m/z, and charge state. Validation: Compare predicted adduct m/z values against reference FMP-10 dataset; accept predictions with mass error ≤5 ppm (or as specified in Nature Methods reference). Clone the Met-ID repository from GitHub to a local or remote environment. Extract and parse the main.yml workflow definition to identify test commands, dependencies, and environment configuration. Install required dependencies (including RDKit and any Python packages listed in requirements files). Execute the test suite and CI commands as defined in the workflow, capturing all output and exit codes. Compare the observed pass/fail status with the badge-reported status to confirm reproducibility. Validation: Workflow execution completes with exit code 0 (success) and matches the badge-reported passing state, or documents the specific failure point if reproducibility is not achieved. Review Met-ID's extensibility architecture and existing derivatizing matrix configuration interface Define and implement configuration for a second derivatizing matrix using specifications or documentation Register the new matrix in Met-ID's configuration loader or plugin system Execute Met-ID on test metabolites using the newly registered matrix Validate predicted adducts against expected ground truth or literature values Validation: adduct annotations produced by Met-ID with the new matrix match expected ions for ≥90% of test metabolites

**Domain:** metabolomics

**Techniques:** metabolite-identification, database-annotation, in-silico-fragmentation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Metabolite identification in Mass Spectrometry Imaging is currently done manually by experts. _[grounded: msi-tool]_
- **(finding)** Manual metabolite identification is not feasible in high throughput studies.
- **(finding)** Met-ID has been developed to automate metabolite identification in Mass Spectrometry Imaging. _[grounded: met-id-system]_
- **(finding)** Met-ID focuses on derivatizing matrices leading to ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode. _[grounded: met-id-system]_
- **(finding)** FMP-10 was developed in house. _[grounded: fmp10-component]_
- **(finding)** FMP-10 features heavily in the Met-ID software. _[grounded: met-id-system]_
- **(finding)** Met-ID is extendable to use any derivatizing matrix. _[grounded: met-id-system]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Met-ID is extendable to use any derivatizing matrix, with FMP-10 featured heavily as a starting point example

## Steps

### Step `task_001`
- Title: Reconstruct the derivatizing-matrix ion adduct enumeration module in Met-ID
- Task kind: `component_reconstruction`
- Task: Implement an adduct ion prediction module that, given a derivatizing matrix identifier (e.g., FMP-10) and a metabolite SMILES string, computes expected adduct masses beyond the common [M+H]+ and [M-H]- ions. Return predicted adduct m/z values and ion formulas as a structured output.
- Inputs:
  - Metabolite SMILES string and derivatizing matrix identifier (e.g., FMP-10)
  - Reference FMP-10 adduct mass dataset from Nature Methods paper
- Expected outputs:
  - Predicted adduct ions table with adduct formula, mass shift, m/z value, and ionization state
  - Validation report comparing predicted adduct masses to reference FMP-10 values
- Tools: RDKit
- Landmark output files: matrix_ruleset_loaded.json, molecules_parsed.tsv, predicted_adducts.csv
- Primary expected artifact: `predicted_adducts.csv`

### Step `task_002`
- Title: Reproduce the CI build passing status for the Met-ID GitHub Actions workflow
- Task kind: `reproduction`
- Task: Clone the Met-ID repository and execute the GitHub Actions CI workflow (main.yml) to verify that the reported passing badge status is reproducible locally or via workflow simulation.
- Inputs:
  - GitHub repository URL: https://github.com/pbjarterot/Met-ID
- Expected outputs:
  - CI workflow execution log (stdout/stderr) with pass/fail status and test results
  - Verification report (text or JSON) documenting workflow completion status and badge reproducibility
- Tools: git, GitHub Actions, RDKit
- Landmark output files: main.yml, ci_workflow_output.log, test_results.txt
- Primary expected artifact: `ci_verification_report.json`

### Step `task_003`
- Depends on: `task_001`
- Title: Extend Met-ID to register a novel derivatizing matrix beyond FMP-10
- Task kind: `extension`
- Task: Implement a configuration or plugin to register a second derivatizing matrix (e.g. TAHS) in Met-ID and verify that the system correctly recognizes and applies it to generate adduct annotations for test metabolites.
- Inputs:
  - Met-ID source code or installed package with extensibility interface
  - Documentation or specifications for the second derivatizing matrix (e.g. TAHS reagent properties and ionization modes)
  - Test metabolite dataset with known or reference adduct forms under derivatization
- Expected outputs:
  - Configuration file or plugin code for the second derivatizing matrix (e.g. tahs_config.json or tahs_plugin.py)
  - Adduct annotation table or report (CSV or JSON) produced by Met-ID using the newly registered matrix on test metabolites
  - Verification report or summary table comparing predicted adducts to expected ground truth
- Tools: RDKit
- Landmark output files: matrix_config.json, adduct_predictions.csv, verification_report.csv
- Primary expected artifact: `verification_report.csv`

## Final expected outputs

- `CI workflow execution log (stdout/stderr) with pass/fail status and test results` (type: file, tolerance: hash)
- `Verification report (text or JSON) documenting workflow completion status and badge reproducibility` (type: file, tolerance: hash)
- `Configuration file or plugin code for the second derivatizing matrix (e.g. tahs_config.json or tahs_plugin.py)` (type: file, tolerance: hash)
- `Adduct annotation table or report (CSV or JSON) produced by Met-ID using the newly registered matrix on test metabolites` (type: file, tolerance: hash)
- `Verification report or summary table comparing predicted adducts to expected ground truth` (type: file, tolerance: hash)

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
  "workflow_id": "coll_metid_workflow",
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
    "CI workflow execution log (stdout/stderr) with pass/fail status and test results": "<locator>",
    "Verification report (text or JSON) documenting workflow completion status and badge reproducibility": "<locator>",
    "Configuration file or plugin code for the second derivatizing matrix (e.g. tahs_config.json or tahs_plugin.py)": "<locator>",
    "Adduct annotation table or report (CSV or JSON) produced by Met-ID using the newly registered matrix on test metabolites": "<locator>",
    "Verification report or summary table comparing predicted adducts to expected ground truth": "<locator>"
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
