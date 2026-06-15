---
name: metabolite-abundance-stratification
description: Use when you have a peak-abundance matrix from FT-ICR MS (peaks as rows, samples as columns with raw peak intensities) and need to compute abundance-based diversity indices or functional diversity metrics that are sensitive to relative vs. absolute peak heights.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# metabolite-abundance-stratification

## Summary

Stratify FT-ICR MS metabolite peaks by abundance rank and apply sample-wise sum-normalization to enable fair comparison of chemodiversity metrics across samples with varying total ion currents. This skill is essential when raw peak intensities span multiple orders of magnitude and downstream diversity calculations (Shannon, Gini-Simpson, Rao's quadratic entropy) are sensitive to absolute abundance differences.

## When to use

Apply this skill when you have a peak-abundance matrix from FT-ICR MS (peaks as rows, samples as columns with raw peak intensities) and need to compute abundance-based diversity indices or functional diversity metrics that are sensitive to relative vs. absolute peak heights. Specifically, use it when inoculation status, treatment group, or environmental condition is the grouping variable and you want to ensure that diversity comparisons are not confounded by differences in ionization efficiency or sample concentration across groups.

## When NOT to use

- Input peak-abundance matrix is already normalized or contains relative abundances (proportions or percentages); applying sum-normalization again would double-normalize and bias results toward uniform distributions.
- You have fewer than 4 samples per group or extremely sparse data (>90% of peaks absent in most samples), making diversity estimates unstable and group comparisons underpowered.
- Your research question targets absolute peak intensity (e.g., ion suppression effects or ionization bias between samples); sum-normalization removes this signal intentionally and is inappropriate.

## Inputs

- peak-abundance matrix (CSV: peaks as rows, samples as columns, raw peak intensities)
- sample metadata (CSV: sample identifiers with experimental grouping variables such as inoculation status or treatment)
- assigned molecular formulas (required for downstream functional diversity via elemental composition and aromaticity traits)

## Outputs

- sum-normalized peak-abundance matrix (CSV: same structure, intensities normalized per sample)
- abundance-based diversity indices per sample (CSV: Shannon diversity index, Gini-Simpson index, Chao1 richness estimator, grouped by experimental variable)
- diversity metric summary statistics and box plots (PNG/PDF: visualization of richness and diversity by group)
- statistical comparison table (CSV: mean, median, std dev, p-values for each diversity metric grouped by experimental condition)

## How to apply

Load the filtered peak-abundance matrix in CSV format (peaks as rows, samples as columns) into MetaboDirect or a compatible R/Python environment. Apply sum-normalization to each sample column independently: divide all peak intensities in a sample by the column sum, then optionally scale back to a fixed total (e.g., 10^6) to preserve dynamic range while making samples directly comparable. Verify that normalized peak intensities are bounded within [0, 1] or your chosen reference scale and that no sample sums to zero (which would indicate complete absence of signal). Then calculate abundance-based diversity indices (Shannon diversity H = −Σ(p_i × ln(p_i)), Gini-Simpson D = 1 − Σ(p_i²), Chao1 richness estimator) using normalized peak proportions via the vegan R package. Group results by your experimental variable (inoculation status, treatment, etc.) and generate summary statistics and box plots to visualize differences in metabolite richness and evenness.

## Related tools

- **MetaboDirect** (command-line pipeline for automated sum-normalization, chemodiversity analysis (Shannon, Gini-Simpson, Rao's quadratic entropy), and visualization of normalized peak-abundance data) — https://github.com/Coayala/MetaboDirect
- **vegan** (R package for calculating abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) on normalized peak proportions)
- **SYNCSA** (R package for calculating functional-based diversity (Rao's quadratic entropy) incorporating elemental composition, decomposability, and aromaticity traits of peaks)

## Examples

```
metabodirect -i peak_abundance.csv -m sample_metadata.csv -n sum -o normalized_output/ --diversity-metrics shannon gini-simpson chao1 --grouping-variable inoculation_status
```

## Evaluation signals

- Verify that each sample's normalized peak intensities sum to 1.0 (or your chosen reference scale, e.g., 10^6) within floating-point tolerance (< 1e−10).
- Check that no sample in the normalized matrix has a negative intensity or any intensity > 1.0 (or reference scale max); the normalized matrix must be bounded and non-negative.
- Confirm that diversity indices (Shannon, Gini-Simpson, Chao1) are calculated on the normalized (not raw) peak proportions; boxplots should show clear separation between experimental groups (inoculated vs. control) and confidence intervals should not fully overlap if effect size is substantial.
- Validate that the number of samples per group, sample richness (number of detected peaks), and group-level diversity estimates match the summary statistics table and match summary tables exported as CSV.
- Ensure that grouping variable metadata (inoculation status, treatment) is correctly merged with diversity metric results; visual inspection of boxplots should show samples of the same group clustered together.

## Limitations

- Sum-normalization assumes that the total ion current (TIC) across a sample is proportional to sample concentration and not driven by ion suppression or matrix effects; if ionization efficiency varies systematically between groups (e.g., due to DOM composition), normalized abundances may still be biased.
- MetaboDirect does not provide raw spectra data preprocessing, so input peak-abundance matrices must already be cleaned (isotopes removed, m/z error filtered to ≤0.5 ppm, low-abundance noise peaks filtered by presence threshold); inappropriate filtering upstream will propagate into diversity estimates.
- Diversity metrics derived from normalized peak intensities are sensitive to the presence/absence of low-abundance peaks; if peaks are filtered aggressively or detection limits vary between samples, richness and evenness estimates may be artificially deflated or inflated.
- Rao's quadratic entropy (functional diversity) relies on accurate trait assignments (elemental composition, decomposability, aromaticity); if molecular formula assignment error is high (>0.5 ppm) or trait values are missing, functional diversity estimates may not reflect true biochemical diversity.

## Evidence

- [other] Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function.: "Sum-normalize raw peak intensities across each sample using MetaboDirect's sum-normalization function."
- [other] Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities.: "Calculate abundance-based diversity metrics (Shannon diversity index, Gini-Simpson index, Chao1 richness estimator) using vegan package functions on normalized peak intensities."
- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [abstract] MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization of a wide range of plots: "MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization of a wide range of plots"
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
