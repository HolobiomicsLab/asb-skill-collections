---
name: cross-language-function-invocation-and-validation
description: Use when your R-based Spectra analysis workflow requires a specific mass
  spectrometry algorithm (e.g., CosineGreedy similarity scoring, spectral normalization,
  or advanced filtering) that is available only in a Python MS package (matchms, spectrum_utils)
  and not yet in native R.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectriPy
  - R
  - Spectra
  - matchms
  - spectrum_utils
  - reticulate
  techniques:
  - LC-MS
  license_tier: open
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

# Cross-language function invocation and validation

## Summary

Invoke Python mass spectrometry package functions from within R-based Spectra workflows using language-bridging wrappers (e.g., SpectriPy), then validate that the wrapped call executes without error and returns properly typed R-native objects. This skill enables seamless exploitation of Python-only MS algorithms (similarity scoring, filtering, normalization) within R analysis pipelines.

## When to use

Your R-based Spectra analysis workflow requires a specific mass spectrometry algorithm (e.g., CosineGreedy similarity scoring, spectral normalization, or advanced filtering) that is available only in a Python MS package (matchms, spectrum_utils) and not yet in native R. You have a language bridge library (SpectriPy) that wraps Python functionality into R.

## When NOT to use

- The algorithm you need is already implemented natively in R or the Spectra package; use the native R function instead to avoid wrapper overhead.
- Your input data is not already a valid Spectra object; first construct the Spectra object using Spectra() constructor with proper msLevel, mz, and intensity vectors.
- Python dependencies (matchms ≥0.31, spectrum_utils ≥0.3.2, numpy ≥2.2.0, Python ≥3.12) cannot be installed or configured on your system; the wrapper requires automatic or manual Python environment setup via reticulate.

## Inputs

- Spectra object with populated msLevel, precursorMz, mz, and intensity fields
- Parameter object from wrapped Python package (e.g., CosineGreedyParam)
- One or more reference Spectra objects for comparison or processing

## Outputs

- Numeric matrix (e.g., pairwise similarity scores)
- Modified or filtered Spectra object
- Data frame with derived spectral properties
- R-native list containing Python function results

## How to apply

Load the SpectriPy package alongside Spectra in R. Create or load a Spectra object containing your MS2 spectra (with msLevel, precursorMz, mz, and intensity fields populated). Call the corresponding SpectriPy wrapper function (e.g., compareSpectriPy) passing the Spectra object and a parameter object from the wrapped Python package (e.g., CosineGreedyParam with tolerance=0.05). The wrapper automatically converts the Spectra object to the Python representation (matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum), executes the Python function, and converts the result back to an R-native type (numeric matrix, data frame, or modified Spectra). Validate the return type matches the expected schema (e.g., numeric matrix for pairwise similarities) and that dimensions or structure conform to the input.

## Related tools

- **SpectriPy** (R package that wraps Python MS package functions (matchms, spectrum_utils) into R functions and handles bidirectional conversion between Spectra and Python spectral objects) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R package providing efficient in-memory and on-disk storage, subsetting, processing, and comparison of mass spectrometry spectra; serves as the container object passed to SpectriPy wrappers) — https://github.com/RforMassSpectrometry/Spectra
- **matchms** (Python library providing spectral similarity algorithms (CosineGreedy, ModifiedCosine) and normalization; wrapped by SpectriPy for use in R) — https://github.com/matchms
- **spectrum_utils** (Python library for spectral filtering and processing; wrapped by SpectriPy for bidirectional object conversion with R) — https://github.com/bittremieux-lab/spectrum_utils
- **reticulate** (R package that manages Python environment setup, dependency installation via py_require(), and R–Python object marshalling beneath SpectriPy) — https://rstudio.github.io/reticulate

## Examples

```
library(Spectra); library(SpectriPy); caf <- Spectra(DataFrame(msLevel=2L, precursorMz=195.0877, mz=list(c(135.04, 138.06)), intensity=list(c(340, 416)))); res <- compareSpectriPy(caf, caf, param=CosineGreedy(tolerance=0.05))
```

## Evaluation signals

- Function call executes without error (no Python exception or R wrapper failure).
- Return object matches expected type (e.g., numeric matrix for compareSpectriPy, Spectra object for a filter function).
- Return object dimensions conform to input (e.g., similarity matrix rows equal number of query spectra, columns equal number of reference spectra).
- Values in return object fall within chemically plausible ranges (e.g., similarity scores in [0, 1] for normalized algorithms).
- Metadata and spectra variables (precursorMz, name, msLevel) are preserved or correctly mapped back into R Spectra object if returned.

## Limitations

- Python version ≥3.12 and specific Python library versions (matchms 0.31, spectrum_utils 0.3.2, numpy 2.2.0) are required; installation may fail on systems with conflicting Python environments or locked package managers.
- First call to a wrapped function incurs Python initialization overhead, causing latency; subsequent calls within the same R session are faster.
- Large Spectra objects (thousands of spectra) may experience memory overhead during bidirectional object conversion; no guidance provided in README for optimal batch sizes.
- Not all Python MS package functions are wrapped by SpectriPy; only those explicitly implemented (e.g., compareSpectriPy, conversion functions for matchms and spectrum_utils objects) are accessible from R without custom wrapper code.

## Evidence

- [readme] By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R.: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R."
- [other] The workflow calls a Python MS package function through the SpectriPy wrapper layer on the Spectra object and verifies the function executes and returns an R-native object.: "Invoke a Python MS package function through the SpectriPy wrapper layer on the Spectra object. Verify that the function call executes without error and returns an R-native object (e.g., list, data"
- [readme] SpectriPy contains functions to convert between R's Spectra objects and matchms.Spectrum and spectrum_utils.spectrum.MsmsSpectrum objects.: "contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects"
- [readme] compareSpectriPy returns a numeric matrix of similarities and uses parameter objects like CosineGreedy with configurable tolerance.: "compareSpectriPy() returns also a numeric matrix of similarities. Note also that the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be initialized."
- [readme] Python library management uses reticulate's py_require() function to automatically install necessary libraries.: "*SpectriPy*'s Python library management uses the [`py_require()`] function introduced in *reticulate* version 1.41 and should hence work on most system without problems."
