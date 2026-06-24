---
name: distance-metric-calculation-bray-curtis-euclidean-jaccard
description: Use when you have normalized peak intensity data (or absence/presence
  matrices) from metabolomics experiments with multiple samples and need to quantify
  compositional differences between them prior to multivariate analysis. This step
  is essential when testing whether categorical factors (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDirect
  - vegan (R package)
  - Python 3.8
  - R 4.0.2
  - R (version 4.0.2 or above)
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis
  (e.g., chemodiversity analysis, multivariate statistics)
- distances (depending on the selected normalization method) using the "vegdist" function
  for the vegan package and then used to perform a permutational analysis of variance
  (PERMANOVA)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# distance-metric-calculation-bray-curtis-euclidean-jaccard

## Summary

Calculate pairwise dissimilarity distances among samples in a normalized metabolomics peak intensity matrix using Bray-Curtis, Euclidean, or Jaccard metrics. These distances serve as input to ordination and statistical tests (PERMANOVA, NMDS) to evaluate whether grouping factors produce significant differences in metabolite composition.

## When to use

You have normalized peak intensity data (or absence/presence matrices) from metabolomics experiments with multiple samples and need to quantify compositional differences between them prior to multivariate analysis. This step is essential when testing whether categorical factors (e.g., phage type, treatment condition) produce statistically significant changes in the metabolite profile.

## When NOT to use

- Raw, non-normalized peak intensities (normalize via MetaboDirect steps 1–4 first).
- Unfiltered peak data with missing values or intensity outliers (apply filtering by m/z, isotopic presence, formula assignment error, and sample presence threshold beforehand).
- Single-sample or two-sample datasets where permutation-based testing lacks power (minimum ~10–15 samples recommended for PERMANOVA with 999 permutations).

## Inputs

- normalized peak intensity matrix (samples × metabolite peaks, CSV or R data frame)
- sample metadata including grouping factor (e.g., phage type: HP1, HS2, control)

## Outputs

- distance matrix (symmetric, n×n; exported as CSV or retained in R memory)
- distance metric choice (Bray-Curtis, Euclidean, or Jaccard) documented in methods

## How to apply

Load the normalized peak intensity matrix (rows = samples, columns = metabolite peaks) and sample metadata into R. Choose a distance metric appropriate to your data: Bray-Curtis for abundance-weighted compositional differences, Euclidean for Cartesian distance in intensity space, or Jaccard for presence/absence-based dissimilarity. Apply the vegdist function from the vegan R package with your chosen metric (metric='bray', 'euclidean', or 'jaccard'). This produces a distance matrix (n×n, where n = number of samples). Validate that the resulting distance matrix is symmetric and contains no missing values. The distances are then passed to PERMANOVA (with 999 permutations) or ordination (NMDS) to test for significant grouping effects.

## Related tools

- **vegan (R package)** (implements vegdist function for distance calculation on normalized peak intensities; supports Bray-Curtis, Euclidean, Jaccard, and other metrics)
- **MetaboDirect** (produces normalized peak intensity matrices (steps 1–4) that serve as input to distance calculations) — https://github.com/Coayala/MetaboDirect
- **R (version 4.0.2 or above)** (environment for vegan and downstream statistical analysis (PERMANOVA, NMDS))

## Examples

```
library(vegan); dist_bray <- vegdist(normalized_intensities, method='bray'); dist_euclidean <- vegdist(normalized_intensities, method='euclidean')
```

## Evaluation signals

- Distance matrix is symmetric (dist[i,j] == dist[j,i]) and has zero diagonal (dist[i,i] == 0).
- No missing or NaN values in the distance matrix; all pairwise distances are finite positive numbers.
- Distance metric choice is documented and reproducible; vegdist call is logged with metric parameter and function signature.
- PERMANOVA p-value and F-statistic computed from the distance matrix align with published results (e.g., p < 0.05 for phage-type effect in Supplementary Fig. 7C).
- NMDS ordination scatterplot (first two components) and stress value are reasonable; stress < 0.15 suggests a good fit.

## Limitations

- Bray-Curtis distance is undefined for zero-abundance samples in both profiles; requires at least one non-zero value per sample.
- Euclidean distance is sensitive to outliers and high-intensity peaks; may not reflect biological relevance in metabolomics where fold-change is often more informative than absolute intensity.
- Jaccard distance discards abundance information, reducing statistical power when peak intensity variation is the primary signal.
- MetaboDirect does not provide raw spectra data preprocessing; distance calculations assume input is post-processed by external tools (e.g., CoreMS, Formularity).

## Evidence

- [other] Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities.: "Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities."
- [other] Load normalized peak intensities and sample metadata from preprocessed CSV files generated by MetaboDirect steps 1–4 for the 36-sample bacterium-phage dataset.: "Load normalized peak intensities and sample metadata from preprocessed CSV files generated by MetaboDirect steps 1–4 for the 36-sample bacterium-phage dataset."
- [other] Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations.: "Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations."
- [other] Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes.: "Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes."
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
