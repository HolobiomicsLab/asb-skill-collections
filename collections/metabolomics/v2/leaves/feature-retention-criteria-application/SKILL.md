---
name: feature-retention-criteria-application
description: Use when after signal drift correction and batch effect removal (step
  4) have been completed and per-feature D-Ratio values are available, but before
  normalization (step 7).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R
  - OUKS
  - OUKS (Omics Untargeted Key Script)
  - MetCorR
  - R (≥4.1.2)
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

# feature-retention-criteria-application

## Summary

Apply D-Ratio threshold filtering to remove low-quality metabolomic features from LC-MS feature tables during the Filtering step of untargeted metabolomics processing. This skill uses per-feature D-Ratio values—a quantitative metric of technical variation relative to biological variation—to retain only features meeting a preset acceptance criterion.

## When to use

After signal drift correction and batch effect removal (step 4) have been completed and per-feature D-Ratio values are available, but before normalization (step 7). Apply this skill when you need to reduce feature table noise by removing features with high technical variability relative to biological signal, which improves statistical power in downstream biomarker discovery.

## When NOT to use

- Feature table has not yet undergone signal drift correction and batch effect removal (step 4); D-Ratio values will not be reliable.
- D-Ratio metric is not appropriate for your experimental design or metabolomics platform (e.g., if technical replication or QC sample structure differs significantly from the OUKS protocol).
- Downstream analysis requires comprehensive feature coverage and can tolerate higher technical noise; aggressive filtering may remove biologically relevant features with acceptable but elevated D-Ratio values.

## Inputs

- Feature table (intensity matrix): rows = metabolomic features, columns = samples
- Per-feature D-Ratio values: numeric vector, one value per feature

## Outputs

- Filtered feature table: subset of input features meeting D-Ratio threshold
- Filter report: list of retained and removed features with their D-Ratio values

## How to apply

Load the feature table (intensity matrix) and corresponding per-feature D-Ratio values computed during the Correction step. Establish a D-Ratio threshold that defines the acceptance criterion for feature quality (the article does not specify an explicit threshold value, but the threshold should reflect acceptable technical-to-biological variance ratios for your experimental context). Apply the threshold filter: iterate through features and identify those with D-Ratio values meeting or exceeding the criterion. Subset the feature table to retain only passing features, discarding those below the threshold. Export the filtered feature table in the same tabular format as the input (e.g., CSV with features as rows and samples as columns).

## Related tools

- **OUKS (Omics Untargeted Key Script)** (Implements D-Ratio filtering as step 6 of the nine-step LC-MS untargeted metabolomics pipeline; step 4 (Correction) computes D-Ratio values; step 6 (Filtering) applies the threshold-based filter.) — https://github.com/plyush1993/OUKS
- **MetCorR** (Companion QC-GAM-based signal drift correction tool that produces cleaned feature intensities and D-Ratio-ready data for input to filtering step.) — https://github.com/plyush1993/MetCorR
- **R (≥4.1.2)** (Runtime environment for OUKS filtering scripts; required for threshold application and feature table subsetting operations.) — https://cloud.r-project.org/

## Examples

```
source('6. Filtering.R'); filtered_table <- apply_dratio_filter(feature_table = raw_features, dratio_values = per_feature_dratio, threshold = 0.5); write.csv(filtered_table, 'filtered_features.csv', row.names = TRUE)
```

## Evaluation signals

- Filtered feature table has fewer rows (features) than input table; all removed features have D-Ratio values below the threshold.
- Retained features show homogeneous D-Ratio distribution above the threshold with no outlier gaps or discontinuities.
- Feature count and D-Ratio statistics are documented in filter report; counts should be reproducible across re-runs with same threshold.
- Downstream statistical analysis (step 9) on filtered features shows improved effect size and reduced p-value inflation compared to unfiltered table, indicating noise reduction.
- Sample composition and metadata relationships are preserved (sample counts unchanged); only feature dimension is reduced.

## Limitations

- D-Ratio threshold value is not explicitly specified in the article; threshold selection relies on domain knowledge or empirical tuning and may require sensitivity analysis.
- D-Ratio metric assumes QC-replicate structure and regular batch/run order sampling; datasets with irregular QC sampling or non-standard batch designs may produce unreliable D-Ratio estimates.
- Filtering is irreversible; features removed below the threshold cannot be recovered. Overly aggressive thresholds may discard biologically relevant features with marginal technical variability.
- No documented benchmarking or validation of D-Ratio threshold sensitivity across different biological matrices, LC-MS instrument types, or metabolite classes.

## Evidence

- [other] OUKS step 6 (Filtering) applies D-Ratio filtering to the feature table, using per-feature D-Ratio values as a threshold-based mechanism to filter and reduce the dataset.: "OUKS step 6 (Filtering) applies D-Ratio filtering to the feature table, using per-feature D-Ratio values as a threshold-based mechanism to filter and reduce the dataset."
- [other] 1. Load the feature table and corresponding per-feature D-Ratio values from the correction step. 2. Apply the D-Ratio threshold filter (step 6 of OUKS) to identify features meeting the acceptance criterion. 3. Subset the feature table to retain only passing features. 4. Export the filtered feature table in the same format as the input.: "Load the feature table and corresponding per-feature D-Ratio values from the correction step. 2. Apply the D-Ratio threshold filter (step 6 of OUKS) to identify features meeting the acceptance"
- [readme] comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "R based open-source collection of scripts called :red_circle:*OUKS*:large_blue_circle: (*Omics Untargeted Key Script*) providing comprehensive nine step LC-MS untargeted metabolomic profiling data"
- [other] "6. Filtering": D-Ratio filtering was added.: ""6. Filtering": D-Ratio filtering was added."
- [other] "4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA: ""4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA"
