---
name: feature-metadata-alignment-across-dimensions
description: Use when you have loaded a feature-by-pixel intensity matrix from an
  MSI HDF5 container and need to perform dimension-preserving corrections (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - LipidQMap
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

# feature-metadata-alignment-across-dimensions

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Align and preserve feature metadata (lipid identifiers, adduct forms, isotope relationships) across the feature and pixel dimensions of a mass spectrometry imaging intensity matrix during correction and transformation workflows. This skill ensures that derived datasets (isotope-corrected, quantified) maintain consistent feature-to-metadata mappings and dimensional scale metadata required by downstream visualization and export steps.

## When to use

Apply this skill when you have loaded a feature-by-pixel intensity matrix from an MSI HDF5 container and need to perform dimension-preserving corrections (e.g., isotopic overlap removal, internal standard normalization) such that all featureData and pixelData metadata remain synchronized with the corrected intensity values. Use this skill specifically when the correction involves identifying paired features (e.g., [M+H]+ and [M+Na]+ lipid species) by neutral lipid identifier and m/z offset, and you must propagate the corrected intensities back into the same HDF5 layout without orphaning or invalidating metadata.

## When NOT to use

- Input intensity matrix has already been transposed to pixel-by-feature layout; re-align to feature-by-pixel before applying this skill.
- Feature metadata is incomplete or missing m/z values, neutral identifiers, or adduct annotations required to identify paired features.
- Correction step requires merging, splitting, or reordering features; this skill assumes feature set is fixed.

## Inputs

- Feature-by-pixel intensity matrix (float32, n_features × n_pixels) from HDF5 spectraData/intensity dataset
- Feature metadata table (featureData group): neutral formula, lipid class, m/z, adduct form, paired feature references
- Pixel metadata table (pixelData group): spatial coordinates, acquisition parameters
- HDF5 dimension scales and layout metadata (Cardinal::HDF5 conventions)

## Outputs

- Corrected feature-by-pixel intensity matrix (float32, same shape n_features × n_pixels) written to spectraData/intensity
- HDF5 container with preserved featureData, pixelData, dimension scales, and layout metadata
- Feature-to-metadata alignment invariant: each row index maps to exactly one featureData entry before and after correction

## How to apply

Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and all associated feature metadata from the HDF5 spectraData/intensity dataset and featureData group using the Cardinal::HDF5 layout convention. Parse the featureData to extract neutral lipid identifiers, m/z values, and adduct form annotations for each feature row. Identify paired features (e.g., [M+H]+ and [M+Na]+ forms of the same neutral lipid) by matching identifiers and validating mass offsets (e.g., ~22 Da for Na vs H). When computing derived values (e.g., isotopic correction coefficients based on natural abundance ratios), apply transformations row-wise to preserve feature identity and ensure each corrected feature row corresponds exactly to one entry in featureData. After correction, write the corrected intensity matrix back to the same spectraData/intensity dataset, explicitly preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and featureData groups unchanged. Verify that feature counts and pixel counts remain constant and that no featureData rows were added, removed, or reordered.

## Related tools

- **LipidQMap** (GUI-based MSI quantitation platform that loads imzML files, performs Type II isotopic correction (matching [M+H]+ and [M+Na]+ features by neutral lipid identity), and exports corrected intensity matrices as HDF5 containers following Cardinal::HDF5 layout, preserving all metadata dimensions.) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (R/Bioconductor package defining HDF5 layout conventions (Cardinal::HDF5) for MSI data, including spectraData, featureData, pixelData groups and dimension scales used by LipidQMap to ensure feature-metadata alignment across corrections.) — https://cardinalmsi.org

## Evaluation signals

- Verify that corrected intensity matrix has identical shape (n_features, n_pixels) as input matrix; no rows or columns added or removed.
- Confirm that featureData group row count equals corrected intensity matrix row count; each feature index maps to exactly one featureData entry.
- Check that dimension scales (feature IDs, pixel coordinates) are present and match intensity matrix dimensions after write-back to HDF5.
- Validate that pixelData group is unchanged (same columns, row count equal to n_pixels).
- Inspect corrected intensity values: verify that clamping rules (e.g., negative values → 0 after isotopic subtraction) were applied correctly and that corrected values remain finite (no NaN or Inf).

## Limitations

- Requires manual curation of feature metadata (neutral formula, adduct form, paired feature references) in the database; mismatched or missing metadata will cause feature pairing to fail silently or produce incorrect corrections.
- Type II isotopic correction model assumes natural isotope abundance ratios are accurate and constant across all pixels; deviations in isotope ratios due to sample heterogeneity or instrumental drift are not modeled.
- HDF5 spectraData/intensity dataset must use float32 or compatible numeric type; integer or complex types are not explicitly handled.
- Correction step is destructive (overwrites spectraData/intensity in-place); no rollback mechanism is provided in the HDF5 container if correction parameters were misconfigured.

## Evidence

- [other] Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout.: "Load the feature-by-pixel intensity matrix (float32, shape n_features × n_pixels) and feature metadata from the input HDF5 file using the Cardinal::HDF5 layout."
- [other] Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution).: "Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution)."
- [other] Write the corrected intensity matrix back to the HDF5 container in the same spectraData/intensity dataset, preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and featureData groups unchanged.: "Write the corrected intensity matrix back to the HDF5 container in the same spectraData/intensity dataset, preserving dimension scales, layout metadata (feature_by_pixel), and all pixelData and"
- [readme] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions."
- [readme] Each row in the Excel database represents a different species, and the file should contain the following columns: ID, Class, Neutral Formula, Adducts, M-2 Isotope, Na+ Isotope.: "Each row in the Excel database represents a different species, and the file should contain the following columns (the column titles need to match exactly): ID, Class, Neutral Formula, Adducts, M-2"
