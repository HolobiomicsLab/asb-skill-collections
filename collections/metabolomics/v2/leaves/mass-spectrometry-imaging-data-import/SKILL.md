---
name: mass-spectrometry-imaging-data-import
description: Use when you have raw MS imaging data in imzML (continuous or processed)
  or Analyze 7.5 format and need to load it into R for spectral processing, normalization,
  peak-picking, or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Cardinal
  - CardinalIO
  - R
  - matter
  - BiocManager
  techniques:
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of
  the new low-level signal processing functions'
- 'We can read an example of a "continuous" imzML file from the `CardinalIO` package:'
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cardinal_cq
    doi: 10.1093/bioinformatics/btv146
    title: Cardinal
  dedup_kept_from: coll_cardinal_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv146
  all_source_dois:
  - 10.1093/bioinformatics/btv146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-imaging-data-import

## Summary

Import raw mass spectrometry imaging datasets in imzML or Analyze 7.5 formats into Cardinal's MSImagingExperiment or MSImagingArrays objects for downstream statistical analysis and visualization. This skill validates that spectral dimensions, m/z features, and pixel coordinates are correctly parsed and retained in memory or as out-of-memory references.

## When to use

You have raw MS imaging data in imzML (continuous or processed) or Analyze 7.5 format and need to load it into R for spectral processing, normalization, peak-picking, or statistical analysis. Use this skill as the first step in any Cardinal-based MS imaging workflow, before any pre-processing or analysis method.

## When NOT to use

- Input is already a processed feature table or peak intensity matrix (use readMSIData() only for raw vendor or mzML/imzML formats).
- Data is already loaded as an MSImagingExperiment in memory or you only need to append new columns (use accessor or merge methods instead).
- Input file is in a non-standard format not supported by Cardinal (e.g., vendor-proprietary binary without imzML or Analyze 7.5 export).

## Inputs

- imzML file (continuous or processed format)
- Analyze 7.5 format file (.hdr, .img, .t2m)
- File path (character string)

## Outputs

- MSImagingExperiment object (in-memory spectral imaging matrix with pixel coordinates and m/z features)
- MSImagingArrays object (out-of-memory spectral imaging matrix backed by matter)
- SpectralImagingData or SpectralImagingExperiment object (new class hierarchy in Cardinal 3.6)

## How to apply

Load the Cardinal package using library(Cardinal), then call readMSIData() with the file path to your imzML or Analyze 7.5 file. The function automatically parses file headers to infer whether the format is 'continuous' (raw unprocessed spectra with shared m/z axes) or 'processed' (centroided peaks), and returns an MSImagingExperiment object (in-memory) or MSImagingArrays (out-of-memory) depending on dataset size. Verify the resulting object by inspecting its class, confirming pixel count (nrow), m/z feature count (ncol), and the integrity of the mass spectral data matrix. For out-of-memory datasets, readMSIData() provides transparent backing via the matter package.

## Related tools

- **Cardinal** (Primary package providing readMSIData() function and MSImagingExperiment/MSImagingArrays class definitions) — https://github.com/kuwisdelu/Cardinal
- **matter** (Provides out-of-memory array backing for MSImagingArrays when datasets exceed RAM)
- **CardinalIO** (Provides example imzML files (continuous and processed) for testing and validation)
- **BiocManager** (Package manager for installing Cardinal and its Bioconductor dependencies)

## Examples

```
library(Cardinal); path_continuous <- CardinalIO::exampleImzMLFile('continuous'); msi_obj <- readMSIData(path_continuous); msi_obj
```

## Evaluation signals

- Returned object has class MSImagingExperiment or MSImagingArrays (or parent SpectralImagingExperiment in Cardinal 3.6+).
- Pixel count (nrow) and m/z feature count (ncol) match the declared dimensions in the imzML file header or Analyze 7.5 metadata.
- All spectra share identical m/z values (for continuous imzML) or have variable m/z axes (for processed imzML); inspect mz(object) to confirm.
- Spectral intensity values are numeric, non-negative, and preserve the dynamic range of the raw data (no unexpected truncation or scaling).
- Pixel coordinate matrix (pixelData) contains spatial (x, y) and optional (z) positions matching the number of spectra.

## Limitations

- readMSIData() does not automatically align or recalibrate m/z axes across spectra; use recalibrate() post-import if needed.
- Continuous imzML files are expected to have all spectra sharing the same m/z axis; processed imzML with variable m/z per spectrum require separate handling.
- Out-of-memory MSImagingArrays objects may be slower for certain operations (e.g., random-access peak picking) compared to in-memory MSImagingExperiment.
- No built-in validation of imzML file integrity or corruption; malformed files may produce cryptic errors or silent data loss.

## Evidence

- [intro] readMSIData() function for imzML and Analyze 7.5 formats: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] MSImagingExperiment and MSImagingArrays classes: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Out-of-memory dataset support via matter: "New imaging experiment classes such as ImagingExperiment, SparseImagingExperiment, and MSImagingExperiment provide better support for out-of-memory datasets"
- [intro] Continuous vs. processed imzML parsing: "Support for writing imzML in addition to reading it; more options and support for importing out-of-memory imzML for both 'continuous' and 'processed' formats"
- [readme] Installation via BiocManager: "Cardinal can be installed via the BiocManager package"
- [readme] Library loading and example imzML retrieval: "Once installed, Cardinal can be loaded with library(): library(Cardinal)"
- [other] Task validation of readMSIData() on continuous imzML: "Reading the CardinalIO 'continuous' example imzML file with readMSIData() returns an MSImagingExperiment object containing 9 mass spectra each with 8,399 m/z values, where all spectra share the same"
