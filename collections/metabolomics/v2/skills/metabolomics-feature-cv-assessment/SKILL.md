---
name: metabolomics-feature-cv-assessment
description: Use when you have a feature intensity matrix from untargeted metabolomics (samples in rows, compounds in columns) and a sample legend identifying QC samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3370
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
---

# metabolomics-feature-cv-assessment

## Summary

Filter out non-reproducible features from untargeted metabolomics data by removing features whose coefficient of variation (CV%) in QC samples exceeds a specified reproducibility threshold. This is the first step in QC-based feature quality control to retain only stable, quantitatively reliable compounds.

## When to use

Apply this skill when you have a feature intensity matrix from untargeted metabolomics (samples in rows, compounds in columns) and a sample legend identifying QC samples. Use it early in the QC filtering pipeline to remove features with high measurement variability that indicate poor technical reproducibility before proceeding to detection frequency, blank contribution, or dilution series checks.

## When NOT to use

- Input is already a fully filtered feature table (e.g., from XCMS with downstream QC already applied).
- QC samples are not available or represent fewer than ~3 technical replicates per group.
- Analysis is targeted (known compound list with isotope-labelled standards); targeted assays often have high CV% by design and should not be pre-filtered by this threshold.

## Inputs

- df_example_feat_intensities: feature intensity matrix (samples × compounds)
- df_example_qc_sampletype: sample legend with sample type classifications (blank, curve, qc, unknown)

## Outputs

- QC-filtered feature table with step 1 applied (features with CV% ≤ cutoff retained)
- Filtered feature intensity matrix (samples × reduced number of compounds)

## How to apply

Load the feature intensity matrix and sample legend (with QC sample type classifications) into R. Execute the QCs_process function with step1=TRUE and specify a step1_cutoff threshold (typically 20–30% CV, depending on analytical platform and metabolite class). The function calculates the relative standard deviation (CV%) for each feature across all QC samples; any feature exceeding the cutoff is filtered out. The rationale is that high CV% in QC replicates indicates technical instability or measurement noise, compromising the reliability of downstream fold-change estimates and statistical inferences. Retain only features with CV% below the cutoff for subsequent multi-step QC filtering (steps 2–4) and biological analysis.

## Related tools

- **GetFeatistics** (R package providing the QCs_process function to execute step 1 CV% filtering on feature intensities) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Runtime environment (version ≥ 4.3.1) for executing QCs_process and feature filtering workflows)
- **XCMS** (Upstream feature extraction tool; output feature tables are fed into QCs_process for CV% filtering)
- **MS-Dial** (Upstream feature extraction tool; alternative source of feature intensity matrices for QC filtering)

## Examples

```
library(GetFeatistics); QCs_process(feat_intensities=df_example_feat_intensities, sample_legend=df_example_qc_sampletype, step1=TRUE, step1_cutoff=25, step2=FALSE, step3=FALSE, step4=FALSE)
```

## Evaluation signals

- Number of features retained should be 60–90% of input (typical retention after step 1); extreme loss (>95%) or no loss (<5%) suggests cutoff may be misspecified.
- Features retained should have CV% ≤ step1_cutoff in all QC samples; spot-check CV% distribution histogram before/after filtering to confirm no features above threshold remain.
- Output feature table dimensions should match input (same sample count, reduced compound count); no samples or rows should be dropped.
- QC sample intensities for retained features should show lower variance than features filtered out; compare median CV% of retained vs. discarded features.
- Downstream statistical tests (ANOVA, t-tests) on retained features should show improved effect size and power due to reduced noise; compare p-value distributions or effect size estimates from step 1-filtered vs. unfiltered data.

## Limitations

- CV% cutoff is user-defined and dataset-dependent; no universal optimal threshold exists. Metabolomics best-practice suggests 20–30% for most platforms, but lipids or derivatized compounds may tolerate higher CV%.
- Step 1 assumes QC samples are true technical replicates with no biological variation; if QC samples represent different QC pools or reference materials, CV% may inflate artificially and filtering may be too stringent.
- Features with intrinsically high noise (e.g., low-abundance, hydrophobic compounds, or those with ion suppression) may be filtered even if biologically relevant; loss of such features is unavoidable without alternative QC strategies (e.g., internal standards or normalization).
- Separate QC group processing (mentioned in task_003) may yield different retained feature sets per QC group; merging across groups can reintroduce some discordant features unless consensus criteria are applied.

## Evidence

- [intro] features with a relative standard deviation (CV%) greater than the value defined in the _step1_cutoff_ will be filtered out: "features with a relative standard deviation (CV%) greater than the value defined in the _step1_cutoff_ will be filtered out"
- [other] step1 removes features with CV% above cutoff: "step1 removes features with CV% above cutoff"
- [other] Execute QCs_process with step1_cutoff filtering to remove features with CV% above threshold in QC samples: "Execute QCs_process with step1_cutoff filtering to remove features with CV% above threshold in QC samples"
- [other] The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff: "The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff"
- [other] Load df_example_feat_intensities (feature intensity matrix with samples in rows, compounds in columns) and df_example_qc_sampletype (sample legend with type classifications: blank, curve, qc, unknown) into R.: "Load df_example_feat_intensities (feature intensity matrix with samples in rows, compounds in columns) and df_example_qc_sampletype (sample legend with type classifications: blank, curve, qc,"
