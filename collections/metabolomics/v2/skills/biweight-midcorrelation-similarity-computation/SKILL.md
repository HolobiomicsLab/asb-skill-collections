---
name: biweight-midcorrelation-similarity-computation
description: Use when you have normalized and imputed metabolite abundance measurements (as a MultiAssayExperiment object or similar matrix) and need to construct a correlation network for co-expression module discovery. Use it specifically when outlier-robust similarity is required—i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3407
  tools:
  - MetaboDiff
  - WGCNA
  - R
  - MultiAssayExperiment
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder and Horvarth
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biweight-midcorrelation-similarity-computation

## Summary

Compute a robust similarity matrix across metabolites using biweight midcorrelation, which downweights outliers and is more stable than Pearson correlation for hierarchical clustering and module detection in metabolomic data.

## When to use

Apply this skill when you have normalized and imputed metabolite abundance measurements (as a MultiAssayExperiment object or similar matrix) and need to construct a correlation network for co-expression module discovery. Use it specifically when outlier-robust similarity is required—i.e., when your metabolite abundance data contain influential extreme values that would distort Pearson or Spearman correlations.

## When NOT to use

- Input metabolite data has not been normalized and imputed; missing values or non-normalized distributions will bias correlation estimates and clustering performance.
- Your goal is differential abundance testing (not network module discovery); use univariate statistical tests instead.
- Metabolite count is very small (< ~20–30 features); biweight midcorrelation requires sufficient sample size to estimate robust pairwise associations reliably.

## Inputs

- normalized and imputed metabolite abundance matrix (MultiAssayExperiment object or data frame with metabolite rows and sample columns)
- metabolite IDs or feature names (rownames of the matrix)

## Outputs

- biweight midcorrelation similarity matrix (metabolite × metabolite)
- adjacency matrix (after soft thresholding conversion)
- dissimilarity matrix (1 − adjacency)
- metabolic module assignments (mapping of metabolite IDs to module colors/names)

## How to apply

Starting from a normalized metabolite abundance matrix, compute pairwise biweight midcorrelation coefficients across all metabolites. Biweight midcorrelation is preferred over absolute Pearson correlation because it assigns lower weight to observations far from the median, making it robust to outliers. The resulting similarity matrix is then converted to an adjacency matrix via soft thresholding (e.g., with power β=3) to emphasize strong relationships, then inverted to a dissimilarity matrix (1 − adjacency) suitable for hierarchical clustering. This dissimilarity-based dendrogram is then subjected to dynamic branch cutting (rather than fixed-height cutoffs) to identify metabolic modules, filtered by a minimum module size threshold (e.g., 5 metabolites) to exclude spurious small clusters.

## Related tools

- **MetaboDiff** (R package providing the complete pipeline for metabolite correlation computation and module detection; integrates biweight midcorrelation calculation with soft thresholding and dynamic branch cutting) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Provides core hierarchical clustering and dynamic branch cutting algorithms adapted for correlation networks; used by MetaboDiff for dendrogram construction and module identification)
- **MultiAssayExperiment** (R data container merging assay matrices (normalized metabolite abundance), feature metadata (rowData), and sample metadata (colData) for downstream correlation and module analysis)

## Examples

```
met <- normalize_met(met); # (after normalization and imputation) library(WGCNA); bicor_matrix <- cor(t(assay(met)), use='p', method='bicor'); adj_matrix <- (bicor_matrix^3); dissim_matrix <- 1 - adj_matrix; tree <- hclust(as.dist(dissim_matrix)); modules <- cutreeDynamic(dendro=tree, minClusterSize=5)
```

## Evaluation signals

- Similarity matrix is square, symmetric, and bounded in [−1, 1] (or [0, 1] if absolute biweight midcorrelation is used); diagonal should be 1.0.
- Adjacency matrix (after soft thresholding) contains values in [0, 1] with meaningful structure—i.e., strong similarity pairs map to adjacency near 1, weak similarity pairs to near 0.
- Dissimilarity matrix is strictly positive (all values > 0) with small dissimilarities between correlated metabolites and large dissimilarities between uncorrelated ones.
- Hierarchical dendrogram produced from dissimilarity matrix is well-balanced (not degenerate) and dynamic branch cutting yields multiple modules with sizes exceeding the minimum threshold (e.g., min_module_size ≥ 5).
- Module assignments include metabolite-to-color/module-name mappings; unassigned metabolites ('gray' module) are absent or minimal, indicating robust clustering.

## Limitations

- Biweight midcorrelation assumes sufficient sample size; with very small sample counts (n << p, where p is metabolite count), correlation estimates become unstable.
- Soft thresholding parameter β (e.g., β=3) is a hyperparameter; suboptimal choices can produce oversized or fragmented modules. No automatic tuning rule is provided; practitioners must experiment or use domain knowledge.
- Minimum module size threshold (e.g., 5 metabolites) is arbitrary and may exclude true biological modules if they are sparse or tissue-specific; conversely, too-low thresholds admit spurious clusters.
- Biweight midcorrelation is designed to handle outliers in individual samples but does not address systematic batch effects or missing data patterns; prior normalization and imputation quality directly affect downstream inference.
- Dynamic branch cutting may fail or produce uninformative partitions if the dendrogram is poorly structured (e.g., if all metabolites are weakly correlated); manual tuning of cutoff parameters may be necessary.

## Evidence

- [methods] Biweight midcorrelation as correlation measure: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient"
- [methods] Soft thresholding with power parameter: "Apply soft thresholding with power β=3 to convert similarity to adjacency, then compute dissimilarity as 1 − adjacency"
- [methods] Dynamic branch cutting for module identification: "We employed the dynamic branch cut method developed by Langfelder and colleagues, as constant height cutoffs exhibit suboptimal performance on complicated dendrograms"
- [methods] Minimum module size filtering: "modules are detected by applying a branch cutting method with a minimal module size of 5 metabolites"
- [readme] Purpose and rationale in package README: "MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network"
