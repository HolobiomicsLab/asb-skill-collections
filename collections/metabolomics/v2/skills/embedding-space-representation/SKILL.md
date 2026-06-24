---
name: embedding-space-representation
description: Use when you have pairs or triplets of MS/MS spectra with associated
  metadata (compound structural information, Tanimoto similarity scores) and want
  to learn embeddings that simultaneously preserve spectral similarity relationships
  and reconstruct peak intensities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Transformer (torch.nn.Transformer or variant)
  - scikit-learn
  - matchms
  techniques:
  - direct-infusion-MS
  license_tier: restricted
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

# embedding-space-representation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct composite loss functions combining contrastive (InfoNCE) and reconstruction (MSE) terms to learn dense embeddings from MS/MS spectra peak information and metadata. This skill applies contrastive learning principles to mass spectrometry data where both pairwise similarity and peak-intensity reconstruction are training signals.

## When to use

You have pairs or triplets of MS/MS spectra with associated metadata (compound structural information, Tanimoto similarity scores) and want to learn embeddings that simultaneously preserve spectral similarity relationships and reconstruct peak intensities. Use this when shallow spectra matching or clustering tasks require dense, learned representations rather than hand-crafted features.

## When NOT to use

- Raw, unpreprocessed MS/MS spectra with missing or inaccurate peak data — preprocess with dataset_preprocessing.ipynb first.
- When Tanimoto or structural similarity scores are unavailable or uncomputed — cal_tanimoto_score.ipynb must be run to provide training supervision.
- For real-time inference or minimal-latency applications — the transformer backbone and composite loss add computational overhead unsuitable for edge deployment.

## Inputs

- Peak intensity vectors normalized to [0, 1] range from MS/MS spectra
- Metadata embeddings (e.g., structural fingerprints or derived features)
- Pairwise similarity scores (e.g., Tanimoto similarity between compounds)
- Batch of spectra (processed via dataset_preprocessing.ipynb)

## Outputs

- Dense embedding vectors from the transformer encoder
- Composite loss scalar (InfoNCE + weighted MSE)
- Per-batch loss breakdown (InfoNCE component, MSE component)
- Reconstructed peak intensity vectors (for validation)

## How to apply

Define an InfoNCE contrastive loss that operates on peak-information and metadata embeddings with temperature scaling to measure spectral similarity in embedding space. Simultaneously define an MSE reconstruction loss that enforces the embedding to reconstruct the original peak intensities. Combine both losses as a weighted sum with tunable parameters (typically equal or MSE-weighted higher) to balance contrastive discrimination with reconstruction fidelity. Implement within a PyTorch module with a sinusoidal embedder and transformer encoder backbone. Validate by confirming gradients flow through both loss terms and that loss magnitudes remain stable across training steps.

## Related tools

- **PyTorch** (Framework for defining and training the composite loss module with autograd gradient flow)
- **Transformer (torch.nn.Transformer or variant)** (Backbone encoder architecture that produces embeddings from peak and metadata inputs)
- **scikit-learn** (Utility for structural similarity computation (Tanimoto) and evaluation metrics)
- **matchms** (Library for MS/MS spectrum matching and preprocessing (version 0.18.0 in CLERMS requirements))

## Evaluation signals

- Composite loss decreases monotonically across training epochs; both InfoNCE and MSE components exhibit independent gradient-based descent.
- Embedding space clusters spectra by compound identity — measured via compound identification accuracy or NMI on held-out GNPS test set.
- Reconstructed peak intensities achieve MSE < 0.05 on validation spectra (normalized intensity range).
- Embedding dimension matches transformer output size (e.g., 256 or 512 dims); no NaN or inf values in loss or gradient tensors.
- Contrastive loss temperature parameter (~0.07) yields stable gradient magnitudes and prevents loss saturation in early training.

## Limitations

- Requires clean, preprocessed spectra; records with inaccurate data or missing information must be removed beforehand (see dataset_preprocessing.ipynb).
- Composite loss is sensitive to the weighting coefficient between InfoNCE and MSE terms — no principled default is provided; grid search or manual tuning required.
- Performance validation is dataset-specific (GNPS); transfer to other spectral databases (e.g., MassBank, Spectral libraries) is not discussed.
- Sinusoidal embedder design is not detailed; unclear how frequency and phase parameters affect learned representations.

## Evidence

- [readme] The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak"
- [other] Define the InfoNCE contrastive loss function operating on peak-information and metadata embeddings with temperature scaling: "1. Define the InfoNCE contrastive loss function operating on peak-information and metadata embeddings with temperature scaling."
- [other] Implement the composite loss as a weighted sum of InfoNCE and MSE terms: "3. Implement the composite loss as a weighted sum of InfoNCE and MSE terms."
- [other] Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module: "5. Validate the loss computation on synthetic embedding tensors and verify gradient flow through the module."
- [readme] Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data.: "Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data."
- [readme] To get the structural similarity for the model training, we calculate the score from the input data. In this process, just run `cal_tanimoto_score.ipynb`.: "To get the structural similarity for the model training, we calculate the score from the input data. In this process, just run `cal_tanimoto_score.ipynb`."
