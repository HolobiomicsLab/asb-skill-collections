---
name: lipid-feature-identifier-matching
description: Use when you have an isotope-corrected or raw MSI dataset stored in HDF5 format following Cardinal::HDF5 conventions, a user-provided internal standard definition (sample identifier and/or feature name), and need to locate and extract the intensity row for that lipid before performing ratio-based.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2421
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - LipidQMap
  - h5py
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

# lipid-feature-identifier-matching

## Summary

Match user-specified lipid identifiers (internal standards or target species) to their corresponding feature rows in mass spectrometry imaging HDF5 data structures by querying featureData metadata. This skill enables precise extraction of intensity vectors for downstream quantitation or comparison operations.

## When to use

You have an isotope-corrected or raw MSI dataset stored in HDF5 format following Cardinal::HDF5 conventions, a user-provided internal standard definition (sample identifier and/or feature name), and need to locate and extract the intensity row for that lipid before performing ratio-based quantitation or statistical comparison. Triggered when moving from generic feature tables to lipid-specific extraction.

## When NOT to use

- Input HDF5 file does not follow Cardinal::HDF5 conventions or lacks featureData/feature_id metadata.
- User identifier is ambiguous or matches multiple lipid species (require disambiguation before proceeding).
- Target lipid is not present in the loaded dataset (e.g., database species not detected in mass spectrum).

## Inputs

- HDF5 file with root attribute image_type ∈ {'raw', 'isotope', 'quant'} following Cardinal::HDF5 conventions
- featureData group containing feature_id array (string identifiers for lipids)
- spectraData/intensity matrix (n_features × n_pixels, float32)
- User-provided lipid identifier string (internal standard definition or target species name)

## Outputs

- Matched feature_id string
- Feature row index (integer)
- Intensity vector (1D float32 array, length n_pixels)

## How to apply

Load the HDF5 MSI export file using an HDF5 reader (h5py or equivalent). Read the featureData metadata group to access the feature_id array, which contains lipid identifiers. Match the user-provided internal standard definition (which may be a feature name, lipid species identifier, or sample label) against the feature_id entries using exact string comparison or normalized matching (e.g., case-insensitive, whitespace-trimmed). Once matched, retrieve the corresponding row index and extract the intensity vector from spectraData/intensity at that row. Handle non-matches by raising a clear error identifying which identifier could not be found and listing available options from featureData/feature_id. Document the matched feature_id, row index, and intensity shape (1 × n_pixels) for audit and downstream validation.

## Related tools

- **LipidQMap** (HDF5 MSI export generator and quantitation interface that produces the Cardinal::HDF5 containers on which this matching skill operates) — https://github.com/swinnenteam/LipidQMap
- **h5py** (HDF5 reader/writer library for loading and querying featureData metadata and intensity matrices)
- **Cardinal** (MSI data format standard (Cardinal::HDF5) that defines featureData structure and conventions used by this skill) — https://cardinalmsi.org

## Examples

```
import h5py
with h5py.File('msi_data.h5', 'r') as f:
    feature_ids = f['featureData/feature_id'][:]
    match_idx = list(feature_ids).index('PE(40:6)')
    intensity = f['spectraData/intensity'][match_idx, :]
```

## Evaluation signals

- Matched feature_id exists in featureData/feature_id array and is returned with exact case/formatting as stored in HDF5.
- Retrieved intensity vector has shape (n_pixels,) and dtype float32, with no NaN or inf values introduced by the matching step itself.
- Row index is a valid integer in range [0, n_features) and correctly indexes into spectraData/intensity.
- User-provided identifier is documented and retrievable for audit; unmatched identifiers raise explicit error with list of available feature_ids.
- When the same user identifier is queried twice in succession, the same feature_id and intensity vector are returned (determinism check).

## Limitations

- Matching is string-based and case-sensitive by default; user identifiers must exactly match featureData/feature_id entries or matching will fail.
- No fuzzy or partial matching: a typo in the user-provided identifier will result in a non-match error rather than a close suggestion.
- If featureData/feature_id contains duplicate lipid identifiers (malformed HDF5), the first match is returned without warning.
- The skill does not validate that the matched lipid is present in all loaded imzML files when multiple files are open simultaneously; subsequent quantitation may fail if the standard is absent from a particular spatial region.

## Evidence

- [other] Read the user-provided internal standard definition (sample identifier and/or feature name).: "Read the user-provided internal standard definition (sample identifier and/or feature name)."
- [other] Locate the internal standard feature in featureData by matching feature_id against the user definition and retrieve its intensity row.: "Locate the internal standard feature in featureData by matching feature_id against the user definition and retrieve its intensity row."
- [readme] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions."
- [other] Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32).: "Extract the isotope-corrected intensity matrix from spectraData/intensity (shape: n_features × n_pixels, float32)."
