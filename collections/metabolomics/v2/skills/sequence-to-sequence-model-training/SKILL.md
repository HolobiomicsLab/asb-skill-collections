---
name: sequence-to-sequence-model-training
description: Use when you have paired multimodal scientific data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Hugging Face Transformers
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

# sequence-to-sequence-model-training

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Training a sequence-to-sequence model through a three-stage pipeline (pretraining, fine-tuning, alignment) on unified tokenized inputs to enable joint modeling of multiple modalities (e.g., mass spectra and molecular structures). This skill applies when you need to leverage language model architectures for multimodal scientific prediction tasks requiring end-to-end learning across precomputed and experimental data.

## When to use

You have paired multimodal scientific data (e.g., mass spectra and molecular structures) that require unified representation learning, and you want to progressively refine model behavior through supervised pretraining on large synthetic/computed datasets, task-specific fine-tuning on experimental examples, and contrastive alignment to harmonize cross-modal latent spaces.

## When NOT to use

- Input modalities cannot be unified under a single vocabulary (e.g., fundamentally incompatible tokenization schemes)
- You only have unimodal data (single modality) and do not need cross-modal alignment
- You have a small labeled dataset and no large pretrain corpus, making the three-stage pipeline unnecessarily expensive

## Inputs

- Raw mass spectra and molecular structure datasets (paired examples)
- Unified tokenizer/vocabulary covering both spectra and molecule modalities
- Pretrain data (clean, Tanimoto similarity-filtered ≥ 0.5, ~4M examples)
- Task-specific labeled examples for fine-tuning
- Pretraining stage checkpoint (for fine-tuning initialization)
- Fine-tuned stage checkpoint (for alignment initialization)

## Outputs

- Pretrained model checkpoint saved after Stage 1
- Fine-tuned model checkpoint saved after Stage 2 (best validation loss)
- Aligned model checkpoint saved after Stage 3
- Loss curves and convergence metrics logged at each stage
- Joint spectra-molecule latent representations in shared embedding space

## How to apply

First, design a unified vocabulary that tokenizes both modalities (e.g., mass spectrum peaks and molecular SMILES), then concatenate spectra-molecule token sequences. Execute Stage 1 (Pretraining): load pretrain data, run end-to-end sequence-to-sequence pretraining on the full 4M clean concatenated dataset using pretraining loss objectives, logging convergence metrics and saving checkpoints. Stage 2 (Fine-tuning): load the pretrained checkpoint, execute supervised fine-tuning on task-specific labeled examples (e.g., experimental mass spectra paired with ground-truth structures) with task loss, selecting the best checkpoint by validation loss. Stage 3 (Alignment): load the fine-tuned checkpoint and apply contrastive alignment to align spectra and molecular representations in a shared latent space using chemical feedback. Validate by confirming loss metrics decrease monotonically at each stage and checkpoint files persist correctly.

## Related tools

- **PyTorch** (Core deep learning framework for implementing the sequence-to-sequence encoder-decoder architecture and loss computation across all three training stages)
- **Hugging Face Transformers** (Provides pretrained transformer backbone components (e.g., BART encoder-decoder) for the sequence-to-sequence model and utilities for checkpoint management)

## Examples

```
bash scripts/pretrain.sh && bash scripts/msg/finetune.sh && bash scripts/msg/align.sh
```

## Evaluation signals

- Loss metrics (pretraining, fine-tuning, alignment losses) decrease monotonically or stabilize within each stage, indicating convergence
- Checkpoint files (.pt or .bin) are saved at each stage milestone without corruption; model can be reloaded and produces consistent outputs
- Validation loss on held-out task examples is lower after fine-tuning than before, confirming task adaptation
- Alignment stage contrastive loss decreases, indicating improved spectra-molecule latent space coherence measurable by cross-modal retrieval metrics
- End-to-end structure elucidation accuracy on test set improves after each stage compared to baseline or single-stage models

## Limitations

- Requires large pretrain corpus (~4M examples) to achieve strong convergence; performance degrades significantly with smaller pretraining datasets
- Unified vocabulary design is dataset- and modality-specific; transferability to other modality pairs (e.g., different spectroscopy types) requires re-tokenization and potential retraining
- Contrastive alignment stage assumes availability of high-quality chemical feedback or contrastive pairs; noisy or misaligned feedback can degrade joint representations
- Three-stage pipeline is computationally expensive (full pretraining + fine-tuning + alignment); not practical for rapid prototyping or resource-constrained settings

## Evidence

- [other] MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling.: "MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling."
- [other] 1. Load mass spectra and molecular structure datasets, tokenizing both modalities using the unified MS-BART vocabulary. 2. Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences. 3. Load the pretrained checkpoint and execute fine-tuning stage on task-specific mass spectra structure elucidation examples with supervised loss. 4. Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space.: "Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences."
- [other] Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly.: "Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly."
- [readme] # Pretrain dataset generation and split 10000 for validation to choose the best model for finetune and alignment: "split 10000 for validation to choose the best model for finetune and alignment"
- [readme] ## Step1: Unified Multi-Task Pretraining on Reliably Computed Fingerprints: "Unified Multi-Task Pretraining on Reliably Computed Fingerprints"
- [readme] ## Step2: Finetuning on Experimental Spectra: "Step2: Finetuning on Experimental Spectra"
- [readme] ## Step3: Contrastive Alignment via Chemical Feedback: "Step3: Contrastive Alignment via Chemical Feedback"
- [readme] pretrain-data # clean pretrain data (filter Tanimoto similarity > 0.5): "clean pretrain data (filter Tanimoto similarity > 0.5)"
