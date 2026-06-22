---
name: imzml-continuous-format-parsing
description: Use when you have acquired raw mass spectrometry imaging data in imzML continuous format (e.g., from CardinalIO or other MSI instruments) and need to load it into R as a structured MSImagingExperiment object to perform statistical analysis, normalization, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Cardinal
  - CardinalIO
  - R
  - BiocManager
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of the new low-level signal processing functions'
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
---

# imzml-continuous-format-parsing

## Summary

Parse mass spectrometry imaging data stored in imzML continuous format into an MSImagingExperiment object for downstream analysis. This skill verifies correct dimensionality, m/z alignment across spectra, and data integrity of the imported dataset.

## When to use

You have acquired raw mass spectrometry imaging data in imzML continuous format (e.g., from CardinalIO or other MSI instruments) and need to load it into R as a structured MSImagingExperiment object to perform statistical analysis, normalization, or visualization. The continuous format encodes all spectra with identical m/z arrays, making this appropriate for high-resolution, uniform-sampling MSI datasets.

## When NOT to use

- Input is already an R object or in-memory data frame; use direct assignment instead of readMSIData().
- imzML file is in processed format rather than continuous; this skill assumes continuous encoding with uniform m/z arrays across all spectra.
- Data has already been normalized, baseline-corrected, or peak-picked; this skill imports raw data — apply pre-processing after import.

## Inputs

- imzML file in continuous format (e.g., '.imzML' with accompanying '.ibd' binary file)
- file path to the imzML file (character string)

## Outputs

- MSImagingExperiment object
- object with slots: pixels (spectra count), features (m/z values count), shared m/z array across all spectra, and intensity matrix

## How to apply

Load the Cardinal package and use readMSIData() with the file path to the imzML file. Verify the returned object is an MSImagingExperiment by inspecting its class and dimensions: confirm the number of pixels (spectra) matches the imaging geometry and the m/z feature count (typically thousands to tens of thousands) is consistent across all spectra. Validate spectral data integrity by spot-checking intensity values and confirming all spectra share identical m/z values (characteristic of continuous imzML). If dimensions or m/z alignment are unexpected, inspect the raw imzML metadata or file structure to diagnose format issues.

## Related tools

- **Cardinal** (provides readMSIData() function to parse imzML continuous format into MSImagingExperiment object) — https://github.com/kuwisdelu/Cardinal
- **CardinalIO** (supplies example imzML continuous test files for validation and reproducibility)
- **R** (execution environment; required to load Cardinal package and run readMSIData())
- **BiocManager** (package manager for installing Cardinal from Bioconductor release)

## Examples

```
library(Cardinal); msi_data <- readMSIData(CardinalIO::exampleImzMLFile('continuous')); print(dim(msi_data))
```

## Evaluation signals

- Object class is 'MSImagingExperiment' (verify via class() or inherits())
- Dimensions match expected imaging geometry: pixels dimension equals number of spectra, features dimension equals m/z count (e.g., 9 pixels × 8,399 m/z values)
- All spectra share identical m/z values: compare m/z array across first and last spectrum; should be bit-identical
- Intensity matrix is non-empty and contains numeric values with expected range (e.g., non-negative counts or intensities)
- No NA or NaN values in m/z or intensity data unless explicitly expected from instrument artifacts

## Limitations

- Assumes imzML file is well-formed and complies with the imzML schema; malformed or corrupted files may fail or produce incorrect objects.
- The continuous format requires all spectra to share identical m/z values; processed imzML files (with varying m/z per spectrum) require different handling.
- Large imzML files (>gigabytes) may require out-of-memory support via MSImagingArrays or other memory-mapped structures; readMSIData() can import these but users must specify appropriate parameters.
- No automatic validation of pixel-to-coordinate mapping; inspect metadata separately if spatial coordinates are critical for subsequent analysis.

## Evidence

- [other] Defines continuous imzML reading workflow: "Read the imzML file into an MSImagingExperiment object using readMSIData() with the retrieved file path. Verify the object structure: confirm class is MSImagingExperiment, inspect dimensions to"
- [other] Confirms continuous format produces uniform m/z arrays: "Reading the CardinalIO 'continuous' example imzML file with readMSIData() returns an MSImagingExperiment object containing 9 mass spectra each with 8,399 m/z values, where all spectra share the same"
- [intro] Establishes readMSIData() as primary parsing function: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] Documents imzML continuous format support scope: "Support for writing imzML in addition to reading it; more options and support for importing out-of-memory imzML for both 'continuous' and 'processed' formats"
- [readme] Provides installation path for Cardinal via BiocManager: "Cardinal can be installed via the BiocManager package. This is the **recommended** installation method."
