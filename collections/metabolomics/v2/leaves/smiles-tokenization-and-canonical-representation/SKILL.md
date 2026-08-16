---
name: smiles-tokenization-and-canonical-representation
description: Use when when preparing SMILES strings as training targets for a sequence-to-sequence
  decoder that reconstructs molecular structures from embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3314
  tools:
  - RDKit
  - PyTorch
  license_tier: open
derived_from:
- doi: 10.1038/s42004-023-00932-3
  title: Spec2Mol
evidence_spans:
- Processing of the chemical data is based on the [RDKit](https://www.rdkit.org/)
  software.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES tokenization and canonical representation

## Summary

Convert molecular structures into canonical SMILES strings and tokenize them into variable-length sequences for use as training targets in sequence-to-sequence models. This skill ensures consistent, unambiguous molecular representation suitable for neural decoder training.

## When to use

When preparing SMILES strings as training targets for a sequence-to-sequence decoder that reconstructs molecular structures from embeddings. Apply this skill when you need to standardize molecular representations before feeding them into cross-entropy loss calculations or when comparing reconstructed molecules against reference structures.

## When NOT to use

- Input molecules are already in a standardized canonical form and exact-match accuracy is not required for your application.
- Your decoder is designed to output molecular representations other than SMILES (e.g., SELFIES, molecular graphs, or InChI strings).
- You are evaluating pre-trained decoders on non-molecular sequence tasks where SMILES canonicalization is not applicable.

## Inputs

- SMILES strings (variable-length character sequences representing molecular structures)
- Molecular structure objects (e.g., RDKit Mol objects)
- Decoder embeddings (fixed-size vector representations from encoder)

## Outputs

- Canonical SMILES strings (standardized, unambiguous molecular representations)
- Tokenized SMILES sequences (variable-length integer or token ID sequences)
- SMILES token vocabulary (mapping of unique tokens to integer indices)
- Reconstructed SMILES strings (predicted from decoder output)

## How to apply

Use RDKit to canonicalize SMILES strings, ensuring each molecule has a unique, standardized representation that eliminates isomeric ambiguity. Tokenize the canonical SMILES into individual token sequences (atoms, bonds, brackets, etc.) to create variable-length token sequences aligned with the decoder's output vocabulary. Apply this preprocessing to both training and held-out test SMILES datasets. During training, use teacher forcing with these tokenized sequences as targets for cross-entropy loss computation on SMILES token prediction. During evaluation, reconstruct molecules from decoder predictions by joining tokens back into SMILES strings, then parse them with RDKit to compute exact-match accuracy and Tanimoto similarity against reference molecules.

## Related tools

- **RDKit** (Parse, canonicalize, and validate SMILES strings; reconstruct molecules from SMILES predictions to compute Tanimoto similarity metrics) — https://www.rdkit.org/
- **PyTorch** (Implement tokenization indices in embedding lookup layers and compute cross-entropy loss on SMILES token predictions during decoder training)

## Examples

```
# Canonicalize SMILES and prepare tokenized sequences for decoder training
from rdkit import Chem
import torch

# Load SMILES strings and canonicalize
smiles_list = ['CC(C)Cc1ccc(cc1)C(C)C(O)=O', 'c1ccc(cc1)C(C)C(O)=O']
canonical_smiles = [Chem.MolToSmiles(Chem.MolFromSmiles(s)) for s in smiles_list]

# Tokenize and create vocabulary
vocab = {'C': 0, '(': 1, ')': 2, '=': 3, 'O': 4, 'c': 5, '1': 6}  # example
tokenized = [[vocab[t] for t in s] for s in canonical_smiles]

# Use in training with teacher forcing
for tokens in tokenized:
    loss = criterion(decoder_output, torch.tensor(tokens))
```

## Evaluation signals

- Canonical SMILES strings are consistent across multiple invocations on the same molecule (e.g., different input SMILES isomers produce identical canonical output).
- All tokens in the tokenized sequences map to entries in the vocabulary; no out-of-vocabulary tokens appear in training or validation sets.
- Exact-match accuracy on held-out test set: reconstructed SMILES strings, when canonicalized, match reference SMILES exactly.
- Tanimoto similarity of reconstructed vs. reference molecules (computed via RDKit fingerprints) is ≥ 0.7 for true-positive predictions, indicating structural coherence.
- Cross-entropy loss converges during decoder training when teacher forcing uses these tokenized SMILES as targets.

## Limitations

- RDKit canonicalization may fail or produce unexpected results for uncommon or invalid SMILES strings; pre-filtering for valid molecules is recommended.
- Tokenization is vocabulary-dependent; if the training set contains rare or novel chemical substructures, the fixed vocabulary may not capture all valid tokens from test molecules.
- Exact-match accuracy is strict and does not account for multiple valid SMILES representations of the same molecule; Tanimoto similarity is a more lenient metric but depends on fingerprint choice.
- No changelog was found in the Spec2Mol repository, so historical changes to SMILES processing or tokenization schemes are not documented.

## Evidence

- [methods] Canonicalization via RDKit: "Prepare SMILES tokenizer and target SMILES string dataset, converting molecules to canonical SMILES format using RDKit."
- [methods] Tokenization for sequence models: "Define the decoder architecture in PyTorch as a sequence-to-sequence model with attention, mapping fixed-size embeddings to variable-length SMILES token sequences."
- [methods] Cross-entropy loss on tokens: "Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training."
- [methods] Reconstruction and evaluation: "Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules (decoded via RDKit)."
- [readme] RDKit chemical data processing: "Processing of the chemical data is based on the RDKit software."
