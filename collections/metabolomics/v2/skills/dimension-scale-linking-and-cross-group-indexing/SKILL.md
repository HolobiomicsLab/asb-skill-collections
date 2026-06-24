---
name: dimension-scale-linking-and-cross-group-indexing
description: Use when when exporting quantified MSI data as HDF5 containers following
  the Cardinal::HDF5 layout convention, and you need to establish bidirectional indexing
  between intensity data (feature-by-pixel matrix) and metadata groups (featureData,
  pixelData).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - LipidQMap
  - Cardinal
  - h5py
  techniques:
  - direct-infusion-MS
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org)
  conventions.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidqmap_cq
    doi: 10.1101/2025.10.15.682422v1
    title: LipidQMap
  dedup_kept_from: coll_lipidqmap_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.10.15.682422v1
  all_source_dois:
  - 10.1101/2025.10.15.682422v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dimension-scale-linking-and-cross-group-indexing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Link HDF5 dataset dimensions to shared index scales across groups to enable standardized cross-group coordinate reference and axis semantics in Cardinal::HDF5 containers. This ensures that feature and pixel axes in intensity matrices are properly annotated and traversable via dimension scales.

## When to use

When exporting quantified MSI data as HDF5 containers following the Cardinal::HDF5 layout convention, and you need to establish bidirectional indexing between intensity data (feature-by-pixel matrix) and metadata groups (featureData, pixelData). Specifically, when your intensity dataset has two dimensions that must be semantically linked to external index columns—axis 0 to featureData/feature_id and axis 1 to pixelData/pixel_index—so that downstream tools can navigate from a spectrum to its metadata without hardcoding positional assumptions.

## When NOT to use

- Input datasets are already dimension-scaled in a different convention (e.g., already linked to different indices or using custom axis semantics)
- HDF5 file structure does not follow the Cardinal::HDF5 group hierarchy (missing or differently named featureData/pixelData groups)
- Intensity data is sparse or stored in a non-dense rectangular format where 1-based pixel indexing or full Cartesian coordinates are not applicable

## Inputs

- intensity dataset (float32, shape n_features × n_pixels) in spectraData group
- featureData group containing feature metadata datasets (feature_id, feature_index, mz, etc.)
- pixelData group containing pixel metadata datasets (pixel_index, x, y, sample_id, etc.)

## Outputs

- intensity dataset with attached dimension scales (HDF5 DIMENSION_LIST metadata)
- spectraData group with layout attribute set to 'feature_by_pixel'
- validated cross-group index linkages (feature_id on axis 0, pixel_index on axis 1)

## How to apply

After creating the intensity dataset (shape n_features × n_pixels, float32) in the spectraData group, attach dimension scales by: (1) creating or retrieving the index dataset in the target metadata group (e.g., featureData/feature_id as UTF-8 strings, or pixelData/pixel_index as int64); (2) converting the index dataset to a dimension scale with `h5py.Dataset.make_scale(name=...)` if not already marked; (3) calling `h5py.Dataset.dims[axis_number].attach_scale(scale_dataset)` on the intensity dataset for each axis, where axis 0 links to featureData/feature_id and axis 1 links to pixelData/pixel_index; (4) adding a layout attribute to intensity specifying 'feature_by_pixel' to document the axis semantics; (5) verifying that dimension scales are properly linked by checking that the HDF5 file's internal DIMENSION_LIST attributes are populated and that tools like h5py can traverse scales without error. The dimension scales must be sorted consistently (e.g., featureData ascending by m/z) and use 1-based indexing conventions where appropriate to align with the Cardinal::HDF5 standard.

## Related tools

- **LipidQMap** (MSI quantitation and HDF5 export engine; orchestrates dimension-scale linking as part of Cardinal::HDF5 container serialization) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Reference standard and downstream consumer of dimension-scaled HDF5 MSI containers; enforces Cardinal::HDF5 layout conventions) — https://cardinalmsi.org
- **h5py** (HDF5 library API for attaching and verifying dimension scales in Python)

## Evaluation signals

- Verify intensity dataset's DIMENSION_LIST attribute is populated with references to featureData/feature_id (axis 0) and pixelData/pixel_index (axis 1) using h5py inspector or h5dump
- Confirm that both featureData/feature_id and pixelData/pixel_index datasets are marked as dimension scales (have CLASS='DIMENSION_SCALE' attribute)
- Check that intensity dataset has a layout attribute with value 'feature_by_pixel'
- Validate that all featureData and pixelData indices align row-wise with intensity axes (n_features and n_pixels match respectively) and are sorted consistently
- Test that a consuming tool (e.g., Cardinal) can traverse the dimension scales and resolve feature/pixel metadata without errors

## Limitations

- Dimension scales require that index datasets be created and marked as scales before attachment; if featureData or pixelData groups are missing or incomplete, dimension scale attachment will fail
- 1-based indexing convention must be applied consistently across all pixel coordinates (x, y, pixel_index) and feature indices; mixing 0-based and 1-based indices will break cross-group navigation
- HDF5 dimension scales are a read-only metadata layer; they do not enforce referential integrity or prevent orphaned indices if metadata is later deleted or modified outside the dimension-scale framework
- The Cardinal::HDF5 convention assumes rectangular dense pixel grids; sparse imaging data or irregularly sampled pixels may not map cleanly to standard dimension scales without additional coordinate metadata (min_x, max_x, etc.)

## Evidence

- [methods] attach dimension scales linking axis 0 to featureData/feature_id and axis 1 to pixelData/pixel_index: "attach dimension scales linking axis 0 to featureData/feature_id and axis 1 to pixelData/pixel_index, and add group attributes n_features and n_spectra"
- [methods] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data."
- [methods] write the intensity dataset with feature_by_pixel layout attribute: "write the intensity dataset with feature_by_pixel layout attribute, attach dimension scales linking axis 0 to featureData/feature_id"
- [methods] Validate the output file: verify all required datasets and groups exist, check dataset shapes and dtypes, confirm dimension scales are properly linked: "Validate the output file: verify all required datasets and groups exist, check dataset shapes and dtypes, confirm dimension scales are properly linked, and verify 1-based indexing is used throughout."
