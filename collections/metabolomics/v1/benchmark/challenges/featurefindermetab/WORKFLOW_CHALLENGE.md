# Workflow Challenge: `coll_featurefindermetab_workflow`


> OpenMS is an open-source software framework for mass spectrometry data analysis. The project welcomes community contributions through issue reporting and pull requests, with guidelines for code quality, testing, and documentation.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 1-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

OpenMS is a community-driven open-source project for mass spectrometry analytics. The documentation describes the contribution process, including procedures for reporting bugs and submitting pull requests. Contributors are expected to adhere to coding conventions, provide unit and functional tests, include proper documentation, and implement Python bindings where applicable. The project emphasizes early communication with core developers to ensure alignment on novel tools or algorithms.

## Research questions

- [![License (3-Clause BSD)](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gR2VuZXJhdG9yOiBBZG9iZSBJbGx1c3RyYXRvciAyNC4xLjEsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAwIEJ1aWxkIDApICAtLT4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iTGF5ZXJfMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeD0iMHB4IiB5PSIwcHgiDQoJIHZpZXdCb3g9IjAgMCA1MTIgN...

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** OpenMS is licensed under the 3-Clause BSD license. _[grounded: openms_system]_
- **(finding)** Contributors should adhere to the OpenMS Code of Conduct when interacting with other developers, users, or community members. _[grounded: openms_system]_
- **(finding)** OpenMS provides a Contributor Onboarding Guide for beginners new to open source or the project. _[grounded: openms_system]_
- **(finding)** When reporting a bug in OpenMS, users should provide the OpenMS version they are running. _[grounded: openms_system]_
- **(finding)** When reporting a bug in OpenMS, users should provide the platform they are running OpenMS on. _[grounded: openms_system]_
- **(finding)** When reporting a bug in OpenMS, users should describe how to reproduce the bug. _[grounded: openms_system]_
- **(finding)** When reporting a bug in OpenMS, users should provide relevant tool output such as error messages. _[grounded: openms_system]_
- **(finding)** When reporting a bug in OpenMS, users should provide data to reproduce the bug, preferably as a GitHub gist or via platforms like Dropbox or Google Drive. _[grounded: openms_system]_
- **(finding)** OpenMS maintainers assign severity labels to issues to indicate if a bug is a blocker for a new release. _[grounded: openms_system]_
- **(finding)** OpenMS has a developer guide available at https://openms.readthedocs.io/en/latest/manual/develop.html. _[grounded: openms_system]_
- **(finding)** Pull request contributors must adhere to OpenMS coding conventions. _[grounded: openms_system]_
- **(finding)** Pull request contributors must have unit tests and functional tests for their code.
- **(finding)** Pull request contributors must have proper documentation for their code.
- **(finding)** Pull request contributors must have Python bindings with nanobind binding files located in src/pyOpenMS/bindings/. _[grounded: pyopenms_component]_
- **(finding)** OpenMS provides wrapping instructions in src/pyOpenMS/CLAUDE.md. _[grounded: openms_system]_
- **(finding)** A core developer will review changes to the main development branch (develop) in OpenMS. _[grounded: openms_system]_
- **(finding)** OpenMS core developers can be indicated as preferred reviewers using links in a comment section. _[grounded: openms_system]_
- **(finding)** Early contact with OpenMS core developers may provide additional guidance on developing novel tools or algorithms. _[grounded: openms_system]_
- **(finding)** OpenMS provides a Developer Guide with detailed coding conventions, architectural guidelines, and technical documentation. _[grounded: openms_system]_

## Steps

### Step `task_001`
- Title: Reconstruct: OpenMS
- Task: Create a bounded scientific task from the article package by linking a research question or finding to available inputs, expected outputs, tools, skills, workflow logic, evidence snippets, missing information, and an evaluation strategy.
- Inputs:
  - figure: figures/AxisWidget.png
  - figure: figures/ColorSelector.png
  - figure: figures/DeMeanderize.png
  - figure: figures/ExperimentalSettings.png
  - figure: figures/HistogramWidget.png
  - figure: figures/INIFileEditor.png
  - figure: figures/Kernel.png
  - figure: figures/Kernel_DataPoints.png
  - figure: figures/MetaDataBrowser.png
  - figure: figures/OpenMS_75x55_transparent.png
  - figure: figures/background.png
  - figure: figures/category.png
  - figure: figures/example_header.png
  - figure: figures/example_wizard.png
  - figure: figures/logo.drawio.svg
  - figure: figures/openms_logo_corner_small.png
  - figure: figures/openms_logo_corner_transparent.png
  - figure: figures/openms_logo_large_transparent.png
  - figure: figures/openms_logo_small_transparent.png
  - figure: figures/splash.png
  - main_article: paper.md
- Expected outputs:
  - figure: figures/AxisWidget.png
  - figure: figures/ColorSelector.png
  - figure: figures/DeMeanderize.png
  - figure: figures/ExperimentalSettings.png
  - figure: figures/HistogramWidget.png
  - figure: figures/INIFileEditor.png
  - figure: figures/Kernel.png
  - figure: figures/Kernel_DataPoints.png
  - figure: figures/MetaDataBrowser.png
  - figure: figures/OpenMS_75x55_transparent.png
  - figure: figures/background.png
  - figure: figures/category.png
  - figure: figures/example_header.png
  - figure: figures/example_wizard.png
  - figure: figures/logo.drawio.svg
  - figure: figures/openms_logo_corner_small.png
  - figure: figures/openms_logo_corner_transparent.png
  - figure: figures/openms_logo_large_transparent.png
  - figure: figures/openms_logo_small_transparent.png
  - figure: figures/splash.png
  - If you found a bug, e.g. an OpenMS tool crashes during data processing, it is essential to provide some basic information: - the OpenMS version you are running - the platform you are running OpenMS on (Windows 10, ...) - how you installed OpenMS (e.g., from within KNIME, binary installers, self compiled) - a description on how to reproduce the bug - relevant tool output (e.g., error messages) - data to repoduce the bug (If possible as a GitHub gist.
- Tools: OpenMS, KNIME, Python, GitHub

## Final expected outputs

- `figure: figures/AxisWidget.png` (type: file, tolerance: hash)
- `figure: figures/ColorSelector.png` (type: file, tolerance: hash)
- `figure: figures/DeMeanderize.png` (type: file, tolerance: hash)
- `figure: figures/ExperimentalSettings.png` (type: file, tolerance: hash)
- `figure: figures/HistogramWidget.png` (type: file, tolerance: hash)
- `figure: figures/INIFileEditor.png` (type: file, tolerance: hash)
- `figure: figures/Kernel.png` (type: file, tolerance: hash)
- `figure: figures/Kernel_DataPoints.png` (type: file, tolerance: hash)
- `figure: figures/MetaDataBrowser.png` (type: file, tolerance: hash)
- `figure: figures/OpenMS_75x55_transparent.png` (type: file, tolerance: hash)
- `figure: figures/background.png` (type: file, tolerance: hash)
- `figure: figures/category.png` (type: file, tolerance: hash)
- `figure: figures/example_header.png` (type: file, tolerance: hash)
- `figure: figures/example_wizard.png` (type: file, tolerance: hash)
- `figure: figures/logo.drawio.svg` (type: file, tolerance: hash)
- `figure: figures/openms_logo_corner_small.png` (type: file, tolerance: hash)
- `figure: figures/openms_logo_corner_transparent.png` (type: file, tolerance: hash)
- `figure: figures/openms_logo_large_transparent.png` (type: file, tolerance: hash)
- `figure: figures/openms_logo_small_transparent.png` (type: file, tolerance: hash)
- `figure: figures/splash.png` (type: file, tolerance: hash)
- `If you found a bug, e.g. an OpenMS tool crashes during data processing, it is essential to provide some basic information: - the OpenMS version you are running - the platform you are running OpenMS on (Windows 10, ...) - how you installed OpenMS (e.g., from within KNIME, binary installers, self compiled) - a description on how to reproduce the bug - relevant tool output (e.g., error messages) - data to repoduce the bug (If possible as a GitHub gist.` (type: file, tolerance: hash)

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
  "workflow_id": "coll_featurefindermetab_workflow",
  "agent_order": [
    "task_001"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "figure: figures/AxisWidget.png": "<locator>",
    "figure: figures/ColorSelector.png": "<locator>",
    "figure: figures/DeMeanderize.png": "<locator>",
    "figure: figures/ExperimentalSettings.png": "<locator>",
    "figure: figures/HistogramWidget.png": "<locator>",
    "figure: figures/INIFileEditor.png": "<locator>",
    "figure: figures/Kernel.png": "<locator>",
    "figure: figures/Kernel_DataPoints.png": "<locator>",
    "figure: figures/MetaDataBrowser.png": "<locator>",
    "figure: figures/OpenMS_75x55_transparent.png": "<locator>",
    "figure: figures/background.png": "<locator>",
    "figure: figures/category.png": "<locator>",
    "figure: figures/example_header.png": "<locator>",
    "figure: figures/example_wizard.png": "<locator>",
    "figure: figures/logo.drawio.svg": "<locator>",
    "figure: figures/openms_logo_corner_small.png": "<locator>",
    "figure: figures/openms_logo_corner_transparent.png": "<locator>",
    "figure: figures/openms_logo_large_transparent.png": "<locator>",
    "figure: figures/openms_logo_small_transparent.png": "<locator>",
    "figure: figures/splash.png": "<locator>",
    "If you found a bug, e.g. an OpenMS tool crashes during data processing, it is essential to provide some basic information: - the OpenMS version you are running - the platform you are running OpenMS on (Windows 10, ...) - how you installed OpenMS (e.g., from within KNIME, binary installers, self compiled) - a description on how to reproduce the bug - relevant tool output (e.g., error messages) - data to repoduce the bug (If possible as a GitHub gist.": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
