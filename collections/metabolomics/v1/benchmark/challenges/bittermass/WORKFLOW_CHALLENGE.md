# Workflow Challenge: `coll_bittermass_workflow`


> BitterPredict is a classifier that predicts whether chemical compounds are bitter or not based on their molecular structure descriptors. The paper reports reproduction of the classifier's predictions and analysis of its sensitivity to individual descriptor subsets.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

BitterPredict.m is a MATLAB classifier that accepts CSV or Excel files containing pre-computed chemical structure descriptors as input and produces binary bitter/not-bitter predictions for each molecule. The reported results include successful reproduction of classifier predictions on molecules with known descriptors, and analysis of prediction sensitivity to individual chemical descriptor subsets through systematic ablation studies where descriptor subgroups are manipulated in the input data. The classifier itself operates on descriptors that must be prepared prior to classification, with details on descriptor specification documented within the BitterPredict.m file.

## Research questions

- What is the input format and data structure required for BitterPredict.m to generate bitter/not-bitter predictions for a set of molecules?
- What descriptor input format and preparation workflow is required to convert raw molecular representations into the CSV or Excel files needed for BitterPredict.m classification?
- Which descriptor subgroups have the greatest impact on bitter/not-bitter prediction accuracy when systematically removed from the BitterPredict classifier?

## Methods overview

Load input CSV or Excel file containing pre-computed molecular descriptors. Parse descriptor matrix and validate presence of required features for BitterPredict classifier. Execute BitterPredict.m inference on descriptor vectors. Map predicted class labels to output identifiers and format as CSV. Validation: output CSV contains one prediction per input molecule with binary labels (bitter/not-bitter); file format is valid and parseable. Load and parse raw SMILES or SDF input files into standardized molecular structures. Validate molecular syntax and apply structure standardization (kekulization, aromaticity perception). Calculate all required molecular descriptors (physicochemical and topological properties) from standardized structures. Assemble descriptor values into a table with molecules as rows and descriptors as named columns. Export table to CSV or Excel format matching BitterPredict.m input specification. Validation: Verify output file format (CSV or Excel), confirm presence and naming of all required descriptor columns, and check that all rows contain valid numeric descriptor values with no missing entries. Load descriptor CSV and organize descriptors into functionally coherent subgroups. For each subgroup, create ablated datasets by zeroing that subgroup's values. Run BitterPredict on each ablated dataset to generate predictions. Compare ablated predictions against baseline (full-descriptor) predictions to identify molecules with changed labels. Calculate per-subgroup prediction-change rate as the fraction of molecules with label flips. Validation: Record per-descriptor-group prediction-change rates in a summary table; verify all molecules are accounted for and all descriptor subgroups are represented.

**Domain:** cheminformatics

**Techniques:** machine-learning, quantitative-structure-activity

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** BitterPredict is a classifier that predicts whether a compound is bitter or not based on its chemical structure. _[grounded: SYS_BitterPredict]_
- **(finding)** BitterPredict.m accepts CSV or EXCEL files as input containing required descriptors of molecules. _[grounded: SYS_BitterPredict]_
- **(finding)** BitterPredict.m calculates predictions for whether each molecule is bitter or not. _[grounded: SYS_BitterPredict]_
- **(finding)** BitterPredict is described in a publication authored by Ayana Dagan Wiener, Ido Nissim, Natalie Ben Abu, Gigliola Borgonovo, Angela Bassoli, and Masha Y. Niv. _[grounded: SYS_BitterPredict]_

**Speculative claims (excluded from scoring):**
- **(finding)** The full code for BitterPredict will be available upon publication. _[grounded: SYS_BitterPredict]_

## Steps

### Step `task_001`
- Title: Reproduce BitterPredict classifier predictions on a set of molecules with known chemical structure descriptors
- Task kind: `reproduction`
- Task: Run the BitterPredict classifier on a CSV or Excel file containing molecular descriptors to generate per-molecule binary bitter/not-bitter predictions. Output predictions as a CSV file with molecule identifiers and predicted class labels.
- Inputs:
  - CSV or Excel file with required chemical structure descriptors for molecules
- Expected outputs:
  - CSV file with per-molecule binary bitter/not-bitter predictions
- Tools: BitterPredict
- Landmark output files: descriptor_validation.log, predictions.csv
- Primary expected artifact: `predictions.csv`

### Step `task_002`
- Title: Reconstruct the chemical structure descriptor extraction pipeline feeding BitterPredict
- Task kind: `component_reconstruction`
- Task: Convert raw molecular representations (SMILES or SDF format) into the named descriptor set required by BitterPredict.m, producing a correctly formatted CSV or Excel file with all required molecular descriptors as input for bitter/non-bitter classification.
- Inputs:
  - Raw molecular structures in SMILES or SDF format
- Expected outputs:
  - CSV or Excel file containing molecular descriptors formatted for BitterPredict.m input
- Tools: BitterPredict
- Landmark output files: molecules_parsed.sdf, molecules_standardized.csv, descriptors_raw.csv
- Primary expected artifact: `descriptors.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Analyze the sensitivity of BitterPredict predictions to individual chemical structure descriptor subsets
- Task kind: `analysis`
- Task: Perform descriptor ablation analysis on the BitterPredict classifier by systematically zeroing out descriptor subgroups and recording prediction label changes per molecule. Produce a table quantifying the per-descriptor-group prediction-change rates across the dataset.
- Inputs:
  - Descriptor CSV file with required molecular descriptors and bitter/not-bitter labels
- Expected outputs:
  - Table of per-descriptor-group prediction-change rates showing how many molecules change prediction label when each descriptor subgroup is ablated
- Tools: BitterPredict
- Landmark output files: descriptor_subgroups.txt, ablated_dataset_*.csv, baseline_predictions.csv
- Primary expected artifact: `ablation_results.csv`

## Final expected outputs

- `CSV or Excel file containing molecular descriptors formatted for BitterPredict.m input` (type: file, tolerance: hash)
- `Table of per-descriptor-group prediction-change rates showing how many molecules change prediction label when each descriptor subgroup is ablated` (type: file, tolerance: hash)

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
  "workflow_id": "coll_bittermass_workflow",
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
    "CSV or Excel file containing molecular descriptors formatted for BitterPredict.m input": "<locator>",
    "Table of per-descriptor-group prediction-change rates showing how many molecules change prediction label when each descriptor subgroup is ablated": "<locator>"
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
