---
name: representation-vector-dimensionality-reduction
description: Use when after obtaining 512-dimensional representation vectors from the Encoder module, when you need to compress these vectors for visualization, clustering, or downstream classification tasks on mass spectrometry imaging data while maintaining interpretability of ion relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - ResNet18
  - UMAP
  - scikit-learn
  - PyTorch
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepion
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  dedup_kept_from: coll_deepion
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05002
  all_source_dois:
  - 10.1021/acs.analchem.3c05002
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Representation Vector Dimensionality Reduction

## Summary

Reduce 512-dimensional encoder output vectors to low-dimensional representations (e.g., 20-D) suitable for downstream analysis tasks in mass spectrometry imaging. This skill applies unsupervised dimensionality reduction to learned ion image representations while preserving spatial and chemical relationships.

## When to use

After obtaining 512-dimensional representation vectors from the Encoder module, when you need to compress these vectors for visualization, clustering, or downstream classification tasks on mass spectrometry imaging data while maintaining interpretability of ion relationships (co-localization or isotope patterns).

## When NOT to use

- Input vectors are already low-dimensional (< 50 dimensions) — reduction may lose critical discriminative information
- Task requires interpretable feature importance or explicit ion-to-dimension mapping — UMAP produces non-linear, uninterpretable embeddings
- Real-time inference with strict latency constraints — UMAP transform can be computationally expensive for large batch sizes

## Inputs

- 512-dimensional representation vectors (output from Encoder module, shape: [batch_size, 512])
- Ion image metadata (ion m/z values, spatial coordinates from MSI data) for validation

## Outputs

- 20-dimensional reduced representation vectors (shape: [batch_size, 20])
- Dimensionality reduction model (fitted UMAP transformer for use on new data)

## How to apply

Apply the Dimensionality Reduction module (UMAP as specified in requirements) to the 512-dimensional representation vectors output by the Encoder to produce 20-dimensional vectors suitable for downstream tasks. Configure UMAP with n_neighbors and min_dist parameters appropriate for ion image manifold structure; validate that the reduced vectors preserve local clustering of co-localized or isotope ions by comparing pair-wise distances before and after reduction. Ensure numerical stability and check that variance is not concentrated in a single dimension, which would indicate loss of representational structure.

## Related tools

- **UMAP** (Primary dimensionality reduction algorithm to compress 512-D vectors to 20-D for downstream analysis)
- **scikit-learn** (Used for distance metrics and clustering validation of reduced vectors)
- **PyTorch** (Tensor operations and batch processing for efficiency during dimensionality reduction)

## Examples

```
from umap import UMAP
reducer = UMAP(n_neighbors=15, min_dist=0.1, n_components=20)
reduced_vectors = reducer.fit_transform(encoder_output_512d)
```

## Evaluation signals

- Output tensor shape is [batch_size, 20] with no NaN or inf values
- Pair-wise Euclidean distances between co-localized or isotope ion vectors are preserved relative to 512-D space (Spearman correlation > 0.8 on distance rankings)
- Visual inspection: 2-D or 3-D projection of 20-D vectors shows clear clustering of ions by mode (COL/ISO) or known ion relationships
- Downstream task (e.g., nearest-neighbor retrieval for co-localization) achieves comparable recall@k to full 512-D vectors
- UMAP hyperparameters are reproducible and consistent across multiple random seeds (if using stochastic UMAP)

## Limitations

- UMAP is non-linear and non-invertible — individual dimensions are not interpretable as ion properties; feature importance cannot be directly extracted
- Reduction quality depends on UMAP hyperparameter tuning (n_neighbors, min_dist); suboptimal settings can destroy local or global structure
- 20-dimensional target may be too aggressive for complex ion image datasets; information loss is not quantified without explicit reconstruction error measurement
- README specifies UMAP version 0.5.1 (dated circa 2020); compatibility with newer PyTorch and Python versions (3.8+) is not guaranteed

## Evidence

- [readme] Dimensionality Reduction module. This module is applied to further reduce the dimensionality of ion image representation to a 20-dimensional vector O for downstream tasks.: "This module is applied to further reduce the dimensionality of ion image representation to a 20-dimensional vector O for downstream tasks"
- [readme] Encoder module. Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors.: "output two 512-dimensional representation vectors"
