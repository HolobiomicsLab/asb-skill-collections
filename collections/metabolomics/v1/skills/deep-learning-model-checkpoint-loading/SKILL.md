---
name: deep-learning-model-checkpoint-loading
description: Use when when you have MS/MS spectra from GNPS or other libraries and need to apply a pre-trained FIDDLE model (TCN formula predictor or Siamese rescore architecture) without training from scratch. Use this skill before running inference on new samples or benchmarks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3172
  tools:
  - msfiddle
  - FIDDLE
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
- doi: 10.5281/zenodo.19181279
  title: ''
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

# Deep-Learning Model Checkpoint Loading

## Summary

Load pre-trained neural network weights from disk checkpoints to enable inference without retraining. This skill is essential for applying trained FIDDLE models to new MS/MS spectra or batch predictions.

## When to use

When you have MS/MS spectra from GNPS or other libraries and need to apply a pre-trained FIDDLE model (TCN formula predictor or Siamese rescore architecture) without training from scratch. Use this skill before running inference on new samples or benchmarks.

## When NOT to use

- Input checkpoints are from different FIDDLE versions with incompatible architectures (e.g., v1.x with pre-Siamese rescore vs. v2.0.0 Siamese rescore) without retesting on reference data.
- You are training a new model from scratch—use training scripts instead; checkpoint loading assumes weights are already optimized.
- Instrument type (Orbitrap vs. Q-TOF) does not match your spectra—load the corresponding instrument-specific checkpoint or retraining will be needed.

## Inputs

- Trained PyTorch checkpoint file (.pt) for TCN formula prediction model
- Trained PyTorch checkpoint file (.pt) for rescore model (Siamese architecture)
- YAML configuration file specifying model architecture parameters
- MS/MS spectrum data in MGF format with required fields: TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY

## Outputs

- Loaded PyTorch model object in memory ready for inference
- CSV file with scored formula candidates per spectrum (columns: ID, Mass, Pred Formula, Refined Formula (0..4), Rescore (0..4))
- JSON/structured output with ranked formula candidates and confidence scores

## How to apply

Download pre-trained checkpoint files (e.g., `fiddle_tcn_orbitrap.pt` and `fiddle_rescore_orbitrap.pt`) from the FIDDLE release page or Zenodo deposit (DOI 10.5281/zenodo.19181279) and place them in the `./check_point/` directory. For CLI workflows, run `msfiddle-download-models` to fetch checkpoints to the default location (`~/.msfiddle/check_point`). Specify checkpoint paths explicitly using `--resume_path` (TCN model) and `--rescore_resume_path` (rescore model) flags, or pass them programmatically to the `MsFiddlePredictor` constructor. The rescore model in v2.0.0 uses a redesigned Siamese architecture that rescores initial formula predictions; ensure your checkpoint version matches your expected architecture. Validate the loaded model by running on a known reference sample (e.g., caffeine from GNPS) and checking that output CSV/JSON contains scored formula candidates.

## Related tools

- **msfiddle** (Command-line and Python API wrapper for FIDDLE inference; provides download-models subcommand and high-level predict functions that handle checkpoint loading internally) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Deep learning method research codebase; contains lower-level training and evaluation scripts; reference implementation for checkpoint loading via config and resume_path arguments) — https://github.com/JosieHong/FIDDLE

## Examples

```
msfiddle --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- Loaded model successfully initializes without shape mismatch or device errors; checkpoint file size and modification date match expected release.
- Running inference on reference caffeine Orbitrap spectrum from GNPS produces output CSV with caffeine formula (C8H10N4O2) ranked in top-5 candidates with non-zero rescore confidence.
- Output CSV schema matches specification: contains ID, Mass, Pred Formula, Refined Formula (0..4), Refined Mass (0..4), Rescore (0..4) columns with numeric scores in valid range [0, 1].
- Model inference latency and GPU/CPU utilization are consistent with documented expectations (checkpoint loaded once, reused across batch predictions).
- Results on external benchmark (CASMI 2016/2017, EMBL-MCF 2.0, NIST23) match published FIDDLE accuracy metrics within sampling variance.

## Limitations

- Checkpoint must match the installed PyTorch and Python versions; mismatched CUDA/ROCm builds may cause silent inference errors or degraded performance. Test on a small reference set first.
- Siamese rescore architecture in v2.0.0 is a breaking change from v1.x; old v1.x checkpoints will not load without explicit version alignment or retraining.
- Instrument-specific checkpoints (Orbitrap vs. Q-TOF) are not interchangeable; applying Orbitrap-trained weights to Q-TOF spectra or vice versa will produce inaccurate predictions.
- No explicit discussion section in source documents; reproducibility gaps and failure modes (e.g., behavior on spectra from unlisted collision energies, extreme m/z ranges) are not fully documented.

## Evidence

- [readme] To use the pre-trained models, please use the following scripts to download the weights from the release page and place them in the `./check_point/` directory: "To use the pre-trained models, please use the following scripts to download the weights from the [release page](https://github.com/JosieHong/FIDDLE/releases/tag/v1.0.0) and place them in the"
- [readme] The rescore model has been redesigned with a Siamese architecture in version 2.0.0: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)"
- [readme] Download the pre-trained checkpoints before running predictions using msfiddle-download-models command: "Download the pre-trained checkpoints before running predictions: msfiddle-download-models"
- [readme] Loaded models can be reused for efficient batched prediction in Python applications: "Reuse loaded models for efficient batched prediction in Python applications"
- [other] The rescore model in FIDDLE v2.0.0 has been redesigned with a Siamese architecture, which is the operative inference architecture for the test: "The rescore model in FIDDLE v2.0.0 has been redesigned with a Siamese architecture, which is the operative inference architecture for the test"
