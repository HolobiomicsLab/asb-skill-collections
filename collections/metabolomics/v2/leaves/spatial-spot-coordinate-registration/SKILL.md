---
name: spatial-spot-coordinate-registration
description: Use when when you have paired spatial transcriptome and metabolome datasets
  with spot-based coordinates that need to be aligned for multi-modal integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3518
  tools:
  - haCCA
  techniques:
  - MS-imaging
  license_tier: restricted
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

# spatial-spot-coordinate-registration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Register and align spot coordinates between spatial transcriptome and metabolome datasets using modified spatial morphological alignment to enable spot-to-spot data integration. This skill achieves high-resolution correspondence between two modalities' spatial coordinate systems for joint analysis.

## When to use

When you have paired spatial transcriptome and metabolome datasets with spot-based coordinates that need to be aligned for multi-modal integration. Use this skill if your goal is to establish one-to-one spot correspondence between two modalities and you have already identified high-correlated feature pairs across them.

## When NOT to use

- Input datasets are not spot-based or do not have explicit 2D/3D spatial coordinates
- High-correlated feature pairs have not yet been identified between modalities
- Spatial coordinates are already pre-aligned or from a single modality only

## Inputs

- spatial transcriptome h5ad file with obsm['spatial'] coordinate matrix
- spatial metabolome h5ad file with obsm['spatial'] coordinate matrix
- feature matrix X (np.ndarray) for both modalities
- spatial coordinate matrix D (np.ndarray) for both modalities
- optional cluster label arrays for validation

## Outputs

- aligned spot coordinate mappings between modalities
- integrated feature matrix combining aligned features from both datasets
- registration validation metrics (coordinate correspondence, spot overlap)

## How to apply

Load both spatial datasets as Data objects containing feature matrices (X as np.ndarray), spatial coordinate matrices (D from obsm['spatial']), and optional cluster labels. Apply a sequence of three alignment methods in order: (1) manual_gross_alignment to establish initial coarse correspondence, (2) icp_3d_alignment to refine spatial registration using iterative closest point, and (3) direct_alignment to produce the final aligned feature predictions. Validate alignment accuracy by checking coordinate correspondence and computing spot overlap metrics between registered spot positions.

## Related tools

- **haCCA** (Primary workflow tool implementing manual_gross_alignment, icp_3d_alignment, and direct_alignment methods for spatial spot coordinate registration) — https://github.com/LittleLittleCloud/haCCA

## Examples

```
from hacca import *; a = Data(X=a_h5ad.X.toarray(), D=a_h5ad.obsm['spatial']); b_prime = Data(X=b_prime_h5ad.X.toarray(), D=b_prime_h5ad.obsm['spatial']); _b_prime = hacca.manual_gross_alignment(a, b_prime); _a, _b_prime = hacca.icp_3d_alignment(a, _b_prime); b_predict = hacca.direct_alignment(_a, _b_prime)
```

## Evaluation signals

- Coordinate correspondence validated: aligned spot positions in modality A should map to nearest neighbors in modality B within expected tolerance
- Spot overlap metrics computed: quantify fractional overlap and distance statistics between registered spot coordinate sets
- Feature consistency check: high-correlated feature pairs used for alignment should maintain or improve correlation in aligned output
- Spatial structure preservation: relative neighborhood relationships in original coordinates should be maintained after alignment
- Output schema validation: aligned coordinate matrices and integrated feature matrix should have matching row counts and valid spatial ranges

## Limitations

- Requires accurate initial coarse alignment (manual_gross_alignment step); poor initial alignment may cause ICP convergence to local minima
- Performance depends on quantity and quality of high-correlated feature pairs; sparse or noisy correlations may degrade registration accuracy
- Method assumes spots in both modalities correspond to the same tissue regions; global coordinate system mismatch may not be fully resolvable
- No changelog provided in repository; algorithm details and validation metrics not fully specified in available documentation

## Evidence

- [readme] haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment: "haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration"
- [other] Modified spatial morphological alignment component operate to align spatial transcriptome and metabolome spots: "Modified spatial morphological alignment to achieve spot-to-spot data integration of spatial transcriptomes and metabolomes"
- [readme] Alignment methods applied in sequence: "manual_gross_alignment | icp_3d_alignment | direct_alignment"
- [readme] Data object structure requirements: "Data is a triplet of (X: np.ndarray, D: np.ndarray, Label: Optional[np.ndarray]), where X is the feature matrix, D is the spatial matrix that contains the location information"
- [other] Validation procedure for alignment accuracy: "Validate alignment accuracy by verifying coordinate correspondence and spot overlap metrics"
