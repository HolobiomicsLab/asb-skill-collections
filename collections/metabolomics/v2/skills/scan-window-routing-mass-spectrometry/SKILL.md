---
name: scan-window-routing-mass-spectrometry
description: Use when when processing LC-MS data with multiple overlapping m/z scan
  windows and observing sawtooth-pattern distortions in EICs during tardisPeaks()
  execution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - xcms
  - Spectra
  - R
  - knitr
  - TARDIS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# scan-window-routing-mass-spectrometry

## Summary

A quality-control technique for LC-MS targeted metabolomics that segregates overlapping m/z scan windows by mass range to eliminate sawtooth artefacts in extracted ion chromatograms (EICs). Proper routing ensures clean peak profiles during automated integration in TARDIS.

## When to use

When processing LC-MS data with multiple overlapping m/z scan windows and observing sawtooth-pattern distortions in EICs during tardisPeaks() execution. This artefact appears because empty spectra within TARDIS filtering cause discontinuities in the chromatographic signal across scan windows that share m/z ranges without separation logic.

## When NOT to use

- When LC-MS data contains only non-overlapping m/z scan windows (sawtooth artefact will not occur)
- When input files are already in processed feature-table format rather than raw mzML
- When peak integration is not the downstream goal; mass_range separation is not needed for screening-mode visibility checks alone

## Inputs

- centroided mzML files
- Spectra object loaded from mzML vignettes
- target list data.frame with columns: compound ID, compound name, m/z, RT (minutes), polarity

## Outputs

- EIC (Extracted Ion Chromatogram) plots without sawtooth artefacts
- clean chromatographic peak profiles suitable for automated integration
- results list containing data.frame with AUC per target per run

## How to apply

After loading centroided mzML data as Spectra objects and defining a target list with compound ID, name, m/z, RT, and polarity columns, execute tardisPeaks() with an explicitly configured mass_range argument that assigns each scan window to a distinct m/z range rather than allowing windows to overlap without separation. The mass_range parameter must route scan windows so that filtering of empty spectra does not create gaps in the EIC trace. Re-run tardisPeaks() with the corrected mass_range configuration and visually compare the resulting EIC plots against the original artefactual output to confirm elimination of sawtooth profiles and restoration of continuous peak shape.

## Related tools

- **TARDIS** (Executes tardisPeaks() function with mass_range routing to separate overlapping scan windows and generate EICs) — https://github.com/pablovgd/TARDIS
- **xcms** (Provides retention time correction algorithm used within TARDIS for peak detection)
- **Spectra** (R class for loading and managing MS data from mzML files prior to tardisPeaks() execution)
- **knitr** (Visualization and output of EIC plots for comparison of artefact presence/absence)

## Examples

```
tardisPeaks(file_paths = c('sample1.mzML', 'sample2.mzML'), target_list = targets_df, mass_range = list(c(100, 250), c(250, 400)), screening_mode = FALSE)
```

## Evaluation signals

- EIC plots show continuous, smooth chromatographic peak profiles without sawtooth discontinuities after mass_range segregation
- Comparison of before/after EIC outputs demonstrates visual elimination of the sawtooth pattern
- Peak quality metrics (AUC, max intensity, SNR, peak_cor) are stable and unaffected by scan-window filtering
- No gaps or missing data points appear in the extracted ion trace across the retention time window of interest
- Results data.frame contains non-zero AUC values for all targets without spurious intensity drops caused by empty-spectra filtering

## Limitations

- Sawtooth artefacts only manifest when multiple m/z scan windows overlap without mass_range separation; proper parameter configuration is prerequisite knowledge
- The fix requires manual re-execution and visual comparison of EIC plots; automated artefact detection is not provided in TARDIS
- No changelog is documented in the TARDIS repository, limiting traceability of mass_range routing behavior changes across versions

## Evidence

- [other] Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS.: "Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS."
- [other] Does the sawtooth artefact appear in extracted ion chromatogram (EIC) output when tardisPeaks() is run on LC-MS data with multiple overlapping m/z scan windows without proper mass_range separation?: "Does the sawtooth artefact appear in extracted ion chromatogram (EIC) output when tardisPeaks() is run on LC-MS data with multiple overlapping m/z scan windows without proper mass_range separation?"
- [other] Re-execute tardisPeaks() with correct mass_range argument routing to segregate scan windows by mass range, producing clean chromatographic peak profiles.: "Re-execute tardisPeaks() with correct mass_range argument routing to segregate scan windows by mass range, producing clean chromatographic peak profiles."
- [intro] compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
