---
name: tcn-encoder-input-preprocessing
description: Use when when reproducing or auditing FIDDLE's formula prediction pipeline,
  or when implementing the TCN encoder in your own codebase and need to confirm that
  the precursor m/z (env[:, 0]) has been removed from the feature vector to avoid
  leakage of mass information into the model's learned.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3070
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tcn-encoder-input-preprocessing

## Summary

Verify that precursor m/z values are consistently zeroed in the input feature array before passing spectra to the temporal convolutional network (TCN) encoder in FIDDLE, preventing mass-based prior learning that would bias molecular formula prediction.

## When to use

When reproducing or auditing FIDDLE's formula prediction pipeline, or when implementing the TCN encoder in your own codebase and need to confirm that the precursor m/z (env[:, 0]) has been removed from the feature vector to avoid leakage of mass information into the model's learned representations.

## When NOT to use

- When the precursor m/z is required as a model input (e.g., for mass refinement or ranking tasks that explicitly use the neutral mass)
- When implementing a variant of FIDDLE that intentionally uses mass information as a supervised signal during training
- When analyzing a different mass spectrometry model that does not claim independence from precursor mass information

## Inputs

- spectrum feature array (env) with precursor m/z in index 0
- Python execution scripts (run_fiddle.py, train_rescore.py, test_caffeine.py)
- configuration YAML files for TCN model
- MGF input file with PRECURSOR_MZ field

## Outputs

- preprocessed feature array with env[:, 0] = 0
- verification report listing script name, preprocessing code location, and pass/fail status
- structured comparison of zeroing operations across three scripts

## How to apply

Load the three main FIDDLE execution scripts (run_fiddle.py, train_rescore.py, test_caffeine.py) and locate the spectrum preprocessing section where the input feature array `env` is assembled before encoder input. Verify that env[:, 0] is explicitly set to zero at the same execution point in all three scripts, ensuring the precursor m/z channel is neutralized before the TCN encoder processes the spectrum. Document the exact line numbers, surrounding context, and confirm the timing of the zeroing operation relative to model inference or training. The zeroing must occur after feature array construction but before the array is passed to the model's forward pass to guarantee no mass information leaks into learned encoder weights.

## Related tools

- **FIDDLE** (Deep learning model for molecular formula prediction from MS/MS spectra; provides the TCN encoder architecture and scripts requiring input preprocessing verification) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package and CLI wrapper for FIDDLE inference; may be used for end-to-end prediction validation to ensure preprocessing is applied correctly) — https://github.com/josiehong/msfiddle

## Examples

```
# Load run_fiddle.py and search for env[:, 0] zeroing:
git clone https://github.com/JosieHong/FIDDLE.git && cd FIDDLE && grep -n "env\[:, 0\]" run_fiddle.py train_rescore.py test_caffeine.py && head -30 run_fiddle.py | grep -A 5 -B 5 'env'
```

## Evaluation signals

- All three scripts (run_fiddle.py, train_rescore.py, test_caffeine.py) contain an explicit assignment env[:, 0] = 0 or equivalent masking operation
- The zeroing operation occurs at the same logical step in the preprocessing pipeline across all three scripts (i.e., same position relative to feature normalization and model input)
- Diff comparison of preprocessing blocks in the three scripts shows identical or semantically equivalent zeroing code and timing
- Formula prediction outputs are invariant to changes in input precursor_mz values (i.e., the same spectrum with different precursor m/z values yields the same predicted formula), confirming no mass leakage
- Code review confirms env[:, 0] is zeroed before the array is indexed into the model.forward() call or equivalent encoder input

## Limitations

- The verification scope is limited to the three named scripts; other unofficial FIDDLE implementations or forks may not follow this preprocessing convention
- Zeroing at the wrong execution point (e.g., after encoder inference has already consumed the value) would pass string matching but still fail functional verification
- The check does not verify whether the zeroing operation is actually executed at runtime; static code inspection alone cannot catch conditional or exception-based logic that skips zeroing
- Pre-trained model weights may have been trained with or without proper zeroing; this skill verifies preprocessing code consistency, not historical training practices

## Evidence

- [other] Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts in the FIDDLE codebase?: "Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts"
- [other] Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder.: "Locate the spectrum preprocessing section in each script where env (input feature array) is prepared before passing to the TCN encoder"
- [other] Confirm that env[:, 0] is set to zero in each script and document the exact line(s) and context.: "Confirm that env[:, 0] is set to zero in each script and document the exact line(s) and context"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction"
- [readme] See test_caffeine.py for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS.: "See test_caffeine.py for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS"
