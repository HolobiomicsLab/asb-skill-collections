---
name: spatial-transcriptomics-integration
description: Use when you have paired spatial transcriptomics and spatial metabolomics datasets from the same sample(s) that are at different spatial resolutions or coordinate systems, and you need to integrate them for joint analysis of cross-modal spatial patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3179
  tools:
  - spatialMETA
  - ConditionalVAESTSM
  - AnnData
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

# spatial-transcriptomics-integration

## Summary

Align and integrate spatial transcriptomics (ST) and spatial metabolomics (SM) data to a unified spatial resolution using conditional VAE models, enabling joint multi-omics analysis within the SpatialMETA framework. This skill unifies disparate spatial modalities so cross-modal patterns can be identified at consistent resolution.

## When to use

Apply this skill when you have paired spatial transcriptomics and spatial metabolomics datasets from the same sample(s) that are at different spatial resolutions or coordinate systems, and you need to integrate them for joint analysis of cross-modal spatial patterns. Typical trigger: ST data (gene expression at spots/pixels) and MS imaging data (metabolite abundance at m/z values) that must be harmonized before downstream analysis.

## When NOT to use

- Input ST and SM datasets are already at identical spatial resolution and do not require alignment — use simpler concatenation methods instead.
- Missing preprocessed AnnData objects or unnormalized raw expression data — must run preprocessing and normalization steps first.
- Single modality only (ST or SM alone) — this skill is designed for multi-modal fusion and would provide no added value for single-modality analysis.

## Inputs

- Preprocessed joint ST/SM AnnData object (normalized via normalize_total_joint_adata_sm_st)
- Architecture hyperparameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension)
- ST and SM expression matrices aligned to common coordinate system (output from spot_align_byknn)

## Outputs

- Fitted ConditionalVAESTSM model state (saved to disk)
- Latent embeddings (stored in AnnData.obsm)
- Normalized expression predictions (reconstructed ST/SM modalities)
- Unified multi-omics representation at common spatial resolution

## How to apply

Load preprocessed, normalized joint ST/SM AnnData objects (output from joint_adata_sm_st and normalize_total_joint_adata_sm_st). Initialize ConditionalVAESTSM with architecture parameters (latent dimension, encoder/decoder layer sizes, conditional layer dimension). Train the model by calling ConditionalVAESTSM.fit() on the normalized expression data, which optimizes the conditional VAE objective to learn shared latent representations bridging ST and SM modalities. After convergence, extract latent embeddings via ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm, then validate by retrieving normalized expression predictions using ConditionalVAESTSM.get_normalized_expression(). Save the fitted model state and embeddings to disk for reproducibility and downstream visualization or spatial pattern mining.

## Related tools

- **spatialMETA** (Implements the ConditionalVAESTSM model and core integration workflow for aligning ST and SM data to unified spatial resolution) — https://github.com/WanluLiuLab/SpatialMETA
- **ConditionalVAESTSM** (Conditional variational autoencoder architecture that learns shared latent representations across ST and SM modalities during fit()) — https://github.com/WanluLiuLab/SpatialMETA
- **AnnData** (Data structure for storing integrated ST/SM expression matrices, coordinates, and latent embeddings in obsm)

## Examples

```
from spatialMETA.model import ConditionalVAESTSM
model = ConditionalVAESTSM(latent_dim=32, encoder_layers=[256, 128], decoder_layers=[128, 256])
model.fit(adata_joint, epochs=100, batch_size=32)
latent_emb = model.get_latent_embedding()
adata_joint.obsm['X_spatialMETA'] = latent_emb
```

## Evaluation signals

- Latent embeddings are non-null and have expected dimensions matching the specified latent dimension parameter
- Normalized expression predictions reconstruct the input ST and SM modalities with low reconstruction error (validate via ConditionalVAESTSM.get_normalized_expression())
- Latent representations cluster spatial regions consistently across ST and SM, confirming cross-modal alignment (inspect via visualization functions)
- Model converges during training (loss decreases monotonically or reaches plateau within expected epoch count)
- Fitted model can be reloaded from disk and produce identical latent embeddings and predictions (reproducibility check)

## Limitations

- Requires ST and SM datasets to be already spatially aligned to a common coordinate system before model training (via spot_align_byknn); model assumes input alignment is correct and will not correct fundamental spatial misalignment.
- Performance depends on quality of input normalization; inadequately normalized or batch-corrected data may produce poor latent representations.
- Conditional VAE architecture imposes computational overhead; may not scale efficiently to very high-resolution spatial imaging (e.g., subcellular pixel-level data across large tissue areas).
- Model is trained on joint ST/SM data from specific sample(s); transfer to new samples or tissues may require retraining or fine-tuning.

## Evidence

- [other] SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow.: "SpatialMETA implements an alignment mechanism that unifies ST and SM data to a common spatial resolution as a core component of its multi-omics integration workflow"
- [other] Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities.: "Call ConditionalVAESTSM.fit() to train the model on normalized expression data, optimizing the conditional VAE objective to learn shared latent representations across ST and SM modalities"
- [other] Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm.: "Extract latent embeddings using ConditionalVAESTSM.get_latent_embedding() and store in AnnData.obsm"
- [readme] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
- [readme] integrates single or multiple sample data to identify cross-modal spatial patterns: "integrates single or multiple sample data to identify cross-modal spatial patterns"
