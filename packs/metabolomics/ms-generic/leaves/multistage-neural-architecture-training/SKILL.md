---
name: multistage-neural-architecture-training
description: 'Use when you have paired mass spectra and molecular structure datasets
  and need to train a model that jointly understands both modalities for tasks like
  structure elucidation. Specifically, use it when: (1) you have large unlabeled or
  weakly-labeled pretraining data with both spectra and molecules;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0417
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3315
  tools:
  - PyTorch
  - Hugging Face Transformers
  - MS-BART
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
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

# multistage-neural-architecture-training

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A three-stage training pipeline (pretraining, fine-tuning, alignment) that progressively specializes a unified sequence-to-sequence model for joint mass spectra and molecular structure modeling. This skill enables models to learn general spectral-molecular patterns before task-specific adaptation and cross-modal representation alignment.

## When to use

Apply this skill when you have paired mass spectra and molecular structure datasets and need to train a model that jointly understands both modalities for tasks like structure elucidation. Specifically, use it when: (1) you have large unlabeled or weakly-labeled pretraining data with both spectra and molecules; (2) smaller task-specific annotated datasets are available for fine-tuning; (3) you want to align spectra and molecular representations in a shared latent space via contrastive objectives; and (4) a single unified vocabulary can tokenize both modalities.

## When NOT to use

- Input spectra and molecules are not naturally paired or aligned — the pipeline assumes strong correspondence between spectra and structure labels.
- Only single-modality data is available (spectra only, or molecules only, without pairings) — the unified vocabulary and cross-modal alignment stages require both modalities.
- Pretraining data quality is poor or has high Tanimoto similarity (>0.5) between examples — MS-BART filters such data; use the provided filtering step before commencing Stage 1.
- Real-time or low-latency inference is required — the three-stage sequential training and checkpoint loading workflow is computationally intensive and offline.

## Inputs

- Raw mass spectra datasets (MGF or CANOPUS format)
- Molecular structure data (SMILES strings or canonical representations)
- Fingerprint annotations (computed or ground-truth)
- Pretraining dataset with paired spectra-molecule examples
- Task-specific annotated fine-tuning examples with experimental spectra
- Unified vocabulary tokenizer for both modalities

## Outputs

- Pretrained checkpoint (Stage 1 model weights)
- Fine-tuned checkpoint (Stage 2 model weights)
- Alignment-trained checkpoint (Stage 3 model weights)
- Training loss logs for convergence validation
- Aligned spectra and molecular representations in shared latent space
- Structure elucidation predictions on held-out test spectra

## How to apply

Begin by tokenizing both mass spectra and molecular structures using a unified vocabulary that represents both modalities. Execute Stage 1 (Unified Multi-Task Pretraining) on reliably computed fingerprints and spectra pairs using a sequence-to-sequence architecture with concatenated spectra-molecule token sequences and a pretraining objective (e.g., denoising or masked span prediction). Load the pretrained checkpoint and execute Stage 2 (Fine-tuning on Experimental Spectra) on task-specific mass spectra structure elucidation examples with supervised loss to adapt the model to experimental conditions. Finally, load the fine-tuned checkpoint and execute Stage 3 (Contrastive Alignment via Chemical Feedback) to align spectra and molecular representations in a shared latent space using contrastive losses. At each stage, log loss metrics and validate model checkpoint files are saved correctly; convergence indicates successful progression.

## Related tools

- **PyTorch** (Deep learning framework for implementing sequence-to-sequence architecture and loss functions across all three training stages)
- **Hugging Face Transformers** (Provides pretrained seq2seq model backbones and utilities for model checkpointing and tokenization management)
- **MS-BART** (Reference implementation of the three-stage unified pretraining, fine-tuning, and alignment pipeline with dataset preprocessing and evaluation scripts) — https://github.com/OpenDFM/MS-BART

## Examples

```
bash scripts/pretrain.sh && bash scripts/msg/finetune.sh && bash scripts/msg/align.sh
```

## Evaluation signals

- Training loss curves at each stage (pretraining, fine-tuning, alignment) show monotonic or convergent decrease; no divergence or NaN values indicate successful backpropagation and gradient flow.
- Model checkpoints are successfully saved after each stage and can be loaded without errors; file sizes and tensor dimensions match expected architecture specifications.
- Fine-tuning stage shows lower loss on task-specific training data than untrained baseline; fine-tuned model outperforms pretrained-only model on held-out validation spectra.
- After alignment stage, spectra and molecular embeddings occupy overlapping regions in the shared latent space; contrastive loss (e.g., InfoNCE or triplet loss) is lower for matched pairs than for negative examples.
- Downstream structure elucidation metrics (exact match, top-k accuracy, or ranking-based metrics) improve from Stage 1 → Stage 2 → Stage 3, confirming cumulative benefit of each training phase.

## Limitations

- Pretraining data quality critically depends on fingerprint reliability; models trained on biased or noisy fingerprints propagate those errors through fine-tuning and alignment. The paper filters pairs with Tanimoto similarity > 0.5 but does not address other sources of label noise.
- The unified vocabulary must effectively tokenize both mass spectra (continuous m/z and intensity values) and molecular structures (discrete SMILES); design choices (binning strategies, special tokens) are not fully detailed and may be dataset-specific.
- Alignment stage assumes that spectra and molecular representations can be meaningfully aligned in a shared latent space; this assumption may fail for novel compound classes or spectra from underrepresented instrument types not seen during training.
- Computational cost is high: three sequential stages, each with its own convergence criteria and checkpoint overhead, increase wall-clock training time; the paper does not report exact runtimes or memory requirements.
- No changelog or ablation studies in the source repository make it difficult to assess which design choices (e.g., loss function weights, alignment temperature, vocabulary size) are critical versus incidental.

## Evidence

- [other] MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling.: "MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling."
- [other] Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences.: "Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences."
- [other] Load the pretrained checkpoint and execute fine-tuning stage on task-specific mass spectra structure elucidation examples with supervised loss.: "Load the pretrained checkpoint and execute fine-tuning stage on task-specific mass spectra structure elucidation examples with supervised loss."
- [other] Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space.: "Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space."
- [readme] Step1: Unified Multi-Task Pretraining on Reliably Computed Fingerprints: "Step1: Unified Multi-Task Pretraining on Reliably Computed Fingerprints"
- [readme] Step2: Finetuning on Experimental Spectra: "Step2: Finetuning on Experimental Spectra"
- [readme] Step3: Contrastive Alignment via Chemical Feedback: "Step3: Contrastive Alignment via Chemical Feedback"
- [readme] The folder tree are: data/CANOPUS/pretrain-data (clean pretrain data filter Tanimoto similarity > 0.5), pretrained-model, train, test, val: "data/CANOPUS/pretrain-data # clean pretrain data (filter Tanimoto similarity > 0.5)"
