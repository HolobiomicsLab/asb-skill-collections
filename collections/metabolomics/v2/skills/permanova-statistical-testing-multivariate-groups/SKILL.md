---
name: permanova-statistical-testing-multivariate-groups
description: Use when you have normalized peak intensities or abundance matrices from mass spectrometry (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDirect
  - vegan (R package)
  - Python 3.8
  - R 4.0.2
  - vegan
  - R
  - Python
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- distances (depending on the selected normalization method) using the "vegdist" function for the vegan package and then used to perform a permutational analysis of variance (PERMANOVA)
- The MetaboDirect pipeline was developed in Python 3.8
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
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

# permanova-statistical-testing-multivariate-groups

## Summary

Permutational multivariate analysis of variance (PERMANOVA) tests whether categorical grouping factors (e.g., treatment, phage type, environmental condition) produce statistically significant differences in multivariate metabolomic or compositional data. This skill is essential for hypothesis-driven metabolomics when you need to determine if a factor of interest significantly structures the overall metabolite abundance or molecular composition profiles.

## When to use

Apply this skill when you have normalized peak intensities or abundance matrices from mass spectrometry (e.g., FT-ICR MS) or other high-dimensional compositional data, and you want to test whether a categorical grouping factor (such as phage type: HP1 vs. HS2 vs. control, or treatment condition) produces a statistically significant difference in metabolite content or molecular composition. The input must be a normalized, sample-by-feature abundance matrix with clear categorical metadata labels for each sample.

## When NOT to use

- Input data are not normalized or have not undergone quality filtering (e.g., peaks with >50% missing values, isotopic duplicates not removed, or formula assignment error > 0.5 ppm tolerance — apply MetaboDirect pre-processing and filtering steps first).
- The grouping factor has only one or two levels with highly unequal sample sizes (n < 3 per group), which violates PERMANOVA assumptions and reduces power.
- Raw, unprocessed FT-ICR MS spectra are provided instead of pre-assigned molecular formulas and peak abundance tables — MetaboDirect does not provide raw spectra preprocessing, so signal processing must be completed separately.

## Inputs

- normalized peak intensity matrix (samples × peaks, CSV format)
- sample metadata with categorical grouping factor (e.g., phage type, treatment)
- assigned molecular formula data (optional, for compound class annotation)

## Outputs

- PERMANOVA results table (p-value, F-statistic, R², degrees of freedom)
- NMDS ordination scores (first two components, CSV format)
- NMDS scatterplot with group labels and confidence ellipses

## How to apply

First, calculate pairwise distances between all samples using an appropriate metric (Bray-Curtis, Euclidean, or Jaccard) via the `vegdist()` function from the R vegan package on the normalized peak intensity matrix. Then execute PERMANOVA using the categorical grouping factor (e.g., phage type) with 999 permutations to generate a permutation distribution under the null hypothesis of no group effect. Extract the p-value, F-statistic, and R² (effect size) from the PERMANOVA output. Compare the p-value against the significance threshold (typically α = 0.05) to determine whether the grouping factor explains a statistically significant portion of multivariate variance. Simultaneously, generate non-metric multidimensional scaling (NMDS) ordination using the same distance metric to visualize the grouping structure and validate that ordination patterns align with the statistical result.

## Related tools

- **vegan** (R package providing vegdist() for distance calculation and adonis() for PERMANOVA execution) — https://cran.r-project.org/package=vegan
- **MetaboDirect** (command-line pipeline that wraps PERMANOVA and NMDS analysis for FT-ICR MS data, executing both analyses and generating ordination visualizations within a unified workflow) — https://github.com/Coayala/MetaboDirect
- **R** (runtime environment (version 4.0.2 or above) required for vegan and downstream multivariate statistics)
- **Python** (scripting language (3.8 or above) for data wrangling, file I/O, and coordinate export)

## Evaluation signals

- PERMANOVA p-value is reported and compared against α = 0.05 threshold; statistical significance is explicit and reproducible.
- NMDS scatterplot visually clusters samples by the grouping factor in a pattern concordant with the PERMANOVA result (significant p-value → clear cluster separation; non-significant p-value → overlapping clusters).
- R² effect size is reported and is consistent with the magnitude of visual separation in the ordination (larger R² → stronger ordination signal).
- Distance metric choice (Bray-Curtis, Euclidean, or Jaccard) is specified and justified; results are sensitive to metric choice and should be consistent with metabolomic conventions (Bray-Curtis for abundance-weighted dissimilarity is most common in ecology).
- Permutation count (999 or higher) is sufficient to estimate a reliable p-value (especially when p-value is near the significance threshold); convergence of the permutation test is confirmed.

## Limitations

- PERMANOVA is sensitive to differences in multivariate spread (dispersion) between groups, not just location; use betadisper() to test homogeneity of variance before interpreting PERMANOVA results.
- The choice of distance metric strongly influences results; Bray-Curtis assumes abundance data and is appropriate for metabolomics, but Euclidean distance assumes normally distributed, continuous data and may not be suitable for sparse or zero-inflated metabolite matrices.
- MetaboDirect does not provide raw spectra data preprocessing; molecular formula assignment and peak detection must be completed by upstream tools before input to the MetaboDirect pipeline.
- PERMANOVA assumes that samples are exchangeable under the null hypothesis; if samples are pseudoreplicated (e.g., technical replicates, or nested within blocks), the test can be anticonservative unless proper blocking or random-effects structures are specified.

## Evidence

- [other] Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations.: "Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations."
- [other] Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities.: "Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities."
- [other] Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes.: "Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes."
- [other] PERMANOVA analysis of the bacterium-phage dataset shows that phage type produces a significant difference in metabolite content with p < 0.05: "PERMANOVA analysis of the bacterium-phage dataset shows that phage type produces a significant difference in metabolite content with p < 0.05"
- [readme] vegan - ggnewscale - ggpubr - KEGGREST - factoextra - UpSetR - pmartR (for normalization tests) - SYNCSA - ggvenn - ggrepel: "vegan - ggnewscale - ggpubr - KEGGREST - factoextra - UpSetR - pmartR (for normalization tests) - SYNCSA - ggvenn - ggrepel"
