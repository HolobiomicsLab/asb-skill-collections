---
name: monte-carlo-p-value-estimation-adaptive
description: Use when when you have ranked gene statistics and gene set collections, and your analysis requires P-value discrimination below a fixed lower bound (e.g., distinguishing between pathways at p < 1e-10).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3813
  tools:
  - fgsea
  - R
  - ggplot2
  - data.table
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
- library(ggplot2)
- ggplot(data=merge(...)) + geom_point(aes(x=logPvalFull, y=logPvalRed))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fgsea
    doi: 10.1101/060012
    title: fgsea
  dedup_kept_from: coll_fgsea
schema_version: 0.2.0
---

# Adaptive Multi-Level Split Monte-Carlo P-Value Estimation

## Summary

A method for computing arbitrarily low gene set enrichment analysis (GSEA) P-values using an adaptive multi-level split Monte-Carlo scheme, eliminating fixed lower-bound constraints by enabling precision refinement through iterative sampling. This skill is essential when gene set rankings must be compared at extreme statistical significance levels or when default P-value resolution (e.g., eps=1e-10) is insufficient for downstream filtering or interpretation.

## When to use

When you have ranked gene statistics and gene set collections, and your analysis requires P-value discrimination below a fixed lower bound (e.g., distinguishing between pathways at p < 1e-10). Particularly relevant when comparing many gene sets where the default eps=1e-10 threshold collapses multiple pathways to identical P-values, or when publication-grade precision is needed for pathway ranking.

## When NOT to use

- Input gene sets are very small (< 15 genes) or very large (> 500 genes) — these are filtered by minSize/maxSize and will not yield valid estimates regardless of eps setting.
- Computational resources are severely constrained — eps=0 requires iterative refinement and will be substantially slower than eps=1e-10; use default eps if runtime is critical.
- Gene ranking is unweighted or non-continuous — fgsea requires preranked, continuous statistics; if you have binary phenotype calls, compute Wilcoxon or t-test statistics first.

## Inputs

- ranked gene statistics (numeric vector with gene identifiers as names)
- gene set collection (list of character vectors containing gene identifiers)
- minSize and maxSize thresholds (integer, typically 15 and 500)

## Outputs

- fgsea results table with columns: pathway, pval, padj, log2err, ES, NES, size
- P-value precision estimates with associated log2err convergence metrics
- comparison table of default vs. adaptive estimates (differences, fold-changes)

## How to apply

Load ranked gene statistics (exampleRanks) and pathway definitions (examplePathways). Run fgsea() with eps=0.0 to disable the lower-bound estimate and activate the adaptive multi-level split Monte-Carlo refinement scheme. This parameter switch allows the algorithm to iteratively refine P-value estimates without a fixed minimum threshold. Compare results against a default run (eps=1e-10) by joining on pathway identifier and computing P-value fold-change ratios and difference distributions (log-scale). Validate by confirming pathway rankings remain consistent between runs, no numerical errors occur, and P-values decrease monotonically as precision increases. Record log2err values to assess convergence of the multi-level scheme.

## Related tools

- **fgsea** (Core implementation of adaptive multi-level split Monte-Carlo P-value estimation; provides fgsea() function with eps parameter control and output table generation.) — https://github.com/ctlab/fgsea
- **data.table** (Efficient joining and comparison of results from eps=1e-10 and eps=0 runs; grouping and aggregation of P-value differences.)
- **ggplot2** (Visualization of P-value distribution changes (log-scale) and identification of pathways with greatest precision improvement.)
- **R** (Runtime environment for fgsea, data.table, and ggplot2 integration.)

## Examples

```
fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, eps = 0.0, minSize = 15, maxSize = 500)
```

## Evaluation signals

- P-values computed with eps=0 are ≤ those with eps=1e-10 for the same pathways (monotonic precision gain).
- log2err values are numeric and finite (not NA or Inf) for eps=0 run, indicating convergence of the multi-level scheme.
- Pathway rankings (order by p-value) remain consistent or improve (no rank inversions) between eps=1e-10 and eps=0 runs.
- No numerical errors or warnings during fgsea execution with eps=0; function completes without NaN or undefined statistics in output table.
- Comparison table shows meaningful P-value differences for pathways originally tied at eps=1e-10 boundary; fold-change ratio distribution is unimodal and right-skewed (most pathways show modest refinement, a few show extreme improvement).

## Limitations

- Adaptive refinement is computationally expensive; eps=0 will significantly increase runtime compared to eps=1e-10, especially for large pathway collections or highly significant pathways.
- Extremely low P-values (< 1e-20) become numerically unstable and may be sensitive to random seed and number of Monte-Carlo iterations; reproducibility requires explicit seed control.
- The adaptive scheme assumes sufficiently many gene-set members to enable reliable split-level refinement; very small gene sets (near minSize) may show erratic log2err or unrepresentative P-value estimates.
- No changelog tracking for algorithm evolution; users upgrading fgsea versions must re-run eps=0 analyses as the underlying multi-level scheme may be refined.

## Evidence

- [methods] fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values for gene set collections without a fixed lower-bound constraint.: "fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values"
- [readme] P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme allowing arbitrarily low P-values.: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [readme] As you can see `fgsea` has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero in the `fgsea` function.: "If you need to estimate P-value more accurately, you can set the `eps` argument to zero"
- [methods] Run fgsea with eps=0 to disable the lower-bound estimate and enable adaptive multi-level split Monte Carlo refinement.: "Run fgsea again with eps=0 to disable the lower-bound estimate and enable adaptive multi-level split Monte Carlo refinement"
- [methods] Validate that eps=0 run completes without numerical errors and produces valid P-value rankings consistent with default run.: "Validate that eps=0 run completes without numerical errors and produces valid P-value rankings consistent with default run"
