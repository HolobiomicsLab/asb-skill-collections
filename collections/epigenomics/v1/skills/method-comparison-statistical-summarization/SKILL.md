---
name: method-comparison-statistical-summarization
description: Use when you have extracted clustering or classification accuracy metrics (NMI, ARI, purity scores) for two or more competing methods evaluated on multiple datasets, and need to determine which method performs overall rather than on individual datasets alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_0091
  tools:
  - SnapATAC
  - chromVAR
  - R
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- newer methods such as SnapATAC outperform chromVAR for the clustering tasks
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chromvar
    doi: 10.1038/nmeth.4401
    title: chromvar
  dedup_kept_from: coll_chromvar
schema_version: 0.2.0
---

# Method-comparison statistical summarization

## Summary

Compile accuracy metrics across multiple methods and datasets into a structured matrix, then compute summary statistics (mean, median, rank) to quantitatively rank method performance. This skill transforms scattered benchmark results into a standardized comparison table suitable for identifying superior approaches.

## When to use

You have extracted clustering or classification accuracy metrics (NMI, ARI, purity scores) for two or more competing methods evaluated on multiple datasets, and need to determine which method performs best overall rather than on individual datasets alone. This is especially useful when one method outperforms others on some datasets but not others, requiring aggregation to resolve the ranking.

## When NOT to use

- Input is a single dataset: summary statistics across datasets are meaningless; report per-dataset results only.
- Methods have not been evaluated on a common set of datasets: direct comparison is invalid; stratify by dataset subset.
- Metrics are on different scales (e.g., one method reports ARI, another reports NMI): standardize or report separately before aggregation.

## Inputs

- Clustering accuracy metrics table (from published benchmark or supplementary data)
- List of methods being compared (e.g., chromVAR variants, SnapATAC)
- List of datasets used in benchmarking
- Individual metric values per method-dataset pair (e.g., NMI, ARI, purity scores)

## Outputs

- Method-by-dataset TSV table (rows=methods, columns=datasets, cells=accuracy scores)
- Summary statistics table (method, mean accuracy, median accuracy, rank)
- Ranking of methods by overall performance (best to worst)

## How to apply

Extract accuracy scores for each method-dataset combination from published benchmark tables or supplementary data (e.g., NMI, ARI, or purity values). Organize these into a matrix with rows representing methods and columns representing datasets. For each method, calculate mean, median, and rank across all datasets. The rationale is that single-dataset comparisons can be dataset-specific; aggregating across multiple datasets using robust summary statistics (median is preferred over mean for outlier robustness) reveals which method generalizes best. Rank methods by their summary statistics to identify the overall winner while documenting which datasets favor which methods, revealing method-dataset interactions.

## Related tools

- **chromVAR** (One of the methods being compared; kmers+PCA variant is the focus for clustering benchmarking) — https://github.com/GreenleafLab/chromVAR
- **SnapATAC** (Competing method against chromVAR; outperforms chromVAR on clustering tasks in benchmark) — https://github.com/r3fang/SnapATAC
- **R** (Language and environment for computing summary statistics, generating matrices, and producing rankings)

## Examples

```
# R: Create method-by-dataset matrix and compute summary statistics
metrics_matrix <- matrix(c(0.78, 0.82, 0.71, 0.85, 0.76, 0.89), nrow=2, dimnames=list(c('chromVAR_kmers_PCA', 'SnapATAC'), c('dataset1', 'dataset2', 'dataset3'))); summary_stats <- data.frame(method=rownames(metrics_matrix), mean=rowMeans(metrics_matrix), median=apply(metrics_matrix, 1, median), rank=rank(-rowMeans(metrics_matrix))); write.table(summary_stats, 'method_comparison_summary.tsv', sep='\t', quote=FALSE, row.names=FALSE)
```

## Evaluation signals

- TSV table is well-formed: all methods appear as rows, all datasets appear as columns, all cells contain numeric accuracy scores with no missing data.
- Summary statistics are internally consistent: median value for each method falls within the range [min, max] of that method's dataset scores.
- Ranking is transitive: if method A has higher mean accuracy than method B, and method B higher than method C, then A > B > C in the rank column.
- Relative performance statement is quantified: e.g., 'SnapATAC mean ARI = 0.85 vs. chromVAR kmers+PCA mean ARI = 0.72' (not just 'SnapATAC is better').
- Dataset-by-dataset variance is documented: report which datasets favor which methods, indicating whether one method dominates all datasets or performance is dataset-dependent.

## Limitations

- Summary statistics (mean, median) obscure dataset-specific strengths; a method poor on one dataset but excellent on others may appear average. Always report per-dataset results alongside summary ranks.
- Equal weighting of all datasets assumes equal importance; if some datasets are larger or more clinically relevant, weighted averaging may be more appropriate.
- Metric choice (NMI vs. ARI vs. purity) affects rankings; different metrics may rank methods differently. Standardize on a single metric or report all three separately.
- No statistical significance testing: summary statistics alone do not account for variance or confidence intervals. Consider reporting confidence bounds if error estimates are available in the source benchmark.

## Evidence

- [other] Extract clustering accuracy metrics and compile into matrix: "Extract clustering accuracy metrics (e.g., NMI, ARI, or purity scores) for chromVAR kmers+PCA and SnapATAC variants across all reported datasets."
- [other] Organize method-by-dataset matrix with summary statistics: "Compile method-by-dataset matrix into a TSV table with rows as methods, columns as datasets, and cells as accuracy scores."
- [other] Calculate aggregate statistics to quantify overall performance: "Calculate summary statistics (mean, median, rank) for each method across datasets to quantify the finding that SnapATAC outperforms chromVAR overall while chromVAR kmers+PCA is superior to other"
- [intro] Identify best-performing variant within method family: "Using kmers + PCA appears to be the best variant of chromVAR for clustering, but newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper."
- [other] Source benchmark data from published preprint: "Access the bioRxiv preprint 739011 (Chen et al.) and locate the clustering benchmark results table or supplementary data."
