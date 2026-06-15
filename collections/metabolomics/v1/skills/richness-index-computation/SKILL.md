---
name: richness-index-computation
description: Use when you have a normalized peak-abundance matrix from FT-ICR MS data (peaks as rows, samples as columns) and need to compare the number and diversity of detected molecular species across experimental conditions—for example, to test whether inoculation or environmental perturbation alters the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - MetaboDirect
  - vegan
  - SYNCSA
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- diversity metrics using functions from the R packages vegan [63]
- diversity metrics using functions from the R packages vegan
- diversity metrics using functions from the R packages vegan [63] and SYNCSA [64]
- diversity metrics using functions from the R packages vegan [63] and SYNCSA
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

# richness-index-computation

## Summary

Compute abundance-based metabolite richness metrics (Chao1, Shannon, Gini-Simpson) from normalized peak-intensity matrices to quantify the diversity of detected molecular species in metabolomic samples. This skill enables comparison of metabolite richness across treatment groups or sample conditions.

## When to use

Apply this skill when you have a normalized peak-abundance matrix from FT-ICR MS data (peaks as rows, samples as columns) and need to compare the number and diversity of detected molecular species across experimental conditions—for example, to test whether inoculation or environmental perturbation alters the richness of metabolites detected in natural organic matter or biological samples.

## When NOT to use

- Data has not been sum-normalized—apply normalization before richness computation to account for total signal variation across samples.
- Peak-abundance matrix contains unfiltered raw peaks—first apply filtering by m/z range, isotopic presence (13C), formula assignment error threshold (0.5 ppm), and sample occupancy (user-defined threshold) to reduce spurious features.
- You need functional diversity metrics that incorporate chemical properties (decomposability, aromaticity, elemental composition)—use Rao's quadratic entropy with SYNCSA package instead, which accounts for trait-based functional differences among peaks.

## Inputs

- Peak-abundance matrix (CSV: peaks as rows, samples as columns, raw peak intensities)
- Sample metadata with experimental grouping variable (CSV, e.g., inoculation status)
- Filtered and assigned molecular formula data from FT-ICR MS preprocessing

## Outputs

- Chao1 richness index values (per-sample estimates and group summaries)
- Shannon diversity index values (per-sample and group means)
- Gini-Simpson index values (per-sample and group means)
- Box plots comparing richness indices across experimental groups (PNG/PDF)
- CSV table of all richness metric values with group assignments and statistical summaries

## How to apply

Load the filtered peak-abundance matrix (CSV format, peaks as rows, samples as columns) from your FT-ICR MS preprocessing pipeline. Apply sum-normalization to raw peak intensities across each sample to account for variation in total ion current. Using the vegan package (R), calculate abundance-based richness indices including the Chao1 richness estimator (which accounts for undetected rare peaks), Shannon diversity index (incorporating evenness), and Gini-Simpson index (probability that two randomly drawn peaks differ). Group all indices by your experimental variable (e.g., inoculation status) and generate box plots to visualize differences. Interpret Chao1 as a conservative estimate of total metabolite diversity, Shannon as sensitivity to dominant peaks, and Gini-Simpson as a robust measure less influenced by rare peaks. Export metric values and statistical summaries as CSV tables for downstream reporting.

## Related tools

- **vegan** (R package for calculating abundance-based richness indices (Chao1, Shannon, Gini-Simpson) from peak-intensity matrices)
- **MetaboDirect** (Command-line pipeline that orchestrates peak filtering, normalization, and chemodiversity analysis including richness index computation) — https://github.com/Coayala/MetaboDirect
- **SYNCSA** (R package for computing functional diversity (Rao's quadratic entropy) when trait-based diversity metrics are needed alongside richness)

## Examples

```
# Load normalized peak matrix and compute richness indices in R:
library(vegan);
peaks <- read.csv('filtered_peak_abundance.csv', row.names=1);
metadata <- read.csv('sample_metadata.csv', row.names=1);
chao1 <- estimateR(t(peaks))['Chao1', ];
shannon <- diversity(t(peaks), index='shannon');
ginisimpson <- diversity(t(peaks), index='simpson', MARGIN=1);
richness_df <- data.frame(sample=names(shannon), Chao1=chao1, Shannon=shannon, GiniSimpson=ginisimpson, group=metadata[names(shannon), 'inoculation_status']);
write.csv(richness_df, 'richness_indices.csv');
```

## Evaluation signals

- Richness index values are positive and fall within expected range for the number of detected peaks (Chao1 ≥ observed peak count; Shannon typically 1–5 for metabolomic data; Gini-Simpson 0–1).
- Sum of normalized peak intensities per sample equals 1.0 (or close to it), confirming proper normalization was applied before richness computation.
- Box plots show visually distinct distributions across experimental groups; statistical significance tested via PERMANOVA or Wilcoxon rank-sum test confirms group differences.
- Chao1 estimates are consistently higher than observed peak counts, reflecting correction for undetected rare species.
- Exported CSV table contains one row per sample with group labels and all three richness indices; no missing or NaN values for samples passing QC filters.

## Limitations

- Chao1 and other richness estimators assume closed (finite) species pools and may overestimate diversity if rare peaks are detection artifacts rather than true rare metabolites.
- Sum-normalization may mask absolute differences in total metabolite abundance between samples; use with caution when absolute signal intensity is biologically meaningful.
- Abundance-based richness does not account for structural or functional similarity among peaks; peaks that are isomers or minor transformations of one another are counted as separate species.
- MetaboDirect does not provide raw spectra preprocessing; richness computation depends on quality of upstream peak detection, formula assignment (0.5 ppm error threshold), and filtering steps—poor preprocessing will inflate or deflate richness estimates.

## Evidence

- [other] Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities.: "Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities."
- [other] Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function.: "Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function."
- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [intro] fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets: "fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets"
- [methods] chemodiversity analysis: "chemodiversity analysis"
- [other] Inoculation of S. fallax leachate with microorganisms increased metabolite richness but decreased functional diversity, suggesting that inoculated samples contained more diverse metabolites overall but were less diverse in terms of decomposability, reactivity, aromaticity, and elemental composition.: "Inoculation of S. fallax leachate with microorganisms increased metabolite richness but decreased functional diversity, suggesting that inoculated samples contained more diverse metabolites overall"
