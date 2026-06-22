---
name: mass-charge-retention-time-validation
description: Use when after loading centroided .mzML LC-MS data and creating a target list with compound ID, name, theoretical or measured m/z, expected RT (in minutes), and polarity designation, perform this validation step to confirm target visibility and refine m/z and RT window parameters before running.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - xcms
  - R
  - TARDIS
  - Spectra
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms` package
- R package for *TArgeted Raw Data Integration In Spectrometry*
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

# Mass-charge-retention-time validation

## Summary

Validates whether targeted compounds are detectable within expected m/z and retention time windows in LC-MS runs prior to peak detection. This screening step ensures that target compounds are visible in the data before committing computational resources to full peak integration.

## When to use

After loading centroided .mzML LC-MS data and creating a target list with compound ID, name, theoretical or measured m/z, expected RT (in minutes), and polarity designation, perform this validation step to confirm target visibility and refine m/z and RT window parameters before running full peak detection across all runs.

## When NOT to use

- Input LC-MS files are not yet centroided or not in .mzML format — convert and preprocess first
- Target list is incomplete or missing required columns (compound ID, m/z, RT, polarity) — curate the target table before validation
- Analysis goal is limited discovery (non-targeted) — this skill is specific to targeted metabolomics/lipidomics where compound targets are a priori known

## Inputs

- Target list data.frame with columns: compound ID, compound name, theoretical or measured m/z, expected RT (minutes), and polarity indicator
- Centroided LC-MS data in .mzML format
- m/z window tolerance (in Da or ppm)
- RT window tolerance (in minutes)
- Polarity specification (positive or negative ionization)

## Outputs

- Extracted ion chromatograms (EICs) for each target, saved to output folder
- Visual confirmation of target detectability within m/z and RT windows
- Validated or revised target list and window parameters for downstream peak detection

## How to apply

Execute the screening mode within TARDIS by setting `screening_mode = TRUE` to perform a visibility check of targets within specified m/z and RT windows. The function extracts ion chromatograms (EICs) for each target compound and visually inspects whether signals appear within the expected retention time and mass-to-charge ratio ranges. Polarity filtering is automatically applied within TARDIS to subset targets by ionization mode (positive or negative). Review the resulting EICs saved to the output folder to confirm target detectability and adjust m/z and RT window tolerances if necessary. Once validation succeeds, re-run with `screening_mode = FALSE` to perform quantitative peak detection across all runs.

## Related tools

- **TARDIS** (Core package that implements screening mode to validate target detectability within m/z and RT windows and generates EICs for visual inspection) — https://github.com/pablovgd/TARDIS
- **xcms** (Provides retention time correction algorithm used within TARDIS for accurate RT alignment across runs)
- **Spectra** (R infrastructure for loading and representing MS data as Spectra objects integrated with TARDIS)

## Examples

```
library(TARDIS); targets <- createTargetList(file = 'targets.xlsx', pol_patterns = list(Positive = '+', Negative = '-'), polarity = 'Positive', pol_col = 'mode', cols_of_interest = c('ID', 'Name', 'mz', 'RT')); tardis_screening <- tardisPeaks(raw_files, targets, screening_mode = TRUE, mz_tol = 0.01, rt_tol = 0.5)
```

## Evaluation signals

- EIC plots show clear signal peaks aligned with expected RT values for each target compound
- No missing or NULL values in extracted ion chromatogram data for targets within specified m/z and RT windows
- Signal intensity (max intensity and area under curve) are non-zero and visually consistent with compound concentration in QC samples
- All targets pass polarity filtering correctly (positive polarity targets appear only in positive ionization data; negative in negative ionization data)
- Comparison of screening-mode results with full peak detection shows no systematic bias or dropout of targets validated in screening

## Limitations

- Screening mode requires manual visual inspection of EICs to confirm target visibility — automated thresholds for signal-to-noise ratio or peak shape are not specified in the article
- m/z and RT window tolerances must be specified a priori; the article does not provide default values or adaptive strategies for different compound classes
- Polarity filtering is performed within TARDIS; if source data lack a polarity indicator column, manual annotation or pre-filtering is required
- Connection timeout issues may occur when installing TARDIS due to included example data; user must increase timeout settings

## Evidence

- [intro] perform a screening step to check if our targets are visible within our m/z and RT windows: "perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [intro] Create target list data.frame with compound ID, name, m/z, RT, and polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [intro] Polarity filtering is done within TARDIS: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [results] EICs are saved to output folder for inspection: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] Input files need to be centroided and in .mzML format: "Input files need to be converted to the .mzML format and have to be centroided"
