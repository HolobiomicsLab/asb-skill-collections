---
name: multi-factorial-experimental-design-handling
description: Use when your lipidomics dataset includes multiple experimental factors (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3407
  tools:
  - ADViSELipidomics
  - limma
  - edgeR
  - ComBat
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
- allows the identification of differentially abundant lipids in simple and complex experimental designs
- dealing with batch effect correction.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
---

# multi-factorial-experimental-design-handling

## Summary

Apply statistical linear models (limma, edgeR) to identify differentially abundant lipids across multi-factor and repeated-measures experimental designs while preserving biological signal through batch effect correction. This skill enables detection of lipid abundance changes in complex experimental layouts where simple pairwise comparisons are insufficient.

## When to use

Your lipidomics dataset includes multiple experimental factors (e.g., treatment + timepoint + genotype), repeated measures within subjects, or blocked designs, AND you need to detect differential lipid abundance while accounting for known batch effects (MS instrument run, sample plate, operator). Use this when batch effects are documented in your metadata and simple group-wise comparisons would conflate biological and technical variation.

## When NOT to use

- Your experimental design is simple (e.g., single binary treatment, no batch effects documented) — simpler methods (t-test, Wilcoxon) may be more appropriate and interpretable.
- Batch effects are unknown or not recorded in metadata — batch correction requires documented batch labels; blindly applying ComBat without batch information risks removing real biological signal.
- Your lipid abundance matrix has not been preprocessed and normalized — this skill assumes valid quantitative data; raw ion intensities or unnormalized counts require preprocessing first.

## Inputs

- Preprocessed and normalized lipid abundance matrix (rows: lipids, columns: samples; numeric values)
- Sample metadata table with batch identifiers, experimental group assignments, and factor levels
- Batch effect annotations (e.g., instrument run ID, plate number, processing date)

## Outputs

- Ranked differential lipid table (CSV) with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means
- Batch-corrected abundance matrix (ComBat-adjusted values)
- Linear model fit object with design matrix and contrast results

## How to apply

Load a preprocessed and normalized lipid abundance matrix with batch identifiers and experimental group assignments (e.g., sample metadata table with columns: sample_id, batch, treatment, timepoint, replicate). Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal. Construct a linear model design matrix accounting for all experimental factors and their interactions using limma or edgeR, which both support complex designs via model specification. Perform differential abundance testing across treatment groups or factor combinations using the batch-corrected matrix and the design model. Calculate fold-change, p-values, and adjusted p-values (FDR correction) for each lipid. Rank lipids by statistical significance and effect size, filtering for differentially abundant lipids meeting significance threshold (adjusted p < 0.05). The rationale is that linear models partition variance among multiple factors simultaneously, and batch correction before modeling prevents batch effects from masking true biological differences.

## Related tools

- **ComBat** (Batch effect correction method applied to the abundance matrix before statistical testing to remove systematic batch variation)
- **limma** (Linear modeling framework for differential abundance testing supporting multi-factor and repeated-measures designs)
- **edgeR** (Alternative linear modeling framework for differential abundance testing with support for complex experimental designs)
- **ADViSELipidomics** (Integrated Shiny application that orchestrates batch correction, linear model specification, and differential lipid detection in a single workflow) — https://github.com/ShinyFabio/ADViSELipidomics

## Examples

```
library("ADViSELipidomics"); run_ADViSELipidomics()
```

## Evaluation signals

- Batch-corrected abundance matrix shows reduced separation by batch ID and preserved separation by experimental treatment (visual inspection via PCA or heatmap before/after ComBat).
- Linear model design matrix correctly encodes all experimental factors and interactions; no aliased or rank-deficient columns.
- Differential lipid results include adjusted p-values (FDR) with majority below 0.05 threshold; effect sizes (log2 fold-change) are biologically plausible (typically ±0.5 to ±3 range for lipidomics).
- Output table rows match number of unique lipids in input matrix; no missing values in fold-change, p-value, or adjusted p-value columns.
- Batch-corrected mean abundances per group sum to expected total abundance; no negative values introduced by ComBat.

## Limitations

- ComBat assumes that batch effects are additive and similar across treatment groups; if batch-by-treatment interactions are strong, batch correction may remove important biological signal. Inspect batch-corrected vs. original data before proceeding.
- Linear models require sufficient replication per factor level; if some factor combinations have <2 samples, the model may be underpowered or rank-deficient.
- Adjusted p-values become conservative with many lipids tested; large-scale lipidomics (>1000 lipids) may result in few discoveries at FDR < 0.05. Consider relaxed thresholds (FDR < 0.10) or fold-change filtering (log2 FC > 1) for exploratory discovery.
- Missing data (NA or zero values) in the abundance matrix must be handled before batch correction; ComBat and limma have different tolerance for sparsity. Imputation or filtering may be necessary.

## Evidence

- [other] Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal.: "Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal."
- [other] Perform differential abundance testing using limma or edgeR for linear models supporting complex experimental designs (e.g., multi-factor, repeated measures).: "Perform differential abundance testing using limma or edgeR for linear models supporting complex experimental designs (e.g., multi-factor, repeated measures)."
- [intro] allows the identification of differentially abundant lipids in simple and complex experimental designs, dealing with batch effect correction.: "allows the identification of differentially abundant lipids in simple and complex experimental designs, dealing with batch effect correction."
- [other] Load preprocessed and normalized lipid abundance matrix (with batch identifiers and experimental group assignments).: "Load preprocessed and normalized lipid abundance matrix (with batch identifiers and experimental group assignments)."
- [other] Calculate fold-change, p-values, and adjusted p-values (FDR correction) for each lipid across treatment groups.: "Calculate fold-change, p-values, and adjusted p-values (FDR correction) for each lipid across treatment groups."
