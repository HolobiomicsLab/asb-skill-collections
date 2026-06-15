---
name: benchmark-table-parsing-and-aggregation
description: Use when you are reproducing a comparative benchmarking claim (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0080
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

# benchmark-table-parsing-and-aggregation

## Summary

Extract method-by-dataset performance matrices from peer-reviewed benchmarking studies, compute summary statistics (mean, median, rank), and compile results into a standardized TSV format to enable quantitative comparison of competing computational methods. This skill is essential when reproducing or validating claims that one method outperforms another across multiple datasets or evaluation metrics.

## When to use

You are reproducing a comparative benchmarking claim (e.g., 'Method A outperforms Method B') from a published study and need to verify the finding by assembling the raw accuracy metrics (NMI, ARI, purity scores, clustering accuracy) reported in the paper's tables or supplementary data, especially when the claim rests on aggregated performance across multiple datasets.

## When NOT to use

- The benchmark study reports only qualitative rankings (e.g., 'Method A is better') without numeric accuracy metrics — aggregation requires numeric data.
- The target study is a review or opinion piece, not a direct empirical comparison with raw metric tables.
- You are comparing methods from different papers using different datasets — inter-paper aggregation introduces confounding factors (dataset-specific difficulty, metric definitions) and should be avoided without explicit cross-study normalization.

## Inputs

- Peer-reviewed benchmarking paper (preprint or published) with comparative method results
- Supplementary data tables, figures, or SI appendices containing raw or summary accuracy metrics
- Method name list (e.g., chromVAR variants, SnapATAC, baseline methods)
- Dataset identifier list or accession numbers used in the benchmark

## Outputs

- Method-by-dataset matrix (TSV) with methods as rows, datasets as columns, metric values as cells
- Summary statistics table (TSV) with rows as methods and columns as mean, median, std dev, rank of performance
- Ranked method list (TSV or CSV) ordered by aggregated performance metric

## How to apply

Locate the benchmark results table or supplementary data in the target paper (e.g., bioRxiv preprint 739011). Extract clustering accuracy metrics (NMI, ARI, purity, or other domain-specific scores) for each method variant and each dataset reported. Arrange these into a method-by-dataset matrix with rows indexed by method name and variants (e.g., 'chromVAR kmers+PCA', 'SnapATAC'), columns indexed by dataset identifier, and cells containing the raw metric values. Compute summary statistics (mean, median, standard deviation) across the dataset dimension for each method to quantify relative performance. Identify the best-performing variant within each method family (e.g., kmers+PCA as the superior chromVAR configuration) and rank all methods by summary metric. Export the method-by-dataset matrix and summary statistics table as TSV files for downstream comparison and visualization.

## Related tools

- **SnapATAC** (Benchmarked method for single-cell ATAC-seq clustering; primary comparison target) — https://github.com/r3fang/SnapATAC
- **chromVAR** (Baseline method with multiple variants (kmers+PCA, motif-based); variant selection is critical to fair comparison) — https://github.com/GreenleafLab/chromVAR
- **R** (Language and environment for reading, parsing, aggregating numeric tables and computing summary statistics)

## Examples

```
# R snippet to parse benchmark table and compute summary statistics
data <- read.csv('chen_et_al_clustering_metrics.csv', row.names=1)
summary_stats <- data.frame(mean=rowMeans(data), median=apply(data,1,median), rank=rank(-rowMeans(data)))
write.table(data, 'method_by_dataset_matrix.tsv', sep='\t')
write.table(summary_stats, 'summary_statistics.tsv', sep='\t')
```

## Evaluation signals

- Method-by-dataset matrix is rectangular and complete (no missing values for reported method–dataset pairs); row and column totals are consistent with the source paper.
- Summary statistics (mean, median) are computed correctly: mean = sum of column values / number of datasets; median is the middle value when sorted.
- Best-performing variant within each method family is correctly identified (e.g., kmers+PCA ranked above other chromVAR configurations in clustering tasks).
- Relative performance claim from paper is validated: numeric comparison (e.g., mean NMI of SnapATAC > mean NMI of chromVAR) supports the stated finding.
- TSV format is valid: tab-separated, no embedded tabs or inconsistent delimiters; row/column headers are present and match method/dataset names from source.

## Limitations

- Metric definitions (NMI, ARI, purity) may differ subtly across papers or implementations; cross-study aggregation requires explicit normalization or is invalid.
- Supplementary data may be incomplete, missing for newer method variants, or reported only in figures (requiring manual extraction or optical character recognition).
- Method variants (e.g., kmers vs. motif-based chromVAR) may use different hyperparameter settings across datasets; aggregation assumes fair and consistent tuning.
- Datasets may vary in size, cell-type complexity, or sequencing depth; summary statistics across heterogeneous datasets may not reflect performance on a new dataset of interest.

## Evidence

- [other] Extract clustering accuracy metrics (e.g., NMI, ARI, or purity scores) for chromVAR kmers+PCA and SnapATAC variants across all reported datasets.: "Extract clustering accuracy metrics (e.g., NMI, ARI, or purity scores) for chromVAR kmers+PCA and SnapATAC variants across all reported datasets."
- [other] Compile method-by-dataset matrix into a TSV table with rows as methods, columns as datasets, and cells as accuracy scores.: "Compile method-by-dataset matrix into a TSV table with rows as methods, columns as datasets, and cells as accuracy scores."
- [other] Calculate summary statistics (mean, median, rank) for each method across datasets to quantify the finding.: "Calculate summary statistics (mean, median, rank) for each method across datasets to quantify the finding that SnapATAC outperforms chromVAR overall while chromVAR kmers+PCA is superior to other"
- [readme] Using kmers + PCA appears to be the best variant of chromVAR for clustering: "Using kmers + PCA appears to be the best variant of chromVAR for clustering"
- [readme] newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper: "newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper"
