---
name: spatial-data-integration-preprocessing
description: Use when when you have paired spatial transcriptome and metabolome datasets (in .h5ad or matrix format) with spatial location information, and you need to establish correspondence between features across modalities before performing spatial morphological alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0621
  tools:
  - haCCA
derived_from:
- doi: 10.1101/2024.08.20.608773v2
  title: haCCA
evidence_spans:
- haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hacca_cq
    doi: 10.1101/2024.08.20.608773v2
    title: haCCA
  dedup_kept_from: coll_hacca_cq
schema_version: 0.2.0
---

# spatial-data-integration-preprocessing

## Summary

Identify and rank high-correlation feature pairs between spatial transcriptome and metabolome datasets as a prerequisite for spot-to-spot multi-modal alignment. This skill prepares paired omics data for integrated spatial registration by computing correlation scores and filtering to retain only the strongest cross-modal associations.

## When to use

When you have paired spatial transcriptome and metabolome datasets (in .h5ad or matrix format) with spatial location information, and you need to establish correspondence between features across modalities before performing spatial morphological alignment. Use this skill when correlation-based feature linking is the intended bridging mechanism for spot-to-spot integration.

## When NOT to use

- Input datasets are already unimodal (single omics type only, not paired transcriptome–metabolome)
- Spatial location information is absent or not aligned between modalities
- Feature matrices have already been pre-integrated or consensus-selected via other means

## Inputs

- Transcriptome feature matrix (h5ad X array or numpy ndarray)
- Metabolome feature matrix (h5ad X array or numpy ndarray)
- Spatial coordinate matrix for transcriptome (h5ad obsm['spatial'])
- Spatial coordinate matrix for metabolome (h5ad obsm['spatial'])

## Outputs

- Ranked feature pair list with correlation coefficients
- Correlation score matrix (filtered by threshold)
- Metadata-enriched pair associations (feature names, absolute correlation values)

## How to apply

Load spatial transcriptome and metabolome feature matrices (X arrays) along with spatial coordinate matrices (obsm['spatial']). Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features. Apply a correlation threshold to retain only high-confidence feature pairs; rank the filtered pairs by absolute correlation coefficient in descending order. Return the ranked feature pair list with correlation scores and metadata. The ranking serves to prioritize strongest cross-modal associations for downstream spatial morphological alignment steps.

## Related tools

- **haCCA** (Orchestrates high-correlated feature pair identification and ranking as part of multi-module spatial transcriptome–metabolome integration workflow) — github.com/LittleLittleCloud/haCCA

## Examples

```
from hacca import Data; import scanpy as sc; a_h5ad = sc.read_h5ad('transcriptome.h5ad'); b_h5ad = sc.read_h5ad('metabolome.h5ad'); a = Data(X=a_h5ad.X.toarray(), D=a_h5ad.obsm['spatial']); b = Data(X=b_h5ad.X.toarray(), D=b_h5ad.obsm['spatial'])
```

## Evaluation signals

- Correlation coefficient distribution is unimodal or bimodal (depending on true correlation structure); mean and median are reasonable for the modality pair (e.g., not collapsed to zero or ±1)
- Ranked pair list is non-empty after filtering and contains pairs with absolute correlation ≥ threshold (verify threshold was applied consistently)
- Feature pair IDs are valid and traceable back to input feature matrices; no orphaned or duplicated pairs
- Metadata fields are populated for all retained pairs (correlation score, feature names, p-values if computed); no missing or NaN values in rank column
- Downstream spatial morphological alignment (manual_gross_alignment, icp_3d_alignment, direct_alignment) successfully ingests the pair rankings without error

## Limitations

- Pearson/Spearman correlation assumes linear associations; non-linear feature relationships will not be captured
- Correlation threshold choice is user-dependent; no adaptive or data-driven threshold selection is described
- Feature pairs are ranked independently of spatial context; correlation alone does not guarantee spatial co-localization
- Assumes both feature matrices are comparable in scale and distribution; extreme skew or batch effects may inflate/deflate correlations

## Evidence

- [other] Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features.: "Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features."
- [other] haCCA utilizes high correlated feature pairs as a core component of its workflow, which are combined with modified spatial morphological alignment to integrate spatial transcriptomes and metabolomes.: "haCCA utilizes high correlated feature pairs as a core component of its workflow, which are combined with modified spatial morphological alignment to integrate spatial transcriptomes and metabolomes."
- [other] Filter feature pairs by correlation threshold to retain only high-correlation pairs.: "Filter feature pairs by correlation threshold to retain only high-correlation pairs."
- [other] Rank filtered pairs by absolute correlation coefficient in descending order.: "Rank filtered pairs by absolute correlation coefficient in descending order."
- [readme] Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information: "Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information"
