---
name: batch-effect-correction-in-metabolomics
description: Use when you have a preprocessed and normalized lipid abundance matrix with documented batch identifiers and experimental group assignments, and you need to perform differential abundance testing across simple or complex experimental designs (multi-factor, repeated measures) where batch effects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-correction-in-metabolomics

## Summary

Removes systematic batch variation from lipidomics abundance matrices while preserving biological signal, enabling valid differential abundance testing across multi-batch experiments. This skill is essential when analyzing lipid data collected across multiple batches, instruments, or time points to prevent batch effects from confounding biological findings.

## When to use

Apply this skill when you have a preprocessed and normalized lipid abundance matrix with documented batch identifiers and experimental group assignments, and you need to perform differential abundance testing across simple or complex experimental designs (multi-factor, repeated measures) where batch effects could inflate false positives or mask true biological differences.

## When NOT to use

- Input is already batch-corrected or comes from a single batch or time point — applying correction unnecessarily may remove true biological heterogeneity.
- Batch identifiers are missing, unknown, or confounded with the experimental grouping — batch correction cannot reliably separate biological signal from technical artifact.
- Sample size is very small (e.g., n < 3 per batch) — batch correction methods require sufficient replication within batches to estimate the batch effect reliably.

## Inputs

- Preprocessed and normalized lipid abundance matrix (rows=lipids, columns=samples)
- Batch identifiers (one per sample)
- Experimental group assignments (treatment/control or multi-factor design)
- Sample metadata (optional: repeated measures, blocking factors)

## Outputs

- Batch-corrected lipid abundance matrix (same dimensions as input)
- Batch effect diagnostics (e.g., before/after PCA plots, variance explained by batch)
- Differential abundance results table (lipid_id, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means)
- Quality control report confirming batch signal removal

## How to apply

Load the abundance matrix with batch labels and sample metadata into ADViSELipidomics or a compatible environment. Apply ComBat or similar batch effect correction method to the normalized abundance values, configured to preserve the experimental group structure while removing systematic batch variation. After correction, verify that batch-level clustering is removed while sample grouping by experimental condition is maintained (e.g., by PCA or hierarchical clustering). Proceed to differential abundance testing using limma or edgeR with linear models that can accommodate complex designs. Report both raw and batch-corrected mean abundances per group in the final results table, and document the batch correction method and parameters in the methods section.

## Related tools

- **ComBat** (Empirical Bayes method for removing batch effects while preserving biological signal)
- **limma** (Linear models for differential abundance testing after batch correction, supporting complex experimental designs)
- **edgeR** (Generalized linear model approach for differential abundance testing on batch-corrected counts, alternative to limma)
- **ADViSELipidomics** (Shiny application integrating batch correction into a complete lipidomics analysis workflow) — https://github.com/ShinyFabio/ADViSELipidomics

## Examples

```
library("ADViSELipidomics"); run_ADViSELipidomics()
```

## Evaluation signals

- Batch-corrected abundance matrix has the same dimensions and lipid identifiers as the input; no samples or lipids are lost.
- PCA or t-SNE plot of batch-corrected data shows no clustering by batch, but samples cluster by experimental group/condition.
- Variance explained by batch (assessed via linear model or PERMANOVA on corrected data) is significantly reduced compared to uncorrected data.
- Differential abundance results include adjusted p-values (FDR-corrected, p < 0.05) and batch-corrected mean abundances per group, enabling interpretation of effect size.
- Sensitivity/specificity of detected lipids is reasonable: true positives align with known biology, and false discovery rate is controlled by FDR correction.

## Limitations

- Batch correction assumes batch effects are additive (ComBat model); multiplicative or interaction effects may not be fully removed.
- Correction requires sufficient sample replication within each batch; sparse designs may yield unreliable batch estimates.
- If batch is confounded with experimental group (e.g., all treatment samples from one batch, all control from another), batch correction cannot distinguish signal from artifact.
- Over-correction is possible if batch identifiers are misspecified; downstream analysis should validate that biological signal is preserved.
- ComBat and similar methods may not handle all complex nested or crossed designs; manual adjustment or alternative methods may be needed for highly imbalanced or multi-level batch structures.

## Evidence

- [intro] batch_effect_correction_method: "Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal."
- [intro] input_requirements: "Load preprocessed and normalized lipid abundance matrix (with batch identifiers and experimental group assignments)."
- [intro] differential_testing_tools: "Perform differential abundance testing using limma or edgeR for linear models supporting complex experimental designs (e.g., multi-factor, repeated measures)."
- [intro] output_format: "Export ranked differential lipid table as CSV with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means."
- [readme] capability_statement: "allows the identification of differentially abundant lipids in simple and complex experimental designs, dealing with batch effect correction."
