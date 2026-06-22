---
name: metabolite-composition-comparison-across-treatments
description: Use when you have normalized peak intensity tables from FT-ICR MS data (e.g., MetaboDirect .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - vegan
  - MetaboDirect
  - R
  - R base (prcomp)
  - ggplot2 / ggpubr
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-composition-comparison-across-treatments

## Summary

A multivariate statistical approach to test whether experimental treatments (e.g., phage type, incubation time) produce statistically significant differences in metabolite/organic compound composition detected by FT-ICR MS. This skill combines distance-based permutation analysis (PERMANOVA) with ordination visualization to detect subtle compositional shifts that may be invisible to unsupervised methods alone.

## When to use

Apply this skill when you have normalized peak intensity tables from FT-ICR MS data (e.g., MetaboDirect .csv output with assigned molecular formulas) and need to test whether two or more categorical treatments (phage type, environmental condition, time point, or other factor) produce statistically significant differences in metabolite composition. Use this specifically when you expect subtle, multivariate differences that univariate or visual ordination methods (PCA, NMDS) may fail to resolve.

## When NOT to use

- Input is already a pre-computed distance matrix without access to the original peak intensities — you cannot recalculate distances under different distance metrics or verify data filtering.
- Treatment groups are continuous variables (e.g., pH, temperature as a numeric gradient) rather than discrete categories — use regression-based or distance-based correlation methods (Mantel test, dbRDA) instead.
- Sample size per treatment group is very small (n < 3) — PERMANOVA relies on permutation and lacks statistical power; consider reporting descriptive statistics and visual clustering only.

## Inputs

- normalized peak intensity matrix (e.g., MetaboDirect .csv output)
- assigned molecular formula table (one row per m/z peak, columns including elemental composition and/or thermodynamic indices)
- sample metadata table mapping each sample to treatment factors (phage type, incubation time, replicate ID, etc.)

## Outputs

- PERMANOVA results table (.csv): F-statistic, R² value, and p-value for each treatment factor and interaction
- Bray-Curtis distance matrix (.csv or R object)
- NMDS ordination coordinates and stress value
- PCA loadings and scree plot
- NMDS scatter plot (samples colored/shaped by treatment)
- PCA biplot (samples and loadings)
- Supplementary ordination diagnostics (e.g., Shepard diagram for NMDS stress)

## How to apply

Load normalized peak intensities grouped by treatment factors (phage type, incubation time, etc.) and calculate Bray-Curtis distance matrices using the R vegan package vegdist function. Perform PERMANOVA using the adonis function to test for significant differences between treatment groups, producing F-statistics, R² values, and p-values for each factor. In parallel, compute NMDS ordination (metaMDS with Bray-Curtis distances, 2 dimensions) and PCA (using prcomp on normalized intensities or thermodynamic indices) to visualize the sample space, even if ordination stress is high or clustering is weak. The rationale is that PERMANOVA tests multivariate compositional differences in a hypothesis-driven way (controlling for multiple factors and their interactions), whereas ordination provides a visual check for concordance: if PERMANOVA is significant but ordination shows poor group separation, this confirms that metabolite differences are statistically real but compositionally subtle. Export PERMANOVA results as .csv and visualize NMDS/PCA scores as scatter plots colored by treatment grouping.

## Related tools

- **vegan** (R package providing vegdist (distance matrix calculation), adonis (PERMANOVA test), and metaMDS (NMDS ordination); core statistical engine for multivariate compositional analysis) — https://github.com/vegandevs/vegan
- **MetaboDirect** (FT-ICR MS data preprocessing and normalization pipeline that produces the normalized peak intensity .csv input required for this skill) — https://github.com/Coayala/MetaboDirect
- **R base (prcomp)** (Standard R function for principal component analysis; used to compute PCA coordinates and loadings alongside NMDS for ordination visualization)
- **ggplot2 / ggpubr** (R visualization libraries for producing publication-quality scatter plots of NMDS and PCA scores colored/shaped by treatment group)

## Examples

```
library(vegan); meta <- read.csv('normalized_intensities.csv', row.names=1); design <- read.csv('treatment_metadata.csv', row.names=1); bray <- vegdist(meta, method='bray'); perm <- adonis2(bray ~ phage_type * time, data=design, permutations=999); nmds <- metaMDS(bray, k=2); print(perm); plot(nmds, type='n'); points(nmds, display='sites', col=as.numeric(design$phage_type))
```

## Evaluation signals

- PERMANOVA p-value is < 0.05 for the treatment factor of interest, indicating statistically significant compositional difference at the multivariate level.
- PERMANOVA R² value (effect size) is >0.05 and <1.0, indicating a meaningful but not overly-deterministic fraction of variance explained by treatment.
- NMDS stress value is ≤0.20 (good fit) or ≤0.30 (acceptable fit); values >0.30 suggest that ordination distorts relationships and results should be interpreted cautiously.
- Sample scores in NMDS/PCA scatter plots show visual clustering by treatment group consistent with the direction and sign of PERMANOVA p-values (e.g., if PERMANOVA is significant, visual separation is expected, even if subtle).
- Reproducibility check: re-running PERMANOVA on the same input with the same random seed (if applicable) and permutation count produces identical F-statistics and p-values (within rounding).

## Limitations

- PERMANOVA cannot identify which specific metabolites or molecular formulas drive the observed compositional differences; follow up with univariate tests (e.g., Wilcoxon rank-sum per metabolite) or machine learning (random forest feature importance) to pinpoint differential compounds.
- Bray-Curtis distance metric ignores double-zeros (absence in both samples) and is sensitive to rare taxa/metabolites; confirm results with alternative metrics (Jaccard, Euclidean) if rare metabolites dominate the dataset.
- FT-ICR MS cannot separate chemical isomers; metabolite identities are limited to molecular formula assignment and are not confirmed by tandem MS or retention time; compositional differences may reflect formula-level but not compound-level resolution.
- High ion suppression or enhancement in MS can bias peak intensities and Bray-Curtis distances; ensure normalization in MetaboDirect is appropriate for your sample type (total intensity, quantile, internal standard, etc.).
- PERMANOVA assumes exchangeability of residuals under the null hypothesis; violation (e.g., temporal autocorrelation, batch effects) inflates Type I error; check for and correct confounding factors before analysis.

## Evidence

- [other] PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05), while NMDS and PCA ordination analyses were unable to discriminate among sample groups: "PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05),"
- [other] Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time.: "Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment"
- [other] Perform PERMANOVA using adonis function in vegan to test for significant differences between treatment groups, generating F-statistics, R² values, and p-values for each factor (phage type and time).: "Perform PERMANOVA using adonis function in vegan to test for significant differences between treatment groups, generating F-statistics, R² values, and p-values"
- [other] Calculate NMDS ordination using vegan metaMDS with Bray-Curtis distances and two dimensions, producing NMDS stress values and sample scores.: "Calculate NMDS ordination using vegan metaMDS with Bray-Curtis distances and two dimensions, producing NMDS stress values and sample scores"
- [methods] peak intensities are normalized in this step based on the user's input: "peak intensities are normalized in this step based on the user's input"
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences: "MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization"
