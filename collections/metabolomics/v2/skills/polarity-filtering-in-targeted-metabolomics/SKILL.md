---
name: polarity-filtering-in-targeted-metabolomics
description: Use when when working with targeted LC–MS metabolomics or lipidomics data where compound targets span both positive and negative ionization modes, or when your raw .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# Polarity filtering in targeted metabolomics

## Summary

Apply ionization mode filtering to LC–MS data to isolate compounds ionized in a specific polarity (positive or negative) before targeted peak detection. This reduces processing overhead and prevents false peak assignments in compounds that cannot ionize under the selected mode.

## When to use

When working with targeted LC–MS metabolomics or lipidomics data where compound targets span both positive and negative ionization modes, or when your raw .mzML files contain spectra from both polarities but you want to focus peak detection on one ionization mode to match your target compound list. Use this skill when you have a target data.frame with a polarity column indicating the expected ionization mode for each compound.

## When NOT to use

- Input data is already single-polarity (e.g., pre-filtered or acquired in positive-mode-only data collection).
- Target compound list lacks ionization polarity information or does not distinguish between positive and negative targets.
- Analysis goal is exploratory or untargeted—polarity filtering is designed specifically for targeted workflows where compound identity and ionization mode are known a priori.

## Inputs

- centroided .mzML files (MS data)
- Spectra object loaded from .mzML files
- target data.frame with columns: compound ID, compound Name, theoretical m/z, expected retention time (minutes), ionization polarity (positive or negative)

## Outputs

- polarity-filtered Spectra object
- diagnostic EIC plots showing targets in the correct ionization polarity
- peak integration results (AUC, max intensity, SNR, peak_cor) for each target in each run

## How to apply

Create a target data.frame that includes a column specifying ionization polarity (positive or negative) for each target compound. Load centroided .mzML files as Spectra objects in R. Pass the target data.frame and file paths to TARDIS with screening_mode = TRUE; TARDIS automatically applies polarity filtering based on the ionization mode column in your target table, removing spectra that do not match the specified polarity. This prevents spurious peak detection outside the intended ionization context and reduces sawtooth artifacts in overlapping m/z scan windows. Verify polarity filtering by inspecting the resulting EIC plots—each target should appear within its expected m/z and retention time window without contributions from the opposite polarity.

## Related tools

- **TARDIS** (R package that automates polarity filtering within the targeted peak integration workflow; receives target data.frame and applies filtering based on ionization mode column) — https://github.com/pablovgd/TARDIS
- **Spectra** (R package that loads and represents MS data as Spectra objects, which TARDIS ingests for polarity-based subsetting)
- **xcms** (Provides retention time correction algorithms that work downstream of polarity filtering in the full TARDIS workflow)
- **MSConvert (ProteoWizard)** (Converts raw vendor MS files to centroided .mzML format, which is the required input format before polarity filtering in TARDIS)

## Examples

```
library(TARDIS); targets <- data.frame(ID=1:10, Name=c('Compound1','Compound2',...), mz=c(200.1,250.2,...), RT=c(5.2,6.1,...), polarity=c('positive','negative',...)); spectra <- Spectra('data.mzML'); results <- tardisPeaks(targets, 'data.mzML', screening_mode=TRUE)
```

## Evaluation signals

- All EIC plots for targets with positive ionization polarity contain signal only in spectra marked as positive; no signal from negative-polarity spectra.
- All EIC plots for targets with negative ionization polarity contain signal only in spectra marked as negative; no signal from positive-polarity spectra.
- Peak detection results (AUC, max intensity) are non-zero only for compounds whose polarity matches the ionization mode of the run.
- Sawtooth artifacts typical of overlapping m/z scan windows are reduced or absent in the integrated peaks.
- Visual inspection of screening-mode EIC plots confirms each target is localized within its expected m/z and retention time window without polarity-based false positives.

## Limitations

- Polarity filtering is performed automatically within TARDIS based on the polarity column in the target data.frame; no manual polarity subsetting is needed, but misconfiguration of the target table polarity column will cause incorrect filtering.
- The workflow assumes centroided .mzML input; profile-mode or unconverted vendor formats will not work.
- Filtering of empty spectra within TARDIS (to avoid sawtooth profiles in data with multiple overlapping m/z scan windows) is automatic and cannot be disabled; this may reduce sensitivity in sparse data regions.

## Evidence

- [intro] Polarity filtering explained in context of target data preparation: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured m/z, Expected RT (in minutes), A column that indicates"
- [intro] Automatic polarity filtering within TARDIS: "Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed"
- [other] Polarity filtering applied during screening mode: "TARDIS automatically applies polarity filtering and filters empty spectra"
- [intro] Sawtooth artifact reduction through empty spectra filtering: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
- [intro] Verification via EIC inspection: "First, we perform a screening step to check if our targets are visible within our m/z and RT windows"
