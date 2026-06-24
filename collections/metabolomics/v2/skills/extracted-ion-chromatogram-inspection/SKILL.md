---
name: extracted-ion-chromatogram-inspection
description: Use when after running tardisPeaks() in screening mode or peak detection
  mode, when you need to visually confirm that target compounds are visible in the
  expected m/z and retention time windows, verify that peak integration boundaries
  are correct, diagnose whether sawtooth artefacts are present.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - TARDIS
  - Spectra
  - xcms
  - R
  - MsExperiment
  - knitr
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- R package for *TArgeted Raw Data Integration In Spectrometry*
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- It makes use of an established retention time correction algorithm from the `xcms`
  package
- Alternatively, instead of using file paths as input for TARDIS, the user can also
  use an `MsExperiment` object
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

# extracted-ion-chromatogram-inspection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Visual and qualitative inspection of extracted ion chromatograms (EICs) saved as diagnostic PNG files to assess peak detection quality, identify sawtooth artefacts from overlapping scan windows, and verify target compound visibility within defined m/z and retention time windows in LC–MS metabolomics and lipidomics data.

## When to use

After running tardisPeaks() in screening mode or peak detection mode, when you need to visually confirm that target compounds are visible in the expected m/z and retention time windows, verify that peak integration boundaries are correct, diagnose whether sawtooth artefacts are present (indicating improper mass_range separation in multi-window acquisition), or quality-check diagnostic outputs for QC runs before proceeding to quantitative peak metrics.

## When NOT to use

- When input .mzML files are not centroided; non-centroided data will produce poor peak profiles unsuitable for visual inspection.
- When the target list lacks accurate retention time or m/z windows; EICs will be uninformative if targets fall outside the search window.
- When quantitative peak metrics (AUC, max intensity, SNR, peak correlation) are the primary requirement and visual inspection is not needed for QC.

## Inputs

- Centroided .mzML LC–MS files (14+ runs recommended for representative QC assessment)
- Target list data.frame with columns: compound ID, compound Name, theoretical m/z, expected retention time (minutes), polarity indicator
- MsExperiment object (alternative input: Spectra object + sampleData data.frame with type labels for QC vs. sample distinction)

## Outputs

- Set of individual extracted ion chromatogram (EIC) PNG files, one per target compound, saved to output/screening/Diagnostic_QCs_Batch_*/ folder
- Visual record of peak detection, integration boundaries, and peak annotation for each target
- Diagnostic artefact assessment (presence/absence of sawtooth profiles and integration quality)

## How to apply

Execute tardisPeaks() with your centroided .mzML files (or an MsExperiment object with annotated sampleData$type) and a target list data.frame containing compound ID, name, theoretical m/z, expected retention time in minutes, and polarity annotation. Set screening_mode=TRUE to generate EICs for target visibility checks; the function automatically applies polarity filtering and saves individual PNG files for each of the 10 targets to the output/screening/Diagnostic_QCs_Batch_*/ folder. Retrieve and open the resulting EIC PNG files and inspect visually for: (1) presence of a single, smooth peak at the expected retention time within the defined m/z window for each target; (2) absence of sawtooth profiles (which indicate unresolved overlapping scan windows); (3) presence of peak annotation and integration boundaries. If sawtooth artefacts appear, re-run tardisPeaks() with corrected mass_range argument to segregate scan windows by mass range. Compare EIC file sets from different invocations (e.g., file-path-based vs. MsExperiment-based) by visual inspection of PNG content to verify functional equivalence.

## Related tools

- **TARDIS** (R package that executes tardisPeaks() function to detect peaks, apply polarity filtering, generate EIC plots, and save diagnostic PNG files for visual inspection) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads centroided .mzML LC–MS data as Spectra objects for input to TARDIS; enables alternative MsExperiment-based invocation)
- **xcms** (Provides retention time correction algorithm integrated into TARDIS for accurate peak localization across runs)
- **MsExperiment** (Container object combining Spectra data and annotated sampleData for QC/sample type distinction in tardisPeaks() invocation)
- **knitr** (Embedding and display of EIC PNG graphics in diagnostic reports via knitr::include_graphics)

## Examples

```
library(TARDIS); tardisPeaks(lcmsData = "path/to/mzML/files/", targetList = targets_df, screening_mode = TRUE, output_folder = "output/screening/Diagnostic_QCs_Batch_1/")
```

## Evaluation signals

- PNG files are successfully generated and saved to the output folder for all 10 targets (5 internal standards + 5 endogenous metabolites); file count and naming are consistent with target list.
- Each EIC PNG displays a single, smooth chromatographic peak at the expected retention time within the defined m/z window; peak annotation and integration boundaries are visible and sensible.
- Absence of sawtooth artefacts in EIC profiles; if sawtooth patterns are present, verify that mass_range argument correctly segregates overlapping scan windows—re-run with corrected mass_range and confirm artefact disappearance.
- Visual content of EIC PNG files from file-path-based and MsExperiment-based invocations are identical, confirming functional equivalence of input modalities.
- QC run diagnostic EICs show consistent peak detection and integration quality across all 14 runs, indicating stable instrument performance and target visibility throughout the batch.

## Limitations

- Sawtooth artefacts appear in EIC output when tardisPeaks() processes data with multiple overlapping m/z scan windows without proper mass_range separation; mass_range argument must be correctly configured to segregate scan windows by mass range.
- Visual inspection is subjective and qualitative; inspection results require human judgment and cannot be fully automated. SNR, peak_cor, and points_over_peak metrics should be consulted alongside visual inspection for comprehensive QC assessment.
- EIC PNG files are diagnostic outputs suitable for QC and method development; they are not substitutes for quantitative peak metrics (AUC, max intensity, SNR) required for targeted metabolomics workflows.
- MsExperiment-based invocation requires sampleData$type to be populated to distinguish QC from sample runs; omission or misconfiguration of this field may produce incomplete or misleading diagnostic outputs.

## Evidence

- [other] tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs showing peak detection and integration for each component.: "tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs showing peak detection and"
- [other] Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS.: "Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation"
- [other] Execute tardisPeaks() function with screening_mode=TRUE to detect peaks and screen for target compound visibility within defined m/z and retention time windows across all runs, automatically applying polarity filtering.: "Execute tardisPeaks() function with screening_mode=TRUE to detect peaks and screen for target compound visibility within defined m/z and retention time windows across all runs, automatically applying"
- [other] The tardisPeaks() function accepts both file paths and MsExperiment objects as input when screening_mode=TRUE, with the MsExperiment approach requiring sampleData$type to be populated to distinguish QC from sample runs.: "The tardisPeaks() function accepts both file paths and MsExperiment objects as input when screening_mode=TRUE, with the MsExperiment approach requiring sampleData$type to be populated to distinguish"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [results] The resulting EICs are again saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
