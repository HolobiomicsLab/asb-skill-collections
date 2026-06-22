---
name: soft-thresholding-adjacency-weighting
description: Use when after computing a biweight midcorrelation similarity matrix across normalized metabolite abundance data, and before hierarchical clustering on dissimilarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - MetaboDiff
  - WGCNA
  - R
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
---

# Soft-thresholding-adjacency-weighting

## Summary

Convert a biweight midcorrelation similarity matrix into a weighted adjacency matrix by applying soft thresholding with a power parameter, which preserves the continuous strength of metabolite relationships while suppressing weak correlations. This step bridges correlation measurement and network topology construction, enabling robust identification of metabolic co-expression modules.

## When to use

After computing a biweight midcorrelation similarity matrix across normalized metabolite abundance data, and before hierarchical clustering on dissimilarity. Use this when you need to weight network edges by correlation strength (rather than threshold them as binary) to better capture subtle metabolite relationships and reduce the distortion caused by hard cutoffs on complicated dendrograms.

## When NOT to use

- Input is already a binary adjacency matrix or hard-thresholded network (soft thresholding is designed to preserve continuous correlation strength, not convert discrete edges).
- Analysis requires explicit correlation cutoff rules (e.g., p < 0.05) rather than correlation-driven weighting; use hard thresholding instead.
- Data have already undergone dissimilarity conversion through another method.

## Inputs

- Biweight midcorrelation similarity matrix (metabolite × metabolite, values in [0, 1])
- Power parameter β (typically 2–4)

## Outputs

- Weighted adjacency matrix (metabolite × metabolite, continuous edge weights)
- Dissimilarity matrix (1 − adjacency, ready for hierarchical clustering)

## How to apply

Apply soft thresholding to the similarity matrix using a power parameter (β) to convert each similarity value s_ij to an adjacency weight a_ij = s_ij^β. In the Priolo et al. study, β=3 was used, which amplifies strong correlations while dampening weak ones without hard cutoff. Compute the dissimilarity matrix as 1 − adjacency. This preserves correlation magnitude information, making the subsequent hierarchical clustering and dynamic branch cutting more sensitive to the actual topology of metabolite relationships. The power parameter should be chosen to balance sensitivity to biological signal against noise; higher powers more aggressively suppress weak edges.

## Related tools

- **WGCNA** (Provides soft-thresholding functions and adjacency weighting for weighted correlation network analysis) — https://github.com/cran/WGCNA
- **MetaboDiff** (Implements workflow steps including soft thresholding in the context of metabolic correlation network construction) — https://github.com/andreasmock/MetaboDiff
- **R** (Computation environment for matrix operations and soft-thresholding calculation)

## Examples

```
# Compute adjacency from biweight midcorrelation similarity with soft threshold (β=3)
require(WGCNA)
similarity_matrix <- cor(t(norm_metabolites), method='bicor')
adjacency <- similarity_matrix^3
dissimilarity <- 1 - adjacency
hc <- hclust(as.dist(dissimilarity), method='average')
```

## Evaluation signals

- Adjacency matrix values are continuous, bounded in [0, 1], and show power-law decay relative to original similarity values
- Dissimilarity matrix (1 − adjacency) is symmetric and non-negative
- Strong correlations (s_ij > 0.8) remain high-weight after soft thresholding; weak correlations (s_ij < 0.3) are substantially suppressed
- Subsequent hierarchical clustering dendrogram exhibits well-separated, distinct branch structures (indicating meaningful network topology was preserved)
- Module assignments from dynamic branch cutting show biological coherence (e.g., modules enriched for specific metabolic pathways or SUB_PATHWAY annotations)

## Limitations

- Power parameter β must be chosen empirically; no universal default exists. Values too low fail to suppress noise; values too high may discard biologically relevant weak correlations.
- Soft thresholding assumes correlation strength is a proxy for biological co-regulation, which may not hold in all metabolic contexts (e.g., nodes in feedback loops may show weak correlation despite strong interaction).
- Sensitive to outliers in the input similarity matrix; pre-filtering of extreme correlation values or use of robust measures (like biweight midcorrelation) is recommended.
- Does not directly handle missing data; imputation and outlier removal should precede soft thresholding.

## Evidence

- [methods] Apply soft thresholding with power β=3 to convert similarity to adjacency: "Apply soft thresholding with power β=3 to convert similarity to adjacency, then compute dissimilarity as 1 − adjacency."
- [methods] Biweight midcorrelation used because it is more robust to outliers: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient"
- [methods] Dynamic branch cut method employed on dissimilarity matrix: "We employed the dynamic branch cut method developed by Langfelder and colleagues, as constant height cutoffs exhibit suboptimal performance on complicated dendrograms."
- [readme] MetaboDiff offers metabolic correlation network exploration: "MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
