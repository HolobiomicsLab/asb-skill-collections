---
name: data-marshalling-and-type-conversion
description: Use when you have Spectra::Spectra objects in R and need to apply Python
  MS algorithms from matchms or spectrum_utils (e.g., CosineGreedy similarity scoring,
  normalization, or filtering), or conversely need to convert Python spectral objects
  back to R for downstream Spectra workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3211
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectriPy
  - R
  - Spectra
  - reticulate
  - matchms
  - spectrum_utils
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.21105/joss.08070
  title: spectripy
evidence_spans:
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based
  MS analysis in R
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based
  MS analysis in R.
- integration of Python MS packages into a [*Spectra*]-based MS analysis in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectripy
    doi: 10.21105/joss.08070
    title: spectripy
  dedup_kept_from: coll_spectripy
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.08070
  all_source_dois:
  - 10.21105/joss.08070
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-marshalling-and-type-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert mass spectrometry spectral objects between R Spectra::Spectra and Python matchms/spectrum_utils representations, marshalling data across language boundaries while preserving spectral metadata and peak m/z–intensity pairs. This enables seamless execution of Python-based MS algorithms within R workflows.

## When to use

You have Spectra::Spectra objects in R and need to apply Python MS algorithms from matchms or spectrum_utils (e.g., CosineGreedy similarity scoring, normalization, or filtering), or conversely need to convert Python spectral objects back to R for downstream Spectra workflows. Use this skill when a single analytical pipeline spans both R and Python environments and type fidelity across the language boundary is critical.

## When NOT to use

- All analysis can be completed entirely within R using Spectra's built-in compareSpectra() or other native functions — marshalling incurs setup overhead.
- Python spectral objects are already available in the Python environment and do not need to be consumed by R code — skip conversion.
- Input spectra lack essential fields (mz, intensity, precursorMz) required for matchms or spectrum_utils objects, or metadata is heterogeneous and not fully representable in the target language's object model.

## Inputs

- Spectra::Spectra object (R) with msLevel, mz list, intensity list, precursorMz, and optional metadata fields (name, id)
- matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum object (Python)
- Parameter objects from matchms (e.g., CosineGreedy) specifying similarity metric configuration

## Outputs

- Converted Python object (matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum) ready for Python library functions
- Converted Spectra::Spectra object (R) or numeric similarity matrix from Python scoring functions
- Numeric matrix of pairwise similarities or scalar scores from Python algorithms

## How to apply

Use SpectriPy's built-in conversion functions to translate between Spectra::Spectra objects and matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum objects. The reticulate package manages the R–Python interface automatically; the conversion preserves m/z, intensity, precursor m/z, and metadata fields (name, id, msLevel). Pass the converted Python object to the target Python function (e.g., CosineGreedy for similarity calculation), then marshal the result back to an R matrix or Spectra object. Validate that all spectral variables (precursor m/z, fragments, metadata) round-trip correctly and that similarity/scoring metrics align between R and Python implementations when both provide the same algorithm.

## Related tools

- **SpectriPy** (Provides R function wrappers and conversion methods (e.g., for translating Spectra::Spectra ↔ matchms.Spectrum) and orchestrates compareSpectriPy() for cross-language similarity scoring) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (Source and sink for spectral data in R; defines the Spectra::Spectra S4 class and backends used as input to SpectriPy conversion) — https://github.com/RforMassSpectrometry/Spectra
- **reticulate** (Manages R–Python process-level data interchange, including object serialization and function calls; SpectriPy's py_require() dependency ensures automatic Python library installation)
- **matchms** (Python library providing Spectrum objects and similarity scoring algorithms (e.g., CosineGreedy) that accept converted spectral data and return numeric scores) — https://github.com/matchms
- **spectrum_utils** (Python library providing MsmsSpectrum objects and normalization/filtering methods; SpectriPy converts to/from this class for advanced peak processing) — https://github.com/bittremieux-lab/spectrum_utils

## Examples

```
res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))
```

## Evaluation signals

- Converted Spectra::Spectra → matchms.Spectrum → Spectra::Spectra round-trip preserves m/z, intensity pairs and all metadata fields with no data loss or truncation.
- Similarity scores from compareSpectriPy() using matchms.CosineGreedy match expected values when validated against matchms direct Python calls or published reference datasets.
- Precursor m/z, msLevel, and optional metadata (name, id) are correctly mapped and accessible in converted Python objects; conversely, Python object fields map back to proper Spectra variable columns.
- Type conversion (numeric precision, array lengths, string encoding) produces valid inputs to matchms/spectrum_utils functions without errors or warnings; Python functions execute without crashes.
- Similarity matrix dimensions are correct (n_query × n_subject), and edge cases (single spectrum, identical spectra, empty peaks) are handled gracefully without segfaults or NaN propagation.

## Limitations

- Python version ≥ 3.12 and specific versions of matchms (0.31), spectrum_utils (0.3.2), and numpy (2.2.0) must be installed; version mismatches may cause conversion failures or silent data loss.
- First compareSpectriPy() call incurs Python initialization overhead; subsequent calls are faster but still carry reticulate serialization cost for large spectral datasets.
- Custom or non-standard spectral variables in Spectra objects may not convert to matchms/spectrum_utils and will be silently dropped; only standard fields (mz, intensity, precursorMz, msLevel, name, id) are guaranteed to round-trip.
- Floating-point precision differences between R and Python (e.g., m/z values at >6 decimal places) may accumulate during conversion; tolerance parameters in similarity functions (e.g., tolerance=0.05 in CosineGreedy) must account for this.

## Evidence

- [readme] SpectriPy enables seamless conversion between Spectra and Python spectral objects: "contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects"
- [readme] Marshalling preserves spectral data integrity across the language boundary: "R and Python spectral objects are easily translated and available in one workflow"
- [readme] Conversion is orchestrated by wrapper functions that hide reticulate complexity: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R"
- [readme] Type conversion supports similarity scoring via parameter objects from matchms: "provides the `compareSpectriPy()` function that allows to perform spectra similarity calculations using the scoring functions from MS Python packages"
- [readme] Python library management and dependency installation is automated via reticulate: "All necessary Python libraries (listed below) are automatically installed by the [*reticulate*](https://rstudio.github.io/reticulate) R package"
