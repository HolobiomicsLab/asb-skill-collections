---
name: mass-spectrometry-data-loading-and-formatting
description: Use when you have raw or curated mass spectrometry data (MS1, MS2, or MSMS) in mzML, mzXML, CDF, MGF, MSP formats, or from a MassBank/MetaboLights repository, and need to convert it into an in-memory or on-disk spectral object that supports filtering, comparison, and annotation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectriPy
  - R
  - Spectra
  - mzR
  - matchms
  - spectrum_utils
  - CompoundDb
  - MsBackendMassbank
  - MsBackendMgf
  - MsBackendMsp
  - MsBackendMetaboLights
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.08070
  all_source_dois:
  - 10.21105/joss.08070
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-loading-and-formatting

## Summary

Load mass spectrometry data from diverse file formats and standardized databases into language-specific spectral objects (R Spectra or Python matchms/spectrum_utils objects) that enable downstream processing, similarity calculations, and cross-language workflows. This skill bridges data ingestion with reproducible MS analysis in R or Python environments.

## When to use

You have raw or curated mass spectrometry data (MS1, MS2, or MSMS) in mzML, mzXML, CDF, MGF, MSP formats, or from a MassBank/MetaboLights repository, and need to convert it into an in-memory or on-disk spectral object that supports filtering, comparison, and annotation workflows. Use this skill before any spectral similarity, normalization, or library matching step.

## When NOT to use

- Your data is already loaded in memory as a processed feature table or abundance matrix (m/z × sample), and you do not need to recover individual spectrum metadata or peak information.
- You are working exclusively with pre-computed spectral similarity scores or cross-library matches, not with raw spectral peak data.
- Your workflow requires real-time streaming of spectra from a live instrument acquisition system rather than static files or databases.

## Inputs

- mzML file
- mzXML file
- CDF (NetCDF) file
- MGF (Mascot Generic Format) file
- MSP (NIST) format file
- MassBank SQL database connection
- MetaboLights repository URL
- CompoundDb database (CompDb)
- DataFrame with spectral variables and peaks lists

## Outputs

- Spectra object (R; in-memory or on-disk backend)
- matchms.Spectrum object (Python)
- spectrum_utils.spectrum.MsmsSpectrum object (Python)
- MsBackend instance (MsBackendMemory, MsBackendMzR, MsBackendDataFrame, etc.)

## How to apply

Choose a backend based on your data source and memory constraints: use `MsBackendMzR` for mzML/mzXML/CDF files (on-disk, low memory footprint), `MsBackendMgf` for MGF format, `MsBackendMsp` for NIST MSP files, or `MsBackendDataFrame` for in-memory processing when speed is prioritized over memory. Create a Spectra object by passing the loaded data and specifying the backend; verify that m/z, intensity, precursor m/z, and MS level variables are correctly populated. For Python workflows, convert the Spectra object to matchms.Spectrum or spectrum_utils.spectrum.MsmsSpectrum using SpectriPy's conversion functions. Validate the loaded object by checking spectrum count, m/z range, intensity distribution, and presence of required metadata (e.g., precursor m/z for MS2 spectra).

## Related tools

- **Spectra** (Core R package for creating, storing, and manipulating MS spectral objects with pluggable backends for different file formats and storage strategies) — https://github.com/RforMassSpectrometry/Spectra
- **SpectriPy** (R package wrapper enabling conversion between R Spectra objects and Python matchms/spectrum_utils objects for cross-language data loading and transformation) — https://github.com/RforMassSpectrometry/SpectriPy
- **mzR** (R package providing efficient on-disk reading of mzML, mzXML, and CDF files via the MsBackendMzR backend)
- **matchms** (Python library for spectral object representation and similarity scoring; input/output target for cross-language workflows via SpectriPy) — https://github.com/matchms
- **spectrum_utils** (Python library for MS spectra processing and representation; conversion bridge for cross-language analysis via SpectriPy) — https://github.com/bittremieux-lab/spectrum_utils
- **CompoundDb** (R package providing MsBackendCompDb backend to load spectra directly from compound databases with on-the-fly data retrieval) — https://github.com/rformassspectrometry/CompoundDb
- **MsBackendMassbank** (R package providing backends (MsBackendMassbank, MsBackendMassbankSql) to import/export MassBank text and SQL database formats) — https://github.com/rformassspectrometry/MsBackendMassbank
- **MsBackendMgf** (R package providing MsBackendMgf backend to import/export Mascot Generic Format files into Spectra objects) — https://github.com/rformassspectrometry/MsBackendMgf
- **MsBackendMsp** (R package providing MsBackendMsp backend to import/export NIST MSP format spectra into Spectra objects) — https://github.com/rformassspectrometry/MsBackendMsp
- **MsBackendMetaboLights** (R package providing MsBackendMetaboLights backend to retrieve and cache MS data files from MetaboLights repository) — https://github.com/rformassspectrometry/MsBackendMetaboLights

