---
name: microbial-phage-infection-experimental-design-interpretation
description: Use when you have a bacterium-phage infection study with normalized peak
  intensities from FT-ICR MS across multiple phage treatment groups (minimum 2–3 conditions
  such as HP1, HS2, control) and sample replicates (n ≥ 6–8 per group), and you need
  to test whether phage-type factor explains.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3373
  tools:
  - MetaboDirect
  - vegan (R package)
  - Python 3.8
  - R 4.0.2
  - R
  - Python
  license_tier: restricted
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

# microbial-phage-infection-experimental-design-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret metabolomic responses of marine bacteria to infection by different phage types (HP1, HS2, control) using multivariate statistical analysis (PERMANOVA) on FT-ICR MS peak intensity data. This skill determines whether phage type produces statistically significant differences in exometabolome composition.

## When to use

You have a bacterium-phage infection study with normalized peak intensities from FT-ICR MS across multiple phage treatment groups (minimum 2–3 conditions such as HP1, HS2, control) and sample replicates (n ≥ 6–8 per group), and you need to test whether phage-type factor explains significant variance in metabolite composition using permutation-based statistical inference rather than parametric assumptions.

## When NOT to use

- Input is raw or unprocessed FT-ICR MS spectra; MetaboDirect requires pre-processed peak abundance and molecular formula assignment data.
- Sample size per phage-type group is < 3 replicates; PERMANOVA requires sufficient within-group replication for reliable permutation-based p-values.
- Metabolite data are already collapsed into a feature table with aggregated counts or ratios (e.g., KEGG pathway abundances); PERMANOVA requires peak-level intensity variation to detect composition differences.

## Inputs

- Normalized peak intensities (CSV matrix: samples × detected peaks with intensity values)
- Sample metadata (CSV: sample_id, phage_type [HP1/HS2/control], replicate_group)
- Assigned molecular formulas (optional, for compound class annotation in ordination plots)

## Outputs

- PERMANOVA results table (p-value, F-statistic, R², degrees of freedom)
- NMDS coordinates (CSV: sample_id, NMDS1, NMDS2, phage_type)
- NMDS ordination scatterplot (two-component visualization with phage-type color coding)
- Distance matrix (Bray-Curtis/Euclidean/Jaccard dissimilarity between all sample pairs)

## How to apply

Load normalized peak intensities and sample metadata (phage type, replicate identifiers) from MetaboDirect pre-processed CSV files. Calculate pairwise distances between samples using Bray-Curtis, Euclidean, or Jaccard distance metrics via the vegan R package vegdist function on the normalized intensity matrix. Execute PERMANOVA (permutational multivariate analysis of variance) with phage type as the grouping factor and 999 permutations to generate a p-value and F-statistic testing the null hypothesis that phage type does not affect metabolite composition. Generate non-metric multidimensional scaling (NMDS) ordination using the same distance metric to visualize sample clustering by phage type. Compare the reported PERMANOVA p-value against the significance threshold α = 0.05; p < 0.05 indicates statistically significant phage-type effect on metabolite content. Export PERMANOVA results (p-value, F-statistic, R²) and NMDS coordinates as CSV files for downstream interpretation and figure generation.

## Related tools

- **MetaboDirect** (Command-line pipeline for pre-processing FT-ICR MS peak intensities, normalization, and export to formats compatible with PERMANOVA; accepts raw peak tables and performs filtering, intensity normalization, and molecular formula annotation prior to statistical analysis.) — https://github.com/Coayala/MetaboDirect
- **vegan (R package)** (Implements vegdist function for distance matrix calculation (Bray-Curtis, Euclidean, Jaccard) and adonis function for PERMANOVA execution with permutation testing.)
- **R** (Statistical computing environment (version 4.0.2 or above) required to execute vegan functions and generate NMDS ordination plots.)
- **Python** (Optional scripting language (3.8 or above) for data wrangling, metadata merging, and post-processing of PERMANOVA and NMDS output files.)

## Examples

```
# In R: Load normalized intensities and metadata, calculate Bray-Curtis distances, and execute PERMANOVA
library(vegan); D <- vegdist(normalized_intensities, method="bray"); permanova_result <- adonis2(D ~ phage_type, data=metadata, permutations=999); nmds <- metaMDS(D, k=2, trymax=20); plot(nmds, type="text", display="sites", col=as.factor(metadata$phage_type))
```

## Evaluation signals

- PERMANOVA p-value is reported and compared against α = 0.05 threshold; significance confirms that phage type explains significant variance in metabolite composition.
- F-statistic and R² (effect size) are positive and reported in results table; R² value indicates the proportion of total variance explained by phage-type factor (expected range 0.05–0.30 for biotic treatment effects on exometabolomes).
- NMDS ordination plot shows visual clustering/separation of samples by phage type along at least one axis; sample overlap between control and phage-treatment groups should be minimal if p < 0.05.
- Distance matrix has no missing or infinite values; Bray-Curtis values fall within [0, 1]; Euclidean distances are non-negative and symmetric.
- Reproducibility check: re-running PERMANOVA with 999 permutations on the same normalized intensities and metadata yields the same p-value (within rounding) and similar F-statistic and R² values across independent runs.

## Limitations

- PERMANOVA assumes that samples are independent replicates; if bacterium-phage pairs are pseudo-replicates (e.g., technical replicates from the same culture), p-values will be anti-conservative and phage-type effect may be overstated.
- Peak intensity normalization method (e.g., total ion count, median, quantile) affects distance calculations and can influence PERMANOVA results; sensitivity to normalization choice should be assessed if results are borderline (p near 0.05).
- NMDS ordination stress value is not reported in the task description; high stress (> 0.20) indicates poor 2D representation of high-dimensional distances, and additional NMDS axes or alternative ordinations (PCA, t-SNE) may be warranted.
- MetaboDirect does not provide raw spectra data preprocessing, so input peak tables must be pre-processed by external software (e.g., Fourier transform, peak picking, baseline correction) before MetaboDirect normalization and PERMANOVA analysis.
- PERMANOVA tests the hypothesis that the centroid or dispersion of phage-type groups differs, but cannot distinguish which individual metabolites drive the difference; post-hoc univariate tests (e.g., Welch's t-test per peak) are needed to identify discriminatory peaks.

## Evidence

- [results] PERMANOVA analysis of the bacterium-phage dataset shows that phage type produces a significant difference in metabolite content with p < 0.05, as displayed in Supplementary Fig. 7C.: "PERMANOVA analysis of the bacterium-phage dataset shows that phage type produces a significant difference in metabolite content with p < 0.05"
- [methods] Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities.: "Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package on normalized intensities"
- [methods] Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations.: "Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations"
- [methods] Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes.: "Generate non-metric multidimensional scaling (NMDS) ordination using the selected distance metric and export NMDS scores as a scatterplot with first two components as axes"
- [intro] MetaboDirect pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules"
