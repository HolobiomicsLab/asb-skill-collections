---
name: statistical-ranking-wilcoxon-test
description: Use when when you have leiden or louvain cluster assignments in single-cell data (stored in adata.obs) and need to identify cluster-specific marker genes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - Python
  - Scanpy
  - anndata
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- Single-Cell Analysis in Python
- type annotations on function parameters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# statistical-ranking-wilcoxon-test

## Summary

Apply the Wilcoxon rank-sum test to rank genes by differential expression across cell clusters in single-cell RNA-seq data. This non-parametric statistical test identifies marker genes for each cluster by computing log-fold-change and p-value scores, enabling robust cluster characterization without assuming expression normality.

## When to use

When you have leiden or louvain cluster assignments in single-cell data (stored in adata.obs) and need to identify cluster-specific marker genes. Use this skill when comparing gene expression distributions between a focal cluster and all other cells, particularly when expression values may violate normality assumptions or when you need reproducible, documented statistical rankings that match published benchmarks.

## When NOT to use

- Cluster assignments are missing or unreliable — ensure clustering is complete and validated before ranking.
- Input is bulk RNA-seq or non-clustered data — Wilcoxon ranking requires meaningful group structure.
- Expression values are not on a compatible scale (e.g., raw counts without normalization) — Scanpy typically expects log-normalized or scaled input.

## Inputs

- AnnData object (adata) with raw or normalized gene expression matrix
- Cluster assignments in adata.obs (e.g., 'leiden' or 'louvain' column)
- Gene expression matrix (cells × genes), typically log-transformed counts or normalized values

## Outputs

- Ranked gene list per cluster with log-fold-change scores
- Adjusted p-values (stored in adata.uns['rank_genes_groups'])
- Summary DataFrame of top marker genes per cluster (via sc.get.rank_genes_groups_df)

## How to apply

Load your clustered AnnData object and call sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon') to compute Wilcoxon test statistics across all clusters. The function tests each gene in each cluster against all other cells, computing log-fold-change and adjusted p-values. Extract results via sc.get.rank_genes_groups_df(adata) or from adata.uns['rank_genes_groups']. Validate by comparing the top 5–10 ranked genes per cluster against known marker genes documented in your experimental context, checking that log-fold-change and p-value scores fall within expected ranges (e.g., |log2FC| > 0.25, p_adj < 0.05). Wilcoxon's non-parametric nature makes it robust to outliers and non-normal distributions common in sparse single-cell data.

## Related tools

- **Scanpy** (Primary tool for differential expression ranking via sc.tl.rank_genes_groups with Wilcoxon method and result extraction via sc.get.rank_genes_groups_df) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) that stores clustered single-cell data, cluster assignments, and ranking results) — https://github.com/scverse/anndata
- **Python** (Programming language for executing Scanpy workflows and result validation)

## Examples

```
import scanpy as sc
adata = sc.datasets.pbmc3k_processed()
sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon')
results_df = sc.get.rank_genes_groups_df(adata)
print(results_df.head(10))
```

## Evaluation signals

- Top-ranked genes per cluster match documented marker gene names for that cell type in published single-cell references or experimental validation studies.
- Log-fold-change values are in expected range (typically |log2FC| ≥ 0.25 for marker genes) and p-values are below significance threshold (p_adj < 0.05).
- Gene ranking order is stable across replicate runs and consistent with cluster identity (e.g., immune markers in immune clusters, neuronal markers in neuronal clusters).
- Summary table of top 5 marker genes per cluster shows no duplicate or ubiquitous genes, confirming cluster-specific differential expression.
- Result structure matches adata.uns['rank_genes_groups'] schema with 'names', 'logfoldchanges', and 'pvals_adj' keys for each group.

## Limitations

- Wilcoxon test assumes independent observations; if cells are highly correlated (e.g., from the same tissue sample), p-values may be overly optimistic.
- The method ranks genes within pairwise comparisons of one cluster vs. rest; it does not account for multi-cluster structure or overlapping marker signatures.
- Performance scales with cluster size and gene count; extremely large datasets may require subsampling or sparse matrix optimizations for computation time.
- Log-fold-change calculation depends on library size normalization; poor normalization upstream will distort fold-change estimates.
- Multiple testing correction (typically FDR) is applied but may still yield false positives in highly granular clustering schemes with many rare clusters.

## Evidence

- [other] Wilcoxon test method supported by Scanpy's rank_genes_groups function: "Run sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon') to compute differential gene expression ranks across leiden clusters."
- [intro] Differential expression testing as core Scanpy capability: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] Result extraction and validation approach: "Extract the result DataFrame using sc.get.rank_genes_groups_df(adata) or access adata.uns['rank_genes_groups']. Validate that the top-ranked genes per cluster match the documented marker gene names"
- [intro] Scanpy built on AnnData for single-cell analysis: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [other] Example workflow using pbmc3k dataset: "Verify that leiden cluster assignments are present in adata.obs. Run sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon') to compute differential gene expression ranks across leiden"
