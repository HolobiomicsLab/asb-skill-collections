# Workflow Challenge: `coll_sirius_workflow`


> SIRIUS is a Java-based software framework offering freely available methods to the scientific community for the analysis of LC-MS/MS data of metabolites and other small molecules, intended for research and education use.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 1-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

SIRIUS provides a suite of computational tools and web services (including CSI:FingerID, CANOPUS, and MSNovelist) designed for metabolomics analysis. The methods are distributed as free resources for academic research and educational purposes, with commercial redistribution prohibited. The framework is maintained by the Böcker group and made available through both academic web services and commercial licensing via Bright Giant GmbH for non-academic users.

## Research questions

- [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blueviolet.svg)](https://www.gnu.org/licenses/agpl-3.0) [![Generic badge](https://img.shields.io/badge/Version-6.3.7-informational.svg)](https://shields.io/) [![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml) [![Join community chat at https://gitter.im/sirius-ms/general](https://badg...

**Domain:** metabolomics

**Techniques:** in-silico-fragmentation, machine-learning, metabolite-identification, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** SIRIUS is licensed under AGPL v3. _[grounded: sirius_system]_
- **(finding)** The current version of SIRIUS is 6.3.7. _[grounded: sirius_system]_
- **(finding)** SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites. _[grounded: sirius_system]_
- **(finding)** SIRIUS methods are offered to the scientific community as freely available resources. _[grounded: sirius_system]_
- **(finding)** Redistribution of SIRIUS methods in whole or in part for commercial purposes is prohibited. _[grounded: sirius_system]_
- **(finding)** The SIRIUS web services CSI:FingerID, CANOPUS, and MSNovelist are hosted by the Böcker group. _[grounded: sirius_system]_
- **(finding)** SIRIUS web services hosted by the Böcker group are for academic research and education use only. _[grounded: sirius_system]_
- **(finding)** Non-academic users can obtain SIRIUS licenses and services from Bright Giant GmbH. _[grounded: sirius_system]_
- **(finding)** Users of SIRIUS tools are asked to cite the corresponding papers in any resulting publications. _[grounded: sirius_system]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Commercial redistribution of methods is prohibited

## Steps

### Step `task_001`
- Title: Reconstruct and evaluate a paper-grounded scientific task
- Task: Create a bounded scientific task from the article package by linking a research question or finding to available inputs, expected outputs, tools, skills, workflow logic, evidence snippets, missing information, and an evaluation strategy.
- Inputs:
  - figure: figures/c-add-doc.svg
  - figure: figures/c-bug.svg
  - figure: figures/c-clipboard.svg
  - figure: figures/c-controls-play.svg
  - figure: figures/c-db.svg
  - figure: figures/c-document.svg
  - figure: figures/c-documents.svg
  - figure: figures/c-download.svg
  - figure: figures/c-dragndrop.svg
  - figure: figures/c-export.svg
  - figure: figures/c-fbmn.svg
  - figure: figures/c-filter-down.svg
  - figure: figures/c-filter-up.svg
  - figure: figures/c-fingerprint.svg
  - figure: figures/c-fmet.svg
  - figure: figures/c-folder-close.svg
  - figure: figures/c-folder-file.svg
  - figure: figures/c-folder-open.svg
  - figure: figures/c-folder.svg
  - figure: figures/sirius-icon.png
  - main_article: paper.md
- Expected outputs:
  - figure: figures/c-add-doc.svg
  - figure: figures/c-bug.svg
  - figure: figures/c-clipboard.svg
  - figure: figures/c-controls-play.svg
  - figure: figures/c-db.svg
  - figure: figures/c-document.svg
  - figure: figures/c-documents.svg
  - figure: figures/c-download.svg
  - figure: figures/c-dragndrop.svg
  - figure: figures/c-export.svg
  - figure: figures/c-fbmn.svg
  - figure: figures/c-filter-down.svg
  - figure: figures/c-filter-up.svg
  - figure: figures/c-fingerprint.svg
  - figure: figures/c-fmet.svg
  - figure: figures/c-folder-close.svg
  - figure: figures/c-folder-file.svg
  - figure: figures/c-folder-open.svg
  - figure: figures/c-folder.svg
  - figure: figures/sirius-icon.png
  - We ask that users of our tools cite the corresponding papers in any resulting publications.</span>*
- Tools: SIRIUS, CSI:FingerID, CANOPUS, MSNovelist, GitHub

## Final expected outputs

- `figure: figures/c-add-doc.svg` (type: file, tolerance: hash)
- `figure: figures/c-bug.svg` (type: file, tolerance: hash)
- `figure: figures/c-clipboard.svg` (type: file, tolerance: hash)
- `figure: figures/c-controls-play.svg` (type: file, tolerance: hash)
- `figure: figures/c-db.svg` (type: file, tolerance: hash)
- `figure: figures/c-document.svg` (type: file, tolerance: hash)
- `figure: figures/c-documents.svg` (type: file, tolerance: hash)
- `figure: figures/c-download.svg` (type: file, tolerance: hash)
- `figure: figures/c-dragndrop.svg` (type: file, tolerance: hash)
- `figure: figures/c-export.svg` (type: file, tolerance: hash)
- `figure: figures/c-fbmn.svg` (type: file, tolerance: hash)
- `figure: figures/c-filter-down.svg` (type: file, tolerance: hash)
- `figure: figures/c-filter-up.svg` (type: file, tolerance: hash)
- `figure: figures/c-fingerprint.svg` (type: file, tolerance: hash)
- `figure: figures/c-fmet.svg` (type: file, tolerance: hash)
- `figure: figures/c-folder-close.svg` (type: file, tolerance: hash)
- `figure: figures/c-folder-file.svg` (type: file, tolerance: hash)
- `figure: figures/c-folder-open.svg` (type: file, tolerance: hash)
- `figure: figures/c-folder.svg` (type: file, tolerance: hash)
- `figure: figures/sirius-icon.png` (type: file, tolerance: hash)
- `We ask that users of our tools cite the corresponding papers in any resulting publications.</span>*` (type: file, tolerance: hash)

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
  "workflow_id": "coll_sirius_workflow",
  "agent_order": [
    "task_001"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "figure: figures/c-add-doc.svg": "<locator>",
    "figure: figures/c-bug.svg": "<locator>",
    "figure: figures/c-clipboard.svg": "<locator>",
    "figure: figures/c-controls-play.svg": "<locator>",
    "figure: figures/c-db.svg": "<locator>",
    "figure: figures/c-document.svg": "<locator>",
    "figure: figures/c-documents.svg": "<locator>",
    "figure: figures/c-download.svg": "<locator>",
    "figure: figures/c-dragndrop.svg": "<locator>",
    "figure: figures/c-export.svg": "<locator>",
    "figure: figures/c-fbmn.svg": "<locator>",
    "figure: figures/c-filter-down.svg": "<locator>",
    "figure: figures/c-filter-up.svg": "<locator>",
    "figure: figures/c-fingerprint.svg": "<locator>",
    "figure: figures/c-fmet.svg": "<locator>",
    "figure: figures/c-folder-close.svg": "<locator>",
    "figure: figures/c-folder-file.svg": "<locator>",
    "figure: figures/c-folder-open.svg": "<locator>",
    "figure: figures/c-folder.svg": "<locator>",
    "figure: figures/sirius-icon.png": "<locator>",
    "We ask that users of our tools cite the corresponding papers in any resulting publications.</span>*": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
