---
name: cross-language-interface-design
description: Use when when you have domain-specific functionality (e.g., spectral
  similarity scoring, peak detection algorithms) implemented in one language (Python)
  but need to make it callable and composable within an R-based analytical pipeline
  (Spectra objects);
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SpectriPy
  - R
  - reticulate
  - Spectra
  - matchms
  - spectrum_utils
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# cross-language-interface-design

## Summary

Design and implement function wrapping and object marshalling layers that translate APIs between compiled/interpreted languages (Python ↔ R) while preserving type semantics and enabling seamless execution within unified analytical workflows. This skill is essential when integrating specialized libraries from one language ecosystem into another without forcing users to switch execution contexts.

## When to use

When you have domain-specific functionality (e.g., spectral similarity scoring, peak detection algorithms) implemented in one language (Python) but need to make it callable and composable within an R-based analytical pipeline (Spectra objects); when end-users should not be aware of the language boundary; and when bidirectional object translation (R ↔ Python) must happen transparently within the same R session.

## When NOT to use

- The Python functionality is already fully accessible via established bindings or REST APIs in R (e.g., via BiocManager or CRAN) — reimplement wrapping only if no maintained bridge exists.
- The R and Python components must run in separate processes or on different machines — this skill assumes same-process execution via reticulate.
- Performance-critical inner loops require sub-millisecond latency; the overhead of repeated cross-language calls may be prohibitive.

## Inputs

- R Spectra objects (mass spectrometry spectral data with mz, intensity, and metadata)
- Python library APIs (matchms, spectrum_utils, numpy)
- Function signatures and class definitions from target Python packages
- Parameter specifications and tolerance thresholds (e.g., cosine similarity tolerance)

## Outputs

- R wrapper functions with signatures compatible with Spectra workflows
- Bidirectional conversion functions (R ↔ Python object translation)
- Numeric matrices of similarity scores or processed Spectra objects
- Error messages and validation reports confirming type preservation across boundary

## How to apply

First, identify the Python library's core API signatures and object models (e.g., matchms.Spectrum, spectrum_utils.spectrum.MsmsSpectrum). Second, design R wrapper functions that map Spectra objects to their Python equivalents using a marshalling layer (reticulate's py_require() for automatic dependency resolution). Third, implement bidirectional conversion functions that translate R DataFrames and lists into Python class instances and vice versa, preserving m/z arrays, intensity arrays, and metadata. Fourth, define tolerance parameters (e.g., CosineGreedy tolerance=0.05) as R function arguments that propagate into Python function calls. Fifth, ensure error handling is language-agnostic and that results (similarity matrices, filtered spectra) are returned in R-native structures (matrices, Spectra objects). Validate with representative MS operations (spectral matching, peak detection) on both synthetic and real spectra to confirm round-trip fidelity.

## Related tools

- **reticulate** (Cross-language bridge enabling R-to-Python object instantiation, function calls, and automatic dependency management via py_require()) — https://rstudio.github.io/reticulate
- **SpectriPy** (Concrete R package implementing the wrapping pattern, providing compareSpectriPy() and conversion functions for matchms/spectrum_utils) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R-side container for MS spectral data that SpectriPy wraps for Python library integration) — https://github.com/RforMassSpectrometry/Spectra
- **matchms** (Python library providing spectral similarity algorithms (CosineGreedy, ModifiedCosine) that are wrapped by SpectriPy) — https://github.com/matchms
- **spectrum_utils** (Python library providing spectral normalization and filtering; its MsmsSpectrum objects are translated to/from R Spectra) — https://github.com/bittremieux-lab/spectrum_utils

## Examples

```
library(Spectra); library(SpectriPy); all <- c(caf, mhd); res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))
```

## Evaluation signals

- Wrapped Python functions execute without errors when called from R and accept Spectra objects or DataFrames as arguments.
- Return values (e.g., similarity matrices from CosineGreedy, normalized Spectra) match expected data types and dimensions; matrices are numeric, Spectra objects retain all original metadata.
- Round-trip conversion (R Spectra → Python MsmsSpectrum → R Spectra) preserves m/z arrays, intensity arrays, precursor m/z, and metadata fields exactly or within expected floating-point tolerance.
- Parameter passing (e.g., tolerance=0.05 in CosineGreedy) correctly propagates from R function signature to Python function call and influences output (e.g., similarity scores differ when tolerance changes).
- Error handling from Python (e.g., type mismatches, invalid m/z ranges) is caught and re-raised in R with intelligible messages.

## Limitations

- Requires Python ≥3.12 to be installed on the system and specified via RETICULATE_PYTHON or RETICULATE_PYTHON_ENV; if environment variables are set, all dependent Python packages (matchms, spectrum_utils, numpy) must be manually installed.
- First call to wrapped functions incurs Python initialization overhead and is noticeably slower than subsequent calls.
- Data interchange via reticulate involves serialization and deserialization; large spectral datasets or very frequent cross-language calls may incur measurable latency.
- Complex Python objects (custom classes, iterators) that do not map to standard R types (list, numeric, character) may require explicit conversion layers.
- Version mismatches between R wrapper and underlying Python libraries (e.g., matchms 0.30 vs. 0.31) can break backward compatibility; SpectriPy documents tested version pins (matchms 0.31, spectrum_utils 0.3.2, numpy 2.2.0).

## Evidence

- [intro] SpectriPy enables seamless integration through function wrapping: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R"
- [readme] Concrete conversion between R and Python spectral objects: "contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects"
- [readme] Bidirectional object translation within unified workflow: "R and Python spectral objects are easily translated and available in one workflow (i.e., a quarto document)"
- [readme] Parameter-driven Python function calls via wrapper: "The *SpectriPy* package provides the `compareSpectriPy()` function that allows to perform spectra similarity calculations using the scoring functions from MS Python packages"
- [readme] Automatic Python dependency resolution: "*SpectriPy*'s Python library management uses the [`py_require()`](https://rstudio.github.io/reticulate/reference/py_require.html) function introduced in *reticulate* version 1.41"
- [readme] Example demonstrating parameter translation to wrapped function: "We calculate the similarity using the *CosineGreedy* function from *matchms*, changing the `tolerance` to a value of `0.05` (instead of the default `0.1`)"
