---
name: lc-ms-retention-time-adjustment
description: Use when you have centroided .mzML LC–MS data with multiple sample runs and a preliminary compound target table with theoretical or measured retention times, but you suspect the expected RT values may not align with actual retention windows in your dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Targeted peak integration of LC-MS data using TARDIS
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
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

# LC-MS Retention Time Adjustment

## Summary

Refine expected retention times (RT) for targeted compounds by executing a screening run in TARDIS, then updating the compound table with corrected RT values before full peak detection. This skill ensures accurate peak detection across all sample runs by accounting for instrument drift and separation variability.

## When to use

Use this skill when you have centroided .mzML LC–MS data with multiple sample runs and a preliminary compound target table with theoretical or measured retention times, but you suspect the expected RT values may not align with actual retention windows in your dataset. Apply it after initial file conversion and before running full peak detection across all runs.

## When NOT to use

- Input files are already in negative/positive ionization mode subsets – TARDIS performs polarity filtering internally, so pre-filtering may duplicate effort
- Expected RT values are already validated and stable across instrument sessions – adjustment is unnecessary if prior screening confirms accuracy
- Peak detection is being repeated on identical instrument configuration and column batch – reuse the previously validated RT table rather than re-screening

## Inputs

- Centroided .mzML LC–MS files (one or more sample runs)
- Spectra objects loaded via the Spectra package
- Target compound data.frame with columns: compound ID, Name, m/z, expected RT (minutes), polarity

## Outputs

- Updated target compound data.frame with refined RT values
- EICs visualizations (saved to output folder) confirming adjusted RT windows
- Screening-mode results list (if screening_mode=TRUE is executed first)

## How to apply

First, execute tardisPeaks with screening_mode = TRUE to perform a quick scan of m/z and RT windows across representative runs (typically QC or screening runs) without full peak integration. Inspect the generated extracted-ion chromatograms (EICs) saved to the output folder to visually identify where targets actually elute. Update the compound target table in R with the observed retention times for compounds showing drift or misalignment (e.g., adjust target 1577 from expected 8.5 min to observed 8.82 min). Then re-execute tardisPeaks with screening_mode = FALSE on the complete dataset using the refined RT table, which will perform full peak detection and integration with the corrected windows. Verify by comparing EIC positions in screening output to updated RT values, and confirm that peak metrics (Max. Int., SNR, peak_cor, points_over_peak) are consistent across runs.

## Related tools

- **TARDIS** (Executes screening_mode = TRUE to scan m/z and RT windows and generate EICs; then re-runs with screening_mode = FALSE using refined RT values for full peak detection) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads centroided .mzML files as Spectra objects for input to TARDIS)
- **R** (Used to load target compound table, update RT values programmatically, and manage TARDIS function calls) — https://cloud.r-project.org/
- **xcms** (Provides retention time correction algorithm integrated into TARDIS for internal alignment)

## Examples

```
library(TARDIS); library(Spectra); targets <- read.csv('compounds.csv'); results_screening <- tardisPeaks(mzML_files, targets, screening_mode = TRUE, output_folder = './screening'); targets$RT[targets$ID == 1577] <- 8.82; targets$RT[targets$ID == 1583] <- 4.0; results_full <- tardisPeaks(mzML_files, targets, screening_mode = FALSE, output_folder = './final_peaks');
```

## Evaluation signals

- EICs from screening mode visually align with peaks in the retention time windows; refined RT values place windows at observed peak apex ± ~0.5 min
- Peak metrics (Max. Int., SNR, peak_cor, points_over_peak) returned by tardisPeaks with screening_mode = FALSE are consistent and non-zero across all 14 runs for each target
- Area-under-curve (AUC) values in the results data.frame are stable and above background noise levels for targets with refined RT values
- No sawtooth artifacts or signal dropout in EICs after adjustment, confirming that empty spectra filtering and RT windows are correctly calibrated
- Comparison of screening-mode EICs to full-mode results shows improved peak shape consistency and higher SNR for targets with corrected RT values

## Limitations

- Screening mode requires visual inspection of EICs; systematic drift or multi-modal peak distributions may require manual curation rather than automatic thresholding
- RT adjustment assumes compound identity is stable across all runs; if compounds co-elute or fragment, manual separation or mass tolerance adjustment may be needed
- The method does not account for non-linear RT shifts; if retention time drift is systematic across the run sequence, consider xcms retention time correction before screening
- Polarity filtering is performed internally by TARDIS; misspecification of the polarity column in the compound table will cause targets to be missed even with correct RT

## Evidence

- [intro] screening_mode_purpose: "First, we perform a screening step to check if our targets are visible within our m/z and RT windows"
- [intro] full_detection_after_adjustment: "Now we can perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [results] screening_output_inspection: "The resulting EICs are again saved in the output folder and can be inspected"
- [other] task_example_rt_update: "update expected RT values for target 1577 to 8.82 min and target 1583 to 4 min using R"
- [results] full_results_metrics: "Results include tables with metrics: Max. Int., SNR, peak_cor and points over the peak"
