---
name: msimagingexperiment-object-validation
description: Use when after reading an imzML file (continuous or processed format)
  using readMSIData() and before proceeding to preprocessing or statistical analysis
  steps. Use this skill whenever you need to confirm that a parsed imaging dataset
  meets expected structural requirements—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - Cardinal
  - CardinalIO
  - R
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

# msimagingexperiment-object-validation

## Summary

Validates that an imzML file has been correctly parsed into an MSImagingExperiment object by checking class type, spectral dimensions (number of spectra and m/z features), and spectral data integrity. This skill ensures that downstream mass spectrometry imaging analysis proceeds with correctly formatted and dimensionally consistent data.

## When to use

After reading an imzML file (continuous or processed format) using readMSIData() and before proceeding to preprocessing or statistical analysis steps. Use this skill whenever you need to confirm that a parsed imaging dataset meets expected structural requirements—e.g., the expected number of mass spectra (pixels), m/z value count per spectrum, and whether all spectra share the same m/z axis.

## When NOT to use

- Input is already an MSImagingExperiment object that has already been validated in an earlier step—skip re-validation unless data has been modified.
- File is not in imzML or Analyze 7.5 format; Cardinal's readMSIData() is specific to these formats.
- You are validating processed or normalized data after statistical analysis; validation should occur immediately post-import, not downstream.

## Inputs

- imzML file (continuous or processed format)
- File path string to CardinalIO example or user-supplied imzML

## Outputs

- Validated MSImagingExperiment object with confirmed dimensions
- Boolean confirmation of class type and dimensional consistency
- Diagnostic report of spectrum count, m/z feature count, and m/z axis uniformity

## How to apply

Load the Cardinal package and import an imzML file using readMSIData(). Verify the returned object's class is MSImagingExperiment. Inspect object dimensions using standard R accessor methods to confirm the number of spectra (pixels) and m/z features per spectrum match expectations. Validate spectral data integrity by confirming that all spectra share identical m/z values (in imzML continuous format, all spectra typically reference a single common m/z axis). If dimensions or class do not match, the import failed or the file format was not as expected.

## Related tools

- **Cardinal** (Provides readMSIData() function to import imzML files and MSImagingExperiment class structure for validation) — github.com/kuwisdelu/Cardinal
- **CardinalIO** (Supplies example imzML test files (continuous and processed formats) for validation testing and verification)
- **R** (Execution environment and provides base object introspection methods (class, dim, etc.) for validation checks)

## Examples

```
library(Cardinal); path_continuous <- CardinalIO::exampleImzMLFile('continuous'); msi <- readMSIData(path_continuous); class(msi); dim(msi); head(mz(msi))
```

## Evaluation signals

- Class of returned object is confirmed to be 'MSImagingExperiment' (or 'MSImagingArrays' in some contexts)
- Dimensions match expected values: nrow (m/z features) = expected count, ncol (spectra/pixels) = expected count
- All spectra share identical m/z values (in continuous imzML, featureNames or mz(object) returns a single vector of length matching nrow)
- No missing or NA values in spectral intensity matrix; object@imageData slot is non-empty and of correct dimension
- Object successfully inherits from SpectralImagingExperiment or SpectralImagingData (class hierarchy check)

## Limitations

- Validation only confirms structural integrity; it does not detect data quality issues (e.g., low signal-to-noise, calibration errors, or missing pixels).
- This skill assumes the imzML file is well-formed; malformed or corrupted imzML files may cause readMSIData() to fail before validation is reached.
- Dimension expectations must be known or inferred in advance; if expected dimensions are unknown, this skill cannot flag spurious imports.
- Processed imzML files may have different structure (e.g., non-uniform m/z axes across spectra); validation logic must adapt accordingly.

## Evidence

- [other] Research question from task_001: "Does readMSIData() correctly parse a 'continuous' imzML file from CardinalIO as an MSImagingExperiment object with the expected dimensions of 9 spectra and 8,399 m/z values per spectrum?"
- [other] Finding from task_001 demonstrates validation workflow: "Reading the CardinalIO 'continuous' example imzML file with readMSIData() returns an MSImagingExperiment object containing 9 mass spectra each with 8,399 m/z values, where all spectra share the same"
- [other] Workflow steps from task_001 detail validation procedure: "Verify the object structure: confirm class is MSImagingExperiment, inspect dimensions to confirm 9 spectra (pixels) and 8,399 m/z features per spectrum, and validate spectral data integrity."
- [intro] Cardinal support for imzML formats: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] MSImagingExperiment class design: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
