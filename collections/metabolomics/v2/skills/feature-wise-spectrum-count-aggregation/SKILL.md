---
name: feature-wise-spectrum-count-aggregation
description: Use when when you have extracted concatenated MS/MS spectra for multiple
  features from replicate mzML files and need to verify that a TIC-based filtering
  step (e.g., top x% TIC extraction) reduces per-feature spectrum counts to expected
  target levels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - dures
  - S4Vectors
  - dplyr
  - Spectra
  - data.table
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# feature-wise-spectrum-count-aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify and aggregate MS/MS spectrum counts per metabolomic feature before and after applying TIC-based filtering to assess the efficacy of spectral denoising. This skill validates that quality-control filters (e.g., top 80% TIC cutoff) reduce spectrum redundancy consistently across features.

## When to use

When you have extracted concatenated MS/MS spectra for multiple features from replicate mzML files and need to verify that a TIC-based filtering step (e.g., top x% TIC extraction) reduces per-feature spectrum counts to expected target levels. Typically applied after extract_raw_spectra() and before consensus spectrum generation to confirm that filtering has removed low-intensity, low-information spectra while retaining sufficient replicates for robust consensus.

## When NOT to use

- Input spectra have not been concatenated by feature — use feature-wise grouping first.
- TIC values are not available or have not been calculated for each spectrum.
- You are working with already-consensus or already-aggregated spectra (not individual replicates).

## Inputs

- Preprocessed spectra list (l1) from preprocess() — concatenated MS/MS replicates for all features
- mzML file folder path
- Feature table (Stats.txt or equivalent) with precursor m/z and retention time
- Top TIC threshold parameter (e.g., 0.8 for 80%)
- Mass tolerance parameter (Da)

## Outputs

- Spectra object (sps_top_tic_2) — filtered spectra post-TIC cutoff
- Dataframe with per-feature spectrum counts: feature ID, count before filter, count after filter
- Aggregation summary table (feature-wise spectrum count delta)

## How to apply

Load the preprocessed spectra list (l1) containing concatenated MS/MS replicates for all features using preprocess(). Call extract_raw_spectra() with parameters: folder_path, l1, mass tolerance (default 0.05 Da), and top TIC threshold (0.8 for 80%). Extract the output Spectra object (sps_top_tic_2) and accompanying dataframe showing before/after spectrum counts per feature. Aggregate and cross-tabulate the counts at the feature level, grouping by feature ID and comparing pre-filter vs. post-filter counts. The rationale is that top 80% TIC cutoff should yield consistent reduction ratios (e.g., 83→66 for feature 1982, 43→34 for feature 872) indicating that low-TIC spectra are being systematically removed without over-filtering. If observed reductions deviate significantly from expected patterns, investigate data quality or TIC threshold appropriateness.

## Related tools

- **dures** (Provides extract_raw_spectra() function to perform TIC-based filtering and return spectra and per-feature counts; preprocess() to concatenate spectra by feature.) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **Spectra** (S4 container for MS/MS spectra objects; supports subsetting and metadata access for spectrum enumeration.)
- **dplyr** (Tabulate and aggregate spectrum counts by feature; group_by(feature_id) and summarise(count_before, count_after).)
- **data.table** (Efficient aggregation and cross-tabulation of large spectrum count matrices by feature.)

## Examples

```
l2 = extract_raw_spectra(folder_path = "~/metabolomics/test_1/", l1, 0.05, 0.8); df_counts <- as.data.frame(table(l2$sps_top_tic_2@metadata$feature_id)); print(df_counts)
```

## Evaluation signals

- Per-feature spectrum count reduction is monotonic (count_after ≤ count_before) for all features.
- Reduction magnitude is consistent with the TIC threshold (e.g., top 80% TIC should reduce counts by ~20% on average, though variance per feature is expected).
- Features with low initial spectrum count (e.g., <5 spectra) may reduce to 0 or very small counts; verify this is acceptable for downstream consensus generation.
- Output dataframe row count equals the number of unique features in the input l1 list.
- Spot-check 2–3 named features (e.g., feature 1982, feature 872) and verify reported reductions match expected values (83→66, 43→34) from task documentation.

## Limitations

- TIC-based filtering assumes that low-TIC spectra are predominantly noise; in complex metabolites with multiple fragmentation pathways, some genuine structural isomers may be discarded.
- The top x% threshold is global; features with naturally low TIC variance may experience minimal reduction regardless of threshold.
- Per-feature counts depend on initial m/z and retention time tolerance used in preprocess(); loose tolerances inflate counts and mask filtering efficacy.
- This skill does not validate spectral quality or signal-to-noise; it only counts. A feature may have 66 spectra post-filter but still contain noisy or redundant fragments.

## Evidence

- [methods] Top 80% TIC cutoff reduced spectra counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872.: "From 83 before to 66 spectra after after top x% TIC"
- [methods] Extract the output Spectra object and dataframe showing before/after spectra counts per feature.: "Extract the output Spectra object (sps_top_tic_2) and dataframe (df) showing before/after spectra counts per feature"
- [methods] Top x% TIC extraction involves extracting the top x% TIC spectra and grouping fragments within specified mass tolerance.: "Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance"
- [readme] The extract_raw_spectra function extracts top x% TIC spectra and groups fragments within a given tolerance.: "l2 = extract_raw_spectra(folder_path = folder_path, l1_subset, 0.05, 0.8)"
- [readme] The workflow loads preprocessed spectra concatenated by feature and then applies TIC filtering.: "l1 = preprocess(folder_path = folder_path, tol_mz = 5, tol_rt = 0.1)"
