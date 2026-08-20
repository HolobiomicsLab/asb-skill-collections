---
name: mse-reconstruction-loss
description: Use when training embeddings from multi-modal spectral data (peak information
  + metadata) where you need to ensure both contrastive discriminability AND reconstruction
  fidelity. Specifically use it in transformer-based architectures that produce embeddings
  from heterogeneous inputs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3361
  tools:
  - PyTorch
  - Transformer architecture
  - Sinusoidal embedder
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

# MSE Reconstruction Loss for Embedding Validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

MSE reconstruction loss measures the fidelity of embeddings by computing mean squared error between original and reconstructed representations. In CLERMS, it is combined with InfoNCE contrastive loss to jointly optimize embedding quality from MS/MS spectra peak information and metadata.

## When to use

Apply this skill when training embeddings from multi-modal spectral data (peak information + metadata) where you need to ensure both contrastive discriminability AND reconstruction fidelity. Specifically use it in transformer-based architectures that produce embeddings from heterogeneous inputs (e.g., sinusoidal-encoded peaks and auxiliary metadata) and require validation that the embedding space preserves reconstructable information.

## When NOT to use

- When input spectra peak data are already aligned to a fixed schema and no information loss is acceptable—MSE alone does not enforce contrastive separation needed for compound identification.
- When the embedding space does not require reconstruction interpretability (e.g., supervised classification tasks without generative downstream use).
- When computational budget is severely constrained and multi-term loss functions cannot be afforded—MSE adds overhead to the optimization loop.

## Inputs

- Peak information tensors from MS/MS spectra (normalized intensity and m/z values)
- Metadata embeddings (e.g., molecular properties, structural features)
- Sinusoidal-encoded peak representations (output of sinusoidal embedder)
- Ground-truth or reference embeddings for reconstruction comparison

## Outputs

- MSE reconstruction loss scalar value (per batch)
- Reconstructed embedding tensors
- Composite loss value (InfoNCE + MSE terms weighted)
- Gradient tensors for backpropagation

## How to apply

Define an MSE reconstruction loss function that computes squared error between original embedding tensors and reconstructed embeddings passed through a decoder or projection layer. Weight this loss term (typically 0.0–1.0) and combine it additively with an InfoNCE contrastive loss using a composite loss function. The composite loss is a weighted sum: L_total = α × L_InfoNCE + β × L_MSE, where α and β are learnable or fixed weight parameters. Validate gradient flow through both loss terms to ensure backpropagation updates both the embedding encoder and reconstruction decoder. Tune the weight ratio empirically based on validation performance on downstream tasks (e.g., compound identification or spectra clustering on GNPS benchmark).

## Related tools

- **PyTorch** (Implements MSE loss module (torch.nn.MSELoss) and composite loss backward pass; wraps loss computation with configurable weight parameters and gradient tracking.) — https://pytorch.org
- **Transformer architecture** (Encodes peak information and metadata into embeddings; decoder projects embeddings back for MSE reconstruction loss computation.) — github.com/HaldamirS/CLERMS
- **Sinusoidal embedder** (Encodes peak positional and intensity information into learnable embeddings; output fed to MSE reconstruction loss.) — github.com/HaldamirS/CLERMS

## Evaluation signals

- Verify MSE loss decreases monotonically or in expected trend across training epochs; divergence signals misaligned scale or vanishing gradients.
- Check that gradient magnitudes for MSE term remain in a healthy range (e.g., 1e−4 to 1e−1) during backpropagation; extreme values indicate poor weight initialization or scale mismatch.
- Validate that composite loss (InfoNCE + MSE) correlates positively with downstream task performance (e.g., compound identification F1-score or spectra clustering ARI on GNPS dataset); negative correlation suggests misweighting α and β.
- Confirm reconstruction error (MSE value) is lower for in-distribution embeddings than out-of-distribution or adversarial embeddings, validating that the loss term captures data-specific structure.
- Cross-check that ablating the MSE term (β = 0) degrades reconstruction fidelity but may improve contrastive separation; validate trade-off tuning on held-out validation set.

## Limitations

- MSE reconstruction loss assumes linear reconstructibility; nonlinear decoder architectures may be required for complex peak manifolds, adding computational cost.
- The weighting parameters α and β are hyperparameters requiring empirical tuning; no principled setting is provided in CLERMS—grid search or Bayesian optimization is needed per dataset.
- MSE is sensitive to outliers in peak intensity or metadata values; preprocessing and normalization of input data (as described in dataset_preprocessing.ipynb) are prerequisites to avoid loss scale explosion.
- In multi-modal scenarios (heterogeneous peak and metadata types), MSE treats all dimensions equally; weighted MSE or per-modality scaling may be necessary if modalities have different intrinsic variance.

## Evidence

- [readme] The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak information and the metadata.: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak"
- [other] CLERMS uses a novel composite loss function that combines InfoNCE loss and MSE loss to obtain good embeddings from peak information and metadata using a sinusoidal embedder within a transformer-based architecture.: "CLERMS uses a novel composite loss function that combines InfoNCE loss and MSE loss to obtain good embeddings from peak information and metadata using a sinusoidal embedder within a transformer-based"
- [other] Implement the composite loss as a weighted sum of InfoNCE and MSE terms.: "Implement the composite loss as a weighted sum of InfoNCE and MSE terms."
- [other] Wrap the composite loss in a PyTorch module with configurable weight parameters.: "Wrap the composite loss in a PyTorch module with configurable weight parameters."
- [other] Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module.: "Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module."
- [readme] Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for the model input.: "Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for"
