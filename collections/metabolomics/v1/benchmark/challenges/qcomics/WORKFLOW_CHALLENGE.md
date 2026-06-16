# Workflow Challenge: `coll_qcomics_workflow`


> QComics is an R package designed to provide quick quality assessments of metabolomics or lipidomics studies by processing pooled QCpool samples measured at regular intervals during analytical sequences.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The QComics package processes pooled QCpool samples that must be measured at regular intervals during one or more analytical sequences and exported from Sciex Multiquant software (> v3.0.3) as text files. The package incorporates mechanisms for detecting QCpool measurement intervals from Sciex Multiquant TXT exports and reconstructing quality overview summaries from parsed QCpool positional data to generate quality assessment information for metabolomics and lipidomics studies.

## Research questions

- How does the QComics package parse Sciex Multiquant TXT export files to identify and locate QCpool samples that were injected at regular intervals across metabolomics or lipidomics sequences?
- What metrics does QComics compute from QCpool injection data to assess metabolomics or lipidomics study quality?

## Methods overview

Load and parse the Sciex Multiquant TXT export to extract sample names and injection sequence metadata. Scan sample identifiers and metadata fields to locate QCpool entries using naming patterns or annotations. Map each QCpool sample to its injection index, sequence identifier, and position within the analytical run. Analyze QCpool spacing to confirm regularity of insertion intervals. Validation: Output table contains all QCpool samples with correct injection indices and documented intervals match expected study design spacing. Load and parse QCpool positional table from Sciex Multiquant txt export, extracting compound identifiers and signal intensities across sequential injections. Calculate per-compound coefficient of variation (CV) to assess technical reproducibility across QCpool replicates. Compute signal-trend metrics (drift, stability index, or slope) to detect instrumental performance changes across the injection sequence. Aggregate CV and trend results by compound into a summary table with quality classification (e.g., acceptable vs. poor). Visualization: generate table or figure presenting per-compound CV, trend metrics, and overall quality assessment for rapid interpretation. Validation: output includes per-compound CV values and trend indicators with quality thresholds suitable for literature reporting or protocol standardization.

**Domain:** metabolomics

**Techniques:** feature-detection, metabolite-identification, quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The QComics package is designed to provide a quick overview of the quality of a metabolomics or lipidomics study. _[grounded: sys_qcomics]_
- **(finding)** QComics requires a pooled sample (QCpool) to be measured in regular intervals during one or more sequences. _[grounded: sys_qcomics]_
- **(finding)** QCpool samples must be analysed with Sciex Multiquant software version greater than 3.0.3. _[grounded: comp_qcpool]_
- **(finding)** QCpool samples analysed with Sciex Multiquant must be exported to txt format for use with QComics. _[grounded: sys_qcomics]_

## Steps

### Step `task_001`
- Title: Implement QCpool interval detection from Sciex Multiquant TXT export
- Task kind: `component_reconstruction`
- Task: Parse a Sciex Multiquant TXT export file to identify QCpool (quality control pooled) samples inserted at regular intervals across one or more analytical sequences, and produce a structured table documenting QCpool sample positions and injection indices.
- Inputs:
  - Sciex Multiquant TXT export file containing sample metadata and injection sequence
- Expected outputs:
  - Structured table of QCpool sample positions, injection indices, sequence IDs, and regularity metrics
- Tools: Sciex Multiquant (> v3.0.3), ricoderks/QComics
- Landmark output files: raw_sample_list.txt, qcpool_candidates.csv, qcpool_positions.csv
- Primary expected artifact: `qcpool_positions.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct quality overview summary from parsed QCpool positional data
- Task kind: `component_reconstruction`
- Task: Using a QCpool positional table exported from Sciex Multiquant txt format, compute per-compound coefficient of variation (CV) and signal-trend metrics across QCpool injections to generate a quality overview report.
- Inputs:
  - QCpool positional table in txt format exported from Sciex Multiquant (v3.0.3 or later)
- Expected outputs:
  - Quality overview report (table or figure) showing per-compound CV and signal-trend metrics across QCpool injections
- Tools: Sciex Multiquant (> v3.0.3), QComics
- Landmark output files: qcpool_intensities.csv, per_compound_cv.csv, signal_trends.csv
- Primary expected artifact: `qcomics_quality_report.csv`

## Final expected outputs

- `Quality overview report (table or figure) showing per-compound CV and signal-trend metrics across QCpool injections` (type: file, tolerance: hash)

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
  "workflow_id": "coll_qcomics_workflow",
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
    "Quality overview report (table or figure) showing per-compound CV and signal-trend metrics across QCpool injections": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
