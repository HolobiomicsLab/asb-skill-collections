---
name: tandem-mass-spectrum-preprocessing-and-normalization
description: Use when you have acquired raw MS/MS spectra (in MGF or mzML format)
  from a mass spectrometry instrument or public repository (e.g., MassIVE, MetaboLights,
  GNPS) that will be used for de novo chemical formula ranking or adduct assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectrum-preprocessing-and-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare raw tandem MS/MS spectra for downstream formula inference by normalizing peak intensities and removing low-intensity noise. This skill is essential before feeding spectra into neural network-based chemical formula ranking models like MIST-CF.

## When to use

Apply this skill when you have acquired raw MS/MS spectra (in MGF or mzML format) from a mass spectrometry instrument or public repository (e.g., MassIVE, MetaboLights, GNPS) that will be used for de novo chemical formula ranking or adduct assignment. Preprocessing is required regardless of ionization mode (positive or negative) before the spectra can be tokenized and passed to the formula transformer architecture.

## When NOT to use

- Do not apply this skill to already-normalized spectra (e.g., if spectra have already been intensity-normalized by your instrument software or an earlier pipeline step) without first inspecting the intensity distribution.
- Do not use a fixed noise threshold across instruments with widely different sensitivity or resolution; instead, calibrate the threshold per instrument class or use a percentile-based approach.
- This skill is not appropriate for preprocessing data that has already been converted into a feature table or vectorized representation; preprocess only raw peak lists.

## Inputs

- Raw tandem MS/MS spectra in MGF format or mzML format
- Spectrum metadata including precursor m/z, precursor charge state, and instrument type
- Noise threshold parameter (e.g., 0.01 for 1% of max intensity)

## Outputs

- Preprocessed MS/MS spectra with normalized intensities and noise-filtered peaks
- Peak lists with m/z and normalized intensity values ready for tokenization
- Optionally: summary statistics (e.g., mean number of peaks per spectrum before/after filtering)

## How to apply

Normalize all peak intensities in each spectrum to a standardized scale (e.g., relative intensity 0–999 or 0–1) to ensure that intensity differences do not bias the model and to improve generalization across instruments with different dynamic ranges. Remove all peaks with intensity below a defined noise threshold (e.g., 1% of the maximum peak intensity in the spectrum) to eliminate chemical noise and reduce the feature dimensionality. Perform these operations uniformly across all spectra in your dataset before adduct tokenization and model input. The exact threshold should be calibrated on your instrument type and sample class, as the README notes that MIST-CF embeds instrument type as a model covariate to account for intensity variations across platforms.

## Related tools

- **MIST-CF** (Downstream formula ranking model that consumes preprocessed spectra; receives noise-filtered peak lists as input to the formula transformer architecture) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Provides sinusoidal formula embeddings used in MIST-CF; referenced for embedding normalization strategies that pair with spectrum preprocessing) — https://arxiv.org/abs/2303.06470
- **SIRIUS** (Used in MIST-CF preprocessing pipeline for generating candidate chemical formulas from m/z; complement to spectrum preprocessing) — https://bio.informatik.uni-jena.de/software/sirius/

## Evaluation signals

- Intensity values in all preprocessed spectra fall within the expected normalized range (e.g., 0–999 or 0–1); no values exceed the chosen scale.
- Peak count per spectrum decreases after noise filtering; verify that >80% of spectra retain at least 3–5 peaks (minimum required for transformer input) after filtering.
- Comparison of top-1, top-5, and top-10 formula ranking accuracy on a validation set before and after preprocessing; preprocessing should not degrade accuracy and may improve it by reducing noise-induced ranking errors.
- Histogram of peak intensities before and after normalization shows a concentrated distribution after normalization and no obvious outliers or bimodal structure.
- Manual inspection of 10–20 representative spectra to confirm that true fragment peaks are retained and only low-intensity noise is removed; verify that the precursor peak (if present in MS/MS) is preserved.

## Limitations

- The optimal noise threshold is instrument- and sample-class-dependent; a fixed threshold applied across heterogeneous data (e.g., high-resolution Orbitrap vs. low-resolution quadrupole) may inadvertently remove true signal or retain excessive noise.
- Normalization to a fixed intensity scale loses absolute intensity information, which may be diagnostically useful for certain metabolite classes or adduct types; downstream models must learn intensity patterns from the training set.
- This skill does not address isotope peak deconvolution, in-source fragmentation, or other advanced mass spectrometry artifacts; it only handles simple noise filtering and intensity normalization.
- The README notes that MIST-CF models trained on NIST20 (commercial library spectra) may be less performant on public NPLIB1 data; preprocessing cannot fully compensate for instrument-specific intensity distributions if the training set was biased toward a particular instrument type.

## Evidence

- [other] Preprocess spectra by normalizing intensity and removing noise below a defined threshold.: "Preprocess spectra by normalizing intensity and removing noise below a defined threshold."
- [intro] MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion instead of computing fragmentation trees: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] Embedding instrument type used to measure the MS/MS as an additional model covariate to help make predictions: "Embedding instrument type used to measure the MS/MS as an additional model covariate to help make predictions"
- [readme] This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)."
- [readme] Four key datasets were used in the process of this paper: 1. biomols: A dataset of biologically relevant molecules that we used to learn a fast filter model 2. NPLIB1: A public natural products dataset extracted from the GNPS database.: "NPLIB1: A public natural products dataset extracted from the GNPS database. NPLIB1 is used for model training and evaluation."
