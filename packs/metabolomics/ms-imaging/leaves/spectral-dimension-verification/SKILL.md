---
name: spectral-dimension-verification
description: Use when after reading an imzML file (continuous or processed format) using readMSIData() in Cardinal, verify the resulting MSImagingExperiment object before performing normalization, baseline reduction, peak-picking, or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Cardinal
  - CardinalIO
  - R
  techniques:
  - MS-imaging
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

# spectral-dimension-verification

## Summary

Verify that mass spectrometry imaging data has been correctly parsed into an MSImagingExperiment object by confirming the expected number of spectra (pixels), m/z feature count per spectrum, and spectral data integrity. This skill validates that imzML file reading was successful before proceeding to downstream analysis.

## When to use

After reading an imzML file (continuous or processed format) using readMSIData() in Cardinal, verify the resulting MSImagingExperiment object before performing normalization, baseline reduction, peak-picking, or statistical analysis. Use this skill when you have a known ground-truth specification for the expected dimensions (e.g., from CardinalIO example datasets or instrument metadata) and need to confirm the data import pipeline did not drop spectra, truncate m/z ranges, or corrupt spectral values.

## When NOT to use

- Input is already a processed feature table (e.g., peak matrix); this skill is for raw spectrum import verification only.
- You do not have access to ground-truth specifications for the expected dimensions (e.g., no metadata or example reference).
- The imzML file is known to be sparse or irregular (e.g., non-rectangular pixel layouts); standard dimension checks may not apply.

## Inputs

- imzML file (continuous or processed format)
- path to imzML file as character string

## Outputs

- MSImagingExperiment object
- validation report (dimensions, class, data integrity status)

## How to apply

Load the MSImagingExperiment object and inspect its class, dimensions, and spectral data integrity through the following steps: (1) confirm the object class is MSImagingExperiment using class(); (2) extract and verify the pixel count (number of spectra) and m/z feature count per spectrum using the dim() accessor or nrow()/ncol() methods; (3) confirm all spectra share the same m/z values by spot-checking spectral data consistency; (4) validate that no spectra or m/z features are NA or NaN unless explicitly expected; (5) compare observed dimensions against the known ground-truth from the imzML metadata or example file specification. If all dimensions match and spectral data are complete, the import was successful and analysis can proceed.

## Related tools

- **Cardinal** (Provides readMSIData() function to read imzML files and MSImagingExperiment class for object structure and dimension accessors) — https://github.com/kuwisdelu/Cardinal
- **CardinalIO** (Provides example imzML files (continuous and processed formats) with known, verifiable dimensions for testing and validation)
- **R** (Execution environment for calling Cardinal functions and dimension inspection methods)

## Examples

```
library(Cardinal); path_continuous <- CardinalIO::exampleImzMLFile('continuous'); msi <- readMSIData(path_continuous); print(class(msi)); print(dim(msi))
```

## Evaluation signals

- Object class is MSImagingExperiment (verified via class() or inherits()).
- Pixel count matches expected number of spectra (e.g., 9 for the CardinalIO continuous example).
- m/z feature count per spectrum matches ground-truth specification (e.g., 8,399 for the CardinalIO continuous example).
- All spectra share identical m/z values (no scatter or per-spectrum drift in m/z axis).
- No NA, NaN, or Inf values in spectral intensity data unless explicitly documented as missing.

## Limitations

- Dimension verification alone does not detect systematic reading errors such as incorrect mass calibration or transposed pixel-to-spectrum mappings.
- Ground-truth specifications must be available (from metadata, CardinalIO examples, or instrument documentation); verification cannot succeed without a reference.
- This skill applies only to rectangular (dense) imzML layouts; sparse or irregular pixel arrangements may require alternative validation strategies.
- Cardinal 3.6 introduced breaking changes to the class hierarchy (SpectralImagingData, SpectralImagingArrays, SpectralImagingExperiment); version-specific class names and accessors may differ.

## Evidence

- [other] research_question_confirmation: "Does readMSIData() correctly parse a 'continuous' imzML file from CardinalIO as an MSImagingExperiment object with the expected dimensions of 9 spectra and 8,399 m/z values per spectrum?"
- [other] finding_dimensional_validation: "Reading the CardinalIO 'continuous' example imzML file with readMSIData() returns an MSImagingExperiment object containing 9 mass spectra each with 8,399 m/z values, where all spectra share the same"
- [other] workflow_verification_steps: "Verify the object structure: confirm class is MSImagingExperiment, inspect dimensions to confirm 9 spectra (pixels) and 8,399 m/z features per spectrum, and validate spectral data integrity."
- [intro] readMSIData_support: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] class_hierarchy_redesign: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] cardinalio_example_data: "We can read an example of a continuous imzML file from the CardinalIO package"
