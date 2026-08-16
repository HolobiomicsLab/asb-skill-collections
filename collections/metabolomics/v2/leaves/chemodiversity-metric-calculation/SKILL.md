---
name: chemodiversity-metric-calculation
description: Use when when you have sum-normalized peak-abundance matrices from FT-ICR
  MS data with assigned molecular formulas and need to compare metabolite diversity
  between treatment groups (e.g., inoculated vs. control samples).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0621
  tools:
  - MetaboDirect
  - vegan
  - SYNCSA
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
- diversity metrics using functions from the R packages vegan [63]
- diversity metrics using functions from the R packages vegan
- diversity metrics using functions from the R packages vegan [63] and SYNCSA [64]
- diversity metrics using functions from the R packages vegan [63] and SYNCSA
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

# chemodiversity-metric-calculation

## Summary

Calculate abundance-based and functional-based diversity metrics on filtered FT-ICR MS peak matrices to quantify metabolite richness and functional trait diversity in environmental or experimental samples. This skill enables comparative assessment of how treatments (e.g., microbial inoculation) shift both the number of distinct metabolites and their decomposability, aromaticity, and elemental composition profiles.

## When to use

When you have sum-normalized peak-abundance matrices from FT-ICR MS data with assigned molecular formulas and need to compare metabolite diversity between treatment groups (e.g., inoculated vs. control samples). Use this skill when your research question requires separating metabolite richness (total number of peaks) from functional diversity (diversity in decomposability, aromaticity, or elemental composition traits). Trigger: presence of both abundance data and functional trait assignments (e.g., via MetaboDirect outputs or similar pipelines).

## When NOT to use

- Peak abundance matrix is not sum-normalized or uses non-comparable normalization methods across samples (e.g., log-transformation without adjustment for baseline); diversity metrics require quantitative comparability of absolute intensities.
- Peaks have not been assigned molecular formulas or functional traits; abundance-based metrics can proceed, but functional diversity (Rao's entropy) requires trait data and will produce uninformative results without it.
- Input is already a pre-computed diversity matrix or a single aggregate diversity score per sample; this skill is for de novo calculation from raw abundance data.

## Inputs

- Sum-normalized peak-abundance matrix (CSV format: peaks as rows, samples as columns, values are normalized intensities)
- Sample metadata file with grouping variable (e.g., inoculation status: 'inoculated' vs. 'control')
- Peak trait table with elemental composition, decomposability index, and aromaticity/unsaturation estimates (one row per peak)

## Outputs

- Box plots or violin plots of diversity indices stratified by treatment group
- CSV table of abundance-based diversity metrics (Shannon, Gini-Simpson, Chao1) per sample
- CSV table of functional diversity metrics (Rao's quadratic entropy) per sample
- Statistical summary table with group means, standard deviations, and p-values from group comparisons
- Interpretation table linking diversity shifts to hypothesized mechanisms (e.g., inoculation increased metabolite richness but homogenized functional traits)

## How to apply

Load sum-normalized peak-abundance matrices (peaks as rows, samples as columns) and sample metadata with treatment grouping variables into R. Calculate abundance-based diversity indices (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions applied to normalized peak intensities. In parallel, assign functional traits (elemental composition, decomposability indices, aromaticity/unsaturation) to each peak from MetaboDirect outputs or external trait databases. Calculate functional diversity using SYNCSA package's Rao's quadratic entropy, which incorporates both abundance and pairwise trait distances. Group all indices by treatment variable and generate box plots or summary statistics stratified by group. Export metric values, p-values from Mann-Whitney U or Kruskal-Wallis tests, and effect sizes as CSV tables for comparison.

## Related tools

- **MetaboDirect** (Generates normalized peak-abundance matrices, assigns molecular formulas, computes elemental composition and aromaticity traits, and automates chemodiversity analysis calculations; used to produce input data and optionally execute diversity metric steps) — https://github.com/Coayala/MetaboDirect
- **vegan** (R package providing Shannon diversity index, Gini-Simpson index, and Chao1 richness estimator functions for abundance-based diversity calculations)
- **SYNCSA** (R package for computing Rao's quadratic entropy and other trait-based diversity indices by incorporating pairwise trait distances and sample abundances)

## Examples

```
# In R: Load normalized peak matrix, assign sample groups, compute diversity indices
set.seed(123)
library(vegan)
library(SYNCSA)
peaks <- read.csv('peaks_normalized.csv', row.names=1)
metadata <- read.csv('samples_metadata.csv', row.names=1)
shannon <- diversity(t(peaks), index='shannon')
gini_simpson <- diversity(t(peaks), index='simpson')
chao1 <- estimateR(t(peaks))['Chao1', ]
# For functional diversity: assign traits to peaks, then use SYNCSA::rao
traits <- read.csv('peak_traits.csv', row.names=1)
rao_div <- rao(comm=t(peaks), traits=as.matrix(traits))
results <- data.frame(sample=rownames(peaks), shannon, gini_simpson, rao=rao_div, group=metadata[rownames(peaks),'treatment'])
write.csv(results, 'diversity_metrics.csv')
```

## Evaluation signals

- Diversity metric values are positive and fall within expected ranges for each index type (Shannon typically 0–5; Gini-Simpson 0–1; Chao1 ≥ observed richness; Rao's entropy ≥ 0).
- Box plots or group summary statistics show visual or statistical separation between treatment groups (e.g., inoculated vs. control) with non-overlapping confidence intervals or significant p-values (α = 0.05) from Mann-Whitney U or Kruskal-Wallis tests.
- Interpretation is consistent with the research question and prior findings: e.g., if the hypothesis predicts increased metabolite richness but decreased functional diversity in inoculated samples, both abundance-based and functional metrics should align with this pattern.
- Exported CSV tables contain no missing values, zero-variance rows, or anomalous negative abundances; row and column counts match input matrix dimensions.
- Reproducibility check: running the same R script on the same input files produces identical numeric outputs (bit-identical diversity metric values and p-values).

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; peak-abundance matrices must be pre-processed (e.g., deisotoping, noise filtering, formula assignment) by upstream software before input to this skill.
- Chemodiversity metrics assume independence of peaks; co-eluting isomers or overlapping m/z features will bias abundance estimates and inflate richness metrics.
- Rao's quadratic entropy results depend critically on the choice and accuracy of functional trait assignments; if aromaticity or decomposability indices are inaccurate or incomplete, functional diversity comparisons may be misleading.
- Small sample sizes (< 4 samples per group) reduce statistical power and increase sensitivity to outliers; the S. fallax leachate dataset consisted of only 4 samples, limiting inference strength.
- The skill does not account for unequal sequencing/measurement depth across samples; if one sample has systematically lower peak detection rates, rarefaction or other depth-normalization corrections may be necessary before diversity comparison.

## Evidence

- [other] Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities.: "Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities."
- [other] Calculate functional-based diversity (Rao's quadratic entropy) using SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected peaks.: "Calculate functional-based diversity (Rao's quadratic entropy) using SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected"
- [other] Inoculation of S. fallax leachate with microorganisms increased metabolite richness but decreased functional diversity, suggesting that inoculated samples contained more diverse metabolites overall but were less diverse in terms of decomposability, reactivity, aromaticity, and elemental composition.: "Inoculation of S. fallax leachate with microorganisms increased metabolite richness but decreased functional diversity, suggesting that inoculated samples contained more diverse metabolites overall"
- [other] Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function.: "Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function."
- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: [vegan, SYNCSA, tidyverse, RColorBrewer, etc.]: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
