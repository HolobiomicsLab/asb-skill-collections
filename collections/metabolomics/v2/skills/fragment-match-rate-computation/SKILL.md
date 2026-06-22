---
name: fragment-match-rate-computation
description: Use when after denoising MS/MS spectra at multiple frequency thresholds and matching each thresholded spectrum against a -matching reference spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rPref
  - DEoptim
  - dplyr
  - ggplot2
  - pbapply
  - magrittr
  - stats
  - data.table
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim"
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

# fragment-match-rate-computation

## Summary

Compute the ratio of matched fragments to total fragments in a spectrum after comparing denoised MS/MS spectra against a reference spectrum using dot product-based metrics. This metric quantifies spectral matching quality and is used to evaluate whether frequency-based denoising improves or degrades fragment recovery.

## When to use

Apply this skill after denoising MS/MS spectra at multiple frequency thresholds and matching each thresholded spectrum against a best-matching reference spectrum. The fragment match rate is computed for each threshold to assess whether denoising retains signal fragments (those present in the reference) or removes them, enabling trade-off analysis between signal retention and noise reduction.

## When NOT to use

- Input spectra have not yet been matched against a reference spectrum using dot product or similar similarity metrics; match must precede rate computation.
- Reference spectrum is not reliably identified or is of poor quality; ambiguous reference matching will propagate uncertainty into the fragment match rate.
- Analysis goal does not require threshold optimization; if a fixed frequency threshold is used without Pareto front evaluation, per-threshold fragment match rates are not needed.

## Inputs

- Denoised MS/MS spectra (subspectra) thresholded at each frequency level
- Best-matching reference spectrum (MS/MS spectrum from curated library)
- Matched fragment lists from dot product-based spectral comparison

## Outputs

- Fragment match rate (numeric: matched fragments / total fragments in denoised spectrum)
- Fragment match rates table per threshold per feature
- After_denoising_matches/ directory with match details (dot products, fragment counts, match rates)

## How to apply

For each denoised spectrum at a given frequency threshold, match its fragments against the best-matching reference spectrum (pre-identified before denoising) using dot product-based metrics. Count the number of fragments in the denoised spectrum that align with fragments in the reference spectrum, then divide by the total number of fragments in the denoised spectrum to obtain the fragment match rate. Repeat this calculation across all 101 frequency thresholds (0.00 to 1.00 in 0.01 increments) for each feature. Store matched results in After_denoising_matches/ directory. The fragment match rate directly informs Pareto front analysis: thresholds yielding higher match rates with positive signal retention are preferred for identifying optimal denoising parameters.

## Related tools

- **dplyr** (Compute and aggregate fragment match rate statistics across features and thresholds)
- **data.table** (Store and retrieve matched fragment data with rapid lookup and filtering by threshold and feature)
- **pbapply** (Apply fragment match rate computation in parallel across multiple features for performance)
- **rPref** (Use fragment match rates as one objective in Pareto front analysis to identify optimal thresholds)

## Evaluation signals

- Fragment match rate values lie in [0, 1] for all thresholds; values outside this range indicate computational error.
- Fragment match rates monotonically increase or remain stable as frequency threshold decreases (lower thresholds retain more fragments, including those matching the reference).
- Thresholds with fragment match rates ≥ threshold used in final denoising step l5 show positive signal retention (no loss of matching fragments).
- CSV files in pareto_results/csv/ contain complete fragment match rate records; spot-check 2–3 features to verify match counts sum correctly.
- Summary dataframe returned by tuning function includes 'fragment_match_rate' column with non-null numeric values for all selected optimal features.

## Limitations

- Fragment match rate depends entirely on the quality and coverage of the reference spectrum library; if the reference spectrum is incomplete or incorrect, fragment match rates will not reflect true signal recovery.
- Fragment match rate does not account for fragment intensity or m/z accuracy; two spectra may have identical fragment counts but different dot product scores due to peak height or mass error differences.
- Match rate is computed only for fragments that pass the dot product threshold during matching; if the dot product threshold is too stringent, valid matching fragments may be missed, artificially lowering the fragment match rate.
- For features with very few fragments in the reference spectrum, fragment match rates exhibit high variance and may not reliably reflect denoising quality.

## Evidence

- [methods] Match all thresholded spectra against the best-matching reference spectrum (identified before denoising in l6) using dot product-based metrics and fragment match rates, storing results in After_denoising_matches/.: "Match all thresholded spectra against the best-matching reference spectrum (identified before denoising in l6) using dot product-based metrics and fragment match rates"
- [methods] Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold.: "Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold"
- [methods] Merge results into a summary table and return a filtered dataframe containing optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match rates, and selected features.: "return a filtered dataframe containing optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match rates, and selected features"
- [methods] Iterate over each matched feature in l5 and retrieve its annotated MS/MS spectra from l4. 2. Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra: "Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra"
- [readme] Where: **Modified Dot Product** measures spectral similarity; **NMF** = Number of Matching Fragments: "**Modified Dot Product** measures spectral similarity; **NMF** = Number of Matching Fragments"
