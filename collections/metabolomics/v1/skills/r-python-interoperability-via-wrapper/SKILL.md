---
name: r-python-interoperability-via-wrapper
description: Use when you have a Spectra object in R and need to apply a specialized Python MS algorithm (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectriPy
  - R
  - Python
  - Spectra
  - matchms
  - spectrum_utils
  - reticulate
derived_from:
- doi: 10.21105/joss.08070
  title: spectripy
evidence_spans:
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R.
- integration of Python MS packages into a [*Spectra*]-based MS analysis in R
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectripy
    doi: 10.21105/joss.08070
    title: spectripy
  dedup_kept_from: coll_spectripy
schema_version: 0.2.0
---

# R-Python Interoperability via Wrapper

## Summary

SpectriPy wraps Python mass spectrometry package functionality (matchms, spectrum_utils) into R function signatures, enabling seamless invocation of Python MS algorithms within R-based Spectra workflows without manual object marshalling. This skill bridges two ecosystems to leverage Python's specialized MS libraries while remaining in R.

## When to use

You have a Spectra object in R and need to apply a specialized Python MS algorithm (e.g., CosineGreedy similarity scoring, spectral normalization, or peak filtering from matchms or spectrum_utils) that is not natively implemented in R's Spectra package, and you want to avoid switching languages or manually converting data structures.

## When NOT to use

- Your desired MS operation is already available as a native R function in Spectra or related packages (use native functions for better performance and tighter integration).
- Your input data is not in Spectra format and converting it would be prohibitively expensive (consider converting offline or using Python natively).
- You are in a production pipeline that cannot tolerate the overhead of Python environment initialization on the first function call, or your system lacks Python ≥3.12.

## Inputs

- Spectra object (from Spectra::Spectra class with peaks data: mz and intensity vectors, metadata: msLevel, precursorMz, name, id)
- Parameter object from wrapped Python algorithm (e.g., CosineGreedyParam)
- Optional: sample Spectra object for comparative operations (e.g., similarity queries)

## Outputs

- Numeric matrix of pairwise or query-based similarity scores
- Modified Spectra object with processed peaks or metadata
- Data frame or list of algorithm-specific results (e.g., matched peaks, normalized intensities)

## How to apply

Load the SpectriPy package alongside Spectra in R. Create or load your mass spectrometry data as a Spectra object (using DataFrame with msLevel, precursorMz, mz, intensity, and metadata columns). Instantiate a parameter object from the wrapped Python algorithm (e.g., CosineGreedy(tolerance=0.05)) and pass it to the corresponding SpectriPy wrapper function (e.g., compareSpectriPy()). SpectriPy internally converts Spectra objects to Python matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum objects, executes the Python function via reticulate, and returns results as R-native objects (numeric matrices, data frames, or modified Spectra). The first call initializes the Python environment and may take longer; subsequent calls are faster.

## Related tools

- **SpectriPy** (Wrapper layer that translates Python MS package APIs and objects into R function signatures and Spectra-compatible return types; manages reticulate communication and automatic Python dependency installation) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R package providing MS data container and backend infrastructure; SpectriPy converts to/from Spectra objects for seamless R workflow integration) — https://github.com/RforMassSpectrometry/Spectra
- **matchms** (Python library providing specialized MS algorithms (spectral similarity, peak matching, normalization) that SpectriPy wraps for use in R) — https://github.com/matchms
- **spectrum_utils** (Python library providing MS spectrum processing utilities (filtering, peak detection); SpectriPy converts between R Spectra and spectrum_utils.spectrum.MsmsSpectrum objects) — https://github.com/bittremieux-lab/spectrum_utils
- **reticulate** (R package that manages Python environment setup, function invocation, and bidirectional object conversion; SpectriPy relies on reticulate v1.41+ for automatic Python library installation via py_require()) — https://rstudio.github.io/reticulate

## Examples

```
library(Spectra); library(SpectriPy); caf <- Spectra(DataFrame(msLevel=2L, precursorMz=195.0877, mz=list(c(135.04, 138.06, 163.04, 195.09)), intensity=list(c(340, 416, 2580, 412)))); res <- compareSpectriPy(caf, caf, param=CosineGreedy(tolerance=0.05))
```

## Evaluation signals

- Wrapper function executes without error and reticulate successfully initializes the Python environment on first call.
- Return object matches expected structure: for compareSpectriPy(), a numeric matrix of similarity scores with correct dimensions (rows = query spectra, columns = library spectra).
- Data type conversion is bidirectional and lossless: Spectra → Python object → result → R object; verify that precursorMz, mz, intensity, and metadata (name, id) are correctly represented in the intermediate Python objects by spot-checking a few conversions.
- Parameter customization propagates correctly: changing CosineGreedy tolerance from default 0.1 to 0.05 produces measurably different (tighter) similarity scores on the same spectrum pair.
- Cross-language error handling: invalid inputs (e.g., empty Spectra, mismatched precursor m/z types) produce informative R error messages, not silent Python crashes or type coercion artifacts.

## Limitations

- Requires Python ≥3.12 installed on the system; SpectriPy does not bundle Python, and environment configuration via RETICULATE_PYTHON or RETICULATE_PYTHON_ENV environment variables requires manual installation of all Python dependencies (matchms 0.31, spectrum_utils 0.3.2, numpy 2.2.0) if automatic py_require() installation is disabled.
- First invocation of a SpectriPy function incurs Python environment initialization overhead (slower than subsequent calls); not suitable for low-latency interactive use cases requiring <100 ms response times.
- Bidirectional object conversion is limited to matchms.Spectrum and spectrum_utils.spectrum.MsmsSpectrum classes; Python libraries outside this set cannot be wrapped without additional code.
- Performance on very large Spectra objects (>100,000 spectra) may be constrained by data marshalling overhead; the package is optimized for moderate datasets typical of targeted MS/MS analysis, not discovery-scale proteomics.

## Evidence

- [readme] The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R.: "The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R."
- [readme] By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R.: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R."
- [readme] SpectriPy can leverage the spectral similarity, filtering, normalization calculations from the Python matchms library and contains functions to convert between R's Spectra::Spectra objects and matchms.Spectrum and spectrum_utils.spectrum.MsmsSpectrum objects.: "SpectriPy can leverage the spectral similarity, filtering, normalization etc. calculations from the Python [*matchms*](https://github.com/matchms) library and contains functions to convert between"
- [readme] *SpectriPy*'s Python library management uses the py_require() function introduced in *reticulate* version 1.41 and should hence work on most systems without problems.: "*SpectriPy*'s Python library management uses the [`py_require()`](https://rstudio.github.io/reticulate/reference/py_require.html) function introduced in *reticulate* version 1.41 and should hence"
- [readme] compareSpectriPy() performs spectra similarity calculations using the scoring functions from MS Python packages, returning a numeric matrix of similarities.: "As a result `compareSpectriPy()` returns also a numeric matrix of similarities. Note also that the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be"
