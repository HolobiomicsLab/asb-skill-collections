---
name: qc-dilution-consistency-validation
description: Use when after CV-based and blank-contribution filtering when you have untargeted metabolomics feature tables with QC samples that include dilution series (QC_half) and you need to ensure features exhibit consistent, approximately proportional intensity changes across dilution steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GetFeatistics
  - ggplot2
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

# QC dilution consistency validation

## Summary

Validates feature reproducibility and quantitative reliability by checking whether feature intensities in QC_half samples (dilution series) fall within an expected percentage range relative to undiluted QC mean intensity. This step filters out features with nonlinear or inconsistent dose–response behavior, ensuring only features suitable for quantitative analysis are retained.

## When to use

Apply this skill after CV-based and blank-contribution filtering when you have untargeted metabolomics feature tables with QC samples that include dilution series (QC_half) and you need to ensure features exhibit consistent, approximately proportional intensity changes across dilution steps. Use it to identify features that behave nonlinearly or show anomalous responses to dilution, which may indicate instrumental artifacts, ion suppression, or contamination.

## When NOT to use

- QC samples do not include a dilution series (QC_half); the feature table lacks replicate diluted QC samples.
- Feature table has already been filtered by other QC steps (CV, detection frequency, blank contribution); step 4 must be applied in the prescribed sequence with steps 1–3.
- Metabolites are expected to show nonlinear dose–response (e.g., due to known saturation or suppression); in such cases, adjust the percentage range threshold or skip this step for those features.

## Inputs

- Feature intensity matrix (samples × compounds, numeric)
- Sample legend table with sample type classifications (blank, curve, qc, qc_half, unknown)
- step4_cutoff parameter (percentage range, e.g. [0.20, 0.80] for 20–80% of QC mean)

## Outputs

- QC-filtered feature table with step 4 filtering applied (features passing dilution consistency check)
- Feature metadata (optional): boolean flag or list of features removed for failing dilution check

## How to apply

Load the feature intensity matrix (samples in rows, compounds in columns) and sample legend (with type classifications including 'qc' and 'qc_half' designations). Calculate the mean intensity for each feature across all QC samples and across QC_half (diluted) samples separately. Define a percentage range threshold (e.g., 20–80% of mean QC intensity) based on your expected dilution factor and acceptable nonlinearity tolerance. For each feature, check whether its mean intensity in QC_half falls within this range: features outside the range are filtered out, as they violate the expected linear (or near-linear) dose–response relationship. Apply this filtering per QC group (if multiple groups exist) before merging confirmed features across groups. The rationale is that features showing disproportionate or unexpected changes under dilution are likely unreliable for quantitation and should be removed.

## Related tools

- **GetFeatistics** (R package that implements QCs_process function with step4_cutoff parameter for dilution consistency validation in metabolomics feature tables) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Statistical computing environment required to execute GetFeatistics and QCs_process function)
- **ggplot2** (R package used for visualization of feature intensity distributions and QC filtering results)

## Examples

```
QCs_filtered <- QCs_process(df_example_feat_intensities, df_example_qc_sampletype, step1=TRUE, step1_cutoff=0.20, step2=TRUE, step2_cutoff=0.80, step3=TRUE, step3_cutoff=0.20, step4=TRUE, step4_cutoff=c(0.20, 0.80))
```

## Evaluation signals

- Verify that filtered feature set contains only features whose mean QC_half intensity falls within the specified percentage range of mean QC intensity (e.g., 20–80% for typical 2× dilution).
- Check that the number of features retained is lower than before step 4 filtering, and that removed features exhibit consistently anomalous dilution responses (e.g., QC_half mean < 20% or > 80% of QC mean).
- Confirm that separate QC group processing produces separate filtered feature lists that are correctly merged (union or intersection strategy) without duplicates.
- Validate that step 4 filtering reduces the proportion of features with nonlinear or suppressed dose–response curves, assessed via residual plots or dilution response linearity metrics.
- Cross-check that output feature table schema matches input (samples in rows, compounds in columns) with metadata columns indicating step 4 filter status.

## Limitations

- Step 4 filtering assumes approximately linear dose–response; features subject to ion suppression, saturation, or other nonlinear effects may be incorrectly discarded or may pass despite unreliability.
- The percentage range threshold (step4_cutoff) is user-defined and must be tailored to expected dilution factors; inappropriate thresholds may filter out valid features or retain artifacts.
- QC_half samples must be present in the sample legend and sufficiently replicated; sparse or missing dilution replicates reduce statistical power and may yield unstable estimates of mean QC_half intensity.
- Step 4 filtering is most effective when applied after steps 1–3 (CV, detection frequency, blank contribution); applying it in isolation or out of order may miss confounding sources of feature variability.

## Evidence

- [intro] step4_cutoff parameter definition and rationale: "if TRUE, features whose mean in "QC_half" samples are not between the percentage range of two values defined in _step4_cutoff_ compared to the mean of QCs will be filtered out"
- [intro] step 4 filtering as part of QCs_process sequential workflow: "step4 removes features with QC_half mean outside specified percentage range, with separate processing per QC group followed by merging of confirmed features across groups"
- [intro] integration into multi-step QC filtering pipeline: "The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff, step2 removes features absent in minimum QC percentage, step3 removes features"
- [intro] feature intensity matrix input format and QC sample legend structure: "Load df_example_feat_intensities (feature intensity matrix with samples in rows, compounds in columns) and df_example_qc_sampletype (sample legend with type classifications: blank, curve, qc, unknown)"
