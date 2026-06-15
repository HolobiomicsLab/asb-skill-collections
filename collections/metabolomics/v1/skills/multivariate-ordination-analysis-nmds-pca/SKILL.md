---
name: multivariate-ordination-analysis-nmds-pca
description: Use when after peak filtering and normalization, when you have a peak-abundance matrix (samples × assigned molecular formulas) and need to visualize and test for differences in overall molecular composition across experimental conditions or sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3697
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDirect
  - Python 3.8
  - R 4.0.2
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - vegan
  - SYNCSA
  - ggpubr
  - factoextra
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- The MetaboDirect pipeline was developed in Python 3.8
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2
- It requires the Python dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
---

# Multivariate Ordination Analysis (NMDS & PCA)

## Summary

Apply non-metric multidimensional scaling (NMDS) and Principal Component Analysis (PCA) to reduced-dimensional visualization and statistical characterization of FT-ICR MS peak abundance matrices, enabling comparison of molecular composition across samples and identification of compositional gradients or clusters.

## When to use

After peak filtering and normalization, when you have a peak-abundance matrix (samples × assigned molecular formulas) and need to visualize and test for differences in overall molecular composition across experimental conditions or sample groups. Use NMDS and PCA to reduce high-dimensional elemental/molecular class composition to 2D or 3D ordination space for pattern discovery and hypothesis testing via PERMANOVA.

## When NOT to use

- Input data has <3 samples per group: PERMANOVA permutation test and NMDS convergence will be unreliable.
- Peak-abundance matrix has not been normalized or filtered by presence/absence thresholds: residual rare peaks or extreme singletons can dominate distance calculations and ordination axes.
- Primary goal is to identify individual molecular formulas or peaks responsible for group separation: use univariate peak abundance tests (e.g., log-fold change, t-test) or PCA loadings inspection instead.

## Inputs

- Filtered and normalized peak-abundance matrix (samples × molecular formula peaks as CSV or data.frame)
- Sample metadata with experimental group/treatment assignments
- Assigned molecular formula identities (elemental composition per peak)

## Outputs

- PCA biplot (PC1 vs. PC2, with sample scores and peak loadings)
- NMDS ordination plot (axis 1 vs. axis 2, with stress value reported)
- PERMANOVA test results (F-statistic, R², p-value, permutation count)
- Bray–Curtis or other ecological distance matrix (if needed for downstream use)

## How to apply

Load the filtered and normalized peak-abundance matrix (samples as rows, molecular formula peaks as columns) into R using the vegan and ggpubr packages. Apply PCA to decompose variance by principal components and plot PC1 vs. PC2 to inspect compositional groupings. Separately apply NMDS ordination (Bray–Curtis or similar ecological distance metric) to the same matrix, setting a stress threshold (typical: <0.2 indicates good 2D fit) and repeating with multiple random starts to avoid local minima. Perform PERMANOVA (permutational ANOVA via vegan::adonis) on the same distance matrix to test for significant differences in molecular composition between predefined sample groups, using 999+ permutations. Visualize both ordinations with sample centroids and confidence ellipses colored by experimental treatment. The rationale: PCA identifies dominant variance axes in elemental space, while NMDS preserves pairwise distances and is more robust to non-linear relationships in high-dimensional compositional data; PERMANOVA tests whether observed ordination separation is statistically significant.

## Related tools

- **vegan** (R package providing NMDS, PCA, Bray–Curtis distance, and PERMANOVA (adonis function))
- **ggpubr** (R package for publication-ready visualization of ordination results with centroids and confidence ellipses)
- **factoextra** (R package for enhanced PCA visualization and extraction of principal component loadings)
- **MetaboDirect** (End-to-end pipeline that internally orchestrates NMDS, PCA, and PERMANOVA on filtered FT-ICR MS data via single command-line invocation) — https://github.com/Coayala/MetaboDirect

## Examples

```
metabodirect --input peak_abundance.csv --metadata sample_groups.csv --analysis ordination --ordination-methods nmds pca --permanova --output ./results
```

## Evaluation signals

- NMDS stress value is <0.2 in 2D (or <0.15 for 3D), indicating faithful representation of original distances in reduced space.
- PERMANOVA permutation test reports p-value ≤ 0.05 (or adjusted p-value if multiple group comparisons) and R² effect size ≥0.1, confirming that compositional differences between groups are statistically significant and non-random.
- PCA loadings inspection shows that the first two principal components capture ≥50% of total variance; ordination axes are interpretable in terms of elemental composition (e.g., PC1 correlated with O:C ratio or molecular class abundance).
- Visual inspection of ordination plots reveals non-overlapping sample clusters or gradients aligned with experimental treatments, consistent with PERMANOVA significance.
- NMDS/PCA reproducibility: rerunning analysis with the same data and parameters (or with a subset of randomly permuted samples) produces ordinations with equivalent stress/R² and visually similar layouts.

## Limitations

- NMDS and PCA are sensitive to peak normalization method and filtering thresholds (presence/absence cutoffs); results may shift substantially if upstream filtering or normalization parameters change.
- PERMANOVA assumes exchangeability of samples under the null hypothesis; blocked or hierarchical designs require careful specification of the permutation scheme (strata argument in adonis).
- High-dimensional elemental composition data may contain collinear peaks (e.g., isotopes or minor mass variants); PCA will spread variance across correlated components, reducing interpretability.
- MetaboDirect does not perform raw spectra data preprocessing, so NMDS/PCA is applied only to post-formula-assignment peak tables; unresolved formula ambiguities or mass calibration errors upstream can propagate.
- NMDS convergence and stress optimization depend on random start seeds; multiple independent runs with different seeds are recommended to confirm solution stability.

## Evidence

- [methods] NMDS ordination performed in paper: "non-metric multidimensional scaling (NMDS)"
- [methods] PCA analysis performed in paper: "Principal Component Analysis (PCA)"
- [methods] PERMANOVA used for statistical testing: "permutational analysis of variance (PERMANOVA)"
- [abstract] MetaboDirect integrates ordination and statistical analysis: "MetaboDirect is designed as a fully automated pipeline capable of generating figures, plots, and analysis commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data"
- [readme] vegan R package listed as dependency: "R

- tidyverse
- RColorBrewer
- vegan"
- [readme] ggpubr R package listed as dependency for visualization: "R

- tidyverse
- RColorBrewer
- vegan
- ggnewscale
- ggpubr"
