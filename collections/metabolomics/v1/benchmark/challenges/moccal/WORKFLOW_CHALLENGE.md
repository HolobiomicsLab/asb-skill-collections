# Workflow Challenge: `coll_moccal_workflow`


> MOCCal is a Python application for analyzing high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry data through collision cross section calibration, biomolecular class assignment, and class-specific CCS calculations without requiring prior feature identification.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MOCCal implements three core mechanisms for TWIM-MS data analysis: (1) a CCS calibration module that transforms arrival-time data into collision cross section values for multi-omic analysis, (2) a biomolecular class assignment module that operates on unidentified features to classify experimental data, and (3) a class-specific CCS calculation module that applies class-appropriate methods to compute CCS values for assigned biomolecular features. The application integrates these components into an end-to-end pipeline capable of processing high-dimensional, multi-omic TWIM-MS datasets.

## Research questions

- How does MOCCal convert raw arrival-time measurements from TWIM-MS into collision cross section (CCS) values through calibration?
- How does MOCCal assign biomolecular class labels to experimental TWIM-MS features without requiring prior feature identification?
- How does MOCCal compute class-specific collision cross section (CCS) values for biomolecular features that have been assigned to experimental classes?
- Can MOCCal successfully execute its complete workflow (CCS calibration, biomolecular class assignment, and class-specific CCS calculations) on a multi-omic TWIM-MS dataset external to its bundled examples?

## Methods overview

Load raw arrival-time measurements and calibration reference template from MOCCal repository Extract known CCS values and corresponding arrival times from calibration reference compounds Construct arrival-time-to-CCS mapping using calibration reference points Apply calibration transform to experimental arrival-time data to compute CCS values Validation: verify that reference compound arrival times map to their known CCS values within expected tolerance Load experimental TWIM-MS data from RawDT or UserDT format containing arrival times and m/z values. Apply MOCCal's biomolecular class-assignment algorithm to classify each feature based on physico-chemical properties. Compile assigned class labels into a tabular format indexed by feature identifier. Validation: Output table contains one row per input feature with no missing class assignments and class labels consistent with MOCCal's supported biomolecular ontology (protein, lipid, metabolite, nucleic acid, or other defined classes). Load feature table containing assigned biomolecular class labels and raw arrival time measurements from TWIM-MS. Stratify features by biomolecular class (e.g., lipid, protein, carbohydrate). Apply class-specific CCS calibration model or coefficients to convert arrival time to CCS for each class stratum. Assemble output table with feature identifiers, class labels, and calibrated CCS values. Validation: Output CCS table contains all input features with valid numeric CCS values and class label match. Load multi-omic TWIM-MS raw data from a public repository in the format expected by MOCCal. Apply CCS calibration using known reference standards or internal calibrants to establish arrival-time-to-CCS conversion. Perform biomolecular class assignment without requiring prior feature identification. Calculate class-specific CCS values for each assigned biomolecular class. Validation: verify CCS output file exists, contains expected columns (class, CCS, arrival time), and all rows have valid numeric CCS values; confirm execution completed without runtime errors.

**Domain:** metabolomics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MOCCal is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data analysis. _[grounded: MOCCal_system]_
- **(finding)** MOCCal provides functionality for collision cross section (CCS) calibration. _[grounded: MOCCal_system]_
- **(finding)** MOCCal provides functionality for experimental data biomolecular class assignment. _[grounded: MOCCal_system]_
- **(finding)** MOCCal provides functionality for experimental class-specific CCS calculations. _[grounded: MOCCal_system]_
- **(finding)** MOCCal offers class assignment and CCS calculations without needing to identify features first. _[grounded: MOCCal_system]_
- **(finding)** The terms arrival time and drift time are used interchangeably within MOCCal software for convenience. _[grounded: MOCCal_system]_
- **(finding)** TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).

## Steps

### Step `task_001`
- Title: Implement CCS Calibration module for TWIM-MS arrival-time data
- Task kind: `component_reconstruction`
- Task: Apply CCS calibration transform to convert raw TWIM-MS arrival-time values to collision cross section (CCS) values using MOCCal calibration templates and example data from the HinesLab/MOCCal repository.
- Inputs:
  - Raw TWIM-MS arrival-time data (example data from HinesLab/MOCCal repository)
  - CCS calibration reference template with known calibrant compounds and their CCS values
- Expected outputs:
  - Calibrated CCS values table with ion identifiers and corresponding collision cross section measurements
- Tools: Python
- Landmark output files: calibration_reference_map.json, calibrated_ccs.csv
- Primary expected artifact: `calibrated_ccs.csv`

### Step `task_002`
- Title: Implement Biomolecular Class Assignment module operating on unidentified features
- Task kind: `component_reconstruction`
- Task: Assign biomolecular class labels to experimental TWIM-MS features using MOCCal's class-assignment logic without prior feature identification. Produce a table mapping each feature to its assigned class label.
- Inputs:
  - Experimental TWIM-MS data in RawDT or UserDT format (arrival times, m/z values, and associated feature metadata)
- Expected outputs:
  - Table of per-feature class labels with feature identifiers and their assigned biomolecular class
- Tools: Python
- Landmark output files: raw_features.csv, feature_class_assignments.csv
- Primary expected artifact: `feature_class_assignments.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Implement Class-Specific CCS Calculation module using assigned class labels
- Task kind: `component_reconstruction`
- Task: Apply class-specific CCS calculation to biomolecule-labeled features from TWIM-MS data to produce a table of calibrated collision cross section values.
- Inputs:
  - Feature table with biomolecular class labels and arrival time measurements
- Expected outputs:
  - CCS calibration table with feature identifiers, class labels, and computed CCS values
- Tools: Python
- Landmark output files: class_assignment_validated.csv, arrival_time_raw.csv
- Primary expected artifact: `ccs_calibrated_features.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Extend MOCCal pipeline to process a new multi-omic TWIM-MS dataset end-to-end
- Task kind: `extension`
- Task: Execute the complete MOCCal workflow (calibration → class assignment → class-specific CCS calculation) on a publicly deposited multi-omic TWIM-MS dataset to verify the application runs without error and produces a structured CCS output file.
- Inputs:
  - Multi-omic TWIM-MS raw data from a public repository (MassIVE, MetaboLights, or PRIDE accession)
- Expected outputs:
  - Structured CCS output file containing calibrated and class-specific collision cross section values
  - Execution log confirming MOCCal workflow completed without error
- Tools: Python, HinesLab/MOCCal
- Landmark output files: calibration_curve.csv, class_assignments.csv, ccs_calibrated_output.csv
- Primary expected artifact: `ccs_calibrated_output.csv`

## Final expected outputs

- `Calibrated CCS values table with ion identifiers and corresponding collision cross section measurements` (type: file, tolerance: hash)
- `CCS calibration table with feature identifiers, class labels, and computed CCS values` (type: file, tolerance: hash)
- `Structured CCS output file containing calibrated and class-specific collision cross section values` (type: file, tolerance: hash)
- `Execution log confirming MOCCal workflow completed without error` (type: file, tolerance: hash)

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
  "workflow_id": "coll_moccal_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
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
    }
  },
  "final_outputs": {
    "Calibrated CCS values table with ion identifiers and corresponding collision cross section measurements": "<locator>",
    "CCS calibration table with feature identifiers, class labels, and computed CCS values": "<locator>",
    "Structured CCS output file containing calibrated and class-specific collision cross section values": "<locator>",
    "Execution log confirming MOCCal workflow completed without error": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
