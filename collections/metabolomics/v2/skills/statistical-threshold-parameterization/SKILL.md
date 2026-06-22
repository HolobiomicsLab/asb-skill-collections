---
name: statistical-threshold-parameterization
description: Use when when you have computed fold-change and p-value statistics from differential expression analysis and need to partition the results into significant and non-significant regions for visualization or downstream filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0203
  tools:
  - R Shiny
  - GraphBio
derived_from:
- doi: 10.3389/fgene.2022.957317
  title: GraphBio
evidence_spans:
- GraphBio---A modular and scalable R Shiny dashboard
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphbio_cq
    doi: 10.3389/fgene.2022.957317
    title: GraphBio
  dedup_kept_from: coll_graphbio_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fgene.2022.957317
  all_source_dois:
  - 10.3389/fgene.2022.957317
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-threshold-parameterization

## Summary

Selection and application of p-value and fold-change cutoff thresholds to classify differential expression results and filter omics data for downstream visualization. This skill is essential for converting continuous statistical measures into categorical signals (significant vs. non-significant) in volcano plots and related omics workflows.

## When to use

When you have computed fold-change and p-value statistics from differential expression analysis and need to partition the results into significant and non-significant regions for visualization or downstream filtering. Typical triggers include: (1) plotting volcano plots where you must define significance boundaries, (2) filtering gene lists prior to enrichment analysis, or (3) applying study-specific statistical cutoffs (e.g., p < 0.05, |log2 fold-change| > 1) rather than accepting software defaults.

## When NOT to use

- Input p-values have not been corrected for multiple comparisons (e.g., raw t-test p-values without Benjamini–Hochberg adjustment); use adjusted p-values instead.
- You are working with pre-filtered or pre-thresholded data where significance has already been assigned; re-thresholding may cause inconsistency.
- Your analysis goal does not require a binary significant/non-significant distinction (e.g., you need to rank all genes continuously without hard cutoffs).

## Inputs

- CSV file with columns: fold change (linear or log2-transformed), p-value
- Numeric fold-change vector
- Numeric p-value vector

## Outputs

- Volcano plot with threshold lines rendered
- Boolean vector or data frame indicating which rows exceed threshold on both axes
- Filtered subset of significant rows (fold-change AND p-value passing thresholds)

## How to apply

Define significance thresholds on two axes: statistical significance (typically p-value ≤ 0.05, visualized as −log10(p-value) on the y-axis) and biological effect size (fold-change, typically |log2 fold-change| ≥ 1 on the x-axis). Compute the −log10(p-value) transformation to make small p-values visually prominent. Render threshold lines as reference boundaries on the plot (horizontal line at −log10(0.05) ≈ 1.3 and vertical lines at ±log2 fold-change cutoffs). Filter or highlight points exceeding both thresholds as significant hits. The rationale is that requiring both statistical and biological thresholds reduces false positives and focuses downstream analysis on robust, reproducible signals.

## Related tools

- **R Shiny** (Interactive web framework for rendering volcano plots with user-adjustable threshold lines and significance highlighting) — https://github.com/databio2022/GraphBio
- **GraphBio** (Omics visualization dashboard implementing volcano plot generation with built-in fold-change and p-value thresholding) — https://github.com/databio2022/GraphBio

## Evaluation signals

- Threshold lines are correctly positioned: horizontal line at −log10(p) corresponding to chosen p-value cutoff (e.g., 1.3 for p=0.05), vertical lines at ±fold-change cutoff on x-axis.
- Points classified as significant (above horizontal AND beyond vertical thresholds) form a consistent subset; verify no points are marked significant that fail either criterion.
- Exported plot or data frame correctly filters rows where |fold-change| exceeds cutoff AND p-value ≤ threshold; spot-check a few rows manually.
- Threshold parameters are documented in plot legend or caption, allowing reproducibility and comparison across studies.
- The number of significant hits is biologically plausible and consistent with prior knowledge (e.g., not filtering away all genes or marking almost all as significant).

## Limitations

- Hard threshold cutoffs (e.g., p=0.05) are arbitrary and may miss borderline signals; consider sensitivity analysis by varying thresholds.
- P-value thresholds do not account for effect size direction; supplementary analyses (e.g., pathway enrichment) should validate biological plausibility.
- GraphBio and similar tools do not perform correction for multiple comparisons automatically; users must supply corrected p-values or apply post-hoc correction.
- Visualization in 2D (fold-change vs. p-value) ignores other relevant metrics (e.g., expression level, variance homogeneity) that may influence confidence in calls.

## Evidence

- [other] Generate interactive volcano plot using R Shiny with significance threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on x-axis).: "Generate interactive volcano plot using R Shiny with significance threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on x-axis)."
- [other] Compute −log10(p-value) transformation for the y-axis.: "Compute −log10(p-value) transformation for the y-axis."
- [readme] volcano_example.csv and volcano_example1.csv for volcano plot: "volcano_example.csv and volcano_example1.csv for volcano plot."
- [other] GraphBio provides volcano plot visualization functionality that accepts demo data files (volcano_example.csv and volcano_example1.csv) as inputs to generate volcano plots depicting statistical significance versus fold change relationships.: "GraphBio provides volcano plot visualization functionality that accepts demo data files (volcano_example.csv and volcano_example1.csv) as inputs to generate volcano plots depicting statistical"
