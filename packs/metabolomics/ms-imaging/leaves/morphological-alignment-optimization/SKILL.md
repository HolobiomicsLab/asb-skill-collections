---
name: morphological-alignment-optimization
description: Use when you have two or more spatial omics datasets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3673
  tools:
  - haCCA
  - scanpy
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.08.20.608773v2
  title: haCCA
evidence_spans:
- haCCA, a workflow utilizing high Correlated feature pairs combined with a modified
  spatial morphological alignment
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# morphological-alignment-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A spatial registration technique that aligns spot coordinates between spatial transcriptome and metabolome datasets using modified morphological operators to achieve accurate spot-to-spot integration. This skill ensures high-resolution multimodal spatial data fusion by registering coordinate systems before feature integration.

## When to use

Apply this skill when you have two or more spatial omics datasets (e.g., spatial transcriptome and metabolome) with overlapping or partially overlapping tissue regions, represented as spot coordinate matrices (D: spatial coordinates) paired with feature matrices (X), and you need to register spots between modalities before joint analysis of correlated features.

## When NOT to use

- Input datasets lack spatial coordinate information or are not in h5ad format with .obsm['spatial'] attribute
- Spatial regions of the two modalities do not substantially overlap or are from different tissue sections
- Spots are already registered or alignment has been performed in an upstream analysis

## Inputs

- h5ad file containing spatial transcriptome data with .obsm['spatial'] coordinate matrix
- h5ad file containing spatial metabolome data with .obsm['spatial'] coordinate matrix
- Feature matrix X (rows=spots, columns=features) from each modality
- Spatial coordinate matrix D (rows=spots, columns=x,y[,z] coordinates) from each modality

## Outputs

- Aligned spot coordinate mapping (transformation matrix or remapped D matrices)
- Integrated feature matrix combining aligned spots from both modalities
- Spot correspondence indices linking transcriptome spots to metabolome spots

## How to apply

Load spatial transcriptome and metabolome datasets as h5ad files and construct Data objects containing feature matrix X, spatial coordinate matrix D, and optional cluster labels. Apply a sequence of alignment methods in order of increasing precision: (1) manual_gross_alignment for coarse spatial overlap correction, (2) icp_3d_alignment for iterative closest-point registration of spot coordinates, and (3) direct_alignment for fine spot-to-spot correspondence. Validate alignment accuracy by comparing coordinate overlap metrics and verifying that spot pairs exhibit high spatial proximity after transformation. The modified spatial morphological alignment operates by iteratively refining the transformation matrix until spot coordinates from both modalities align within acceptable tolerance.

## Related tools

- **haCCA** (Workflow engine implementing modified spatial morphological alignment combined with high correlated feature pair identification for spot-to-spot integration) — https://github.com/LittleLittleCloud/haCCA
- **scanpy** (Data container and I/O for h5ad spatial datasets)

## Examples

```
from hacca import *; a = Data(X=a_h5ad.X.toarray(), D=a_h5ad.obsm['spatial']); b_prime = Data(X=b_prime_h5ad.X.toarray(), D=b_prime_h5ad.obsm['spatial']); _b_prime = hacca.manual_gross_alignment(a, b_prime); _a, _b_prime = hacca.icp_3d_alignment(a, _b_prime); b_predict = hacca.direct_alignment(_a, _b_prime)
```

## Evaluation signals

- Coordinate correspondence after alignment: verify that homologous spots from transcriptome and metabolome modalities have spatial distance below a defined threshold (e.g., <1 spot diameter)
- Spot overlap metrics: compute the Intersection-over-Union (IoU) or Hausdorff distance between aligned coordinate sets; expect IoU >0.8 or normalized Hausdorff distance <0.1 for successful registration
- Feature correlation validation: measure correlation of high-confidence feature pairs before and after alignment; expect significant increase in correlation after alignment for truly co-localized features
- Transformation matrix invertibility: verify that the derived transformation matrix from icp_3d_alignment is numerically stable and that applying the inverse transformation recovers original coordinates with negligible error (<0.01 in normalized space)

## Limitations

- Alignment accuracy depends on substantial spatial overlap between modalities; non-overlapping or minimally overlapping tissue regions may result in poor registration
- ICP-based methods can converge to local minima; manual_gross_alignment step must provide a sufficiently accurate initialization
- Algorithm assumes spot coordinates are registered to the same reference frame (e.g., same tissue slide or section); cross-slide registration is not addressed
- Performance and convergence may degrade with very high-dimensional feature spaces or sparse feature matrices; feature selection or dimensionality reduction may be required

## Evidence

- [other] haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration: "haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes."
- [intro] The workflow ensures high resolution and accuracy of spot-to-spot data integration: "ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes"
- [readme] Data object structure for spatial datasets contains feature matrix X, spatial matrix D with location information, and optional cluster labels: "Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information"
- [readme] Sequential alignment pipeline: manual_gross_alignment, icp_3d_alignment, direct_alignment: "manual_gross_alignment | icp_3d_alignment | direct_alignment"
- [other] Workflow validates alignment accuracy by verifying coordinate correspondence and spot overlap metrics: "Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics."
