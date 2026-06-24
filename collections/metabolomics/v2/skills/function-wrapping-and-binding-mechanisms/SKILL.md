---
name: function-wrapping-and-binding-mechanisms
description: Use when when you have Spectra objects in R and need to apply Python
  MS library functionality (spectral similarity scoring, filtering, normalization)
  without leaving the R environment, or when you want to create custom hybrid workflows
  that leverage both R and Python MS packages within a single.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectriPy
  - R
  - reticulate
  - Spectra
  - matchms
  - spectrum_utils
  techniques:
  - LC-MS
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

# function-wrapping-and-binding-mechanisms

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A cross-language binding technique that wraps Python mass spectrometry library functions (e.g., matchms, spectrum_utils) as callable R functions within the Spectra object model, enabling seamless data interchange and interoperability between R and Python analysis workflows in a single process.

## When to use

When you have Spectra objects in R and need to apply Python MS library functionality (spectral similarity scoring, filtering, normalization) without leaving the R environment, or when you want to create custom hybrid workflows that leverage both R and Python MS packages within a single quarto document or analysis session.

## When NOT to use

- Python is not installed on the system or required Python libraries (matchms, spectrum_utils) cannot be installed via py_require().
- The analysis must execute in isolation or in a system where R and Python processes cannot share memory (e.g., separate Docker containers without IPC).
- The target Python MS library API is unstable or lacks type-stable output (making result marshalling unpredictable).

## Inputs

- Spectra object (R; collection of MS2 spectra with m/z and intensity vectors)
- Python MS library function specification (library name, function name, parameter schema)
- Scalar or vector parameters for the Python function (e.g., tolerance value, algorithm variant)

## Outputs

- Numeric matrix (similarity scores or computed metrics)
- Spectra object (filtered or transformed spectra)
- List or data.frame of results compatible with R Spectra workflows

## How to apply

Use the reticulate R package (version ≥ 1.41) and its py_require() function to automatically manage Python library dependencies (matchms ≥ 0.31, spectrum_utils ≥ 0.3.2, numpy ≥ 2.2.0). Construct wrapper functions that (1) convert R Spectra objects to Python matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum objects, (2) invoke the Python library's API methods with the converted objects and desired parameters (e.g., tolerance thresholds for similarity scoring), (3) marshal the results (numeric matrices, filtered spectra lists) back to R data structures compatible with Spectra. Validate that Python setup initializes correctly on first call (which may incur latency) and that wrapped function signatures match the Spectra comparison interface (e.g., compareSpectriPy returns a numeric similarity matrix).

## Related tools

- **reticulate** (R package providing in-process R-to-Python function binding and data marshalling; manages Python environment initialization and library installation via py_require()) — https://rstudio.github.io/reticulate
- **SpectriPy** (R package implementing the wrapper layer; provides compareSpectriPy() and conversion functions (Spectra ↔ matchms.Spectrum / MsmsSpectrum) and parameter classes (CosineGreedyParam)) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R package providing the MS spectra object model and comparison interface into which wrapped Python functions integrate) — https://github.com/RforMassSpectrometry/Spectra
- **matchms** (Python library providing spectral similarity scoring functions (CosineGreedy, ModifiedCosine) and spectral processing operations wrapped and exposed via SpectriPy) — https://github.com/matchms
- **spectrum_utils** (Python library providing MsmsSpectrum class and normalization/filtering operations; objects converted to/from R Spectra via SpectriPy) — https://github.com/bittremieux-lab/spectrum_utils

## Examples

```
library(Spectra); library(SpectriPy); res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))
```

## Evaluation signals

- Wrapped function executes without error on representative Spectra objects and returns expected output type (numeric matrix for similarity, Spectra object for filtering).
- Cross-language type conversion is verified: R Spectra object is successfully converted to matchms.Spectrum/MsmsSpectrum, processed, and converted back; intermediate Python objects are instantiated and destroyed cleanly.
- Numerical results match or are consistent with direct Python library invocation on equivalent data (e.g., CosineGreedy similarity scores computed in R via SpectriPy match scores from native Python matchms call).
- Error handling and type mismatches between R and Python inputs are caught and reported with informative messages (e.g., mismatched vector lengths, unsupported parameter values).
- Performance: first call incurs Python environment initialization latency; subsequent calls execute without re-initialization overhead.

## Limitations

- Requires Python ≥ 3.12 installed on the system; automatic library installation via py_require() may fail in restricted or offline environments, requiring manual installation and environment variable configuration (RETICULATE_PYTHON or RETICULATE_PYTHON_ENV).
- First invocation of a wrapped function incurs latency due to Python interpreter initialization and module loading; unsuitable for real-time or ultra-low-latency applications.
- Data conversion between R and Python (e.g., large m/z/intensity vectors) involves memory allocation and serialization overhead; not optimized for streaming or extremely large spectral datasets.
- Wrapper correctness depends on stable Python library APIs; breaking changes in matchms or spectrum_utils versions may require re-wrapping or parameter adjustment.

## Evidence

- [readme] wrapping Python functionality into R functions enables seamless integration: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R"
- [readme] matchms and spectrum_utils are the target Python libraries for conversion: "contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects from the Python [*matchms*](https://github.com/matchms)"
- [readme] reticulate and py_require manage Python dependency installation: "*SpectriPy*'s Python library management uses the [`py_require()`](https://rstudio.github.io/reticulate/reference/py_require.html) function introduced in *reticulate* version 1.41 and should hence"
- [readme] Similarity comparison returns a numeric matrix: "As a result `compareSpectriPy()` returns also a numeric matrix of similarities"
- [readme] First call incurs initialization latency: "Note also that the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be initialized"
