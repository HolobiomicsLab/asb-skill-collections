---
name: ms-ms-spectrum-prediction
description: Use when you have MS/MS spectra (in MGF format) with required metadata fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) and need to predict candidate molecular formulas ranked by confidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - msfiddle
  - BUDDY
  - SIRIUS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
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

# MS/MS Spectrum Prediction

## Summary

Use deep learning (FIDDLE v2.0.0 with Siamese-architecture rescore model) to predict molecular formulas from tandem mass spectra (MS/MS), producing ranked formula candidates with confidence scores. This skill is essential when you need to identify unknown compounds from high-resolution MS/MS data without prior structure knowledge.

## When to use

You have MS/MS spectra (in MGF format) with required metadata fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) and need to predict candidate molecular formulas ranked by confidence. Apply this skill when working with Orbitrap or Q-TOF instruments and when integration with external tools (BUDDY, SIRIUS) is optional but beneficial for refining candidates.

## When NOT to use

- Input spectra lack required MGF metadata fields (PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) — preprocessing to standardize headers is needed first.
- MS/MS data are from instruments not covered by pre-trained models (only Orbitrap and Q-TOF supported); retraining on instrument-specific data is required.
- You have already-identified compounds and only need library matching or validation — use spectral library search instead of de novo prediction.

## Inputs

- MGF file with MS/MS spectra (required fields: TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY)
- Pre-trained FIDDLE model checkpoints (TCN and rescore, instrument-specific)
- Configuration YAML file (instrument and model architecture specifications)
- Optional: BUDDY output CSV or SIRIUS formula results for candidate refinement

## Outputs

- CSV file with one row per spectrum, including columns: ID, Mass, Pred Formula, Pred Mass, Pred Atom Num, Pred H/C Num, Refined Formula (0..4), Refined Mass (0..4), Rescore (0..4)
- Ranked molecular formula candidates with confidence scores
- Neutral mass and predicted atom/H-C counts per spectrum

## How to apply

Load the MS/MS spectra via MGF input file format and select the appropriate instrument-specific pre-trained checkpoint (Orbitrap or Q-TOF). Execute the FIDDLE TCN formula-prediction model followed by the Siamese-architecture rescore model (v2.0.0) to generate initial predictions and confidence-ranked refinements. The rescore model re-ranks candidates using learned relationships between spectra and formula properties, producing standardized Rescore (k) output columns for top-5 candidates. Export results to CSV with columns including ID, predicted formula, mass, atom count, H/C count, and ranked refined formulas with associated confidence scores. Validate by checking that output columns are properly labeled, rescore values fall in valid confidence ranges [0–1], and formula masses match theoretical predictions within instrument-specific ppm tolerance.

## Related tools

- **FIDDLE** (Deep learning framework for predicting molecular formulas from MS/MS spectra; contains research codebase for model training, evaluation, and inference) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API wrapper for FIDDLE; handles model download, prediction batching, and output CSV formatting) — https://github.com/josiehong/msfiddle
- **BUDDY** (Optional companion tool for generating candidate formulas; results can be integrated with FIDDLE predictions to refine ranking)
- **SIRIUS** (Optional companion tool for formula identification; outputs can be combined with FIDDLE rescore model to re-rank candidates)

## Examples

```
python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- Output CSV contains all required columns (ID, Pred Formula, Rescore (0..4)) with no missing or NaN values for valid spectra.
- Rescore (k) confidence values are numeric, in range [0, 1], and ranked in descending order for each spectrum (top-1 score ≥ top-2 ≥ ... ≥ top-5).
- Predicted formula masses match theoretical masses within instrument tolerance (typically ±5 ppm for Orbitrap, ±10 ppm for Q-TOF); validate using Pred Mass vs. theoretical neutral mass.
- Refined formulas (0..4) are chemically valid (positive atom counts, obey valence rules); cross-check against Hill system notation or molecular weight ranges.
- When BUDDY or SIRIUS candidates are provided, verify that FIDDLE's top-1 rescore candidate is among the input candidates (indicating successful re-ranking) or check Spearman correlation of FIDDLE rescore ranks vs. input tool ranks to confirm integration.

## Limitations

- Model performance depends on instrument type and collision energy; predictions are optimized for Orbitrap and Q-TOF with standard CID/HCD. Unknown or non-standard collision energies may degrade accuracy.
- Siamese rescore architecture in v2.0.0 is a breaking change; model checkpoints from FIDDLE v1.x are not compatible; v2.0.0 checkpoint assets must be explicitly downloaded.
- MGF input requires complete metadata (PRECURSOR_TYPE, COLLISION_ENERGY); missing fields cause parsing errors or silent skipping depending on workflow.
- Top-k predictions (default k=5) are heuristic refinements; true formula may rank lower if spectrum is noisy, chimeric, or from an out-of-distribution sample pool.
- External tool integration (BUDDY, SIRIUS) expects native/original output formats; deprecated msfiddle-normalized CSV formats are no longer supported and emit DeprecationWarning.

## Evidence

- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction."
- [readme] Siamese architecture redesign in v2.0.0 for rescore model: "Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md"
- [readme] Required MGF fields for input: "The required MGF fields are TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, and COLLISION_ENERGY"
- [readme] Output CSV columns including Rescore (k) scores: "Rescore (0..4): Confidence scores for the default top-5 refined candidates."
- [readme] Workflow steps for running FIDDLE on caffeine test spectrum: "See test_caffeine.py for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS."
- [readme] Integration with BUDDY and SIRIUS for candidate refinement: "If you'd like to integrate the results from SIRIUS and BUDDY, please organize the results in the format shown in ./demo/buddy_output.csv and ./demo/sirius_output.csv, and provide them to run FIDDLE"
- [readme] Instrument-specific model checkpoints: "Orbitrap models: fiddle_tcn_orbitrap.pt: formula prediction model on Orbitrap spectra; fiddle_rescore_orbitrap.pt: rescore model on Orbitrap spectra. Q-TOF models: fiddle_tcn_qtof.pt: formula"
