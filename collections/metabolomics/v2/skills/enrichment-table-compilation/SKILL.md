---
name: enrichment-table-compilation
description: Use when you have completed Fisher's exact test enrichment analysis on a set of metabolites or lipids against a pathway/ontology reference (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0202
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - readr
  - enrichmet
  - Fisher's exact test
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
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

# enrichment-table-compilation

## Summary

Compile and format pathway or ontology enrichment analysis results into a structured data.frame with statistical metrics, effect sizes, and overlap counts. This skill transforms raw Fisher's exact test outputs into a publication-ready enrichment table suitable for downstream visualization and interpretation.

## When to use

You have completed Fisher's exact test enrichment analysis on a set of metabolites or lipids against a pathway/ontology reference (e.g., KEGG pathways, LION lipid categories, or custom ontology mappings), and you need to consolidate per-pathway p-values, adjusted p-values, odds ratios, and member counts into a single structured result table for reporting or filtering.

## When NOT to use

- Input metabolite list has not yet been tested for association with pathways/ontologies—you need to run Fisher's exact test first, not just compile existing statistics.
- You are working with pre-ranked metabolite sets (GSEA-style) rather than binary presence/absence lists; use a different enrichment output schema (NES, nominal p-value, FDR q-value) tailored to GSEA.
- Pathway reference (PathwayVsMetabolites) is not well-curated or contains ambiguous metabolite identifiers that do not match your input list; enrichment counts and odds ratios will be unreliable.

## Inputs

- list of input metabolites or lipids (character vector with standardized IDs: KEGG, LION category identifiers, or custom ontology entity names)
- PathwayVsMetabolites reference file (data.frame with pathway/ontology_category names as rows and comma-separated metabolite/lipid lists as columns, or equivalent long-format mapping)
- per-pathway Fisher's exact test results (raw p-values, contingency counts for each pathway)
- optional: precomputed odds ratios or relative risk estimates from Fisher tests

## Outputs

- enrichment results data.frame (S3 object) with columns: Pathway, P_value, Adjusted_P_value, Odds_Ratio, Count (of overlapping entities), Pathway_Size
- enrichment CSV file with same schema for archival or external tool import
- optional: filtered subset data.frame meeting user-specified p-value and minimum occurrence thresholds

## How to apply

After running Fisher's exact test on each pathway or ontology category independently, collect the following per-pathway statistics: raw p-value, count of overlapping metabolites/lipids in the input list, and odds ratio. Apply Benjamini–Hochberg false discovery rate correction to all raw p-values to obtain adjusted p-values. Organize these statistics into a data.frame with columns: pathway/category name, Fisher test p-value, adjusted p-value, odds ratio, and overlapping entity count. Filter to pathways meeting user-specified thresholds (e.g., p_value_cutoff = 0.05, min_pathway_occurrence = 2) to retain only significant, well-represented hits. Sort results by adjusted p-value or odds ratio for intuitive prioritization, then export as CSV or retain as an R S3 data.frame object for further downstream analysis or visualization.

## Related tools

- **enrichmet** (executes Fisher's exact test enrichment and generates the enrichment results data.frame via the enrichmet() function; computes Benjamini–Hochberg adjusted p-values and organizes output into structured tables) — https://github.com/biodatalab/enrichmet
- **R** (host language for data manipulation, statistical computation, and data.frame assembly)
- **readr** (writes enrichment results data.frame to CSV format for export and archival)
- **Fisher's exact test** (computes raw p-values and odds ratios for each pathway; outputs are the foundation for the enrichment table)

## Examples

```
results <- enrichmet(inputMetabolites = inputMetabolites, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_out, p_value_cutoff = 0.05, min_pathway_occurrence = 2); write.csv(results$pathway_enrichment_all, 'enrichment_table.csv', row.names = FALSE)
```

## Evaluation signals

- Output data.frame has exactly one row per tested pathway/ontology category with no duplicates; row count matches the number of pathways in PathwayVsMetabolites.
- Adjusted p-values are monotonically non-decreasing when sorted alongside raw p-values (i.e., Benjamini–Hochberg correction preserves order and increases or maintains p-values).
- Overlapping entity count is ≤ the smaller of (input metabolite list size, pathway size); odds ratio is finite and positive.
- All p-values and adjusted p-values are in [0, 1]; count columns are non-negative integers.
- After filtering by p_value_cutoff and min_pathway_occurrence, retained pathways are consistent with thresholds: adjusted_p_value ≤ cutoff, overlapping_count ≥ min_occurrence.

## Limitations

- Accuracy depends on quality and completeness of PathwayVsMetabolites reference mapping; unmapped or misidentified metabolites will reduce statistical power and inflate false negatives.
- Small pathway sizes or low input metabolite counts reduce effective statistical power; odds ratios and p-values become unreliable for rare pathways (min_pathway_occurrence filtering mitigates but does not eliminate this).
- Benjamini–Hochberg correction assumes independence of tests, which is violated when pathways share many metabolites; this can lead to overestimation of adjusted p-values in interconnected pathway networks.
- The skill does not account for metabolite-level annotation uncertainty (e.g., isomeric ambiguity, mass spectral adducts); prior deduplication or standardization of the input list is assumed.
- No built-in visualization; compiled table must be passed to separate plotting routines to generate enrichment plots, heatmaps, or network diagrams.

## Evidence

- [other] Execute Fisher's exact test on each lipid ontology category using the enrichmet workflow to test for significant association between the input lipid list and each category, applying p_value_cutoff = 0.05 and min_pathway_occurrence = 2.: "Execute Fisher's exact test on each lipid ontology category using the enrichmet workflow to test for significant association between the input lipid list and each category, applying p_value_cutoff ="
- [other] Compute adjusted p-values using Benjamini–Hochberg correction.: "Compute adjusted p-values using Benjamini–Hochberg correction."
- [other] Compile results into a data.frame with lipid ontology categories, Fisher test p-values, adjusted p-values, odds ratios, and counts of overlapping lipids.: "Compile results into a data.frame with lipid ontology categories, Fisher test p-values, adjusted p-values, odds ratios, and counts of overlapping lipids."
- [intro] The enrichmet() function produces three tables (S3 data.frame objects), which may include the MetSEA table, metabolite centrality, and pathway enrichment results.: "The enrichmet() function produces three tables (S3 data.frame objects), which may include the MetSEA table, metabolite centrality, and pathway enrichment results."
- [intro] This file defines the mapping between metabolic pathways and their associated metabolites and serves as the background reference for the Fisher exact test used during enrichment: "This file defines the mapping between metabolic pathways and their associated metabolites and serves as the background reference for the Fisher exact test used during enrichment"
