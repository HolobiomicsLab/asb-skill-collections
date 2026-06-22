---
name: encoder-decoder-end-to-end-training
description: Use when you have a pretrained encoder that produces fixed-size embeddings from MS/MS spectra (or similar spectral data), a tokenized target dataset of canonical SMILES strings representing molecular structures, and you need to learn a decoder that reliably reconstructs the molecular structure from.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3303
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
---

# encoder-decoder-end-to-end-training

## Summary

Train an encoder-decoder sequence-to-sequence model end-to-end to map fixed-size embeddings (e.g., from MS/MS spectra) to variable-length molecular SMILES token sequences. This skill is essential when you need to reconstruct chemical structures from latent representations, as in de novo molecular structure prediction from mass spectra.

## When to use

You have a pretrained encoder that produces fixed-size embeddings from MS/MS spectra (or similar spectral data), a tokenized target dataset of canonical SMILES strings representing molecular structures, and you need to learn a decoder that reliably reconstructs the molecular structure from the embedding. Apply this skill when exact-match molecular reconstruction accuracy and chemical validity (measured via RDKit parsing and Tanimoto similarity) are critical for your downstream application.

## When NOT to use

- Your encoder has not been trained or validated; train and evaluate the encoder separately first to ensure embedding quality.
- Your target SMILES dataset is not canonicalized or tokenized consistently; preprocessing inconsistency will degrade decoder learning.
- You lack ground-truth reference SMILES for evaluation; you cannot reliably measure exact-match accuracy or Tanimoto similarity without held-out references.

## Inputs

- Pretrained encoder model and its output embeddings (from upstream encoder task or checkpoint)
- SMILES tokenizer configuration
- Dataset of target SMILES strings in canonical form (converted via RDKit)

## Outputs

- Trained decoder model weights (PyTorch checkpoint)
- Validation metrics (exact-match accuracy, Tanimoto similarity scores)
- Reconstructed SMILES strings for test embeddings
- Decoded molecules as RDKit mol objects for chemical validation

## How to apply

Define a sequence-to-sequence decoder architecture in PyTorch with attention mechanisms that maps each fixed-size embedding to a variable-length SMILES token sequence. Prepare your target SMILES dataset by converting molecules to canonical form using RDKit and tokenizing them consistently. Train the decoder end-to-end using cross-entropy loss on token-level predictions, employing teacher forcing during training (feeding ground-truth tokens at each step rather than model predictions). Evaluate on held-out test embeddings by computing exact-match accuracy (percentage of reconstructed SMILES that exactly match reference strings) and Tanimoto similarity (computed via RDKit fingerprints) between original and decoded molecules. Save trained decoder weights and log validation metrics to enable reproducibility and model selection based on held-out performance.

## Related tools

- **PyTorch** (Framework for defining and training the sequence-to-sequence decoder architecture with attention, computing cross-entropy loss on SMILES token predictions, and managing teacher forcing during training.)
- **RDKit** (Converts molecules to canonical SMILES format, tokenizes SMILES strings, computes molecular fingerprints for Tanimoto similarity calculation, and validates reconstructed SMILES by parsing into mol objects.) — https://www.rdkit.org/

## Examples

```
python predict_embs.py -pos_low_file 'sample_data/[M+H]_low.csv' -pos_high_file 'sample_data/[M+H]_high.csv' -neg_low_file 'sample_data/[M-H]_low.csv' -neg_high_file 'sample_data/[M-H]_high.csv'
```

## Evaluation signals

- Exact-match accuracy on held-out test embeddings: percentage of reconstructed SMILES strings that exactly match reference SMILES (higher is better; threshold context-dependent).
- Tanimoto similarity distribution: computed via RDKit fingerprints between original and reconstructed molecules; mean and median should be substantially > 0.7 for meaningful molecular recovery.
- All reconstructed SMILES are valid: all can be parsed by RDKit into mol objects without errors; any parse failure indicates decoder error.
- Loss convergence: training and validation cross-entropy loss should decrease monotonically over epochs and plateau; divergence suggests architectural or hyperparameter issues.
- No token sequence length violations: all reconstructed sequences are within the maximum tokenization length of the training set (indicates decoder learned appropriate stopping behavior).

## Limitations

- Decoder performance depends critically on encoder embedding quality; poor encoder embeddings cannot be recovered by a well-trained decoder.
- Teacher forcing during training can cause exposure bias at inference time; model predictions may degrade when fed its own token predictions rather than ground truth. Consider scheduled sampling or beam search decoding during evaluation.
- Exact-match accuracy is a stringent metric; chemically equivalent molecules represented by different SMILES (e.g., different aromaticity or ring notation) will count as mismatches despite identical chemical structure. Tanimoto similarity and RDKit canonical form comparison are more robust.
- The decoder assumes fixed-size embeddings; variable-size or multi-modal encoder outputs may require architectural adaptation (e.g., attention pooling).
- Training dataset composition (molecular diversity, spectrum quality, ionization modes) directly affects generalization; the original Spec2Mol decoder was trained on the commercial NIST Tandem Mass Spectral Library 2020.

## Evidence

- [intro] The decoder architecture and training procedure.: "The decoder takes an embedding produced by the encoder and reconstructs the molecular structure in SMILES format as its output."
- [readme] Encoder-decoder workflow in Spec2Mol.: "The endoder creates an embedding from a given set of MS/MS spectra. The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates."
- [other] Concrete training methodology with teacher forcing and loss function.: "Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training."
- [other] Evaluation metrics for decoder reconstruction quality.: "Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules (decoded via RDKit)."
- [readme] Primary tools for decoder training and validation.: "The implementation of the Spec2Mol architecture is based on the Pytorch library. Processing of the chemical data is based on the RDKit software."
- [readme] Training dataset provenance.: "The spectra encoder has been trained on the NIST Tandem Mass Spectral Library 2020 which is a commercial dataset."
