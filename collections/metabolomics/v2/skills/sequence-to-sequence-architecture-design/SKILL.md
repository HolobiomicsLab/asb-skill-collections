---
name: sequence-to-sequence-architecture-design
description: Use when when you have encoder-produced fixed-size embeddings and need to generate variable-length discrete sequences (e.g., SMILES tokens, protein sequences, chemical formulas) as outputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0602
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sequence-to-sequence-architecture-design

## Summary

Design and implement a sequence-to-sequence (seq2seq) model with attention that maps fixed-size embeddings to variable-length token sequences, such as reconstructing SMILES strings from molecular embeddings. This skill bridges continuous latent representations to discrete symbolic outputs using an encoder-decoder paradigm with teacher forcing during training.

## When to use

When you have encoder-produced fixed-size embeddings and need to generate variable-length discrete sequences (e.g., SMILES tokens, protein sequences, chemical formulas) as outputs. Specifically applicable when the input is a continuous embedding and the output is a sequence of categorical tokens with no predetermined length.

## When NOT to use

- Input is already a sequence (use sequence-to-sequence without an embedding bottleneck instead).
- Output is fixed-length or continuous-valued (use a fully connected regression head or classifier instead).
- Target sequences are very short (single tokens) or deterministic transformations (use a simple lookup table or rule-based decoder).

## Inputs

- encoder-produced embeddings (fixed-size continuous vectors)
- SMILES token vocabulary or domain-specific tokenizer
- target sequence dataset (e.g., canonical SMILES strings, protein sequences)

## Outputs

- trained decoder model weights
- decoded variable-length sequences (e.g., SMILES strings)
- validation metrics (exact-match accuracy, Tanimoto similarity, cross-entropy loss)

## How to apply

Define a sequence-to-sequence model in PyTorch with an embedding layer that accepts the fixed-size encoder output, followed by an attention-equipped recurrent decoder (e.g., LSTM or GRU) that predicts one token at a time. Prepare a tokenizer for your target domain (e.g., SMILES tokenizer via RDKit) and convert all target sequences to canonical representations. Train the decoder end-to-end using cross-entropy loss on token prediction with teacher forcing (feeding ground-truth tokens during training rather than model predictions). Evaluate using exact-match accuracy on held-out embeddings and domain-specific similarity metrics (e.g., Tanimoto similarity between decoded and reference molecules via RDKit). Log validation metrics and save trained decoder weights separately from the encoder for modularity.

## Related tools

- **PyTorch** (framework for implementing sequence-to-sequence model architecture with attention, cross-entropy loss computation, and backpropagation training)
- **RDKit** (tokenization of SMILES strings, canonicalization of molecular structures, and computation of Tanimoto similarity for evaluation) — https://www.rdkit.org/

## Examples

```
decoder = Seq2SeqDecoder(embedding_dim=256, vocab_size=120, hidden_dim=512, num_layers=2, attention=True); criterion = nn.CrossEntropyLoss(); optimizer = torch.optim.Adam(decoder.parameters(), lr=0.001); for epoch in range(num_epochs): loss = train_epoch(decoder, train_loader, criterion, optimizer, teacher_forcing_ratio=1.0); val_acc, val_tanimoto = evaluate(decoder, val_loader); print(f'Epoch {epoch}: train_loss={loss:.4f}, val_acc={val_acc:.4f}, val_tanimoto={val_tanimoto:.4f}')
```

## Evaluation signals

- Exact-match accuracy on held-out test embeddings (reconstructed SMILES == reference SMILES without RDKit canonicalization errors).
- Tanimoto similarity between decoded and reference molecules (via RDKit fingerprints; expect high similarity if decoding is faithful).
- Cross-entropy loss converging and validation loss decreasing over training epochs.
- All generated sequences are valid tokens according to the target tokenizer vocabulary.
- Decoder output sequences vary in length as expected (not all identical lengths) and respect chemical feasibility constraints when decoded to molecules.

## Limitations

- Teacher forcing during training can cause exposure bias: at inference, the decoder conditions on its own (potentially erroneous) predictions rather than ground truth, degrading sequence quality over long horizons.
- Attention mechanism assumes the embedding is sufficiently informative; if the encoder embedding loses critical structural information, the decoder cannot recover it.
- Exact-match accuracy is brittle for SMILES (same molecule can have multiple valid SMILES representations); Tanimoto similarity or other fuzzy metrics are more robust but slower to compute.
- Training requires paired encoder embeddings and target sequences; unpaired or weakly labeled data cannot be used directly.

## Evidence

- [other] Define the decoder architecture in PyTorch as a sequence-to-sequence model with attention, mapping fixed-size embeddings to variable-length SMILES token sequences.: "Define the decoder architecture in PyTorch as a sequence-to-sequence model with attention, mapping fixed-size embeddings to variable-length SMILES token sequences."
- [other] Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training.: "Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training."
- [other] Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules (decoded via RDKit).: "Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules (decoded via RDKit)."
- [readme] The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates.: "The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates."
- [readme] The implementation of the Spec2Mol architecture is based on the Pytorch library. Processing of the chemical data is based on the RDKit software.: "The implementation of the Spec2Mol architecture is based on the Pytorch library. Processing of the chemical data is based on the RDKit software."
