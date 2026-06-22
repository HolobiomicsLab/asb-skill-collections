---
name: isotope-corrected-image-quantitation
description: Use when after isotopic correction has been performed on MSI ion images and you need to convert normalized intensities into absolute quantitative values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3379
  tools:
  - LipidQMap
  - Cardinal
  - h5py
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

# isotope-corrected-image-quantitation

## Summary

Convert isotope-corrected mass spectrometry ion-image intensities into quantified lipid abundance values by normalizing against user-defined internal standards. This skill enables absolute quantitation of spatial lipid distributions in MSI data by dividing target lipid intensity matrices by internal standard intensity, handling division-by-zero artifacts.

## When to use

Apply this skill after isotopic correction has been performed on MSI ion images and you need to convert normalized intensities into absolute quantitative values. Trigger when: (1) you have isotope-corrected intensity matrices stored in HDF5 format (image_type='isotope'), (2) you have selected a lipid species as the quantitation target, (3) you have identified and located an appropriate internal standard lipid with known quantity (pmol/mm²), and (4) you want to toggle between raw, isotope-corrected, and quantified image views for validation.

## When NOT to use

- Input intensity matrix has not undergone isotopic correction (image_type ≠ 'isotope'); apply isotope correction first.
- No suitable internal standard has been defined or located in the dataset; quantitation requires a known-quantity standard.
- Internal standard intensity is uniformly zero or below detection threshold across all pixels; normalization will produce NaN/zero matrices.

## Inputs

- HDF5 MSI export file with image_type='isotope' attribute
- Isotope-corrected intensity matrix (n_features × n_pixels, float32)
- Feature metadata table (featureData) with feature_id and m/z
- User-defined internal standard identifier (sample ID or feature name)
- Target lipid feature identifier (sample ID or feature name)

## Outputs

- Quantified intensity matrix (single feature × n_pixels, float32)
- HDF5 MSI export file with image_type='quant' attribute
- Updated featureData metadata reflecting quantified target
- Quantified ion image (toggleable view in LipidQMap GUI)

## How to apply

Load the HDF5 MSI export file containing isotope-corrected intensities (verified by root attribute image_type='isotope') using an HDF5 reader (h5py or equivalent). Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32) and retrieve both the target lipid feature row and the internal standard feature row by matching featureData/feature_id against user-defined identifiers. Divide the target lipid intensity vector element-wise by the internal standard intensity vector to produce normalized quantitation. Handle division-by-zero pixels (where standard intensity ≤ 0) by masking them as NaN or zero to avoid spurious values. Write the resulting quantified intensity matrix to a new HDF5 file following Cardinal::HDF5 conventions, updating the root attribute image_type to 'quant' and featureData metadata to reflect the single quantified target. Validate by toggling the image view between raw, isotope-corrected, and quantified modes to confirm spatial patterns are preserved and intensity scales are reasonable.

## Related tools

- **LipidQMap** (Graphical interface for importing imzML files, performing isotopic correction, selecting internal standards, and toggling between raw, isotope-corrected, and quantified image views; exports HDF5 containers following Cardinal::HDF5 conventions) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines HDF5 container conventions and metadata structure for MSI data storage; LipidQMap writes exports following Cardinal::HDF5 standard) — https://cardinalmsi.org
- **h5py** (HDF5 reader/writer library for loading and writing isotope-corrected and quantified intensity matrices and metadata in Python)

## Evaluation signals

- Output HDF5 root attribute image_type equals 'quant' (not 'isotope')
- Quantified intensity matrix has shape (1, n_pixels) or single-feature subset, with values normalized relative to internal standard baseline
- No NaN or infinite values appear in quantified pixels where both target and standard intensity are > 0
- Spatial patterns in quantified image preserve the spatial distribution visible in isotope-corrected image, only with intensity rescaled
- Division-by-zero pixels (standard intensity ≤ 0) are consistently masked as NaN or zero across all quantified features

## Limitations

- Quantitation accuracy depends critically on internal standard quality and homogeneous spatial distribution; non-uniform standard distribution will introduce spatial bias.
- Division-by-zero handling (masking as NaN or zero) is a lossy operation; downstream analyses must account for masked pixels.
- The skill assumes the user has correctly identified and defined the internal standard; mislabeled or missing standards will produce invalid quantitation.
- LipidQMap currently available only for Windows 10+ and Mac (Apple silicon M1+); quantitation workflow unavailable on Linux or Intel Mac.

## Evidence

- [other] LipidQMap performs quantitation based on user-defined internal standards, enabling conversion of ion-image intensities to quantified values.: "LipidQMap performs quantitation based on user-defined internal standards, enabling conversion of ion-image intensities to quantified values."
- [other] Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32). Read the user-provided internal standard definition (sample identifier and/or feature name). Divide the target lipid intensity vector element-wise by the internal standard intensity vector (normalized quantitation); handle division-by-zero pixels (standard intensity ≤ 0) by masking them as NaN or zero.: "Divide the target lipid intensity vector element-wise by the internal standard intensity vector (normalized quantitation); handle division-by-zero pixels (standard intensity ≤ 0) by masking them as"
- [other] The software allows toggling between raw, isotope-corrected, and quantified image views.: "The software allows toggling between raw, isotope-corrected, and quantified image views."
- [intro] Can toggle view between raw, isotope corrected and quantified images.: "Can toggle view between raw, isotope corrected and quantified images."
- [methods] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions."
