---
name: missing-value-imputation-by-data-recursion
description: Use when after sample alignment and feature grouping in untargeted LC-MS workflows, when the aligned feature table contains missing intensity values (NA or zero entries) due to features falling below the detection limit in some samples but being present above-threshold in others.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - manual expert review
  - SLAW
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# missing-value-imputation-by-data-recursion

## Summary

A gap-filling strategy for untargeted LC-MS feature tables that recursively searches related samples (by retention time and m/z proximity) to recover missing feature intensities, replacing NA or zero entries with values from alternate sample batches or replicates. This technique restores the sample-feature matrix structure without requiring external reference libraries.

## When to use

After sample alignment and feature grouping in untargeted LC-MS workflows, when the aligned feature table contains missing intensity values (NA or zero entries) due to features falling below the detection limit in some samples but being present above-threshold in others. Particularly valuable in large cohorts with thousands of samples where inter-sample missing patterns are systematic and correlated by m/z and retention time.

## When NOT to use

- Input is already a complete feature table with no missing values or has undergone aggressive filtering that removed features with >X% missing entries.
- The missing pattern is random or non-systematic across samples (e.g., random instrumental failure); data recursion assumes missingness is correlated by m/z and RT and will introduce bias if that assumption is violated.
- Samples belong to fundamentally different cohorts or experimental conditions with distinct metabolite profiles; recursive retrieval from unrelated samples may propagate false intensities.

## Inputs

- Aligned feature table with missing values (NA or zero entries) in sample-feature matrix format (rows=features, columns=samples)
- Feature metadata including retention time (RT) and m/z for each feature
- Sample grouping or batch/replicate information (implicit in column order or explicit metadata)

## Outputs

- Completed feature table with gap-filled intensity values in CSV or mzTab format
- Log or report of which features and samples had gaps filled and from which source samples the values were recursively retrieved

## How to apply

Load the aligned feature table produced by peak picking, sample alignment, and isotopologue/adduct grouping. For each missing intensity entry (NA or zero), apply a recursive search algorithm that queries related samples ranked by retention time proximity and m/z proximity to the target feature coordinates. When recursion identifies a matching feature with a non-missing intensity value in a related sample, transfer that intensity to the gap. Maintain the sample-feature matrix structure and output the completed table in CSV or mzTab format. The rationale is that features detected in one sample replicate or batch are biochemically present in related replicates; their absence in some samples reflects stochastic under-sampling or instrumental drift rather than true biological absence.

## Related tools

- **SLAW** (Complete untargeted LC-MS workflow that implements gap-filling by data recursion as an integrated step after alignment and isotopologue/adduct grouping) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm (one of three wrapped options in SLAW) that identifies features; outputs are aligned upstream of gap-filling)

## Evaluation signals

- Count and proportion of missing values (NA/zero entries) before and after gap-filling; expect significant reduction without complete elimination (some gaps may be unrecoverable if no related sample has the feature above threshold).
- Distribution of filled vs. unfilled gaps by m/z and RT ranges; verify that filled gaps cluster near their source samples' RT and m/z coordinates, indicating proximity-based recursion worked correctly.
- Comparison of gap-filled intensities against the source samples from which they were recursively retrieved; expect high correlation (e.g., Pearson r > 0.7) to confirm biological consistency.
- Sample-wise coverage: verify that rows (features) and columns (samples) maintain the original matrix dimensions and no spurious features or samples were introduced.
- Downstream statistical robustness: compare feature-level fold-changes, clustering, or PCA before and after gap-filling to confirm imputation does not artificially inflate or deflate effect sizes.

## Limitations

- The success of data recursion depends critically on the availability and abundance of related samples; cohorts with few replicates or widely scattered samples may yield low gap-filling rates.
- If the m/z and RT proximity thresholds are set too loosely, the algorithm may conflate true biological isobars or co-eluting isomers and propagate spurious intensities; if thresholds are too strict, genuine related features are missed.
- Imputation does not recover true quantitative information; filled values are proxies borrowed from related samples and may not reflect the true (unmeasured) intensity in the target sample, particularly if ionization efficiency varies across batches or replicates.
- Assumes missing entries are missing-at-random (MAR) or missing-completely-at-random (MCAR) conditional on m/z and RT; if missingness is driven by hidden sample-level confounders (e.g., instrument malfunction specific to one sample), recursion may propagate systematic bias.
- SLAW currently supports DDA (data-dependent acquisition) only; DIA-MS2 spectra are skipped, and MS2-only files ('MS2' flagged in samples.csv) will have MS2 mapped to MS1 features post-alignment but will not contribute to gap-filling itself.

## Evidence

- [other] Load aligned feature table with missing intensity values (NA or zero entries) from prior alignment step. Apply data recursion algorithm to identify features present in some samples but absent (below detection) in others. For each missing feature intensity, search recursively through related samples (by retention time and m/z proximity) to locate intensity values in alternate sample batches or replicates.: "Load aligned feature table with missing intensity values (NA or zero entries) from prior alignment step. Apply data recursion algorithm to identify features present in some samples but absent (below"
- [other] SLAW includes gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts.: "SLAW includes gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts."
- [other] Fill missing intensities using the recursively retrieved values, maintaining sample-feature matrix structure. Output completed feature table with filled intensities to CSV or mzTab format.: "Fill missing intensities using the recursively retrieved values, maintaining sample-feature matrix structure. Output completed feature table with filled intensities to CSV or mzTab format."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic"
