---
name: ce-ms-migration-time-to-mobility-transformation
description: Use when your CE-MS dataset exhibits migration time drift between runs
  due to electroosmotic flow (EOF) variation, and you have identified two internal
  mobility markers (e.g., Paracetamol and Procaine) with known charges whose migration
  times can be measured in the raw data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# ce-ms-migration-time-to-mobility-transformation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transform capillary electrophoresis–mass spectrometry (CE-MS) data from migration time scale to effective mobility scale using two-marker calibration, enabling reproducible peak alignment across runs despite electroosmotic flow variations. This skill applies the mobilityTransform function to OnDiskMSnExp objects and outputs unified .mzML files containing both positive and negative effective mobilities.

## When to use

Your CE-MS dataset exhibits migration time drift between runs due to electroosmotic flow (EOF) variation, and you have identified two internal mobility markers (e.g., Paracetamol and Procaine) with known charges whose migration times can be measured in the raw data. Use this skill when you need to align peaks across multiple CE-MS files on a physically stable scale for downstream feature detection or when reproducibility of peak positions is critical.

## When NOT to use

- Your CE-MS data lacks identified internal mobility markers or their migration times cannot be reliably extracted from the raw data
- You only have one marker available (the method requires two-marker calibration for robust transformation)
- Your data is already in effective mobility scale or has been processed by another transformation software (applying transformation twice will introduce artifacts)

## Inputs

- OnDiskMSnExp object (from MSnbase, loaded from raw CE-MS data in netCDF or mzML format)
- Two-marker calibration data.frame with columns: rtime, fileIdx, markerID, mobility

## Outputs

- .mzML file containing transformed CE-MS spectra with effective mobility scale (single file covering both polarities)
- OnDiskMSnExp object with transformed migration times (optional intermediate)

## How to apply

First, construct a two-marker calibration data.frame containing columns: rtime (observed migration time in seconds), fileIdx (file index), markerID (marker name), and mobility (charge-based effective mobility value). Load your raw CE-MS data as an OnDiskMSnExp object using MSnbase::readMSData(). Apply MobilityTransformR::mobilityTransform() with the marker data.frame as input; the function internally uses the two markers to compute a linear transformation equation that converts all migration times in the OnDiskMSnExp to effective mobility values on a unified scale. Export the transformed object using MSnbase::writeMSData() with copy=FALSE to generate a single .mzML file; unlike ROMANCE, this outputs one file containing both positive and negative effective mobilities rather than two separate files.

## Related tools

- **MobilityTransformR** (Core package providing mobilityTransform() function for migration time to effective mobility conversion) — https://github.com/LiesaSalzer/MobilityTransformR
- **MSnbase** (Loads raw CE-MS data as OnDiskMSnExp objects and exports transformed data via writeMSData())
- **MetaboCoreUtils** (Provides underlying transformation utilities leveraged by MobilityTransformR)
- **xcms** (Optional downstream package for feature detection on mobility-transformed spectra)
- **Spectra** (Spectral data representation layer used in transformation pipeline)

## Examples

```
library(MobilityTransformR); markers <- data.frame(rtime=c(120, 240), fileIdx=c(1, 1), markerID=c('Paracetamol', 'Procaine'), mobility=c(-4.5, -6.2)); onDiskExp <- MSnbase::readMSData('raw_ce_ms.mzML', mode='onDisk'); transformed <- mobilityTransform(onDiskExp, markers); MSnbase::writeMSData(transformed, file='transformed.mzML', copy=FALSE)
```

## Evaluation signals

- Output .mzML file is valid and readable by standard MS data parsers; check file size is reasonable and contains expected number of spectra
- Effective mobility values in output span expected range for your compound class (e.g., negative and positive ion mobilities are both present if input had both polarities)
- Peaks from the same compound across different input files now align at the same effective mobility value (within instrumental precision), whereas migration times would have drifted
- The two marker compounds appear at their expected effective mobility positions in the transformed data (verify via extracted ion chromatogram or spectrum browser)
- Comparison of transformed data with ROMANCE output (if available) shows identical effective mobility values but MobilityTransformR output is a single .mzML instead of two separate files

## Limitations

- Effective mobility transformation for CE-MS is more complex than for CE-UV; the two-marker approach assumes linearity of the migration time to mobility relationship across the entire electropherogram
- Marker selection is critical—markers must be well-resolved, ionize reproducibly, and span the expected migration time range; poor marker choice will propagate transformation error across all compounds
- No R implementation existed before MobilityTransformR, so the method is relatively new in the ecosystem and may not be compatible with all downstream CE-MS analysis pipelines
- The method requires that marker migration times be measured and known a priori; automated marker detection is not built into MobilityTransformR

## Evidence

- [intro] Effective mobility remains stable in the same electrophoretic system: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] Two-marker calibration required for transformation: "accepts an OnDiskMSnExp object and a marker data.frame containing rtime, fileIdx, markerID, and mobility columns for two markers"
- [intro] Single .mzML output includes both polarities: "However, the outputs are two separate files, each for positive and negative mobilities... the output will be a single file containing both, the positive and negative effective mobilities"
- [intro] No prior R implementation for CE-MS mobility transformation: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [readme] Installation via BiocManager: "To install MobilityTransformR, use the stable version available at Bioconductor. Enter: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager");"
