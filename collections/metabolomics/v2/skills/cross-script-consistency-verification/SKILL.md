---
name: cross-script-consistency-verification
description: Use when when a deep learning pipeline processes mass spectrometry spectra through multiple independent scripts (e.g., train_rescore.py, run_fiddle.py, test_caffeine.py) and a specific feature must be removed or masked to prevent the model from learning directly from a protected input (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - msfiddle
  - FIDDLE
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
---

# cross-script-consistency-verification

## Summary

Verify that a critical preprocessing operation (e.g., zeroing the precursor m/z feature) is applied consistently across multiple execution scripts in a codebase before model inference. This ensures that no unintended leakage of protected information into the feature encoder occurs across different workflow stages (training, evaluation, reproduction).

## When to use

When a deep learning pipeline processes mass spectrometry spectra through multiple independent scripts (e.g., train_rescore.py, run_fiddle.py, test_caffeine.py) and a specific feature must be removed or masked to prevent the model from learning directly from a protected input (e.g., precursor m/z value env[:, 0] must be zeroed before TCN encoding to prevent mass-based prior learning). Use this skill to audit whether the masking operation is implemented identically in all code paths that feed spectra to the encoder.

## When NOT to use

- The preprocessing step is already documented in a single centralized module (e.g., a shared preprocessing.py file that all scripts import), making cross-script verification redundant—instead, verify the module directly.
- The feature masking logic is parameterized in a configuration file (e.g., YAML) and applied uniformly by all scripts, eliminating the need to check each script individually.
- The scripts do not share a common preprocessing step or operate on fundamentally different input schemas, so feature-level consistency is not applicable.

## Inputs

- Python script files (run_fiddle.py, train_rescore.py, test_caffeine.py, or equivalent) from the FIDDLE codebase
- Source code text containing spectrum preprocessing code and TCN encoder invocation
- Documentation or comments describing the intended preprocessing pipeline

## Outputs

- Structured verification report (CSV, JSON, or plain text table) with columns: Script Name, File Path, Preprocessing Location (line number), Feature Index Zeroed, Operation Type, Timing Relative to Encoder, Pass/Fail Status
- Summary table indicating whether all scripts show consistent zeroing behavior
- List of any discrepancies or missing operations (e.g., script that does not zero env[:, 0])

## How to apply

Load each execution script from the codebase and locate the spectrum preprocessing section where the input feature array (env) is prepared before passing to the encoder model. For each script, identify the exact line(s) where the zeroing operation occurs, document the array indexing (e.g., env[:, 0] = 0), and verify that the operation targets the same feature index, uses the same assignment method, and occurs at the same point in the pipeline (before encoder input). Construct a structured verification report for each script listing the file path, preprocessing code location, line number(s), and a pass/fail status. Cross-check that the timing of the operation is identical relative to encoder invocation—if one script zeros the feature before calling the encoder but another zeros it after, or if one script omits the operation entirely, flag a consistency failure. Generate a summary table documenting whether all scripts pass the consistency check.

## Related tools

- **msfiddle** (CLI and Python API for running FIDDLE inference; used to execute preprocessing and spectrum encoding across run_fiddle.py, train_rescore.py, and test_caffeine.py scripts) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Deep learning codebase containing the three main execution scripts (run_fiddle.py, train_rescore.py, test_caffeine.py) that require consistency verification of the precursor m/z zeroing operation) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- All three scripts (run_fiddle.py, train_rescore.py, test_caffeine.py) contain env[:, 0] = 0 (or equivalent zeroing operation) in their preprocessing sections
- The feature index is identical across all scripts (e.g., all zero the first column [0], not inconsistent indices like [0], [1], [2])
- The zeroing operation occurs before the spectrum is passed to the TCN encoder in all scripts; no script encodes the spectrum before masking
- Line numbers and surrounding context (e.g., variable names, function names) confirm the operation is in the same logical preprocessing stage across all scripts
- The operation uses the same assignment syntax (e.g., array indexing and direct assignment) consistently, not alternative methods like masking, filtering, or conditionals

## Limitations

- This skill only verifies syntactic and positional consistency; it does not validate whether the zeroing operation is semantically correct or sufficient to prevent information leakage (e.g., if the precursor m/z is encoded indirectly through other features or metadata).
- If preprocessing is refactored into a shared utility function and called by all scripts, the verification becomes a check of function availability and invocation, not line-by-line code inspection.
- Changes to the codebase after the verification report is generated are not automatically detected; the report is a point-in-time snapshot and must be re-run after code updates.
- The skill assumes that the three main scripts are the only code paths feeding spectra to the encoder; if other scripts or entry points exist (e.g., Jupyter notebooks, API wrappers, or internal helper functions), they may not be included in the verification scope.

## Evidence

- [other] Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts in the FIDDLE codebase?: "Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts"
- [other] Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder.: "Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder"
- [other] Verify consistency of the zeroing operation across all three scripts (same index, same operation, same timing relative to encoder input).: "Verify consistency of the zeroing operation across all three scripts (same index, same operation, same timing relative to encoder input)"
- [readme] This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "This repository contains the full research codebase for model training, evaluation, and paper reproduction"
- [readme] See [`test_caffeine.py`](./test_caffeine.py) for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS.: "See [`test_caffeine.py`](./test_caffeine.py) for a worked example running FIDDLE"
