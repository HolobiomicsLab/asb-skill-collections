---
name: d-ratio-threshold-filtering
description: Use when after signal drift correction (step 4) has computed per-feature
  D-Ratio values, and before normalization (step 7).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - OUKS
  - MetCorR
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
- comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# D-Ratio threshold filtering

## Summary

Apply per-feature D-Ratio values as quantitative thresholds to filter low-quality metabolomic features from LC-MS feature tables, removing signals with high technical variation relative to biological signal. This quality-control step reduces noise and improves downstream statistical power in untargeted metabolomics workflows.

## When to use

After signal drift correction (step 4) has computed per-feature D-Ratio values, and before normalization (step 7). Apply this filter when your feature table contains metabolomic signals with unknown or heterogeneous quality, particularly when batch effects or instrument drift have been partially corrected and you need to identify which features are reproducible enough for downstream statistical analysis or biomarker discovery.

## When NOT to use

- Input feature table has not yet undergone signal drift correction or D-Ratio computation — run step 4 (Correction) first.
- Per-feature D-Ratio values are not available or are missing for a subset of features.
- You have already manually curated or filtered features by other criteria and need to preserve those decisions; this filter may remove additional features that passed your prior screening.

## Inputs

- Feature table (intensity matrix, rows=features, columns=samples)
- Per-feature D-Ratio values (numeric vector, length=number of features)

## Outputs

- Filtered feature table (same format as input, subset of original features)
- Logical or integer vector indicating which features passed filtering

## How to apply

Load the feature table (intensity matrix) and the corresponding per-feature D-Ratio values computed during the Correction step. For each feature, compare its D-Ratio value against an acceptance threshold (the article uses per-feature D-Ratio as a threshold-based mechanism but does not specify a fixed cutoff value in the available text). Retain only features that meet the acceptance criterion; subset the feature table to exclude low-quality features. Export the filtered feature table in the same format (CSV or R object) as the input. The D-Ratio metric itself quantifies technical variation relative to biological signal; features with high D-Ratio values indicate poor reproducibility across QC samples or batches and should be removed.

## Related tools

- **OUKS** (R-based workflow framework implementing D-Ratio filtering as step 6 of a nine-step LC-MS untargeted metabolomics pipeline) — https://github.com/plyush1993/OUKS
- **R** (Programming language for loading feature tables, applying threshold logic, and subsetting data) — https://cloud.r-project.org/
- **MetCorR** (Companion package for QC-based signal drift correction (step 4) that computes D-Ratio values used by this filter) — https://github.com/plyush1993/MetCorR

## Evaluation signals

- Output feature table has fewer features than input (number of filtered-out features ≥ 1).
- All retained features have D-Ratio values meeting or exceeding the acceptance threshold; no feature below the threshold remains in the output.
- Feature names/IDs and sample columns are preserved in the output; only rows (features) are subset.
- Export format matches input format (CSV, RData, or R object); no loss of metadata or sample information.
- Filtering is reproducible: running the filter again on the same input with the same threshold produces identical output.

## Limitations

- D-Ratio threshold value is not explicitly specified in the available documentation; practitioners must determine or justify their own cutoff, potentially leading to inconsistent filtering across studies.
- The article does not provide validation or sensitivity analysis showing how threshold choice affects downstream biomarker discovery or statistical power.
- D-Ratio computation assumes that QC samples are representative of technical variation; if QC samples are not truly comparable or are collected under different conditions, D-Ratio may not reliably indicate feature quality.
- No benchmarking or comparison against alternative quality filters (e.g., relative standard deviation, blank-to-sample ratio, signal-to-noise) is provided.

## Evidence

- [other] OUKS step 6 (Filtering) applies D-Ratio filtering to the feature table, using per-feature D-Ratio values as a threshold-based mechanism to filter and reduce the dataset.: "OUKS step 6 (Filtering) applies D-Ratio filtering to the feature table, using per-feature D-Ratio values as a threshold-based mechanism to filter and reduce the dataset."
- [other] Workflow: 1. Load the feature table and corresponding per-feature D-Ratio values from the correction step. 2. Apply the D-Ratio threshold filter (step 6 of OUKS) to identify features meeting the acceptance criterion. 3. Subset the feature table to retain only passing features. 4. Export the filtered feature table in the same format as the input.: "Load the feature table and corresponding per-feature D-Ratio values from the correction step. 2. Apply the D-Ratio threshold filter (step 6 of OUKS) to identify features meeting the acceptance"
- [readme] comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "R based open-source collection of scripts called OUKS (*Omics Untargeted Key Script*) providing comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox"
- [other] "6. Filtering": D-Ratio filtering was added.: ""6. Filtering": D-Ratio filtering was added."
- [readme] peaks filtering for quality checking and accounting of technical variation: "peaks filtering for quality checking and accounting of technical variation"
