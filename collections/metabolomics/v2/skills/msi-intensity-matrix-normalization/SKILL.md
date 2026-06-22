---
name: msi-intensity-matrix-normalization
description: Use when after isotope correction when you have extracted intensity matrices from imzML or HDF5 MSI data and need to convert raw or isotope-corrected ion-image intensities into quantified values using a known internal standard lipid species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - LipidQMap
  - Cardinal
  - h5py / h5netcdf
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

# msi-intensity-matrix-normalization

## Summary

Normalize Mass Spectrometry Imaging (MSI) ion-image intensity matrices by dividing target lipid intensities element-wise by user-defined internal standard intensities, converting raw or isotope-corrected values into quantified measurements. This skill enables accurate lipid quantitation by correcting for instrument response variation and sample preparation differences across pixels.

## When to use

Apply this skill after isotope correction when you have extracted intensity matrices from imzML or HDF5 MSI data and need to convert raw or isotope-corrected ion-image intensities into quantified values using a known internal standard lipid species. Use it when the internal standard feature has been identified in the feature metadata and you want to normalize pixel-by-pixel intensity ratios.

## When NOT to use

- Input image_type is not 'isotope' (e.g., raw or already quantified data); skip normalization or restart from isotope-corrected stage.
- Internal standard feature is absent or cannot be matched in featureData; user must select a valid internal standard before proceeding.
- Internal standard intensity is uniformly zero or missing across all pixels; normalization would produce all-NaN output and should be flagged as a data quality issue.

## Inputs

- HDF5 MSI export file with root attribute image_type='isotope'
- spectraData/intensity matrix (n_features × n_pixels, float32)
- featureData with feature_id column
- user-defined internal standard identifier (feature name or sample identifier)
- target lipid feature identifier

## Outputs

- Quantified intensity matrix (1 × n_pixels, float32)
- HDF5 file with root attribute image_type='quant'
- Updated featureData metadata for quantified result
- NaN or zero-masked pixel values for invalid standard intensities

## How to apply

Load the isotope-corrected intensity matrix (shape: n_features × n_pixels, float32) and featureData from the HDF5 MSI export. Identify the user-defined internal standard feature by matching its feature_id in featureData; retrieve its intensity row as the denominator vector. For each target lipid feature, retrieve its intensity row and divide element-wise by the internal standard intensity vector. Handle division-by-zero and invalid pixels (standard intensity ≤ 0) by masking them as NaN or zero to prevent propagation of spurious quantified values. Write the resulting normalized intensity matrix to a new HDF5 file following Cardinal::HDF5 conventions, updating the root attribute image_type to 'quant' and maintaining dimension scales and feature metadata referencing the single quantified target.

## Related tools

- **LipidQMap** (GUI application that wraps intensity normalization and performs isotope correction prior to quantitation; reads user-defined internal standards from Excel and toggles quantified view) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines HDF5 container conventions for MSI export files; normalization output must conform to Cardinal::HDF5 schema) — https://cardinalmsi.org
- **h5py / h5netcdf** (HDF5 reader/writer libraries for programmatic access to intensity matrices and metadata during normalization)

## Examples

```
import h5py
with h5py.File('isotope_corrected.h5', 'r') as f:
    target_idx = list(f['featureData']['feature_id']).index('PC(32:0)[M+H]+')
    standard_idx = list(f['featureData']['feature_id']).index('PC(34:1)[M+H]+')
    target_int = f['spectraData']['intensity'][target_idx, :]
    standard_int = f['spectraData']['intensity'][standard_idx, :]
    quant = target_int / (standard_int + 1e-10)
    quant[standard_int <= 0] = 0
```

## Evaluation signals

- Output intensity matrix shape is (1, n_pixels) after normalization of a single target lipid.
- Root attribute image_type in output HDF5 file equals 'quant'.
- All pixel intensities where internal standard intensity ≤ 0 are masked as NaN or zero (no division-by-zero results).
- Quantified intensities are bounded and plausible (no Inf values); spot-check a few pixels by hand division: target[i] / standard[i].
- featureData in output file references the single target lipid and includes its quantitation metadata.

## Limitations

- Division-by-zero and invalid pixels (standard intensity ≤ 0) must be explicitly masked; naive element-wise division produces Inf or -Inf that will corrupt visualizations and downstream analysis.
- Normalization assumes the internal standard is homogeneously distributed across the tissue section; spatial heterogeneity of the standard will introduce systematic bias into quantified values.
- No statistical uncertainty propagation; output quantified matrix contains point estimates only, with no error bars or confidence intervals for individual pixel ratios.
- Requires isotope-corrected input (image_type='isotope'); normalization of raw intensity matrices will conflate isotopic overlap with quantitation errors.

## Evidence

- [other] Divide the target lipid intensity vector element-wise by the internal standard intensity vector (normalized quantitation); handle division-by-zero pixels (standard intensity ≤ 0) by masking them as NaN or zero.: "Divide the target lipid intensity vector element-wise by the internal standard intensity vector (normalized quantitation); handle division-by-zero pixels (standard intensity ≤ 0) by masking them as"
- [other] LipidQMap performs quantitation based on user-defined internal standards, enabling conversion of ion-image intensities to quantified values.: "LipidQMap performs quantitation based on user-defined internal standards, enabling conversion of ion-image intensities to quantified values."
- [readme] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions."
- [readme] Can toggle view between raw, isotope corrected and quantified images.: "Can toggle view between raw, isotope corrected and quantified images."
- [other] Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32).: "Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32)."
