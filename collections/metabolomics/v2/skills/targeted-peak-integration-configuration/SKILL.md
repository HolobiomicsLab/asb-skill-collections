---
name: targeted-peak-integration-configuration
description: Use when when performing targeted quantification of known compounds in
  LC-MS data using TARDIS, especially when the instrument acquired data with multiple
  overlapping m/z scan windows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0130
  - http://edamontology.org/topic_3370
  tools:
  - xcms
  - Spectra
  - R
  - knitr
  - TARDIS
  - ProteoWizard / MSConvert
  - knitr / kableExtra
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms`
  package
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- R package for *TArgeted Raw Data Integration In Spectrometry*
- knitr::include_graphics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# targeted-peak-integration-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and validate input parameters for targeted peak detection and integration in LC-MS data, including proper m/z window segregation, target list definition, and screening to ensure artifact-free extraction of ion chromatograms. This skill prevents sawtooth artefacts and ensures correct peak profiling by routing scan windows through accurate mass_range separation.

## When to use

When performing targeted quantification of known compounds in LC-MS data using TARDIS, especially when the instrument acquired data with multiple overlapping m/z scan windows. Specifically: (1) you have centroided mzML files and a list of target compounds with known m/z, retention time, and polarity; (2) you need to avoid sawtooth artefacts in extracted ion chromatograms (EICs) caused by improper segregation of overlapping scan windows; (3) you want to screen target visibility before full peak detection across all runs.

## When NOT to use

- Input files are already in non-centroided format (profile mode) without prior centroiding—TARDIS requires centroided mzML files
- Target list lacks m/z precision or retention time windows (TARDIS requires all four columns: ID, name, m/z, RT, polarity) to define mass_range and time windows
- Analysis goal is discovery or untargeted screening rather than quantification of predefined compounds

## Inputs

- Centroided mzML files (LC-MS raw data)
- Spectra objects (MS data loaded as Bioconductor Spectra)
- Target list data.frame with columns: compound ID, compound name, m/z, retention time (minutes), polarity

## Outputs

- Extracted ion chromatogram (EIC) plots with visual confirmation of artefact presence/absence
- Configuration validation report confirming scan-window routing correctness
- Peak detection results (area under curve, max intensity, SNR, peak_cor, points over peak) in subsequent tardisPeaks() execution

## How to apply

First, prepare a target list as a data.frame with columns for compound ID, compound name, theoretical or measured m/z, expected retention time (in minutes), and polarity (positive/negative). Load centroided mzML files as Spectra objects using the xcms/Spectra framework. Execute tardisPeaks() in screening_mode = TRUE to verify that targets are visible within the defined m/z and RT windows; this step reveals whether mass_range parameters are correctly segregating overlapping scan windows. If EIC plots show sawtooth profiles during screening, adjust the mass_range argument to ensure each scan window is routed separately rather than merged. Once screening passes without artefacts, set screening_mode = FALSE and run peak detection across all samples. The key rationale is that TARDIS filters empty spectra internally; without proper mass_range separation, filtering creates artificial gaps in the EIC, producing the sawtooth profile. Verify clean chromatography by comparing EICs before and after correct mass_range routing.

## Related tools

- **TARDIS** (Main R package for targeted peak integration and configuration; executes tardisPeaks() with mass_range routing and screening modes) — https://github.com/pablovgd/TARDIS
- **xcms** (Provides retention time correction algorithm used internally by TARDIS for chromatographic alignment)
- **Spectra** (Bioconductor package for MS data representation; TARDIS loads mzML files as Spectra objects for downstream processing)
- **ProteoWizard / MSConvert** (File conversion tool to prepare raw vendor formats as centroided mzML input)
- **knitr / kableExtra** (Used for rendering and displaying EIC plots and results tables in reports)

## Examples

```
library(TARDIS); targets <- data.frame(ID=c('cmp1','cmp2'), Name=c('Compound1','Compound2'), mz=c(200.0523, 250.1234), RT=c(5.2, 7.8), polarity=c('pos','pos')); results <- tardisPeaks(files='data/sample.mzML', targets=targets, mass_range=list(c(199.5,200.5), c(249.5,250.5)), screening_mode=TRUE)
```

## Evaluation signals

- EIC plots generated during screening_mode = TRUE show smooth, unimodal peak profiles without sawtooth artefacts
- Comparison of 'before' (incorrect mass_range) and 'after' (correct mass_range) EIC plots visually confirms removal of sawtooth structure
- All target compounds are detected in screening output (targets visible within m/z and RT windows as defined)
- Peak quality metrics (SNR, peak_cor, points over peak) are consistent and above expected thresholds after configuration validation
- Polarity filtering within TARDIS correctly segregates positive and negative mode targets without cross-contamination

## Limitations

- Configuration correctness depends critically on accurate m/z and retention time values in the target list; incorrect window definitions will still produce artefacts or miss peaks
- Sawtooth artefacts arise specifically from filtering of empty spectra within TARDIS when overlapping scan windows are not properly segregated; this limitation is instrument-specific and may not apply to non-windowed or single-window acquisitions
- No changelog is available for TARDIS, limiting visibility into past configuration parameter changes or known issues that may affect specific use cases
- Centroiding is a strict requirement; profile-mode (non-centroided) mzML files will not be processed correctly and must be converted before configuration

## Evidence

- [other] Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation: "Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS."
- [intro] Configuration requires target list data frame with compound ID, name, m/z, RT, and polarity columns: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [intro] Centroided mzML files are mandatory input format: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Screening mode validates target visibility before full peak detection: "perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [intro] Spectra objects are the standard data representation for TARDIS integration: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [results] EICs are visually inspected to confirm proper configuration: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] Polarity filtering is handled within TARDIS automatically: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
