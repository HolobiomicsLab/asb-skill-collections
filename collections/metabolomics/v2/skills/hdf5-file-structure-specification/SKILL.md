---
name: hdf5-file-structure-specification
description: Use when when exporting quantified MSI data (feature-by-pixel intensity matrices with associated ion m/z, lipid annotations, and pixel spatial coordinates) from LipidQMap and you need to produce a standards-compliant HDF5 container that can be read by Cardinal and other MSI analysis tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3371
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HDF5 File Structure Specification

## Summary

Specification and validation of HDF5 container structure for Mass Spectrometry Imaging (MSI) data exports following the Cardinal::HDF5 layout convention. This skill ensures quantified ion images are serialized with standardized group hierarchies, dimension scales, metadata attributes, and indexing schemes for interchange and downstream analysis.

## When to use

When exporting quantified MSI data (feature-by-pixel intensity matrices with associated ion m/z, lipid annotations, and pixel spatial coordinates) from LipidQMap and you need to produce a standards-compliant HDF5 container that can be read by Cardinal and other MSI analysis tools. Apply this skill when the output must preserve feature metadata (m/z, lipid class, adduct, standard status), pixel metadata (spatial coordinates, sample provenance), and bidirectional linkage between spectral and pixel axes via dimension scales.

## When NOT to use

- Input is already in a different standardized MSI format (e.g., native Cardinal .hdf5 produced by another pipeline) — validate and reuse rather than re-export.
- Pixel coordinates are unavailable or sparse (non-rectangular imaging) — use only if you have complete spatial coverage or explicitly document sparse pixel mapping in min_*/max_* attributes.
- Feature metadata (m/z, lipid annotations) is absent or incomplete — this specification requires feature_id, lipid_class, and adduct fields; missing fields will break downstream Cardinal imports.

## Inputs

- Quantified ion image intensity matrix (n_features × n_pixels, float32)
- Feature metadata table (feature_index, feature_id, lipid_class, adduct, neutral_id, m/z, is_standard)
- Pixel metadata table (pixel_index, x, y coordinates, sample_index, run, sample_id)
- Sample-level attributes (sample_id, height_px, width_px, n_pixels, pixel_size_um_x/y if known)
- Destination file path for HDF5 output

## Outputs

- HDF5 file following Cardinal::HDF5 layout convention
- Validated HDF5 structure with spectraData, pixelData, featureData, and samples groups
- Dimension-scaled linking between intensity matrix axes and feature/pixel metadata
- File-level and group-level metadata attributes documenting format version and data provenance

## How to apply

Organize quantified ion image intensities as a feature-by-pixel matrix (n_features × n_pixels, float32 dtype). Create an HDF5 file with GZIP level 4 compression and shuffle filter. Populate five major groups: (1) root attributes (format='Cardinal::HDF5', creator, version); (2) spectraData group with intensity dataset, dimension scales linking axes to featureData/feature_id and pixelData/pixel_index, and group metadata n_features and n_spectra; (3) pixelData group with per-pixel column datasets (pixel_index int64, x/y int32 using 1-based coordinates, sample/run/sample_id strings, coord matrix) sorted to align with intensity axis 1; (4) featureData group with per-feature datasets (feature_index, feature_id, lipid_class, adduct, neutral_id, mz float32, is_standard bool) sorted ascending by m/z and aligned with intensity axis 0; (5) samples subgroup (one per unique sample, keyed by 1-based index string) containing sample attributes (sample_id, height_px, width_px, n_pixels, pixel_size_um_x/y if available). After writing, validate: all required datasets and groups exist, dataset shapes and dtypes match specification, dimension scales are properly linked, and 1-based indexing is used throughout.

## Related tools

- **LipidQMap** (MSI quantitation and HDF5 export engine; generates quantified ion images and manages lipid metadata prior to serialization) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (MSI analysis framework that reads and consumes Cardinal::HDF5 containers; defines the layout convention and validation semantics) — https://cardinalmsi.org

## Evaluation signals

