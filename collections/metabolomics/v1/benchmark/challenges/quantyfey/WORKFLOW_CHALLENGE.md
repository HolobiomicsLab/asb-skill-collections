# Workflow Challenge: `coll_quantyfey_workflow`


> QuantyFey is a Shiny application for visualization, analysis, and quantification of mass spectrometry data using external calibration, designed to address intensity drifts through multiple correction strategies.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

QuantyFey implements an external calibration quantification module for mass spectrometry data and incorporates multiple correction strategies to address intensity drifts in MS datasets. The application integrates these mechanisms within a Shiny-based pipeline to enable accurate quantification of mass spectrometry data. QuantyFey is currently restricted to Windows operating systems; cross-platform deployment to Linux and macOS would require resolution of unidentified platform-specific dependencies.

## Research questions

- How does QuantyFey implement external calibration to convert raw mass spectrometry intensity measurements into quantified concentration values?
- What correction strategies does QuantyFey implement to address intensity drifts in mass spectrometry datasets?
- What platform-specific dependencies currently prevent QuantyFey from running on Linux or macOS?

## Methods overview

Load and parse raw MS intensity data and calibration standard reference data Fit a regression model (linear or polynomial) relating MS intensity to known standard concentrations Evaluate model fit quality using R² and residual diagnostics Apply the calibration model to convert raw sample intensities to quantified concentrations Validation: Calibration model R² ≥ 0.99 and prediction residuals within acceptable range for quantitative accuracy Load raw MS intensity table into QuantyFey Shiny interface Inspect and diagnose intensity drift patterns in the dataset Select appropriate drift correction strategy from QuantyFey's available methods Apply correction algorithm to remove or mitigate intensity drift artifacts Validation: Corrected intensity table exhibits reduced drift while preserving quantitative relationships and peak identity Retrieve and parse the QuantyFey source code from the CDLMarkus/QuantyFey repository. Perform static code analysis to identify Windows-only dependencies, hard-coded file paths, and platform-conditional logic. Document all identified incompatibilities with OS context and severity level. Refactor configuration and application code to use platform-agnostic patterns (file.path, Sys.info(), conditional package loading). Validation: Modified application launches without errors on a Linux or macOS test environment and produces a compatibility report with zero unresolved critical dependencies.

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry data using external calibration. _[grounded: sys_quantyfey]_
- **(finding)** QuantyFey is specifically designed to address intensity drifts in datasets. _[grounded: sys_quantyfey]_
- **(finding)** QuantyFey offers multiple correction strategies to ensure accurate quantification. _[grounded: sys_quantyfey]_
- **(finding)** QuantyFey is compatible with Windows operating systems only. _[grounded: sys_quantyfey]_

## Steps

### Step `task_001`
- Title: Implement the External Calibration quantification module for MS data in QuantyFey
- Task kind: `component_reconstruction`
- Task: Implement the external calibration component of QuantyFey that converts raw MS intensity data into quantified concentration outputs using calibration curves. Produce a calibration model and apply it to generate concentration predictions.
- Inputs:
  - Raw MS intensity data with sample identifiers and measured ion intensities
  - Calibration standard data containing known concentrations and corresponding MS intensities
- Expected outputs:
  - Quantified concentration table with sample identifiers and calculated concentration values
  - Calibration curve parameters (model coefficients and fit metrics)
- Tools: Shiny
- Landmark output files: calibration_standards_processed.csv, calibration_curve_fit.json, calibration_model_metrics.txt
- Primary expected artifact: `quantified_concentrations.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Implement the Intensity Drift Correction module within the QuantyFey pipeline
- Task kind: `component_reconstruction`
- Task: Apply intensity drift correction to a mass spectrometry intensity table using QuantyFey's correction strategies, producing a corrected intensity table suitable for downstream quantification.
- Inputs:
  - Raw MS intensity table with intensity drift artifacts
- Expected outputs:
  - Corrected MS intensity table with drift correction applied
- Tools: Shiny
- Landmark output files: drift_diagnostic_plot.png, correction_strategy_applied.log
- Primary expected artifact: `corrected_intensity_table.csv`

### Step `task_003`
- Title: Extend QuantyFey's Shiny interface to support Linux/macOS deployment
- Task kind: `extension`
- Task: Identify and resolve platform-specific dependencies in the QuantyFey Shiny application to enable cross-platform execution on Linux or macOS. Produce a modified app configuration and dependency resolution report documenting required changes.
- Inputs:
  - QuantyFey source code repository (CDLMarkus/QuantyFey)
- Expected outputs:
  - Modified Shiny application configuration files with platform-agnostic code
  - Platform dependency resolution and compatibility report
  - Test log confirming successful application launch on Linux or macOS
- Tools: Shiny
- Landmark output files: dependency_audit.txt, platform_incompatibilities.csv, modified_app.R, test_log_linux.txt
- Primary expected artifact: `compatibility_report.md`

## Final expected outputs

- `Corrected MS intensity table with drift correction applied` (type: file, tolerance: hash)
- `Modified Shiny application configuration files with platform-agnostic code` (type: file, tolerance: hash)
- `Platform dependency resolution and compatibility report` (type: file, tolerance: hash)
- `Test log confirming successful application launch on Linux or macOS` (type: file, tolerance: hash)

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
  "workflow_id": "coll_quantyfey_workflow",
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
    "Corrected MS intensity table with drift correction applied": "<locator>",
    "Modified Shiny application configuration files with platform-agnostic code": "<locator>",
    "Platform dependency resolution and compatibility report": "<locator>",
    "Test log confirming successful application launch on Linux or macOS": "<locator>"
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
