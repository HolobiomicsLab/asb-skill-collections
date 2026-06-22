---
name: multivariate-ordination-analysis
description: Use when when you have normalized peak intensities from FT-ICR MS metabolomic data (or similar high-dimensional compositional data) grouped by experimental treatments (e.g., phage type, incubation time) and want to visualize whether sample groups cluster separately in reduced dimensionality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - vegan
  - MetaboDirect
  - R
  - R prcomp
  - ggplot2 (R)
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

# multivariate-ordination-analysis

## Summary

Ordination analysis (NMDS and PCA) reduces high-dimensional metabolomic data to low-dimensional visual representations to assess whether treatment groups separate in chemical composition space. This skill is applied after distance matrix calculation to visualize subtle metabolite compositional differences, though it often fails to discriminate groups that PERMANOVA detects as statistically significant.

## When to use

When you have normalized peak intensities from FT-ICR MS metabolomic data (or similar high-dimensional compositional data) grouped by experimental treatments (e.g., phage type, incubation time) and want to visualize whether sample groups cluster separately in reduced dimensionality. Apply this skill after calculating Bray-Curtis distance matrices when you need to assess the visual separation of treatment groups, especially when PERMANOVA reveals statistically significant differences but NMDS/PCA fail to show clear separation—indicating subtle, multivariate differences.

## When NOT to use

- Input is already a 2D/3D feature representation or embedding (e.g., t-SNE, UMAP output); ordination would be redundant.
- Sample size is very small (n < 6 per group); ordination plots become unreliable for visual pattern assessment.
- Treatment groups are known *a priori* to be well-separated in 1D (e.g., univariate metabolite levels already show clear differences); multivariate ordination adds little value.

## Inputs

- Normalized peak intensity matrix (.csv) with rows = metabolites and columns = samples
- Bray-Curtis distance matrix (output from vegan::vegdist)
- Treatment group assignments (phage type: HP1/HS2/control; incubation time)
- Thermodynamic indices and molecular composition table for PCA

## Outputs

- NMDS scores matrix (sample coordinates in 2D space)
- NMDS stress value (single numeric)
- PCA scores matrix (sample projections on principal components)
- PCA scree plot (variance explained per component)
- NMDS scatter plot (samples colored by treatment group)
- PCA biplot (samples and feature loadings)

## How to apply

Load Bray-Curtis distance matrices computed from normalized metabolite intensities grouped by treatment factors. Perform NMDS ordination using the vegan::metaMDS function with Bray-Curtis distances and two dimensions, recording the stress value as a measure of ordination quality (lower stress indicates better 2D representation). Simultaneously compute PCA using prcomp on magnitude-averaged thermodynamic indices and molecular composition features. Generate scatter plots for both ordinations with points colored/shaped by treatment group (phage type and incubation time). Compare the two ordination plots: if PERMANOVA p < 0.05 but NMDS and PCA show no clear group separation, this indicates treatment effects are real but distributed across many small differences in the metabolomic profile rather than dominated by one or two principal axes.

## Related tools

- **vegan** (Compute Bray-Curtis distance matrices (vegdist), perform NMDS ordination (metaMDS), calculate diversity metrics, and support multivariate statistical tests) — https://github.com/vegandevs/vegan
- **R prcomp** (Perform PCA on magnitude-averaged thermodynamic indices and molecular composition features)
- **MetaboDirect** (Pre-process FT-ICR MS data, normalize peak intensities, and generate thermodynamic indices used as PCA input) — https://github.com/Coayala/MetaboDirect
- **ggplot2 (R)** (Visualize NMDS and PCA scores as scatter plots with treatment group colorings)

## Examples

```
vegdist(normalized_intensities, method='bray') |> metaMDS(k=2) -> nmds_result; prcomp(thermodynamic_indices, scale=TRUE) -> pca_result
```

## Evaluation signals

- NMDS stress value should be < 0.2 for reliable 2D representation; values > 0.3 indicate poor fit and suggest 3+ dimensions needed.
- PCA scree plot should show cumulative variance explained by first two PCs; if < 40%, the data is not well-represented in 2D and differences are truly multivariate.
- Visual inspection: treatment groups should be somewhat separable in NMDS/PCA space if effects exist; complete overlap suggests ordination has not captured the signal (consistent with PERMANOVA p > 0.05).
- Cross-validation: if PERMANOVA is significant (p < 0.05) but ordination shows no separation, this is expected and confirms effects are subtle; if PERMANOVA is non-significant and ordination shows separation, investigate for spurious clustering.
- Sample replicates should cluster tightly within their treatment group in both ordinations; high within-group scatter suggests high biological/technical variability.

## Limitations

- NMDS and PCA ordination can fail to discriminate treatment groups even when PERMANOVA detects statistically significant differences, because ordination compresses high-dimensional differences into 2D, losing information about subtle multivariate effects distributed across many features.
- NMDS stress values increase when groups are poorly separated or sample size is very small, making 2D visualization unreliable; 3+ dimensional ordination may be necessary but harder to visualize.
- PCA assumes linear relationships among features; if treatment effects are nonlinear or involve feature interactions, PCA may not capture them effectively.
- FT-ICR MS data has inherent limitations including inability to separate chemical isomers and signal suppression/enhancement from ion effects, which can obscure true metabolomic separation even in ordination space.
- Choice of distance metric (Bray-Curtis) and normalization method affects ordination outcome; other metrics (Euclidean, Hellinger) may yield different visual separations.

## Evidence

- [other] Calculate NMDS ordination using vegan metaMDS with Bray-Curtis distances and two dimensions, producing NMDS stress values and sample scores.: "Calculate NMDS ordination using vegan metaMDS with Bray-Curtis distances and two dimensions, producing NMDS stress values and sample scores."
- [other] Generate PCA using prcomp on magnitude-averaged thermodynamic indices and molecular composition of samples, producing scree plots and biplots.: "Generate PCA using prcomp on magnitude-averaged thermodynamic indices and molecular composition of samples, producing scree plots and biplots."
- [other] PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05), while NMDS and PCA ordination analyses were unable to discriminate among sample groups, suggesting the differences are subtle.: "PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05),"
- [other] Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time.: "Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time."
- [readme] vegan — tidyverse — RColorBrewer — vegan — ggnewscale — ggpubr — KEGGREST — factoextra — UpSetR — pmartR (for normalization tests) — SYNCSA: "R packages: tidyverse, RColorBrewer, vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR (for normalization tests), SYNCSA"