- Root-level attributes include format='Cardinal::HDF5', creator, and creator_version; file is valid HDF5 and opens without I/O errors.
- spectraData group contains intensity dataset with correct shape (n_features × n_pixels), float32 dtype, and dimension scales properly linked to featureData/feature_id (axis 0) and pixelData/pixel_index (axis 1).
- pixelData group contains pixel_index (int64), x and y (int32, 1-based), sample_index, run, sample_id (UTF-8 strings), and coord dataset (n_pixels × 2 int32 matrix); row count equals intensity matrix column count.
- featureData group contains feature_index (int64), feature_id, lipid_class, adduct, neutral_id (UTF-8 strings), mz (float32), is_standard (bool); row count equals intensity matrix row count; features are sorted ascending by m/z.
- samples subgroup structure is present with one subgroup per unique sample (keyed by 1-based index string), each containing sample attributes (sample_id, height_px, width_px, n_pixels); sparse exports include min_*/max_* coordinate bounds, dense rectangular exports omit these attributes.

## Limitations

- 1-based indexing is mandatory throughout (pixel_index, feature_index, sample subgroup keys); datasets using 0-based indexing will violate the Cardinal::HDF5 convention and cause downstream import failures.
- Feature metadata sorting (ascending by m/z) must be performed before HDF5 writing; unsorted features will cause axis misalignment and incorrect spectral-to-feature mapping in Cardinal.
- Dimension scales (links from intensity axes to featureData and pixelData rows) are required for proper bidirectional traceability; omission breaks automated downstream workflows that depend on axis metadata.
- Dense rectangular exports should omit min_*/max_* pixel coordinate attributes; including them when all pixels are present introduces ambiguity and may cause parsing errors in strict validators.
- Sample attributes (height_px, width_px, pixel_size_um_x/y) are optional but recommended; pixel_size_um fields are used by downstream visualization and registration tools — omission may degrade spatial interpretation.

## Evidence

- [methods] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions"
- [methods] Load quantified ion image intensities and organize as a feature-by-pixel matrix (n_features × n_pixels) with float32 dtype. Create the HDF5 root file with GZIP level 4 compression and shuffle filter applied to large numeric arrays.: "Load quantified ion image intensities and organize as a feature-by-pixel matrix (n_features × n_pixels) with float32 dtype. Create the HDF5 root file with GZIP level 4 compression and shuffle filter"
- [methods] Write root-level attributes (format='Cardinal::HDF5', creator='LipidQMap', creator_version, image_type). Populate the spectraData group: write the intensity dataset with feature_by_pixel layout attribute, attach dimension scales linking axis 0 to featureData/feature_id and axis 1 to pixelData/pixel_index: "Write root-level attributes (format='Cardinal::HDF5', creator='LipidQMap', creator_version, image_type). Populate the spectraData group: write the intensity dataset with feature_by_pixel layout"
- [methods] Populate the pixelData group with column datasets (pixel_index as int64, x and y as int32 using 1-based coordinates, sample_index, run, sample_id as UTF-8 strings) maintaining row alignment with intensity axis 1: "Populate the pixelData group with column datasets (pixel_index as int64, x and y as int32 using 1-based coordinates, sample_index, run, sample_id as UTF-8 strings) maintaining row alignment with"
- [methods] Populate the featureData group with per-feature metadata datasets (feature_index as int64, feature_id and lipid_class and adduct and neutral_id as UTF-8 strings, mz as float32 for sorting, is_standard as bool) aligned with intensity axis 0, sorted ascending by mz: "Populate the featureData group with per-feature metadata datasets (feature_index as int64, feature_id and lipid_class and adduct and neutral_id as UTF-8 strings, mz as float32 for sorting,"
- [methods] Create the samples subgroup structure with one subgroup per sample (keyed by 1-based index string) containing sample attributes (sample_id, height_px, width_px, n_pixels, pixel_size_um_x/y if known; omit min_*/max_* for dense rectangular exports, include them only for sparse): "Create the samples subgroup structure with one subgroup per sample (keyed by 1-based index string) containing sample attributes (sample_id, height_px, width_px, n_pixels, pixel_size_um_x/y if known;"
- [methods] Validate the output file: verify all required datasets and groups exist, check dataset shapes and dtypes, confirm dimension scales are properly linked, and verify 1-based indexing is used throughout.: "Validate the output file: verify all required datasets and groups exist, check dataset shapes and dtypes, confirm dimension scales are properly linked, and verify 1-based indexing is used throughout"
- [readme] Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook.: "Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook"
