---
name: gradient-flow-verification
description: Use when after implementing a composite loss function that combines multiple
  loss terms (e.g., InfoNCE contrastive loss and MSE reconstruction loss) in a PyTorch
  module, and before running full-scale training on MS/MS spectra data.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - PyTorch
  - Transformer
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

# Gradient-flow-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that gradients propagate correctly through a composite loss function (combining InfoNCE and MSE terms) during backpropagation in a transformer-based embedding model. This validation ensures that both contrastive and reconstruction loss components contribute meaningfully to weight updates during training.

## When to use

After implementing a composite loss function that combines multiple loss terms (e.g., InfoNCE contrastive loss and MSE reconstruction loss) in a PyTorch module, and before running full-scale training on MS/MS spectra data. Apply this skill when you need to confirm that gradients flow through all learnable parameters in the sinusoidal embedder and transformer layers without vanishing or exploding.

## When NOT to use

- Input embeddings are already detached or frozen (gradients will always be None by design).
- Loss function uses only a single term (e.g., only InfoNCE); gradient flow is trivial and requires no composite verification.
- Model has been trained and converged; gradient inspection is a post-hoc debug step, not a real-time training signal.

## Inputs

- Synthetic peak-information embeddings (torch.Tensor: batch_size × embedding_dim)
- Synthetic metadata embeddings (torch.Tensor: batch_size × embedding_dim)
- Composite loss module with configurable InfoNCE and MSE weights (torch.nn.Module)
- Learnable parameters of sinusoidal embedder and transformer layers

## Outputs

- Gradient tensors for all trainable parameters (verified non-None and finite)
- Gradient norm statistics per layer (mean, max, min)
- Validation report confirming gradient flow through composite loss

## How to apply

1. Create synthetic embedding tensors with the same shape and device as your actual peak-information and metadata embeddings (e.g., batch_size × embedding_dim). 2. Pass these tensors through your composite loss module (weighted sum of InfoNCE and MSE terms) with a known set of weights. 3. Call .backward() on the resulting loss scalar. 4. Inspect the `.grad` attribute of all trainable parameters in the embedder and transformer layers to verify they are non-None and not uniformly zero. 5. Check that gradient magnitudes are within a reasonable range (not NaN, not explosively large) by computing gradient norms. 6. Repeat with different weight configurations to confirm both InfoNCE and MSE components contribute to gradients.

## Related tools

- **PyTorch** (Framework for defining composite loss modules, executing backpropagation, and inspecting gradient tensors)
- **Transformer** (Architecture component whose parameters must receive non-zero gradients from the composite loss)

## Evaluation signals

- All trainable parameters in the sinusoidal embedder and transformer layers have non-None .grad attributes after backward().
- Gradient norms (torch.nn.utils.clip_grad_norm_) are finite and within typical ranges (e.g., 0.01–10.0); no NaN or inf values.
- InfoNCE term weight > 0 produces non-zero gradients; MSE term weight > 0 produces non-zero gradients; composite loss combines both.
- Gradient flow test passes on synthetic tensors before training on actual GNPS MS/MS spectra data.
- Comparison of gradient magnitudes across different weight configurations shows that neither InfoNCE nor MSE term is masked or inactive.

## Limitations

- Synthetic tensor test does not guarantee correct gradient flow on real MS/MS peak information and metadata; recommend validation on a small batch from preprocessed GNPS data after dataset_preprocessing.ipynb.
- Gradient flow verification does not detect semantic issues in loss function design (e.g., incorrect temperature scaling in InfoNCE or wrong reconstruction target in MSE); it only confirms mathematical differentiability.
- High gradient norms may indicate instability in the composite weight balance; additional techniques (e.g., gradient clipping, learning rate tuning) may be needed.

## Evidence

- [other] Wrap the composite loss in a PyTorch module with configurable weight parameters: "Wrap the composite loss in a PyTorch module with configurable weight parameters."
- [other] Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module: "Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module."
- [other] Implement the composite loss as a weighted sum of InfoNCE and MSE terms: "Implement the composite loss as a weighted sum of InfoNCE and MSE terms."
- [intro] The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss"
