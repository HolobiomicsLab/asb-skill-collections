---
name: blank-contamination-ratio-evaluation
description: Use when you have a feature intensity matrix with both blank and QC (quality control) samples and need to remove features whose background contamination is too high relative to their signal in QC samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GetFeatistics
  - XCMS
  - MS-Dial
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration of metabolomics data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# blank-contamination-ratio-evaluation

## Summary

Filtering features from untargeted metabolomics data by removing those where the mean blank intensity exceeds a threshold ratio of the mean QC intensity, thereby eliminating contamination artifacts and non-specific signals. This step validates feature quality by detecting whether features are driven by background rather than true analyte signal.

## When to use

Apply this skill when you have a feature intensity matrix with both blank and QC (quality control) samples and need to remove features whose background contamination is too high relative to their signal in QC samples. This is especially critical in untargeted metabolomics workflows after initial feature extraction from XCMS or MS-Dial output, to distinguish genuine metabolites from contaminants introduced during sample preparation or measurement.

## When NOT to use

- Workflow has no blank samples (sampling strategy did not include blanks for contamination control).
- Feature intensity matrix has already been QC-filtered by a prior pipeline; applying step 3 again risks over-filtering and losing valid signals.
- Analysis targets only targeted metabolomics with pre-validated compound lists where blank contamination has been ruled out a priori.

## Inputs

- feature intensity matrix (samples in rows, compounds/features in columns)
- sample legend with type classifications (blank, curve, qc, unknown)
- step3_cutoff parameter (numeric, ratio threshold; e.g., 0.5)

## Outputs

- filtered feature intensity matrix with blank-contaminated features removed
- list of removed feature identifiers and their blank contribution ratios

## How to apply

Calculate the ratio of mean blank intensity to mean QC intensity for each feature. Remove any feature whose blank contribution ratio (mean blank / mean QC) exceeds the step3_cutoff threshold specified by the user. The rationale is that a high blank ratio indicates the feature signal is largely driven by background noise rather than true sample analyte, making it unreliable for downstream metabolomics analysis. The cutoff threshold should be set conservatively (e.g., 0.5 or lower) depending on the analytical method's sensitivity and blank handling protocols. Apply this filtering after step 1–2 QC filtering (CV and detection frequency checks) but before step 4 (dilution series validation), as blank contamination is independent of feature reproducibility but precedes concentration-response validation.

## Related tools

- **GetFeatistics** (R package implementing QCs_process function with step3_cutoff parameter for blank contamination filtering) — https://github.com/FrigerioGianfranco/GetFeatistics
- **XCMS** (Upstream tool for initial feature extraction; output is the input to blank-contamination-ratio-evaluation)
- **MS-Dial** (Alternative upstream tool for initial feature extraction; output is the input to blank-contamination-ratio-evaluation)

## Examples

```
QCs_process(df_example_feat_intensities, df_example_qc_sampletype, step3 = TRUE, step3_cutoff = 0.5)
```

## Evaluation signals

- Number of features removed is reasonable relative to total features (typically 5–20% of features, depending on cutoff stringency and experimental design).
- Removed features have blank/QC ratios ≥ step3_cutoff; retained features have blank/QC ratios < step3_cutoff.
- Blank contribution ratio distribution in retained features is skewed toward low values (mean << step3_cutoff), confirming removal of high-contamination outliers.
- Downstream statistics (e.g., fold-change, ANOVA p-values) show improved effect sizes and reduced noise variance in retained features compared to pre-filtered data.
- Visual inspection of heatmaps or PCA plots post-filtering shows reduced clustering artifacts driven by blank samples.

## Limitations

- Effectiveness depends on quality of blank sample collection and handling; if blanks are contaminated or improperly prepared, the filter may remove valid signals or fail to remove actual contaminants.
- A single scalar cutoff may be suboptimal for features with widely varying dynamic ranges; features with low abundance may have high blank ratios even when absolute blank intensities are negligible.
- Does not distinguish between systemic contamination (e.g., solvent residues) and feature-specific contamination; all features are evaluated against the same threshold.
- Requires blank samples to be present and annotated correctly in the sample legend; missing or misclassified blanks will invalidate the filtering step.

## Evidence

- [intro] step3 removes features with blank contribution ratio above cutoff: "step3 removes features with blank contribution ratio (mean blank / mean QC) exceeding threshold"
- [intro] blank contribution defined as ratio of mean blank to mean QC: "features with a blank contribution, i.e.: the ratio between mean of blank and mean of QC, greater than the value defined in the _step3_cutoff_ will be filtered out"
- [intro] step3 is applied as part of multi-step QC filtering sequence: "The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff, step2 removes features absent in minimum QC percentage, step3 removes features"
- [readme] QCs_process function integrates step3 filtering in R workflow: "Getting streamlined elaboration of targeted and non-targeted metabolomics data, including elaboration of feature tables, separate QC processing, advanced statistics"
