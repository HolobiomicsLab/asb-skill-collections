---
name: mass-spectrometry-preprocessing
description: Use when when you have raw mass-spectrometry data (precursor m/z, ionization mode, and fragment m/z–intensity pairs) that must be fed into a CNN model for metabolite annotation via compound fingerprint prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - TensorFlow
  - PyTorch
  - scikit-learn
  - Open Babel
  - PyFingerprint
derived_from:
- doi: 10.1007/s11306-020-01726-7
  title: MetFID
evidence_spans:
- No usage/docs found.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfid_cq
    doi: 10.1007/s11306-020-01726-7
    title: MetFID
  dedup_kept_from: coll_metfid_cq
schema_version: 0.2.0
---

# mass-spectrometry-preprocessing

## Summary

Preparation and normalization of mass-spectrometry spectral data (m/z and intensity arrays) into a format compatible with machine learning input layers, specifically for CNN-based compound fingerprint prediction. This skill ensures spectral matrices are properly structured, intensity-normalized, and aligned for downstream model ingestion.

## When to use

When you have raw mass-spectrometry data (precursor m/z, ionization mode, and fragment m/z–intensity pairs) that must be fed into a CNN model for metabolite annotation via compound fingerprint prediction. Apply this skill before training or inference with a neural network expecting fixed-dimension spectral tensors.

## When NOT to use

- Input is already a pre-trained CNN model checkpoint (.h5 weights file); use model loading instead.
- Spectral data is already in a neural network–ready format (e.g., pre-binned NumPy arrays); skip to model inference.
- Analysis goal is exploratory (e.g., library matching or cosine similarity ranking) rather than CNN fingerprint prediction; consider traditional spectral similarity metrics instead.

## Inputs

- Raw mass-spectrometry spectral data file (txt format with precursor m/z, ionization mode, and m/z–intensity pairs)
- List of candidate InChIKeys for validation/ranking
- Specification of target CNN input tensor shape and intensity normalization scheme

## Outputs

- Preprocessed spectral matrices (fixed-dimension arrays compatible with CNN input layer)
- Normalized intensity tensors (range-scaled to model training specification)
- Matched spectrum–candidate metadata mapping for downstream scoring

## How to apply

Load mass-spectrometry input data specifying precursor mass, ionization mode (positive/negative), and intensity pairs (m/z and normalized intensity values). Construct spectral matrices by binning or aligning fragment m/z values into fixed-dimension arrays, normalizing intensities (e.g., base peak = 100) to a consistent scale. Ensure the resulting tensor shape matches the CNN input layer dimensions (e.g., 1D or 2D convolution kernel expectations). Validate that all spectra in a batch have identical dimensions and that intensity ranges fall within [0, 1] or [0, 100] as the model was trained on. Save preprocessed data in a format (e.g., NumPy arrays or HDF5) that the TensorFlow/PyTorch training pipeline can directly consume.

## Related tools

- **TensorFlow** (Framework for defining CNN input layer shape and loading preprocessed spectral tensors during training and inference) — https://www.tensorflow.org/
- **PyTorch** (Alternative deep learning framework for constructing and training CNN models on preprocessed spectral data)
- **Open Babel** (Converts chemical structures (InChIKey) to molecular fingerprints for comparison against CNN predictions) — https://openbabel.org/wiki/Python
- **PyFingerprint** (Generates molecular fingerprints from compounds for ground-truth labels during CNN training) — https://github.com/hcji/PyFingerprint

## Examples

```
python3 main.py
```

## Evaluation signals

- All preprocessed spectra have identical tensor dimensions matching the CNN input layer specification (e.g., shape [1, sequence_length] for 1D convolution).
- Intensity values are normalized to the expected range (0–1 or 0–100) with no NaN or infinite values.
- Precursor m/z and ionization mode are correctly paired with their corresponding fragment intensity arrays.
- Batch-wise preprocessing is reproducible: running the same spectrum through preprocessing yields bitwise-identical output tensors.
- CNN model successfully ingests the preprocessed data without shape mismatch errors or type casting warnings.

## Limitations

- Spectral matrices must be padded or trimmed to a fixed dimension; spectra with very few fragments or many overlapping peaks may lose information or require aggressive quantization.
- Intensity normalization scheme (e.g., base peak = 100) assumes a consistent ionization and detection response; spectra from different instruments or modes may require separate normalization.
- The method does not validate chemical plausibility of the candidate InChIKey list; incorrect or out-of-distribution compounds will still yield CNN scores.
- No mechanism is provided to handle missing or corrupt m/z–intensity pairs; malformed input rows will cause parsing errors.

## Evidence

- [other] Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer.: "Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer."
- [readme] The first row represents the precursor mass and ionization mode, followed by intensity pairs.: "The first row represents the precursor mass and ionization mode, followed by intensity pairs."
- [other] Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance.: "Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance."
- [readme] The second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score.: "The second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score."
