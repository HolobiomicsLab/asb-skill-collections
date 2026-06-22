---
name: molecular-structure-reconstruction-from-embeddings
description: Use when you have a pretrained encoder that produces fixed-size embeddings from MS/MS spectra (or other molecular data modalities) and you need to recover the corresponding molecular structure as a SMILES string.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3511
  tools:
  - RDKit
  - PyTorch
  techniques:
  - tandem-MS
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

# molecular-structure-reconstruction-from-embeddings

## Summary

Decode fixed-size molecular embeddings into canonical SMILES strings using a sequence-to-sequence decoder with attention. This skill is essential when you have pretrained encoder embeddings (e.g., from MS/MS spectra) and need to recover the molecular structure in human-readable format for validation, retrieval, or downstream chemical analysis.

## When to use

Apply this skill when you have a pretrained encoder that produces fixed-size embeddings from MS/MS spectra (or other molecular data modalities) and you need to recover the corresponding molecular structure as a SMILES string. Typical triggers: (1) you have encoder checkpoint weights and embedding outputs but no decoder yet; (2) you need to benchmark decoder reconstruction accuracy on held-out test embeddings; (3) you want to integrate structure prediction into an end-to-end inference pipeline from raw spectra to molecules.

## When NOT to use

- Input embeddings are variable-length or already tokenized sequences — use a standard seq2seq model without the fixed-to-variable mapping assumption.
- You do not have a pretrained encoder or encoder embeddings — train or obtain embeddings first before attempting decoder training.
- Target molecules are represented in formats other than SMILES (e.g., InChI, SMARTS, 3D coordinates) — adapt tokenization and evaluation accordingly or preprocess to canonical SMILES.

## Inputs

- pretrained encoder model (PyTorch checkpoint)
- encoder output embeddings (fixed-size numerical vectors)
- SMILES string dataset (canonical format via RDKit)
- SMILES tokenizer vocabulary

## Outputs

- trained decoder model weights (PyTorch checkpoint)
- reconstructed SMILES strings (for test embeddings)
- exact-match accuracy metrics
- Tanimoto similarity scores (molecular fingerprint comparison)
- validation metric logs

## How to apply

Load the pretrained encoder model and collect its output embeddings (from checkpoint or upstream inference). Define a sequence-to-sequence decoder architecture in PyTorch with attention mechanism, mapping the fixed-size embedding to variable-length SMILES token sequences. Tokenize target SMILES strings using a SMILES tokenizer (RDKit canonical format) and prepare a training dataset of embedding–SMILES pairs. Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, applying teacher forcing during training to stabilize convergence. Evaluate on held-out test embeddings by measuring exact-match accuracy (fraction of perfectly reconstructed SMILES) and Tanimoto similarity (comparing molecular fingerprints of reconstructed vs. reference molecules using RDKit). Save trained decoder weights and log validation metrics to file for reproducibility and ablation studies.

## Related tools

- **PyTorch** (implements the sequence-to-sequence encoder–decoder architecture with attention for SMILES token prediction)
- **RDKit** (tokenizes SMILES strings into canonical format, generates molecular fingerprints for Tanimoto similarity computation, and validates reconstructed structures) — https://www.rdkit.org/

## Examples

```
# Train decoder on pretrained encoder embeddings
python -c "import torch; from model import Decoder; decoder = Decoder(embed_dim=512, vocab_size=100, hidden_dim=256); opt = torch.optim.Adam(decoder.parameters(), lr=1e-3); loss_fn = torch.nn.CrossEntropyLoss(); # load embeddings and SMILES tokens, apply teacher forcing and compute cross-entropy loss"
```

## Evaluation signals

- Exact-match accuracy on test set: fraction of decoder outputs that match reference SMILES strings exactly (character-for-character match after canonicalization).
- Tanimoto similarity of reconstructed vs. reference molecules: computed from RDKit fingerprints; should be ≥ 0.9 for valid reconstructions.
- Cross-entropy loss on held-out test embeddings converges and plateaus; validation loss does not diverge.
- Reconstructed SMILES pass RDKit validity checks (parse without error and encode valid molecular structures).
- Consistency check: re-encoding the same embedding multiple times (after deployment) yields identical SMILES output (deterministic decoder).

## Limitations

- Decoder performance depends critically on quality and diversity of the pretrained encoder embeddings; poor encoder representations will propagate to reconstruction errors.
- Teacher forcing during training can cause exposure bias at inference time; consider scheduled sampling or inference-time beam search to mitigate.
- Exact-match accuracy is strict and may penalize valid alternative SMILES representations of the same molecule; Tanimoto similarity provides a more forgiving chemical equivalence metric.
- The method is restricted to SMILES as the output representation; other molecular formats (3D coordinates, graph structures) require alternative decoder designs.
- Computational cost scales with sequence length; longer or more complex molecules may incur higher latency and memory overhead during decoding.

## Evidence

- [intro] encoder_embedding_to_smiles_decoding: "The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates."
- [other] seq2seq_attention_architecture: "Define the decoder architecture in PyTorch as a sequence-to-sequence model with attention, mapping fixed-size embeddings to variable-length SMILES token sequences."
- [other] teacher_forcing_training: "Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training."
- [other] tanimoto_and_exact_match_evaluation: "Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules (decoded via RDKit)."
- [readme] pytorch_rdkit_tools: "The implementation of the Spec2Mol architecture is based on the Pytorch library. Processing of the chemical data is based on the RDKit software."
- [other] canonical_smiles_format: "Prepare SMILES tokenizer and target SMILES string dataset, converting molecules to canonical SMILES format using RDKit."
