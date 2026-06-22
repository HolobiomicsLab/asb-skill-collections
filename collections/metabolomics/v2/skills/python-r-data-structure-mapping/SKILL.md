---
name: python-r-data-structure-mapping
description: Use when when you have mass spectrometry data in R's Spectra format but need to leverage Python libraries (matchms, spectrum_utils) for specialized operations like spectral similarity scoring, filtering, or normalization that lack native R implementations or perform better in Python.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3356
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3068
  tools:
  - SpectriPy
  - R
  - Python
  - Spectra
  - reticulate
  - matchms
  - spectrum_utils
derived_from:
- doi: 10.21105/joss.08070
  title: spectripy
evidence_spans:
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R
- MS analysis in R. By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R
- integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R. By wrapping Python functionality into R functions
- allows integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R. By wrapping Python functionality into R functions
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
---

# Python-R Data Structure Mapping

## Summary

Convert between R Spectra objects and Python mass spectrometry data structures (matchms.Spectrum, spectrum_utils.MsmsSpectrum) to enable seamless execution of Python MS algorithms within R workflows. This skill bridges language barriers by serializing R objects, executing Python routines, and deserializing results back into R-compatible formats.

## When to use

When you have mass spectrometry data in R's Spectra format but need to leverage Python libraries (matchms, spectrum_utils) for specialized operations like spectral similarity scoring, filtering, or normalization that lack native R implementations or perform better in Python. Particularly relevant when building custom workflows that integrate both R and Python MS packages in a single analysis pipeline.

## When NOT to use

- The desired operation is already available in R's Spectra package (e.g., compareSpectra for native similarity scoring) — use native R functions to avoid serialization overhead.
- Python dependencies (matchms ≥0.31, spectrum_utils ≥0.3.2, numpy ≥2.2.0) cannot be installed on the system or are incompatible with the R environment.
- Real-time or streaming analysis on very large spectra collections where serialization/deserialization latency is prohibitive.

## Inputs

- R Spectra object (containing MS/MS spectra with m/z, intensity, precursor m/z, and metadata)
- Python matchms or spectrum_utils library reference (pre-configured via reticulate)
- Tolerance/parameter settings for the target Python algorithm

## Outputs

- R Spectra object (result of Python computation, with all attributes preserved)
- Numeric matrix of pairwise similarity scores (if using compareSpectriPy)
- Filtered or normalized Spectra object (if using Python filtering/normalization routines)

## How to apply

Define an R function that accepts a Spectra object as input. Use SpectriPy's cross-language interface (powered by reticulate) to serialize the Spectra object into a Python-compatible structure (matchms.Spectrum or spectrum_utils.MsmsSpectrum). Execute the target Python routine on the converted data. Deserialize the Python result back into an R Spectra object, ensuring all expected attributes (msLevel, precursorMz, mz, intensity, metadata fields) are preserved and valid. Validate the round-trip by confirming schema integrity and comparing downstream calculations performed in both languages on identical input data.

## Related tools

- **SpectriPy** (Provides the R-to-Python wrapping interface and conversion functions (compareSpectriPy, Spectra-to-matchms serialization)) — https://github.com/RforMassSpectrometry/SpectriPy
- **Spectra** (Defines the R data structure (Spectra objects, backends) that serve as input/output containers for cross-language conversion) — https://github.com/RforMassSpectrometry/Spectra
- **reticulate** (Underlying R package that manages Python environment configuration, object serialization, and function calls between R and Python)
- **matchms** (Python MS package providing spectral similarity algorithms (CosineGreedy, etc.) and spectrum object format that SpectriPy wraps) — https://github.com/matchms
- **spectrum_utils** (Python MS utilities library offering spectrum preprocessing and MsmsSpectrum object format compatible with SpectriPy conversion) — https://github.com/bittremieux-lab/spectrum_utils

## Examples

```
library(Spectra); library(SpectriPy); all <- c(caf, mhd); res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))
```

## Evaluation signals

- Returned Spectra object is valid (schema conforms to Spectra class requirements; no null/NaN in critical fields like msLevel, precursorMz, mz, intensity).
- Round-trip integrity: attributes present in input Spectra match those in output Spectra after Python round-trip conversion.
- Computational equivalence: similarity scores or filtering results from compareSpectriPy with CosineGreedy(tolerance=X) match expected values from direct Python matchms calls on identical spectra.
- No data loss: mz and intensity vectors preserve numeric precision and order after serialization/deserialization cycles.
- Metadata preservation: custom spectra variables (id, name, etc.) survive the round-trip conversion.

## Limitations

- Requires Python ≥3.12 and manual installation of matching versions of matchms (0.31), spectrum_utils (0.3.2), and numpy (2.2.0); version mismatches can cause silent data corruption or conversion failures.
- No changelog available in SpectriPy repository, limiting reproducibility and version tracking across updates.
- Serialization/deserialization overhead makes this approach slower than pure R operations; most beneficial for algorithms unavailable in R rather than those that exist natively in Spectra.
- Cross-language object conversion may introduce floating-point precision artifacts or reordering of peaks if not carefully implemented; validate numerical stability for downstream quantitative comparisons.

## Evidence

- [readme] SpectriPy enables seamless integration: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R"
- [other] Conversion workflow steps: "1. Define an R function that takes a Spectra object as input. 2. Use SpectriPy's cross-language interface to serialize the Spectra object and pass it to a Python MS package routine. 3. Execute the"
- [readme] Supported Python object formats: "contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects from the Python [*matchms*](https://github.com/matchms)"
- [readme] Python dependency requirements: "*SpectriPy* needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries (listed below) are automatically installed by the"
- [readme] Example usage with CosineGreedy: "res <- compareSpectriPy(all, caf, param = CosineGreedy(tolerance = 0.05))"
