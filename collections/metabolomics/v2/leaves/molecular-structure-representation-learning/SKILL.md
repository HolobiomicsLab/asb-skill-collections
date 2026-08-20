---
name: molecular-structure-representation-learning
description: Use when when you have paired mass spectra and molecular structure data
  and need to train a model that can bidirectionally map between experimental spectra
  and chemical structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - PyTorch
  - Hugging Face Transformers
  - MS-BART (OpenDFM/MS-BART)
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.48550/arxiv.2510.20615
  title: MS-BART
evidence_spans:
- github.com/OpenDFM/MS-BART
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_bart_cq
    doi: 10.48550/arxiv.2510.20615
    title: MS-BART
  dedup_kept_from: coll_ms_bart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.48550/arxiv.2510.20615
  all_source_dois:
  - 10.48550/arxiv.2510.20615
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-representation-learning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Learning joint representations of mass spectra and molecular structures through unified tokenization and multi-stage pretraining, fine-tuning, and alignment. This skill enables end-to-end modeling where spectra and molecules share a common vocabulary and latent space, enabling structure elucidation from experimental mass spectra.

## When to use

When you have paired mass spectra and molecular structure data and need to train a model that can bidirectionally map between experimental spectra and chemical structures. Specifically, apply this skill when you aim to: (1) learn a joint representation space for spectra–molecule pairs with limited labeled experimental data, or (2) improve generalization of mass spectra-based structure elucidation by leveraging unlabeled pretraining data with computed fingerprints.

## When NOT to use

- Input spectra are already paired with high-confidence molecular structures from a comprehensive reference library (e.g., NIST library with >0.95 match score) — use lookup-based methods instead.
- You have only unpaired mass spectra with no known molecular structures and no access to computed fingerprints — the alignment and fine-tuning stages require supervision.
- The molecular structures are known to be in non-standard or heavily modified chemical spaces not well-represented in typical pretraining corpora — domain-specific pretraining data curation is required first.

## Inputs

- Mass spectra datasets (in MGF or equivalent format)
- Molecular structure data (SMILES strings or molecular graphs)
- Computed fingerprints (for pretraining data cleaning)
- Tanimoto similarity scores (for filtering pretraining pairs)

## Outputs

- Unified MS-BART vocabulary (spectra + molecule tokens)
- Pretrained model checkpoint (after Stage 1)
- Fine-tuned model checkpoint (after Stage 2)
- Aligned model checkpoint with joint spectra-molecule representation space (after Stage 3)
- Loss metrics and convergence logs for each stage

## How to apply

Execute a three-stage pipeline: (1) **Pretraining** — tokenize both mass spectra and molecular structures using a unified vocabulary, then train a sequence-to-sequence model on concatenated spectra-molecule token sequences using a pretraining objective on reliably computed fingerprints (filtered to Tanimoto similarity > 0.5 to remove unreliable pairings). (2) **Fine-tuning** — load the pretrained checkpoint and train on task-specific experimental mass spectra and known molecular structures with supervised loss to adapt to real spectra. (3) **Alignment** — load the fine-tuned checkpoint and apply contrastive learning with chemical feedback to align spectra and molecular representations in a shared latent space. Monitor loss convergence metrics at each stage and validate checkpoint files are saved at each transition point.

## Related tools

- **PyTorch** (Core deep learning framework for implementing the sequence-to-sequence architecture and training loops across pretraining, fine-tuning, and alignment stages)
- **Hugging Face Transformers** (Provides pre-built encoder–decoder architectures and tokenization utilities for implementing the unified vocabulary and end-to-end training)
- **MS-BART (OpenDFM/MS-BART)** (Reference implementation and trained checkpoints for mass spectra and molecular structure co-representation learning) — github.com/OpenDFM/MS-BART

## Examples

```
bash scripts/pretrain.sh && bash scripts/canopus/finetune.sh && bash scripts/canopus/align.sh
```

## Evaluation signals

- Loss metrics decrease monotonically and stabilize within each of the three stages; checkpoints saved at stage transitions contain valid model weights and vocabulary files.
- Pretraining loss converges on the clean filtered dataset (Tanimoto > 0.5); compare loss on filtered vs. unfiltered pretraining data to verify filtering rationale.
- Fine-tuning loss on experimental spectra improves relative to the pretrained baseline; verify fine-tuned model outperforms pretrained model on task-specific held-out test set.
- After alignment stage, mass spectra and molecular structures cluster together in the shared latent space (e.g., cosine similarity between aligned spectra and structure embeddings increases); verify alignment via embedding visualization or nearest-neighbor retrieval metrics.
- Checkpoint files exist and are loadable at each stage boundary; verify file integrity and model architecture consistency across stage transitions.

## Limitations

- Pretraining data quality is critical — filtering by Tanimoto similarity > 0.5 removes potentially valid but ambiguous pairings; lower thresholds increase noise but may improve data diversity.
- The unified vocabulary must accommodate both spectra tokenization (peaks, intensities) and molecular structure tokenization (atoms, bonds); vocabulary size and token design directly impact model capacity and convergence.
- Alignment via contrastive learning assumes that spectra and molecular structures are sufficiently correlated in the latent space; if spectra are highly noisy or molecules have multiple isomers, alignment may fail to converge or produce ambiguous representations.
- The method requires paired mass spectra and molecular structures for fine-tuning and alignment stages; unpaired data from either modality cannot be leveraged.

## Evidence

- [other] MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling.: "MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism"
- [other] Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences.: "Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences"
- [other] Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space.: "Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space"
- [intro] MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment.: "MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment"
- [readme] Pretrain dataset generation and split 10000 for validation to choose the best model for finetune and alignment: "Pretrain dataset generation and split 10000 for validation to choose the best model for finetune and alignment"
- [readme] The preprocessed and model weight from the [Figshare] and put them in data folder. The folder tree are: data/CANOPUS/pretrain-data # clean pretrain data (filter Tanimoto similarity > 0.5): "clean pretrain data (filter Tanimoto similarity > 0.5)"
- [readme] Step1: Unified Multi-Task Pretraining on Reliably Computed Fingerprints: "Unified Multi-Task Pretraining on Reliably Computed Fingerprints"
