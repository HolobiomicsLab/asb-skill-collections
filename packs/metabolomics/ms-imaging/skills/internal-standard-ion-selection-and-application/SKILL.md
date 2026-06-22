---
name: internal-standard-ion-selection-and-application
description: Use when after isotope correction has been applied to MSI ion images, when you have sprayed or identified a reference lipid standard of known amount (pmol/mm²) and need to normalize target lipid intensities against this standard to remove matrix effects and enable cross-pixel and cross-sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - LipidQMap
  - Cardinal
  - h5py or h5netcdf
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

# internal-standard-ion-selection-and-application

## Summary

Select and apply user-defined internal standard lipid ions to normalize isotope-corrected ion-image intensities, enabling conversion of raw mass spectrometry imaging signals to quantified values. This skill is essential for converting relative ion intensities into absolute or semi-quantitative lipid abundance estimates across tissue or sample regions.

## When to use

After isotope correction has been applied to MSI ion images, when you have sprayed or identified a reference lipid standard of known amount (pmol/mm²) and need to normalize target lipid intensities against this standard to remove matrix effects and enable cross-pixel and cross-sample comparisons. Use this skill when the goal is to move from raw or isotope-corrected intensity matrices to quantified image data suitable for statistical analysis or biomarker discovery.

## When NOT to use

- Input ion images have not yet undergone isotope correction (use isotope correction skill first)
- No internal standard lipid has been identified, sprayed, or quantified in the sample
- The internal standard intensity is uniformly zero or near-detection limit across most pixels (normalization will produce unreliable or NaN-dominated output)

## Inputs

- HDF5 MSI export file with image_type='isotope' (isotope-corrected ion images)
- User-defined internal standard specification (feature ID or name from database)
- Target lipid feature ID or name to be quantified
- featureData table with feature_id column for standard and target lookup

## Outputs

- HDF5 MSI export file with image_type='quant' containing normalized quantified intensity matrix
- Updated featureData metadata reflecting single quantified target lipid
- Quantified ion image displayable in LipidQMap with Q (quantitative) view toggle

## How to apply

Identify the internal standard lipid species in the sample database by matching either the sample identifier or feature name; retrieve its isotope-corrected intensity row from the HDF5 spectraData/intensity matrix. For each target lipid of interest, retrieve its corresponding intensity row. Perform element-wise division of the target lipid intensity vector by the internal standard intensity vector to produce normalized quantitation. Handle division-by-zero pixels (where standard intensity ≤ 0) by masking them as NaN or zero. Export the normalized matrix to a new HDF5 file with root attribute image_type set to 'quant' and updated featureData metadata following Cardinal::HDF5 conventions. Verify that the quantified image shows spatial patterns consistent with the isotope-corrected view but with reduced pixel-to-pixel noise and improved comparability across regions.

## Related tools

- **LipidQMap** (Primary GUI application for selecting internal standards from database, toggling between raw/isotope-corrected/quantified views, and exporting quantified images) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines HDF5 container conventions for MSI exports; quantified output must follow Cardinal::HDF5 standard) — https://cardinalmsi.org
- **h5py or h5netcdf** (HDF5 reader/writer library for programmatic access to isotope-corrected intensity matrix and metadata; required for scripted quantification workflows)

## Examples

```
In LipidQMap: (1) Import imzML file with isotope correction enabled. (2) Click on target lipid in Species table. (3) In Settings, confirm the database row 'IS' column points to a standard with 'Is standard'=TRUE and 'Standard amount (pmol/mm2)' populated. (4) Click Settings → select internal standard from dropdown. (5) Press 'Q' to toggle to Quantitative view. (6) Click 'Save images' and select 'Save Quantitative images'.
```

## Evaluation signals

- Output HDF5 file root attribute image_type equals 'quant' (not 'isotope' or 'raw')
- Output quantified intensity matrix shape matches input (n_features × n_pixels) with float32 dtype
- Pixels with zero or negative internal standard intensity are masked as NaN or zero (no inf or invalid values)
- Quantified image view (Q toggle in LipidQMap) displays smooth spatial patterns without extreme outliers caused by low-intensity standard pixels
- featureData metadata in output HDF5 reflects single target lipid (not all original features) with quantitation method documented in file attributes

## Limitations

- Internal standard must be present in the sample at detectable intensity across representative tissue regions; sparse or highly variable standard signal will produce unreliable quantitation
- Quantitation is relative to the chosen internal standard and does not yield absolute abundance without independent standard calibration
- Division-by-zero handling (masking as NaN) reduces effective pixel count in quantified image; high frequency of masked pixels indicates poor internal standard coverage
- Database column 'IS' (internal standard ID reference) must be correctly populated for each target lipid, or standard lookup will fail

## Evidence

- [intro] LipidQMap performs quantitation based on user-defined internal standards: "Performs quantitation based on user defined internal standards."
- [other] Isotope-corrected intensity matrix from HDF5 spectraData/intensity: "Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32)."
- [other] Feature lookup by matching feature_id against user definition: "Locate the internal standard feature in featureData by matching feature_id against the user definition and retrieve its intensity row."
- [other] Element-wise division with NaN/zero masking for zero-intensity pixels: "Divide the target lipid intensity vector element-wise by the internal standard intensity vector (normalized quantitation); handle division-by-zero pixels (standard intensity ≤ 0) by masking them as"
- [other] Output HDF5 follows Cardinal::HDF5 conventions with image_type='quant': "Write the quantified intensity matrix to a new HDF5 file following Cardinal::HDF5 conventions, updating root attribute image_type to 'quant'"
- [readme] Toggle view in LipidQMap between raw, isotope-corrected, and quantified images: "Can toggle view between raw, isotope corrected and quantified images."
- [readme] Database column 'IS' specifies internal standard for quantitation: "**IS**: ID of the standard species that should be used for the quantitation."
