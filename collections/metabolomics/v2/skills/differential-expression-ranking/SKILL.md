---
name: differential-expression-ranking
description: Use when you have completed a two-group or multi-group differential expression analysis with computed logFC values (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
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
---

# differential-expression-ranking

## Summary

Rank lipid molecules by log fold-change from differential expression analysis to identify and visualize significantly enriched or depleted lipid classes and chain properties. This skill uses lipid set enrichment analysis (LSEA) to detect preferential regulation patterns across predefined lipid sets.

## When to use

You have completed a two-group or multi-group differential expression analysis with computed logFC values (e.g., benign vs. cancer, cancer vs. metastasis comparisons), and you want to discover which lipid classes, chain lengths, or unsaturation patterns are systematically enriched or depleted rather than examining individual lipid molecules in isolation.

## When NOT to use

- Your differential expression analysis has not yet been computed or lacks logFC values.
- You only have raw or normalized abundance data without fold-change or statistical significance estimates.
- Your research question focuses on individual lipid molecules rather than lipid class patterns or pathway-level regulation.

## Inputs

- LipidomicsExperiment object with completed two-group or multi-group differential expression analysis
- de_analysis result object containing logFC, p-values, and adjusted p-values per lipid molecule

## Outputs

- significant_lipidsets table with enrichment scores and adjusted p-values
- Ranked lipid set enrichment visualization plots
- Filtered lipid class and chain property enrichment results

## How to apply

Load the differential expression result object containing logFC values into the lsea() function with the rank.by='logFC' parameter to rank all measured lipids by their fold-change magnitude and direction. The function computes enrichment statistics for predefined lipid sets (grouped by lipid class, chain length, and unsaturation). Extract the significant_lipidsets table from the lsea output and filter for lipid sets meeting your significance threshold (typically adjusted p-value < 0.05). Visualize enriched sets with their enrichment scores and adjusted p-values to identify systematic lipid class shifts. This approach captures coordinated lipid regulation that single-molecule analysis might miss.

## Related tools

- **lipidr** (Performs lipid set enrichment analysis (lsea) with rank.by='logFC' parameter and extracts significant lipid sets for visualization) — https://github.com/ahmohamed/lipidr
- **limma** (Underlying statistical package required for differential expression analysis preceding the ranking step)

## Examples

```
lsea_result <- lsea(two_group, rank.by='logFC')
significant_sets <- lsea_result$significant_lipidsets
filtered_sets <- filter(significant_sets, adj.pval < 0.05)
```

## Evaluation signals

- significant_lipidsets table is non-empty and contains lipid sets with adjusted p-values below your chosen threshold (e.g., < 0.05)
- Enrichment scores are directional (positive for up-regulated, negative for down-regulated lipid sets) and consistent with the input logFC ranking direction
- Enriched lipid class patterns align with biological expectations (e.g., PCs and PGs up-regulated in cancer vs. benign, CLs and TGs down-regulated)
- Volcano plot or enrichment visualization shows clear separation of significant lipid sets from background with interpretable scores and p-values
- Filtering criteria (e.g., significance threshold) are documented and reproducible across independent analyses

## Limitations

- LSEA depends on predefined lipid sets; novel lipid class groupings or custom set definitions require manual curation outside lipidr's default sets.
- Ranking by logFC assumes fold-change magnitude is the primary biological signal; other ranking metrics (e.g., by p-value or effect size) may yield different results and are not explored here.
- Small sample sizes or low lipid coverage can reduce statistical power to detect enrichment, especially for rare lipid classes.
- Results are sensitive to upstream differential expression methodology (choice of test, normalization, batch correction); confounding variables not corrected at that stage propagate into enrichment rankings.

## Evidence

- [other] Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid classes and chain unsaturations.: "Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid"
- [readme] A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns.: "A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns."
- [other] Call lsea() function with rank.by='logFC' parameter to rank lipid molecules by log fold-change and compute enrichment statistics for predefined lipid sets.: "Call lsea() function with rank.by='logFC' parameter to rank lipid molecules by log fold-change and compute enrichment statistics for predefined lipid sets."
- [other] Extract the significant_lipidsets table from lsea output, filtering for lipid classes and chain-length features meeting the significance threshold.: "Extract the significant_lipidsets table from lsea output, filtering for lipid classes and chain-length features meeting the significance threshold."
- [intro] PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues compared to benign samples: "PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues compared to benign samples"
