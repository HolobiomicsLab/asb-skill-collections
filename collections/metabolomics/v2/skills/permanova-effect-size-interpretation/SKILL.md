---
name: permanova-effect-size-interpretation
description: Use when after running PERMANOVA on distance matrices derived from FT-ICR MS metabolite peak intensities or other high-dimensional compositional data, when p-values indicate statistical significance but ordination plots (NMDS, PCA) fail to discriminate among treatment groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2426
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2269
  tools:
  - vegan
  - MetaboDirect
  - R
  - R (prcomp)
  - ggplot2 / seaborn
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- calculate diversity metrics using functions from the R packages vegan [63] and SYNCSA [64]
- using functions from the R packages vegan [63]
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
---

# permanova-effect-size-interpretation

## Summary

Interpret PERMANOVA effect sizes (R² and F-statistics) to distinguish between statistically significant and ecologically meaningful differences in multivariate metabolomic or compositional data. This skill addresses the gap between statistical significance and ordination visualization, where subtle but real differences may not be visually apparent in NMDS or PCA plots.

## When to use

After running PERMANOVA on distance matrices derived from FT-ICR MS metabolite peak intensities or other high-dimensional compositional data, when p-values indicate statistical significance but ordination plots (NMDS, PCA) fail to discriminate among treatment groups. Use this skill to decide whether the detected differences are subtle but real, or whether the effect size is too small to be practically meaningful.

## When NOT to use

- When PERMANOVA p-value is not significant (p ≥ 0.05); effect size interpretation is moot if no statistical signal is detected.
- When ordination plots clearly show distinct clusters AND PERMANOVA is significant; in this case, effect size is large and does not require special interpretation.
- When raw (non-normalized) FT-ICR MS peak intensities are used without prior filtering by m/z range, isotopic presence, formula assignment error, or sample abundance thresholds; effect size estimates depend on data quality.
- When sample size is very small (n < 3 per group); permutation tests underlying PERMANOVA become unreliable.

## Inputs

- PERMANOVA results table (.csv) with F-statistics, R², and p-values for each factor
- NMDS ordination stress values and sample coordinates
- PCA scree plot and variance explained per principal component
- Normalized peak intensity matrix or distance matrix metadata

## Outputs

- Interpreted PERMANOVA summary table documenting effect size (R²), F-statistic, p-value, and ordination agreement
- Annotated scatterplots (NMDS or PCA) with effect size and stress annotations
- Decision statement: whether differences are subtle-but-real or negligibly small

## How to apply

Extract R² (coefficient of determination) and F-statistics from PERMANOVA output for each tested factor (e.g., phage type, incubation time). R² indicates the proportion of total variance explained by that factor; low R² values (e.g., <0.1) coupled with p < 0.05 signal subtle but statistically detectable differences. Compare PERMANOVA results against ordination stress values (NMDS stress > 0.2 or low variance explained in PCA) to confirm that the lack of visual clustering is not a failure of the ordination method but a true feature of the data—namely, that group separation, though significant, is small in effect size. Document R² and F-values in a summary table alongside sample size, distance metric (e.g., Bray-Curtis), and p-value thresholds to contextualize the biological or chemical significance of the differences.

## Related tools

- **vegan** (Provides adonis function for PERMANOVA testing and metaMDS for NMDS ordination; vegdist computes Bray-Curtis distance matrices required for effect size calculation)
- **MetaboDirect** (Generates pre-processed normalized FT-ICR MS peak intensity matrices (.csv) and performs data diagnostics (filtering by m/z, isotope, formula error, sample abundance) prior to distance calculation and PERMANOVA) — https://github.com/Coayala/MetaboDirect
- **R (prcomp)** (Computes PCA on magnitude-averaged thermodynamic indices or molecular composition; produces scree plots and variance explained for comparison against PERMANOVA effect sizes)
- **ggplot2 / seaborn** (Visualizes NMDS and PCA ordination scores as scatterplots with treatment groupings and annotations of stress values or R² effect sizes)

## Examples

```
# Load normalized intensities, compute Bray-Curtis distances, run PERMANOVA, extract R² and F-statistics
library(vegan)
D <- vegdist(metabolite_intensities, method="bray")
permanova_result <- adonis(D ~ phage_type + incubation_time, data=metadata)
print(permanova_result)  # Check R² and F for each factor; if p < 0.05 and R² < 0.1, interpret as subtle effect
```

## Evaluation signals

- R² value is quantified and reported alongside p-value; if p < 0.05 and R² < 0.1, explicitly label the finding as 'subtle effect size'.
- NMDS stress value is documented and compared to R² interpretation: stress > 0.2 or low PCA variance explained validates that lack of visual separation is consistent with low effect size.
- PERMANOVA F-statistics are within the expected range for the study design (e.g., F > 1 indicates factor explains more variance than residual error).
- Summary table includes all four metrics (F, R², p-value, sample size) for each factor tested, enabling reader judgment of effect size magnitude.
- Scatterplots are annotated with stress or variance labels and include a caption explicitly stating whether differences are statistically significant but visually subtle.

## Limitations

- PERMANOVA R² does not account for spatial structure or non-linear patterns in the metabolomic space; low R² may reflect high within-group heterogeneity rather than negligible between-group difference.
- Bray-Curtis distance (and other compositional metrics) can be sensitive to rare or abundant metabolites and to zero-inflation; filtering thresholds (sample prevalence, peak intensity cutoffs) should be reported to enable interpretation of R² in context.
- NMDS and PCA are 2D projections of high-dimensional data; subtle differences may exist in dimensions not visualized, making ordination-based judgment of effect size incomplete. Multi-dimensional ordination (e.g., 3D NMDS) or alternative visualization (e.g., Van Krevelen diagrams) may reveal structure not obvious in 2D.
- PERMANOVA permutation distribution can be unstable with very small sample sizes (n < 3 per group) or imbalanced designs; p-values and R² are more reliable when sample size and replication are adequate.
- FT-ICR MS data quality issues (ion suppression, inability to separate isomers, mass resolution limits) can introduce measurement noise that inflates or deflates apparent effect sizes; MetaboDirect filtering parameters (m/z range, formula error threshold, isotope presence) must be reported.

## Evidence

- [other] PERMANOVA analysis revealed that phage type produced statistically significant differences in metabolite content (p < 0.05), while NMDS and PCA ordination analyses were unable to discriminate among sample groups, suggesting the differences are subtle.: "PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05),"
- [other] PERMANOVA results should be exported as a CSV table with F-statistics and R² values for each factor.: "Perform PERMANOVA using adonis function in vegan to test for significant differences between treatment groups, generating F-statistics, R² values, and p-values for each factor (phage type and time)."
- [other] Bray-Curtis distance matrices are the standard metric for metabolomic composition comparisons.: "Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time."
- [methods] Data must be pre-processed and normalized before statistical analysis.: "Filtering and normalization of data ✔"
- [abstract] MetaboDirect performs pre-processing and normalization on FT-ICR MS data prior to statistical analysis.: "MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization"
