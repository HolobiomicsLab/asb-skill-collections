---
name: coordinate-system-normalization-1based-indexing
description: Use when when exporting quantified ion images and pixel metadata from LipidQMap to HDF5 format for use in downstream Cardinal or other MSI analysis workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - LipidQMap
  - Cardinal
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions.
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
---

# Coordinate-system normalization to 1-based indexing

## Summary

Convert spatial coordinates and pixel indices from 0-based to 1-based indexing when exporting MSI data to HDF5 containers that follow the Cardinal::HDF5 convention. This ensures standardized interchange and correct spatial interpretation across MSI analysis platforms.

## When to use

When exporting quantified ion images and pixel metadata from LipidQMap to HDF5 format for use in downstream Cardinal or other MSI analysis workflows. Specifically, apply this skill when populating pixelData and samples subgroups in the HDF5 structure to ensure spatial coordinates are consistently 1-based throughout the file.

## When NOT to use

- Input spatial data is already in 1-based coordinates — applying a second conversion would produce incorrect indices.
- Exporting to non-HDF5 formats or to formats that require 0-based indexing (e.g., NumPy arrays, NetCDF without Cardinal convention) — coordinate remapping should match the target format's convention.
- Internal LipidQMap processing or visualization that uses 0-based indexing — apply normalization only at the export boundary, not to intermediate computations.

## Inputs

- Quantified ion image intensities as a feature-by-pixel matrix (float32, n_features × n_pixels)
- Pixel spatial coordinates and metadata (x, y positions, sample assignment, run labels)
- Per-feature metadata (feature_id, lipid_class, adduct, neutral_id, m/z, is_standard flag)
- Sample-level attributes (sample_id, pixel dimensions in pixels, pixel size in micrometers if known)

## Outputs

- HDF5 file with pixelData group containing 1-based pixel_index, x, y, and coord datasets
- HDF5 featureData group with 1-based feature_index and sorted feature metadata
- HDF5 samples subgroup structure with 1-based sample index strings and spatial metadata
- Validated Cardinal::HDF5 compliant export with internally consistent 1-based indexing throughout

## How to apply

During HDF5 export, convert all pixel spatial indices and coordinates from the internal 0-based representation to 1-based before writing to disk. For the pixelData group, write x and y coordinates as int32 arrays using 1-based indexing (i.e., increment all x and y values by 1 before writing). Similarly, for the samples subgroup, include height_px, width_px, and n_pixels metadata using 1-based bounds. In the featureData and pixelData groups, write feature_index and pixel_index as int64 sequences starting from 1, not 0. Create a coord dataset as an n_pixels × 2 int32 matrix of [x, y] pairs in 1-based coordinates. Validate the conversion by confirming all spatial indices and pixel_index values in the final HDF5 file begin at 1 and increment sequentially without gaps.

## Related tools

- **LipidQMap** (MSI quantitation and export tool that performs the coordinate normalization and writes the HDF5 container) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (MSI analysis framework that defines and reads the Cardinal::HDF5 convention; sets the 1-based indexing standard) — https://cardinalmsi.org

## Evaluation signals

- All pixel_index values in pixelData group begin at 1 and increment sequentially to n_pixels with no gaps or 0 values.
- All x and y coordinate values in pixelData are ≥1 and do not exceed the declared sample dimensions (height_px, width_px).
- The coord dataset (n_pixels × 2 matrix) contains only [x, y] pairs in the range [1, max_x] × [1, max_y].
- Feature indices in featureData start at 1 and match the axis 0 dimension scale linking to spectraData intensity matrix.
- Sample indices in the samples subgroup are 1-based string keys ('1', '2', ..., not '0', '1', ...) and match the spatial bounds declared in each sample's metadata.

## Limitations

- Dense rectangular MSI exports omit min_*/max_* spatial bounds attributes; 1-based conversion assumes all pixels within the declared height_px and width_px are present. Sparse exports include min_*/max_* bounds and require careful validation that 1-based coordinates respect those bounds.
- If upstream data already uses mixed 0-based and 1-based conventions, conversion at export time may not catch prior coordinate errors; validation should include cross-check against original imzML pixel positions.
- No mechanism in the HDF5 schema itself enforces 1-based indexing; compliance depends on the exporting tool (LipidQMap) and validation by downstream readers (e.g., Cardinal). Manual inspection of a subset of coordinates is recommended for new export configurations.

## Evidence

- [other] Populate the pixelData group with column datasets (pixel_index as int64, x and y as int32 using 1-based coordinates: "Populate the pixelData group with column datasets (pixel_index as int64, x and y as int32 using 1-based coordinates, sample_index, run, sample_id as UTF-8 strings)"
- [other] Create a coord dataset (n_pixels × 2 int32 matrix of [x, y] pairs) and add group attribute columns listing dataset names.: "create a coord dataset (n_pixels × 2 int32 matrix of [x, y] pairs) and add group attribute columns listing dataset names"
- [other] Validation requires that 1-based indexing is used throughout the HDF5 file.: "verify 1-based indexing is used throughout"
- [readme] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data."
