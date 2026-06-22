---
name: nmds-ordination-distance-metric-selection
description: Use when when you have normalized peak intensity matrices from FT-ICR MS data or other high-resolution metabolomics experiments and need to visualize sample relationships and assess whether categorical grouping factors (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3697
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDirect
  - vegan (R package)
  - Python 3.8
  - R 4.0.2
  - R (4.0.2 or above)
  - ggplot2 or base R graphics
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

# NMDS Ordination with Distance Metric Selection

## Summary

Select and apply an appropriate distance metric (Bray-Curtis, Euclidean, or Jaccard) to calculate pairwise distances among normalized metabolite abundance samples, then perform non-metric multidimensional scaling (NMDS) to generate a 2D ordination for visualization of sample clustering and biological grouping effects.

## When to use

When you have normalized peak intensity matrices from FT-ICR MS data or other high-resolution metabolomics experiments and need to visualize sample relationships and assess whether categorical grouping factors (e.g., phage type, treatment condition) produce meaningful clustering in metabolite composition space. Apply this skill after peak filtering, formula assignment, and intensity normalization but before statistical testing (e.g., PERMANOVA) to inspect data structure.

## When NOT to use

- Input is already a pre-computed distance matrix or ordination; skip directly to visualization or statistical testing.
- Sample size is very small (n < 4–5 per group); NMDS may be unstable; consider PCA or hierarchical clustering instead.
- Peak intensity data has not been normalized; apply normalization (e.g., log-transformation, relative abundance) before distance calculation to avoid bias from highly abundant peaks.

## Inputs

- Normalized peak intensity matrix (samples × peaks, with intensities normalized by MetaboDirect steps 1–4)
- Sample metadata table with grouping factors (e.g., phage type, treatment)
- Assigned molecular formulas (optional, for interpretation)

## Outputs

- Pairwise distance matrix (samples × samples, using selected metric)
- NMDS scores table (samples × 2 or more components)
- NMDS ordination scatterplot (with samples grouped by factor)
- NMDS coordinates CSV file for downstream analysis

## How to apply

Load normalized peak intensity data and sample metadata from preprocessed CSV files. Calculate pairwise distances between all samples using the vegdist function from the vegan R package, selecting one of three distance metrics: Bray-Curtis (recommended for compositional metabolomics data to account for relative abundance differences), Euclidean (for continuous multivariate data), or Jaccard (for presence/absence data). Execute NMDS ordination on the resulting distance matrix using the selected metric. Extract NMDS scores (typically the first two components) and generate a 2D scatterplot with samples colored or shaped by the grouping factor of interest. Export NMDS coordinates as CSV for downstream statistical analysis (e.g., to overlay PERMANOVA results).

## Related tools

- **vegan (R package)** (Calculate pairwise distances (vegdist function) and perform NMDS ordination; provide Bray-Curtis, Euclidean, and Jaccard distance options) — https://cran.r-project.org/web/packages/vegan/
- **MetaboDirect** (Generate normalized peak intensity matrices and sample metadata as input for distance calculation; orchestrate pre-processing steps 1–4) — https://github.com/Coayala/MetaboDirect
- **R (4.0.2 or above)** (Execute vegan functions and generate ordination plots)
- **ggplot2 or base R graphics** (Visualize NMDS scatterplots with sample groupings)

## Examples

```
library(vegan); distances <- vegdist(normalized_peaks, method='bray'); nmds_result <- metaMDS(distances, k=2, try=20); plot(nmds_result, type='n'); points(nmds_result, col=as.factor(metadata$phage_type)); write.csv(nmds_result$points, 'nmds_scores.csv')
```

## Evaluation signals

- NMDS stress value is ≤ 0.2 (acceptable fit) or ≤ 0.1 (good fit); values >0.3 suggest poor ordination and warrant trying a different distance metric or checking data quality.
- Samples cluster visually by the grouping factor (e.g., phage type) on the 2D plot, consistent with expected biological differences; non-overlapping 95% confidence ellipses per group strengthen evidence.
- Distance matrix is symmetric, contains no missing values, and spans a reasonable range (not all zeros or identical); NMDS coordinates are numeric and finite.
- Reproducibility check: re-running NMDS with the same metric on the same normalized data produces identical ordination (up to axis reflection), confirming stochastic convergence.
- Statistical support: downstream PERMANOVA on the same distance matrix yields p < 0.05 for the grouping factor, validating that visual clustering reflects a significant effect.

## Limitations

- NMDS is a heuristic algorithm; convergence to global optimum is not guaranteed. Run multiple random starts (e.g., k=20) and check for consistent stress values.
- Distance metric choice strongly influences results; Bray-Curtis is standard for compositional metabolomics but may not be optimal for all data types. Compare metrics or use domain knowledge to select appropriately.
- NMDS visualization is inherently 2D (or 3D) but true metabolome complexity may require more dimensions; inspect higher dimensions (NMDS component 3) or use PCA if ordination seems distorted.
- Small sample size (n < 5–10 per group) or unbalanced designs can lead to unreliable ordination and weak statistical power in downstream tests.
- Peak intensity data must be normalized before distance calculation; unnormalized counts will be dominated by the most abundant peaks and mask biological signal from rare metabolites.

## Evidence

- [other] Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations.: "Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations."
- [other] Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities.: "Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities."
- [other] Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes.: "Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes."
- [methods] non-metric multidimensional scaling (NMDS): "non-metric multidimensional scaling (NMDS)"
- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
