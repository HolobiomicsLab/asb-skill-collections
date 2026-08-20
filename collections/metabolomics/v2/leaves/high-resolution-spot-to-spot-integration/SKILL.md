---
name: high-resolution-spot-to-spot-integration
description: 'Use when you have two spatial omics datasets (e.g., spatial transcriptome
  and metabolome spot matrices) collected from the same or adjacent tissue sections,
  with both feature matrices (X: np.ndarray) and spatial coordinates (D: np.ndarray
  containing location information in .'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3056
  tools:
  - haCCA
  - hacca Python package
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

# high-resolution-spot-to-spot-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill applies haCCA's modified spatial morphological alignment combined with high-correlated feature pair identification to integrate spatial transcriptome and metabolome spot coordinate systems with high accuracy. Use it when you have paired spatial omics datasets (transcriptomics and metabolomics) acquired on the same tissue section and need to align spots between modalities for multi-omics analysis.

## When to use

You have two spatial omics datasets (e.g., spatial transcriptome and metabolome spot matrices) collected from the same or adjacent tissue sections, with both feature matrices (X: np.ndarray) and spatial coordinates (D: np.ndarray containing location information in .h5ad obsm['spatial'] format), and you need spot-to-spot correspondence to perform integrated downstream analysis across modalities.

## When NOT to use

- Datasets are from different tissue sections or regions without spatial overlap — alignment will fail to find meaningful correspondences
- One or both datasets lack spatial coordinate information or are already pre-aligned — the alignment step would be redundant
- Feature matrices contain very sparse or low-quality data with insufficient correlated feature pairs for anchor identification

## Inputs

- spatial transcriptome .h5ad file (X: feature matrix, obsm['spatial']: coordinate matrix)
- spatial metabolome .h5ad file (X: feature matrix, obsm['spatial']: coordinate matrix)
- Data object triplets: (feature_matrix: np.ndarray, spatial_coordinates: np.ndarray, optional_labels: np.ndarray)

## Outputs

- aligned spatial coordinate mappings between modalities
- integrated feature matrix with spot-to-spot correspondence
- alignment validation metrics (coordinate correspondence, spot overlap)

## How to apply

Load both datasets as Data objects (triplets of feature matrix X, spatial coordinate matrix D, and optional cluster labels). First, identify high-correlated feature pairs between the two modalities to establish cross-modal anchors. Second, apply the modified spatial morphological alignment algorithm in a three-stage pipeline: (1) manual_gross_alignment for coarse registration, (2) icp_3d_alignment for refined spatial registration, and (3) direct_alignment for final spot-to-spot mapping. Validate alignment accuracy by verifying coordinate correspondence and measuring spot overlap metrics between registered spots. The rationale is that high-correlation features provide biological signal for anchor selection, while progressive refinement from gross to fine alignment ensures robust convergence even with initial spatial misalignment.

## Related tools

- **haCCA** (primary workflow implementation for correlated feature pair identification and modified spatial morphological alignment) — github.com/LittleLittleCloud/haCCA
- **hacca Python package** (pip-installable implementation providing manual_gross_alignment, icp_3d_alignment, and direct_alignment methods) — https://badge.fury.io/py/hacca

## Examples

```
from hacca import *; import scanpy as sc; a = Data(X=sc.read_h5ad('transcriptome.h5ad').X.toarray(), D=sc.read_h5ad('transcriptome.h5ad').obsm['spatial']); b_prime = Data(X=sc.read_h5ad('metabolome.h5ad').X.toarray(), D=sc.read_h5ad('metabolome.h5ad').obsm['spatial']); _b_prime = hacca.manual_gross_alignment(a, b_prime); _a, _b_prime = hacca.icp_3d_alignment(a, _b_prime); b_predict = hacca.direct_alignment(_a, _b_prime)
```

## Evaluation signals

- Coordinate correspondence between aligned spots meets spatial distance threshold (e.g., <1 spot diameter)
- Spot overlap metrics show high consistency across modality pairs (>0.8 overlap coefficient)
- High-correlated feature pairs (identified in first step) show consistent spatial localization post-alignment
- Integrated feature matrix dimensions match expected cardinality (rows = aligned spots, columns = combined features from both modalities)
- Visual inspection of aligned spot coordinates shows minimal systematic translation, rotation, or scaling artifacts

## Limitations

- Requires both datasets to originate from the same or immediately adjacent tissue sections with biological overlap
- Alignment accuracy depends critically on the availability of high-correlated feature pairs; datasets with low cross-modal correlation will produce poor alignments
- Three-stage alignment pipeline may require manual parameter tuning for datasets with unusual spatial scaling or orientation differences
- No changelog provided in repository documentation, limiting reproducibility across versions

## Evidence

- [other] haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration: "haCCA integrates high correlated feature pairs with a modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes"
- [intro] ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes: "ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes"
- [readme] Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information: "Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information"
- [readme] Infer b_predict from (a, b_prime) using the following alignment methods: manual_gross_alignment | icp_3d_alignment | direct_alignment: "Infer b_predict from (a, b_prime) using the following alignment methods: manual_gross_alignment | icp_3d_alignment | direct_alignment"
- [other] Apply the modified spatial morphological alignment algorithm to register spots between modalities. Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics: "Apply the modified spatial morphological alignment algorithm to register spots between modalities. Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics"
