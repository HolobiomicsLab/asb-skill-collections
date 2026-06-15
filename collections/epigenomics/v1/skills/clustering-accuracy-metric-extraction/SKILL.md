---
name: clustering-accuracy-metric-extraction
description: Use when when you need to reproduce or validate benchmark comparisons between clustering methods on single-cell chromatin accessibility data, particularly when the source publication reports multiple accuracy metrics across heterogeneous datasets and you must decide which method variant (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3673
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

# clustering-accuracy-metric-extraction

## Summary

Extract and tabulate clustering performance metrics (NMI, ARI, purity) from benchmark studies comparing single-cell ATAC-seq methods. This skill enables quantitative comparison of clustering quality across methods and datasets by compiling method-by-dataset matrices of standardized accuracy scores.

## When to use

When you need to reproduce or validate benchmark comparisons between clustering methods on single-cell chromatin accessibility data, particularly when the source publication reports multiple accuracy metrics across heterogeneous datasets and you must decide which method variant (e.g., kmers+PCA vs. full-feature approaches) produces superior clustering.

## When NOT to use

- If clustering metrics are not explicitly reported in the source study or supplementary materials—no extraction is possible without access to raw accuracy values.
- If the benchmark study lacks multiple independent datasets; single-dataset comparisons cannot be generalized using this skill's aggregation and ranking approach.
- If the study uses non-standard or undocumented clustering metrics that cannot be directly compared across methods without recalculation from raw cluster assignments.

## Inputs

- Published benchmark results table or supplementary data file with method names, dataset identifiers, and accuracy metrics
- Method variant names and configurations (e.g., 'chromVAR kmers+PCA', 'SnapATAC with Leiden clustering')
- Clustering evaluation metrics (NMI, ARI, purity) as reported in the benchmark study

## Outputs

- Method-by-dataset TSV matrix with rows as methods and columns as datasets, cells populated with accuracy scores
- Summary statistics table: mean, median, and per-method rank for each clustering accuracy metric across datasets
- Comparative finding document summarizing which method variant (e.g., kmers+PCA) is best within a framework and how it ranks against competing methods (e.g., SnapATAC)

## How to apply

Locate the benchmark results table or supplementary data from the source publication (e.g., bioRxiv preprint 739011 for Chen et al.). Extract clustering accuracy metrics—NMI (normalized mutual information), ARI (adjusted Rand index), or purity scores—for each method variant across all reported datasets. Organize the metrics into a TSV table with rows as methods (e.g., chromVAR kmers+PCA, SnapATAC), columns as datasets, and cells as accuracy values. Calculate summary statistics (mean, median, per-method rank across datasets) to quantify relative performance and identify which method or variant achieves superior clustering fidelity. Document the metric definitions and any preprocessing or postprocessing steps (e.g., whether PCA was applied to the feature set before clustering) to ensure fair comparison.

## Related tools

- **chromVAR** (Source method for clustering performance extraction; kmers+PCA variant is identified as best chromVAR configuration for clustering tasks) — https://github.com/GreenleafLab/chromVAR
- **SnapATAC** (Competing method in benchmark comparison; demonstrates superior clustering performance relative to chromVAR variants) — https://github.com/r3fang/SnapATAC
- **R** (Environment for parsing benchmark tables, calculating summary statistics, and generating method-by-dataset comparison matrices)

## Examples

```
# R workflow: extract clustering metrics from Chen et al. benchmark
library(readr); library(dplyr)
bench_table <- read_tsv('chen_et_al_739011_benchmark_table.tsv')
method_dataset_matrix <- bench_table %>% pivot_wider(names_from=dataset, values_from=accuracy_metric)
summary_stats <- method_dataset_matrix %>% rowwise() %>% mutate(mean_acc = mean(c_across(where(is.numeric))), median_acc = median(c_across(where(is.numeric))))
write_tsv(method_dataset_matrix, 'chromvar_snapatac_accuracy_matrix.tsv')
write_tsv(summary_stats, 'method_summary_statistics.tsv')
```

## Evaluation signals

- TSV matrix schema validation: rows are method names, columns are dataset identifiers, all cells contain numeric accuracy scores in valid range [0, 1] for normalized metrics or [-1, 1] for ARI
- No missing data in the method-by-dataset matrix for methods and datasets reported in the source publication; any missing entries are explicitly documented with rationale
- Summary statistics (mean, median) for each method are mathematically consistent with cell values; per-method rank correctly orders methods by aggregated accuracy
- Extracted finding matches the published conclusion (e.g., 'kmers+PCA is the best chromVAR variant for clustering' and 'SnapATAC outperforms chromVAR overall') when summary statistics are inspected
- All accuracy metric definitions (NMI, ARI, purity) and their ranges are documented alongside the table to enable downstream interpretation and comparison with other studies

## Limitations

- Extraction accuracy depends on clarity and accessibility of the source benchmark table; if metrics are embedded in figure captions or narratively described without tabular data, manual interpretation introduces potential transcription errors.
- The skill assumes metrics are directly comparable across datasets; if datasets vary substantially in scale, sparsity, or cluster number, raw metric values may not be equally meaningful—normalization or dataset stratification may be needed.
- Summary statistics (e.g., mean accuracy) can obscure dataset-specific patterns where one method dominates on small datasets and another on large ones; per-dataset breakdown should be retained and inspected.
- This skill does not address statistical significance testing or confidence intervals; benchmark studies may not report uncertainty, limiting ability to determine whether differences between methods are meaningful.

## Evidence

- [other] Extract clustering accuracy metrics (e.g., NMI, ARI, or purity scores) for chromVAR kmers+PCA and SnapATAC variants across all reported datasets.: "Extract clustering accuracy metrics (e.g., NMI, ARI, or purity scores) for chromVAR kmers+PCA and SnapATAC variants across all reported datasets."
- [other] Compile method-by-dataset matrix into a TSV table with rows as methods, columns as datasets, and cells as accuracy scores.: "Compile method-by-dataset matrix into a TSV table with rows as methods, columns as datasets, and cells as accuracy scores."
- [other] Calculate summary statistics (mean, median, rank) for each method across datasets to quantify the finding that SnapATAC outperforms chromVAR overall while chromVAR kmers+PCA is superior to other chromVAR configurations.: "Calculate summary statistics (mean, median, rank) for each method across datasets to quantify the finding that SnapATAC outperforms chromVAR overall while chromVAR kmers+PCA is superior to other"
- [readme] Using kmers + PCA appears to be the best variant of chromVAR for clustering, but newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper.: "Using kmers + PCA appears to be the best variant of chromVAR for clustering, but newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper."
- [readme] For a paper evaluating chromVAR and other methods as a method for enabling clustering of single cells, see the preprint from Huidong Chen et al.: "For a paper evaluating chromVAR and other methods as a method for enabling clustering of single cells, see the preprint from Huidong Chen et al."
