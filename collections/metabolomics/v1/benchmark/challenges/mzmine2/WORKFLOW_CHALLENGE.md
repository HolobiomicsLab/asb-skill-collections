# Workflow Challenge: `coll_mzmine2_workflow`


> MZmine 2 is an open-source software framework for mass-spectrometry data processing designed to provide user-friendly, flexible, and easily extendable tools for the complete MS data analysis workflow.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 1-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MZmine 2 is presented as an open-source software platform for mass-spectrometry data processing. The project aims to deliver a comprehensive suite of modules that cover the entire MS data analysis workflow, with emphasis on user-friendliness, flexibility, and extensibility to accommodate diverse analytical needs in mass spectrometry research.

## Research questions

- The goals of the project is to provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow.

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MZmine 2 aims to provide user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow [evidence_step: task_001]
- **(finding)** All development of MZmine now happens in a new repository called mzmine3. _[grounded: mzmine3_system]_
- **(finding)** The mzmine2 repository serves only as a reference to the old MZmine 2. _[grounded: mzmine2_system]_
- **(finding)** MZmine 2 is an open-source software for mass-spectrometry data processing. _[grounded: mzmine2_system]_
- **(finding)** MZmine 2 was succeeded by mzmine. _[grounded: mzmine2_system]_

## Steps

### Step `task_001`
- Title: Reconstruct and evaluate a paper-grounded scientific task
- Task: Create a bounded scientific task from the article package by linking a research question or finding to available inputs, expected outputs, tools, skills, workflow logic, evidence snippets, missing information, and an evaluation strategy.
- Inputs:
  - figure: figures/DBCustomIcon.png
  - figure: figures/DBLipidsIcon.png
  - figure: figures/DBOnlineIcon.png
  - figure: figures/DBSpectraIcon.png
  - figure: figures/KMDIcon.png
  - figure: figures/MZmine_logo_CMYK.jpg
  - figure: figures/MZmine_logo_CMYK.png
  - figure: figures/MZmine_logo_RGB.jpg
  - figure: figures/MZmine_logo_RGB.png
  - figure: figures/MZmine_logo_black.jpg
  - figure: figures/MZmine_logo_black.png
  - figure: figures/MZmine_logo_white.png
  - figure: figures/RKMIcon.png
  - figure: figures/annotationsicon.png
  - figure: figures/arrowdownicon.png
  - figure: figures/arrowupicon.png
  - figure: figures/axesicon.png
  - figure: figures/bgicon.png
  - figure: figures/blocksizeicon.png
  - figure: figures/btnAccept.png
  - main_article: paper.md
- Expected outputs:
  - figure: figures/DBCustomIcon.png
  - figure: figures/DBLipidsIcon.png
  - figure: figures/DBOnlineIcon.png
  - figure: figures/DBSpectraIcon.png
  - figure: figures/KMDIcon.png
  - figure: figures/MZmine_logo_CMYK.jpg
  - figure: figures/MZmine_logo_CMYK.png
  - figure: figures/MZmine_logo_RGB.jpg
  - figure: figures/MZmine_logo_RGB.png
  - figure: figures/MZmine_logo_black.jpg
  - figure: figures/MZmine_logo_black.png
  - figure: figures/MZmine_logo_white.png
  - figure: figures/RKMIcon.png
  - figure: figures/annotationsicon.png
  - figure: figures/arrowdownicon.png
  - figure: figures/arrowupicon.png
  - figure: figures/axesicon.png
  - figure: figures/bgicon.png
  - figure: figures/blocksizeicon.png
  - figure: figures/btnAccept.png
- Tools: MZmine 2, mzmine2, GitHub, MZmine

## Final expected outputs

- `figure: figures/DBCustomIcon.png` (type: file, tolerance: hash)
- `figure: figures/DBLipidsIcon.png` (type: file, tolerance: hash)
- `figure: figures/DBOnlineIcon.png` (type: file, tolerance: hash)
- `figure: figures/DBSpectraIcon.png` (type: file, tolerance: hash)
- `figure: figures/KMDIcon.png` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_CMYK.jpg` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_CMYK.png` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_RGB.jpg` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_RGB.png` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_black.jpg` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_black.png` (type: file, tolerance: hash)
- `figure: figures/MZmine_logo_white.png` (type: file, tolerance: hash)
- `figure: figures/RKMIcon.png` (type: file, tolerance: hash)
- `figure: figures/annotationsicon.png` (type: file, tolerance: hash)
- `figure: figures/arrowdownicon.png` (type: file, tolerance: hash)
- `figure: figures/arrowupicon.png` (type: file, tolerance: hash)
- `figure: figures/axesicon.png` (type: file, tolerance: hash)
- `figure: figures/bgicon.png` (type: file, tolerance: hash)
- `figure: figures/blocksizeicon.png` (type: file, tolerance: hash)
- `figure: figures/btnAccept.png` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mzmine2_workflow",
  "agent_order": [
    "task_001"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "figure: figures/DBCustomIcon.png": "<locator>",
    "figure: figures/DBLipidsIcon.png": "<locator>",
    "figure: figures/DBOnlineIcon.png": "<locator>",
    "figure: figures/DBSpectraIcon.png": "<locator>",
    "figure: figures/KMDIcon.png": "<locator>",
    "figure: figures/MZmine_logo_CMYK.jpg": "<locator>",
    "figure: figures/MZmine_logo_CMYK.png": "<locator>",
    "figure: figures/MZmine_logo_RGB.jpg": "<locator>",
    "figure: figures/MZmine_logo_RGB.png": "<locator>",
    "figure: figures/MZmine_logo_black.jpg": "<locator>",
    "figure: figures/MZmine_logo_black.png": "<locator>",
    "figure: figures/MZmine_logo_white.png": "<locator>",
    "figure: figures/RKMIcon.png": "<locator>",
    "figure: figures/annotationsicon.png": "<locator>",
    "figure: figures/arrowdownicon.png": "<locator>",
    "figure: figures/arrowupicon.png": "<locator>",
    "figure: figures/axesicon.png": "<locator>",
    "figure: figures/bgicon.png": "<locator>",
    "figure: figures/blocksizeicon.png": "<locator>",
    "figure: figures/btnAccept.png": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
