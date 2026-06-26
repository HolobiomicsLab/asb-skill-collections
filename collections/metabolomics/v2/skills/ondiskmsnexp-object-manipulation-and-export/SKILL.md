---
name: ondiskmsnexp-object-manipulation-and-export
description: Use when you have raw CE-MS data and need to (1) transform migration
  time values to effective mobility using two calibration markers (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0630
  tools:
  - R
  - MobilityTransformR
  - MSnbase
  - MetaboCoreUtils
  - xcms
  - Spectra
  techniques:
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- there is no implementation in R that performs effective mobility transformation
  of CE-MS(/MS) data
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MSnbase")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# OnDiskMSnExp Object Manipulation and Export

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load raw CE-MS data as an OnDiskMSnExp object, apply mobility transformation to convert migration times to effective mobility scale, and export the transformed data to a single .mzML file containing both positive and negative ion modes. This skill bridges memory-efficient in-memory representation with standardized output formats for downstream analysis.

## When to use

You have raw CE-MS data and need to (1) transform migration time values to effective mobility using two calibration markers (e.g., Paracetamol and Procaine with known charges and migration times), (2) preserve both positive and negative ion modes in a unified coordinate system, and (3) export to a portable .mzML format for sharing or further processing. Apply this when electroosmotic flow variations cause migration time fluctuations but effective mobility remains stable within your electrophoretic system.

## When NOT to use

- Input data are already in effective mobility coordinates — applying transformation twice will corrupt the scale.
- You have fewer than two calibration markers with known mobility values; the linear transformation requires at least two reference points.
- Raw data are in NetCDF or other non-OnDiskMSnExp formats without prior conversion via MSnbase import.
- You require separate output files for positive and negative modes; MobilityTransformR produces a single consolidated .mzML by design.

## Inputs

- OnDiskMSnExp object (raw CE-MS run loaded via MSnbase)
- Two-marker calibration data.frame with columns: rtime, fileIdx, markerID, mobility

## Outputs

- OnDiskMSnExp object with transformed migration time scale to effective mobility
- .mzML file containing both positive and negative effective mobilities in unified scale

## How to apply

First, load the raw CE-MS data into an OnDiskMSnExp object using MSnbase functions to enable memory-efficient handling of large runs. Construct a two-marker calibration data.frame containing columns: rtime (migration time in seconds), fileIdx (run index), markerID (character identifier), and mobility (effective mobility value in cm²/V·s) for two reference compounds with known charges. Apply the mobilityTransform function from MobilityTransformR, which accepts the OnDiskMSnExp object and marker data.frame, performing linear interpolation to transform all migration times to the effective mobility scale. The function returns a transformed OnDiskMSnExp object preserving all spectral metadata. Export the result using writeMSData with copy=FALSE parameter to generate a single .mzML file that consolidates positive and negative effective mobilities without duplicating raw data.

## Related tools

- **MobilityTransformR** (Executes the mobilityTransform function to convert migration times to effective mobility using two-marker calibration data) — https://github.com/LiesaSalzer/MobilityTransformR
- **MSnbase** (Loads raw CE-MS data into OnDiskMSnExp objects and provides writeMSData for .mzML export)
- **MetaboCoreUtils** (Provides utility functions underlying the mobility transformation pipeline)
- **Spectra** (Handles spectral data structures and metadata within the transformation workflow)

## Examples

```
# Load raw CE-MS data and apply mobility transformation in R:
library(MSnbase); library(MobilityTransformR)
raw_data <- readMSData('CE-MS-run.raw', mode='onDisk')
markers <- data.frame(rtime=c(120, 240), fileIdx=c(1, 1), markerID=c('Paracetamol', 'Procaine'), mobility=c(45.2, 32.8))
transformed <- mobilityTransform(raw_data, markers)
writeMSData(transformed, file='transformed_data.mzML', copy=FALSE)
```

## Evaluation signals

- The returned OnDiskMSnExp object has rtime values within the expected effective mobility range (typically 0–100 cm²/V·s for small-molecule metabolites), not the original migration time range (seconds).
- Both positive and negative ion modes are present in the output .mzML file as a single consolidated document, not as separate files.
- The .mzML file contains a single unified mobility scale; spot-checking a few m/z peaks shows their mobility values are consistent with known standard compounds.
- No spectral data are duplicated; writeMSData with copy=FALSE produces a file size proportional to the input raw data, not inflated by redundancy.
- The transformation is mathematically consistent: the two marker compounds retain their input mobility values (within numerical precision), confirming correct calibration anchor points.

## Limitations

- Effective mobility transformation for CE-MS data is more complex than for CE-UV due to the multidimensional nature of MS data; two-marker calibration may not capture non-linearity across the full migration time range.
- The transformation requires accurate migration times and marker identities in the calibration data.frame; errors in marker assignment or rtime values will propagate to all transformed data.
- OnDiskMSnExp objects are optimized for large files but require sufficient disk space for the intermediate object representation during transformation.
- The skill assumes the same electrophoretic system is used throughout; different instruments, buffers, or pH conditions will have different effective mobility scales and require new marker calibrations.

## Evidence

- [other] The mobilityTransform function accepts an OnDiskMSnExp object and a marker data.frame containing rtime, fileIdx, markerID, and mobility columns for two markers: "The mobilityTransform function accepts an OnDiskMSnExp object and a marker data.frame containing rtime, fileIdx, markerID, and mobility columns for two markers"
- [other] Transforms the migration time scale to effective mobility scale and returns an OnDiskMSnExp object that can be exported to .mzML format using writeMSData with copy=FALSE parameter: "transforms the migration time scale to effective mobility scale and returns an OnDiskMSnExp object that can be exported to .mzML format using writeMSData with copy=FALSE parameter"
- [intro] The effective mobility µ_eff of a compound remains stable in the same electrophoretic system, whereas migration times show fluctuations due to electroosmotic flow variations: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] MobilityTransformR outputs a single file containing both positive and negative effective mobilities, unlike ROMANCE which produces two separate files: "the output will be a single file containing both, the positive and negative effective mobilities"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV, and until now there is no implementation in R that performs effective mobility transformation before MobilityTransformR: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [intro] The transformation is performed using functionality from the packages MSnbase, MetaboCoreUtils, xcms, and Spectra: "The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`, `r BiocStyle::Biocpkg("xcms")`, `r BiocStyle::Biocpkg("MSnbase")`, `r"
