---
name: correlation-network-construction-omics
description: Use when when you have a feature abundance table (rows=features, columns=samples)
  with >10,000 features from microbiome, metabolomics, transcriptomics, or multi-omics
  data and need to identify correlated or co-occurring features for network-based
  analysis, module detection, or cross-omics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3050
  tools:
  - MetaNet
  - R
  - igraph
  - pcutils
  license_tier: restricted
derived_from:
- doi: 10.1101/2025.06.26.661636v1
  title: MetaNet
evidence_spans:
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers.
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers
- MetaNet, a high-performance R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanet_cq
    doi: 10.1101/2025.06.26.661636v1
    title: MetaNet
  dedup_kept_from: coll_metanet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.06.26.661636v1
  all_source_dois:
  - 10.1101/2025.06.26.661636v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# correlation-network-construction-omics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct correlation-based networks from high-dimensional omics feature abundance tables (>10,000 features) by computing pairwise correlations, applying statistical thresholding, and building graph objects with nodes representing features and weighted edges representing correlation strengths. This skill enables fast, scalable network construction and is essential when integrating multiple omics layers or identifying co-occurrence and co-abundance patterns.

## When to use

When you have a feature abundance table (rows=features, columns=samples) with >10,000 features from microbiome, metabolomics, transcriptomics, or multi-omics data and need to identify correlated or co-occurring features for network-based analysis, module detection, or cross-omics integration. Specifically apply this skill when correlation structure—rather than raw abundance—is the primary analysis goal.

## When NOT to use

- Input is already a pre-computed correlation or adjacency matrix (use c_net_build() directly instead)
- Feature count is <100 and computational efficiency is not a concern (standard R cor() may suffice)
- The goal is to identify differential features between groups rather than correlation structure (use differential abundance testing instead)

## Inputs

- Feature abundance table (matrix or data.frame: rows=features, columns=samples)
- Transposed feature table (rows=samples, columns=features; preferred for correlation calculation)
- Correlation threshold parameter (numeric; e.g., 0.65)
- Optional: p-value adjustment method (string; e.g., 'BH')
- Optional: correlation method (string; 'pearson' or 'spearman')

## Outputs

- igraph network object with features as vertices
- Correlation matrix (pairwise Pearson/Spearman coefficients)
- P-value matrix (statistical significance of correlations)
- Network summary statistics (node count, edge count, correlation ranges)

## How to apply

Load the feature abundance table into R and transpose it if needed (samples as rows, features as columns). Use MetaNet's c_net_calculate() function to compute pairwise Pearson/Spearman correlations and p-values across all features using optimized vectorized matrix algorithms, which scale efficiently to >10,000 features. Apply correlation thresholding (e.g., r_threshold=0.65) to retain only significant edges, optionally after p-value adjustment. Construct an igraph network object via c_net_build() with features as nodes and correlation coefficients as weighted edges. Validate the resulting network by checking node and edge counts, verifying correlation value ranges, and confirming igraph object integrity (e.g., no orphaned nodes if threshold is strict).

## Related tools

- **MetaNet** (Primary R package providing optimized correlation calculation (c_net_calculate), network construction (c_net_build), and igraph integration for high-dimensional omics data) — https://github.com/Asa12138/MetaNet
- **igraph** (Underlying graph library used by MetaNet for network object representation, manipulation, and topology analysis)
- **pcutils** (Companion utility package providing helper functions (e.g., t2() for transposition) and demo datasets for MetaNet workflows) — https://github.com/Asa12138/pcutils
- **R** (Execution environment for correlation computation and network construction)

## Examples

```
library(MetaNet); library(pcutils); data('otutab', package='pcutils'); totu <- t2(otutab[1:70, ]); cor <- c_net_calculate(totu); net <- c_net_build(cor, r_threshold=0.65); c_net_plot(net)
```

## Evaluation signals

- Node count equals the number of features retained after filtering (no spurious or orphaned nodes)
- Edge count is non-zero and reflects the proportion of feature pairs exceeding the correlation threshold
- Correlation edge weights fall within the expected range (typically |r| ≥ threshold; e.g., ≥0.65 or ≤−0.65)
- igraph object passes integrity checks: is_connected(), is_simple(), all vertex and edge attributes are present
- Network density and degree distribution are consistent with biological expectations (e.g., not a complete graph, not a star graph unless specific biological mechanism warrants it)

## Limitations

- Correlation-based networks do not imply causality; a strong correlation between two features may reflect indirect association through a third feature or confounding
- High-dimensional datasets with >10,000 features may produce very dense networks even at stringent thresholds, requiring additional filtering (e.g., by degree or module membership) for interpretability
- Correlation thresholds are user-defined and lack a universal standard; the choice significantly impacts network topology and downstream conclusions
- Pearson correlation assumes linear relationships and may miss nonlinear co-occurrence patterns; Spearman correlation is more robust but computationally more expensive
- Missing data, zero-inflation, and compositional biases (common in microbiome data) can distort correlation estimates; preprocessing (e.g., normalization, pseudocount addition) may be necessary before network construction

## Evidence

- [other] MetaNet implements a correlation-based network construction module that operates on datasets with more than 10,000 features, enabling fast and scalable network building from feature abundance tables.: "MetaNet implements a correlation-based network construction module that operates on datasets with more than 10,000 features, enabling fast and scalable network building from feature abundance tables."
- [intro] MetaNet enables fast and scalable correlation-based network construction for datasets with more than 10,000 features: "MetaNet enables fast and scalable correlation-based network construction for datasets with more than 10,000 features"
- [readme] Pairwise correlation computation is central to most network-based omics tools, but the growing scale of omics datasets imposes substantial computational demands. MetaNet addresses this through optimized vectorized matrix algorithms for calculating correlation coefficients and corresponding p-values, greatly reducing memory use and runtime.: "MetaNet addresses this through optimized vectorized matrix algorithms for calculating correlation coefficients and corresponding p-values, greatly reducing memory use and runtime"
- [other] Compute pairwise correlations between all features using MetaNet's correlation engine, which is optimized for datasets exceeding 10,000 features.: "Compute pairwise correlations between all features using MetaNet's correlation engine, which is optimized for datasets exceeding 10,000 features."
- [other] Apply correlation thresholding to retain only significant edges (specific threshold determined by user or statistical criteria).: "Apply correlation thresholding to retain only significant edges (specific threshold determined by user or statistical criteria)."
- [other] Construct an igraph network object from the thresholded correlation matrix, with features as nodes and correlations as weighted edges.: "Construct an igraph network object from the thresholded correlation matrix, with features as nodes and correlations as weighted edges."
- [readme] Benchmarking shows that MetaNet delivers up to a 100-fold improvement in computation time and a 50-fold reduction in memory usage compared to existing R packages.: "Benchmarking shows that MetaNet delivers up to a 100-fold improvement in computation time and a 50-fold reduction in memory usage compared to existing R packages."
