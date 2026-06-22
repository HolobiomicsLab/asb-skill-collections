---
name: variational-autoencoder-training
description: Use when after preprocessing and normalizing joint ST/SM AnnData objects using joint_adata_sm_st and normalize_total_joint_adata_sm_st, when you need to align spatial transcriptomics and metabolomics data to a unified latent resolution for multi-omics integration and cross-modal spatial pattern.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3173
  tools:
  - spatialMETA
  techniques:
  - MS-imaging
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

# variational-autoencoder-training

## Summary

Train a conditional VAE model on joint spatial transcriptomics and spatial metabolomics data to learn shared latent representations across modalities. This skill produces unified embeddings and normalized expression predictions that enable downstream cross-modal spatial pattern discovery.

## When to use

After preprocessing and normalizing joint ST/SM AnnData objects using joint_adata_sm_st and normalize_total_joint_adata_sm_st, when you need to align spatial transcriptomics and metabolomics data to a unified latent resolution for multi-omics integration and cross-modal spatial pattern identification.

## When NOT to use

- Input data is not normalized or jointly preprocessed—run normalize_total_joint_adata_sm_st first
- You have only single-modality data (ST or SM alone) without cross-modal alignment goals
- Latent dimension or layer sizes are not justified by your data's complexity or downstream analysis requirements

## Inputs

- joint preprocessed AnnData object (ST/SM) from joint_adata_sm_st
- normalized joint AnnData object from normalize_total_joint_adata_sm_st
- architecture parameters (latent_dim, encoder_layer_sizes, decoder_layer_sizes, conditional_layer_dim)

## Outputs

- trained ConditionalVAESTSM model state
- latent embeddings (stored in AnnData.obsm)
- normalized expression predictions
- serialized model checkpoint

## How to apply

Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension) appropriate to your data dimensionality. Call ConditionalVAESTSM.fit() to train the model on the normalized joint expression data, optimizing the conditional VAE objective to learn shared latent representations bridging ST and SM modalities. Extract learned latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm for downstream analysis. Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() to validate reconstruction quality. Save the fitted model state and embeddings to disk for reproducibility and reuse.

## Related tools

- **spatialMETA** (framework implementing ConditionalVAESTSM model and VAE training workflow for spatial multi-omics integration) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.model import ConditionalVAESTSM
model = ConditionalVAESTSM(latent_dim=32, encoder_layer_sizes=[256, 128], decoder_layer_sizes=[128, 256], conditional_layer_dim=64)
model.fit(joint_adata.X, epochs=100, batch_size=32)
latent_embeddings = model.get_latent_embedding()
reconstructed_expr = model.get_normalized_expression()
```

## Evaluation signals

- Latent embeddings have expected dimensionality (latent_dim) and are stored in AnnData.obsm without NaN/Inf values
- Normalized expression predictions reconstruct the input data with low reconstruction error (check via ConditionalVAESTSM.get_normalized_expression() vs. input expression)
- Model training converges (loss decreases monotonically or reaches stable plateau across training epochs)
- Latent embeddings are continuous and map spatial coordinates smoothly without isolated clusters unrelated to biology
- Cross-modal correlation in latent space is higher than expected by chance (e.g., ST and SM spots co-localized in latent space align in physical coordinates)

## Limitations

- ConditionalVAESTSM requires pre-aligned or co-localized ST and SM spots; misalignment will degrade latent representation quality
- Model performance depends on careful tuning of architecture parameters (latent dimension, layer sizes); no universal defaults are provided
- VAE training is stochastic; reproducibility requires fixed random seeds and documented hyperparameters
- Computational cost scales with data size (number of spots and features); very large datasets may require GPU acceleration or data subsampling

## Evidence

- [other] How does the ConditionalVAESTSM model align spatial transcriptomics (ST) and spatial metabolomics (SM) data to a unified resolution within the SpatialMETA integration framework?: "ConditionalVAESTSM model align spatial transcriptomics (ST) and spatial metabolomics (SM) data to a unified resolution"
- [other] Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension).: "Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension)"
- [other] Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities.: "Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations"
- [other] Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm.: "Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm"
- [other] Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() for validation.: "Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() for validation"
- [other] SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow.: "alignment mechanism that unifies ST and SM data to a common spatial resolution"
- [readme] Update `spatialmeta.model.ConditionalVAESTSM`: "Update `spatialmeta.model.ConditionalVAESTSM`"
