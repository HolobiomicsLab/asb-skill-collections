---
name: replicate-spectrum-comparison
description: Use when you have multiple MS/MS spectra (replicates) for a single metabolic
  feature (same m/z and RT window) and need to identify which fragments are reproducibly
  detected across replicates versus noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - dures
  - dplyr
  - Spectra
  - data.table
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

# replicate-spectrum-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare and aggregate MS/MS spectra from replicate measurements of the same feature to identify recurrent fragments and calculate fragment frequencies across replicates. This skill enables consensus spectrum generation and noise reduction by quantifying fragment recurrence patterns.

## When to use

Apply this skill when you have multiple MS/MS spectra (replicates) for a single metabolic feature (same m/z and RT window) and need to identify which fragments are reproducibly detected across replicates versus noise. Use it as a prerequisite step before frequency-based denoising or when generating a consensus spectrum for spectral matching.

## When NOT to use

- Input consists of a single MS/MS spectrum (no replicates available) — consensus generation requires ≥2 replicates to compute meaningful frequencies.
- Spectra have already been denoised or consensus-aggregated; applying this skill again would double-count or lose information about individual replicate variation.
- Fragment m/z precision is known to be poor or inconsistently calibrated, preventing reliable within-tolerance grouping.

## Inputs

- concatenated MS/MS spectra for a single feature (output of Spectra::peaksData() or dures preprocess())
- mass tolerance parameter (Da, typically 0.05)
- TIC percentile cutoff (typically 0.8 for top 80%)
- mzML file collection with replicate measurements

## Outputs

- aggregated consensus spectrum with fragment frequencies
- per-fragment recurrence counts (number of replicates in which each m/z appears)
- per-fragment frequency ratios (recurrence count / total replicate spectra)
- labeled individual spectra with frequency annotations

## How to apply

After extracting and concatenating replicate spectra for a given feature using preprocess() with specified m/z and RT tolerance (e.g., 5 ppm and 0.1 min), filter to the top x% TIC spectra (typically 80%) using extract_raw_spectra(). Group fragments within each spectrum using intra-spectrum grouping (merging m/z values by mean and summing intensities within a mass tolerance, typically 0.05 Da). Aggregate the grouped spectra using call_aggregate() to compute fragment frequencies—the proportion of replicate spectra in which each m/z appears. These frequencies are then used to label individual spectra and serve as the basis for denoising thresholds (e.g., retain fragments appearing in ≥10% of replicates) and for assessing consistency of signal across replicates.

## Related tools

- **Spectra** (Bioconductor S4 class for storing and manipulating mass spectrometry spectra; used to extract peak data (m/z, intensity pairs) before and after grouping)
- **dures** (R package implementing the full 5-step DuReS workflow; provides preprocess(), extract_raw_spectra(), call_aggregate(), and label_individual_spectrum() functions for replicate comparison and fragment frequency computation) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **dplyr** (Data manipulation and summary statistics for organizing fragment frequency tables)
- **data.table** (High-performance data frame operations for aggregating large numbers of spectra and computing per-fragment frequencies)

## Examples

```
l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path); l4 = label_individual_spectrum(l3, folder_path, 0.05)
```

## Evaluation signals

- Fragment frequencies should range from 0 to 1 (or 0% to 100%), with recurrent fragments appearing in multiple replicates and noise fragments appearing in only 1 replicate
- Intra-spectrum grouping should reduce fragment counts within individual spectra (e.g., 98 → 81 fragments for feature 872, 23 → 22 for feature 1982), verifiable by comparing peaksData() before and after grouping
- Top x% TIC filtering should reduce the total number of spectra per feature before aggregation (e.g., 83 → 66 spectra for feature 1982 at 80% cutoff), indicating successful filtering
- Consensus spectrum fragments should be a subset of or equal to the union of all fragments across replicates (no novel m/z values should appear in the consensus)
- Frequency distribution should show a clear bimodal or heavy-tailed pattern: true signal fragments with high recurrence (e.g., >50%), noise fragments with recurrence near the frequency threshold (e.g., 10%)

## Limitations

- Replicate comparison requires ≥2 MS/MS spectra per feature; features with only 1 spectrum cannot compute meaningful frequencies
- Mass tolerance (typically 0.05 Da for intra-spectrum grouping) must be tuned to the mass accuracy of the instrument; poor calibration can cause false grouping or fragmentation
- Top x% TIC filtering is heuristic and may remove weak but authentic fragments if they occur in low-intensity spectra; the 80% threshold is data-dependent and may need adjustment for different ionization modes or sample types
- Frequency-based denoising assumes that signal fragments recur across replicates; features with genuine biological variation (e.g., post-translational modifications, isoforms) may have variable fragment patterns that are incorrectly flagged as noise
- Fragment grouping is sensitive to RT and m/z tolerance parameters; misspecified tolerances can lead to either under-grouping (inflated fragment counts) or over-grouping (loss of distinct fragments)

## Evidence

- [methods] Extract and organize replicate spectra, compute fragment frequencies: "The extracted spectra are then concatenated for all replicate spectra belonging to a given feature"
- [methods] Intra-spectrum grouping by mass tolerance: "fragments within a default tolerance of **0.05 Da** of one another were merged"
- [methods] Top TIC filtering reduces spectrum count before aggregation: "From 83 before to 66 spectra after after top x% TIC"
- [methods] Fragment frequency computation in consensus spectra: "a **consensus spectrum** is generated using the **top 80% TIC spectra**, and the corresponding **fragment frequencies** are calculated"
- [methods] Frequency-based labeling and denoising decision: "Using the **recurrence frequencies** calculated in **Step 3**, we will now label the fragments of every **top TIC spectra** for a given feature"
- [readme] DuReS workflow overview with preprocess, extract, aggregate, label: "This step reads in the mzML files, prepares the stats.txt file in a format that extracts MS2 spectra and returns a list"
- [readme] Aggregate step for frequency computation: "This step aggregates the top 80% TIC spectra from step2 and calculates the fragment frequencies"
