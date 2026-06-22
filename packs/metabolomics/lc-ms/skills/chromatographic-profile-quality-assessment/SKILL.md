---
name: chromatographic-profile-quality-assessment
description: Use when running targeted peak detection on LC-MS data acquired with multiple overlapping m/z scan windows and observing distorted or periodically discontinuous peak profiles in EIC plots.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - Spectra
  - R
  - knitr
  - TARDIS
  - ProteoWizard/MSConvert
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms` package
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-profile-quality-assessment

## Summary

Identify and diagnose artefacts (e.g. sawtooth profiles) in extracted ion chromatograms (EICs) produced by peak-detection workflows on LC-MS data with complex scan-window configurations. This skill detects when improper mass-range separation causes filtering of empty spectra within the processing pipeline, degrading peak profile quality.

## When to use

Apply this skill when running targeted peak detection on LC-MS data acquired with multiple overlapping m/z scan windows and observing distorted or periodically discontinuous peak profiles in EIC plots. The sawtooth artefact surfaces specifically when tardisPeaks() processes data without proper mass_range argument routing to segregate scan windows by mass range.

## When NOT to use

- Input data is acquired with single, non-overlapping m/z scan windows—sawtooth artefacts do not occur in this simpler configuration.
- EIC output already displays clean, continuous peak profiles—the skill is redundant if the artefact is absent.
- Raw data has not been centroided or is in non-mzML format—the skill requires preprocessed, standardized input.

## Inputs

- centroided mzML files (LC-MS raw data)
- Spectra objects (loaded from mzML)
- target list data.frame (columns: compound ID, name, m/z, RT, polarity)

## Outputs

- EIC plots (Extracted Ion Chromatogram visualizations)
- visual comparison of peak profiles (with/without artefacts)
- diagnostic assessment of mass_range parameter configuration

## How to apply

Execute tardisPeaks() twice: first with multi-window mass_range configuration *without* scan-window separation enabled, then re-execute with corrected mass_range argument routing that segregates scan windows by mass range. Load centroided mzML files as Spectra objects and define a target list data.frame with compound ID, name, m/z, RT, and polarity columns. Generate and visually inspect EIC plots from both runs side-by-side: the first should exhibit sawtooth profiles (jagged, discontinuous intensity baseline) while the second should display clean, continuous peak profiles. The artefact arises because improper mass_range configuration causes TARDIS to filter empty spectra within individual scan windows, creating gaps in the EIC that render as sawtooth discontinuities. Correct mass_range separation ensures all spectra are retained and properly integrated across overlapping windows.

## Related tools

- **TARDIS** (performs targeted peak detection and EIC generation; exposes mass_range parameter controlling scan-window segregation) — https://github.com/pablovgd/TARDIS
- **Spectra** (loads and represents centroided MS data in memory; integrates with TARDIS workflow)
- **xcms** (provides retention-time correction algorithm underlying TARDIS processing)
- **ProteoWizard/MSConvert** (converts proprietary MS file formats to centroided mzML for input to TARDIS)

## Examples

```
library(TARDIS); targets <- data.frame(cmpd_id=c('A','B'), name=c('CompA','CompB'), mz=c(200.05,250.10), rt=c(5.2,8.1), polarity=c('positive','positive')); result_bad <- tardisPeaks(file_path='data.mzML', targets=targets, mass_range=c(150,350)); result_good <- tardisPeaks(file_path='data.mzML', targets=targets, mass_range=list(c(150,250),c(200,350)));
```

## Evaluation signals

- Visual inspection of EIC plots: incorrect mass_range configuration produces sawtooth (jagged, periodic discontinuities in baseline intensity); correct configuration yields smooth, continuous peak profiles.
- Consistency of peak profile shape across replicate runs with identical correct mass_range configuration—repeated runs should produce visually identical EICs.
- Presence/absence of empty spectra filtering artifacts: log or debug output from tardisPeaks() should indicate no empty-spectra filtering when mass_range segregation is properly configured.
- Peak integration metrics (AUC, max intensity, SNR) should be stable and reproducible when mass_range is corrected; unstable metrics with sawtooth profiles suggest uncontrolled artefact.
- Comparison of EIC appearance before and after mass_range correction: the same compound should show visibly discontinuous intensity baseline before correction and smooth baseline after.

## Limitations

- The sawtooth artefact is specific to multi-window m/z acquisition schemes; single-window data will not exhibit this failure mode.
- Visual inspection of EIC plots is the primary diagnostic method—no automated detection algorithm is documented in the article, so assessment is subjective and operator-dependent.
- The skill assumes the user can correctly specify the mass_range parameter; no automated validation or suggestion mechanism is mentioned in the README or article.
- EIC quality depends on upstream data preprocessing (centroiding, format conversion); corrupted or poorly centroided mzML files may exhibit spurious artefacts unrelated to mass_range configuration.

## Evidence

- [full_text] sawtooth_artefact_definition: "Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS."
- [intro] eic_workflow_step: "Execute tardisPeaks() with multi-window mass_range configuration without scan-window separation enabled, generating EIC plots that exhibit sawtooth artefacts."
- [full_text] correction_method: "Re-execute tardisPeaks() with correct mass_range argument routing to segregate scan windows by mass range, producing clean chromatographic peak profiles."
- [intro] target_list_specification: "Define a target list data.frame with compound ID, name, m/z, RT, and polarity columns."
- [full_text] eic_output_inspection: "Save both sets of EIC plots and inspect for artefact presence/absence as visual confirmation of scan-window routing impact."
- [intro] centroided_input_requirement: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] polarity_filtering_automatic: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
