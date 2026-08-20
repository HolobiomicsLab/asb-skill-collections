---
name: fold-change-and-p-value-ranking
description: Use when after performing differential abundance testing (via limma or
  edgeR) on batch-corrected lipid abundance data, use this skill to rank and filter
  lipids when you need to prioritize results by both effect size and statistical confidence,
  especially in complex experimental designs with.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - ADViSELipidomics
  - limma
  - edgeR
  - ComBat
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration
  per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization
  of lipidomics data.
- allows the identification of differentially abundant lipids in simple and complex
  experimental designs
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

# fold-change-and-p-value-ranking

## Summary

Rank differentially abundant lipids by fold-change magnitude and statistical significance (p-value and FDR-adjusted p-value) to identify the most robust and biologically meaningful changes across treatment groups. This skill filters candidates by significance threshold and produces an interpretable ranked table for downstream validation and annotation.

## When to use

After performing differential abundance testing (via limma or edgeR) on batch-corrected lipid abundance data, use this skill to rank and filter lipids when you need to prioritize results by both effect size and statistical confidence, especially in complex experimental designs with multiple treatment comparisons or repeated measures.

## When NOT to use

- Input lipid abundance matrix has not been batch-corrected; apply batch effect correction (ComBat or similar) first.
- Differential abundance testing has not yet been performed; run limma or edgeR linear models before ranking.
- Data lacks replicate structure or group assignments needed to define contrasts for fold-change calculation.

## Inputs

- batch-corrected lipid abundance matrix (samples × lipids)
- experimental group assignments (per-sample factor vector)
- design matrix for linear model (supports multi-factor and repeated-measures designs)
- lipid annotation table (lipid_id, lipid_class, chain_length, saturation)

## Outputs

- ranked differential lipid table (CSV): lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means
- filtered lipid result set (meeting adjusted p < 0.05 threshold)

## How to apply

Calculate log2-fold-change and p-values for each lipid from the linear model output; apply FDR correction (e.g. Benjamini-Hochberg) to account for multiple testing. Rank lipids by adjusted p-value (ascending) and secondarily by absolute log2-fold-change (descending) to surface both statistically significant and biologically meaningful changes. Filter for differentially abundant lipids meeting adjusted p-value threshold (typically adjusted p < 0.05). Annotate the ranked results with batch-corrected mean abundances per group, lipid class, chain length, and saturation information to enable biological interpretation and confidence assessment.

## Related tools

- **limma** (linear model framework for differential abundance testing with complex design support; produces fold-change and p-value estimates per lipid)
- **edgeR** (alternative linear model and count-based framework for differential abundance testing; supports generalized linear models for complex designs)
- **ADViSELipidomics** (integrated Shiny application that implements ranking, filtering, annotation, and export of differentially abundant lipids with batch-corrected means) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- Adjusted p-values are monotonically ordered (ascending); no p-value exceeds 0.05 in filtered output.
- Each row contains non-null values for log2_fold_change, p_value, adjusted_p_value, and per-group batch-corrected mean abundances.
- Lipid annotation columns (lipid_class, chain_length, saturation) are populated and consistent with input lipid reference.
- Rank order correlates with both statistical significance and effect size: top-ranked lipids show lowest adjusted p-values and highest |log2-fold-change|.
- Output CSV schema matches declared format; numeric columns are numeric; no missing values in required fields.

## Limitations

- Ranking relies on FDR correction accuracy; extreme p-value distributions or very small sample sizes may inflate false discovery rates despite conservative thresholds.
- Fold-change may be inflated when baseline (control group) abundance is near detection limit; consider supplementary filters on minimum fold-change or effect size.
- Batch effect correction quality directly impacts result validity; residual batch effects that survive ComBat or similar tools will inflate or deflate fold-changes unpredictably.
- Complex experimental designs (multi-factor, repeated measures) require correctly specified design matrix; misspecification will produce invalid contrasts and ranking.

## Evidence

- [other] Calculate fold-change, p-values, and adjusted p-values: "Calculate fold-change, p-values, and adjusted p-values (FDR correction) for each lipid across treatment groups."
- [other] Rank lipids by statistical significance and effect size: "Rank lipids by statistical significance and effect size, filtering for differentially abundant lipids meeting significance threshold (adjusted p < 0.05)."
- [other] Annotate results with lipid class, chain length, saturation, and batch-corrected mean abundances: "Annotate results with lipid class, chain length, saturation, and batch-corrected mean abundances per group."
- [other] Export ranked differential lipid table as CSV: "Export ranked differential lipid table as CSV with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means."
- [other] limma or edgeR for linear models supporting complex experimental designs: "Perform differential abundance testing using limma or edgeR for linear models supporting complex experimental designs (e.g., multi-factor, repeated measures)."
