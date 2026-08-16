---
name: mass-spectrometry-wrapper-function-design
description: Use when when you have a Spectra-based MS analysis workflow in R but need access to specialized spectral similarity, filtering, or normalization algorithms available only in Python libraries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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
derived_from:
- doi: 10.21105/joss.08070
  title: spectripy
evidence_spans:
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R
- MS analysis in R. By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectripy_cq
    doi: 10.21105/joss.08070
    title: spectripy
  dedup_kept_from: coll_spectripy_cq
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

# Mass Spectrometry Wrapper Function Design

## Summary

Design and implement R functions that wrap Python mass spectrometry library functionality to enable seamless cross-language integration of spectral analysis workflows. This skill enables reuse of specialized Python MS packages (e.g., matchms, spectrum_utils) within R-based Spectra objects without reimplementing algorithms.

## When to use

When you have a Spectra-based MS analysis workflow in R but need access to specialized spectral similarity, filtering, or normalization algorithms available only in Python libraries. Specifically when you want to leverage Python packages like matchms or spectrum_utils while maintaining R's Spectra object format and avoiding full reimplementation of algorithms.

## When NOT to use

- Input spectra are already in Python format and do not need to be converted back to R Spectra objects; use Python libraries directly instead.
- The required Python MS library (matchms, spectrum_utils) is not available and cannot be installed via reticulate's py_require().
- Latency-critical workflows where Python environment initialization overhead or serialization cost is prohibitive.

## Inputs

- Spectra object (R S4 object with MS spectra data)
- Python MS library function parameters (e.g., tolerance, algorithm selection)

## Outputs

- Numeric similarity matrix (or modified Spectra object with computed attributes)
- Spectra object with preserved metadata and attributes

## How to apply

Design an R function that accepts a Spectra object as input. Use the reticulate R package to serialize the Spectra object and pass it to a Python MS package routine via a cross-language interface. Execute the Python routine on the passed data using appropriate Python library functions (e.g., CosineGreedy from matchms with configurable parameters like tolerance). Deserialize the result back into an R-native format and return it as a Spectra object with all expected attributes preserved. The wrapper should handle Python environment initialization (via py_require() in reticulate ≥1.41) and manage bidirectional translation between R's Spectra::Spectra objects and Python equivalents (matchms.Spectrum, spectrum_utils.spectrum.MsmsSpectrum).

## Related tools

- **SpectriPy** (R package that provides wrapper functions (compareSpectriPy) and conversion utilities to call Python MS functions on Spectra objects) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R S4 infrastructure for storing and managing MS spectra objects; data format passed to and returned from wrapper functions) — https://github.com/RforMassSpectrometry/Spectra
- **reticulate** (R package providing cross-language interface for serialization, Python environment setup (py_require), and bidirectional object translation) — https://rstudio.github.io/reticulate
- **matchms** (Python library providing spectral similarity algorithms (CosineGreedy, etc.) wrapped via SpectriPy) — https://github.com/matchms
- **spectrum_utils** (Python library providing spectral filtering and normalization; objects (MsmsSpectrum) converted to/from Spectra format) — https://github.com/bittremieux-lab/spectrum_utils

## Examples

```
library(Spectra); library(SpectriPy); all <- c(caf, mhd); res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))
```

## Evaluation signals

- Returned object is a valid Spectra object with expected attributes (msLevel, precursorMz, mz, intensity) preserved and unchanged
- Numeric output (e.g., similarity matrix) has dimensions matching the input Spectra object (n_query × n_reference)
- Values returned from Python function match manual verification using native Python library call on same input data
- Python environment initializes without error on first invocation and required libraries (matchms ≥0.31, spectrum_utils ≥0.3.2, numpy ≥2.2.0) are available
- Round-trip conversion (Spectra → Python → Spectra) preserves m/z and intensity values within numerical precision (floating-point tolerance)

## Limitations

- Requires Python ≥3.12 installed on system; SpectriPy cannot be used in environments restricted to R-only execution.
- Serialization and deserialization overhead makes wrapper functions slower than native R implementations for small spectral datasets; most suitable when leveraging complex Python algorithms unavailable in R.
- Manual Python library installation required if RETICULATE_PYTHON or RETICULATE_PYTHON_ENV environment variables are set; automatic dependency resolution via py_require() does not apply in those cases.
- No changelog available in repository, limiting reproducibility and version-tracking for wrapper function behavior across releases.

## Evidence

- [intro] SpectriPy integrates Python functionality into R-based workflows: "The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R"
- [other] Wrapper functions serialize Spectra, execute Python routines, and deserialize results: "Use SpectriPy's cross-language interface to serialize the Spectra object and pass it to a Python MS package routine. Execute the Python routine on the passed data. Deserialize the result and return"
- [readme] Python objects must be converted to/from Spectra format: "contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects"
- [readme] reticulate py_require() enables automatic dependency management: "*SpectriPy*'s Python library management uses the [`py_require()`](https://rstudio.github.io/reticulate/reference/py_require.html) function introduced in *reticulate* version 1.41"
- [readme] Wrapper functions return numeric similarity matrices or Spectra objects: "As a result `compareSpectriPy()` returns also a numeric matrix of similarities"
- [readme] Round-trip conversion enables bidirectional workflow: "R and Python spectral objects are easily translated and available in one workflow (i.e., a quarto document), enabling the advanced user or developer to create custom functions"
