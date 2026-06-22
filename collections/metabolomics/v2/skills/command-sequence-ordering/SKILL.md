---
name: command-sequence-ordering
description: Use when you have a workflow.csv file co-located with sequence.csv in a session directory, and you need to initialize a reproducible, ordered chain of processing steps (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SmartPeak
  - SmartPeakCLI
  - SmartPeakGUI
  - pyOpenMS
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

# command-sequence-ordering

## Summary

Load and validate a CSV-based workflow specification into an ordered sequence of executable processing commands, preserving row order and command name validation. This skill ensures that SmartPeak can reliably reconstruct a default workflow from configuration files during session startup.

## When to use

You have a workflow.csv file co-located with sequence.csv in a session directory, and you need to initialize a reproducible, ordered chain of processing steps (e.g., LOAD_RAW_DATA → MAP_CHROMATOGRAMS → EXTRACT_CHROMATOGRAM_WINDOWS → ZERO_CHROMATOGRAM_BASELINE → PICK_MRM_FEATURES → SELECT_FEATURES → STORE_FEATURES) without manual re-ordering or step omission.

## When NOT to use

- Workflow commands are already loaded in memory as an ordered data structure — re-parsing the CSV would be redundant.
- The workflow.csv file is missing, malformed, or does not co-exist with the sequence.csv file — initialization will fail.
- You need dynamic workflow re-ordering or conditional branching at runtime; this skill enforces static, row-based ordering.

## Inputs

- workflow.csv (comma-separated values file; each row contains a workflow_step command name)
- session directory path (co-located with sequence.csv)

## Outputs

- ordered list of validated workflow step command names (e.g., [LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ...])
- command list ready for downstream workflow executor invocation

## How to apply

Read workflow.csv from the session directory line-by-line. Extract the workflow_step command name from each row (e.g., 'LOAD_RAW_DATA', 'PICK_MRM_FEATURES'). Validate each command against the known set of supported workflow commands provided by SmartPeak. Construct an ordered list that preserves the exact row sequence from the file, rejecting or flagging invalid commands. Return the validated, ordered command list to the workflow executor, which then invokes each step sequentially. This approach ensures deterministic, reproducible workflow execution and guards against transposition errors or unsupported command invocation.

## Related tools

- **SmartPeak** (Primary application providing workflow command definitions and executor; parses workflow.csv and invokes validated commands in sequence.) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface that loads and validates workflow commands from CSV configuration for headless execution.) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakGUI** (Graphical interface that displays loaded workflow steps and allows user review of parsed and validated command sequence before execution.) — https://github.com/AutoFlowResearch/SmartPeak
- **pyOpenMS** (Python bindings for OpenMS; used to parse and process configuration files if workflow.csv is extended or augmented with metadata.)

## Evaluation signals

- Verify that the returned command list preserves the exact row order from workflow.csv (row 1 → position 0, row 2 → position 1, etc.).
- Confirm that all returned commands are members of the supported command set (LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES, etc.).
- Check that invalid or unsupported commands are flagged, logged, or rejected without being added to the ordered list.
- Verify that the workflow executor successfully invokes each command in sequence without transposition, duplication, or omission.
- Confirm that workflow output (e.g., feature tables, QC reports, calibration curves) is generated in the expected sequence and location, indicating correct command ordering.

## Limitations

- No changelog or discussion section content provided in the source material; edge cases or version-specific command compatibility are not documented.
- The skill assumes workflow.csv is well-formed CSV with a consistent schema; robustness to malformed or mixed-delimiter files is not specified.
- Row-based ordering is rigid; no support for conditional branching, loops, or dynamic re-ordering of commands at runtime.
- Validation is against a static set of known commands; new or user-defined commands would require schema extension, which is not described.

## Evidence

- [methods] Read the workflow.csv file from the session directory (co-located with sequence.csv). Parse each row to extract the workflow_step command name.: "Read the workflow.csv file from the session directory (co-located with sequence.csv). Parse each row to extract the workflow_step command name."
- [methods] Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES).: "Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES,"
- [methods] Construct an ordered list preserving the row sequence from the file. Return the ordered command list for downstream workflow executor to invoke each step in sequence.: "Construct an ordered list preserving the row sequence from the file. Return the ordered command list for downstream workflow executor to invoke each step in sequence."
- [intro] SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting.: "SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting."
- [readme] Edit the workflow with ``Edit | Workflow``. You have an option to cherry pick the custom workflow or to choose the predefined set of operations.: "Edit the workflow with ``Edit | Workflow``. You have an option to cherry pick the custom workflow or to choose the predefined set of operations."
