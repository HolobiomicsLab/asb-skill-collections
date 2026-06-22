---
name: peak-intensity-normalization
description: Use when you have raw MS/MS spectral peak lists with absolute intensity values and need to compare spectra using entropy similarity, dot product, or other distance metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - SpectralEntropy
  - MSEntropy
  - spectral_similarity module
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
- This repository contains the original source code for the paper
- These are all integrated into the [MSEntropy package
- These are all integrated into the MSEntropy package (https://github.com/YuanyueLi/MSEntropy)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_entropy_cq
    doi: 10.1038/s41592-021-01331-z
    title: Spectral entropy
  dedup_kept_from: coll_spectral_entropy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01331-z
  all_source_dois:
  - 10.1038/s41592-021-01331-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-intensity-normalization

## Summary

Normalize MS/MS spectral peak intensities to a common scale (typically 0–1 or 0–100%) to enable fair comparison between spectra with different total intensities. This preprocessing step is essential before computing spectral similarity metrics, as it removes the confounding effect of absolute intensity differences and ensures that entropy similarity and other distance metrics depend only on peak distribution patterns.

## When to use

Apply this skill when you have raw MS/MS spectral peak lists with absolute intensity values and need to compare spectra using entropy similarity, dot product, or other distance metrics. Normalization is required before benchmarking spectral similarity methods, as unnormalized intensities introduce bias toward spectra with higher total signal. Use it as a standard preprocessing step in any compound identification workflow using the SpectralEntropy or MSEntropy packages.

## When NOT to use

- Input spectra are already normalized (peak intensities already in [0, 1] or [0, 100] range)
- Your analysis requires preservation of absolute intensity information for quantification or external calibration
- You are comparing spectra from different ionization modes or instruments where intensity scales must be preserved for instrument-specific corrections

## Inputs

- raw MS/MS spectral peak lists (m/z and intensity pairs, one or multiple spectra)
- absolute intensity values (e.g., from .mgf, .msp, .mzML, or .lbm2 files)

## Outputs

- normalized MS/MS spectral peak lists (m/z and normalized intensity pairs, range [0, 1] or [0, 100])
- per-spectrum maximum intensity metadata (for audit and verification)

## How to apply

Load raw MS/MS spectral data containing m/z and intensity pairs. Identify the maximum intensity value within each spectrum. Divide all peak intensities in that spectrum by the maximum intensity value, scaling them to the range [0, 1]. Optionally multiply by 100 to express as a percentage scale [0, 100]. Apply this normalization independently to each spectrum in your dataset—do not normalize across spectra or against a reference library spectrum, as each spectrum is normalized relative to its own maximum. After normalization, verify that the highest intensity peak in each spectrum equals 1.0 (or 100 if percentage-scaled). This normalization is a prerequisite for subsequent noise filtering (e.g., removing peaks <1% of maximum intensity) and for accurate entropy similarity computation.

## Related tools

- **MSEntropy** (Python package that incorporates peak intensity normalization as part of spectral preprocessing before entropy similarity computation) — https://github.com/YuanyueLi/MSEntropy
- **SpectralEntropy** (Original repository containing spectral_similarity and ms_distance modules that operate on normalized spectral peak intensities) — https://github.com/YuanyueLi/SpectralEntropy
- **spectral_similarity module** (Computes entropy similarity and dot product metrics on normalized peak intensity data) — https://github.com/YuanyueLi/SpectralEntropy

## Evaluation signals

- Maximum intensity in each normalized spectrum equals exactly 1.0 (or 100.0 if percentage-scaled); no spectrum has intensity > 1.0
- All peak intensities fall within the expected range [0, 1] or [0, 100]; no negative values or out-of-range outliers
- Entropy similarity scores computed on normalized spectra fall within the expected range [0, 1] and match reference outputs for known spectrum pairs
- Spectral entropy values computed on normalized spectra are reproducible and consistent with published benchmarks
- Peak ranking and relative intensity relationships are preserved—the peak with the highest original intensity remains the highest after normalization

## Limitations

- Normalization does not address potential artifacts in very low-intensity regions; additional noise filtering (e.g., removing peaks <1% of maximum intensity) is recommended after normalization
- For spectra with very weak signals or high noise floors, normalization may amplify baseline noise; consider quality filtering before normalization
- Normalization is independent per spectrum and does not account for batch effects, instrumental drift, or systematic intensity biases across a spectral library; additional calibration may be needed for cross-instrument comparisons

## Evidence

- [other] Before calculating spectral similarity, it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed: "Before calculating spectral similarity, it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton"
- [other] Prepare input MS/MS spectral data by removing spectral noise using the recommended filter of peaks with intensity less than 1% of maximum intensity.: "Prepare input MS/MS spectral data by removing spectral noise using the recommended filter of peaks with intensity less than 1% of maximum intensity."
- [other] The entropy similarity function from the spectral_similarity module computes the similarity score between two preprocessed MS/MS spectra (with noise removed: peaks <1% of maximum intensity filtered).: "Load two preprocessed MS/MS spectra (with noise removed: peaks <1% of maximum intensity filtered) from input files."
- [readme] Spectral entropy is an useful property to measure the complexity of a spectrum. Entropy similarity, which measured spectral similarity based on spectral entropy, has been shown to outperform dot product similarity in compound identification.: "`Entropy similarity`, which measured spectral similarity based on spectral entropy, has been shown to outperform dot product similarity in compound identification."
