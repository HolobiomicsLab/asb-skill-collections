---
name: lipid-abundance-differential-analysis
description: Use when you have a preprocessed and normalized lipid abundance matrix with batch identifiers and experimental group assignments, and you need to compare lipid levels across treatment conditions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - ADViSELipidomics
  - limma
  - edgeR
  - ComBat
  - LIPID MAPS
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-abundance-differential-analysis

## Summary

Identifies differentially abundant lipids across simple and complex experimental designs by applying batch effect correction and statistical testing to normalized lipid abundance matrices. This skill enables detection of lipids with significant fold-changes while controlling for systematic batch variation and multiple-testing error.

## When to use

Apply this skill when you have a preprocessed and normalized lipid abundance matrix with batch identifiers and experimental group assignments, and you need to compare lipid levels across treatment conditions (e.g., disease vs. control, or multi-factor designs) while accounting for known technical batch effects that could confound biological signals.

## When NOT to use

- Input is raw, unpreprocessed mass spectrometry data; use preprocessing and normalization steps first.
- No batch structure is present in the experiment; batch correction is unnecessary and may introduce spurious corrections.
- Samples lack explicit experimental group assignments or design is purely descriptive with no comparison groups defined.

## Inputs

- preprocessed normalized lipid abundance matrix (rows=lipids, columns=samples)
- batch identifiers per sample
- experimental group/treatment assignments per sample
- experimental design metadata (e.g., multi-factor covariates, repeated measures structure)

## Outputs

- ranked differential lipid table (CSV format with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means)
- filtered list of differentially abundant lipids meeting significance threshold
- batch-corrected abundance estimates per lipid per group

## How to apply

First, apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal in the normalized abundance matrix. Then perform differential abundance testing using limma or edgeR, which support complex experimental designs (multi-factor, repeated measures) and generate linear model estimates. Calculate log2 fold-change, raw p-values, and FDR-corrected p-values (adjusted p-value) for each lipid across all treatment group comparisons. Rank lipids by statistical significance and effect size, then filter for differentially abundant lipids meeting your significance threshold (typically adjusted p < 0.05). Finally, annotate results with lipid structural properties (class, chain length, saturation) and batch-corrected mean abundances per group for biological interpretation.

## Related tools

- **ComBat** (batch effect correction to remove systematic batch variation while preserving biological signal)
- **limma** (linear modeling for differential abundance testing supporting complex experimental designs)
- **edgeR** (differential abundance testing with support for complex experimental designs as alternative to limma)
- **ADViSELipidomics** (Shiny application integrating batch correction, differential abundance testing, and visualization) — https://github.com/ShinyFabio/ADViSELipidomics
- **LIPID MAPS** (lipid species classification and annotation of differential results)

## Examples

```
library(ADViSELipidomics); run_ADViSELipidomics()  # or programmatically: limma::lmFit(batch_corrected_matrix, design_matrix) %>% limma::eBayes() to obtain log2_fc, p_value, adj.P.Val for each lipid
```

## Evaluation signals

- Batch effect correction visually removes systematic clustering by batch in PCA or heatmap plots while preserving group separation.
- Adjusted p-values (FDR-corrected) follow expected distribution; false discovery rate control is demonstrated (e.g., q-value histogram peaked near 0).
- Differentially abundant lipids show consistent direction and magnitude of fold-change across replicates within treatment groups after batch correction.
- Ranked results include complete annotations (lipid class, chain length, saturation, batch-corrected means per group) enabling biological interpretation.
- Comparison of results before and after batch correction shows that batch-corrected log2 fold-changes are more stable and replicate-consistent than uncorrected values.

## Limitations

- Batch effect correction (e.g., ComBat) may be ineffective if batch and biological group structure are confounded; experimental design must allow batch and treatment effects to be separable.
- Linear models (limma, edgeR) assume normality and homogeneity of variance; heavily non-normal or zero-inflated lipid abundances may violate assumptions.
- Complex experimental designs require explicit specification of the design matrix; incorrect specification will produce biased fold-change and p-value estimates.
- Results depend critically on accurate batch assignment; missing or misclassified batch identifiers will lead to incomplete or erroneous batch correction.

## Evidence

- [intro] batch effect correction mechanism: "ADViSELipidomics implements a mechanism to identify differentially abundant lipids across simple and complex experimental designs by applying batch effect correction as part of the analysis workflow."
- [other] workflow steps including batch correction and statistical testing: "Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal. 3. Perform differential abundance testing using limma or edgeR"
- [other] output format and annotation requirements: "Export ranked differential lipid table as CSV with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means."
- [other] significance threshold specification: "filtering for differentially abundant lipids meeting significance threshold (adjusted p < 0.05)"
- [readme] capability for complex designs: "it allows the identification of differentially abundant lipids in simple and complex experimental designs, dealing with batch effect correction."
