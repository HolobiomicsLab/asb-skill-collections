---
name: metabolite-distance-metric-calculation
description: Use when you have normalized peak intensity tables from FT-ICR MS data
  (or MetaboDirect pre-processed .csv output) with samples grouped by experimental
  treatments (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3960
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - vegan
  - MetaboDirect
  - R
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- calculate diversity metrics using functions from the R packages vegan [63] and SYNCSA
  [64]
- using functions from the R packages vegan [63]
- Molecular transformation networks for each sample (mass difference network-based
  approach) are generated in this step
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-distance-metric-calculation

## Summary

Calculate Bray-Curtis distance matrices from normalized FT-ICR MS peak intensity data to quantify compositional dissimilarity between metabolomic samples. This distance metric is the prerequisite for ordination (NMDS, PCA) and permutation-based multivariate testing (PERMANOVA) to detect phage-type or treatment-driven shifts in metabolite content.

## When to use

Apply this skill when you have normalized peak intensity tables from FT-ICR MS data (or MetaboDirect pre-processed .csv output) with samples grouped by experimental treatments (e.g., phage type, incubation time, environmental condition) and you need to test whether treatment groups have statistically significant differences in overall metabolite composition. Bray-Curtis is indicated when samples contain count-like or intensity data, absent values should be treated as zero, and you want a metric sensitive to changes in relative abundance.

## When NOT to use

- Input is a phylogenetic community table with abundance data already aggregated by taxonomy — use UniFrac or phylogenetic distance instead.
- Distance matrix has already been computed; re-computing adds no analytical value.
- Samples contain binary presence/absence data (1/0) only — consider Jaccard or Sørensen dissimilarity instead.
- Metabolite intensities have not been normalized or log-transformed; raw counts or disparate scales will bias Bray-Curtis.

## Inputs

- Normalized peak intensity table (CSV): rows=metabolites with molecular formula assignments, columns=samples, values=normalized intensities
- Sample metadata: treatment groupings (phage type: HP1, HS2, control; incubation time; etc.)
- Pre-processed MetaboDirect output with intensity normalization applied

## Outputs

- Bray-Curtis distance matrix (symmetric, numeric): pairwise compositional dissimilarities between all samples
- Distance matrix suitable for NMDS ordination, PCA biplots, and PERMANOVA input

## How to apply

Load the normalized peak intensity matrix (rows = metabolites with assigned molecular formulas, columns = samples) from MetaboDirect pre-processed output. Use the vegan R package vegdist() function with method='bray' to compute pairwise Bray-Curtis distances, grouping samples by treatment factors (phage type, time point, etc.). The Bray-Curtis dissimilarity d_ij = Σ|x_ik − x_jk| / Σ(x_ik + x_jk) over all metabolites k, yielding a symmetric distance matrix. Retain the full distance matrix as input to downstream ordination (NMDS, PCA) and permutation tests (PERMANOVA adonis). The rationale: Bray-Curtis emphasizes abundant metabolites and is robust to sparse or absent signals typical of mass spectrometry metabolomics.

## Related tools

- **vegan** (R package providing vegdist() function to compute Bray-Curtis dissimilarity matrices and adonis() for PERMANOVA)
- **MetaboDirect** (Command-line pipeline for FT-ICR MS data pre-processing, filtering, normalization, and output as normalized intensity .csv suitable for distance calculation) — https://github.com/Coayala/MetaboDirect
- **R** (Statistical computing environment required to run vegan vegdist and downstream ordination/PERMANOVA)

## Examples

```
library(vegan); D <- vegdist(normalized_intensities, method='bray'); permanova_result <- adonis(D ~ phage_type + time, data=metadata, permutations=999)
```

## Evaluation signals

- Distance matrix is symmetric (d_ij = d_ji) and has zero diagonal (d_ii = 0).
- All pairwise distances fall in the valid range [0, 1] for Bray-Curtis dissimilarity.
- Samples within the same treatment group (e.g., HP1 replicates) show lower median distances than samples across treatment groups, indicating treatment effect is detectable.
- PERMANOVA adonis() produces significant p-values (p < 0.05) for treatment factors when applied to the distance matrix, consistent with the article's finding.
- NMDS or PCA performed on the distance matrix produces ordination stress values and separation patterns that correlate with treatment assignments.

## Limitations

- Bray-Curtis is sensitive to rare metabolites and absent signals (zeros); sparse or highly skewed intensity distributions may reduce statistical power.
- The metric assumes metabolite intensities are on a comparable scale; unequal normalization across samples or batches will bias distances.
- Bray-Curtis cannot distinguish chemical isomers; FT-ICR MS lacks chromatographic separation, so isobaric compounds are indistinguishable in the distance calculation.
- The article notes that NMDS and PCA ordination were unable to visualize treatment group separation despite PERMANOVA significance, suggesting distances among groups are subtle; ordination plots alone may be misleading.
- Distance-based approaches discard the identity and biological meaning of individual metabolites; complementary feature-level or compound-class analysis is needed to interpret which metabolites drive treatment differences.

## Evidence

- [other] Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time.: "Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time."
- [other] PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05), while NMDS and PCA ordination analyses were unable to discriminate among sample groups: "PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05)"
- [methods] peak intensities are normalized in this step based on the user's input: "peak intensities are normalized in this step based on the user's input"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above): "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"
