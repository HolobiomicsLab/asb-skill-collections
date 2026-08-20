---
name: hdf5-cardinal-format-preservation
description: Use when after performing isotopic correction, quantitation, or other pixel-level transformations on a feature-by-pixel intensity matrix imported from an imzML file via Cardinal's HDF5 layout.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - LipidQMap
  - Cardinal
  techniques:
  - MS-imaging
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

# HDF5 Cardinal Format Preservation

## Summary

Preserve the HDF5 structure, dimension scales, layout metadata, and data groups when writing corrected Mass Spectrometry Imaging intensity matrices back to disk. This ensures downstream Cardinal tools and analysis pipelines can read and process the modified data without re-importing or reformatting.

## When to use

After performing isotopic correction, quantitation, or other pixel-level transformations on a feature-by-pixel intensity matrix imported from an imzML file via Cardinal's HDF5 layout. Use this skill when you need to write corrected intensities back to the same HDF5 container while maintaining compatibility with Cardinal-aware visualization and analysis tools.

## When NOT to use

- Input is not in Cardinal::HDF5 format (e.g., raw imzML, netCDF, or proprietary vendor formats) — re-import or convert first.
- You need to change the feature-by-pixel layout (e.g., transpose to pixel-by-feature) — use a separate conversion/reshape operation.
- Metadata (feature IDs, m/z, pixel coordinates) has been modified or needs to be updated — update those groups explicitly before or after intensity write.

## Inputs

- HDF5 file following Cardinal::HDF5 conventions (spectraData/intensity dataset as float32, shape n_features × n_pixels)
- Feature metadata (feature identifiers, m/z values, lipid class, adduct type)
- Pixel metadata (coordinates, sample annotations)
- Corrected intensity matrix (float32, same shape as input)

## Outputs

- HDF5 file with corrected intensities written to spectraData/intensity dataset
- Preserved dimension scales, layout metadata (feature_by_pixel), pixelData and featureData groups
- Cardinal-compatible MSI export file

## How to apply

Load the feature-by-pixel intensity matrix and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout convention. After correcting intensities (e.g., subtracting [M+Na]+ contribution from [M+H]+ features), write the corrected intensity matrix back to the spectraData/intensity dataset in the same HDF5 container. Preserve all dimension scales, the feature_by_pixel layout metadata annotation, and leave all pixelData and featureData groups unchanged. This maintains the tidy data structure expected by Cardinal and allows toggling between raw, isotope-corrected, and quantified views without re-import.

## Related tools

- **Cardinal** (Defines the HDF5 layout conventions (Cardinal::HDF5) that structure the intensity matrix, dimension scales, and metadata groups preserved by this skill) — https://cardinalmsi.org
- **LipidQMap** (Writes MSI exports as HDF5 containers following Cardinal::HDF5 conventions; uses this preservation approach when saving isotope-corrected and quantified images) — https://github.com/swinnenteam/LipidQMap

## Evaluation signals

- HDF5 file can be opened with Cardinal or h5py and spectraData/intensity dataset is readable with correct shape (n_features × n_pixels, float32).
- Dimension scales and axis labels are preserved and match the original input.
- Layout metadata 'feature_by_pixel' annotation is present and unchanged.
- All pixelData and featureData groups remain in the file with original content.
- Corrected intensity values are within [0, max] range (no spurious NaNs or Infs after clamping negative values to zero).
- User can toggle between raw, isotope-corrected, and quantified image views in LipidQMap without re-import.

## Limitations

- Only applicable to feature-by-pixel layout; pixel-by-feature or other tidy formats require a separate transpose or conversion step before using this skill.
- Assumes the input HDF5 file strictly adheres to Cardinal::HDF5 conventions; non-standard or malformed files may not be correctly preserved.
- Writing large intensity matrices (e.g., 5 GB imzML files with 2500 features) can be slow on disk-bound systems; no streaming or chunked write optimization is described.
- No explicit version control or audit trail is recorded when overwriting the intensity dataset; prior values are lost unless separately backed up.

## Evidence

- [other] Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout.: "Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout."
- [other] Write the corrected intensity matrix back to the HDF5 container in the same spectraData/intensity dataset, preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and featureData groups unchanged.: "Write the corrected intensity matrix back to the HDF5 container in the same spectraData/intensity dataset, preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and"
- [readme] LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions."
- [readme] Can toggle view between raw, isotope corrected and quantified images.: "Can toggle view between raw, isotope corrected and quantified images."
