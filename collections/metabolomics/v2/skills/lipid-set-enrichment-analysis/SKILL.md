---
name: lipid-set-enrichment-analysis
description: Use when after completing two-group or multi-group differential expression analysis on lipidomics data when you have computed log fold-change (logFC) values and want to identify which lipid classes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0153
  tools:
  - lipidr
  - R
  - limma
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Lipid Set Enrichment Analysis (LSEA) Ranked by Log Fold-Change

## Summary

Lipid set enrichment analysis (LSEA) identifies significantly enriched or depleted lipid classes and chain properties by ranking individual lipid molecules according to log fold-change from differential expression results. This technique reveals coordinated regulation patterns across predefined lipid sets that may not be apparent from individual lipid statistics alone.

## When to use

Apply this skill after completing two-group or multi-group differential expression analysis on lipidomics data when you have computed log fold-change (logFC) values and want to identify which lipid classes (e.g., PC, PG, CL, TG) or chain-length/unsaturation features show coordinated enrichment or depletion across the ranked lipid list, rather than examining individual lipids in isolation.

## When NOT to use

- Input lipid-level data lacks log fold-change values or statistical ranking (use univariate analysis first)
- Sample size is too small to reliably estimate differential expression (typically need n ≥ 3 per group)
- Research question focuses on individual lipid biomarkers rather than coordinated lipid class regulation

## Inputs

- de_analysis result object with logFC values
- Two-group or multi-group differential expression table with log fold-change computed
- Predefined lipid set definitions (provided by lipidr)

## Outputs

- significant_lipidsets table filtered by significance threshold
- Enrichment scores and adjusted p-values for each lipid set
- Visualizations (e.g., plots and tables) of enriched/depleted lipid classes and chain properties

## How to apply

Load the differential expression result object containing logFC values (e.g., from benign vs. cancer or cancer vs. metastasis comparisons). Call the lsea() function with rank.by='logFC' parameter to rank all measured lipid molecules by their log fold-change values and compute enrichment statistics against predefined lipid sets (organized by lipid class, chain length, and unsaturation). Extract the significant_lipidsets table from lsea output and filter for lipid sets meeting your significance threshold (typically adjusted p-value < 0.05). Visualize and tabulate the results to show enrichment scores, adjusted p-values, and the direction of enrichment for each significant lipid set.

## Related tools

- **lipidr** (R package providing lsea() function, differential expression analysis (de_analysis), and visualization of enrichment results) — https://github.com/ahmohamed/lipidr
- **limma** (Underlying R package required for statistical computation of differential expression and logFC values)
- **R** (Programming language and runtime for executing lipidr and enrichment analysis workflow)

## Examples

```
lsea_result <- lsea(two_group, rank.by='logFC'); significant_sets <- lsea_result$significant_lipidsets; plot_enrichment(lsea_result)
```

## Evaluation signals

- Significant lipid sets table is non-empty and contains expected lipid classes (PC, PG, CL, TG, etc.)
- Adjusted p-values of significant lipid sets are below the chosen threshold (e.g., padj < 0.05)
- Enrichment direction (up-regulated vs. down-regulated) is biologically concordant with the comparison (e.g., PCs and PGs up-regulated in cancer vs. benign)
- Visualization shows clear separation or clustering of enriched lipid sets with interpretable scores and p-values
- Results are reproducible when re-running lsea() with the same rank.by='logFC' parameter and threshold

## Limitations

- LSEA requires predefined lipid set annotations; results are limited to lipid classes, chain lengths, and unsaturation patterns encoded in the reference sets
- Ranking by logFC alone does not account for effect size variability or confidence intervals; integration with p-values or adjusted effect sizes may provide additional context
- Small sample sizes may lead to unstable logFC estimates and reduced statistical power for enrichment detection
- The method assumes independence between lipid molecules within sets, which may not hold for co-regulated pathways or structural isomers

## Evidence

- [other] Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid classes and chain unsaturations.: "Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid"
- [other] Call lsea() function with rank.by='logFC' parameter to rank lipid molecules by log fold-change and compute enrichment statistics for predefined lipid sets.: "Call lsea() function with rank.by='logFC' parameter to rank lipid molecules by log fold-change and compute enrichment statistics for predefined lipid sets."
- [other] Extract the significant_lipidsets table from lsea output, filtering for lipid classes and chain-length features meeting the significance threshold.: "Extract the significant_lipidsets table from lsea output, filtering for lipid classes and chain-length features meeting the significance threshold."
- [readme] A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns.: "A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns."
- [intro] PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues compared to benign samples: "PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues compared to benign samples"
