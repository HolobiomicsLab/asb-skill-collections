---
name: neural-network-hyperparameter-optimization
description: Use when when you have preprocessed joint ST/SM AnnData objects (output from joint_adata_sm_st and normalize_total_joint_adata_sm_st) and need to fit a ConditionalVAESTSM model to unify spatial transcriptomics and spatial metabolomics data to a common resolution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0091
  tools:
  - spatialMETA
derived_from:
- doi: 10.1038/s41467-025-63915-z
  title: SpatialMETA
evidence_spans:
- spatialMETA is a method for integrating spatial multi-omics data
- spatialmeta.pp.calculate_qc_metrics_sm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spatialmeta_cq
    doi: 10.1038/s41467-025-63915-z
    title: SpatialMETA
  dedup_kept_from: coll_spatialmeta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-63915-z
  all_source_dois:
  - 10.1038/s41467-025-63915-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-hyperparameter-optimization

## Summary

Optimize the architecture and training parameters of a conditional VAE model for joint spatial transcriptomics and metabolomics alignment. This skill tunes latent dimension, encoder/decoder layer sizes, and conditional layer dimensions to maximize the model's ability to learn shared representations across modalities.

## When to use

When you have preprocessed joint ST/SM AnnData objects (output from joint_adata_sm_st and normalize_total_joint_adata_sm_st) and need to fit a ConditionalVAESTSM model to unify spatial transcriptomics and spatial metabolomics data to a common resolution. Use this skill when you are uncertain about appropriate architecture parameters or when the default initialization produces poor alignment or unstable training.

## When NOT to use

- Input data is not jointly preprocessed or normalized using the SpatialMETA pipeline (joint_adata_sm_st and normalize_total_joint_adata_sm_st).
- You have only single-modality data (ST only or SM only); ConditionalVAESTSM is designed for multi-modal alignment.
- Spatial resolution alignment has already been performed by another method; this skill is redundant if ST and SM are already at unified resolution.

## Inputs

- Preprocessed joint ST/SM AnnData object with normalized expression data
- ConditionalVAESTSM model architecture specification (latent dimension, layer sizes, conditional layer dimension)

## Outputs

- Trained ConditionalVAESTSM model state
- Latent embeddings (stored in AnnData.obsm)
- Normalized expression predictions for validation

## How to apply

Initialize ConditionalVAESTSM with candidate architecture parameters: latent dimension (typically 10–50), encoder/decoder layer sizes (e.g., 256, 128 units per layer), and conditional layer dimension. Call ConditionalVAESTSM.fit() on the normalized joint expression data, monitoring the conditional VAE objective function across epochs to detect convergence or overfitting. Extract latent embeddings via ConditionalVAESTSM.get_latent_embedding() and validate alignment by comparing normalized expression predictions (ConditionalVAESTSM.get_normalized_expression()) against the input data; inspect whether ST and SM modalities occupy the same latent space by examining embedding distributions and cross-modal spatial pattern consistency. Adjust parameters iteratively if embeddings collapse to low rank, if the objective plateaus prematurely, or if predicted expression diverges significantly from the input.

## Related tools

- **spatialMETA** (Provides ConditionalVAESTSM model class, joint data preparation (joint_adata_sm_st, normalize_total_joint_adata_sm_st), and latent embedding extraction methods) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.model import ConditionalVAESTSM; model = ConditionalVAESTSM(latent_dim=32, encoder_dims=[256, 128], decoder_dims=[128, 256], conditional_dim=64); model.fit(adata_joint, epochs=100); latent = model.get_latent_embedding(); adata_joint.obsm['latent_embedding'] = latent
```

## Evaluation signals

- Conditional VAE objective function converges smoothly without early plateau or divergence during training.
- Latent embeddings are non-degenerate (rank > 1 and variance explained across latent dimensions is distributed, not concentrated in one dimension).
- Reconstructed normalized expression (via get_normalized_expression) exhibits low mean squared error or correlation > 0.8 with input expression data.
- Spatial transcriptomics and metabolomics samples cluster together in latent space (low inter-modality distance), indicating successful alignment.
- Extracted latent embeddings stored in AnnData.obsm match expected shape (n_spots, latent_dimension) and contain no NaNs or infinities.

## Limitations

- Model convergence and embedding quality depend on the choice of latent dimension and layer sizes; no automatic hyperparameter search is documented in the README.
- ConditionalVAESTSM requires normalized joint ST/SM data; poor preprocessing or batch effects upstream will degrade alignment.
- The article does not provide explicit guidance on hyperparameter ranges, learning rate, or stopping criteria; practitioners must experiment or rely on defaults.
- Validation relies on comparing reconstructed vs. input expression; systematic evaluation against ground truth cross-modal spatial patterns is not documented.

## Evidence

- [other] Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension).: "Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension)."
- [other] Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities.: "Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities."
- [other] Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm.: "Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm."
- [other] Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() for validation.: "Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() for validation."
- [readme] Update `spatialmeta.model.ConditionalVAESTSM`: "Update `spatialmeta.model.ConditionalVAESTSM`"
- [other] SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow.: "SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow."
