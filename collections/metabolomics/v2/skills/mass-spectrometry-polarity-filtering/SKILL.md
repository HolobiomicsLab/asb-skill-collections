---
name: mass-spectrometry-polarity-filtering
description: Use when when processing centroided .mzML LC–MS runs with a multi-polarity
  target list (i.e., some targets ionize in positive mode, others in negative mode,
  or both) and you need to detect peaks and extract ion chromatograms without manually
  subsetting the raw data by polarity beforehand.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - TARDIS
  - Spectra
  - xcms
  - R
  - MsExperiment
  - knitr
  - ProteoWizard (MSConvert)
  techniques:
  - mass-spectrometry
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

# Mass Spectrometry Polarity Filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automatic subsetting of targeted LC–MS data by ionization mode (positive or negative) during peak detection and extraction, eliminating the need for manual pre-filtering of raw spectral data. This skill ensures that only m/z and retention time windows corresponding to the correct polarity are queried for each target compound, reducing false positives and computational overhead.

## When to use

When processing centroided .mzML LC–MS runs with a multi-polarity target list (i.e., some targets ionize in positive mode, others in negative mode, or both) and you need to detect peaks and extract ion chromatograms without manually subsetting the raw data by polarity beforehand. This is critical for screening-mode and full peak-detection workflows where targets have assigned polarities in the input data.frame.

## When NOT to use

- Input .mzML files are already pre-split by polarity (e.g., separate positive and negative files) — manual subsetting has already been performed
- Target list lacks a polarity annotation column — TARDIS requires explicit polarity metadata for each target
- Raw (non-centroided) LC–MS data — TARDIS requires centroided .mzML format as input

## Inputs

- Centroided .mzML LC–MS runs (multi-polarity acquisition or single-polarity runs)
- Target list data.frame with columns: compound ID, compound name, theoretical m/z, expected retention time (minutes), and polarity ('+' or '−' or equivalent designation)

## Outputs

- Extracted ion chromatogram (EIC) plots for targets, saved per polarity mode
- Peak detection and integration results (AUC, Max. Int., SNR, peak_cor, points over peak) filtered by target polarity
- Results data.frame with metrics stratified by target and polarity context

## How to apply

During tardisPeaks() execution, the TARDIS package automatically applies polarity filtering based on the polarity column in your target list data.frame (which must contain a column indicating positive or negative ionization for each target). The function internally matches each target's polarity annotation with the corresponding polarity stream(s) in the centroided .mzML file, screening for target visibility and detecting peaks only within the assigned polarity context. This eliminates the need for separate polarity subsetting steps before calling tardisPeaks(). The filtering is applied transparently within the TARDIS environment, so you provide a single multi-polarity .mzML file and a target list with polarity annotations, and the function handles the rest.

## Related tools

- **TARDIS** (Performs automated polarity filtering during peak detection via tardisPeaks() with screening_mode parameter) — https://github.com/pablovgd/TARDIS
- **xcms** (Underlying retention time correction algorithm invoked by TARDIS during peak detection)
- **Spectra** (Object format for loading and managing MS data within TARDIS for polarity-aware querying)
- **MsExperiment** (Alternative input container for multi-polarity LC–MS data in TARDIS)
- **ProteoWizard (MSConvert)** (File conversion tool to generate centroided .mzML format required for TARDIS input)

## Examples

```
library(TARDIS); tardis_results <- tardisPeaks(mzML_files = c('run1.mzML', 'run2.mzML'), targets = target_list, screening_mode = TRUE)
```

## Evaluation signals

- Polarity-specific EIC plots are generated and saved without errors; plots for targets assigned to one polarity do not contain noise or false peaks from the opposite polarity
- Peak detection results (AUC, Max. Int., SNR) are computed only for m/z and RT windows matching the target's assigned polarity
- No manual polarity subsetting step was required before calling tardisPeaks(); the function accepts a single multi-polarity .mzML file and target list
- Results data.frame includes a polarity column or is stratified such that each target's metrics correspond only to its assigned ionization mode
- Visual inspection of diagnostic QC plots confirms that peaks are detected only in the correct ion stream (e.g., positive targets appear in positive-mode EICs, negative targets in negative-mode EICs)

## Limitations

- Polarity filtering is transparent and automated; users cannot manually override or tune polarity assignments at the peak detection stage without modifying the input target list
- If the target list polarity annotation is incorrect or missing, the skill will either fail or produce incorrect results without explicit validation warnings
- Polarity filtering applies only after .mzML loading and centroiding; data quality issues (e.g., mass calibration drift, low signal in one polarity) are not corrected by this step

## Evidence

- [intro] Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Target list data.frame must include a polarity column: "A column that indicates the polarity"
- [other] tardisPeaks() with screening_mode=TRUE automatically applies polarity filtering during target screening: "Execute tardisPeaks() function with screening_mode=TRUE to detect peaks and screen for target compound visibility within defined m/z and retention time windows across all runs, automatically applying"
- [intro] Input files must be centroided .mzML format: "Input files need to be converted to the .mzML format and have to be centroided"
