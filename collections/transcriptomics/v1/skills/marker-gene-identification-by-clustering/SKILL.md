---
name: marker-gene-identification-by-clustering
description: Use when you have a processed single-cell expression matrix (AnnData object) with pre-computed cluster assignments (e.g., leiden or louvain clusters in adata.obs) and want to discover which genes define each cluster's transcriptional identity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0080
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

# Marker gene identification by clustering

## Summary

Identify cluster-specific marker genes by applying statistical differential expression testing (e.g., Wilcoxon rank-sum test) across leiden-clustered single-cell RNA-seq data in Scanpy. This skill surfaces the most differentially expressed genes per cluster, ranked by effect size and p-value, to characterize cell type identity.

## When to use

Apply this skill when you have a processed single-cell expression matrix (AnnData object) with pre-computed cluster assignments (e.g., leiden or louvain clusters in adata.obs) and want to discover which genes define each cluster's transcriptional identity. Use it after clustering and before manual cell-type annotation to guide interpretation of cluster biology.

## When NOT to use

- Input clusters are not biologically meaningful or are artifacts of preprocessing (e.g., batch effects). Validate clustering quality before running differential expression.
- Sample size is very small (n < 3 cells per cluster); statistical power is insufficient for Wilcoxon test.
- Data are raw (non-normalized) counts; normalize and log-transform first to avoid violating Wilcoxon test assumptions.

## Inputs

- AnnData object with normalized gene expression matrix (genes × cells)
- Cluster assignments in adata.obs (e.g., 'leiden' or 'louvain' column)
- Processed, log-normalized count matrix (raw counts not recommended)

## Outputs

- Ranked genes per cluster (DataFrame with columns: gene name, log-fold-change, p-value, adjusted p-value)
- Top N marker genes per cluster (e.g., top 5–10)
- Summary table of marker genes with their differential expression statistics

## How to apply

Load the processed AnnData object (e.g., pbmc3k_processed) and verify cluster assignments are present in adata.obs. Call sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon') to compute differential expression statistics (log-fold-change, p-values, adjusted p-values) for each gene across clusters using the Wilcoxon rank-sum test. Extract ranked results using sc.get.rank_genes_groups_df(adata) or access the raw table in adata.uns['rank_genes_groups']. Filter results by p-value threshold (e.g., p < 0.05) and effect size to identify top marker genes per cluster. Validate that top-ranked genes per cluster match expected biological marker names and that scores fall within expected ranges (e.g., log-fold-change ≥ 0.25, p-values < 0.01 for strong markers).

## Related tools

- **Scanpy** (Perform differential expression testing via rank_genes_groups with Wilcoxon method and extract ranked marker gene tables) — https://github.com/scverse/scanpy
- **anndata** (Store and access cluster assignments and differential expression results in adata.obs and adata.uns) — https://github.com/scverse/anndata
- **Python** (Primary language for Scanpy workflow and result manipulation)

## Examples

```
import scanpy as sc; adata = sc.datasets.pbmc3k_processed(); sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon'); markers = sc.get.rank_genes_groups_df(adata); print(markers.head(10))
```

## Evaluation signals

- Top-ranked genes per cluster align with known biological markers for expected cell types (e.g., CD14, LYZ for monocytes in PBMC data)
- Log-fold-change values are positive and fall within biologically plausible ranges (typically 0.25–4.0 for marker genes)
- Adjusted p-values for top markers are < 0.05 or < 0.01, indicating statistical significance after multiple-testing correction
- No single gene appears as a top marker in all clusters; markers should be cluster-specific
- Summary table can be visualized with heatmaps or dotplots to confirm cluster-gene specificity

## Limitations

- Wilcoxon test assumes independent samples; pseudo-replication (multiple cells from same sample) violates assumptions and may inflate significance.
- Method does not account for continuous or compositional confounders; batch effects or subject-level variables can bias results.
- Results are sensitive to cluster resolution; over-clustering produces many small, low-power clusters; under-clustering obscures heterogeneity.
- Statistical testing does not establish functional importance; markers must be validated experimentally or cross-referenced with literature.

## Evidence

- [other] Wilcoxon test produces marker gene rankings matching expected documentation examples: "Run sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon') to compute differential gene expression ranks across leiden clusters"
- [other] Differential expression is a core capability of Scanpy: "Scanpy includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] Extraction and validation of ranked results: "Extract the result DataFrame using sc.get.rank_genes_groups_df(adata) or access adata.uns['rank_genes_groups']. Validate that the top-ranked genes per cluster match the documented marker gene names"
- [other] AnnData object structure for storing results: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
