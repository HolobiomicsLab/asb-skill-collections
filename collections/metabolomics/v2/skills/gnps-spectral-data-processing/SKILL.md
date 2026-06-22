---
name: gnps-spectral-data-processing
description: Use when your input is raw or semi-processed MS/MS spectra fetched from GNPS or a compatible library (e.g., EMBL-MCF 2.0, NIST23) and you need to prepare them for neural-network-based formula prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - FIDDLE
  - msfiddle
  - GNPS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
---

# GNPS spectral data processing

## Summary

Load, parse, and standardize tandem mass spectrometry (MS/MS) spectra from GNPS databases into a structured format suitable for molecular formula inference. This skill prepares raw spectral data with required metadata fields (precursor m/z, adduct type, collision energy) for downstream deep learning prediction.

## When to use

Your input is raw or semi-processed MS/MS spectra fetched from GNPS or a compatible library (e.g., EMBL-MCF 2.0, NIST23) and you need to prepare them for neural-network-based formula prediction. The spectra must contain or be enriched with precursor m/z, precursor type (adduct), and collision energy; spectra lacking these fields cannot proceed through FIDDLE inference.

## When NOT to use

- Your spectra are already in a processed feature representation (e.g., molecular fingerprints, spectral embeddings). Processing is for raw or minimally processed spectral data only.
- Precursor m/z or adduct type is unknown or cannot be inferred. FIDDLE requires these fields; spectra with missing critical metadata should be filtered or annotated separately.
- Input is from a non-MS/MS modality (e.g., GC-MS, LC-UV). FIDDLE is trained on high-resolution tandem mass spectra; other modalities require different preprocessing pipelines.

## Inputs

- GNPS spectral records (raw or via API)
- MGF file with required fields: TITLE, PEPMASS, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY
- MS/MS peak lists (m/z array, intensity array)
- Precursor m/z and adduct annotation

## Outputs

- Standardized MGF file with validated metadata
- Parsed spectral objects ready for FIDDLE inference
- Peak intensity arrays normalized and sorted by m/z

## How to apply

Retrieve spectral records from GNPS or load them via a Python script (e.g., test_caffeine.py) and convert them to MGF format, ensuring each spectrum record includes TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, and COLLISION_ENERGY fields. Normalize peak m/z and intensity arrays to the expected range (commonly 0–100 for relative intensity). Validate that precursor m/z matches the observed [M+H]+ or [M−H]− adduct mass and collision energy is numeric. Once standardized, export to MGF or load directly into the FIDDLE inference pipeline via the MsFiddlePredictor API or CLI. Proper parsing and field presence are critical; missing or malformed metadata will cause inference to fail or produce unreliable predictions.

## Related tools

- **FIDDLE** (Neural network model for molecular formula prediction from MS/MS spectra; consumes standardized MGF and outputs formula candidates with confidence scores) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API wrapper for FIDDLE; provides command-line and programmatic interfaces for batch spectral processing and inference) — https://github.com/josiehong/msfiddle
- **GNPS** (Source database and API for retrieving and querying MS/MS spectra from public libraries)

## Examples

```
python test_caffeine.py
```

## Evaluation signals

- All required MGF fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) are present and non-empty for ≥95% of spectra.
- Peak m/z values are monotonically increasing and within typical instrument range (m/z 50–1000 or higher); intensity values are numeric and non-negative.
- Precursor m/z matches the calculated neutral mass for the inferred adduct (e.g., [M+H]+ should have precursor_mz = M + 1.00783, within instrument accuracy ~5 ppm for Orbitrap or ~30 ppm for Q-TOF).
- FIDDLE inference runs without errors and produces Rescore (k) output columns with numeric confidence scores in a valid range (typically 0–1 or normalized percentiles).
- Output CSV contains one row per input spectrum with renamed columns 'Refined Formula (0..4)' and 'Rescore (0..4)' as specified in the FIDDLE v2.0.0 schema.

## Limitations

- FIDDLE v2.0.0 requires collision energy to be present and numeric; spectra with collision energy labeled 'Unknown' or missing may produce suboptimal predictions.
- Spectral quality and precursor isolation purity directly affect formula inference; heavily chimeric or contaminated spectra may yield low-confidence or incorrect predictions.
- The rescore model (v2.0.0 with Siamese architecture) is trained on Orbitrap and Q-TOF data; application to other instrument types (e.g., sector-based, ion traps) without retraining may degrade performance.
- GNPS spectra fetched live may have variable metadata completeness; local curation or filtering may be required for large-scale batch processing.
- Peak intensity normalization and filtering strategies (e.g., removal of low-abundance fragments) are not explicitly standardized in the public CLI; custom preprocessing may be needed for instrument-specific workflows.

## Evidence

- [readme] The input format is `mgf`, where `title`, `precursor_mz`, `precursor_type`, `collision_energy` fields are required.: "The input format is `mgf`, where `title`, `precursor_mz`, `precursor_type`, `collision_energy` fields are required."
- [readme] See [`test_caffeine.py`](./test_caffeine.py) for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS.: "See [`test_caffeine.py`] for a worked example running FIDDLE on a caffeine Orbitrap spectrum fetched live from GNPS."
- [other] Extract rescore predictions and rename Rescore (k) output columns to standardized format.: "Extract rescore predictions and rename Rescore (k) output columns to standardized format."
- [readme] Use the package from the command line, from native Python arrays, or from MGF files.: "Use the package from the command line, from native Python arrays, or from MGF files."
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
