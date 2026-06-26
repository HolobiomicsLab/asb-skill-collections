---
name: mass-spectrometry-package-integration
description: Use when you have R Spectra objects and need to apply Python-only MS
  algorithms (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
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

# Cross-Language Mass Spectrometry Package Integration

## Summary

Wrap Python mass spectrometry libraries (matchms, spectrum_utils) as R-callable functions within the Spectra framework, enabling seamless bidirectional translation of spectral objects and leveraging specialized Python algorithms (e.g., CosineGreedy similarity, spectral normalization) in R-based MS analysis workflows.

## When to use

You have R Spectra objects and need to apply Python-only MS algorithms (e.g., modified cosine similarity, advanced filtering, or normalization from matchms or spectrum_utils) without switching environments, or you are building a unified R–Python workflow where custom spectral operations must be callable from both languages within a single notebook or script.

## When NOT to use

- Python dependencies (matchms ≥0.31, spectrum_utils ≥0.3.2, numpy ≥2.2.0) cannot be installed or Python ≥3.12 is unavailable on the system.
- All required MS operations are available natively in R Spectra or other R packages; wrapping adds initialization overhead (reticulate setup) with no algorithmic gain.
- The workflow must operate in a strictly isolated Python or R environment with no inter-process communication capability.

## Inputs

- R Spectra object (DataFrame-backed with msLevel, precursorMz, mz, intensity columns)
- Similarity/comparison parameter object (e.g., CosineGreedy, ModifiedCosine from matchms)
- Optional: Python virtual environment path (via RETICULATE_PYTHON_ENV or RETICULATE_PYTHON environment variable)

## Outputs

- Numeric matrix of spectral similarities or comparison scores
- Processed Spectra object with algorithm-applied results (e.g., filtered/normalized peaks)
- Converted Python spectrum object (matchms.Spectrum, spectrum_utils.MsmsSpectrum) for downstream Python use

## How to apply

Install SpectriPy (which auto-installs Python dependencies via reticulate's py_require()) and confirm Python ≥3.12 is available. Create R Spectra objects from your MS data (e.g., using DataFrame with msLevel, precursorMz, mz, intensity columns). Call SpectriPy wrapper functions (e.g., compareSpectriPy() with a param object such as CosineGreedy(tolerance=0.05)) to translate R Spectra to matchms.Spectrum or spectrum_utils.MsmsSpectrum objects internally, execute the Python algorithm with specified parameters, and marshal the result (e.g., similarity matrix) back to R. Validate that returned objects preserve expected data types (numeric matrix, list structure) and match ground-truth results from direct Python execution when available.

## Related tools

- **SpectriPy** (R package that wraps Python MS library functions and provides conversion between R Spectra and Python spectrum objects (matchms.Spectrum, spectrum_utils.MsmsSpectrum)) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (R infrastructure package for storing, subsetting, and processing MS spectra; serves as the R object container into which Python results are marshalled) — https://github.com/RforMassSpectrometry/Spectra
- **matchms** (Python library providing spectral similarity functions (CosineGreedy, CosineHungarian, ModifiedCosine) and spectral filtering/normalization algorithms called via SpectriPy wrappers) — https://github.com/matchms
- **spectrum_utils** (Python library for MS spectrum object representation (MsmsSpectrum) and peak processing, interfaced through SpectriPy) — https://github.com/bittremieux-lab/spectrum_utils
- **reticulate** (R package enabling inter-process Python–R communication; SpectriPy uses its py_require() function to manage Python dependencies) — https://rstudio.github.io/reticulate

## Examples

```
library(Spectra); library(SpectriPy); res <- compareSpectriPy(all_spectra, reference_spectra, param = CosineGreedy(tolerance = 0.05))
```

## Evaluation signals

- Wrapped Python function executes without reticulate or module-import errors; first call initializes Python environment (observable latency), subsequent calls are faster.
- Returned similarity matrix dimensions match the Cartesian product of query and reference spectrum counts; all values are finite numeric (no NaN/Inf from failed conversions).
- Spot-check: similarity scores for identical or highly similar spectra (e.g., two caffeine MS2 spectra) are high (>0.8 for cosine-like metrics); dissimilar compound pairs score low.
- Round-trip consistency: converting a Spectra object to matchms.Spectrum, applying an operation in Python, and converting back yields the same logical result as calling compareSpectriPy() directly from R.
- Parameter sensitivity: varying tolerance (e.g., 0.05 vs. 0.1 in CosineGreedy) produces visibly different similarity matrices in the expected direction (stricter tolerance → lower scores for borderline matches).

## Limitations

- First call to a wrapped Python function incurs Python initialization overhead (seconds); subsequent calls are faster because the Python environment persists within the R session.
- Requires Python ≥3.12 and specific versions of matchms (0.31) and spectrum_utils (0.3.2); environment variable RETICULATE_PYTHON_ENV or RETICULATE_PYTHON must be set correctly if using system/custom Python; auto-install via py_require() may fail on systems with restricted package managers.
- Data interchange is lossy for non-standard spectrum metadata or peak annotations not explicitly mapped in the Spectra ↔ matchms conversion; custom spectrum variables in R may not survive round-trip conversion.
- Cosine-family similarity scores are symmetric but may differ slightly from hand-calculated values due to numerical precision in the Python implementation; always validate against reference benchmarks for publication-grade claims.

## Evidence

- [readme] By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R"
- [readme] SpectriPy can leverage the spectral similarity, filtering, normalization etc. calculations from the Python *matchms* library: "SpectriPy can leverage the spectral similarity, filtering, normalization etc. calculations from the Python *matchms* library"
- [readme] functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects: "functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects"
- [readme] *SpectriPy* needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries are automatically installed by the *reticulate* R package: "*SpectriPy* needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries are automatically installed by the *reticulate* R package"
- [readme] The *SpectriPy* package provides the `compareSpectriPy()` function that allows to perform spectra similarity calculations using the scoring functions from MS Python packages: "The *SpectriPy* package provides the `compareSpectriPy()` function that allows to perform spectra similarity calculations using the scoring functions from MS Python packages"
- [readme] As a result `compareSpectriPy()` returns also a numeric matrix of similarities. Note also that the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be initialized: "As a result `compareSpectriPy()` returns also a numeric matrix of similarities. Note also that the first `compareSpectriPy()` call takes usually a little longer because the Python setup has to be"
