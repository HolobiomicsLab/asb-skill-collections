---
name: unified-mobility-scale-construction-across-polarities
description: Use when you have CE-MS raw data in OnDiskMSnExp format with both positive and negative polarity acquisitions, migration times that vary due to electroosmotic flow drift, and access to two well-characterized mobility markers (e.g., Paracetamol and Procaine with known charges and migration times).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MobilityTransformR
  - MSnbase
  - MetaboCoreUtils
  - xcms
  - Spectra
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data
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
---

# unified-mobility-scale-construction-across-polarities

## Summary

Transform CE-MS migration time data to a unified effective mobility scale spanning both positive and negative polarities using two-marker calibration. This produces a single polarity-agnostic .mzML file with reproducible, system-independent mobility values replacing migration times.

## When to use

You have CE-MS raw data in OnDiskMSnExp format with both positive and negative polarity acquisitions, migration times that vary due to electroosmotic flow drift, and access to two well-characterized mobility markers (e.g., Paracetamol and Procaine with known charges and migration times). Use this skill when you need to align and compare peaks across runs or polarities without re-optimizing separation conditions.

## When NOT to use

- Your CE-MS data is already in effective mobility scale (already calibrated); re-applying this skill will introduce spurious double-transformation.
- You have only one polarity in your dataset; simpler single-polarity transformation methods may be more appropriate.
- Your two markers lack reliable literature or experimentally determined mobility values; the calibration will be unreliable.

## Inputs

- OnDiskMSnExp object (CE-MS raw data in memory-mapped format)
- two-marker calibration data.frame with columns: rtime, fileIdx, markerID, mobility

## Outputs

- .mzML file containing both positive and negative effective mobilities on unified scale
- transformed OnDiskMSnExp object with migration time axis replaced by effective mobility axis

## How to apply

Construct a calibration data.frame containing rtime, fileIdx, markerID, and mobility columns for your two chosen markers, recording their migration times and their effective mobility values (computed from their charge and known system parameters). Load the CE-MS raw data as an OnDiskMSnExp object using MSnbase. Call mobilityTransform() from MobilityTransformR with the OnDiskMSnExp object and marker data.frame; the function will fit a transformation model across both polarities and rescale all migration times to effective mobility units on a unified scale. Export the transformed OnDiskMSnExp to a single .mzML file using writeMSData(..., copy=FALSE), which will contain both positive and negative effective mobilities in one file. Verify that the output .mzML file contains both polarities and that effective mobility values are stable across replicate runs.

## Related tools

- **MobilityTransformR** (core package implementing mobilityTransform() function for two-marker effective mobility transformation) — https://github.com/LiesaSalzer/MobilityTransformR
- **MSnbase** (loads and represents CE-MS raw data as OnDiskMSnExp objects for transformation)
- **MetaboCoreUtils** (provides utility functions underlying the transformation computation)
- **xcms** (supports feature detection and peak alignment on transformed effective mobility scale)
- **Spectra** (represents and manipulates spectrum metadata during mobility transformation)

## Examples

```
markers_df <- data.frame(rtime=c(450, 520), fileIdx=1, markerID=c('Paracetamol','Procaine'), mobility=c(2.1e-4, 3.5e-4)); transformed <- mobilityTransform(msnexp, markers_df); writeMSData(transformed, file='unified_mobilities.mzML', copy=FALSE)
```

## Evaluation signals

- Output .mzML file is valid and readable; readMSData() can load it without errors and returns an OnDiskMSnExp with both positive and negative spectra.
- All migration time (rtime) values in the transformed object are replaced with effective mobility values; new rtime scale is approximately linear and monotonic.
- Effective mobility scale is unified: positive and negative polarity spectra occupy the same m/z × mobility space without separate files.
- Peak reproducibility is improved: replicate CE-MS runs show higher correlation of peak intensities at matched effective mobility coordinates compared to raw migration time.
- The two calibration markers appear at their literature effective mobility values (within 5% tolerance) in the transformed output.

## Limitations

- Requires two well-characterized mobility markers with known charges and stable migration times; poor marker selection or degradation will propagate large systematic errors.
- Transformation assumes the effective mobility–charge–migration-time relationship is linear across the migration time range; non-linearity or high electroosmotic flow variation will reduce accuracy.
- Unlike the ROMANCE software reference implementation, MobilityTransformR produces a single unified file; workflows expecting separate positive/negative files will require post-processing.
- Effective mobility transformation is more complex for CE-MS than CE-UV because both migration time and mass-to-charge dimensions must be preserved simultaneously.

## Evidence

- [other] The mobilityTransform function accepts an OnDiskMSnExp object and a marker data.frame containing rtime, fileIdx, markerID, and mobility columns for two markers: "the mobilityTransform function accepts an OnDiskMSnExp object and a marker data.frame containing rtime, fileIdx, markerID, and mobility columns for two markers"
- [intro] Effective mobility remains stable in the same electrophoretic system, whereas migration times show fluctuations due to electroosmotic flow variations: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] Output is a single file containing both positive and negative effective mobilities, unlike ROMANCE which produces two separate files: "the output will be a single file containing both, the positive and negative effective mobilities"
- [intro] Using effective mobility scale instead of migration time scale produces highly reproducible peaks in CE-MS analysis: "will result in highly reproducible peaks, which has already been shown in 2001"
- [intro] There was no R implementation for effective mobility transformation of CE-MS data before MobilityTransformR: "until now and to our knowledge there is no implementation in R that performs effective mobility"
- [readme] Installation via BiocManager from stable Bioconductor release or development version via devtools: "To install MobilityTransformR, use the stable version available at Bioconductor"
