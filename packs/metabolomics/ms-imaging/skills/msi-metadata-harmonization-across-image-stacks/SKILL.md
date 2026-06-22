---
name: msi-metadata-harmonization-across-image-stacks
description: Use when you have processed and quantified MSI data from one or more imzML files in LipidQMap and need to export them as a unified, standards-compliant HDF5 container that preserves feature-by-pixel intensity matrices, per-feature lipid annotations (m/z, lipid class, adduct, neutral ID), per-pixel.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3382
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

# MSI Metadata Harmonization Across Image Stacks

## Summary

Reconstruct and validate HDF5 export containers for mass spectrometry imaging (MSI) data collections following the Cardinal::HDF5 convention, ensuring standardized storage and interchange of quantified ion images with consistent metadata alignment across multiple imzML sources. This skill is essential when exporting multiple MSI samples or experimental replicates to enable downstream analysis in Cardinal or other HDF5-aware imaging platforms.

## When to use

Apply this skill when you have processed and quantified MSI data from one or more imzML files in LipidQMap and need to export them as a unified, standards-compliant HDF5 container that preserves feature-by-pixel intensity matrices, per-feature lipid annotations (m/z, lipid class, adduct, neutral ID), per-pixel spatial coordinates and metadata (x, y, sample_id, run), and per-sample acquisition parameters (dimensions, pixel size). Use this skill specifically when the downstream analysis requires interoperability with Cardinal or when you are creating image collections from multiple imzML files that must maintain consistent dimension scales and indexing conventions.

## When NOT to use

- Input is already a validated HDF5 file following Cardinal::HDF5 convention—use direct read/query instead of reconstruction.
- Ion image data is sparse and irregularly sampled (e.g., individual spots not on a rectangular grid)—may require inclusion of min_*/max_* bounding box attributes for sparse coordinate handling.
- Downstream tool does not support HDF5 or dimension scales (e.g., legacy imaging software expecting NetCDF, Analyze, or NIFTI formats)—export to alternative format instead.

## Inputs

- Quantified ion image intensities (feature-by-pixel matrix, n_features × n_pixels, float32)
- Per-feature metadata (feature_id, lipid_class, adduct, neutral_id, m/z, is_standard flag)
- Per-pixel spatial and sample metadata (x, y in 1-based pixel coordinates, sample_index, run, sample_id)
- Per-sample acquisition parameters (sample_id, height_px, width_px, n_pixels, optional pixel_size_um_x/y)
- Source imzML file collection metadata (image_type, creator_version)

## Outputs

- HDF5 container file conforming to Cardinal::HDF5 convention
- Root-level attributes (format, creator, creator_version, image_type)
- spectraData group with dimension-scaled intensity matrix
- pixelData group with pixel_index, x, y, sample_index, run, sample_id columns and coord dataset
- featureData group with feature_index, feature_id, lipid_class, adduct, neutral_id, mz, is_standard columns sorted by m/z
- samples subgroups with per-sample metadata (sample_id, height_px, width_px, n_pixels, pixel_size_um_x/y)

## How to apply

Organize quantified ion image intensities as a feature-by-pixel matrix (n_features × n_pixels, float32 dtype) and create an HDF5 root file with GZIP level 4 compression and shuffle filter. Write root-level attributes (format='Cardinal::HDF5', creator='LipidQMap', creator_version, image_type) and populate three primary groups: (1) spectraData—write the intensity dataset with feature_by_pixel layout attribute, attach dimension scales linking axis 0 to featureData/feature_id and axis 1 to pixelData/pixel_index, add n_features and n_spectra attributes; (2) pixelData—write column datasets (pixel_index as int64, x/y as int32 using 1-based coordinates, sample_index, run, sample_id as UTF-8 strings) row-aligned with intensity axis 1, create a coord dataset (n_pixels × 2 int32 matrix of [x, y] pairs), add columns group attribute; (3) featureData—write per-feature metadata datasets (feature_index, feature_id, lipid_class, adduct, neutral_id as UTF-8; mz as float32 for sorting; is_standard as bool) aligned with intensity axis 0, sorted ascending by m/z, add columns group attribute. Create a samples subgroup with one subgroup per sample (keyed by 1-based index string) containing sample attributes (sample_id, height_px, width_px, n_pixels, pixel_size_um_x/y if known). Finally, validate the output: verify all required datasets and groups exist, check shapes and dtypes, confirm dimension scales are properly linked, and verify 1-based indexing throughout.

