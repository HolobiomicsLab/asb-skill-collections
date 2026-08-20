---
name: metabolite-trend-classification
description: Use when when you have compiled p-values and fold-changes from multiple
  metabolomics studies and need to assign a single trend label (up/down/none) to each
  metabolite for meta-analysis or cross-study comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - amanida
  - compute_amanida
  - check_names
  - webchem
  - volcano_plot
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-trend-classification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Classify metabolites as up-regulated, down-regulated, or no trend by combining statistical significance (p-value), effect direction (fold-change), and study size weights in a meta-analysis framework. This skill integrates quantitative signals across multiple studies to assign a single consensus trend per metabolite.

## When to use

When you have compiled p-values and fold-changes from multiple metabolomics studies and need to assign a single trend label (up/down/none) to each metabolite for meta-analysis or cross-study comparison. Use this skill when standard deviation data are unavailable but study size (N) is known, and you want trend classification that reflects both statistical significance and biological effect direction weighted by study contribution.

## When NOT to use

- Input data already includes a single pre-computed trend or consensus label from another tool — do not re-classify.
- Raw individual-level metabolite measurements are available — use primary differential analysis instead of meta-analysis trend classification.
- Study sizes (N) are unknown or unavailable; weighted methods cannot be reliably applied without study size information.

## Inputs

- amanida data structure: harmonized metabolite identifier, p-value per study, fold-change per study, study size (N) per study, and reference columns
- computed @stat table from compute_amanida with combined p-values and weighted average fold-changes
- user-defined significance cutoffs: p-value threshold (e.g., 0.05) and fold-change magnitude threshold (e.g., 2 in log2 scale)

## Outputs

- trend label per metabolite: +1 (up-regulation), −1 (down-regulation), or 0 (no trend)
- trend classification table with metabolite identifiers, combined p-values, combined fold-changes, and assigned trend direction
- N_total (sum of study sizes) for each metabolite
- vote-counting qualitative results (@vote table) reflecting trend consensus across studies

## How to apply

After combining p-values using weighted Fisher's method (with gamma-distributed weights proportional to study size) and fold-changes via log2 transformation and study-size-weighted averaging using compute_amanida, extract the trend direction from the resulting @stat table. The trend is classified as: +1 for up-regulation, −1 for down-regulation, and 0 for no trend, based on the combined p-value significance (typically p < 0.05) and the direction and magnitude of the weighted average log2 fold-change (biologically meaningful if |FC| > 2 log2-units, roughly FC > 4 linear scale). Apply user-defined cutoffs for p-value (e.g., 0.05) and fold-change magnitude (e.g., 2 in log2 scale) to determine which metabolites cross the significance threshold and thus receive a non-zero trend label. The trend output is used downstream for vote-counting, visualization (volcano plots), and consensus reporting.

## Related tools

- **amanida** (R package that computes weighted meta-analysis combining p-values and fold-changes, generating @stat table with trend direction and N_total for trend classification) — https://github.com/mariallr/amanida
- **compute_amanida** (Core amanida function that applies weighted Fisher's method to combine p-values and log2-transformed, study-size-weighted averaging for fold-changes, producing the @stat result table used for trend assignment) — https://github.com/mariallr/amanida
- **check_names** (amanida function that harmonizes metabolite identifiers across studies by converting to PubChem IDs and detecting duplicates prior to trend classification) — https://github.com/mariallr/amanida
- **webchem** (R package used by amanida to retrieve PubChem IDs and standardize metabolite nomenclature before trend classification)
- **volcano_plot** (amanida visualization function that displays trend classification results, plotting log10(p-value) against log2(fold-change) with user-defined cutoffs) — https://github.com/mariallr/amanida

## Examples

```
amanida_result <- compute_amanida(datafile, comp.inf = FALSE); trend_table <- amanida_result@stat; volcano_plot(amanida_result, cutoff = c(0.05, 2))
```

## Evaluation signals

- Trend assignments are binary or ternary (±1 or 0) and match the direction of the combined fold-change: positive FC → +1 trend, negative FC → −1 trend, or FC within cutoff → 0.
- All metabolites in the output table have a trend label; none are missing or NaN.
- Metabolites with combined p-value > 0.05 and/or |log2 FC| < 2 are labeled as trend = 0 (no trend); metabolites meeting both thresholds receive ±1.
- Volcano plot correctly plots metabolites with trend = ±1 outside the user-specified cutoff boundaries; those inside are plotted as trend = 0.
- N_total values are positive integers equal to or less than the sum of individual study N values, confirming no data loss during combination.

## Limitations

- Trend classification requires consistent measurement and reporting of p-values and fold-changes across all input studies; missing or inconsistent data are ignored, which may bias results if missingness is not random.
- Negative fold-change values are inverted (1/value) to positive before log2 transformation, which may obscure the directionality of originally negative fold-changes in some workflows.
- Cutoff thresholds (p-value and fold-change) are user-defined and subjective; different cutoffs produce different trend classifications. The paper recommends p < 0.05 and |FC| > 2 log2 for biological meaningfulness, but other cutoffs may be appropriate depending on context.
- Trend classification does not account for study heterogeneity or quality; all studies contribute equally (weighted only by size) regardless of methodology or bias risk.
- Vote-counting output is restricted to 30 compounds for readability, limiting visualization of trend classifications for large metabolite inventories.

## Evidence

- [intro] votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend: "votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
- [intro] P-value: weighted p-values combination, which is a variant of Fisher's method with gamma-distributed weights proportional to study size: "P-value: weighted p-values combination, which is a variant of Fisher's method. A gamma distribution is used to assign non-integral weights proportional to study size to each p-value."
- [intro] Fold-change combination via log2 transformation and study-size-weighted averaging: "Fold-change: logarithmic transformation for average with weighting by number of participants"
- [methods] compute_amanida generates @stat results table with trend direction and N_total: "Execute compute_amanida function in R to generate the @stat results table, including trend direction (up-regulation, down-regulation, or no trend) and N_total (sum of study sizes across all"
- [intro] Features with fold-change higher than 2 are recommended for biological meaningfulness: "in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness"
- [intro] negative values of fold-change are transformed to positive (1/value): "negative values of fold-change are transformed to positive (1/value)"
