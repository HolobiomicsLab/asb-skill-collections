---
name: lipid-ontology-category-mapping
description: Use when you have a list of detected lipids (e.g., from LC-MS/MS lipidomics
  data) with associated statistical measures (p-values, fold-changes), and you need
  to test whether specific lipid ontology categories (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3407
  tools:
  - R
  - readr
  - enrichmet
  - LION lipid ontology database
  - Fisher's exact test
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed
  through a single R function call
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-ontology-category-mapping

## Summary

Apply Fisher's exact test enrichment analysis to lipidomics data by mapping lipids to standardized lipid ontology categories using the LION lipid ontology, enabling identification of significantly enriched lipid classes and functional groups in differential lipid profiles.

## When to use

You have a list of detected lipids (e.g., from LC-MS/MS lipidomics data) with associated statistical measures (p-values, fold-changes), and you need to test whether specific lipid ontology categories (e.g., phospholipids, sphingolipids, sterol esters) are significantly over- or under-represented compared to a background lipid ontology mapping. This skill applies when ontology-level interpretation is more informative than individual lipid features.

## When NOT to use

- Your input lipids are already annotated to a single, definitive lipid class and you seek only to characterize that class, not test for enrichment across multiple categories.
- You lack a curated lipid ontology mapping file or cannot map your lipid identifiers to the ontology nomenclature; standard pathway databases (e.g., KEGG) may be insufficient for lipid-specific category grouping.
- Your lipidomics data are quantitative and you require abundance-based statistical tests (e.g., GSEA, Wilcoxon rank-sum) rather than presence/absence category testing via Fisher's exact test.

## Inputs

- lipid list (character vector of lipid identifiers, e.g. LION nomenclature or mass-based identifiers)
- LION lipid ontology mapping file (CSV; LION_Lipid_Ontology.csv format with ontology categories and member lipids)
- optional: differential analysis results (data.frame with lipid identifiers, p-values, log2 fold-changes)

## Outputs

- enrichment results table (data.frame: lipid ontology categories, p-values, adjusted p-values, odds ratios, overlap counts)
- CSV export of enrichment table with significant categories (filtered by adjusted p-value and parameter thresholds)

## How to apply

Load the input lipid list and the LION lipid ontology mapping file (LION_Lipid_Ontology.csv from Zenodo 17819145) into R. Reformat the lipid list and ontology mapping into a PathwayVsMetabolites-compatible structure with lipid ontology categories as rows and individual lipids as columns, ensuring consistent lipid identifier nomenclature. Execute Fisher's exact test on each lipid ontology category to evaluate the association between your input lipid list and each category, applying p_value_cutoff = 0.05 and min_pathway_occurrence = 2 to filter categories with insufficient representation. Compute adjusted p-values using Benjamini–Hochberg multiple-testing correction. Compile results into a data.frame reporting lipid ontology categories, raw Fisher test p-values, adjusted p-values, odds ratios, and counts of overlapping lipids between your list and each category. Return and export the enrichment table as a CSV file for downstream interpretation and visualization.

## Related tools

- **enrichmet** (R package that implements Fisher's exact test enrichment workflow and provides the enrichmet() function to execute category-level enrichment analysis on metabolite and lipid lists against ontology mappings) — https://github.com/biodatalab/enrichmet
- **readr** (R package for efficient reading and parsing of CSV lipid lists and LION ontology mapping files)
- **LION lipid ontology database** (Curated lipid ontology resource providing LION_Lipid_Ontology.csv mapping file linking lipid identifiers to standardized ontology categories) — https://zenodo.org/records/17819145
- **Fisher's exact test** (Statistical method for testing independence between input lipid presence and lipid ontology category membership, yielding p-values and odds ratios per category)

## Examples

```
results <- enrichmet(inputMetabolites = lipid_list, PathwayVsMetabolites = PathwayVsMetabolites, p_value_cutoff = 0.05, min_pathway_occurrence = 2)
```

## Evaluation signals

- Verify that all input lipids are successfully mapped to at least one LION ontology category; report fraction of lipids with zero ontology assignments as a data quality metric.
- Confirm that adjusted p-values are computed correctly: recompute Benjamini–Hochberg correction independently and verify rank-order and magnitude match the output table.
- Check that overlap counts and odds ratios are consistent: for each enriched category, manually verify the contingency table (lipids in category ∩ input list, lipids in category ∖ input list, etc.) and recalculate Fisher's exact test p-value and odds ratio.
- Validate parameter application: confirm that only categories with ≥ min_pathway_occurrence (default 2) lipids and Fisher test p-values ≤ p_value_cutoff (default 0.05) are retained in output.
- Cross-check output against LION schema: ensure all reported lipid ontology categories are valid entries in the input LION_Lipid_Ontology.csv file and no orphan categories are created.

## Limitations

- Mapping accuracy depends on consistency of lipid nomenclature between input lipid list and LION ontology; mismatches due to different ionization adducts, in-source fragmentation notation, or database version will reduce overlap detection.
- Fisher's exact test assumes independence between lipid ontology categories, which may not hold if categories share members or are hierarchically nested within LION; results should not be interpreted as mutually exclusive.
- LION ontology may not represent novel or non-canonical lipids discovered in your experiment; enrichment analysis is limited to categories defined in the reference mapping file.
- Multiple-testing correction (Benjamini–Hochberg) controls false discovery rate across all categories but does not account for non-independence in the category structure; consider secondary validation or effect-size filtering (e.g., odds ratio > 2).
- Fisher's exact test on small category memberships (min_pathway_occurrence = 2) may yield unstable or spurious p-values; authors recommend min_pathway_occurrence ≥ 3 for robust results.

## Evidence

- [other] Load the user-provided lipid list and the LION lipid ontology mapping file (LION_Lipid_Ontology.csv from Zenodo) into R.: "Load the user-provided lipid list and the LION lipid ontology mapping file (LION_Lipid_Ontology.csv from Zenodo)"
- [other] Format the lipid list and ontology mapping into a PathwayVsMetabolites-compatible structure with lipid ontology categories as rows and lipids as columns.: "Format the lipid list and ontology mapping into a PathwayVsMetabolites-compatible structure with lipid ontology categories as rows and lipids as columns."
- [other] Execute Fisher's exact test on each lipid ontology category using the enrichmet workflow to test for significant association between the input lipid list and each category, applying p_value_cutoff = 0.05 and min_pathway_occurrence = 2.: "Execute Fisher's exact test on each lipid ontology category using the enrichmet workflow to test for significant association between the input lipid list and each category, applying p_value_cutoff ="
- [other] Compute adjusted p-values using Benjamini–Hochberg correction.: "Compute adjusted p-values using Benjamini–Hochberg correction."
- [other] Compile results into a data.frame with lipid ontology categories, Fisher test p-values, adjusted p-values, odds ratios, and counts of overlapping lipids.: "Compile results into a data.frame with lipid ontology categories, Fisher test p-values, adjusted p-values, odds ratios, and counts of overlapping lipids."
- [other] The enrichmet workflow successfully adapted to lipidomics by applying Fisher's exact test enrichment analysis against a lipid ontology mapping file generated in the same PathwayVsMetabolites format, demonstrating the framework's applicability beyond metabolomics to additional measurement modalities.: "The enrichmet workflow successfully adapted to lipidomics by applying Fisher's exact test enrichment analysis against a lipid ontology mapping file generated in the same PathwayVsMetabolites format,"
