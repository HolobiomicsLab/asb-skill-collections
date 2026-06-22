---
name: pytorch-model-implementation
description: Use when you have preprocessed MS/MS spectral data (m/z and intensity arrays) and need to map it to a fixed-size latent vector for use in an encoder–decoder architecture. Specifically applicable when the downstream task requires a molecular structure reconstruction (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - PyTorch
  - RDKit
derived_from:
- doi: 10.1038/s42004-023-00932-3
  title: Spec2Mol
evidence_spans:
- The implementation of the Spec2Mol architecture is based on the Pytorch library.
- Processing of the chemical data is based on the [RDKit](https://www.rdkit.org/) software.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemprop_ir_cq
    doi: 10.1021/acs.jcim.1c00055
    title: Chemprop-IR
  - build: coll_spec2mol_cq
    doi: 10.1038/s42004-023-00932-3
    title: Spec2Mol
  dedup_kept_from: coll_spec2mol_cq
schema_version: 0.2.0
---

# pytorch-model-implementation

## Summary

Implement a PyTorch neural network encoder that transforms MS/MS spectra into fixed-dimension embedding vectors for downstream molecular structure prediction. This skill bridges raw spectral data and learned representations suitable for sequence-to-sequence decoding.

## When to use

Use this skill when you have preprocessed MS/MS spectral data (m/z and intensity arrays) and need to map it to a fixed-size latent vector for use in an encoder–decoder architecture. Specifically applicable when the downstream task requires a molecular structure reconstruction (e.g., SMILES generation) conditioned on spectral information.

## When NOT to use

- Input spectra are already embedded or featurized; use this skill only on raw or minimally preprocessed MS/MS data.
- Task does not require a learned latent representation (e.g., direct spectral fingerprinting or rule-based matching may suffice).
- Embedding dimension or spectral preprocessing requirements are unknown and cannot be inferred from downstream tasks.

## Inputs

- MS/MS spectral data (CSV or array format with m/z values and intensity values)
- Preprocessed spectral tensors (normalized intensity arrays indexed by m/z)
- PyTorch tensor of shape [batch_size, spectral_feature_dim]

## Outputs

- Fixed-dimension embedding vectors (PyTorch tensor of shape [batch_size, embedding_dim])
- Encoder neural network module (PyTorch model)

## How to apply

First, normalize and preprocess MS/MS spectra by scaling intensities and binning m/z values into a standardized input format (typically intensity arrays indexed by m/z). Define a sequential PyTorch neural network consisting of fully connected or convolutional layers that progressively reduce spectral dimensionality to a target embedding dimension. Initialize encoder weights and implement a forward pass that maps spectral tensors to embedding vectors. Validate that all encoder outputs have consistent shape and dtype (e.g., all embeddings are float32 tensors of shape [batch_size, embedding_dim]). Train or load pretrained weights, then test the encoder on held-out spectra to confirm it produces deterministic, fixed-dimension embeddings.

## Related tools

- **PyTorch** (Core framework for defining, initializing, and executing the encoder neural network layers and forward pass)
- **RDKit** (Preprocessing and validation of chemical data; conversion of molecular structures to SMILES and vice versa) — https://www.rdkit.org/

## Examples

```
python predict_embs.py -pos_low_file 'sample_data/[M+H]_low.csv' -pos_high_file 'sample_data/[M+H]_high.csv' -neg_low_file 'sample_data/[M-H]_low.csv' -neg_high_file 'sample_data/[M-H]_high.csv'
```

## Evaluation signals

- Encoder produces tensors with consistent shape [batch_size, embedding_dim] for all inputs.
- Output dtype is correct (typically float32) and reproducible across repeated inference runs.
- Embedding values are within expected numerical range (no NaN, Inf, or extreme outliers).
- Downstream decoder successfully uses encoder embeddings to reconstruct molecular structures.
- Test spectra from the training distribution produce lower reconstruction error than out-of-distribution spectra (qualitative sanity check).

## Limitations

- The encoder was trained on the NIST Tandem Mass Spectral Library 2020, which is a commercial dataset; performance on spectra from other sources or ionization methods may degrade.
- Input spectra must be provided in the four-ionization-mode format (pos_low [M+H]+ 35% NCE, pos_high [M+H]+ 130% NCE, neg_low [M-H]- 35% NCE, neg_high [M-H]- 130% NCE) as expected by Spec2Mol.
- No changelog or version history is available in the repository, limiting reproducibility across time.

## Evidence

- [intro] The encoder module in Spec2Mol transforms MS/MS spectra into a fixed embedding vector: "The encoder creates an embedding from a given set of MS/MS spectra"
- [other] Preprocessing steps normalize spectral data before encoder input: "Normalize and preprocess spectra (e.g., intensity scaling, m/z binning) as required by the encoder input layer"
- [readme] PyTorch is the primary framework for the encoder implementation: "The implementation of the Spec2Mol architecture is based on the Pytorch library"
- [other] Encoder outputs must be validated for fixed dimensionality and dtype: "Validate that encoder output produces fixed-dimension embeddings (vector shape and dtype) for test spectra"
- [readme] Input spectra are provided as CSV files with m/z and intensity columns: "Each csv file has the m/z values in the first column and the intensity values in the second column"
- [readme] Encoder is part of an encoder–decoder architecture for SMILES reconstruction: "The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates"
