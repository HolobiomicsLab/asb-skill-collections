---
name: peak-abundance-normalization
description: Use when after peak detection and before any comparative analysis (e.g., diversity indices, ordination, or statistical testing) when working with direct injection FT-ICR MS data where raw peak intensities vary across samples due to instrumental factors. The task_id=task_005 example applies it to S.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MetaboDirect
  - vegan
  - SYNCSA
  - pmartR
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-abundance-normalization

## Summary

Normalize peak intensity values across FT-ICR MS samples to correct for instrumental variation and enable fair comparison of molecular composition between samples. This is a critical preprocessing step that standardizes the abundance matrix before downstream chemodiversity or multivariate statistical analysis.

## When to use

Apply this skill after peak detection and before any comparative analysis (e.g., diversity indices, ordination, or statistical testing) when working with direct injection FT-ICR MS data where raw peak intensities vary across samples due to instrumental factors. The task_id=task_005 example applies it to S. fallax leachate samples where inoculated and control groups must be rendered comparable via sum-normalization before computing Shannon diversity, Gini-Simpson, and Rao's quadratic entropy metrics.

## When NOT to use

- Raw FT-ICR MS spectra have not yet undergone signal processing and molecular formula assignment — use MetaboDirect's upstream preprocessing and formula assignment steps first.
- Peak intensity data is already in normalized or log-transformed form — re-normalizing may distort downstream metrics.
- Your analysis goal is to preserve absolute quantitative differences (e.g., absolute metabolite concentrations) rather than relative composition — sum-normalization removes magnitude information.

## Inputs

- Peak-abundance matrix (CSV format: peaks as rows, samples as columns, raw intensity values)
- Sample metadata file (CSV) with sample identifiers and grouping variables (e.g., inoculation status)

## Outputs

- Sum-normalized peak-abundance matrix (CSV: peaks as rows, samples as columns, relative proportions per sample)
- Normalized abundance values suitable for downstream diversity and statistical analysis

## How to apply

Load the peak-abundance matrix in CSV format with peaks as rows and samples as columns. Apply MetaboDirect's sum-normalization function, which standardizes raw peak intensities within each sample by dividing each peak's intensity by the sum of all peak intensities in that sample. This converts absolute abundances to relative proportions, removing scale bias introduced by varying sample amounts or ionization efficiency. After normalization, the sum of all peak abundances per sample equals 1.0 or 100%, enabling fair cross-sample comparison. Proceed to diversity metrics (Shannon index, Chao1, Rao's quadratic entropy) or ordination methods (PCA, NMDS) on the normalized matrix.

## Related tools

- **MetaboDirect** (Pipeline providing the sum-normalization function and encompassing pre-processing, diagnostics, and chemodiversity analysis) — https://github.com/Coayala/MetaboDirect
- **vegan** (R package for computing abundance-based diversity metrics (Shannon, Gini-Simpson, Chao1) on normalized peak intensities)
- **SYNCSA** (R package for computing functional diversity (Rao's quadratic entropy) using trait-based decomposability and aromaticity from normalized abundance data)
- **pmartR** (R package for normalization tests to validate choice of normalization method)

## Evaluation signals

- Sum of normalized peak abundances per sample equals 1.0 (or 100% if expressed as percentages) — verify no sample has total < 0.99 or > 1.01.
- All normalized peak intensity values fall in the range [0, 1] with no negative or >1 values.
- Relative ranking of peaks within a sample is preserved (if peak A was more abundant than peak B before normalization, it remains so after).
- Diversity indices computed on the normalized matrix (Shannon, Gini-Simpson, Chao1) fall within expected biological ranges for the sample type (e.g., S. fallax leachate typically yields 1000–2000 detected peaks).
- Downstream ordination plots (PCA, NMDS) or statistical comparisons (PERMANOVA) between inoculated and control groups show expected grouping patterns consistent with the research hypothesis.

## Limitations

- Sum-normalization removes absolute quantitative differences; if absolute metabolite amounts or stoichiometry matter for your interpretation, consider alternative normalization (e.g., internal standard scaling) or retain both raw and normalized matrices.
- MetaboDirect does not perform raw spectra preprocessing; normalization assumes input peak-abundance matrix has already been extracted from processed FT-ICR MS spectra with molecular formula assignment.
- Normalization may amplify noise in low-abundance peaks (rare metabolites with low signal-to-noise ratios become relatively inflated when dividing by small totals); filtering low-abundance peaks before normalization is often beneficial.
- Sum-normalization assumes that total ionizable signal per sample is comparable; severe ion suppression or enhancement specific to certain peaks may not be fully corrected and should be evaluated during diagnostics step.

## Evidence

- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [other] Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function.: "Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function."
- [other] Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities.: "Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities."
- [methods] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
