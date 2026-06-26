---
name: contrastive-loss-implementation
description: 'Use when training embeddings from MS/MS spectra and you need to simultaneously
  enforce: (1) discrimination between spectra with different structural properties
  via contrastive learning on peak information and metadata embeddings, and (2) accurate
  reconstruction of embeddings from peak features via.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - PyTorch
  - Transformer architecture
  - matchms
  - CLERMS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c00260
  title: CLERMS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_clerms_cq
    doi: 10.1021/acs.analchem.3c00260
    title: CLERMS
  dedup_kept_from: coll_clerms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00260
  all_source_dois:
  - 10.1021/acs.analchem.3c00260
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# contrastive-loss-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Implement a composite loss function that combines InfoNCE contrastive loss and MSE reconstruction loss for training transformer-based embeddings from MS/MS spectra peak information and metadata. This skill is essential when learning discriminative representations from multi-modal spectral data where both contrastive discrimination and reconstruction fidelity are required.

## When to use

Apply this skill when training embeddings from MS/MS spectra and you need to simultaneously enforce: (1) discrimination between spectra with different structural properties via contrastive learning on peak information and metadata embeddings, and (2) accurate reconstruction of embeddings from peak features via MSE loss. Triggered by the need to obtain good embeddings from peak information and metadata without ground-truth labels.

## When NOT to use

- When input spectra are unlabeled and no structural similarity ground truth (Tanimoto scores) is available for contrastive pairs.
- When embeddings are already pre-computed by another method; this skill is for training, not inference.
- When the input is a feature table or pre-extracted embedding matrix without access to raw peak intensities and metadata.

## Inputs

- Peak information tensors (m/z and intensity normalized according to dataset_preprocessing.ipynb)
- Metadata embeddings (e.g., molecular descriptors or structural features)
- Batch of paired spectra with known structural similarity scores (from Tanimoto calculation)
- Temperature hyperparameter for InfoNCE scaling
- Loss weight parameters (alpha for InfoNCE, beta for MSE)

## Outputs

- Composite loss scalar (InfoNCE + MSE weighted sum)
- Per-sample contrastive loss values
- Per-sample reconstruction loss values
- Gradient tensors for parameter updates

## How to apply

Define the InfoNCE contrastive loss function operating on paired peak-information and metadata embeddings with temperature scaling to control the sharpness of the similarity distribution. In parallel, define an MSE reconstruction loss function that measures the difference between original and reconstructed embeddings. Implement the composite loss as a weighted sum of the InfoNCE and MSE terms, wrapping both in a PyTorch module with configurable weight parameters to balance the two objectives. Validate gradient flow through the composite loss by backpropagating on synthetic embedding tensors and checking that both components contribute to parameter updates. Use this within a transformer-based architecture equipped with sinusoidal embeddings to encode peak information.

## Related tools

- **PyTorch** (Framework for implementing the composite loss function as a differentiable module and managing gradient computation.)
- **Transformer architecture** (Backbone architecture housing the sinusoidal embedder and embedding extraction layers that receive peak and metadata inputs.)
- **matchms** (Spectral processing library for loading and normalizing MS/MS peak data prior to loss computation.)
- **CLERMS** (Reference implementation combining InfoNCE and MSE into a composite loss for MS/MS spectra representation.) — https://github.com/HaldamirS/CLERMS

## Evaluation signals

- Verify loss computation on synthetic embedding tensors produces non-NaN, finite scalar values for both InfoNCE and MSE components.
- Check gradient flow: backward pass through composite loss produces non-zero gradients for all trainable parameters in the embedder.
- Confirm weighted sum computation: loss_total = alpha * loss_infonce + beta * loss_mse with configurable weights, and verify both components contribute when weights are non-zero.
- Validate contrastive behavior: InfoNCE loss decreases when paired spectra have high structural similarity (Tanimoto score) and increases for random negative pairs.
- Monitor loss convergence during training: composite loss should decrease monotonically on validation batches over epochs, indicating stable optimization.

## Limitations

- Requires pre-computed Tanimoto structural similarity scores (computed separately via cal_tanimoto_score.ipynb); InfoNCE alone cannot generate these labels.
- Performance depends on correct normalization of peak intensities in preprocessing; missing or inaccurate records in raw spectra data must be removed before training.
- Loss function design assumes balanced contributions from both contrastive and reconstruction objectives; suboptimal weight choices (alpha, beta) may lead to one term dominating.
- Composite loss is demonstrated on GNPS dataset; generalization to other MS/MS databases or different spectra types (e.g., different ionization modes) is not discussed.

## Evidence

- [other] CLERMS uses a novel composite loss function that combines InfoNCE loss and MSE loss to obtain good embeddings from peak information and metadata using a sinusoidal embedder within a transformer-based architecture.: "combines InfoNCE loss and MSE loss to obtain good embeddings from peak information and metadata using a sinusoidal embedder within a transformer-based architecture"
- [other] Define the InfoNCE contrastive loss function operating on peak-information and metadata embeddings with temperature scaling.: "Define the InfoNCE contrastive loss function operating on peak-information and metadata embeddings with temperature scaling"
- [other] Implement the composite loss as a weighted sum of InfoNCE and MSE terms.: "Implement the composite loss as a weighted sum of InfoNCE and MSE terms"
- [other] Wrap the composite loss in a PyTorch module with configurable weight parameters.: "Wrap the composite loss in a PyTorch module with configurable weight parameters"
- [other] Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module.: "Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module"
- [readme] The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss"
- [readme] To get the structural similarity for the model training, we calculate the score from the input data. In this process, just run cal_tanimoto_score.ipynb.: "To get the structural similarity for the model training, we calculate the score from the input data. In this process, just run cal_tanimoto_score.ipynb"
