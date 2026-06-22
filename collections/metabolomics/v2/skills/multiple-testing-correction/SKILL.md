---
name: multiple-testing-correction
description: Use when whenever you have performed Fisher's exact test or another statistical enrichment test on multiple pathways, lipid categories, or metabolite sets simultaneously (typically ≥2 tests, often 50–100+ tests in practice).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3517
  tools:
  - R
  - readr
  - KEGG
  - R p.adjust() function
  - enrichmet
  - stats::p.adjust (R base)
  - Python (pandas, NumPy, SciPy)
  - scipy.stats
  - R stats or p.adjust()
  - MetENP (R package)
  - R (base stats and Bioconductor)
  - qvalue package
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
- doi: 10.1101/2020.11.20.391912
  title: ''
- doi: 10.1093/bioinformatics/btad523/7248906
  title: ''
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
- library(readr)
- curated KEGG data for enrichment using Fisher's Exact Test
- MetENP
- An R workflow for network-driven over-representation analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  - build: coll_metenp_cq
    doi: 10.1101/2020.11.20.391912
    title: MetENP
  - build: coll_metgwas_1_0_cq
    doi: 10.1093/bioinformatics/btad523/7248906
    title: metGWAS 1.0
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  - 10.1101/2020.11.20.391912
  - 10.1093/bioinformatics/btad523/7248906
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiple-testing-correction

## Summary

Apply multiple-testing correction (Benjamini–Hochberg or other family-wise error rate control) to p-values derived from pathway enrichment tests to control false discovery rate across many simultaneous statistical tests. This skill prevents inflated Type I error when testing hundreds of pathways or metabolite categories against a single input metabolite set.

## When to use

Apply this skill whenever you have performed Fisher's exact test or another statistical enrichment test on multiple pathways, lipid categories, or metabolite sets simultaneously (typically ≥2 tests, often 50–100+ tests in practice). The raw p-values from each individual test do not account for the multiple comparisons problem; correction is required before reporting or filtering significant results.

## When NOT to use

- Input is a single hypothesis test (n=1 pathway or category) — no correction needed.
- P-values have already been corrected by the upstream software — applying correction twice will introduce bias.
- Analysis is exploratory and raw p-values are acceptable — though not recommended for publication without adjustment disclosure.

## Inputs

- vector or data.frame column of raw p-values from Fisher's exact test (one p-value per pathway or metabolite category)
- number of tests performed (inferred from p-value vector length)

## Outputs

- data.frame or vector of adjusted p-values (same length as input)
- enrichment results table with columns: pathway/category name, raw p-value, adjusted p-value, odds ratio or effect size, metabolite count

## How to apply

After computing raw p-values from Fisher's exact test for each pathway or category, apply Benjamini–Hochberg (BH) correction to the full set of p-values using a standard method (e.g., R's p.adjust() function with method='BH'). The BH procedure controls false discovery rate (FDR) while preserving statistical power better than strict Bonferroni correction. Store both raw and adjusted p-values in the enrichment results table; use adjusted p-values (typically with threshold p_adj ≤ 0.05) for downstream filtering, visualization, and reporting. Document the correction method and cutoff in all output tables and figures.

## Related tools

- **R p.adjust() function** (Performs Benjamini–Hochberg and other multiple-testing corrections on p-value vectors)
- **enrichmet** (Integrates Benjamini–Hochberg correction as a built-in step in pathway enrichment workflow; automatically computes and returns adjusted p-values in enrichment results table) — https://github.com/biodatalab/enrichmet
- **stats::p.adjust (R base)** (General-purpose multiple-testing correction for any set of p-values)

## Examples

```
results <- enrichmet(inputMetabolites = inputMetabolites, PathwayVsMetabolites = PathwayVsMetabolites, p_value_cutoff = 0.05, min_pathway_occurrence = 2); # Benjamini–Hochberg correction is applied internally; view corrected p-values in results$pathway_enrichment_all
```

## Evaluation signals

- Adjusted p-values are monotonically non-decreasing when sorted by raw p-value (verification of correct BH ranking).
- Adjusted p-value ≥ corresponding raw p-value for all tests (BH correction always inflates p-values to be conservative).
- Number of significant pathways after adjustment (adj_p ≤ 0.05) is ≤ number before adjustment.
- Enrichment results table contains both 'P_value' (raw) and adjusted p-value columns with clear labeling (e.g., 'Adjusted_P_value' or 'FDR').
- Reported significant findings cite the corrected p-value threshold and correction method (e.g., 'Benjamini–Hochberg corrected p ≤ 0.05').

## Limitations

- BH correction assumes tests are independent or positively dependent; if pathways share metabolites (common in real data), the assumption may be violated, though BH remains valid.
- With very large numbers of tests (e.g., >10,000), BH correction may be overly conservative and reduce power; more sophisticated methods (e.g., Storey's q-value) may be preferred in those cases.
- Correction cannot recover signal from inherently noisy or underpowered individual tests; if raw p-values are all close to 1, correction will not rescue significance.
- Choice of FDR threshold (0.05 vs. 0.1 vs. 0.01) is arbitrary and should be stated a priori; post-hoc threshold selection risks p-hacking.

## Evidence

- [intro] Compute adjusted p-values using Benjamini–Hochberg correction: "Compute adjusted p-values using Benjamini–Hochberg correction."
- [intro] enrichment results table with pathways, metabolite counts, p-values, adjusted p-values, and effect sizes: "data.frame with pathways, metabolite counts, p-values, adjusted p-values, and effect sizes"
- [intro] p_value_cutoff parameter controls significance threshold for individual tests: "p_value_cutoff = 0.05"
- [intro] Fisher's exact test enrichment workflow executed on each category: "Execute Fisher's exact test on each lipid ontology category using the enrichmet workflow to test for significant association"