## Related tools

- **LipidQMap** (Primary tool that quantifies MSI data from imzML files and exports quantified ion images as HDF5 containers following Cardinal::HDF5 conventions.) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Downstream R package for spatial mass spectrometry imaging analysis that reads and interprets HDF5 containers exported via LipidQMap using the Cardinal::HDF5 layout convention.) — https://cardinalmsi.org

## Evaluation signals

- Root-level attributes present and correctly set: format='Cardinal::HDF5', creator='LipidQMap', creator_version populated, image_type specified.
- All required groups exist (spectraData, pixelData, featureData, samples) with correct structure and no missing datasets.
- spectraData intensity dataset shape matches (n_features, n_pixels), dtype is float32, and dimension scales are properly linked to featureData/feature_id (axis 0) and pixelData/pixel_index (axis 1).
- featureData datasets sorted ascending by mz; feature_index, feature_id, lipid_class, adduct, neutral_id are UTF-8 strings; mz is float32; is_standard is bool; all aligned with axis 0 of intensity matrix.
- pixelData pixel_index is int64, x and y are int32 with 1-based coordinates; sample_index, run, sample_id are UTF-8 strings; all column datasets row-aligned with axis 1 of intensity matrix; coord dataset is n_pixels × 2 int32 matrix of [x, y] pairs.
- samples subgroups keyed by 1-based index strings, each containing sample_id, height_px, width_px, n_pixels attributes; pixel_size_um_x/y included if known; min_*/max_* omitted for dense rectangular exports.
- File validates without schema errors; all datasets are contiguous or chunked with GZIP level 4 compression and shuffle filter applied.

## Limitations

- No changelog available in the LipidQMap repository—version compatibility of exported HDF5 files with future Cardinal releases is not explicitly documented.
- Sparse imaging data (non-rectangular pixel grids) requires inclusion of min_*/max_* bounding box attributes, which are omitted for dense rectangular exports; the skill as documented does not cover sparse sampling edge cases.
- 1-based indexing convention may cause confusion for users familiar with 0-based array languages (Python, C); transformation logic must be explicitly handled at export time.
- The skill assumes that per-feature metadata (lipid_class, adduct, neutral_id) are present and non-null; incomplete or missing feature annotations will result in incomplete featureData groups.

## Evidence

- [methods] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data.: "LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions, enabling standardized storage and interchange of quantified imaging data."
- [methods] Load quantified ion image intensities and organize as a feature-by-pixel matrix (n_features × n_pixels) with float32 dtype. Create the HDF5 root file with GZIP level 4 compression and shuffle filter applied to large numeric arrays.: "Load quantified ion image intensities and organize as a feature-by-pixel matrix (n_features × n_pixels) with float32 dtype. 2. Create the HDF5 root file with GZIP level 4 compression and shuffle"
- [methods] Write root-level attributes (format='Cardinal::HDF5', creator='LipidQMap', creator_version, image_type). Populate the spectraData group: write the intensity dataset with feature_by_pixel layout attribute, attach dimension scales linking axis 0 to featureData/feature_id and axis 1 to pixelData/pixel_index.: "Write root-level attributes (format='Cardinal::HDF5', creator='LipidQMap', creator_version, image_type). 4. Populate the spectraData group: write the intensity dataset with feature_by_pixel layout"
- [methods] Populate the featureData group with per-feature metadata datasets (feature_index as int64, feature_id and lipid_class and adduct and neutral_id as UTF-8 strings, mz as float32 for sorting, is_standard as bool) aligned with intensity axis 0, sorted ascending by mz.: "Populate the featureData group with per-feature metadata datasets (feature_index as int64, feature_id and lipid_class and adduct and neutral_id as UTF-8 strings, mz as float32 for sorting,"
- [methods] Validate the output file: verify all required datasets and groups exist, check dataset shapes and dtypes, confirm dimension scales are properly linked, and verify 1-based indexing is used throughout.: "Validate the output file: verify all required datasets and groups exist, check dataset shapes and dtypes, confirm dimension scales are properly linked, and verify 1-based indexing is used throughout."
- [readme] LipidQMap is a program to support accurate quantitation of Mass Spectrometry Imaging data. It has the following features: User friendly graphical user interface.: "LipidQMap is a program to support accurate quantitation of Mass Spectrometry Imaging data. It has the following features: User friendly graphical user interface."
- [readme] Can export the images, both as individual files or as image collection in panels.: "Can export the images, both as individual files or as image collection in panels."
