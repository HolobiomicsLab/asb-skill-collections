---
name: metabolite-abundance-normalization-comparison
description: Use when you have normalized peak intensities using MetaboDirect's data preprocessing step and are preparing to perform PERMANOVA or NMDS ordination on a bacterium-phage or environmental metabolomics dataset (36+ samples).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - MetaboDirect
  - vegan (R package)
  - Python 3.8
  - R 4.0.2
  - R (4.0.2+)
  - Python (3.8+)
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-abundance-normalization-comparison

## Summary

Compare the effects of different peak intensity normalization methods on downstream multivariate statistical analysis (PERMANOVA, NMDS) of FT-ICR MS metabolomics data to ensure robust and reproducible findings. This skill validates whether normalization choice materially affects the significance and interpretation of phage-type or treatment effects on metabolite composition.

## When to use

You have normalized peak intensities using MetaboDirect's data preprocessing step and are preparing to perform PERMANOVA or NMDS ordination on a bacterium-phage or environmental metabolomics dataset (36+ samples). Apply this skill when you need to verify that your downstream statistical conclusions (e.g., p-value, effect size, ordination pattern) are stable across normalization schemes, especially before reporting a finding in a supplementary figure or manuscript.

## When NOT to use

- Input data has not yet undergone formula assignment filtering (≤ 0.5 ppm error threshold) — filter first using MetaboDirect steps 1–4.
- Sample count is below 12 per treatment group — PERMANOVA power and NMDS robustness are compromised.
- You have already committed to a single normalization method and lack access to alternative preprocessed files — comparison is impossible without re-running preprocessing.

## Inputs

- Normalized peak intensity matrix (CSV) from MetaboDirect steps 1–4 preprocessed using one normalization method
- Sample metadata with treatment/grouping factor (phage type or condition)
- Molecular formula assignments for feature annotation
- Multiple normalized datasets using alternative normalization schemes (e.g., quantile, median, total area, log-ratio)

## Outputs

- PERMANOVA results table (p-value, F-statistic, R²) for each normalization method
- NMDS ordination coordinates (CSV) for each normalization method
- NMDS scatterplot(s) with first two components, colored by treatment group
- Comparison summary: consensus findings across normalization methods or flagged sensitivity

## How to apply

Load the normalized peak intensity matrices from MetaboDirect steps 1–4 (after filtering by m/z, isotopic presence, formula assignment error ≤ 0.5 ppm, and sample prevalence threshold). Calculate pairwise distance matrices (Bray-Curtis, Euclidean, or Jaccard) using the vegan R package's vegdist function on each normalized dataset independently. Execute PERMANOVA with 999 permutations and the same grouping factor (e.g., phage type: HP1, HS2, control) for each normalization variant. Generate NMDS ordinations with the first two components and overlay the same treatment groups. Compare the resulting p-values, F-statistics, R² values, and NMDS patterns across normalization methods. A normalization method is acceptable if the p-value remains below your significance threshold (α = 0.05) and the ordination pattern (separation between treatment groups) is visually consistent; if results diverge significantly, the finding may be normalization-dependent and require sensitivity analysis or method justification.

## Related tools

- **MetaboDirect** (Preprocessing, filtering, and normalization of peak intensities prior to comparison) — https://github.com/Coayala/MetaboDirect
- **vegan (R package)** (Calculation of pairwise distances and execution of PERMANOVA with 999 permutations)
- **R (4.0.2+)** (Runtime environment for vegan, ggplot2, and NMDS ordination)
- **Python (3.8+)** (Optional: post-processing and comparison of PERMANOVA/NMDS results across methods)

## Examples

```
# In R: library(vegan); D_bc <- vegdist(norm_intensities, method='bray'); perm_result <- adonis2(D_bc ~ phage_type, data=metadata, permutations=999); nmds_ord <- metaMDS(D_bc, k=2); plot(nmds_ord, type='n'); points(nmds_ord, col=as.numeric(metadata$phage_type), pch=19)
```

## Evaluation signals

- PERMANOVA p-value direction and magnitude consistency: the p-value for the treatment factor should remain below α = 0.05 (or above, consistently) across all tested normalization methods; divergence suggests normalization-dependent results.
- NMDS ordination visual separation: treatment groups should occupy distinct or overlapping regions in ordination space consistently; if one normalization method produces tight clustering and another produces diffuse scatter, document this sensitivity.
- R² effect size agreement: the proportion of variance explained by the grouping factor should not differ by >20% between normalization methods; larger divergence indicates instability.
- Reproducibility check: re-run PERMANOVA with 999 permutations and confirm p-values are within 0.01 of the original; random seed ensures determinism.
- Distance metric agreement: if multiple metrics (Bray-Curtis, Euclidean, Jaccard) are tested, at least two should yield consistent p-value direction and ordination pattern.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; normalization comparison assumes input data have already been signal-processed and formula-assigned upstream.
- PERMANOVA assumes exchangeability of samples within groups; if strong batch effects exist (e.g., run date, instrument drift), add batch as a covariate or filter before analysis.
- NMDS is stochastic (random initialization); use a fixed seed or run multiple iterations to confirm ordination stability across normalization methods.
- Sample size and group balance matter: unequal group sizes or very small n per group (<5) can inflate Type I error; the bacterium-phage study used n=36 (balanced by treatment); scale accordingly.
- Normalization choice may be driven by study design: if you suspect ion suppression or signal enhancement in certain samples, log-ratio or quantile normalization may be more appropriate than total-area, but this is a domain decision, not a statistical one.

## Evidence

- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [other] Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations.: "Execute permutational analysis of variance (PERMANOVA) with phage type (HP1, HS2, control) as the grouping factor using 999 permutations."
- [other] Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package: "Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) using the vegdist function from the vegan R package"
- [other] PERMANOVA analysis of the bacterium-phage dataset shows that phage type produces a significant difference in metabolite content with p < 0.05, as displayed in Supplementary Fig. 7C.: "PERMANOVA analysis of the bacterium-phage dataset shows that phage type produces a significant difference in metabolite content with p < 0.05, as displayed in Supplementary Fig. 7C."
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [readme] pmartR (for normalization tests): "pmartR (for normalization tests)"
