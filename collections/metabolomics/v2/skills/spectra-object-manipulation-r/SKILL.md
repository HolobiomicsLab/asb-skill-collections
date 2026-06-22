---
name: spectra-object-manipulation-r
description: Use when when you have extracted and concatenated MS/MS spectra from multiple replicates for a set of metabolomic features (stored in a preprocessed list), and need to apply intensity-based filtering (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - dures
  - S4Vectors
  - dplyr
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
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

# Spectra Object Manipulation in R

## Summary

Load, filter, and manipulate tandem MS/MS spectra as S4 Spectra objects in R, applying intensity thresholds and mass tolerance constraints to prepare concatenated replicate spectra for denoising and analysis.

## When to use

When you have extracted and concatenated MS/MS spectra from multiple replicates for a set of metabolomic features (stored in a preprocessed list), and need to apply intensity-based filtering (e.g., top x% TIC selection) or prepare spectra objects for downstream consensus generation, frequency labeling, or spectral matching workflows.

## When NOT to use

- Input is already a consensus spectrum or aggregated frequency table; Spectra object manipulation is for raw MS/MS data, not summary statistics.
- You have only a single replicate per feature; the skill is designed for replicate concatenation and filtering, not singleton spectra.
- Your data are in formats other than mzML (e.g., raw Thermo .raw files without prior conversion); the dures package requires mzML input.

## Inputs

- Preprocessed spectra list (l1) from preprocess() containing concatenated MS/MS replicates
- Folder path to mzML files
- Mass tolerance parameter (Da)
- Top TIC threshold parameter (0–1, e.g., 0.8)

## Outputs

- Spectra object (S4 class) containing intensity-filtered spectra
- Data frame with before/after spectra counts per feature

## How to apply

Load the preprocessed spectra list (l1) output from the preprocess() step using the dures package. Call extract_raw_spectra() with parameters: folder_path, the l1 list, mass tolerance (e.g., 0.05 Da for intra-spectrum grouping), and a top TIC threshold (e.g., 0.8 for top 80% intensity cutoff). The function returns a Spectra object (sps_top_tic_2) containing filtered spectra and a dataframe reporting spectra counts before and after filtering for each feature. Verify the reduction by checking that features meet expected thresholds (e.g., feature 1982: 83→66 spectra; feature 872: 43→34 spectra). Use the filtered Spectra object as input to downstream steps such as call_aggregate() for consensus spectrum generation.

## Related tools

- **Spectra** (S4 class for storing and manipulating MS/MS spectra objects; core data structure for filtering and accessing spectrum metadata and intensity data)
- **dures** (Provides extract_raw_spectra() function that wraps Spectra object creation, applies top x% TIC filtering, groups fragments within mass tolerance, and returns filtered Spectra object and summary statistics) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **S4Vectors** (Bioconductor package providing S4 class infrastructure used by Spectra for object-oriented spectrum data storage)
- **dplyr** (Used for filtering and summarizing spectra count dataframes by feature)

## Examples

```
l2 = extract_raw_spectra(folder_path = "~/metabolomics/test_1/", l1, 0.05, 0.8)
```

## Evaluation signals

- Verify that the returned Spectra object has fewer spectra per feature than the input l1 list, consistent with the specified top TIC cutoff (e.g., 80% intensity retention)
- Check that before/after spectra count dataframe matches expected reductions for known features (e.g., feature 1982: 83→66; feature 872: 43→34)
- Confirm that mass tolerance grouping reduced fragment counts within each spectrum (e.g., 98→81 fragments after 0.05 Da grouping)
- Validate that no spectra are returned for features with zero MS/MS data or those below the TIC threshold
- Ensure Spectra object is S4-compliant and compatible with downstream dures functions (call_aggregate, label_individual_spectrum)

## Limitations

- Top TIC cutoff may be too aggressive on features with few high-intensity fragments, removing informative signal; tuning via Pareto front analysis or Wilcoxon rank-sum tests is recommended.
- Mass tolerance parameter (e.g., 0.05 Da) assumes accurate mass calibration; miscalibrated instruments may cause over-grouping or under-grouping of fragments.
- Spectra object manipulation does not denoise; it only filters by intensity and groups fragments. Actual denoising (removal of noise fragments based on recurrence frequency) occurs in downstream steps (generate_denoised_spectra).
- Requires input in mzML format; conversion from other formats (e.g., .raw) must be completed beforehand using external tools (e.g., MSConvert).

## Evidence

- [other] Call extract_raw_spectra() with parameters: folder_path, l1, mass tolerance 0.05 Da, and top TIC threshold 0.8 (80%). Extract the output Spectra object (sps_top_tic_2) and dataframe (df) showing before/after spectra counts per feature.: "Call extract_raw_spectra() with parameters: folder_path, l1, mass tolerance 0.05 Da, and top TIC threshold 0.8 (80%). Extract the output Spectra object (sps_top_tic_2) and dataframe (df) showing"
- [methods] The extracted spectra are then concatenated for all replicate spectra belonging to a given feature: "The extracted spectra are then concatenated for all replicate spectra belonging to a given feature"
- [methods] Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance: "Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance"
- [readme] l2 = extract_raw_spectra(folder_path = folder_path, l1_subset, 0.05, 0.8): "l2 = extract_raw_spectra(folder_path = folder_path, l1_subset, 0.05, 0.8)"
- [methods] Top 80% TIC cutoff reduced 83 spectra to 66 spectra for feature 1982: "Top 80% TIC cutoff reduced 83 spectra to 66 spectra for feature 1982"
- [methods] After grouping, the number of fragments reduced to `81`: "After grouping, the number of fragments reduced to `81`"
