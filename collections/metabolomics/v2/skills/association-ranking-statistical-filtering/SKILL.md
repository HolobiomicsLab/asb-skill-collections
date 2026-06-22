---
name: association-ranking-statistical-filtering
description: Use when you have identified co-occurring metabolite–genomic variant associations from a network-driven over-representation analysis and need to rank them by confidence and control the family-wise error rate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3056
  - http://edamontology.org/topic_3517
  tools:
  - R
  - metGWAS 1.0
  - qvalue R package
  - Benjamini–Hochberg correction
derived_from:
- doi: 10.1093/bioinformatics/btad523/7248906
  title: metGWAS 1.0
evidence_spans:
- An R workflow for network-driven over-representation analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metgwas_1_0_cq
    doi: 10.1093/bioinformatics/btad523/7248906
    title: metGWAS 1.0
  dedup_kept_from: coll_metgwas_1_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad523/7248906
  all_source_dois:
  - 10.1093/bioinformatics/btad523/7248906
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# association-ranking-statistical-filtering

## Summary

Filter and rank molecular associations (metabolite–variant pairs) by statistical significance, then adjust p-values for multiple testing to control false discovery rate. This skill bridges independent metabolomic and GWAS datasets by identifying robust cross-study associations that survive stringent correction.

## When to use

You have identified co-occurring metabolite–genomic variant associations from a network-driven over-representation analysis and need to rank them by confidence and control the family-wise error rate. Apply this skill when you have raw enrichment p-values from hypergeometric tests or similar statistical tests and must distinguish signal from noise across hundreds of potential associations.

## When NOT to use

- Input p-values have already been corrected for multiple testing in an upstream analysis; applying correction again risks over-conservative thresholds.
- You are working with a single pre-registered hypothesis test; Benjamini–Hochberg and similar corrections are designed for exploratory screening of many associations, not confirmatory single tests.
- Sample size or association count is extremely small (< 10 associations); multiple-testing correction may lack power and produce inflated adjusted p-values.

## Inputs

- raw p-values from over-representation analysis (hypergeometric test results)
- effect sizes or enrichment scores for each association
- feature identifiers (gene names, metabolite IDs, pathway names)
- significance threshold (default p < 0.05 or user-specified)

## Outputs

- ranked association table with feature names, enrichment scores, raw p-values, and adjusted p-values
- filtered association set (associations passing significance threshold after correction)
- correction method metadata (e.g., 'Benjamini–Hochberg')

## How to apply

Begin by filtering associations to retain only those meeting a pre-specified significance threshold (typically p < 0.05 or user-defined cutoff). Compute adjusted p-values using a multiple-testing correction procedure (e.g., Benjamini–Hochberg FDR correction) to account for the number of tests performed. Rank enriched features (genes, metabolites, pathways) by adjusted p-value in ascending order, with the most significant associations appearing first. Document the correction method and original p-value alongside the adjusted p-value in the results table. This ranking allows downstream interpretation to focus on the most robust associations first and provides transparency about the stringency applied.

## Related tools

- **R** (Environment for implementing filtering, p-value adjustment (via p.adjust() or qvalue package), and ranking operations; supports data frame manipulation and export of results tables.)
- **metGWAS 1.0** (Performs hypergeometric over-representation tests to generate raw p-values and enrichment scores that are then filtered and ranked by this skill.) — https://github.com/saifurbd28/metGWAS-1.0
- **qvalue R package** (Computes q-values (FDR-adjusted p-values) using the Benjamini–Hochberg method and related corrections.)
- **Benjamini–Hochberg correction** (Multiple-testing adjustment method used to rank and filter associations while controlling false discovery rate.)

## Examples

```
# Adjust p-values from over-representation analysis and rank by significance
adjusted_p <- p.adjust(enrichment_results$pvalue, method='BH')
enrichment_results_ranked <- enrichment_results[order(adjusted_p), ]
enrichment_results_ranked$adjusted_pvalue <- adjusted_p[order(adjusted_p)]
write.csv(enrichment_results_ranked[enrichment_results_ranked$adjusted_pvalue < 0.05, ], 'ranked_associations.csv')
```

## Evaluation signals

- Adjusted p-values are monotonically non-decreasing when sorted alongside raw p-values (each adjusted p-value ≥ its corresponding raw p-value).
- Number of associations retained after filtering matches the expected count given the threshold and total number of tests (e.g., if 500 tests performed and FDR = 0.05, expect roughly 25 associations with q < 0.05 under the null).
- Results table contains exactly four columns per association: feature name, enrichment score, raw p-value, and adjusted p-value; no missing values in these fields.
- Ranking order is identical to ascending adjusted p-value order; spot-checks confirm the top-ranked association has the smallest adjusted p-value.
- Metadata documents the correction method and number of tests performed, allowing reproducibility and interpretation of stringency.

## Limitations

- Benjamini–Hochberg correction assumes independence or positive dependence among tests; if associations are highly correlated (e.g., due to network structure), the method may be conservative and miss true signals.
- Filtering at a fixed p-value threshold (e.g., p < 0.05) before correction can introduce bias; threshold should be applied to adjusted p-values, not raw p-values.
- metGWAS 1.0 is limited to genes with known metabolite interactions (via KEGG, HMDB, or similar databases); associations involving novel metabolites or genes not yet annotated will be missed regardless of statistical significance.
- Multiple-testing correction power declines with the number of tests; if the over-representation analysis tests hundreds or thousands of features, even true associations may not survive stringent correction.

## Evidence

- [methods] Filter associations by significance threshold (typically p < 0.05 or user-specified cutoff).: "Filter associations by significance threshold (typically p < 0.05 or user-specified cutoff)"
- [methods] Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank enriched features by significance.: "Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank enriched features by significance"
- [methods] Export over-representation results table with feature names, enrichment scores, adjusted p-values, and network membership.: "Export over-representation results table with feature names, enrichment scores, adjusted p-values, and network membership"
- [readme] generates and statistically compares metabolic and genomic gene sets using a hypergeometric test: "generates and statistically compares metabolic and genomic gene sets using a hypergeometric test"
