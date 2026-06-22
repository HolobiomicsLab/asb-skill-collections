---
name: spatial-transcriptome-metabolome-coregistration
description: Use when you have paired spatial transcriptome and metabolome datasets (both as h5ad files with .obsm['spatial'] coordinate matrices and .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0091
  tools:
  - haCCA
  - scanpy
  techniques:
  - MS-imaging
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.08.20.608773v2
  all_source_dois:
  - 10.1101/2024.08.20.608773v2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spatial Transcriptome–Metabolome Coregistration

## Summary

Aligns spot coordinates between paired spatial transcriptome and metabolome datasets using high-correlated feature pairs and modified spatial morphological alignment to enable integrated spot-to-spot analysis. This skill bridges two complementary spatial omics modalities by registering their spot geometries and feature spaces for joint interpretation.

## When to use

You have paired spatial transcriptome and metabolome datasets (both as h5ad files with .obsm['spatial'] coordinate matrices and .X feature matrices) acquired from the same or adjacent tissue sections, and you need to integrate their spot-level information to correlate gene expression with metabolite abundance or discover co-localized transcriptomic–metabolomic signatures.

## When NOT to use

- Input datasets are from different tissue samples or anatomically unrelated regions—coregistration assumes shared or adjacent spatial domains.
- Spatial coordinates are already pre-registered by the imaging platform—redundant alignment may introduce noise.
- Feature matrices are sparse or missing (<<1% non-zero entries per spot)—feature correlation detection becomes unreliable.

## Inputs

- Spatial transcriptome h5ad file with feature matrix (X) and spatial coordinates (obsm['spatial'])
- Spatial metabolome h5ad file with feature matrix (X) and spatial coordinates (obsm['spatial'])
- Optional: cluster labels (obsm) for each modality

## Outputs

- Aligned spatial coordinate mappings for both modalities
- Integrated feature matrix with spot-to-spot correspondence
- Coordinate transformation parameters (rotation, translation, scale, local warps)

## How to apply

Load both modality datasets as Data objects (triplet of feature matrix X, spatial coordinate matrix D, and optional cluster labels). Apply a three-stage alignment pipeline: (1) gross alignment to establish initial coordinate correspondence using manual_gross_alignment or icp_3d_alignment to handle rotation, translation, and scale differences; (2) refined feature-driven alignment via direct_alignment to warp spot positions based on high-correlated feature pair correspondences; (3) validate by checking coordinate overlap metrics and verifying that aligned spots from both modalities occupy consistent spatial regions. The modified morphological alignment component leverages identified feature correlations to infer local spatial deformations, ensuring biological relevance rather than purely geometric registration.

## Related tools

- **haCCA** (Implements high-correlated feature pair identification and modified spatial morphological alignment for multimodal spot registration and integrated analysis) — https://github.com/LittleLittleCloud/haCCA
- **scanpy** (Provides h5ad file I/O and data structure management (anndata.AnnData) for loading and manipulating spatial omics datasets)

## Examples

```
from hacca import *; import scanpy as sc; a = Data(X=sc.read_h5ad('transcriptome.h5ad').X.toarray(), D=sc.read_h5ad('transcriptome.h5ad').obsm['spatial']); b_prime = Data(X=sc.read_h5ad('metabolome.h5ad').X.toarray(), D=sc.read_h5ad('metabolome.h5ad').obsm['spatial']); _b_prime = hacca.manual_gross_alignment(a, b_prime); _a, _b_prime = hacca.icp_3d_alignment(a, _b_prime); b_predict = hacca.direct_alignment(_a, _b_prime)
```

## Evaluation signals

- Coordinate correspondence: aligned spot pairs from transcriptome and metabolome modalities should exhibit Euclidean distance <1–2 μm (or typical spot radius), indicating geometric registration success.
- Feature overlap validation: spots aligned in space should show elevated correlation of co-localized gene–metabolite pairs compared to pre-alignment random pairing (Pearson r or Spearman ρ uplift).
- Spot count consistency: number of aligned spot pairs should be ≥85% of the smaller modality's spot count, indicating minimal loss during registration.
- Morphological preservation: tissue boundaries and anatomical landmarks (e.g., glandular structures) visible in both modalities should remain spatially congruent post-alignment.
- Transformation stability: iterative alignment runs on the same input pair should yield identical or near-identical coordinate mappings (transformation reproducibility).

## Limitations

- Requires sufficient high-correlated feature pairs between modalities; datasets with weak global transcriptome–metabolome association may yield misaligned spots.
- Assumes both modalities share substantial spatial overlap; non-overlapping or partially overlapping tissue sections may require manual gross pre-alignment.
- Performance depends on input spot density and coordinate precision; sparse sampling or low-resolution imaging reduces alignment robustness.
- No changelog or version history provided; users should verify compatibility with their h5ad schema and library versions.

## Evidence

- [other] haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes.: "haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes."
- [other] Apply the modified spatial morphological alignment algorithm to register spots between modalities.: "Apply the modified spatial morphological alignment algorithm to register spots between modalities."
- [other] Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics.: "Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics."
- [intro] ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes: "ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes"
- [readme] manual_gross_alignment | icp_3d_alignment | direct_alignment; b_predict contains aligned feature from a and samples from b_prime: "manual_gross_alignment | icp_3d_alignment | direct_alignment; b_predict contains aligned feature from a and samples from b_prime"
- [readme] Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information: "Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information"
