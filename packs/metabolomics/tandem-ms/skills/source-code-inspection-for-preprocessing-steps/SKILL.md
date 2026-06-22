---
name: source-code-inspection-for-preprocessing-steps
description: Use when when you need to verify that a specific data transformation (e.g., precursor m/z zeroing, feature scaling, or field masking) is applied consistently across multiple execution workflows (training, evaluation, inference) in a codebase.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Source code inspection for preprocessing steps

## Summary

Systematically inspect and trace preprocessing operations (e.g., feature normalization, array zeroing, format conversions) across multiple execution scripts to verify consistency and document the exact locations and timing of data transformations before model input. This skill is essential for validating that prior learning biases are prevented and that preprocessing is reproducibly applied.

## When to use

When you need to verify that a specific data transformation (e.g., precursor m/z zeroing, feature scaling, or field masking) is applied consistently across multiple execution workflows (training, evaluation, inference) in a codebase. Use this skill when the preprocessing step is known to affect model behavior or fairness (e.g., preventing mass-based prior learning) and requires audit across all code paths that feed data to a model.

## When NOT to use

- The preprocessing operation is documented only in configuration files (YAML, JSON) without code-level implementation; instead, parse and validate the config files directly.
- The codebase uses a single centralized preprocessing module (e.g., preprocess.py) applied uniformly across all scripts; inspect that module once rather than tracing across multiple scripts.
- You need to verify runtime behavior (e.g., whether the zeroing actually happens during execution); use dynamic instrumentation or unit tests instead.

## Inputs

- Python execution scripts (e.g., run_fiddle.py, train_rescore.py, test_caffeine.py)
- Repository file tree or source code directory
- Specification of the preprocessing operation to audit (e.g., 'env[:, 0] = 0')

## Outputs

- Structured verification report (CSV, JSON, or text table) with columns: script name, file path, line number(s), preprocessing code snippet, consistency status (pass/fail)
- Diff or side-by-side comparison of preprocessing implementations across scripts
- Evidence log documenting exact locations and contexts of the transformation

## How to apply

Identify the three or more main execution scripts (e.g., run_fiddle.py, train_rescore.py, test_caffeine.py) that process input data. For each script, locate the section where the input feature array (env) is constructed before passing to the model encoder. Search for the specific transformation operation (e.g., env[:, 0] = 0) and record its exact line number, surrounding code context, and timing relative to encoder invocation. Cross-compare the three implementations for consistency: verify the same index, operation, and pre-encoder timing across all scripts. Document any deviations. Generate a verification report listing script name, preprocessing code location (file:line), the transformation code snippet, and a pass/fail status for consistent application.

## Related tools

- **msfiddle** (CLI and Python API for FIDDLE inference; primary tool executing the preprocessing steps under audit) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Deep learning method repository containing the training, evaluation, and inference scripts to be inspected for preprocessing consistency) — https://github.com/JosieHong/FIDDLE

## Examples

```
# Inspect run_fiddle.py for precursor m/z zeroing
grep -n "env\[:, 0\]\|precursor_mz" ./run_fiddle.py | head -20
# Then compare with train_rescore.py and test_caffeine.py
for script in run_fiddle.py train_rescore.py test_caffeine.py; do echo "=== $script ==="  && grep -B2 -A2 "env\[:, 0\] = 0" $script; done
```

## Evaluation signals

- All three scripts (run_fiddle.py, train_rescore.py, test_caffeine.py) contain the same preprocessing operation (e.g., env[:, 0] = 0) at the same array index and with identical syntax.
- The preprocessing operation is applied immediately before the spectrum is passed to the TCN encoder, with no intervening transformations.
- Verification report shows 100% pass status across all scripts with no deviations in index, operation, or timing.
- Diff of preprocessing sections across scripts shows zero or only cosmetic differences (whitespace, variable naming); no logic differences.
- Code inspection confirms that the zeroed field (e.g., precursor m/z) is not re-populated or modified after zeroing and before encoder input.

## Limitations

- This skill inspects static source code and cannot detect runtime behavior changes (e.g., if a script dynamically loads a different preprocessing module or if the zeroing is conditionally applied based on runtime flags).
- The skill requires manual identification of the exact preprocessing operation signature; if the operation is abstracted or obfuscated (e.g., via function calls with generic names), tracing becomes difficult and may require code execution or dynamic analysis.
- Consistency verification is snapshot-based; if scripts are updated independently over time, this inspection must be re-run to detect drift.
- The skill does not validate the correctness or necessity of the preprocessing operation itself—only that it is consistently applied across scripts.

## Evidence

- [other] Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder.: "Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder."
- [other] Confirm that env[:, 0] is set to zero in each script and document the exact line(s) and context.: "Confirm that env[:, 0] is set to zero in each script and document the exact line(s) and context."
- [other] Verify consistency of the zeroing operation across all three scripts (same index, same operation, same timing relative to encoder input).: "Verify consistency of the zeroing operation across all three scripts (same index, same operation, same timing relative to encoder input)."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction."
- [readme] The input format is `mgf`, where `title`, `precursor_mz`, `precursor_type`, `collision_energy` fields are required.: "The input format is `mgf`, where `title`, `precursor_mz`, `precursor_type`, `collision_energy` fields are required."
