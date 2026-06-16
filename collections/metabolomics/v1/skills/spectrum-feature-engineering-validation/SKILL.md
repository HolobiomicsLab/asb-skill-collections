---
name: spectrum-feature-engineering-validation
description: Use when when implementing or auditing a deep learning pipeline for MS/MS-based molecular formula prediction, verify that precursor m/z values in the input feature array are zeroed before they reach the spectrum encoder (e.g., TCN).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
---

# spectrum-feature-engineering-validation

## Summary

Validate that precursor m/z values are consistently zeroed before spectrum encoding in neural network pipelines to prevent mass-based leakage during formula prediction. This ensures the model learns chemical composition patterns from fragment ions rather than precursor mass.

## When to use

When implementing or auditing a deep learning pipeline for MS/MS-based molecular formula prediction, verify that precursor m/z values in the input feature array are zeroed before they reach the spectrum encoder (e.g., TCN). This is critical if you suspect the model may be learning shortcuts from precursor mass rather than fragment patterns, or when reproducing published results where feature preprocessing is not explicitly documented.

## When NOT to use

- Input is already a preprocessed feature tensor or model checkpoint; use this skill only on source code and raw feature construction logic.
- The model architecture does not use a precursor m/z input at index 0 or uses an entirely different feature encoding scheme.
- You are validating a published checkpoint or inference API without access to the training code; in this case, request the original training scripts from the authors.

## Inputs

- Python training/evaluation script (e.g., run_fiddle.py, train_rescore.py, test_caffeine.py)
- Input feature array (env) containing spectrum metadata and fragment peaks
- Configuration file specifying preprocessing parameters (e.g., fiddle_tcn_orbitrap.yml)

## Outputs

- Structured verification report listing each script, preprocessing code location, and pass/fail status
- Confirmation that env[:, 0] is zeroed consistently across all scripts
- Evidence of consistent timing: precursor m/z zeroing before spectrum encoder input

## How to apply

Load and inspect each execution script (e.g., run_fiddle.py, train_rescore.py, test_caffeine.py) that prepares input features for the spectrum encoder. Locate the preprocessing section where the input feature array (env) is constructed before encoder input, and confirm that env[:, 0] (the precursor m/z column) is explicitly set to zero. Document the exact line number, surrounding context, and operation type for each script. Cross-check that the zeroing operation uses the same index, same operation type (direct assignment to zero), and consistent timing relative to encoder instantiation. Generate a structured verification report with pass/fail status for each script; any inconsistency or missing zeroing is a red flag indicating potential prior learning on mass.

## Related tools

- **msfiddle** (CLI and Python API for FIDDLE formula prediction; inspect run_fiddle.py and test_caffeine.py within this package to verify spectrum preprocessing and precursor m/z zeroing before TCN encoder input.) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase containing training scripts (train_rescore.py, train_tcn_gpus.py), evaluation scripts (run_fiddle.py), and demo scripts (test_caffeine.py); use to locate and verify spectrum preprocessing and precursor m/z zeroing logic across all three main execution paths.) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- Presence of explicit line(s) setting env[:, 0] = 0 (or equivalent zeroing operation) in the preprocessing section of each script.
- Consistent index (0) and operation type (direct assignment to zero) across all three scripts (run_fiddle.py, train_rescore.py, test_caffeine.py).
- Timing verification: the zeroing operation occurs after env array construction but before passing to the TCN encoder (or spectrum encoding layer).
- No conditional logic or exceptions that skip zeroing for certain data splits or input types.
- Code search for alternative precursor m/z references (e.g., 'pepmass', 'precursor_mz', 'env[:, 0]' in non-zeroed contexts) returns no matches in the encoder input path.

## Limitations

- This skill requires access to source code; it cannot validate preprocessing in closed-source or compiled models.
- Zeroing env[:, 0] is necessary but not sufficient; other metadata columns (e.g., collision energy, charge state) may also leak information if not properly handled.
- The skill assumes a fixed precursor m/z location at index 0; non-standard feature orderings (e.g., precursor m/z at a different index) require adaptation.
- Repository README and CHANGELOG lack explicit discussion of methodological constraints or limitations, so edge cases (e.g., spectra with missing or invalid precursor m/z) may not be documented.

## Evidence

- [other] Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts in the FIDDLE codebase?: "Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts in the FIDDLE codebase?"
- [other] Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder.: "Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder."
- [other] Verify consistency of the zeroing operation across all three scripts (same index, same operation, same timing relative to encoder input).: "Verify consistency of the zeroing operation across all three scripts (same index, same operation, same timing relative to encoder input)."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction."
- [readme] See [`test_caffeine.py`](./test_caffeine.py) for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS.: "See [`test_caffeine.py`](./test_caffeine.py) for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS."
