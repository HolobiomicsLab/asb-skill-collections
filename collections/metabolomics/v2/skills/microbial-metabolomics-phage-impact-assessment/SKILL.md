---
name: microbial-metabolomics-phage-impact-assessment
description: 'Use when you have normalized peak intensities (with assigned molecular
  formulas) from FT-ICR MS analysis of treated and control bacterial samples (or environmental
  microbial communities), grouped by two or more treatment factors (e.g., phage type:
  HP1, HS2, control;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0757
  tools:
  - vegan
  - MetaboDirect
  - R
  - R (prcomp, ggplot2)
  - FT-ICR MS
  techniques:
  - direct-infusion-MS
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

# microbial-metabolomics-phage-impact-assessment

## Summary

Assess whether phage infection (or other treatments) produces statistically significant shifts in bacterial metabolite composition using distance-based multivariate analysis (PERMANOVA) on FT-ICR MS peak intensities. This skill detects subtle metabolic differences that ordination methods alone may miss, enabling interpretation of how external stressors alter microbial organic matter production.

## When to use

You have normalized peak intensities (with assigned molecular formulas) from FT-ICR MS analysis of treated and control bacterial samples (or environmental microbial communities), grouped by two or more treatment factors (e.g., phage type: HP1, HS2, control; incubation time), and you need to test whether treatment groups differ significantly in their aggregate metabolite composition despite visual clustering being unclear or absent in ordination plots.

## When NOT to use

- Peak intensities have not been normalized or quality-filtered (PERMANOVA assumes comparable sampling effort across samples; unnormalized data violates distributional assumptions)
- Sample size is very small (n < 3 per group) or severely unbalanced, making permutation tests unreliable
- You are testing a single categorical variable with only two levels — a simpler univariate or pairwise distance test may be more appropriate

## Inputs

- Normalized peak intensity matrix (.csv) from MetaboDirect pre-processing with assigned molecular formulas
- Sample metadata table with treatment factor columns (phage type, incubation time, replicate ID)
- Molecular formula assignments (elemental composition) for each peak

## Outputs

- PERMANOVA results table (.csv): factors, F-statistics, R² values, p-values, degrees of freedom
- Bray-Curtis distance matrix (.csv or R object)
- NMDS ordination scores (.csv) with NMDS stress value and sample coordinates
- PCA biplot (.png/.pdf) with scree plot and sample loadings
- Scatter plots (.png/.pdf) of NMDS and PCA scores annotated by treatment group

## How to apply

Load normalized peak intensities from MetaboDirect output (.csv) and calculate Bray-Curtis distance matrices on intensity values grouped by treatment factors using the vegan package vegdist function. Run PERMANOVA (adonis function in vegan) on the distance matrix to test each factor (phage type, time) for statistical significance, recording F-statistics, R² effect sizes, and permutation p-values (α < 0.05). Compute NMDS and PCA in parallel to visualize sample ordination; if ordination fails to discriminate groups but PERMANOVA is significant (p < 0.05), this indicates subtle but statistically real metabolic shifts. Export PERMANOVA results as a summary table (factors, statistics, p-values) and generate scatter plots of NMDS/PCA scores colored by treatment group. This workflow leverages the sensitivity of distance-based tests to detect multivariate differences even when individual metabolites show small effect sizes.

## Related tools

- **vegan** (Computes Bray-Curtis distance matrices (vegdist) and performs PERMANOVA multivariate hypothesis testing (adonis function); core statistical framework for distance-based analysis)
- **MetaboDirect** (Pre-processes FT-ICR MS raw data, assigns molecular formulas, normalizes peak intensities, and outputs the filtered .csv intensity matrix fed into distance calculations) — https://github.com/Coayala/MetaboDirect
- **R (prcomp, ggplot2)** (Performs PCA on molecular composition/thermodynamic indices and generates publication-ready ordination scatter plots with treatment groupings)
- **FT-ICR MS** (High-resolution mass spectrometry instrument that generates the raw mass spectral data and enables ultra-high mass accuracy formula assignment (< 0.5 ppm error) for thousands of peaks)

## Examples

```
# R code: library(vegan); D <- vegdist(normalized_intensities, method='bray'); perm_result <- adonis(D ~ phage_type + incubation_time, data=metadata, permutations=999); nmds <- metaMDS(D, k=2, trymax=100); plot(nmds, type='n'); points(nmds, display='sites', col=as.numeric(metadata$phage_type))
```

## Evaluation signals

- PERMANOVA p-value < 0.05 for the treatment factor of interest, with R² > 0.05 (effect size at least 5% of total variance explained)
- Permutation test converges (Monte Carlo replicates do not warn of insufficient unique permutations; typically ≥ 999 permutations performed)
- NMDS stress value is < 0.20 (indicating acceptable 2D ordination quality); if stress is high but PERMANOVA is significant, document that metabolic differences are real but not visually obvious
- Bray-Curtis distance matrix is symmetric, non-negative, and has zero diagonal (distance from a sample to itself is 0); matrix dimensions match number of samples
- Treatment group means in NMDS/PCA space show separation or tight clustering that is proportional to the PERMANOVA effect size and p-value (visual and statistical results should be concordant or explicitly reconciled)

## Limitations

- PERMANOVA on Bray-Curtis distances can be sensitive to differences in within-group multivariate spread, not just location; verify homogeneity of dispersion (betadisper function in vegan) to rule out false positives driven by variance differences rather than true group shifts
- FT-ICR MS cannot separate chemical isomers and may suffer ion suppression or enhancement, meaning some metabolite presence/absence calls are ambiguous; peak intensities reflect ionization efficiency as much as absolute abundance
- Ordination plots (NMDS, PCA) may fail to visualize subtle metabolic differences detected by PERMANOVA, making biological interpretation difficult; metabolites driving significant differences may need to be identified via post-hoc univariate or effect-size analysis
- Results are specific to the normalized intensity values output by MetaboDirect; different pre-processing parameters (m/z filtering, isotope handling, normalization scheme) can alter distance matrices and significance thresholds
- PERMANOVA permutation test assumes exchangeability of samples under the null hypothesis; if samples are pseudo-replicated (e.g., multiple technical replicates from the same biological replicate treated as independent), p-values will be biased downward

## Evidence

- [other] PERMANOVA analysis of the bacterium-phage dataset revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05), while NMDS and PCA ordination analyses were unable to discriminate among sample groups, suggesting the differences are subtle.: "PERMANOVA analysis...revealed that phage type (HP1, HS2, or control) produced statistically significant differences in metabolite/organic compound content (p < 0.05), while NMDS and PCA ordination"
- [other] Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities, grouping by phage treatment (uninfected, HP1, HS2) and incubation time. Perform PERMANOVA using adonis function in vegan to test for significant differences between treatment groups, generating F-statistics, R² values, and p-values for each factor (phage type and time).: "Calculate Bray-Curtis distance matrices using the vegan package vegdist function on normalized intensities...Perform PERMANOVA using adonis function in vegan to test for significant differences"
- [methods] peak intensities are normalized in this step based on the user's input: "peak intensities are normalized in this step based on the user's input"
- [methods] detected peaks are filtered by their m/z values (based on the user's input), isotopic presence (13C peaks), error in formula assignment (0.5 ppm), and based on the number of samples that they are present in (threshold determined by the user): "detected peaks are filtered by their m/z values...isotopic presence (13C peaks), error in formula assignment (0.5 ppm), and based on the number of samples that they are present in"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: vegan, tidyverse, RColorBrewer: "MetaboDirect requires Python (3.5 and above), R (4 and above)...vegan"
- [intro] Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers, lack of fine resolving power, and signal suppression or enhancement from ion suppression: "Even though DI-MS has ample coverage and can detect a wide range of compounds...some drawbacks are its inability to separate chemical isomers, lack of fine resolving power, and signal suppression or"
