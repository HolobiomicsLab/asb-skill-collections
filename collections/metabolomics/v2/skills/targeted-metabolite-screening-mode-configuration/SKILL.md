---
name: targeted-metabolite-screening-mode-configuration
description: Use when beginning a targeted LC–MS metabolomics or lipidomics study with a predefined list of compounds (e.g., 10+ targets) and you have centroided .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
  - MSConvert (ProteoWizard)
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Targeted peak integration of LC-MS data using TARDIS
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
- It makes use of an established retention time correction algorithm from the `xcms` package
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

# targeted-metabolite-screening-mode-configuration

## Summary

A diagnostic workflow to visually validate that targeted metabolite compounds are correctly detected and integrated within their expected m/z and retention time windows before full-scale LC–MS peak detection. This skill uses TARDIS screening mode to generate EIC plots that confirm target visibility and localization, ensuring parameter windows are appropriately set for downstream processing.

## When to use

Apply this skill when beginning a targeted LC–MS metabolomics or lipidomics study with a predefined list of compounds (e.g., 10+ targets) and you have centroided .mzML data but have not yet verified whether your theoretical m/z windows and expected retention time ranges correctly capture all targets in your actual chromatographic runs. Use it before committing to full peak detection to avoid wasted computational effort on misconfigured windows.

## When NOT to use

- Input files are already in profile (non-centroided) mode — centroiding is a prerequisite, not performed by this skill.
- You have already performed full peak detection and have a feature table; screening mode is a pre-detection validation step, not a post-hoc review tool.
- Your target list is incomplete or lacks theoretical m/z or expected RT values — screening requires these specifications to define detection windows.

## Inputs

- centroided .mzML files (LC–MS raw data)
- data.frame with columns: compound ID, compound Name, theoretical m/z, expected retention time (minutes), ionization polarity (positive/negative)
- Spectra objects loaded from .mzML files in R

## Outputs

- EIC (Extracted Ion Chromatogram) plots saved to screening output folder (one per target or run)
- visual confirmation of target detection and localization within m/z and retention time windows
- diagnostic evidence for window parameter refinement

## How to apply

First, construct a data.frame containing one row per target compound with columns for compound ID, Name, theoretical m/z, expected retention time (in minutes), and ionization polarity (positive or negative). Load your centroided .mzML files as Spectra objects in R. Execute the tardisPeaks function with screening_mode = TRUE, passing the target data.frame and file paths; TARDIS will automatically apply polarity filtering and remove empty spectra. Inspect the resulting EIC plots saved in the screening output folder to visually confirm that each target is visible and correctly localized within its m/z and retention time window. Pay special attention to targets eluting near window edges, as this indicates whether your RT tolerance is adequate. Adjust m/z or RT windows if targets fall outside the expected regions, then re-run screening mode before proceeding to screening_mode = FALSE for full peak detection.

## Related tools

- **TARDIS** (executes screening_mode = TRUE to generate diagnostic EIC plots with automatic polarity filtering and empty spectrum removal) — https://github.com/pablovgd/TARDIS
- **Spectra** (loads centroided MS data from .mzML files as R objects for consumption by TARDIS)
- **xcms** (provides retention time correction algorithm integrated into TARDIS workflow)
- **MSConvert (ProteoWizard)** (pre-processing tool to convert vendor raw files to .mzML format and apply centroiding)
- **R** (environment for loading Spectra objects, constructing target data.frame, and calling tardisPeaks function) — https://cloud.r-project.org/index.html

## Examples

```
library(TARDIS); targets_df <- data.frame(ID=1:10, Name=c('Cmpd1','Cmpd2',...), mz=c(100.05,150.12,...), RT_min=c(2.5,3.1,...), polarity=c('positive','negative',...)); tardis_result <- tardisPeaks(targets_df, mzML_files=list.files(pattern='.mzML$'), screening_mode=TRUE, output_dir='screening_output')
```

## Evaluation signals

- All 10 (or N) target compounds produce visible peaks in their respective EIC plots within the defined m/z and retention time windows.
- Targets near retention time window edges are flagged visually (e.g., eluting toward the boundary), confirming window adequacy or indicating need for adjustment.
- No spurious peaks or off-target signals appear in the EIC plots for the specified m/z windows, indicating polarity filtering and window precision are correct.
- EIC plots are successfully saved to the screening output folder with file names that map to each target ID, confirming processing completion.
- Subsequent peak detection with screening_mode = FALSE uses the same windows without additional manual parameter tuning, validating that screening-mode windows are production-ready.

## Limitations

- Screening mode requires pre-defined theoretical m/z and retention time windows; compounds without prior chromatographic or spectroscopic reference data may require iterative window adjustment.
- Empty spectra filtering within TARDIS can produce sawtooth-profile peaks in data with multiple overlapping m/z scan windows, complicating visual interpretation if scan strategy is complex.
- EIC plots are visual/qualitative; screening mode does not quantify detection rates, peak shape metrics, or signal-to-noise ratios — these are computed only in full peak detection mode.

## Evidence

- [methods] Screening mode diagnostic EIC plots validate target visibility and localization: "Inspect the resulting EIC plots saved in the screening output folder to verify each target is visible and correctly localized within its m/z and retention-time window."
- [intro] Target data.frame specification with ID, Name, m/z, RT, and polarity: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured *m/z*, Expected RT (in minutes), A column that indicates"
- [intro] TARDIS screening_mode parameter and automatic polarity/empty spectrum filtering: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Centroided .mzML format requirement: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Peak detection follows screening mode after window confirmation: "Now we can perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [methods] Example finding: targets 1577 and 1583 elute toward RT window edges: "visual confirmation that targets 1577 and 1583 elute toward the retention time window edges"
- [intro] Empty spectra filtering can produce sawtooth profiles: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
- [intro] R environment and Spectra objects load .mzML data: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
