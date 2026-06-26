---
name: mass-spectrometry-data-validation
description: Use when when reproducing or validating a tandem mass spectrometry denoising
  pipeline on mzML files with known feature precursor m/z and RT coordinates, compare
  pre- and post-filter counts of spectra and fragments at each major step (TIC cutoff,
  intra-spectrum grouping, frequency-based labeling).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - dures
  - dplyr
  - data.table
  - S4Vectors
  - Spectra
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
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils",
  "stats", "rPref", "ggplot2", "DEoptim"
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

# mass-spectrometry-data-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validates that MS/MS spectral denoising workflows correctly reduce fragment and spectrum counts according to expected thresholds and filter parameters. This skill involves reproducibly verifying intermediate data transformations (TIC-based filtering, intra-spectrum grouping, fragment frequency labeling) to ensure denoising does not introduce systematic errors or lose signal.

## When to use

When reproducing or validating a tandem mass spectrometry denoising pipeline on mzML files with known feature precursor m/z and RT coordinates, compare pre- and post-filter counts of spectra and fragments at each major step (TIC cutoff, intra-spectrum grouping, frequency-based labeling) against documented or expected reductions to confirm the pipeline is functioning as designed.

## When NOT to use

- Input spectra are already denoised or have been manually curated outside the documented pipeline; no intermediate reference counts are available.
- The feature metadata is missing precursor m/z or retention time, preventing reliable spectrum extraction and grouping.
- Only the final denoised output is available and intermediate snapshots (pre-TIC, post-grouping, pre-frequency-labeling) have not been saved or logged.

## Inputs

- mzML files (tandem mass spectrometry data)
- feature metadata (precursor m/z, retention time, feature ID) as txt or Stats.txt format
- preprocessed spectra list (Spectra object l1 from preprocess() call)
- reference peak count data (MS2_scans_before_denoising txt files or documented fragment/spectrum tallies)
- mass tolerance parameter (Da)
- TIC percentile threshold (e.g., 0.8 for top 80%)

## Outputs

- Pre/post filter comparison table (data.frame or data.table) with fragment or spectrum counts per feature
- Boolean validation report (PASS/FAIL per feature and per filter step)
- Numeric reduction ratios (e.g., 23→22, 98→81) compared against expected values
- Optional: discrepancy log flagging features where observed counts deviate from expected ranges

## How to apply

Load preprocessed MS/MS spectra using preprocess() with specified m/z and RT tolerances (e.g., 5 ppm and 0.1 min). At each filtering stage—top 80% TIC extraction, intra-spectrum fragment grouping (mass tolerance 0.05 Da), and frequency-based denoising—extract peak counts or spectrum counts from the Spectra object and compare them to independently verified reference counts (from MS2_scans files or prior literature). Verify that fragment reduction (e.g., 98→81 for feature 872) and spectrum reduction (e.g., 83→66 for feature 1982) match the expected thresholds. Use dplyr and data.table to join pre- and post-filter tallies and flag any discrepancies. The rationale is that bit-exact or threshold-consistent reproducibility of intermediate counts serves as a proxy for correctness of the grouping logic and tolerance parameters.

## Related tools

- **Spectra** (R/Bioconductor S4 class for storing and filtering MS/MS peak data; peaksData() extracts m/z and intensity arrays pre- and post-grouping)
- **dures** (R package containing preprocess(), extract_raw_spectra(), call_aggregate(), label_individual_spectrum() functions; orchestrates the five-step denoising workflow) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **dplyr** (Data frame filtering and joining to align pre/post counts by feature and filter stage)
- **data.table** (Efficient aggregation and tallying of spectrum or fragment counts per feature)
- **S4Vectors** (Dependency for Spectra S4 class object manipulation and metadata access)

## Examples

```
l1 <- preprocess(folder_path = folder_path, tol_mz = 5, tol_rt = 0.1); l2 <- extract_raw_spectra(folder_path, l1, 0.05, 0.8); observed_counts <- data.frame(feature = c(1982, 872), pre_spectra = c(83, 43), post_spectra = c(length(l2$sps_top_tic_2[l2$sps_top_tic_2$feature_id == 1982]), length(l2$sps_top_tic_2[l2$sps_top_tic_2$feature_id == 872]))); stopifnot(all(observed_counts$post_spectra == c(66, 34)))
```

## Evaluation signals

- Fragment count reduction for each feature matches expected values within a tolerance band (e.g., observed 81 == expected 81 for feature 872 intra-spectrum grouping).
- Spectrum count reduction after top 80% TIC filter is reproducible (e.g., feature 1982: 83→66, feature 872: 43→34).
- Cumulative fragment loss across all five denoising steps is consistent with published results (e.g., 23 fragments → 9 fragments after all steps).
- No spectra or fragments are lost unexpectedly between consecutive pipeline steps; total counts form a monotonic non-increasing sequence.
- Peak data extracted via Spectra::peaksData() before and after intra-spectrum grouping shows correct m/z merging (mean) and intensity summation within the specified mass tolerance (0.05 Da).

## Limitations

- Validation requires access to intermediate snapshots (Spectra objects, MS2_scans files) at each step; if only the final output is retained, reproducibility of intermediate counts cannot be verified.
- Expected reference counts must be independently verified or published; if documentation is incomplete or thresholds vary (e.g., TIC cutoff 0.8 vs. 0.85), expected values may not match observed ones and false negatives will occur.
- The skill assumes that m/z and RT tolerances are held constant across validation runs; changes in preprocess(tol_mz, tol_rt) or extract_raw_spectra(mass_tolerance) parameters will shift fragment and spectrum counts unpredictably.
- Pareto front analysis and frequency-based denoising (steps 4–5) introduce user-defined frequency thresholds (default = 0.1) that require tuning; validation of these steps is less deterministic than TIC and intra-spectrum grouping.

## Evidence

- [other] Verify reported reductions: feature 1982 from 23→22 fragments and feature 872 from 98→81 fragments by comparing pre- and post-grouping peak counts.: "Verify reported reductions: feature 1982 from 23→22 fragments and feature 872 from 98→81 fragments by comparing pre- and post-grouping peak counts."
- [other] Top 80% TIC cutoff reduced spectra counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872.: "Top 80% TIC cutoff reduced spectra counts from 83 to 66 for feature 1982 and from 43 to 34 for feature 872."
- [other] Extract peak data using Spectra::peaksData() before intra-spectrum grouping for features 1982 (spectrum scan_1587, expected 23 fragments) and 872 (spectrum scan_1120, expected 98 fragments).: "Extract peak data using Spectra::peaksData() before intra-spectrum grouping for features 1982 (spectrum scan_1587, expected 23 fragments) and 872 (spectrum scan_1120, expected 98 fragments)."
- [methods] After applying all five steps of the package, only 9 fragments remained from the original spectrum: "After applying all five steps of the package, only 9 fragments remained"
- [methods] In the second step, we will use `l1` from the previous step as input to: 1. **Extract the top x% TIC spectra**, and 2. **Group fragments** within a specified **mass tolerance**: "Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance"
- [methods] fragments within a default tolerance of **0.05 Da** of one another were merged: "fragments within a default tolerance of **0.05 Da** of one another were merged"
- [readme] This step removed fragments with frequencies below the given threshold (denoising step): "This step removed fragments with frequencies below the given threshold (denoising step)"