## Examples

```
library(Spectra); library(SpectriPy); caf <- Spectra(DataFrame(msLevel=c(2L,2L), name='Caffeine', precursorMz=c(195.0877, 195.0877), mz=list(c(135.0432, 138.0632, 163.0375, 195.0880), c(110.0710, 138.0655, 138.1057, 138.1742, 195.0864)), intensity=list(c(340.0, 416, 2580, 412), c(388.0, 3270, 85, 54, 10111))))
```

## Evaluation signals

- Spectrum count matches the input file or query result (no spectra dropped or duplicated during loading).
- All required spectral variables (msLevel, precursorMz for MS2, mz and intensity peak vectors) are non-null and correctly typed in the loaded Spectra object.
- m/z values are within expected range (typically 50–2000 m/z) and sorted in ascending order within each spectrum; intensity values are non-negative and numeric.
- Metadata fields (compound name, ID, collision energy, etc.) are preserved and match the source file; spot-check a few spectra against the original file or database record.
- For on-disk backends (MsBackendMzR, MsBackendCompDb), memory footprint remains constant regardless of file size; for in-memory backends, memory scales linearly with spectrum count.
- Cross-language conversion (Spectra → matchms.Spectrum via SpectriPy) preserves m/z, intensity, and metadata without loss; verify by comparing the Python object's attributes to the original R Spectra.

## Limitations

- Some backends (MsBackendMemory, MsBackendDataFrame) load entire datasets into memory, making them unsuitable for large datasets (>100k spectra or >10 GB); use on-disk backends (MsBackendMzR, MsBackendCompDb) for large files.
- File format support depends on installed backend packages; missing a backend requires additional installation (e.g., MsBackendMgf for MGF files).
- Python integration via SpectriPy requires Python ≥ 3.12 and automatic installation of Python dependencies (matchms 0.31, spectrum_utils 0.3.2, numpy 2.2.0); environment variable RETICULATE_PYTHON or RETICULATE_PYTHON_ENV may be needed for manual Python configuration.
- Some metadata fields from non-standard or custom file formats may be dropped if the backend does not explicitly support them; always validate metadata preservation after loading.
- Real-time or streaming acquisition workflows are not supported; all data must be available as a static file or database before loading.

## Evidence

- [readme] The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra and functionality to subset, process, visualize and compare spectra data.: "The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra and functionality to subset, process, visualize and compare spectra data."
- [readme] *Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets ensuring a small memory footprint.: "*Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets"
- [readme] MsBackendMzR (package: *Spectra*): by using the `mzR` package it supports import of MS data from mzML, mzXML and CDF files. This backend keeps only general spectra variables in memory and retrieves the peaks data (m/z and intensity values) on-the-fly from the original data files.: "MsBackendMzR (package: *Spectra*): by using the `mzR` package it supports import of MS data from mzML, mzXML and CDF files. This backend keeps only general spectra variables in memory and retrieves"
- [readme] By wrapping Python functionality into R functions, *SpectriPy* allows a seamless integration of Python libraries into R. For example, *SpectriPy* can leverage the spectral similarity, filtering, normalization etc. calculations from the Python [*matchms*](https://github.com/matchms) library and contains functions to convert between R's `Spectra::Spectra` objects and `matchms.Spectrum` and `spectrum_utils.spectrum.MsmsSpectrum` objects: "*SpectriPy* allows a seamless integration of Python libraries into R. For example, *SpectriPy* can leverage the spectral similarity, filtering, normalization etc. calculations from the Python"
- [readme] *SpectriPy* needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries (listed below) are automatically installed by the [*reticulate*](https://rstudio.github.io/reticulate) R package.: "*SpectriPy* needs Python (version >= 3.12) to be installed on the system. All necessary Python libraries are automatically installed by the [*reticulate*] R package."
- [other] Instantiate a Spectra object from the dataset. 4. Invoke a Python MS package function through the SpectriPy wrapper layer on the Spectra object.: "Instantiate a Spectra object from the dataset. 4. Invoke a Python MS package function through the SpectriPy wrapper layer on the Spectra object."
