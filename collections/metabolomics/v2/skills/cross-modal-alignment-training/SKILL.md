---
name: cross-modal-alignment-training
description: Use when after completing pretraining and fine-tuning stages when you have a checkpoint with task-specific performance but need to improve cross-modal consistency.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3316
  tools:
  - PyTorch
  - Hugging Face Transformers
  - MS-BART
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
---

# cross-modal-alignment-training

## Summary

Train a unified sequence-to-sequence model to align representations of two distinct modalities (mass spectra and molecular structures) in a shared latent space using contrastive feedback. This skill enables joint end-to-end modeling of both modalities for improved structure elucidation.

## When to use

Apply this skill after completing pretraining and fine-tuning stages when you have a checkpoint with task-specific performance but need to improve cross-modal consistency. Use it specifically when you have paired mass spectra–molecule examples and seek to align their learned representations so that spectra and structures map to the same latent region, enabling bidirectional inference.

## When NOT to use

- Input is a pretrained but not yet fine-tuned checkpoint; perform fine-tuning first to establish task-specific signal before alignment.
- Mass spectra and molecular structures are unpaired or misaligned; alignment requires reliable correspondence to avoid learning spurious correlations.
- Latent space dimensionality or architectural incompatibilities prevent meaningful cross-modal projection; verify embedding dimensions match between modalities.

## Inputs

- fine-tuned model checkpoint from stage 2
- paired mass spectra–molecule dataset (tokenized using unified MS-BART vocabulary)
- alignment loss configuration (contrastive margin, temperature, weighting)

## Outputs

- aligned model checkpoint with improved cross-modal latent space
- alignment loss curves and convergence metrics
- validated spectra-molecule representation pairs in shared latent space

## How to apply

Load the fine-tuned model checkpoint and train an alignment stage using contrastive loss on spectra-molecule pairs. The alignment objective enforces that encoded mass spectra and their corresponding molecular structures are pulled together in the latent space while unrelated pairs are pushed apart. This is typically done via chemical feedback mechanisms that refine alignment by comparing model predictions against known chemical rules or similarity metrics. Log alignment loss and verify convergence over epochs; save checkpoint files to track alignment progress separately from pretraining and fine-tuning artifacts.

## Related tools

- **PyTorch** (Deep learning framework for implementing contrastive alignment loss and gradient-based optimization of model parameters)
- **Hugging Face Transformers** (Provides sequence-to-sequence architecture (BART-based) and checkpoint loading/saving utilities for multi-stage training pipeline)
- **MS-BART** (Reference implementation of unified vocabulary tokenization and three-stage training including alignment stage scripts) — github.com/OpenDFM/MS-BART

## Examples

```
bash scripts/msg/align.sh
```

## Evaluation signals

- Alignment loss monotonically decreases over epochs and plateaus, indicating convergence of cross-modal representation learning.
- Checkpoint files are saved correctly at each alignment epoch and can be reloaded without errors.
- Aligned model produces spectra and molecule embeddings that cluster by chemical similarity in latent space (verified by computing cosine similarity between paired embeddings).
- Downstream task performance (e.g., structure elucidation accuracy) improves or stabilizes after alignment compared to fine-tuned baseline.
- Validation loss on held-out spectra-molecule pairs shows generalization rather than overfitting to training alignment pairs.

## Limitations

- Alignment stage assumes fine-tuned checkpoint already captures task-relevant structure; poor fine-tuning will not be remedied by alignment alone.
- Contrastive alignment requires sufficient paired spectra-molecule examples; sparse or noisy pairings may lead to misaligned representations.
- The unified vocabulary and tokenization scheme must be consistent across all three stages (pretraining, fine-tuning, alignment); vocabulary mismatches will corrupt learned representations.
- No explicit evaluation metric for cross-modal alignment quality is reported; alignment success is inferred indirectly from downstream task performance.

## Evidence

- [other] MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling.: "MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment"
- [other] Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space.: "Load the fine-tuned checkpoint and execute alignment stage to align spectra and molecular representations in a shared latent space"
- [intro] MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment.: "MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment"
- [readme] ## Step3: Contrastive Alignment via Chemical Feedback: "## Step3: Contrastive Alignment via Chemical Feedback"
- [other] Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly.: "Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly"
