---
name: ms2-fragment-m-z-grouping-and-aggregation
description: Use when you have extracted MS/MS spectra for a given metabolomic feature
  across multiple replicates (e.g., after top-TIC filtering) and need to identify
  which fragments are reproducible across replicates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - dures
  - S4Vectors
  - dplyr
  - Spectra
  - call_aggregate
  - extract_raw_spectra
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils",
  "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils",
  "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager",
  "knitr", "markdown"),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dures_cq
    doi: 10.1021/acs.analchem.5c01726
    title: DuReS
  dedup_kept_from: coll_dures_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01726
  all_source_dois:
  - 10.1021/acs.analchem.5c01726
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 Fragment m/z Grouping and Aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill groups MS/MS fragments across replicate spectra by m/z tolerance, merges nearby peaks, and aggregates their intensities to generate a consensus spectrum with fragment recurrence frequencies. It is applied to denoise tandem mass spectrometry data by identifying reproducible signal fragments across replicates.

## When to use

Apply this skill when you have extracted MS/MS spectra for a given metabolomic feature across multiple replicates (e.g., after top-TIC filtering) and need to identify which fragments are reproducible across replicates. This is particularly useful after filtering to top 80% TIC spectra, where you want to merge m/z peaks within a specified tolerance (e.g., 0.05 Da) and count how often each merged fragment appears across the replicate set.

## When NOT to use

- Input spectra have not yet been filtered by quality metrics (e.g., TIC threshold); perform preprocessing and TIC filtering first.
- You need to denoise at the individual spectrum level before grouping; apply intra-spectrum fragment grouping (merge fragments within tolerance within a single spectrum) before inter-spectrum aggregation.
- Your goal is to match spectra against a reference library without consensus-building; skip aggregation and proceed directly to spectral matching.

## Inputs

- List of extracted MS/MS spectra for a single feature across replicates (Spectra S4 object, filtered by top x% TIC)
- m/z mass tolerance threshold (Da; default 0.05)
- Folder path containing mzML files and feature information

## Outputs

- Consensus spectrum dataframe with grouped fragments (mean m/z, mean intensity, recurrence frequency)
- Fragment count for the consensus spectrum (e.g., 498 fragments for feature 1982)
- Recurrence frequency matrix for labeling individual spectra

## How to apply

First, extract the top-TIC-filtered replicate spectra for a feature (e.g., 66 spectra after 80% TIC filtering from an original 83) using extract_raw_spectra with a specified m/z tolerance (default 0.05 Da). Then apply call_aggregate to perform inter-spectrum fragment grouping: fragments within the tolerance window are merged, their m/z values are averaged, and their intensities are summed. The function simultaneously calculates the recurrence frequency—how many replicate spectra contributed a fragment to each merged m/z bin. This produces a consensus spectrum dataframe with mean m/z, mean intensity, and recurrence frequency for each grouped fragment. The m/z tolerance (typically 0.05 Da) is the critical parameter; choose it based on your instrument's mass accuracy.

## Related tools

- **Spectra** (S4 object class for storing and manipulating MS/MS spectral data; required to represent grouped spectra before aggregation) — https://bioconductor.org/packages/Spectra
- **call_aggregate** (Function that performs inter-spectrum fragment grouping and aggregation; merges fragments within m/z tolerance and calculates recurrence frequencies) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **extract_raw_spectra** (Function that extracts and prepares top-TIC-filtered spectra as input for aggregation; performs initial intra-spectrum grouping within specified m/z tolerance) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **dplyr** (Data manipulation and summarization of consensus spectrum dataframes (mean m/z, intensity aggregation, frequency counts)) — https://cran.r-project.org/package=dplyr
- **S4Vectors** (Provides S4 object infrastructure for handling spectral data structures and recurrence frequency matrices) — https://bioconductor.org/packages/S4Vectors

## Examples

```
l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)
```

## Evaluation signals

- Fragment count in output consensus spectrum matches expected value (e.g., 498 for feature 1982; verify by row count of consensus dataframe)
- Recurrence frequencies are non-negative integers ≤ total number of replicate spectra and reflect observed fragment occurrence patterns
- Mean m/z values in consensus spectrum fall within the original m/z range and merged peaks respect the specified tolerance window (e.g., 0.05 Da)
- Intensity summation is correct: summed intensities of merged fragments are consistent with input spectra; no negative or NaN values appear
- Consensus spectrum contains no duplicate m/z values within the tolerance threshold

## Limitations

- The choice of m/z tolerance (default 0.05 Da) directly affects fragment grouping resolution; narrower tolerances yield more fragments, wider tolerances risk losing spectral detail. Instrument mass accuracy must be known a priori.
- Aggregation assumes replicate spectra represent the same metabolite feature; misalignment in RT or m/z during feature extraction will degrade consensus quality.
- Fragments present in only one or few replicates will have low recurrence frequencies and may be filtered out in downstream denoising steps; this can lose genuine low-abundance signal if replicates are noisy or few in number.
- No in-built handling of isotope patterns or neutral loss series; fragments related by mass difference must be grouped manually if needed for specialized applications.

## Evidence

- [methods] Extract top x% TIC spectra, and Group fragments within a specified mass tolerance: "Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance"
- [methods] call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities: "Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities."
- [methods] Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies: "Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments."
- [methods] fragments in the reference spectra that fall within the specified m/z tolerance (tol) are grouped together: "Inter-spectrum fragment grouping: fragments in the reference spectra that fall within the specified m/z tolerance (tol) are grouped together"
- [readme] l2 = extract_raw_spectra(folder_path = folder_path, l1, 0.05, 0.8); l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path): "l2 = extract_raw_spectra(folder_path = folder_path, l1, 0.05, 0.8) #extract top x% (where x = 0.8) TIC spectra, groups fragments within a given tolerance (0.05 Da); l3 ="
