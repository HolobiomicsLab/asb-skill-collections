---
name: tensor-preprocessing-normalization
description: Use when when you have raw MS/MS spectral data in the form of intensity arrays indexed by m/z values and need to feed them into the Spec2Mol encoder neural network. Apply this skill before encoder inference to ensure spectral inputs conform to the encoder's expected dimensionality and value ranges.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - PyTorch
derived_from:
- doi: 10.1038/s42004-023-00932-3
  title: Spec2Mol
evidence_spans:
- Processing of the chemical data is based on the [RDKit](https://www.rdkit.org/) software.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spec2mol_cq
    doi: 10.1038/s42004-023-00932-3
    title: Spec2Mol
  dedup_kept_from: coll_spec2mol_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42004-023-00932-3
  all_source_dois:
  - 10.1038/s42004-023-00932-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tensor Preprocessing and Normalization

## Summary

Normalize and preprocess MS/MS spectral data into tensor form suitable for neural network input, including intensity scaling and m/z binning. This step is essential for converting raw mass spectrometry output into fixed-dimension embeddings that encode chemical information.

## When to use

When you have raw MS/MS spectral data in the form of intensity arrays indexed by m/z values and need to feed them into the Spec2Mol encoder neural network. Apply this skill before encoder inference to ensure spectral inputs conform to the encoder's expected dimensionality and value ranges.

## When NOT to use

- Input is already in the form of fixed-dimension embedding vectors (skip directly to decoder).
- Spectral data is in a proprietary binary format not convertible to CSV m/z–intensity pairs.
- You are using a different deep learning framework (e.g., TensorFlow) where PyTorch tensor I/O is not applicable.

## Inputs

- CSV files with m/z values (column 1) and intensity values (column 2)
- MS/MS spectra in four ionization modes: [M+H]+ at 35% NCE, [M+H]+ at 130% NCE, [M-H]- at 35% NCE, [M-H]- at 130% NCE

## Outputs

- PyTorch tensors of normalized intensities with fixed shape matching encoder input layer
- Preprocessed spectra with scaled intensities and binned m/z domain

## How to apply

Load MS/MS spectral data in standardized format (m/z values in first column, intensity values in second column, comma-separated). Apply intensity scaling (e.g., normalization to [0,1] or log-scale transformation) and m/z binning to discretize the spectral domain into fixed bins aligned with the encoder's input layer dimensions. Convert the preprocessed spectra into PyTorch tensors with consistent shape and dtype (e.g., float32). The preprocessing must preserve chemical information while reducing high-dimensional raw spectra to a fixed-size tensor that the encoder's sequential layers can process to generate the embedding vector.

## Related tools

- **PyTorch** (Create and manipulate normalized spectral tensors and define forward pass through encoder layers)
- **RDKit** (Validate chemical plausibility of preprocessed spectra and support intensity/m/z coordinate transformations) — https://www.rdkit.org/

## Examples

```
python predict_embs.py -pos_low_file 'sample_data/[M+H]_low.csv' -pos_high_file 'sample_data/[M+H]_high.csv' -neg_low_file 'sample_data/[M-H]_low.csv' -neg_high_file 'sample_data/[M-H]_high.csv'
```

## Evaluation signals

- Output tensor shape matches encoder input layer dimensions (e.g., fixed-size vector or matrix).
- Intensity values fall within expected normalized range (e.g., [0, 1] or log-scaled bounds).
- No NaN or Inf values present in output tensors after normalization.
- Encoder forward pass executes without shape mismatch errors when fed preprocessed tensors.
- Multiple spectra from the same compound produce identical or near-identical embeddings, indicating reproducible preprocessing.

## Limitations

- Preprocessing is specific to the four ionization modes and collision energies used in NIST 2020 training set; spectra from different ionization protocols may require retraining or transfer learning.
- m/z binning strategy is not explicitly detailed in the article; practitioners must match the encoder's expected input dimensions by inferring or reverse-engineering the original preprocessing pipeline.
- No validation data or thresholds provided for intensity scaling decisions (e.g., log vs. linear, clipping strategy), so preprocessing parameters may require empirical tuning.

## Evidence

- [other] Normalize and preprocess spectra (e.g., intensity scaling, m/z binning) as required by the encoder input layer.: "Normalize and preprocess spectra (e.g., intensity scaling, m/z binning) as required by the encoder input layer."
- [other] Load MS/MS spectral data in a standardized format (e.g., intensity arrays indexed by m/z values).: "Load MS/MS spectral data in a standardized format (e.g., intensity arrays indexed by m/z values)."
- [readme] Each csv file has the m/z values in the first column and the intensity values in the second column. The columns are separated with commas.: "Each csv file has the m/z values in the first column and the intensity values in the second column. The columns are separated with commas."
- [intro] The endoder creates an embedding from a given set of MS/MS spectra.: "The endoder creates an embedding from a given set of MS/MS spectra."
- [readme] The implementation of the Spec2Mol architecture is based on the Pytorch library.: "The implementation of the Spec2Mol architecture is based on the Pytorch library."
