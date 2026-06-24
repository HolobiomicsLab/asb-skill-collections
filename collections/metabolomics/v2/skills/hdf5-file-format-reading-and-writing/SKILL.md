---
name: hdf5-file-format-reading-and-writing
description: 'Use when you have isotope-corrected or raw ion-image intensity matrices
  from LipidQMap or similar MSI software and need to: (1) export them as persistent
  HDF5 containers for archival or sharing, (2) programmatically read an existing Cardinal::HDF5
  export to extract intensity matrices and feature.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - LipidQMap
  - HDF5 reader/writer library (h5py, h5netcdf, or equivalent)
  - h5py
  - h5netcdf
  - Cardinal
  techniques:
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

# HDF5 File Format Reading and Writing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Read and write mass spectrometry imaging data in HDF5 format following Cardinal::HDF5 conventions, enabling interoperability between imzML-based workflows and quantitative image processing pipelines. This skill is essential for converting raw or isotope-corrected MSI intensities into Cardinal-compliant containers that preserve feature metadata and enable downstream quantitation.

## When to use

Use this skill when you have isotope-corrected or raw ion-image intensity matrices from LipidQMap or similar MSI software and need to: (1) export them as persistent HDF5 containers for archival or sharing, (2) programmatically read an existing Cardinal::HDF5 export to extract intensity matrices and feature annotations for custom quantitation, or (3) convert between imzML and HDF5 representations while preserving dimension scales and featureData metadata.

## When NOT to use

- Input is a raw imzML file that has not yet been processed: use imzML-to-HDF5 conversion within LipidQMap's import dialog instead.
- You need real-time visualization of ion images: HDF5 files are data containers; use LipidQMap's GUI or downstream imaging software for interactive exploration.
- Feature or pixel metadata is absent or corrupted: HDF5 reading will succeed but featureData or pixelData lookups will fail; validate schema integrity first.

## Inputs

- HDF5 file following Cardinal::HDF5 conventions with root attribute image_type and datasets spectraData/intensity (n_features × n_pixels float32), featureData (feature_id, mz arrays), and pixelData (pixel coordinates)
- Intensity matrix (n_features × n_pixels float32) derived from imzML or prior HDF5 export
- Feature metadata (feature_id, mz, neutral_formula, adduct) as structured array or DataFrame
- Pixel metadata (x, y coordinates) as structured array or DataFrame

## Outputs

- HDF5 file compliant with Cardinal::HDF5 conventions containing spectraData/intensity, featureData, pixelData datasets, and root attributes (image_type, polarity, etc.)
- Intensity matrix (n_features × n_pixels float32) extracted from HDF5 spectraData/intensity
- Feature metadata dictionary or DataFrame with columns feature_id, mz, neutral_formula, adduct
- Pixel coordinate array or DataFrame with x, y positions for spatial registration

## How to apply

Load an HDF5 MSI export using h5py or equivalent HDF5 library and verify the root attribute image_type (should be 'raw', 'isotope', or 'quant'). Extract the intensity matrix from the spectraData/intensity dataset (shape: n_features × n_pixels, typically float32) and featureData arrays (feature_id, mz, etc.). For writing: arrange your processed intensity matrix (e.g., quantified or filtered values) into the same n_features × n_pixels shape, create a new HDF5 file following Cardinal conventions, write intensity to spectraData/intensity, copy or update featureData metadata (especially feature_id and mz), set root attribute image_type to reflect the processing stage ('quant' for quantified, 'isotope' for isotope-corrected), and establish dimension scales linking features to rows and pixels to columns. Always handle division-by-zero or missing-value pixels by masking them as NaN or zero before writing.

## Related tools

- **h5py** (Python HDF5 reader/writer library used to load and construct Cardinal::HDF5 containers)
- **h5netcdf** (Alternative HDF5 reader/writer library with NetCDF compatibility for MSI data export)
- **Cardinal** (R/Bioconductor package that defines the HDF5 MSI format standard (Cardinal::HDF5 conventions); LipidQMap exports follow this specification) — https://cardinalmsi.org
- **LipidQMap** (Source tool that generates HDF5 MSI exports in Cardinal::HDF5 format after isotope correction and quantitation) — https://github.com/swinnenteam/LipidQMap

## Examples

```
import h5py
with h5py.File('lipidqmap_export.h5', 'r') as f:
    intensity = f['spectraData/intensity'][:]
    feature_id = f['featureData/feature_id'][:]
    mz = f['featureData/mz'][:]
    image_type = f.attrs['image_type']
print(f'Loaded {intensity.shape[0]} features × {intensity.shape[1]} pixels, image_type={image_type}')
```

## Evaluation signals

- Root attribute image_type matches expected processing stage ('raw', 'isotope', or 'quant').
- spectraData/intensity dataset shape is (n_features, n_pixels) with dtype float32; no NaN or inf values in valid regions except where explicitly masked.
- featureData arrays (feature_id, mz) have length equal to n_features; all feature_id values are unique and match experimental database.
- pixelData arrays (x, y coordinates) have length equal to n_pixels and span expected sample spatial dimensions.
- Dimension scales correctly link rows (features) and columns (pixels) to their corresponding metadata arrays; file can be read by Cardinal's readMSIData() without errors.
- No division-by-zero artifacts: if quantitation was performed, internal standard intensities are > 0 in all pixels or are masked as NaN.

## Limitations

- HDF5 files are static containers: they do not support real-time streaming or interactive parameter adjustment; re-export required if upstream processing (e.g., isotope correction parameters) changes.
- Cardinal::HDF5 format requires strict adherence to dimension scale and metadata conventions; malformed files may not be readable by Cardinal or other downstream tools.
- Large imzML files (e.g., 5 GB) produce correspondingly large HDF5 exports; no lossy compression is applied by default, so storage and transfer times may be significant.
- Pixel imputation (mean of 3×3 neighbors) is applied at import time in LipidQMap; the HDF5 export does not record which pixels were imputed, limiting traceability of missing-data handling.

## Evidence

- [methods] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions."
- [other] Extract isotope-corrected intensity matrix from spectraData/intensity, verify root attribute image_type equals 'isotope', and read user-provided internal standard definition.: "1. Load the HDF5 MSI export file with h5py or similar HDF5 reader, verifying the root attribute image_type equals 'isotope'. 2. Extract the isotope-corrected intensity matrix from"
- [other] Write quantified intensity matrix to new HDF5 file following Cardinal::HDF5 conventions, updating root attribute image_type to 'quant'.: "7. Write the quantified intensity matrix to a new HDF5 file following Cardinal::HDF5 conventions, updating root attribute image_type to 'quant', dimension scales, and featureData metadata to reflect"
- [other] Handle division-by-zero pixels by masking them as NaN or zero when dividing target lipid intensity by internal standard intensity.: "6. Divide the target lipid intensity vector element-wise by the internal standard intensity vector (normalized quantitation); handle division-by-zero pixels (standard intensity ≤ 0) by masking them"
- [intro] LipidQMap can toggle view between raw, isotope corrected and quantified images, with each stored in HDF5 format.: "Can toggle view between raw, isotope corrected and quantified images."
