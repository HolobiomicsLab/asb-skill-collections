---
name: diversity-visualization-by-treatment
description: Use when you have normalized peak-abundance matrices with sample metadata containing categorical treatment variables (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MetaboDirect
  - vegan
  - SYNCSA
  techniques:
  - direct-infusion-MS
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

# diversity-visualization-by-treatment

## Summary

Generate grouped box plots and statistical summaries of alpha and functional diversity metrics stratified by treatment or inoculation status in metabolomic or chemodiversity datasets. This skill enables visual and quantitative comparison of diversity trajectories across experimental conditions using abundance-based (Shannon, Gini-Simpson, Chao1) and trait-based (Rao's quadratic entropy) indices.

## When to use

You have normalized peak-abundance matrices with sample metadata containing categorical treatment variables (e.g., inoculated vs. control, time points, environmental conditions) and you need to assess whether biological interventions or environmental conditions alter both metabolite richness and functional trait diversity. Apply this skill after sum-normalization and diversity metric calculation when the research question concerns differential diversity responses across treatment groups.

## When NOT to use

- Diversity indices have not yet been calculated from the normalized peak-intensity matrix — compute them first using vegan or equivalent package functions.
- Treatment/inoculation metadata is missing or not categorical — metadata must contain discrete group labels for grouping.
- Raw FT-ICR MS spectra have not been preprocessed and molecular formula assigned — MetaboDirect requires post-assignment peak abundance and formula data as input.

## Inputs

- filtered peak-abundance matrix (CSV: peaks as rows, samples as columns, normalized by sum-normalization)
- sample metadata table with treatment/inoculation status categorical variable
- assigned molecular formula data with elemental composition
- functional trait annotations (decomposability indices, aromaticity/unsaturation values)

## Outputs

- box plots stratified by treatment group (Shannon diversity, Gini-Simpson, Chao1, Rao's quadratic entropy)
- CSV table of diversity metric values per sample
- CSV table of statistical summaries (median, quartiles, mean) per treatment group

## How to apply

First, calculate abundance-based diversity indices (Shannon diversity, Gini-Simpson, Chao1 richness) using vegan package functions on the sum-normalized peak-intensity matrix. Then compute functional-based diversity (Rao's quadratic entropy) using the SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected peaks as functional traits. Group all calculated diversity indices by the treatment/inoculation metadata variable. Generate box plots with the treatment variable as the grouping factor on the x-axis and diversity metric values on the y-axis, ensuring clear visual separation between groups. Export the raw diversity metric values and descriptive statistics (median, quartiles, mean) as CSV tables for downstream statistical testing and reporting.

## Related tools

- **MetaboDirect** (command-line pipeline for automated chemodiversity analysis and visualization of FT-ICR MS data; handles normalization, diversity calculation, and plot generation) — https://github.com/Coayala/MetaboDirect
- **vegan** (R package for calculating abundance-based diversity indices (Shannon, Gini-Simpson, Chao1) from peak-intensity matrices)
- **SYNCSA** (R package for computing functional-based diversity metrics (Rao's quadratic entropy) using elemental composition and molecular trait data)

## Examples

```
metabodirect --input peak_matrix.csv --metadata samples.csv --group_by inoculation_status --diversity_indices shannon gini_simpson chao1 --functional_traits rao_q --plot_type box --output_dir results/
```

## Evaluation signals

- Box plot visual inspection: clear separation or overlap between treatment groups consistent with the biological hypothesis (e.g., inoculated samples show higher richness but lower functional diversity).
- CSV export schema validation: diversity metric table contains one row per sample with columns for sample ID, treatment group, and each diversity index; summary table aggregates by treatment group with median, quartiles, and mean.
- Diversity index ranges are biologically plausible: Shannon diversity typically 1–5 for metabolomic datasets; Rao's quadratic entropy constrained by trait variance and group size.
- Statistical consistency: samples within the same treatment group cluster together in central tendency (median/mean) when viewed across replicates; between-group differences align with MetaboDirect's reported findings on richness vs. functional diversity trade-offs.
- Reproducibility check: running the same normalized matrix and metadata through vegan and SYNCSA functions with identical parameters produces identical diversity values in the exported CSV tables.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; molecular formula assignment must be completed upstream before diversity metrics can be computed.
- Functional trait assignment (decomposability, aromaticity, elemental composition) depends on completeness and accuracy of molecular formula annotation; peaks without assigned formulae cannot contribute to functional diversity estimates.
- Box plot visualization may become uninformative with very large numbers of treatment groups (>10); consider alternative strategies (violin plots, density plots, faceted layouts) for complex experimental designs.
- DI-MS signal suppression/enhancement effects can confound peak-intensity estimates used in abundance-based diversity metrics; this confounder is not addressed by the diversity calculation itself and must be acknowledged during interpretation.
- Treatment group sample sizes should be ≥3–4 replicates per group for robust box plot and statistical inference; very small groups (n=1–2) yield unreliable quartile and median estimates.

## Evidence

- [other] Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function.: "Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function."
- [other] Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities.: "Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities."
- [other] Calculate functional-based diversity (Rao's quadratic entropy) using SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected peaks.: "Calculate functional-based diversity (Rao's quadratic entropy) using SYNCSA package, incorporating elemental composition, decomposability indices, and aromaticity/unsaturation traits of detected"
- [other] Group all diversity indices by inoculation status (inoculated vs. control) and generate box plots with grouping variable.: "Group all diversity indices by inoculation status (inoculated vs. control) and generate box plots with grouping variable."
- [other] Export diversity metric values and statistical summaries as CSV tables.: "Export diversity metric values and statistical summaries as CSV tables."
- [abstract] MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization of a wide range of plots: "MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization of a wide range of plots"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
