---
name: effective-mobility-transformation
description: Use when you have raw CE-MS data (mzML or netCDF format) with migration
  time measurements and need to establish a reproducible compound-specific axis that
  is independent of run-to-run electroosmotic flow fluctuations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MobilityTransformR
  - Spectra
  - xcms
  - MetaboCoreUtils
  - MSnbase
  - R
  - ROMANCE
  techniques:
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# effective-mobility-transformation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transform CE-MS migration time data to effective mobility (µeff) scale to account for electroosmotic flow variations and produce highly reproducible peak positions across electrophoretic runs. This is essential for compound identification and quantification in capillary electrophoresis–mass spectrometry when migration times alone are unstable.

## When to use

You have raw CE-MS data (mzML or netCDF format) with migration time measurements and need to establish a reproducible compound-specific axis that is independent of run-to-run electroosmotic flow fluctuations. Apply this skill when comparing peaks across multiple CE-MS runs or when absolute peak positions must be stable for reliable extracted ion electropherogram generation and peak boundary identification.

## When NOT to use

- Input is CE-UV data, not CE-MS; effective mobility transformation for CE-UV is more straightforward and does not require specialized CE-MS software.
- Compound migration time is already stable across runs (e.g., high-pH separation with negligible EOF drift); transformation adds no reproducibility benefit.
- Analysis requires only qualitative peak detection without cross-run retention time alignment; raw migration time axis is sufficient.

## Inputs

- CE-MS raw data in mzML or netCDF format
- Target m/z value(s) for ion extraction
- Mass tolerance (ppm)
- Effective mobility window range (mm²/(kV·min))

## Outputs

- Extracted ion electropherogram plotted on µeff scale
- Peak records: µeff position, peak intensity, peak area
- Single file containing positive and negative effective mobilities
- Peak boundary coordinates on effective mobility axis

## How to apply

Load CE-MS raw data containing your analyte(s) of interest using Spectra or MSnbase libraries. Use MobilityTransformR to apply effective mobility transformation, which converts the migration time axis to the µeff scale (in mm²/(kV·min)) by accounting for electroosmotic flow variations specific to your electrophoretic system. Extract the ion trace for your target m/z value with specified mass tolerance using xcms or MetaboCoreUtils, filtering to your analysis window (e.g., 1000–2500 mm²/(kV·min) for Lysine). Generate the extracted ion electropherogram on the transformed µeff axis, identify peak boundaries, and export peak records (µeff position, intensity, area) as a data table. The output is a single file containing both positive and negative effective mobilities, enabling direct cross-run peak comparison.

## Related tools

- **MobilityTransformR** (Performs effective mobility transformation on CE-MS(/MS) data, converting migration time to µeff scale while accounting for electroosmotic flow variations) — https://github.com/LiesaSalzer/MobilityTransformR
- **Spectra** (Loads and manages CE-MS raw data (mzML/netCDF); provides container for mass spectrometry data)
- **MSnbase** (Alternative library for loading and handling CE-MS raw data; integrates with transformation workflow)
- **xcms** (Extracts ion traces for specified m/z values with mass tolerance; filters data to mobility windows)
- **MetaboCoreUtils** (Provides core metabolomics utilities; supports ion extraction and filtering operations within transformation pipeline)
- **ROMANCE** (Earlier open-source software model for effective mobility transformation; MobilityTransformR improves workflow by consolidating positive and negative mobilities into single output file)

## Examples

```
library(MobilityTransformR); library(Spectra); data <- readMsData('lysine_CEMS.mzML'); data_transformed <- transformEffectiveMobility(data); eie <- extractIon(data_transformed, mz=147.112806, tolerance=0.01, mobilityRange=c(1000, 2500))
```

## Evaluation signals

- Extracted ion electropherogram shows a single, sharp peak within the specified µeff window (e.g., 1000–2500 mm²/(kV·min) for Lysine at m/z 147.112806) with clear peak boundaries on the transformed axis.
- Peak position (µeff value) remains consistent across multiple CE-MS runs from the same electrophoretic system, whereas raw migration time values show drift.
- Output file contains both positive and negative effective mobility values in a single consolidated record, not separated into two files.
- Peak intensity and area values are reproducible (low run-to-run variance) when plotted on µeff axis compared to raw migration time axis.
- Mass tolerance filtering correctly isolates the target ion; no m/z interferences or artifacts appear in the extracted electropherogram.

## Limitations

- Effective mobility transformation for CE-MS is more complex than for CE-UV; prior to MobilityTransformR, no R implementation existed for this specific application.
- Transformation accuracy depends on stable and well-characterized electroosmotic flow in the electrophoretic system; systems with poorly defined or highly variable EOF may yield less reproducible µeff values.
- The skill requires high-quality raw CE-MS data; data with poor signal-to-noise ratio or significant EOF fluctuations may produce unreliable peak boundaries on the µeff axis.

## Evidence

- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system"
- [intro] will result in highly reproducible peaks, which has already been shown in 2001: "will result in highly reproducible peaks"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R"
- [intro] However, the outputs are two separate files, each for positive and negative mobilities... the output will be a single file containing both, the positive and negative effective mobilities: "the output will be a single file containing both, the positive and negative effective mobilities"
- [other] Lysine (mz = 147.112806) can be extracted and visualized as an EIE on the effective mobility scale, with the chromatogram plotted over the µeff range 1000–2500 mm²/(kV·min): "with the chromatogram plotted over the µeff range 1000–2500 mm²/(kV·min)"
