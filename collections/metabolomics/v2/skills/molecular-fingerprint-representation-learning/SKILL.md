---
name: molecular-fingerprint-representation-learning
description: Use when when you have labeled mass-spectrometry spectral data (precursor m/z and fragment m/z–intensity pairs) paired with known molecular structures (as InChIKeys or SMILES), and need to perform metabolite annotation by ranking candidate compounds based on spectral similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3369
  tools:
  - TensorFlow
  - PyTorch
  - scikit-learn
  - PyFingerprint
  - RDKit
  - PubChemPy
  - Open Babel
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

# molecular-fingerprint-representation-learning

## Summary

Train and apply a CNN-based model to predict molecular fingerprints from mass-spectrometry data, enabling compound annotation through learned spectral-to-fingerprint representation mapping. This skill converts raw m/z and intensity arrays into fixed-length fingerprint vectors that encode structural similarity for metabolite identification.

## When to use

When you have labeled mass-spectrometry spectral data (precursor m/z and fragment m/z–intensity pairs) paired with known molecular structures (as InChIKeys or SMILES), and need to perform metabolite annotation by ranking candidate compounds based on spectral similarity. Apply this skill when traditional rule-based fingerprinting is insufficient and you have sufficient training data to learn spectral feature patterns.

## When NOT to use

- Input spectra lack intensity normalization or precursor m/z metadata — preprocessing is required before model input.
- You have fewer than ~100 labeled training spectra with known structures — CNN models require sufficient data to learn meaningful spectral patterns without severe overfitting.
- Query compounds are outside the chemical space of the training set — fingerprint predictions will be unreliable on structurally novel molecules.

## Inputs

- mass-spectrometry spectral data (m/z–intensity pairs formatted as precursor m/z, ionization mode, then fragment m/z and normalized intensity values)
- reference molecular fingerprints or InChIKeys for training/validation compounds
- training/validation spectral data split with known true compound identities

## Outputs

- trained CNN model weights and architecture (.h5 or equivalent checkpoint)
- predicted molecular fingerprint vectors (binary or continuous) for query spectra
- Tanimoto similarity scores ranking candidate compounds for each query spectrum
- ranked InChIKey predictions with similarity scores per spectrum

## How to apply

Prepare training data by loading MS spectra as normalized m/z–intensity matrices or precursor-fragment arrays, paired with reference molecular fingerprints (e.g., Morgan or RDKit fingerprints converted to binary vectors). Design a CNN architecture with convolutional layers to extract spectral patterns, pooling to aggregate features, and dense output layers producing fingerprint-length binary or continuous vectors. Train using binary cross-entropy or Tanimoto-based loss with validation monitoring to prevent overfitting. After training, compute Tanimoto similarity scores between predicted fingerprints and candidate compound fingerprints, ranking candidates by descending score. Evaluate on a held-out test set to confirm the model generalizes across unknown spectra.

## Related tools

- **TensorFlow** (Deep learning framework for implementing and training the CNN model architecture) — https://www.tensorflow.org/
- **PyTorch** (Alternative deep learning framework for CNN model construction and optimization)
- **PyFingerprint** (Library for computing reference molecular fingerprints used as training targets) — https://github.com/hcji/PyFingerprint
- **RDKit** (Cheminformatics toolkit for fingerprint generation and Tanimoto similarity computation)
- **PubChemPy** (Python client for retrieving compound structures and fingerprints from PubChem) — https://pubchempy.readthedocs.io/en/latest/guide/install.html
- **Open Babel** (Chemical structure converter and fingerprint generator for reference compounds) — https://openbabel.org/wiki/Python
- **scikit-learn** (Machine learning utilities for data splitting, preprocessing, and evaluation metrics)

## Examples

```
python3 main.py
```

## Evaluation signals

- Validation loss plateaus and test Tanimoto similarity scores are consistent with training performance (no catastrophic overfitting).
- For known test spectra, the true compound InChIKey ranks in the top 1–3 predictions with Tanimoto score > 0.5.
- Model predictions on independent MS datasets show rank-1 accuracy > 60% and mean reciprocal rank (MRR) > 0.7 when candidate lists are provided.
- Output file format matches expected structure: ranked InChIKeys with descending Tanimoto scores per spectrum, separated by spectrum ID blocks.
- Fingerprint prediction dimensionality matches the reference fingerprint length (e.g., 2048 bits for Morgan fingerprints); no NaN or out-of-range values in output scores.

## Limitations

- Model performance degrades on spectra from instruments or ionization modes not represented in training data.
- CNN fingerprint predictions are black-box; interpretation of which spectral fragments drive predictions is not directly accessible.
- Tanimoto similarity threshold for accepting a prediction as correct is dataset- and application-dependent; no universal cutoff is provided.
- Requires a pre-trained or newly trained model (.h5 file); no model is shipped with the repository, and training data collection is labor-intensive.

## Evidence

- [other] MetFID implements a CNN-based approach for predicting compound fingerprints from mass-spectrometry data, serving as the core predictor component for metabolite annotation.: "MetFID implements a CNN-based approach for predicting compound fingerprints from mass-spectrometry data, serving as the core predictor component for metabolite annotation."
- [other] Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer. Design a CNN architecture with appropriate convolutional, pooling, and dense layers to map spectral features to fingerprint vector outputs.: "Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer. Design a CNN architecture with appropriate"
- [other] Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance.: "Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance."
- [readme] The first row represents the precursor mass and ionization mode, followed by intensity pairs.: "The first row represents the precursor mass and ionization mode, followed by intensity pairs."
- [readme] The first column represents the `InChIKeys`, and the second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score.: "The first column represents the `InChIKeys`, and the second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score."
