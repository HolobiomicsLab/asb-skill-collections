---
name: spectra-object-instantiation-and-manipulation
description: Use when you have mass spectrometry spectral data (m/z and intensity pairs, precursor m/z, MS level, and metadata) in R memory or in a file format (mzML, mzXML, CDF, MGF, MSP), and you need to organize it into a queryable, processable object before performing spectral similarity calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpectriPy
  - Spectra
  - R
  - reticulate
  - mzR
  - matchms
derived_from:
- doi: 10.21105/joss.08070
  title: spectripy
evidence_spans:
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R
- The *SpectriPy* package allows integration of Python MS packages into a [*Spectra*]-based MS analysis in R.
- integration of Python MS packages into a [*Spectra*](https://github.com/RforMassSpectrometry/Spectra)-based MS analysis in R
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

# Spectra-object-instantiation-and-manipulation

## Summary

Create and manipulate Spectra objects in R to represent mass spectrometry data, enabling downstream MS analysis workflows. This skill bridges raw or tabular MS data into R's native Spectra infrastructure, which supports efficient backends, spectral processing, and cross-language integration.

## When to use

You have mass spectrometry spectral data (m/z and intensity pairs, precursor m/z, MS level, and metadata) in R memory or in a file format (mzML, mzXML, CDF, MGF, MSP), and you need to organize it into a queryable, processable object before performing spectral similarity calculations, filtering, normalization, or comparison tasks within an R-based Spectra workflow.

## When NOT to use

- Input is already a Spectra object and no new instantiation is needed—use direct subsetting or manipulation methods instead.
- Data is stored in a relational database (SQL) and you require live querying without loading all spectra into memory—use MsBackendMassbankSql or MsBackendCompDb backends instead of MsBackendMemory.
- Raw instrument data has not yet been converted to a standard open format (mzML, CDF); pre-process with vendor software or mzR-compatible tools first.

## Inputs

- DataFrame with spectral variables (msLevel, name, precursorMz, id) and list columns (mz, intensity)
- mzML/mzXML/CDF file paths (for MsBackendMzR)
- MGF or MSP file paths (for format-specific backends)
- Spectra object (for downstream manipulation or merging)

## Outputs

- Spectra object (R S4 class)
- subsetted or filtered Spectra object
- numeric vectors or matrices (from compareSpectra output)
- modified Spectra object (after normalization, filtering, or Python function application)

## How to apply

Instantiate a Spectra object by passing a DataFrame containing spectral variables (msLevel, name, precursorMz, id) and nested list columns for m/z and intensity vectors. Choose a backend appropriate to your data size and access patterns—use MsBackendMemory (default) for fast in-memory processing of small datasets, MsBackendMzR for on-disk access to mzML/mzXML/CDF files with minimal memory footprint, or specialized backends (MsBackendMgf, MsBackendMsp) for standard spectral library formats. Once instantiated, the Spectra object exposes methods for subsetting, filtering, metadata access, and downstream processing. The object remains immutable to its backend but can be piped into comparison functions (compareSpectra, compareSpectriPy) and passed as input to Python MS libraries via the SpectriPy wrapper layer.

## Related tools

- **Spectra** (Core R package providing the Spectra S4 class and backends for efficient MS data storage and manipulation) — https://github.com/RforMassSpectrometry/Spectra
- **SpectriPy** (R wrapper enabling Spectra objects to be passed to and returned from Python MS package functions (matchms, spectrum_utils)) — https://github.com/RforMassSpectrometry/SpectriPy
- **reticulate** (R package managing Python environment and function wrapping; required by SpectriPy for cross-language integration)
- **mzR** (R package supporting import of mzML, mzXML, and CDF files via the MsBackendMzR backend)
- **matchms** (Python MS package providing spectral similarity scoring (CosineGreedy, ModifiedCosine) callable through SpectriPy) — https://github.com/matchms

## Examples

```
library(Spectra); library(SpectriPy); caf <- DataFrame(msLevel = c(2L, 2L), name = "Caffeine", precursorMz = c(195.0877, 195.0877)); caf$intensity <- list(c(340.0, 416, 2580, 412), c(388.0, 3270, 85, 54, 10111)); caf$mz <- list(c(135.0432, 138.0632, 163.0375, 195.0880), c(110.0710, 138.0655, 138.1057, 138.1742, 195.0864)); caf <- Spectra(caf)
```

## Evaluation signals

- Spectra object instantiates without error and returns a valid S4 object of class Spectra.
- Length of Spectra object matches the number of input spectra (nrow(DataFrame) or number of spectra imported from file).
- Accessor methods (msLevel, mz, intensity, precursorMz, metaData) return expected data types and values.
- Spectra object can be subset or filtered using standard R indexing or Spectra-specific filter functions without loss of data integrity.
- Spectra object can be successfully passed to compareSpectra or compareSpectriPy, returning a numeric similarity matrix with expected dimensions and values in [0, 1] range for cosine-based similarity.

## Limitations

- Default MsBackendMemory loads all spectra into RAM; for datasets >1–2 GB, use on-disk backends (MsBackendMzR, MsBackendHdf5Peaks) or streaming approaches.
- Nested list columns (mz, intensity) must be properly formatted as list-of-numeric; malformed or ragged arrays will cause instantiation failure.
- SpectriPy requires Python ≥3.12 and external Python libraries (matchms 0.31, spectrum_utils 0.3.2, numpy 2.2.0) to be installed; automatic installation via reticulate may fail on systems with conflicting Python environments.
- Spectra objects are immutable to their backend; in-place modification of peaks data is not supported—create a new Spectra object or use MsBackendDataFrame for mutable backends.
- Large-scale similarity comparisons (n > 10,000 spectra) between all pairs can be memory-intensive and computationally slow even with optimized backends.

## Evidence

- [readme] The Spectra package defines an efficient infrastructure for storing and handling mass spectrometry spectra and functionality to subset, process, visualize and compare spectra data.: "The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra and functionality to subset, process, visualize and compare spectra data."
- [readme] Spectra provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets ensuring a small memory footprint.: "Spectra provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets ensuring"
- [readme] By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R.: "By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R."
- [readme] Create a Spectra object with two MS2 spectra for Caffeine using DataFrame with msLevel, name, precursorMz, and list columns for intensity and mz.: "Create a Spectra object with two MS2 spectra for Caffeine. caf <- DataFrame( msLevel = c(2L, 2L), name = "Caffeine", precursorMz = c(195.0877, 195.0877) ); caf$intensity <- list(...); caf$mz <-"
- [other] Instantiate a Spectra object from the dataset in the task workflow, invoking a Python MS package function through the SpectriPy wrapper layer on the Spectra object.: "Instantiate a Spectra object from the dataset. 4. Invoke a Python MS package function through the SpectriPy wrapper layer on the Spectra object."
- [readme] SpectriPy needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries are automatically installed by the reticulate R package.: "*SpectriPy* needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries (listed below) are automatically installed by the"
