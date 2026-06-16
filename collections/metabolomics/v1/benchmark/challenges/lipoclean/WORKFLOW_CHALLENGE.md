# Workflow Challenge: `coll_lipoclean_workflow`


> LipoCLEAN is a command-line tool that filters lipid identifications from MS-DIAL through configuration via TOML-formatted options files. The tool supports MS-DIAL versions 4 and 5, with version-specific default configuration templates that can be generated and customized.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

LipoCLEAN accepts all configuration options, including MS-DIAL export file locations, through a TOML-formatted text file. Version-specific default configuration files can be generated for MS-DIAL 4 or MS-DIAL 5 using the `--print MSD4` or `--print MSD5` command-line arguments, which create an `options.txt` file that users can subsequently edit. The tool can be installed and run as an executable, a Python package, or a Docker container.

## Research questions

- How does the LipoCLEAN command-line tool accept configuration input and what file format is required to specify MS-DIAL export locations?
- How does the LipoCLEAN CLI generate default configuration files for different MS-DIAL versions?

## Methods overview

Prepare TOML configuration file with LipoCLEAN options, specifying MS-DIAL version and input dataset path. Invoke LipoCLEAN command-line interface with the TOML configuration as the primary argument. Capture tool output and error streams to verify successful execution. Validation: Confirm tool exits with status code 0, output file exists and contains quality-scored lipid identifications in the expected tabular format. Invoke LipoCLEAN CLI with `--print MSD4` or `--print MSD5` flag to retrieve default configuration for the target MS-DIAL version Capture or redirect the generated TOML-formatted options output to options.txt file Validation: Confirm that options.txt file exists and contains valid TOML syntax with all expected configuration keys for the specified MS-DIAL version

**Domain:** lipidomics

**Techniques:** machine-learning, quality-control, metabolite-identification

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** LipoCLEAN is a command line tool. _[grounded: lipoclean_system]_
- **(finding)** Usage instructions for LipoCLEAN can be obtained using the `--help` flag. _[grounded: lipoclean_system]_
- **(finding)** LipoCLEAN options are given to the tool in a TOML formatted text file. _[grounded: lipoclean_system]_
- **(finding)** Default options files for MS-DIAL 4 can be obtained using the `--print MSD4` command line argument. _[grounded: msdial_tool]_
- **(finding)** Default options files for MS-DIAL 5 can be obtained using the `--print MSD5` command line argument. _[grounded: msdial_tool]_
- **(finding)** The default options file created by LipoCLEAN is named `options.txt` and can be edited. _[grounded: lipoclean_system]_
- **(finding)** LipoCLEAN can be installed and run as an executable. _[grounded: lipoclean_system]_
- **(finding)** LipoCLEAN can be installed and run as a Python package. _[grounded: lipoclean_system]_
- **(finding)** LipoCLEAN can be installed and run as a Docker container. _[grounded: lipoclean_system]_
- **(finding)** LipoCLEAN is a machine learning based quality filter for lipid identifications from MS-DIAL. _[grounded: lipoclean_system]_

## Steps

### Step `task_001`
- Title: Reconstruct LipoCLEAN CLI invocation using a TOML options file to filter MS-DIAL lipid identifications
- Task kind: `component_reconstruction`
- Task: Run the LipoCLEAN command-line tool with a TOML-formatted configuration file pointing to an MS-DIAL export, and verify that the tool executes successfully and produces filtered lipid identification output.
- Inputs:
  - MS-DIAL lipid identification export file (CSV or tabular format)
  - TOML-formatted options file with LipoCLEAN configuration parameters
- Expected outputs:
  - Filtered lipid identification table with quality-assessed lipid assignments
- Tools: LipoCLEAN, MS-DIAL
- Landmark output files: toml_config_prepared.toml, lipoclean_execution.log
- Primary expected artifact: `filtered_lipids.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct generation of a default TOML options file for MS-DIAL 4 or MS-DIAL 5 via LipoCLEAN --print argument
- Task kind: `component_reconstruction`
- Task: Run the LipoCLEAN CLI with either `--print MSD4` or `--print MSD5` flag to generate a default configuration file (options.txt) and verify that the output file is created with all expected configuration keys.
- Inputs:
  - LipoCLEAN CLI tool (from stavis1/LipoCLEAN repository or installed executable/Docker container)
  - Target MS-DIAL version (4 or 5)
- Expected outputs:
  - options.txt file in TOML format containing default configuration keys for the specified MS-DIAL version
- Tools: LipoCLEAN
- Primary expected artifact: `options.txt`

## Final expected outputs

- `options.txt file in TOML format containing default configuration keys for the specified MS-DIAL version` (type: file, tolerance: hash)

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
  "workflow_id": "coll_lipoclean_workflow",
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
    "options.txt file in TOML format containing default configuration keys for the specified MS-DIAL version": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
