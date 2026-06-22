---
name: ms2-spectra-tic-filtering
description: Use when after concatenating replicate MS/MS spectra for each precursor feature (m/z and retention time), use this skill when you have multiple replicate scans per feature and need to reduce spectral count while preserving the highest-intensity, most-reliable spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - dures
  - S4Vectors
  - dplyr
  - readr
  - magrittr
  - pbapply
  - data.table
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim"
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

# ms2-spectra-tic-filtering

## Summary

Filter tandem mass spectrometry replicate spectra by retaining only those with Total Ion Current (TIC) in the top x% (typically 80%) of the distribution for a given precursor feature. This reduces spectral redundancy and noise before consensus spectrum generation and fragment frequency calculation.

## When to use

After concatenating replicate MS/MS spectra for each precursor feature (m/z and retention time), use this skill when you have multiple replicate scans per feature and need to reduce spectral count while preserving the highest-intensity, most-reliable spectra. Apply it before intra-spectrum fragment grouping and consensus spectrum generation to focus on signal-rich replicates.

## When NOT to use

- Input spectra have already been quality-filtered by TIC or intensity threshold upstream.
- All replicate spectra for a feature must be retained for downstream statistical analyses (e.g., replicate consistency assessment).
- The dataset contains single-scan (non-replicate) spectra per feature; TIC filtering will not reduce spectrum count meaningfully.

## Inputs

- Concatenated replicate MS/MS spectra (Spectra object) from preprocessing step
- Preprocessed spectra list (l1) containing all features with replicate scans
- Folder path containing mzML files and feature statistics
- Top TIC percentage threshold (scalar, 0–1; typically 0.8)

## Outputs

- Filtered Spectra object (sps_top_tic_2) containing only top x% TIC spectra per feature
- Data frame (df) with before/after spectrum counts per feature
- Grouped fragment peaks with merged m/z values and summed intensities within mass tolerance

## How to apply

Load the concatenated replicate spectra list (Spectra object) for all features from the preprocessing step. Call extract_raw_spectra() with a top TIC threshold parameter (typically 0.8 for 80th percentile). The function ranks spectra for each feature by their total ion current, selects only those above the cutoff, and returns a filtered Spectra object and a data frame showing before/after spectrum counts per feature. Verify the filtering by comparing reported spectrum counts: for example, feature 1982 should reduce from 83 to 66 spectra, and feature 872 from 43 to 34 spectra when using the 80% TIC threshold. The mass tolerance parameter (default 0.05 Da) is applied during intra-spectrum fragment grouping that occurs concurrently with TIC filtering.

## Related tools

- **Spectra** (S4 container for storing and manipulating MS/MS spectra objects; peaksData() extracts fragment m/z and intensity pairs for verification)
- **dures** (Provides extract_raw_spectra() function that implements top x% TIC filtering and intra-spectrum fragment grouping) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **data.table** (Handles before/after spectrum count tabulation and filtering output)
- **dplyr** (Data frame manipulation for filtering and summarizing spectrum counts per feature)

## Examples

```
l2 = extract_raw_spectra(folder_path = folder_path, l1, 0.05, 0.8)
```

## Evaluation signals

- Spectrum count reduction per feature matches expected values: verify that feature 1982 reduces from 83→66 and feature 872 from 43→34 when using 80% TIC cutoff.
- All remaining spectra have TIC values ≥ the calculated threshold (80th percentile) for their feature.
- Output Spectra object contains no duplicate scans and maintains correct feature-to-spectrum associations.
- Intra-spectrum fragment grouping (mass tolerance 0.05 Da) is successfully applied: fragments merged by m/z mean, intensities summed; verify fragment count reduction in filtered output.
- Data frame output has one row per feature with columns: feature_id, spectra_before, spectra_after; no missing values.

## Limitations

- TIC filtering is sensitive to the choice of percentile threshold (e.g., 80% vs. 90%); no universal optimal value is recommended; users should tune using Pareto front analysis (see dures-vignette-tuning).
- Features with very few replicate spectra (<3) may be reduced to 0 spectra if all fall below the TIC cutoff; such features should be flagged or excluded.
- TIC filtering assumes replicate spectra have comparable ionization efficiency and detector response; biased MS acquisition (e.g., time-dependent signal decay) can distort TIC distributions.
- Mass tolerance parameter (0.05 Da default) is applied during fragment grouping concurrently with TIC filtering; misspecification will affect both fragment counts and overall downstream results.

## Evidence

- [other] Does applying a top 80% TIC selection filter reduce the per-feature spectrum counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872 in test_1?: "Does applying a top 80% TIC selection filter reduce the per-feature spectrum counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872"
- [other] Top 80% TIC cutoff reduced spectra counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872.: "Top 80% TIC cutoff reduced spectra counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872"
- [other] Call extract_raw_spectra() with parameters: folder_path, l1, mass tolerance 0.05 Da, and top TIC threshold 0.8 (80%).: "Call extract_raw_spectra() with parameters: folder_path, l1, mass tolerance 0.05 Da, and top TIC threshold 0.8 (80%)"
- [methods] In the second step, we will use `l1` from the previous step as input to: 1. **Extract the top x% TIC spectra**, and 2. **Group fragments** within a specified **mass tolerance**: "Extract the top x% TIC spectra, and 2. **Group fragments** within a specified **mass tolerance**"
- [readme] This step extracts the top 80% TIC spectra and groups fragments within a given mass tolerance: "This step extracts the top 80% TIC spectra and groups fragments within a given mass tolerance"
- [readme] l2 = extract_raw_spectra(folder_path = folder_path, l1_subset, 0.05, 0.8): "l2 = extract_raw_spectra(folder_path = folder_path, l1_subset, 0.05, 0.8)"
