---
name: metabolomics-workflow-step-enumeration
description: Use when when initializing a SmartPeak session and you have a workflow.csv file co-located with sequence.csv in the session directory, and you need to determine the precise order and validity of peak detection, calibration, and QC operations before execution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0629
  - http://edamontology.org/topic_3172
  tools:
  - SmartPeak
  - SmartPeakCLI
  - OpenMS
  techniques:
  - GC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03421
  all_source_dois:
  - 10.1021/acs.analchem.0c03421
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-workflow-step-enumeration

## Summary

Load and parse a workflow configuration file (workflow.csv) to enumerate an ordered sequence of processing steps for metabolomics data analysis in SmartPeak. This skill validates each step command against a known set of supported operations and constructs the execution order for downstream workflow invocation.

## When to use

When initializing a SmartPeak session and you have a workflow.csv file co-located with sequence.csv in the session directory, and you need to determine the precise order and validity of peak detection, calibration, and QC operations before execution. Use this skill whenever session startup requires reproducible workflow enumeration from a configuration file rather than GUI-based manual step definition.

## When NOT to use

- The workflow.csv file is absent or missing the workflow_step column — fall back to GUI-based workflow editing or manual step construction.
- You are dynamically generating workflow steps programmatically rather than loading from a static configuration file.
- The workflow commands contain unsupported operations not in the known set (LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES) — validation will fail and require manual step curation.

## Inputs

- workflow.csv file (tabular text format with workflow_step column)
- session directory path (containing co-located sequence.csv)

## Outputs

- ordered list of workflow command names (strings)
- workflow execution plan (structured sequence preserving CSV row order)

## How to apply

Read the workflow.csv file from the session directory (co-located with sequence.csv). Parse each row to extract the workflow_step command name (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES). Validate each command against the known set of supported workflow commands. Construct an ordered list that preserves the row sequence from the file, maintaining the precedence dependencies for peak detection before integration, calibration curve optimization before quantification, and feature storage after selection. Return the ordered command list to the workflow executor, which will invoke each step in sequence without modification.

## Related tools

- **SmartPeak** (Primary workflow orchestration platform that executes the enumerated steps in sequence) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for workflow loading and validation without GUI) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing the algorithmic implementations for workflow commands (peak detection, calibration, feature storage))

## Evaluation signals

- All rows from workflow.csv are parsed without parsing errors or skipped rows.
- Each parsed command matches one of the supported workflow commands (LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES).
- The returned ordered list preserves the row sequence from the CSV file; row N in the file maps to position N in the output list.
- Validation rejects unsupported commands and raises an error or warning, halting execution until the workflow.csv is corrected.
- The workflow executor successfully invokes each enumerated step in order, and the session log records the command sequence matching the CSV order.

## Limitations

- Enumeration does not verify cross-command dependencies or data flow compatibility; validation is lexical only (command name matching against known set).
- Missing or malformed workflow.csv file will cause enumeration to fail; no automatic fallback to a default workflow is specified in the source material.
- The skill does not support conditional branching or step skipping; all enumerated steps are mandatory and executed in strict order.
- No version control or backward-compatibility handling is mentioned; if SmartPeak adds or deprecates workflow commands, existing workflow.csv files may become invalid without warning.

## Evidence

- [methods] 1. Read the workflow.csv file from the session directory (co-located with sequence.csv). 2. Parse each row to extract the workflow_step command name. 3. Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES). 4. Construct an ordered list preserving the row sequence from the file.: "Read the workflow.csv file from the session directory (co-located with sequence.csv). Parse each row to extract the workflow_step command name. Validate each command against the known set of"
- [methods] SmartPeak automates processing through an ordered workflow that includes peak detection and integration, calibration curve optimization, and quality control reporting steps.: "SmartPeak automates processing through an ordered workflow that includes peak detection and integration, calibration curve optimization, and quality control reporting steps."
- [readme] The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting.: "The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting."
- [readme] Start the session with ``File | Load session from sequence`` Choose the corresponding directory with ``Change dir``. The path to example folder can be shortened to f.e. ``/data/GCMS_SIM_Unknowns`` Select the sequence file: "Start the session with ``File | Load session from sequence`` Choose the corresponding directory with ``Change dir``"
