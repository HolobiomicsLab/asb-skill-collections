---
name: spatial-metabolomics-integration
description: Use when when you have paired spatial metabolomics and spatial transcriptomics measurements from the same tissue samples and need to identify how metabolite distributions relate to gene expression patterns at aligned spatial coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
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

# spatial-metabolomics-integration

## Summary

Integrate spatial metabolomics (SM) data with spatial transcriptomics (ST) data by aligning them to a unified spatial resolution and learning shared latent representations across modalities. This skill enables identification of cross-modal spatial patterns in multi-omics tissue studies.

## When to use

When you have paired spatial metabolomics and spatial transcriptomics measurements from the same tissue samples and need to identify how metabolite distributions relate to gene expression patterns at aligned spatial coordinates. Specifically, use this when SM data has been preprocessed (read from CSV or imzML, merged across ionization modes, and filtered) and ST data is available as normalized AnnData, and you aim to discover concordant or discordant spatial features across the two modalities.

## When NOT to use

- Input spatial metabolomics data has not been preprocessed (QC metrics not calculated, or contains unfiltered low-quality spots/metabolites)
- Spatial transcriptomics and metabolomics data are from different tissue samples or lack common spatial coordinates for alignment
- You only have single-modality data (SM or ST alone); the integration skill requires both modalities to learn shared representations

## Inputs

- Preprocessed spatial metabolomics AnnData object (from read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg with QC metrics and filtering applied)
- Preprocessed spatial transcriptomics AnnData object (normalized and with spatial coordinates)
- Architecture hyperparameters: latent dimension, encoder/decoder layer sizes, conditional layer dimension

## Outputs

- Fitted ConditionalVAESTSM model (saved to disk)
- Joint AnnData object with shared latent embeddings stored in .obsm
- Normalized expression predictions from the model for both ST and SM modalities
- Unified spatial resolution coordinate system for ST and SM spots

## How to apply

Load preprocessed spatial metabolomics and spatial transcriptomics AnnData objects. Apply spot_align_byknn to align SM and ST spots to a common spatial resolution using k-nearest neighbors. Create a joint AnnData object via joint_adata_sm_st that combines both modalities. Normalize the joint data using normalize_total_joint_adata_sm_st. Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension) and call fit() to train the conditional variational autoencoder on the normalized joint expression data. Extract latent embeddings via get_latent_embedding() — these shared representations capture cross-modal spatial structure. Validate the fit by comparing original and reconstructed expression via get_normalized_expression(). The conditional VAE learns which features in one modality predict features in the other, enabling downstream analysis of spatially coordinated metabolite–gene relationships.

## Related tools

- **spatialMETA** (Core integration framework providing spot_align_byknn, joint_adata_sm_st, normalize_total_joint_adata_sm_st, ConditionalVAESTSM model, and latent embedding extraction functions for multi-omics spatial alignment and learning) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.model import ConditionalVAESTSM; model = ConditionalVAESTSM(latent_dim=20, encoder_layers=[256, 128], decoder_layers=[128, 256]); model.fit(adata_joint); latent_emb = model.get_latent_embedding(); adata_joint.obsm['latent_embedding'] = latent_emb
```

## Evaluation signals

- Latent embeddings have reduced dimensionality compared to original data (e.g., latent_dim << number of genes + metabolites) and capture variance from both modalities
- Reconstructed expression (from get_normalized_expression) shows good correlation with original normalized values, indicating the model learned valid data distribution
- Aligned spots from ST and SM occupy nearby regions in latent space, demonstrating that the conditional VAE captured spatial coherence
- QC metric distributions (per-spot total intensity, metabolite detection frequency) remain consistent before and after alignment, signaling no data corruption
- Joint AnnData.obsm contains embeddings with shape (n_spots, latent_dimension) and no NaN or Inf values

## Limitations

- Requires careful hyperparameter tuning (latent dimension, layer sizes) to balance model complexity and generalization; poor choices may lead to underfit or overfit latent representations
- Assumes spatial coordinates and spot annotations are reliable; misalignment or coordinate drift between ST and SM platforms can propagate errors into shared embeddings
- Conditional VAE assumes multimodal data is generated from a shared latent distribution; if ST and SM patterns are fundamentally uncorrelated, learned representations may be uninformative
- Computational cost scales with the number of spots and features; very large datasets may require subsampling or distributed training (not discussed in methods)

## Evidence

- [other] SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow.: "SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow"
- [other] ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities.: "Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities"
- [other] Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm.: "Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm"
- [readme] SMOI aligns ST and SM to a unified resolution, integrates single or multiple sample data to identify cross-modal spatial patterns: "SMOI aligns ST and SM to a unified resolution, integrates single or multiple sample data to identify cross-modal spatial patterns"
- [other] Load preprocessed joint ST/SM AnnData object (output from joint_adata_sm_st and normalize_total_joint_adata_sm_st).: "Load preprocessed joint ST/SM AnnData object (output from joint_adata_sm_st and normalize_total_joint_adata_sm_st)"
