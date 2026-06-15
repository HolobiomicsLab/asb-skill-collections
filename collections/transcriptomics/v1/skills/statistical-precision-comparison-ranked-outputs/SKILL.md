---
name: statistical-precision-comparison-ranked-outputs
description: Use when when a statistical method offers a parameter to trade computational cost for precision (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0085
  - http://edamontology.org/topic_3473
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

# Statistical Precision Comparison of Ranked Outputs

## Summary

Compare P-value precision and ranking consistency between two statistical estimation modes (e.g., default lower-bound vs. adaptive refinement) to validate whether relaxing precision constraints produces numerically valid and meaningful differences in gene set enrichment rankings.

## When to use

When a statistical method offers a parameter to trade computational cost for precision (e.g., eps parameter controlling P-value lower-bound estimation), and you need to determine whether disabling the lower-bound constraint yields materially different rankings, more accurate P-values, or improved discriminatory power among pathways without introducing numerical instability.

## When NOT to use

- The method does not support precision tuning parameters (e.g., no eps-like argument available).
- Output is already a summary statistic (e.g., a single aggregate P-value) rather than a ranked table—comparison requires per-entity rankings.
- Computational cost difference is negligible, making the trade-off comparison moot.

## Inputs

- Gene set pathways (e.g., examplePathways: list of named character vectors)
- Pre-ranked gene statistics (e.g., exampleRanks: named numeric vector of log fold-changes or test statistics)
- Statistical enrichment results from default mode (data.table with columns: pathway, pval, padj, ES, NES, size)

## Outputs

- Comparison table joining default and refined results by pathway identifier
- P-value difference and fold-change ratio columns (log-scale recommended)
- Distribution visualization (log-scale histogram or violin plot of P-value changes)
- Ranked list of pathways by precision improvement magnitude
- Validation report confirming numerical stability and ranking consistency

## How to apply

Run the same enrichment analysis twice: once with default precision settings (e.g., eps=1e-10) and once with adaptive refinement enabled (e.g., eps=0). Join results by pathway identifier and compute P-value differences and fold-change ratios in P-value magnitude. Visualize the distribution of P-value changes on a log scale and rank pathways by the degree of precision improvement. Validate that the refined run completes without numerical errors, produces valid P-value rankings (monotonically ordered), and shows consistency in top-ranked pathways between both runs—ensuring that the precision gain does not fundamentally alter biological interpretation.

## Related tools

- **fgsea** (Fast preranked GSEA implementation with configurable eps parameter to control P-value estimation precision via adaptive multi-level split Monte-Carlo scheme) — https://github.com/ctlab/fgsea
- **data.table** (Efficient joining, filtering, and comparison of result tables by pathway identifier)
- **ggplot2** (Visualization of P-value change distributions and ranked pathway comparisons)

## Examples

```
fgseaRes_default <- fgsea(pathways = examplePathways, stats = exampleRanks, eps = 1e-10, minSize = 15, maxSize = 500); fgseaRes_refined <- fgsea(pathways = examplePathways, stats = exampleRanks, eps = 0.0, minSize = 15, maxSize = 500); comparison <- merge(fgseaRes_default[, .(pathway, pval_default=pval)], fgseaRes_refined[, .(pathway, pval_refined=pval)], by="pathway")[, fold_change := pval_default / pval_refined]
```

## Evaluation signals

- P-value differences are monotonic and log-distributed (no sign flips or non-monotonic P-value ratios for the same pathway).
- Refined run completes without numerical errors, NaN values, or infinite P-values.
- Top-ranked pathways (e.g., top 10 by default p-value) remain in top-ranked positions in refined results, with rank order preserved or improved by precision.
- P-value fold-change distribution shows expected pattern: smallest P-values improve most (largest fold-change), largest P-values show minimal change.
- Comparison table row counts match and all pathways are represented in the join (no missing or unmatched entries).

## Limitations

- Enabling adaptive refinement (eps=0) may increase computational time substantially and is not suitable for real-time analysis of very large pathway collections.
- P-value precision improvements are most visible for pathways with moderate-to-high enrichment signal; weakly enriched pathways may show minimal differences.
- The adaptive multi-level scheme is specific to the GSEA algorithm; different enrichment methods may not support or benefit from this precision trade-off.

## Evidence

- [other] fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values without a fixed lower-bound constraint: "fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values for gene set collections without a fixed lower-bound constraint."
- [other] Run fgsea twice with different eps values and construct comparison by pathway ID, computing P-value differences and fold-change ratios: "Construct comparison table joining results from both runs by pathway identifier, computing P-value differences and fold-change ratios."
- [other] Validate that refined run completes without errors and produces valid P-value rankings consistent with default run: "Validate that eps=0 run completes without numerical errors and produces valid P-value rankings consistent with default run."
- [readme] fgsea has a default lower bound eps=1e-10; setting eps=0 enables more accurate P-value estimation: "fgsea has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero in the `fgsea` function."
- [other] Visualize distribution of P-value changes and identify pathways with greatest precision improvement: "Visualize distribution of P-value changes (log-scale) and identify pathways with greatest precision improvement."
