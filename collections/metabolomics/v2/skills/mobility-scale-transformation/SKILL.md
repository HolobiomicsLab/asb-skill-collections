---
name: mobility-scale-transformation
description: Use when analyzing CE-MS(/MS) data where electroosmotic flow fluctuations cause variable migration times for the same compounds across runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MobilityTransformR
  - R
  - Spectra
  - xcms
  - MetaboCoreUtils
  - MSnbase
  - ROMANCE
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("Spectra")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
- The MT of the peak will be determined by `findChromPeaks` from `xcms`.
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

# mobility-scale-transformation

## Summary

Transform CE-MS migration time data to effective mobility (µeff) scale using calibration with internal EOF markers, producing reproducible compound peaks independent of electroosmotic flow variations. This skill is essential when CE-MS analyses show migration time drift caused by EOF instability, requiring normalization to a stable physicochemical property for reliable peak alignment and quantification across runs.

## When to use

Apply this skill when analyzing CE-MS(/MS) data where electroosmotic flow fluctuations cause variable migration times for the same compounds across runs. Use it when you have: (1) CE-MS raw data (mzML or netCDF format) with known reference marker(s) and their effective mobilities, (2) metadata on experimental parameters (applied voltage U in kV, capillary length L in mm, electrical field ramp time tR in minutes), and (3) a need for reproducible compound identification and quantification on a migration-time-independent scale. Avoid this skill if your data are already aligned to an effective mobility scale or if you lack calibration markers with assigned µeff values.

## When NOT to use

- Input data are already expressed on an effective mobility scale or have been pre-aligned by another method.
- No reference marker or calibration standard with known effective mobility is available for the analysis.
- CE-UV (capillary electrophoresis–ultraviolet) data, as the transformation procedure differs fundamentally from CE-MS and does not require MobilityTransformR.

## Inputs

- CE-MS raw data file (mzML or netCDF format)
- Marker data frame with columns: marker name, migration time (min), assigned effective mobility (mm²/(kV·min))
- Experimental parameters: applied voltage U (kV), capillary length L (mm), electrical field ramp time tR (minutes)

## Outputs

- Data frame with effective mobility scale (µeff in mm²/(kV·min)) replacing migration time axis
- Extracted ion electropherogram(s) plotted on µeff scale
- Peak records with retention time on µeff axis, peak intensity, and peak area

## How to apply

Load raw CE-MS data (mzML or netCDF) and extract migration times for your compound(s) of interest and for calibration marker(s) with known effective mobilities. Invoke MobilityTransformR's mobilityTransform function with the experimental parameters: reference marker migration time and µeff, applied voltage (U, in kV), capillary length (L, in mm), and field ramp time (tR, in minutes). The function applies equation 1 (single-marker method) or multi-marker calibration to compute µeff for each compound using: µeff = ((L / (U × tR)) × ((migration_time − t_marker) / (t_marker))) + µ_marker. Output the transformed data as a data frame with migration time on the effective mobility scale (mm²/(kV·min)). Verify transformation by confirming that peak positions for the same compound are now stable across multiple CE-MS runs, and that peaks cluster in expected mobility windows for compound classes (e.g., Lysine in the 1000–2500 mm²/(kV·min) range).

## Related tools

- **MobilityTransformR** (Implements effective mobility transformation using single-marker or multi-marker calibration; computes µeff from migration time and experimental parameters; outputs single file with both positive and negative mobilities.) — https://github.com/LiesaSalzer/MobilityTransformR
- **Spectra** (Loads and manages CE-MS raw data (mzML, netCDF) for extraction and transformation.)
- **MSnbase** (Handles mass spectrometry data objects and supports data retrieval before transformation.)
- **xcms** (Performs peak detection, integration, and filtering on the transformed effective mobility scale.)
- **MetaboCoreUtils** (Provides utility functions for transformation and metabolomics data manipulation within the MobilityTransformR workflow.)
- **ROMANCE** (Open-source software used as a model for MobilityTransformR design; produces two separate files for positive and negative mobilities (contrast: MobilityTransformR outputs single file).)

## Examples

```
library(MobilityTransformR); data <- mobilityTransform(migration_time = procaine_tR, marker_rtime = 3/60, marker_mobility = 0, tR = 3/60, U = 30, L = 800); plot(data$effective_mobility, data$intensity)
```

## Evaluation signals

- Peak positions for the same compound are reproducible across multiple CE-MS runs when plotted on the µeff scale, whereas migration times vary.
- Effective mobility values fall within expected literature ranges for the compound class (e.g., amino acids, cationic compounds in specified voltage/field conditions).
- Extracted ion electropherogram peaks resolve into distinct clusters within defined mobility windows (e.g., Lysine in 1000–2500 mm²/(kV·min)) with no overlap with off-target m/z signals.
- Marker calibration point(s) map correctly: the input marker migration time and assigned µeff produce zero residual error when back-calculated through the transformation equation.
- Output data frame schema matches input requirements: contains µeff column (numeric, units mm²/(kV·min)), peak intensity, peak area, and identifiers for compound and run.

## Limitations

- Effective mobility transformation for CE-MS is more complex than for CE-UV and requires precise knowledge of experimental parameters (U, L, tR) and at least one calibration marker with known µeff.
- If electroosmotic flow is severely suppressed or unstable, single-marker calibration may be insufficient; multi-marker or higher-order calibration strategies may be needed.
- Output is a single file containing both positive and negative effective mobilities, which differs from ROMANCE (two separate files); downstream filtering or separation of polarity may be required depending on workflow.
- Transformation assumes constant electrical field ramp time (tR) and applied voltage (U) throughout the run; variations in these parameters during acquisition are not accounted for and will introduce systematic error.

## Evidence

- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] will result in highly reproducible peaks, which has already been shown in 2001: "will result in highly reproducible peaks, which has already been shown in 2001"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [intro] However, the outputs are two separate files, each for positive and negative mobilities... the output will be a single file containing both, the positive and negative effective mobilities: "the output will be a single file containing both, the positive and negative effective mobilities"
- [other] The mobilityTransform function computes Procaine's effective mobility using equation 1 (single marker method) with the Paracetamol EOF marker as reference, requiring inputs of migration time, marker rtime and mobility, electrical field ramp time (tR), applied voltage (U), and capillary length (L).: "The mobilityTransform function computes Procaine's effective mobility using equation 1 (single marker method) with the Paracetamol EOF marker as reference, requiring inputs of migration time, marker"
- [other] Lysine (mz = 147.112806) can be extracted and visualized as an EIE on the effective mobility scale, with the chromatogram plotted over the µeff range 1000–2500 mm²/(kV·min), showing the compound's peak distribution on the transformed mobility axis.: "Lysine (mz = 147.112806) can be extracted and visualized as an EIE on the effective mobility scale, with the chromatogram plotted over the µeff range 1000–2500 mm²/(kV·min), showing the compound's"
- [other] Apply effective mobility transformation to convert migration time to µeff scale using MobilityTransformR, accounting for electroosmotic flow variations.: "Apply effective mobility transformation to convert migration time to µeff scale using MobilityTransformR, accounting for electroosmotic flow variations."
