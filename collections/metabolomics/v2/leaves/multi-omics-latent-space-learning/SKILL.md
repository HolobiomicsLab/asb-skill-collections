---
name: multi-omics-latent-space-learning
description: Use when you have preprocessed and jointly normalized ST and SM data
  from the same sample(s) aligned to a common spatial resolution (via joint_adata_sm_st
  and normalize_total_joint_adata_sm_st), and you need to discover shared latent structure
  across modalities to identify co-localized spatial.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_3895
  - http://edamontology.org/topic_0092
  tools:
  - spatialMETA
  techniques:
  - MS-imaging
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-omics-latent-space-learning

## Summary

Train a conditional variational autoencoder (ConditionalVAESTSM) on joint spatial transcriptomics and spatial metabolomics data to learn unified latent representations across modalities at aligned spatial resolution. This skill enables cross-modal pattern discovery and downstream integration analysis in the SpatialMETA framework.

## When to use

You have preprocessed and jointly normalized ST and SM data from the same sample(s) aligned to a common spatial resolution (via joint_adata_sm_st and normalize_total_joint_adata_sm_st), and you need to discover shared latent structure across modalities to identify co-localized spatial patterns or enable cross-modal imputation and visualization.

## When NOT to use

- Input ST and SM data are not yet aligned to a common spatial resolution; run spot_align_byknn and joint_adata_sm_st first.
- Input expression data is not normalized; apply normalize_total_joint_adata_sm_st before model training.
- You have only single-modality data (ST or SM alone); ConditionalVAESTSM requires both modalities to learn conditional structure.

## Inputs

- Joint normalized AnnData object (ST and SM combined, output from normalize_total_joint_adata_sm_st)
- Expression matrix (.X layer) containing normalized counts for both modalities
- Spatial coordinates stored in .obsm

## Outputs

- Fitted ConditionalVAESTSM model state (serialized to disk)
- Latent embeddings (stored in AnnData.obsm)
- Reconstructed normalized expression predictions for validation

## How to apply

Initialize a ConditionalVAESTSM model by specifying latent dimension, encoder/decoder layer sizes, and conditional layer dimension appropriate to your data's complexity. Call ConditionalVAESTSM.fit() on the normalized joint expression matrix to optimize the conditional VAE objective, learning latent embeddings that capture both ST and SM signal. Extract latent embeddings via ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm for downstream spatial analysis. Validate by retrieving normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() and comparing reconstruction fidelity across both modalities. The model's capacity to align both modalities in a single latent space is validated by assessing whether embeddings cluster coherently by spatial location and whether cross-modal correlations emerge in the learned space.

## Related tools

- **spatialMETA** (Python package implementing ConditionalVAESTSM model and multi-omics integration workflow, including model initialization, fitting, and latent embedding extraction) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialMETA import ConditionalVAESTSM; model = ConditionalVAESTSM(latent_dim=32, encoder_layers=[256, 128], decoder_layers=[128, 256], conditional_dim=16); model.fit(joint_adata); latent = model.get_latent_embedding(); joint_adata.obsm['latent_CVAE'] = latent
```

## Evaluation signals

- Latent embeddings are successfully extracted and stored in AnnData.obsm with correct shape (n_spots × latent_dim)
- Reconstructed normalized expression predictions reproduce the input modalities with acceptable reconstruction error across ST and SM features
- Latent embeddings show spatial coherence: nearby spots in original coordinate space cluster together in learned latent space
- Cross-modal correlations emerge: ST and SM features sharing spatial localization exhibit correlated representations in the latent space
- Model training converges: VAE objective (ELBO) stabilizes and does not diverge; no numerical errors or NaN values in embeddings

## Limitations

- Requires both ST and SM data from the same sample(s) pre-aligned to unified spatial resolution; performance degrades if alignment quality is poor.
- Latent dimension and encoder/decoder architecture must be chosen empirically; no principled selection method is provided in the article.
- Computational cost scales with joint data size (total ST + SM spots × features); large datasets may require GPU acceleration.
- Model assumes that ST and SM distributions can be captured by a single shared latent space; highly divergent modality distributions may limit alignment quality.

## Evidence

- [other] Load preprocessed joint ST/SM AnnData object (output from joint_adata_sm_st and normalize_total_joint_adata_sm_st). Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension). Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities.: "Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension). Call ConditionalVAESTSM.fit() to train the model on normalized"
- [other] Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm. Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() for validation.: "Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm. Retrieve normalized expression predictions via ConditionalVAESTSM.get_normalized_expression() for"
- [other] SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow.: "SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow."
- [readme] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
- [readme] Update `spatialmeta.model.ConditionalVAESTSM`: "Update `spatialmeta.model.ConditionalVAESTSM`"
