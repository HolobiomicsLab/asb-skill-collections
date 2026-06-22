---
name: workflow-configuration-parsing
description: Use when you have a workflow.csv file co-located with sequence.csv in a SmartPeak session directory and need to load a default or custom workflow configuration into an executable command sequence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SmartPeak
  - SmartPeakCLI
  - OpenMS
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartpeak_cq
    doi: 10.1021/acs.analchem.0c03421
    title: SmartPeak
  dedup_kept_from: coll_smartpeak_cq
schema_version: 0.2.0
---

# workflow-configuration-parsing

## Summary

Parse and validate a workflow configuration file (workflow.csv) to construct an ordered sequence of processing commands that SmartPeak will execute during session initialization. This skill bridges file-based workflow definition and downstream workflow execution.

## When to use

You have a workflow.csv file co-located with sequence.csv in a SmartPeak session directory and need to load a default or custom workflow configuration into an executable command sequence. Apply this skill at session startup or when reconfiguring the processing pipeline without rebuilding the application.

## When NOT to use

- Workflow configuration is already loaded in memory as a command object or data structure; parsing is unnecessary.
- You are modifying workflow steps interactively via SmartPeak GUI; use the GUI workflow editor instead of re-parsing the file.
- The workflow.csv file is missing or the session directory is not accessible.

## Inputs

- workflow.csv file (text format, one workflow_step command per row)
- session directory path (co-located with sequence.csv)

## Outputs

- ordered list of validated workflow command names
- validation report (recognized vs. unrecognized commands)

## How to apply

Read the workflow.csv file from the session directory row-by-row and extract the workflow_step command name from each row. Validate each extracted command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES). Preserve the row sequence from the file as the execution order. Reject any unrecognized commands and report validation errors. Return the ordered command list for the downstream workflow executor to invoke each step sequentially. The parsing must maintain strict ordering because workflow steps have interdependencies (e.g., raw data must be loaded before chromatogram extraction).

## Related tools

- **SmartPeak** (workflow execution engine that consumes parsed command sequence) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (command-line interface for loading and validating workflow configurations programmatically) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (underlying toolkit providing the individual workflow step implementations)

## Evaluation signals

- All rows in workflow.csv are successfully parsed and no commands are dropped or reordered.
- Each extracted command matches one of the known supported workflow commands (validate against the supported set); any unrecognized command is flagged and rejected.
- The output command list preserves row order exactly as it appears in the CSV file.
- The workflow executor receives the ordered command list and invokes each step without errors or out-of-sequence execution.
- Downstream steps (e.g., EXTRACT_CHROMATOGRAM_WINDOWS) succeed only if their prerequisites (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS) appear earlier in the parsed sequence.

## Limitations

- Parsing does not validate semantic correctness of the workflow (e.g., whether the chosen steps are suitable for the data type or experiment type); validation is lexical only.
- The parser assumes workflow.csv is well-formed (correct delimiters, no malformed rows); handling of corrupted or non-standard CSV formatting is not specified.
- No changelog or discussion of known parsing edge cases is provided in the source material, limiting guidance on failure modes or version compatibility.

## Evidence

- [other] Read the workflow.csv file from the session directory (co-located with sequence.csv): "Read the workflow.csv file from the session directory (co-located with sequence.csv). 2. Parse each row to extract the workflow_step command name."
- [other] Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES): "Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES,"
- [other] Construct an ordered list preserving the row sequence from the file. 5. Return the ordered command list for downstream workflow executor: "Construct an ordered list preserving the row sequence from the file. 5. Return the ordered command list for downstream workflow executor to invoke each step in sequence."
- [methods] SmartPeak automates processing through an ordered workflow that includes peak detection and integration, calibration curve optimization, and quality control reporting steps: "SmartPeak automates processing through an ordered workflow that includes peak detection and integration, calibration curve optimization, and quality control reporting steps."
- [readme] Edit the workflow with ``Edit | Workflow``. You have an option to cherry pick the custom workflow or to choose the predefined set of operations.: "Edit the workflow with ``Edit | Workflow``. You have an option to cherry pick the custom workflow or to choose the predefined set of operations."
