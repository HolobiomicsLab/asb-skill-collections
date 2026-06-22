---
name: spectral-peak-intensity-aggregation
description: Use when you have multiple replicate MS/MS spectra for the same metabolic feature (e.g., 66 top-TIC spectra for feature 1982) and need to identify robust peaks by merging nearby m/z values and pooling their signal strength.
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
  - extract_raw_spectra
  - call_aggregate
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-intensity-aggregation

## Summary

Aggregate m/z peaks and their intensities across multiple replicate MS/MS spectra by grouping fragments within a specified mass tolerance and summing their intensities to produce a consensus spectrum. This is a foundational denoising step that reduces noise by consolidating signal across replicates before applying frequency-based filters.

## When to use

Apply this skill when you have multiple replicate MS/MS spectra for the same metabolic feature (e.g., 66 top-TIC spectra for feature 1982) and need to identify robust peaks by merging nearby m/z values and pooling their signal strength. Use it after extracting top x% TIC spectra and before applying frequency-based denoising thresholds.

## When NOT to use

- If you have single-replicate spectra or no within-feature replicates; aggregation requires multiple spectra per feature to be meaningful.
- If your input spectra have not been TIC-filtered or preprocessed; apply preprocessing and top-x%-TIC extraction first.
- If you need to preserve individual spectrum identity for downstream matched filtering or library comparison; aggregation consolidates replicates into a single consensus, losing per-spectrum granularity.

## Inputs

- Filtered top-TIC MS/MS spectra (e.g., from extract_raw_spectra output)
- Mass tolerance threshold in Da (e.g., 0.05)
- Replicate spectrum set for a single feature

## Outputs

- Consensus spectrum dataframe with columns: mean m/z, mean intensity, fragment recurrence frequency
- Total fragment count for the consensus spectrum
- Aggregated peak list with grouped m/z values and pooled intensities

## How to apply

Load preprocessed MS/MS spectra for a single feature using extract_raw_spectra with a specified mass tolerance (e.g., 0.05 Da) and TIC threshold (e.g., 0.8 to retain only top-80%-intensity spectra). Pass the filtered spectral set to call_aggregate, which groups fragments within the mass tolerance window, sums their intensities across all replicate spectra, and records the recurrence frequency (number of spectra in which each fragment appears). The output is a consensus spectrum dataframe listing mean m/z, mean intensity, and fragment recurrence for each unique grouped peak. Verify correctness by confirming the total fragment count matches expected values and that intensities are properly summed across replicates.

## Related tools

- **Spectra** (S4 class for storing and manipulating MS/MS spectra objects; used to load and manage replicate spectra before aggregation)
- **extract_raw_spectra** (Extracts top x% TIC-filtered spectra and performs intra-spectrum fragment grouping; output is the input to call_aggregate) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **call_aggregate** (Core aggregation function that groups fragments within mass tolerance across all replicates, sums intensities, and calculates recurrence frequencies to generate the consensus spectrum) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **S4Vectors** (Provides S4 class infrastructure for spectral data structures used in aggregation)
- **dplyr** (Used for data manipulation and verification of aggregated dataframe outputs (filtering, grouping, summarization))

## Examples

```
l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)
```

## Evaluation signals

- Consensus spectrum fragment count matches the reported value (e.g., 498 fragments for feature 1982); verify by row-counting the output dataframe.
- Mean m/z values fall within the input spectra's m/z range and cluster peaks separated by less than the mass tolerance; check for anomalous or duplicate groupings.
- Summed intensities per grouped fragment are monotonically related to the number of replicates in which the peak appears (recurrence frequency); peaks appearing in more spectra should have higher aggregate intensity.
- Fragment recurrence frequencies range from 1 to the total number of input spectra (e.g., 1–66 for 66 top-TIC spectra); verify no frequency exceeds the replicate count.
- Comparison with expected consensus spectrum size confirms that inter-spectrum grouping (e.g., mass tolerance 0.05 Da) reduces the fragment count relative to the union of all intra-spectrum grouped peaks.

## Limitations

- Mass tolerance parameter (e.g., 0.05 Da) is user-defined and must balance fragment resolution against artificial merging; inappropriate thresholds can cause false coalescence of distinct m/z peaks or fragmentation of true multiplets.
- Aggregation assumes that replicate spectra are independent and similarly informative; highly skewed TIC distributions or outlier spectra can distort consensus intensity estimates.
- Recurrence frequency alone does not distinguish true signal from systematic noise; frequency-based denoising thresholds must be applied in subsequent steps to retain only robust fragments.
- The method is sensitive to preprocessing and TIC-filtering quality; contamination or inadequate normalization in earlier steps can propagate into the consensus spectrum.

## Evidence

- [other] Load preprocessed MS/MS data for feature 1982 including top 80% TIC-filtered spectra (66 spectra after filtering from original 83) using the extract_raw_spectra function with mass tolerance 0.05 Da and TIC threshold 0.8: "Load preprocessed MS/MS data for feature 1982 including top 80% TIC-filtered spectra (66 spectra after filtering from original 83) using the extract_raw_spectra function with mass tolerance 0.05 Da"
- [other] Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities: "Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities."
- [other] Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments: "Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments."
- [readme] In the **third step**, a **consensus spectrum** is generated using the **top 80% TIC spectra**, and the corresponding **fragment frequencies** are calculated: "In the **third step**, a **consensus spectrum** is generated using the **top 80% TIC spectra**, and the corresponding **fragment frequencies** are calculated"
- [readme] l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path): "l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)"
