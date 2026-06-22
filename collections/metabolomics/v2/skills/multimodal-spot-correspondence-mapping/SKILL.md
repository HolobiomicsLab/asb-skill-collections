---
name: multimodal-spot-correspondence-mapping
description: Use when when you have paired spatial transcriptome and metabolome datasets in h5ad format with spatial coordinate matrices (obsm['spatial']) and you need to establish spot-level correspondence across modalities for downstream integration or co-analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
  tools:
  - haCCA
  - scanpy
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

# multimodal-spot-correspondence-mapping

## Summary

Align spatial transcriptome and metabolome spots via high-correlated feature pair identification combined with modified spatial morphological alignment to achieve accurate spot-to-spot correspondence mapping between modalities. This enables integrated analysis of multi-omics spatial data with preserved coordinate fidelity.

## When to use

When you have paired spatial transcriptome and metabolome datasets in h5ad format with spatial coordinate matrices (obsm['spatial']) and you need to establish spot-level correspondence across modalities for downstream integration or co-analysis. Specifically, when spots are not inherently aligned and you require both feature correlation and spatial geometry to resolve cross-modality spot identity.

## When NOT to use

- Input data is already perfectly aligned or from the same experiment with matching spot indices — skip to direct feature integration
- Only one spatial modality is available — this skill requires paired transcriptome and metabolome data
- Spatial coordinates are missing or not stored in obsm['spatial'] format — preprocessing to extract and normalize coordinates is required first

## Inputs

- spatial transcriptome h5ad file (containing X feature matrix and obsm['spatial'] coordinates)
- spatial metabolome h5ad file (containing X feature matrix and obsm['spatial'] coordinates)
- optional cluster label arrays for each modality

## Outputs

- aligned spot coordinate mappings (coordinate correspondence matrix)
- integrated feature matrix combining aligned transcriptome and metabolome features
- spot overlap and alignment accuracy metrics

## How to apply

Load spatial transcriptome and metabolome data as Data objects containing feature matrices (X), spatial coordinate matrices (D), and optional cluster labels. Identify high-correlated feature pairs between modalities to establish initial correspondence hints. Apply the modified spatial morphological alignment algorithm sequentially: first manual_gross_alignment to coarse-register the spatial coordinate systems, then icp_3d_alignment to refine 3D rigid alignment, and finally direct_alignment to compute the predicted aligned features and validated spot mappings. Validate alignment by verifying coordinate correspondence metrics and spot overlap ratios. Output the aligned spot coordinate mappings and integrated feature matrix.

## Related tools

- **haCCA** (primary workflow for spot-to-spot integration via high-correlated feature pairs and modified spatial morphological alignment) — https://github.com/LittleLittleCloud/haCCA
- **scanpy** (h5ad file I/O and anndata object manipulation for loading spatial transcriptome and metabolome data)

## Examples

```
from hacca import *; import scanpy as sc; a = Data(X=sc.read_h5ad('transcriptome.h5ad').X.toarray(), D=sc.read_h5ad('transcriptome.h5ad').obsm['spatial']); b_prime = Data(X=sc.read_h5ad('metabolome.h5ad').X.toarray(), D=sc.read_h5ad('metabolome.h5ad').obsm['spatial']); _b_prime = hacca.manual_gross_alignment(a, b_prime); _a, _b_prime = hacca.icp_3d_alignment(a, _b_prime); b_predict = hacca.direct_alignment(_a, _b_prime)
```

## Evaluation signals

- Coordinate correspondence validation: spot coordinates from one modality map to expected positions in the other modality within a defined tolerance (e.g., pixel distance < threshold)
- Spot overlap metrics: percentage of spots with successful 1:1 correspondence across modalities should be > 95% for high-quality alignment
- Feature correlation preservation: high-correlated feature pairs identified pre-alignment maintain or improve correlation post-alignment
- Spatial consistency: aligned spots maintain local neighborhood topology (k-NN graph similarity pre- and post-alignment)
- Schema validation: output integrated feature matrix dimensions match (total spots × combined features) and spot labels are consistent across modalities

## Limitations

- Alignment accuracy depends on sufficient overlap between spatial regions of transcriptome and metabolome data; non-overlapping tissues cannot be aligned
- Modified spatial morphological alignment assumes rigid or near-rigid transformations; highly non-linear spatial deformations between modalities may not resolve correctly
- Manual_gross_alignment step requires user-guided initialization and may be sensitive to initial coordinate system orientation
- No changelog or versioning information provided; reproducibility across tool versions may be affected

## Evidence

- [readme] haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration: "haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration"
- [other] haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes.: "haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes"
- [other] Apply the modified spatial morphological alignment algorithm to register spots between modalities. Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics.: "Apply the modified spatial morphological alignment algorithm to register spots between modalities. Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics"
- [readme] manual_gross_alignment | icp_3d_alignment | direct_alignment. b_predict contains aligned feature from a and samples from b_prime: "manual_gross_alignment | icp_3d_alignment | direct_alignment. b_predict contains aligned feature from a and samples from b_prime"
