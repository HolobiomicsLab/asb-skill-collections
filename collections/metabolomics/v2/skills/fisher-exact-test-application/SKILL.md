---
name: fisher-exact-test-application
description: Use when you have a list of metabolites or lipids with associated p-values (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - R
  - KEGG
  - readr
  - enrichmet
  - fgsea
  - igraph
  - KEGG / KEGGREST
  - LION lipid ontology database
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
- curated KEGG data for enrichment using Fisher's Exact Test
- library(readr)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
---

# fisher-exact-test-application

## Summary

Apply Fisher's exact test to identify statistically significant metabolic pathways or lipid ontology categories enriched in a user-supplied metabolite or lipid list. This skill tests the null hypothesis of independence between group membership (e.g., significantly dysregulated metabolites) and pathway/category membership using contingency tables, producing p-values, adjusted p-values, odds ratios, and effect sizes.

## When to use

Use this skill when you have a list of metabolites or lipids with associated p-values (e.g., from differential analysis) and a reference mapping file (pathway-to-metabolite or lipid-to-ontology category) and want to identify which pathways or lipid categories are statistically overrepresented in your dysregulated metabolites. It is appropriate when the contingency table is small (expected counts < 5 are common in pathway enrichment) and exact inference is preferred over asymptotic approximation.

## When NOT to use

- Input metabolites are already pre-filtered and p-values are not available or are unreliable (e.g., from visual inspection rather than statistical test).
- Pathway membership is continuous or probabilistic rather than binary (e.g., pathway membership scores 0–1); use rank-based methods (e.g., fgsea, GSEA) instead.
- The reference pathway database is incomplete, outdated, or not applicable to the organism/tissue in your study; validation against curated, organism-specific mappings (e.g., KEGG for human) is essential.

## Inputs

- Filtered metabolite list (character vector with KEGG IDs and associated p-values from differential analysis)
- PathwayVsMetabolites mapping file (data.frame with columns: Pathway, Metabolites; metabolites comma-separated or pipe-delimited)
- p-value cutoff threshold (numeric, e.g., 0.05)
- Minimum pathway occurrence filter (integer, e.g., 2)
- Minimum metabolite occurrence filter (integer, e.g., 1)

## Outputs

- Pathway enrichment results table (data.frame with columns: Pathway, Fisher_p_value, Adjusted_p_value, Odds_Ratio, Metabolite_Count, Pathway_Size)
- CSV file export of enrichment results
- Pathway enrichment visualization plot (volcano-style or bar plot of -log10(p) by pathway)

## How to apply

First, filter the input metabolite list using a p-value cutoff (e.g., p ≤ 0.05) to identify significantly dysregulated metabolites. Next, load the reference PathwayVsMetabolites file (or LION lipid ontology mapping in the same format), which maps each pathway/category (rows) to its constituent metabolites (comma-separated columns). For each pathway/category, construct a 2×2 contingency table: (metabolites in pathway AND in input list, metabolites in pathway AND NOT in input list, metabolites NOT in pathway AND in input list, metabolites NOT in pathway AND NOT in input list). Execute Fisher's exact test on each table. Apply min_pathway_occurrence (e.g., ≥ 2) and min_metabolite_occurrence (e.g., ≥ 1) filters to exclude uninformative pathways with too few metabolites. Compute Benjamini–Hochberg adjusted p-values across all tests. Extract pathways with adjusted p < 0.05 or unadjusted p < 0.05 (depending on multiple-testing strategy), and tabulate results with pathway names, Fisher p-values, adjusted p-values, odds ratios, and metabolite overlap counts.

## Related tools

- **enrichmet** (R package that wraps Fisher's exact test within a complete pathway enrichment workflow, executing contingency table construction, Fisher test, multiple-testing correction, and visualization in a single function call) — https://github.com/biodatalab/enrichmet
- **fgsea** (Integrated within enrichmet for fast Metabolite Set Enrichment Analysis (MetSEA) as a complementary rank-based enrichment method)
- **igraph** (Integrated within enrichmet for computing betweenness centrality of metabolites in pathway networks and generating topology-based visualizations)
- **KEGG / KEGGREST** (Source of curated pathway-to-metabolite mappings and KEGG identifiers; accessed via KEGGREST R package for dynamic pathway queries)
- **LION lipid ontology database** (Alternative reference database for Fisher's exact test enrichment when input is a lipid list; provides lipid-to-ontology-category mappings in PathwayVsMetabolites-compatible format) — https://zenodo.org/api/records/17819145/files/LION_Lipid_Ontology.csv/content

## Examples

```
results <- enrichmet(inputMetabolites = c("C00001", "C00002", "C00003"), PathwayVsMetabolites = PathwayVsMetabolites, p_value_cutoff = 0.05, min_pathway_occurrence = 2, min_metabolite_occurrence = 1)
```

## Evaluation signals

- Fisher's exact test p-values range from 0 to 1 and decrease (more significant) when metabolite-pathway overlap is larger and pathway size is controlled for.
- Adjusted p-values (Benjamini–Hochberg) are monotonically non-decreasing and ≥ their corresponding unadjusted p-values; no adjusted p-value should be < 0.05 if all unadjusted p-values are > 0.05.
- Odds ratios are positive and typically > 1 for enriched pathways (metabolite overlap higher than expected by chance); extreme OR values (e.g., > 100) may indicate small sample sizes or perfect separation in contingency table.
- Pathway enrichment results table has no missing values in key columns (Pathway, Fisher_p_value, Adjusted_p_value, Metabolite_Count); row count equals number of pathways passing min_pathway_occurrence and min_metabolite_occurrence filters.
- Top enriched pathways (lowest adjusted p-values) have metabolite counts matching the intersection of input metabolites and pathway membership in the reference file; manual spot-check validates contingency table logic.

## Limitations

- Fisher's exact test assumes metabolites are independent observations; if metabolites are correlated (e.g., co-regulated), p-values may be conservative or anticonservative.
- Pathway membership is binary and static; Fisher's test cannot capture partial membership, probabilistic associations, or context-dependent pathway activity.
- Multiple-testing correction (e.g., Benjamini–Hochberg) is applied across all pathways; with thousands of pathways and small sample sizes, FDR control can be stringent and result in few significant discoveries.
- Performance depends critically on the quality, completeness, and currency of the reference PathwayVsMetabolites mapping file; outdated or organism-mismatched databases yield unreliable results.
- Very small contingency table counts (e.g., < 5 total metabolites, < 2 pathways) can lead to separation or instability; minimum thresholds (e.g., min_pathway_occurrence ≥ 2) are enforced to mitigate.

## Evidence

- [intro] enrichmet performs pathway enrichment analysis using Fisher's exact test: "enrichmet performs pathway enrichment analysis using Fisher's exact test, computes betweenness centrality for metabolites, and performs Metabolite Set Enrichment Analysis (MetSEA)."
- [other] Fisher exact test-based pathway enrichment with parameter filtering: "Execute enrichmet() function with inputMetabolites, PathwayVsMetabolites, p_value_cutoff=0.05, min_pathway_occurrence=2, and min_metabolite_occurrence=1 parameters to perform Fisher's exact"
- [other] Output is a table with Fisher test statistics and metabolite counts: "Extract and export the pathway enrichment results table (data.frame with pathways, metabolite counts, p-values, adjusted p-values, and effect sizes) as a CSV file."
- [other] Extension to lipidomics using LION ontology mapping: "The enrichmet workflow successfully adapted to lipidomics by applying Fisher's exact test enrichment analysis against a lipid ontology mapping file generated in the same PathwayVsMetabolites format"
- [other] Benjamini–Hochberg adjustment for multiple testing: "Compute adjusted p-values using Benjamini–Hochberg correction. 5. Compile results into a data.frame with lipid ontology categories, Fisher test p-values, adjusted p-values, odds ratios, and counts of"
