---
name: weighted-loss-function-optimization
description: Use when when training a dual-encoder architecture (bi-encoder + cross-encoder) on NMR spectral data where independent encoding and joint pair processing produce competing or imbalanced gradient signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0081
  tools:
  - Python
  - Anaconda
  - PyTorch
  - FlavorFormer
derived_from:
- doi: 10.1016/j.microc.2025.115372
  title: FlavorFormer
evidence_spans:
- Python 3.13.2 and Pytorch (version 2.7.0+cu118)
- Install [Anaconda](https://www.anaconda.com/).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flavorformer_cq
    doi: 10.1016/j.microc.2025.115372
    title: FlavorFormer
  dedup_kept_from: coll_flavorformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2025.115372
  all_source_dois:
  - 10.1016/j.microc.2025.115372
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# weighted-loss-function-optimization

## Summary

Optimize a weighted loss function that balances contributions from bi-encoder and cross-encoder branches during end-to-end training of a hybrid CNN-Transformer model for NMR spectral compound identification. This skill ensures both encoder paths contribute meaningfully to the final relevance scores and compound predictions.

## When to use

When training a dual-encoder architecture (bi-encoder + cross-encoder) on NMR spectral data where independent encoding and joint pair processing produce competing or imbalanced gradient signals. Use this skill when naïve unweighted combination of encoder logits leads to one branch dominating learning or when you need to control the relative importance of local spectral similarity versus joint spectrum-compound refinement.

## When NOT to use

- Input uses only a single encoder (bi-encoder or cross-encoder alone); weighted loss is unnecessary—use standard cross-entropy or contrastive loss instead.
- Spectrum-compound pairs are not available or cannot be reliably annotated; cross-encoder branch cannot be trained.
- NMR spectra are already pre-classified or dimensionally reduced to a known compound index; use simpler supervised classification rather than dual-encoder retrieval.

## Inputs

- Preprocessed 1H NMR spectral data (numeric arrays or tensors)
- Compound reference labels and embeddings
- Spectrum-compound pair annotations for cross-encoder training
- Bi-encoder and cross-encoder logit outputs from forward pass
- Validation set with ground-truth compound identities

## Outputs

- Weighted loss scalar (differentiable)
- Trained hybrid CNN-Transformer backbone with optimized fusion pooling
- Trained bi-encoder and cross-encoder heads
- Model checkpoint with best validation compound identification accuracy
- Performance report (accuracy, ranking metrics)

## How to apply

Construct a weighted loss function that sums the bi-encoder and cross-encoder logit contributions with learnable or fixed weights α and (1−α), ensuring both branches receive meaningful gradients during backpropagation. Initialize weights based on validation performance of each encoder in isolation, or use a schedule that gradually shifts weight emphasis as training progresses. During end-to-end training, backpropagate through the combined loss to update the hybrid CNN-Transformer backbone, fusion pooling parameters, and encoder-specific heads. Monitor compound identification accuracy and ranking metrics (e.g., top-k retrieval recall, mean reciprocal rank) on a held-out validation set to verify that neither encoder branch is being suppressed and that the fusion strategy improves over either encoder alone.

## Related tools

- **PyTorch** (Deep learning framework for defining weighted loss functions, implementing bi-encoder and cross-encoder branches, and end-to-end backpropagation) — https://pytorch.org
- **FlavorFormer** (Complete hybrid CNN-Transformer model implementing weighted loss for NMR compound identification; repository includes trained checkpoints and demo code) — https://github.com/yfWang01/FlavorFormer
- **Anaconda** (Environment manager for Python 3.13.2, PyTorch 2.7.0+cu118, and project dependencies) — https://www.anaconda.com/

## Evaluation signals

- Weighted loss decreases monotonically (or in expected cycles) across training epochs; sudden spikes suggest weight imbalance or divergence.
- Compound identification accuracy on the validation set improves or stabilizes above the accuracy achievable by either encoder branch alone.
- Gradient magnitudes flowing to bi-encoder and cross-encoder branches are comparable in magnitude; gross imbalance (e.g., one > 10× the other) indicates poor weight choice.
- Top-k retrieval recall (especially top-1 and top-5) and mean reciprocal rank on held-out test set match or exceed published FlavorFormer benchmarks for the same NMR dataset.
- Loss ratio (bi-encoder loss / cross-encoder loss) remains within a target range (e.g., 0.5–2.0) throughout training, confirming neither branch is starved.

## Limitations

- The optimal weight balance α between bi-encoder and cross-encoder is dataset and architecture-dependent; transfer from one NMR mixture type or spectrometer to another may require re-tuning.
- Weighted loss assumes both encoders produce comparable loss scales; if raw losses differ by orders of magnitude, normalization or scaling of individual losses may be necessary before weighting.
- No explicit mechanism in the weighted loss formula prevents mode collapse where one encoder ignores the other's signals; regularization on encoder orthogonality or auxiliary diversity losses may be needed for highly imbalanced mixtures.

## Evidence

- [readme] leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly: "leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly"
- [other] Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation.: "Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation."
- [other] Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report.: "Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report."
