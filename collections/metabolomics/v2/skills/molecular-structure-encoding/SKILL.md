---
name: molecular-structure-encoding
description: Use when you have molecular structures (SMILES strings or molecular graphs)
  that need to be input to a transformer model for property prediction (e.g., Collision
  Cross Section), and the model requires tokenized or embedded representations rather
  than raw chemical notation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - Transformers (Hugging Face)
  - PyTorch / PyTorch Lightning
  - MoLFormer (Pre-trained)
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c03492
  title: HyperCCS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hyperccs_cq
    doi: 10.1021/acs.analchem.5c03492
    title: HyperCCS
  dedup_kept_from: coll_hyperccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03492
  all_source_dois:
  - 10.1021/acs.analchem.5c03492
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-encoding

## Summary

Encode molecular structures into fixed-dimensional vector representations suitable for transformer-based deep learning models. This skill bridges chemical notation (SMILES, molecular graphs) and numerical feature spaces required for CCS prediction and other molecular property modeling tasks.

## When to use

Use this skill when you have molecular structures (SMILES strings or molecular graphs) that need to be input to a transformer model for property prediction (e.g., Collision Cross Section), and the model requires tokenized or embedded representations rather than raw chemical notation.

## When NOT to use

- Molecular structures are already encoded as pre-computed embeddings or feature tables; re-encoding would be redundant.
- The downstream task does not require transformer-based processing (e.g., simple rule-based property lookup or QSAR with fixed descriptors).
- SMILES strings are malformed, incomplete, or represent invalid chemical structures that cannot be tokenized or fingerprinted.

## Inputs

- SMILES strings (molecular representation)
- Molecular graphs or molecular structure objects
- Adduct type labels ([M+H]+, [M+Na]+, [M-H]-)
- ECFP fingerprint vectors (optional, 1024-dimensional)

## Outputs

- Tokenized SMILES sequences
- Contextual molecular embeddings (transformer hidden states)
- Fused feature vectors (early or late fusion format)
- Input tensors ready for CCS prediction head

## How to apply

Tokenize SMILES strings using a molecular vocabulary (e.g., bert_vocab.txt) to convert each molecule into a sequence of discrete tokens. Optionally compute auxiliary molecular features such as ECFP fingerprints (Extended-Connectivity Fingerprint, typically 1024-dimensional) and adduct type embeddings ([M+H]+, [M+Na]+, [M-H]-). Choose an early or late fusion strategy to combine SMILES tokens with auxiliary features: early fusion concatenates features before transformer encoding; late fusion processes them separately and merges transformer outputs. Pass the combined representation through the transformer encoder to produce contextualized molecular embeddings, which are then fed to the CCS prediction head. Validate that output embeddings have the expected dimensionality (e.g., 768 for n_embd=768) and that all molecules in the batch produce consistent tensor shapes.

## Related tools

- **RDKit** (Parse and validate SMILES strings; generate ECFP fingerprints and molecular property descriptors) — https://www.rdkit.org/
- **Transformers (Hugging Face)** (Tokenize molecular sequences and provide transformer encoder blocks for contextual embedding) — https://github.com/huggingface/transformers
- **PyTorch / PyTorch Lightning** (Implement and train transformer encoder and fusion layers; manage batch tensor operations) — https://github.com/PyTorchLightning/pytorch-lightning
- **MoLFormer (Pre-trained)** (Provide pre-trained molecular transformer checkpoints and vocabulary for SMILES tokenization) — https://github.com/NeoNexusX/HyperCCS

## Examples

```
python data_prepare_example.py --input molecules.csv --smiles_col smiles --adduct_col adduct --output encoded_features.h5 --ecfp_num 1024
```

## Evaluation signals

- Tokenized SMILES sequences contain only valid tokens from bert_vocab.txt and have length consistent with molecular complexity.
- ECFP fingerprints are non-zero sparse vectors with exactly 1024 dimensions and Hamming weight > 0.
- Transformer output embeddings have shape [batch_size, sequence_length, n_embd] (e.g., [64, 128, 768]) with no NaN or Inf values.
- Early/late fusion output maintains consistent dimensionality across the batch; gradients flow correctly during backpropagation (checked via .grad attributes).
- Round-trip validation: encode a known reference molecule (e.g., glucose) and confirm reproducibility of embeddings across multiple runs with fixed random seed.

## Limitations

- Encoding quality depends on vocabulary coverage; out-of-vocabulary tokens may degrade performance on unseen chemical scaffolds.
- ECFP fingerprints are fixed-size (1024-dim) and may not capture rare or highly specific substructures.
- Early vs. late fusion strategy requires tuning; the article specifies fusion type ('early' or 'later') but does not provide guidance on which is optimal for different molecular domains.
- SMILES canonicalization is not explicitly handled; non-canonical SMILES for the same molecule may produce different tokenizations and embeddings.
- Adduct type must be provided as external metadata; the encoding skill does not infer adduct type from structure alone.

## Evidence

- [readme] SMILES tokenization for molecular representation: "The model uses a transformer-based architecture with: - SMILES tokenization for molecular representation"
- [readme] Auxiliary features and fusion strategy: "- Early and late fusion options for feature integration"
- [readme] ECFP fingerprint integration parameter: "- `--ecfp_num`: ECFP fingerprint size (default: 1024)"
- [readme] Transformer encoder dimensionality: "- `--n_embd`: Embedding dimension (default: 768)"
- [readme] Adduct type support in encoding: "Support for different adduct types ([M+H]+, [M+Na]+, [M-H]-)"
- [intro] Core workflow: Define transformer encoder for molecular structure information: "Define the transformer encoder component to process molecular structure information (SMILES strings, molecular graphs, or feature vectors as per repository specification)."
