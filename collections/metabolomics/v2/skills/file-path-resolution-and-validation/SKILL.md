---
name: file-path-resolution-and-validation
description: Use when when initializing a SmartPeak session from a sequence file, you need to load and validate the workflow.csv and sequence.csv files that are co-located in the session directory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SmartPeak
  - SmartPeakCLI
  - SmartPeakGUI
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

# file-path-resolution-and-validation

## Summary

Resolve and validate file paths for session data files (workflow.csv, sequence.csv) co-located in a session directory, and verify their integrity before loading into SmartPeak for metabolomics workflow execution. This skill ensures that critical configuration and data files are correctly located, readable, and schema-compliant before downstream processing begins.

## When to use

When initializing a SmartPeak session from a sequence file, you need to load and validate the workflow.csv and sequence.csv files that are co-located in the session directory. Apply this skill at session startup to detect missing, mislocated, or malformed configuration files before attempting to parse or execute workflow steps.

## When NOT to use

- Workflow configuration has already been loaded and validated in memory — skip re-validation.
- User is working with a custom programmatic workflow definition (not CSV-based) — this skill applies only to CSV-driven workflows.
- Session is being resumed from a persisted state where file paths and integrity have been previously verified and cached.

## Inputs

- Session directory path (string)
- workflow.csv file (CSV text file with workflow_step column)
- sequence.csv file (CSV text file co-located in session directory)

## Outputs

- Ordered list of validated workflow command names (list of strings)
- Resolved absolute file paths for workflow.csv and sequence.csv (file paths)
- Integrity check report (boolean: pass/fail, with list of errors if any)

## How to apply

First, resolve the session directory path from the user-selected sequence file location or from the session metadata. Locate the workflow.csv file co-located in the same directory as sequence.csv. Read the workflow.csv file line-by-line and parse each row to extract the workflow_step command name (e.g., LOAD_RAW_DATA, EXTRACT_CHROMATOGRAM_WINDOWS, PICK_MRM_FEATURES). Validate each extracted command against the known set of supported workflow commands maintained by SmartPeak. If a command is not recognized, flag it as an integrity error and halt file validation. Construct an ordered list of commands preserving the row sequence from the file. Use SmartPeak's built-in integrity checks (accessible via GUI: Actions | Integrity checks) to verify that all referenced files and paths are accessible and well-formed. Return the validated, ordered command list and resolved file paths for downstream workflow executor invocation.

## Related tools

- **SmartPeak** (Orchestrates workflow parsing and execution; provides integrity check API and file validation mechanisms) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for session loading and file path resolution without GUI; callable via docker or direct binary) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakGUI** (Graphical file browser and integrity check viewer; exposes file resolution and validation via Actions | Integrity checks menu) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing file I/O and validation primitives used by SmartPeak for CSV and data file handling)

## Evaluation signals

- All workflow command names extracted from workflow.csv match the documented set of supported commands (LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES, etc.)
- Row order in the parsed command list exactly matches the row sequence in the source workflow.csv file
- SmartPeak integrity check reports pass with zero file-not-found or schema-validation errors for workflow.csv and sequence.csv
- File paths resolve to readable, non-empty files accessible by the SmartPeak process; no permission or I/O errors occur during file open/read
- Parsed CSV rows contain no empty or null workflow_step values; malformed rows are flagged and reported to the user

## Limitations

- The skill assumes workflow.csv and sequence.csv are co-located in a single session directory; workflows split across multiple directories are not supported.
- File path validation is filesystem-dependent; network paths or cloud storage may have latency or transient access issues not caught at validation time.
- The integrity check does not validate the semantic correctness or inter-dependency of workflow commands — only syntactic presence in the supported command set. A valid command sequence that violates data flow requirements (e.g., STORE_FEATURES before PICK_MRM_FEATURES) will pass validation but fail at execution.
- No changelog or version-specific command support information is available; if SmartPeak is updated with new workflow commands, the validation set must be manually updated.

## Evidence

- [other] Read the workflow.csv file from the session directory (co-located with sequence.csv). Parse each row to extract the workflow_step command name.: "Read the workflow.csv file from the session directory (co-located with sequence.csv). Parse each row to extract the workflow_step command name."
- [other] Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES, SELECT_FEATURES, STORE_FEATURES).: "Validate each command against the known set of supported workflow commands (e.g., LOAD_RAW_DATA, MAP_CHROMATOGRAMS, EXTRACT_CHROMATOGRAM_WINDOWS, ZERO_CHROMATOGRAM_BASELINE, PICK_MRM_FEATURES,"
- [readme] The integrity of the loaded data can be checked with ``Actions | Integrity checks``. The results of the integrity checks can be viewed with ``View | Info``.: "The integrity of the loaded data can be checked with ``Actions | Integrity checks``. The results of the integrity checks can be viewed with ``View | Info``."
- [readme] Start the session with ``File | Load session from sequence``. Choose the corresponding directory with ``Change dir``. The path to example folder can be shortened to f.e. ``/data/GCMS_SIM_Unknowns``. Select the sequence file.: "Start the session with ``File | Load session from sequence``. Choose the corresponding directory with ``Change dir``."
- [other] Construct an ordered list preserving the row sequence from the file. Return the ordered command list for downstream workflow executor to invoke each step in sequence.: "Construct an ordered list preserving the row sequence from the file. Return the ordered command list for downstream workflow executor to invoke each step in sequence."
