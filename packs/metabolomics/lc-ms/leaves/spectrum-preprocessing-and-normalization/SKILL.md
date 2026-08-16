---
name: spectrum-preprocessing-and-normalization
description: Use when you have raw MS/MS spectra in MGF or other standard formats that need to be ingested into a machine learning pipeline for cross-modal matching against molecular structures, or when spectra from different collision energy levels or instruments require standardization before comparative.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rdkit
  - PyTorch
  - PyTorch Geometric
  - matchms
  - Python
  - conda
  - pip
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01594
  title: CSU-MS2
evidence_spans:
- '- [rdkit](https://rdkit.org/)'
- '- [pytorch](https://pytorch.org/)'
- '- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '- [matchms](https://matchms.readthedocs.io/en/latest/)'
- '- [python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_csu_ms2_cq
    doi: 10.1021/acs.analchem.5c01594
    title: CSU-MS2
  dedup_kept_from: coll_csu_ms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01594
  all_source_dois:
  - 10.1021/acs.analchem.5c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-preprocessing-and-normalization

## Summary

Preprocess MS/MS spectra from raw instrument data into normalized, standardized feature representations suitable for machine learning and cross-modal retrieval tasks. This skill prepares spectra for contrastive embedding by cleaning noise, normalizing intensity values, and aligning metadata.

## When to use

Apply this skill when you have raw MS/MS spectra in MGF or other standard formats that need to be ingested into a machine learning pipeline for cross-modal matching against molecular structures, or when spectra from different collision energy levels or instruments require standardization before comparative analysis.

## When NOT to use

- Spectra are already embedded in feature space (use this skill before embedding, not after)
- Input is a pre-aggregated spectral library or consensus spectrum (preprocessing assumes raw instrument-level data)
- Metadata (precursor m/z, collision energy) is missing or cannot be reliably reconstructed

## Inputs

- MS/MS spectrum file (MGF format)
- Raw Spectrum object with peaks and metadata (from matchms)
- Collision energy level (low, medium, or high)

## Outputs

- Normalized Spectrum object with cleaned peaks and validated metadata
- Precursor m/z value (scalar)
- Spectrum feature vector ready for neural encoding

## How to apply

Load MS/MS spectrum data using matchms (e.g., from MGF files via `load_from_mgf()`). Apply spectrum_processing() to normalize intensities, remove artifacts, and validate metadata fields such as precursor_mz and collision energy. Extract the precursor m/z (often adjusted by subtracting 1.008 for protonated [M+H]+ ions) to enable subsequent mass-based filtering and library search. The processed spectrum object should retain both the normalized peak intensities and validated metadata for downstream embedding and similarity scoring.

## Related tools

- **matchms** (Load and standardize MS/MS spectra from MGF files; provide Spectrum objects with peak and metadata accessors) — https://matchms.readthedocs.io/en/latest/
- **PyTorch** (Encode preprocessed spectra into normalized tensor representations for contrastive learning) — https://pytorch.org/
- **rdkit** (Validate and extract molecular properties (e.g., mass) for cross-modal alignment with spectrum precursor m/z) — https://rdkit.org/

## Examples

```
spectrum = spectrum_processing(spectrum); query_ms = float(spectrum.metadata['precursor_mz'])-1.008; ms_list=list(load_from_mgf('spectra.mgf'))
```

## Evaluation signals

- Spectrum object retains all required metadata fields (precursor_mz, collision_energy, SMILES or InChI if available)
- Peak intensities are normalized to a consistent scale (e.g., 0–1 or 0–100) with no NaN or infinite values
- Precursor m/z computed as float(spectrum.metadata['precursor_mz'])-1.008 matches expected m/z range for the compound class
- Output spectrum can be successfully passed to model_inference.ms2_encode() without shape or type errors
- Preprocessing reduces noise (removes low-intensity peaks below instrument noise floor) while preserving diagnostic fragment peaks

## Limitations

- Preprocessing quality depends on MGF metadata completeness; missing or malformed precursor_mz or collision energy may compromise downstream retrieval accuracy
- The m/z adjustment (-1.008 for [M+H]+) assumes protonation; non-standard ionization modes (e.g., [M-H]−, [M+Na]+) require alternative adjustments
- Normalization strategy is not explicitly detailed in the README; the choice of intensity scaling (linear, log, square-root) may impact contrastive embedding quality
- No explicit handling of variable-length spectra or missing peak lists documented; edge cases with sparse or empty spectra may cause failures

## Evidence

- [other] Load MS/MS spectrum data and molecular structure datasets (SMILES or SDF format) using matchms and rdkit.: "Load MS/MS spectrum data and molecular structure datasets (SMILES or SDF format) using matchms and rdkit."
- [other] Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric.: "Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric."
- [readme] spectrum = spectrum_processing(spectrum): "spectrum = spectrum_processing(spectrum)"
- [readme] query_ms = float(spectrum.metadata['precursor_mz'])-1.008: "query_ms = float(spectrum.metadata['precursor_mz'])-1.008"
- [readme] ms_list=list(load_from_mgf(".../.mgf")): "ms_list=list(load_from_mgf(".../.mgf"))"
