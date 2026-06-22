---
name: msi-intensity-matrix-isotope-correction
description: Use when you have loaded a feature-by-pixel intensity matrix (HDF5 format following Cardinal::HDF5 layout) from imzML MSI data in positive ion mode and you have identified paired [M+H]+ and [M+Na]+ features for the same neutral lipid species (differing by ~22 Da in m/z).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# msi-intensity-matrix-isotope-correction

## Summary

Type II isotopic correction removes [M+Na]+ adduct overlap from [M+H]+ ion images in mass spectrometry imaging (MSI) data by subtracting scaled sodium adduct intensities from protonated adduct intensities across all pixels in a feature-by-pixel intensity matrix. This correction is essential for accurate lipid quantitation in imzML-formatted MSI experiments where multiple adduct forms of the same neutral lipid species co-ionize.

## When to use

Apply this skill when you have loaded a feature-by-pixel intensity matrix (HDF5 format following Cardinal::HDF5 layout) from imzML MSI data in positive ion mode and you have identified paired [M+H]+ and [M+Na]+ features for the same neutral lipid species (differing by ~22 Da in m/z). Use this when [M+H]+ signals are contaminated by isotopic overlap from [M+Na]+ adducts and you need corrected intensities for downstream quantitation based on internal standards.

## When NOT to use

- Input is negative ion mode MSI data (Type II correction applies only to [M+H]+/[M+Na]+ pairs in positive mode)
- No paired [M+H]+/[M+Na]+ features exist in the feature list (correction requires identifiable sodium adduct partners)
- Intensity matrix is not in feature-by-pixel layout or does not follow Cardinal::HDF5 conventions (workflow assumes specific HDF5 structure)

## Inputs

- Feature-by-pixel intensity matrix (float32, shape n_features × n_pixels)
- Feature metadata including neutral lipid identifiers and m/z values
- HDF5 container with Cardinal::HDF5 layout (spectraData/intensity dataset, featureData, pixelData groups)

## Outputs

- Corrected feature-by-pixel intensity matrix (float32, same shape as input)
- Updated HDF5 container with corrected spectraData/intensity dataset
- Preserved featureData, pixelData, and all dimension scales and layout metadata

## How to apply

First, identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and verifying their m/z difference is approximately 22 Da (accounting for the mass difference of Na vs H substitution). For each [M+Na]+ feature, calculate its fractional contribution to the corresponding [M+H]+ feature using natural isotope abundance ratios (the Type II correction model). Subtract the scaled [M+Na]+ pixel intensities from the corresponding [M+H]+ pixel intensities across the entire feature-by-pixel matrix, then clamp all negative resulting values to zero to preserve physical meaning. Write the corrected intensity matrix back to the HDF5 container in the spectraData/intensity dataset while preserving all dimension scales, metadata (feature_by_pixel layout flag), and the pixelData and featureData groups unchanged.

## Related tools

- **LipidQMap** (Implements Type II isotopic correction via graphical interface; loads imzML files, identifies [M+H]+/[M+Na]+ pairs, performs correction, and exports corrected ion images) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines the HDF5 data structure (Cardinal::HDF5 conventions) used to store and retrieve the feature-by-pixel intensity matrix and metadata) — https://cardinalmsi.org

## Evaluation signals

- Corrected [M+H]+ intensities are ≤ raw [M+H]+ intensities at each pixel (subtraction never increases signal)
- No negative intensity values remain in the corrected matrix (all clamped to zero)
- Feature and pixel metadata (IDs, m/z values, spatial coordinates) are unchanged in featureData and pixelData groups
- HDF5 dimension scales and layout flag (feature_by_pixel) are preserved in the output container
- User can toggle between raw, isotope-corrected, and quantified images in LipidQMap UI, confirming correction was applied

## Limitations

- Type II correction assumes natural isotope abundance ratios are constant; unusual isotope enrichment in samples will invalidate the correction model
- Correction requires precise m/z matching (~22 Da difference) to pair [M+H]+ and [M+Na]+ features; low mass resolution or miscalibration may fail to identify pairs
- Negative pixel intensities are clamped to zero, potentially losing information about noise or measurement artifacts
- Correction is applied globally across all pixels; spatial heterogeneity in adduct formation is not accounted for

## Evidence

- [other] LipidQMap performs Type II isotopic correction by correcting [M+H]+ adducts for isotopic overlap contributed by [M+Na]+ adducts in ion images.: "LipidQMap performs Type II isotopic correction by correcting [M+H]+ adducts for isotopic overlap contributed by [M+Na]+ adducts in ion images."
- [other] Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout.: "Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout."
- [other] Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution).: "Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution)."
- [other] For each [M+Na]+ feature, calculate its fractional contribution to the corresponding [M+H]+ feature based on natural isotope abundance ratios (Type II correction model).: "For each [M+Na]+ feature, calculate its fractional contribution to the corresponding [M+H]+ feature based on natural isotope abundance ratios (Type II correction model)."
- [other] Subtract the scaled [M+Na]+ intensities from the [M+H]+ intensities across all pixels, clamping negative values to zero.: "Subtract the scaled [M+Na]+ intensities from the [M+H]+ intensities across all pixels, clamping negative values to zero."
- [other] Write the corrected intensity matrix back to the HDF5 container in the same spectraData/intensity dataset, preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and featureData groups unchanged.: "Write the corrected intensity matrix back to the HDF5 container in the same spectraData/intensity dataset, preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and"
- [readme] Can perform Type II isotopic correction, and can correct [M+H]+ adducts for isotopic overlap from [M+Na]+ adducts.: "Can perform Type II isotopic correction, and can correct [M+H]+ adducts for isotopic overlap from [M+Na]+ adducts."
- [readme] In the imzML import dialog, click on the "Open Files" button to select one or more imzML files. Select if the file contains positive or negative ion mode data.: "In the imzML import dialog, click on the "Open Files" button to select one or more imzML files. Select if the file contains positive or negative ion mode data."
