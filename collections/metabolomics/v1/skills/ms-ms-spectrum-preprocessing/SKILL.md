---
name: ms-ms-spectrum-preprocessing
description: Use when you have raw MS/MS spectra (in MGF or mzML format) with unscaled peak intensities and noise artifacts, and you plan to rank chemical formulas, predict adducts, or score precursor–spectrum agreement using a machine learning model such as MIST-CF.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
---

# MS/MS Spectrum Preprocessing

## Summary

Normalize MS/MS spectrum intensities and filter noise from tandem mass spectra prior to chemical formula or adduct ranking. This prepares raw spectral data for downstream neural network-based scoring or fragmentation analysis.

## When to use

Apply this skill when you have raw MS/MS spectra (in MGF or mzML format) with unscaled peak intensities and noise artifacts, and you plan to rank chemical formulas, predict adducts, or score precursor–spectrum agreement using a machine learning model such as MIST-CF. Skip this skill only if spectra have already been normalized and noise-filtered upstream.

## When NOT to use

- Spectra have already been normalized and filtered by an upstream preprocessing step (e.g., vendor software or GNPS); applying this skill again may introduce double-normalization artifacts.
- Your analysis requires preservation of absolute intensity information for quantification; normalization will destroy this signal.
- Input spectra are from a database (e.g., NIST20, GNPS) that has already been preprocessed and validated; use the library spectra directly.

## Inputs

- Raw MS/MS spectra in MGF (Mascot Generic Format) or mzML file format
- Precursor m/z values associated with each spectrum
- Ground-truth chemical formula and adduct annotations (optional, for evaluation)

## Outputs

- Normalized MS/MS spectra (intensity-scaled and noise-filtered)
- Extracted precursor m/z values
- Preprocessing metadata (normalization method, filtering thresholds used)

## How to apply

Load raw MS/MS spectra from an MGF or mzML file and extract the m/z and intensity arrays for each spectrum. Normalize intensities by dividing by the maximum intensity per spectrum (or using other scaling methods such as square-root or log transformation), then apply noise filtering—remove peaks below a signal-to-noise threshold or absolute intensity cutoff. Extract and record the precursor m/z value for each spectrum, as it is required for downstream formula candidate generation and adduct assignment. Document the normalization and filtering parameters (e.g., SNR threshold, minimum absolute intensity) used so they can be consistently applied to validation or test data.

## Related tools

- **MIST-CF** (Downstream neural network model that scores normalized spectra against chemical formula and adduct candidates) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Baseline tool for generating chemical formula candidates from m/z values (used to compare against MIST-CF predictions after preprocessing)) — https://bio.informatik.uni-jena.de/software/sirius/

## Evaluation signals

- Verify that all spectra have maximum intensity = 1.0 (or the chosen normalization ceiling) and that no peak exceeds this value.
- Check that precursor m/z values are correctly extracted and stored (e.g., lie within the expected mass range for the instrument).
- Confirm that low-intensity noise peaks have been removed by comparing peak counts before and after filtering; document the SNR threshold or absolute intensity cutoff used.
- Run a sample of preprocessed spectra through the downstream MIST-CF model and confirm that predictions (top-k formula and adduct ranks) are generated without errors.
- Compare preprocessing parameters (normalization method, noise threshold) across all spectra in a batch to ensure consistency; any variation should be documented in the preprocessing metadata.

## Limitations

- Normalization discards absolute intensity information, which may be valuable for downstream quantification or machine learning models sensitive to intensity magnitudes.
- Noise filtering thresholds (SNR, absolute intensity cutoff) are dataset- and instrument-dependent; thresholds optimized for Orbitrap data may not transfer to lower-resolution quadrupole or time-of-flight instruments.
- Simple max-intensity normalization does not account for spectral baseline drift or detector saturation; more sophisticated preprocessing (e.g., baseline subtraction, robust scaling) may be required for challenging datasets.
- The article notes that MIST-CF models trained on NIST20 (higher resolution) data 'may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)', suggesting that preprocessing choices affect downstream model generalization.

## Evidence

- [other] Preprocess MS/MS spectra (normalize intensities, filter noise) and extract precursor m/z values.: "Preprocess MS/MS spectra (normalize intensities, filter noise) and extract precursor m/z values."
- [other] Load benchmark MS/MS dataset containing unknown spectra and ground-truth chemical formulas.: "Load benchmark MS/MS dataset containing unknown spectra and ground-truth chemical formulas."
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach"
- [readme] This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)."
