---
name: ce-ms-data-import-and-parsing
description: Use when you have raw CE-MS instrument output in mzML or netCDF format and need to extract specific ion traces (by m/z value), filter by effective mobility windows, or apply transformations to migration time data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - MobilityTransformR
  - Spectra
  - xcms
  - MetaboCoreUtils
  - MSnbase
  - R
  - msdata
  - BiocManager
  techniques:
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("Spectra")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
- The MT of the peak will be determined by `findChromPeaks` from `xcms`.
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac441
  all_source_dois:
  - 10.1093/bioinformatics/btac441
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CE-MS data import and parsing

## Summary

Load and parse raw capillary electrophoresis–mass spectrometry (CE-MS) data from standard formats (mzML, netCDF) into R memory structures that preserve spectral, mobility, and mass-to-charge information for downstream transformation and feature extraction. This is the foundational step that enables reproducible analysis of CE-MS electropherograms.

## When to use

You have raw CE-MS instrument output in mzML or netCDF format and need to extract specific ion traces (by m/z value), filter by effective mobility windows, or apply transformations to migration time data. Use this skill when beginning a CE-MS analysis pipeline or when integrating new CE-MS datasets from different instruments or electroosmotic flow regimes.

## When NOT to use

- Input data is already a feature table, peak list, or aggregated matrix — use this skill only for raw instrument files.
- You need only summary statistics (total ion chromatogram, mass accuracy report) without storing full spectral detail — lighter summarization tools may be more efficient.
- Data has already been converted to a different format (e.g. mzXML, HDF5) in a prior step — use format-specific parsers for those formats.

## Inputs

- Raw CE-MS data file (mzML format)
- Raw CE-MS data file (netCDF format)
- Instrument metadata (electroosmotic flow parameters, capillary dimensions, applied voltage)

## Outputs

- Spectra object (R) containing all scans with m/z, intensity, and migration time
- MSnbase Spectrum2 collection with spectral annotations
- Data table of scan-level metadata (scan number, migration time, polarity, precursor m/z if applicable)

## How to apply

Load raw CE-MS data using the Spectra or MSnbase package, which parse mzML or netCDF files into R spectral objects preserving m/z, intensity, and retention time (migration time) metadata. Verify that the loaded object contains the expected m/z range, number of scans, and scan-level metadata (polarity, activation, precursor masses if MS/MS). Check that migration time values span the expected range for your CE method and that no scans are missing or corrupted. Store the parsed object for use in downstream m/z extraction, effective mobility transformation, and peak detection workflows.

## Related tools

- **Spectra** (Primary package for loading and representing CE-MS spectral data from mzML and netCDF into R; provides low-level access to m/z and intensity arrays and metadata.)
- **MSnbase** (Alternative/complementary package for importing and working with mass spectrometry data objects, including CE-MS; supports object-oriented access to spectral data.)
- **msdata** (Provides reference CE-MS test datasets in mzML format for development and validation of import and parsing workflows.)
- **BiocManager** (Bioconductor package manager used to install Spectra, MSnbase, and related CE-MS analysis packages.)

## Examples

```
library(Spectra); library(msdata); mzml_file <- system.file('TripleTOF5600/PestMix_Pos_5uLInj_01_Infusion.mzML', package='msdata'); sp <- Spectra(mzml_file); sp
```

## Evaluation signals

- Spectra or MSnbase object is successfully created with non-zero scan count and all expected metadata fields (m/z array, intensity array, migration time, polarity).
- m/z values span the expected instrument range (e.g. 50–2000 m/z for typical CE-MS) and match the known analyte mass ± instrument accuracy.
- Migration time values are positive, monotonically increasing across scans, and consistent with the expected CE run duration (typically 10–100 min).
- No NaN, Inf, or missing values in critical fields (m/z, intensity, migration time); any flagged scans have documented reasons (e.g. low signal, detector saturation).
- Extracted ion trace for a known internal standard or reference compound (e.g. Lysine m/z 147.112806) returns a non-empty signal and peak-like intensity profile across the migration time window.

## Limitations

- Effective mobility transformation requires electroosmotic flow correction metadata that may not always be embedded in raw mzML/netCDF files; manual entry or external calibration may be needed.
- Some older CE-MS instruments or local data export formats may not produce standards-compliant mzML or netCDF; custom parsers or format conversion may be required.
- Large raw files (>1 GB) may exceed available RAM if fully loaded into memory; chunked or lazy-loading strategies may be necessary.
- netCDF format support depends on system netCDF library availability; mzML is more portable across platforms.

## Evidence

- [other] Load raw CE-MS data (mzML or netCDF) containing Lysine signal using Spectra or MSnbase.: "Load CE-MS raw data (mzML or netCDF) containing Lysine signal using Spectra or MSnbase."
- [intro] The transformation is performed using functionality from the packages Spectra, MSnbase, xcms, and MetaboCoreUtils.: "The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("Spectra")`"
- [intro] There is no R implementation for CE-MS effective mobility transformation prior to MobilityTransformR.: "there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data"
- [intro] CE-MS test data are provided in the msdata package for development and validation.: "The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package"
- [readme] Installation via BiocManager provides stable versions of import and analysis packages.: "To install MobilityTransformR, use the stable version available at Bioconductor."
