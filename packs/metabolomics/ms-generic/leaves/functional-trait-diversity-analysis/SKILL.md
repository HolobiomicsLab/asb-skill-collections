---
name: functional-trait-diversity-analysis
description: Use when when you have abundance-normalized FT-ICR MS peak data with
  assigned molecular formulas and need to distinguish between richness (total number
  of distinct metabolites) and functional diversity (diversity in metabolic potential).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - MetaboDirect
  - vegan
  - SYNCSA
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# functional-trait-diversity-analysis

## Summary

Quantifies functional diversity of molecular metabolites by integrating trait-based metrics (elemental composition, decomposability, aromaticity/unsaturation) into entropy calculations, revealing how microbial inoculation alters not just metabolite richness but the functional repertoire of decomposable and reactive species.

## When to use

When you have abundance-normalized FT-ICR MS peak data with assigned molecular formulas and need to distinguish between richness (total number of distinct metabolites) and functional diversity (diversity in metabolic potential). Apply this skill when your research question specifically asks whether an experimental treatment (e.g., microbial inoculation) changes both the breadth of metabolites AND their functional capacity for decomposition, reactivity, or aromaticity—not just presence/absence.

## When NOT to use

- Input peak data has not been sum-normalized or lacks abundance values; functional diversity requires weighted trait integration and cannot be computed on presence/absence matrices alone.
- Molecular formulas have not been assigned or elemental composition is unavailable; Rao's quadratic entropy requires trait values for each peak.
- Research question only asks whether total metabolite count differs between treatments; abundance-based richness metrics (Chao1) are sufficient and simpler than functional diversity.
- Sample size is very small (n < 3 per group); statistical grouping and comparison of diversity distributions become unreliable.

## Inputs

- Peak-abundance matrix (CSV: peaks as rows, samples as columns, sum-normalized intensities)
- Sample metadata with grouping variable (e.g., inoculation status: inoculated/control)
- Assigned molecular formula data with elemental composition (C, H, N, O, S counts)
- Trait matrix or calculation rules for decomposability indices and aromaticity/unsaturation scores per peak

## Outputs

- Abundance-based diversity indices per sample (Shannon index, Gini-Simpson index, Chao1 richness)
- Functional diversity index per sample (Rao's quadratic entropy)
- Box plots comparing richness and functional diversity grouped by experimental factor
- CSV tables of diversity metric values and statistical summaries (mean, SD, p-value by group)

## How to apply

Begin with sum-normalized peak-abundance matrix (peaks as rows, samples as columns, intensities normalized by sample totals). Extract elemental composition (C, H, N, O, S counts), decomposability indices, and aromaticity/unsaturation traits from assigned molecular formulas for each peak. Calculate abundance-based diversity metrics (Shannon, Gini-Simpson, Chao1) using vegan package functions on normalized peak intensities to quantify metabolite richness. Then calculate Rao's quadratic entropy (functional diversity) using SYNCSA package, incorporating the trait matrix (elemental composition, decomposability, aromaticity) weighted by peak abundances. Group samples by experimental factor (e.g., inoculation status: inoculated vs. control) and compare richness vs. functional diversity distributions; divergence between these metrics indicates that inoculation increased metabolite diversity but concentrated functional capacity (decreased functional evenness across traits).

## Related tools

- **vegan** (Computes abundance-based diversity indices (Shannon, Gini-Simpson, Chao1) on normalized peak intensities)
- **SYNCSA** (Calculates Rao's quadratic entropy (functional diversity) by integrating trait matrix (elemental composition, decomposability, aromaticity) weighted by peak abundances)
- **MetaboDirect** (Pre-processes FT-ICR MS peak data: sum-normalization, molecular formula assignment, and chemodiversity analysis pipeline) — https://github.com/Coayala/MetaboDirect

## Examples

```
# In R, after loading normalized peak-abundance matrix and trait data:
shannon <- vegan::diversity(t(peak_matrix), index='shannon')
rao_entropy <- SYNCSA::rao(comm=t(peak_matrix), traits=trait_matrix, phylogenetic=FALSE)
boxplot(shannon ~ inoculation_status, data=metadata); boxplot(rao_entropy ~ inoculation_status, data=metadata)
```

## Evaluation signals

- Richness indices (Shannon, Chao1) are higher in inoculated samples; functional diversity (Rao's entropy) is lower, confirming divergence between metabolite abundance and functional breadth.
- Box plots show non-overlapping distributions or statistically significant difference (e.g., p < 0.05 by Wilcoxon test) between inoculated and control groups for at least one metric pair.
- Trait values (elemental composition, decomposability, aromaticity) are present and vary across peaks; functional diversity should differ from richness only if trait variance exists.
- CSV output tables include all samples, named diversity metrics, grouping variable values, and summary statistics (mean, SD per group); no missing or zero-valued metrics.
- Rao's entropy calculation is transparent: verify that it weights peaks by their normalized abundance and incorporates pairwise trait distances between metabolites, not just trait presence.

## Limitations

- FT-ICR MS cannot separate chemical isomers; peaks with identical m/z may represent different functional compounds, inflating or distorting functional diversity estimates.
- Decomposability and aromaticity indices are inferred computationally from elemental formulas; they are proxies for true metabolic reactivity and may not fully capture enzymatic accessibility or bioavailability in microbial communities.
- SYNCSA and vegan assume that trait values and abundances are properly scaled and that samples are independent; strong autocorrelation or unequal library sizes can bias diversity comparisons.
- MetaboDirect does not provide raw spectra preprocessing; peak detection, deisotoping, and formula assignment errors upstream propagate into functional diversity calculations.
- Small sample size (e.g., n = 4 as in the S. fallax data set) limits statistical power for group comparisons; results should be interpreted as exploratory rather than confirmatory.

## Evidence

- [other] Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities.: "Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities."
- [other] Calculate functional-based diversity (Rao's quadratic entropy) using SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected peaks.: "Calculate functional-based diversity (Rao's quadratic entropy) using SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected"
- [other] Inoculation of S. fallax leachate with microorganisms increased metabolite richness but decreased functional diversity, suggesting that inoculated samples contained more diverse metabolites overall but were less diverse in terms of decomposability, reactivity, aromaticity, and elemental composition.: "Inoculation of S. fallax leachate with microorganisms increased metabolite richness but decreased functional diversity, suggesting that inoculated samples contained more diverse metabolites overall"
- [other] Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function.: "Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function."
- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: ... vegan ... SYNCSA ...: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: ... vegan ... SYNCSA ..."
- [intro] fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets: "fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets"
