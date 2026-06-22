---
name: multi-window-mass-range-parameter-optimization
description: Use when you observe sawtooth or discontinuous peak profiles in EICs after running tardisPeaks() on LC-MS data acquired with multiple overlapping or sequential m/z scan windows (e.g., positive and negative polarity scans, or data-independent acquisition with staggered windows).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3636
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - xcms
  - Spectra
  - R
  - knitr
  - TARDIS
  - ProteoWizard (MSConvert)
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

# multi-window-mass-range-parameter-optimization

## Summary

Optimize the mass_range parameter in tardisPeaks() to properly segregate overlapping m/z scan windows and eliminate sawtooth artefacts in extracted ion chromatograms (EICs). This skill ensures that when LC-MS data contain multiple acquisition windows at different m/z ranges, the filtering logic correctly routes each target to its corresponding scan window, preventing spurious peak profile distortion caused by spectrum filtering.

## When to use

Apply this skill when you observe sawtooth or discontinuous peak profiles in EICs after running tardisPeaks() on LC-MS data acquired with multiple overlapping or sequential m/z scan windows (e.g., positive and negative polarity scans, or data-independent acquisition with staggered windows). The artefact manifests as repetitive up-down intensity oscillations in the chromatogram and indicates improper mass_range routing.

## When NOT to use

- Input data are already merged or deconvoluted (e.g., EICs pre-computed), as re-optimization of mass_range will have no effect on stored chromatograms.
- LC-MS acquisition used a single, continuous m/z range with no window switching; mass_range optimization is unnecessary and introduces no benefit.
- Peak profiles are already clean and peak_cor metrics are high; sawtooth artefacts are absent or due to other causes (e.g., column degradation, ion suppression).

## Inputs

- centroided mzML files (as Spectra objects)
- target list data.frame with columns: compound ID, name, m/z, RT, polarity
- LC-MS acquisition metadata describing m/z scan window configuration (ranges, overlap, polarity assignment)

## Outputs

- EIC plots saved to output folder with clean, smooth peak profiles
- results list containing data.frame with AUC per target per run
- tibble with average quality metrics (Max. Int., SNR, peak_cor, points_over_peak) per target in QC runs
- corrected mass_range parameter configuration for downstream reuse

## How to apply

First, load your centroided mzML files as Spectra objects and prepare a target list data.frame with compound ID, name, m/z, RT, and polarity columns. Execute tardisPeaks() with a mass_range argument that explicitly defines non-overlapping m/z intervals for each scan window (e.g., mass_range = list(c(200, 500), c(500, 1000)) for two sequential windows). The key rationale is that TARDIS filters empty spectra during processing; when mass_range is not properly segregated by scan window, targets may fall into gaps where no spectra are available in their assigned window, causing the chromatogram to skip scans and produce sawtooth patterns. After running with corrected mass_range separation, visually inspect the resulting EIC plots and compare peak profile smoothness with the previous run to confirm artefact removal. Validate by checking that peak_cor (peak correlation metric) and points_over_peak counts improve relative to the misconfigured run.

## Related tools

- **TARDIS** (Core package that executes targeted peak integration with configurable mass_range parameter for scan-window routing and EIC generation) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads and manages centroided LC-MS data as in-memory objects before tardisPeaks() processing)
- **xcms** (Provides retention time correction algorithm used internally by TARDIS for chromatographic alignment)
- **ProteoWizard (MSConvert)** (Converts raw vendor LC-MS files to centroided mzML format required as input)
- **knitr** (Renders EIC plot outputs for visual inspection and comparison of peak profile quality before and after optimization)

## Examples

```
tardisPeaks(files = list.files('data/', pattern = '\.mzML$', full.names = TRUE), targets = targets_df, mass_range = list(c(200, 500), c(500, 1000)), screening_mode = FALSE, output_folder = 'results/')
```

## Evaluation signals

- EIC plots exhibit smooth, monotonic peak profiles without sawtooth oscillations or repeated up-down intensity spikes when mass_range is correctly segregated by scan window.
- peak_cor (peak correlation metric) increases relative to the misconfigured run, indicating improved peak shape consistency across retention time points.
- points_over_peak count rises, indicating more spectrum scans are assigned and retained for each target within the optimized mass_range window.
- SNR (signal-to-noise ratio) and Max. Int. values remain stable or improve, confirming no signal loss or integration error introduced by the parameter change.
- Comparison of AUC values before and after optimization shows consistency (within expected biological/analytical variation), ensuring quantification is not distorted by the fix.

## Limitations

- Optimization requires prior knowledge of the LC-MS instrument's scan window configuration (m/z ranges, switching logic, polarity assignment). If this metadata is missing or incorrect, mass_range segregation cannot be tuned accurately.
- Sawtooth artefacts may also arise from other causes (e.g., ion suppression, column carryover, or detector saturation); mass_range optimization will not resolve non-parameter-related peak quality issues.
- Visual inspection of EICs for artefact presence is subjective. Quantitative thresholds for acceptable peak_cor or points_over_peak are not provided in the article; practitioner judgment and QC standards must be applied.

## Evidence

- [other] Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS.: "Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS."
- [other] Re-execute tardisPeaks() with correct mass_range argument routing to segregate scan windows by mass range, producing clean chromatographic peak profiles.: "Re-execute tardisPeaks() with correct mass_range argument routing to segregate scan windows by mass range, producing clean chromatographic peak profiles."
- [intro] automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data: "automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
- [intro] compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [results] The resulting EICs are again saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
