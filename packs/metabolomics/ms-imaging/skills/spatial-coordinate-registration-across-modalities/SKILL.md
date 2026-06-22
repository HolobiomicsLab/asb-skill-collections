---
name: spatial-coordinate-registration-across-modalities
description: Use when when you have preprocessed spatial transcriptomics (ST) and spatial metabolomics (SM) datasets in AnnData format with spatial coordinates, and need to align them to a common resolution before joint downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3352
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - spatialMETA
  - scikit-learn (NearestNeighbors)
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

# spatial-coordinate-registration-across-modalities

## Summary

Register spatial spots from distinct omics modalities (spatial transcriptomics and spatial metabolomics) to a unified coordinate resolution using k-nearest neighbors matching. This skill enables multi-modal spatial data integration by establishing spot-level correspondence between modalities with different native resolutions.

## When to use

When you have preprocessed spatial transcriptomics (ST) and spatial metabolomics (SM) datasets in AnnData format with spatial coordinates, and need to align them to a common resolution before joint downstream analysis. Use this skill specifically when ST and SM have different spot densities or sampling grids and you require one-to-one or many-to-one spot correspondence for cross-modal pattern identification.

## When NOT to use

- Input modalities are already aligned to the same coordinate space
- SM or ST data lack valid spatial coordinates or have extreme coordinate outliers
- You require probabilistic or soft assignment rather than hard nearest-neighbor matching

## Inputs

- Preprocessed ST AnnData object with spatial coordinates and filtered features
- Preprocessed SM AnnData object with spatial coordinates and filtered features

## Outputs

- Aligned coordinate mappings (SM-to-ST index pairs)
- Joint AnnData object with spot correspondence stored in metadata
- Distance distributions for validation

## How to apply

Build a k-nearest neighbors (KNN) index on the ST spot coordinates using scikit-learn's NearestNeighbors, then query it with SM spot coordinates to find the k nearest ST neighbors for each SM spot. Assign each SM spot to its nearest ST neighbor based on minimum Euclidean distance, creating SM-to-ST index pair mappings. Store the resulting spot correspondence in the joint AnnData object metadata. Validate that all SM spots have been assigned and inspect the distance distribution to confirm alignment quality is reasonable; spots with anomalously large distances may indicate preprocessing errors or spatial misalignment between modalities.

## Related tools

- **spatialMETA** (Implements the spot_align_byknn workflow step for KNN-based spatial spot alignment in multi-omics integration) — https://github.com/WanluLiuLab/SpatialMETA
- **scikit-learn (NearestNeighbors)** (Constructs KNN index on ST coordinates and performs efficient neighbor queries)

## Examples

```
from spatialmeta.pp import spot_align_byknn; spot_align_byknn(st_adata, sm_adata, k=1)
```

## Evaluation signals

- All SM spots are assigned to an ST spot (no unmatched spots)
- Euclidean distance distribution between matched SM and ST spot pairs is unimodal with reasonable median (e.g., < 1–2 spot units)
- SM-to-ST index pairs are stored in joint AnnData object metadata without gaps or duplicates
- Visual inspection: overlay of matched spots on tissue image shows spatial coherence across modalities
- Downstream joint analysis (e.g., cross-modal correlation) exhibits expected signal enrichment compared to unaligned data

## Limitations

- KNN matching is deterministic and does not account for biological uncertainty; spots with similar distances may be arbitrarily assigned
- Method assumes Euclidean distance is the appropriate metric; anisotropic tissue distortion or rotation between modalities is not corrected
- Quality depends critically on upstream preprocessing (feature filtering, coordinate validity); poor-quality input data will not be corrected by alignment alone
- Many-to-one mapping from SM to ST may lose fine spatial resolution if SM spots are denser than ST spots

## Evidence

- [other] Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors. Query the KNN index with SM spot coordinates to find k nearest ST neighbors for each SM spot. Assign each SM spot to its nearest ST spot based on minimum Euclidean distance.: "Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors. 3. Query the KNN index with SM spot coordinates to find k nearest ST neighbors for each SM spot. 4. Assign each SM spot"
- [other] The spot_align_byknn workflow step is the mechanism that performs spatial spot alignment between spatial transcriptomics (ST) and spatial metabolomics (SM) modalities to achieve unified resolution integration in spatialMETA.: "The spot_align_byknn workflow step is the mechanism that performs spatial spot alignment between spatial transcriptomics (ST) and spatial metabolomics (SM) modalities to achieve unified resolution"
- [readme] SMOI aligns ST and SM to a unified resolution, integrates single or multiple sample data to identify cross-modal spatial patterns: "SMOI aligns ST and SM to a unified resolution, integrates single or multiple sample data to identify cross-modal spatial patterns"
- [other] Validate that all SM spots have been assigned and distance distributions are reasonable.: "Validate that all SM spots have been assigned and distance distributions are reasonable."
