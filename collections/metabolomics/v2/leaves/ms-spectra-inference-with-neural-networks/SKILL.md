---
name: ms-spectra-inference-with-neural-networks
description: Use when you have MGF or native MS/MS arrays (mz_array, intensity_array,
  precursor_mz, adduct) and want to predict the most likely molecular formula. The
  input spectra must include required MGF fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE,
  COLLISION_ENERGY) or equivalent Python API parameters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msfiddle
  - FIDDLE
  - BUDDY (msbuddy)
  - SIRIUS
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

# ms-spectra-inference-with-neural-networks

## Summary

Apply a pre-trained deep neural network (FIDDLE) to predict molecular formulas directly from tandem MS/MS spectra, using a two-stage architecture (TCN for initial prediction + Siamese rescore model for ranking candidates). This skill is essential when you need rapid, high-accuracy formula assignment from high-resolution mass spectrometry without external tools like SIRIUS or BUDDY.

## When to use

You have MGF or native MS/MS arrays (mz_array, intensity_array, precursor_mz, adduct) and want to predict the most likely molecular formula. The input spectra must include required MGF fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) or equivalent Python API parameters. Use this skill when you need fast batch inference on Orbitrap or Q-TOF instruments without relying on external formula annotation tools.

## When NOT to use

- Input spectra are from low-resolution instruments (e.g., ion traps, older TOF systems) not explicitly supported by Orbitrap or Q-TOF models; accuracy may degrade significantly.
- You require post-hoc integration of BUDDY or SIRIUS structure elucidation results; use the native tool outputs directly or refer to msfiddle's deprecated CSV input formats (deprecated in msfiddle 3.0.0).
- Spectra lack required MGF fields (PRECURSOR_TYPE, COLLISION_ENERGY) or the collision energy is unknown and cannot be reliably inferred; the model may produce lower-confidence candidates.

## Inputs

- MGF file with required fields: TITLE, PEPMASS/PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY, and peak list (mz/intensity pairs)
- MS/MS spectrum as native Python arrays: mz_array (float list), intensity_array (float list), precursor_mz (float), adduct (string, e.g. '[M+H]+'), collision_energy (float or 'Unknown')
- Pre-trained model checkpoint files: fiddle_tcn_*.pt and fiddle_rescore_*.pt (from zenodo or msfiddle-download-models)

## Outputs

- CSV file with one row per spectrum, containing columns: ID, Mass, Pred Formula, Pred Mass, Pred Atom Num, Pred H/C Num, Refined Formula (0..4), Refined Mass (0..4), Rescore (0..4)
- Python list of candidate dictionaries, each with keys: formula (string), score (float 0–1), mass (float), metadata (dict)
- Ranked set of molecular formula candidates with confidence scores from the Siamese rescore model

## How to apply

Load the pre-trained FIDDLE checkpoint (TCN + rescore model) for your instrument type (orbitrap or qtof) from the zenodo deposit or via msfiddle-download-models. For single spectra, call predict_from_spectrum() with mz_array, intensity_array, precursor_mz, adduct, collision_energy, and instrument_type. For batched predictions, instantiate MsFiddlePredictor once and call predict_batch() on a list of spectrum dictionaries, which avoids reloading checkpoints. The model outputs ranked formula candidates with rescoring confidence scores; extract the top-k candidates (default top-5) from the Rescore columns in CSV or the candidates list in the API response. Validate output by checking that at least one formula candidate is returned with a non-null score and that the predicted neutral mass is chemically plausible (typically within 5 ppm of the observed precursor mass).

## Related tools

- **msfiddle** (Python API and CLI wrapper for FIDDLE inference; loads pre-trained checkpoints, handles MGF parsing, and outputs scored formula candidates.) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Core research codebase containing the TCN and Siamese rescore model architectures, training scripts, and evaluation benchmarks.) — https://github.com/JosieHong/FIDDLE
- **BUDDY (msbuddy)** (Optional external tool for formula candidate generation; outputs can be integrated alongside FIDDLE predictions via --buddy_path.)
- **SIRIUS** (Optional external tool for formula and structure annotation; outputs can be integrated alongside FIDDLE predictions via --sirius_path.)

## Examples

```
msfiddle --test_data ./demo/input_msms.mgf --instrument_type orbitrap --result_path ./output_fiddle.csv --device 0
```

## Evaluation signals

- Output CSV or API response contains at least one formula candidate with a non-null Rescore (confidence score between 0 and 1).
- Predicted neutral mass (Pred Mass or mass key) matches the observed precursor mass within ±5 ppm, indicating chemically plausible predictions.
- Refined Formula candidates are valid molecular formulas (e.g., C8H10N4O2 for caffeine) with ranks 0–4 corresponding to descending Rescore values.
- When compared to ground-truth formulas (e.g., GNPS or CASMI test sets), rank-1 accuracy and top-5 accuracy align with published FIDDLE benchmark results (typically >90% top-1 on Orbitrap data).
- No null or NaN values in ID, Mass, Pred Formula, or top-1 Rescore columns; missing candidates indicate inference failure or input format errors.

## Limitations

- The rescore model in v2.0.0 uses a Siamese architecture; earlier versions may not be compatible with the same checkpoint format, and results are not directly comparable across versions.
- Accuracy is instrument-dependent: separate Orbitrap and Q-TOF models are required; applying an Orbitrap model to Q-TOF spectra (or vice versa) may produce poor predictions.
- Collision energy is a required or inferred input; unknown or misspecified collision energies can reduce ranking quality of candidates.
- Spectra from chimeric (mixed) compounds or heavily noisy data may produce lower-confidence scores; the model has not been explicitly optimized for those scenarios.
- Predictions are limited to molecular formula; structural isomers cannot be distinguished by FIDDLE alone—integration with BUDDY or SIRIUS is needed for full structure elucidation.

## Evidence

- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra."
- [readme] The rescore model has been redesigned with a Siamese architecture in v2.0.0.: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)."
- [readme] MGF input format requires TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, and COLLISION_ENERGY fields.: "The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`"
- [readme] Python API supports one-off and batched prediction via predict_from_spectrum and MsFiddlePredictor.: "Use `predict_from_spectrum` for one-off prediction from native MS/MS arrays... For repeated or batched prediction, reuse `MsFiddlePredictor` so checkpoints are loaded once"
- [readme] CSV output includes ranked formula candidates with confidence scores (Rescore columns 0–4).: "| `Refined Formula (0..4)` | Ranked refined formula candidates for the default top-5 output. | | `Rescore (0..4)` | Confidence scores for the default top-5 refined candidates. |"
- [other] The model workflow includes an initial TCN prediction stage followed by Siamese rescore ranking.: "The rescore model in FIDDLE v2.0.0 has been redesigned with a Siamese architecture, which is the operative inference architecture for the test."
- [readme] Predictions can be validated against known formulas and benchmarks (CASMI, NIST23, EMBL-MCF).: "Evaluate on external benchmarks (CASMI 2016, CASMI 2017, EMBL-MCF 2.0)"
