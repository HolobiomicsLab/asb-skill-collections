---
name: spectral-workflow-validation
description: Use when after implementing or modifying a cross-language integration layer that wraps Python mass spectrometry functions (e.g., spectral matching, peak detection, normalization from matchms or spectrum_utils) as R-callable functions within Spectra workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
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
derived_from:
- doi: 10.21105/joss.08070
  title: spectripy
evidence_spans:
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R.
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
---

# spectral-workflow-validation

## Summary

Verify that cross-language wrapped spectral analysis functions (Python MS libraries integrated into R via reticulate) execute correctly and return expected data structures when invoked from R Spectra workflows. This skill ensures type conversion, error handling, and data marshalling work as intended across R–Python process boundaries.

## When to use

After implementing or modifying a cross-language integration layer that wraps Python mass spectrometry functions (e.g., spectral matching, peak detection, normalization from matchms or spectrum_utils) as R-callable functions within Spectra workflows. Validate before deploying wrapped functions to production pipelines or publishing integration code.

## When NOT to use

- Input already consists of pre-computed similarity scores or processed results—no conversion or function invocation is needed.
- Wrapping layer is being designed for the first time; use this skill only after the wrapper architecture (reticulate bindings, object marshalling protocol) is already implemented.
- Testing single-language (R-only or Python-only) mass spectrometry pipelines without cross-language boundaries.

## Inputs

- R Spectra object(s) with MS/MS spectral data (mz, intensity, precursor m/z, metadata)
- Python parameter objects (e.g., CosineGreedyParam, normalization settings)
- Test spectra with known reference results or manual ground truth

## Outputs

- Numeric similarity matrix (Spectra::compareSpectra format)
- Boolean vector indicating successful conversion and execution
- Error log or validation report documenting type conversions and parameter propagation
- Converted Spectra objects round-tripped through Python and back to R

## How to apply

Execute representative MS operations (e.g., CosineGreedy spectral similarity, peak filtering, spectrum normalization) using the wrapped Python functions on small, well-characterized test spectra with known ground-truth results. Verify that: (1) wrapped functions return numeric matrices or Spectra objects of correct shape and type; (2) tolerance and parameter values passed from R (e.g., tolerance=0.05 for CosineGreedy) propagate correctly to Python; (3) R Spectra objects successfully convert to Python matchms.Spectrum or spectrum_utils.MsmsSpectrum objects and back without data loss; (4) error messages from Python operations surface appropriately in R; (5) cross-language type conversions (e.g., R numeric vectors to Python numpy arrays, R lists to Python dicts) preserve precision and structure. Use the reticulate package's integration hooks to monitor object instantiation and result marshalling.

## Related tools

- **SpectriPy** (Primary integration layer wrapping Python MS functions (matchms, spectrum_utils) as R callables in Spectra workflows) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R infrastructure for storing, handling, and comparing MS spectra objects; hosts wrapped Python functions as methods) — https://github.com/RforMassSpectrometry/Spectra
- **reticulate** (R package managing Python environment, object conversion, and cross-language function calls; enables py_require() and environment variable configuration) — https://rstudio.github.io/reticulate
- **matchms** (Python library providing spectral similarity metrics (CosineGreedy, CosineHungarian, etc.) and spectrum object definitions wrapped by SpectriPy) — https://github.com/matchms
- **spectrum_utils** (Python library providing spectrum objects (MsmsSpectrum) and normalization/filtering functions convertible to/from R Spectra) — https://github.com/bittremieux-lab/spectrum_utils

## Examples

```
res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))
if (is.matrix(res) && nrow(res) == length(all) && ncol(res) == length(caf)) { cat('Validation passed\n') }
```

## Evaluation signals

- Similarity matrix returned by compareSpectriPy() has correct dimensions (n_query × n_library) and numeric values in [0, 1] range for cosine-based metrics.
- Tolerance and other parameters (e.g., tolerance=0.05) passed to CosineGreedyParam in R produce numerically identical results to calling the same Python function directly with the same parameters.
- R Spectra objects with mz, intensity, precursorMz, and metadata convert to Python matchms.Spectrum or spectrum_utils.MsmsSpectrum objects with no data loss; round-trip conversion (R→Python→R) yields identical or near-identical spectra within floating-point precision.
- Python exceptions (e.g., invalid parameter values, malformed spectra) are caught and re-raised as R errors with informative messages and call stacks.
- Test spectra with manually verified ground-truth similarity scores (e.g., caffeine–caffeine = 1.0, caffeine–1-methylhistidine < 0.5) match wrapped function outputs within a small tolerance (e.g., ±0.01).

## Limitations

- Initial SpectriPy setup and first Python function call incur overhead (Python environment initialization via reticulate); subsequent calls are faster but still cross-language boundary.
- Python version ≥3.12 and specific dependency versions (matchms 0.31, spectrum_utils 0.3.2, numpy 2.2.0) must be installed; manual installation or RETICULATE_PYTHON environment variable configuration required if automatic py_require() fails.
- Floating-point precision and rounding behavior may differ slightly between R and Python implementations of the same algorithm; exact bit-for-bit equivalence not guaranteed.
- Large spectral libraries (many thousands of spectra) may encounter memory constraints during conversion or comparison due to object duplication across R and Python processes within the same process space.

## Evidence

- [intro] By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R"
- [other] SpectriPy operates by wrapping Python functionality into R functions, thereby enabling seamless integration of Python libraries into R-based Spectra mass spectrometry analysis.: "SpectriPy operates by wrapping Python functionality into R functions, thereby enabling seamless integration of Python libraries into R-based Spectra mass spectrometry analysis."
- [other] Map the integration layer's architecture showing how Python objects are instantiated, called, and their results marshalled back to R.: "Map the integration layer's architecture showing how Python objects are instantiated, called, and their results marshalled back to R."
- [other] Verify cross-language type conversion and error handling for representative MS operations (e.g., spectral matching, peak detection).: "Verify cross-language type conversion and error handling for representative MS operations (e.g., spectral matching, peak detection)."
- [readme] *SpectriPy* can leverage the spectral similarity, filtering, normalization etc. calculations from the Python [*matchms*](https://github.com/matchms) library and contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects: "functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects"
- [readme] All necessary Python libraries (listed below) are automatically installed by the [*reticulate*](https://rstudio.github.io/reticulate) R package. *SpectriPy*'s Python library management uses the [`py_require()`](https://rstudio.github.io/reticulate/reference/py_require.html) function: "All necessary Python libraries are automatically installed by the [*reticulate*](https://rstudio.github.io/reticulate) R package."
- [readme] Note also that the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be initialized.: "the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be initialized."
- [readme] We calculate the similarity using the *CosineGreedy* function from *matchms*, changing the `tolerance` to a value of `0.05` (instead of the default `0.1`).: "We calculate the similarity using the *CosineGreedy* function from *matchms*, changing the `tolerance` to a value of `0.05`"
- [readme] As a result `compareSpectriPy()` returns also a numeric matrix of similarities.: "`compareSpectriPy()` returns also a numeric matrix of similarities."
