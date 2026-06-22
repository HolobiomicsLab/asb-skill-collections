---
name: hierarchical-metabolite-annotation-mapping
description: Use when you have a metabolomics count data frame with metabolite identifiers (e.g., compound IDs, KEGG IDs) and wish to organize them into functional or taxonomic hierarchies for class-based statistical testing, fold-change stratification, or visualization by metabolic pathway or organism type.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3172
  tools:
  - R
  - KEGGREST
  - omu_summary
  - plot_volcano
  - plot_bar
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- Omu is an R package that enables rapid analysis of Metabolomics data sets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_omu_metabolomics_count_data_tool_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-metabolite-annotation-mapping

## Summary

Assign standardized hierarchical metabolite classifications (KEGG, KO_Number, Prokaryote, or Eukaryote ontologies) to a metabolomics count matrix to enable comparative analysis and visualization by metabolic class. This enables downstream statistical filtering, enrichment queries, and class-stratified plotting.

## When to use

You have a metabolomics count data frame with metabolite identifiers (e.g., compound IDs, KEGG IDs) and wish to organize them into functional or taxonomic hierarchies for class-based statistical testing, fold-change stratification, or visualization by metabolic pathway or organism type. Use this skill before running omu_summary or plot_volcano to enable filtering and coloring by metabolic class.

## When NOT to use

- Metabolite identifiers are already annotated with functional classes in your count frame—use directly without re-mapping.
- Your metabolite IDs are not KEGG identifiers and no KEGG API mapping is available for your identifier scheme.
- You require organism-level taxonomy rather than metabolic function; use Prokaryote or Eukaryote identifiers only if organism origin is known.

## Inputs

- metabolomics count data frame (rows=metabolites, columns=samples)
- metabolite identifier column (KEGG IDs, KO Numbers, or organism-specific identifiers)

## Outputs

- annotated count data frame with added 'Class' hierarchical column
- mapping of metabolites to KEGG pathway classes or organism-level functional groups

## How to apply

Call the assign_hierarchy function on your metabolomics count data frame, specifying the identifier scheme matching your metabolite IDs (KEGG, KO_Number, Prokaryote, or Eukaryote). Set keep_unknowns=TRUE to retain metabolites with no matching annotation; set it to FALSE if you want only annotated metabolites. The function retrieves hierarchical class data from the KEGG API (via KEGGREST) and adds class columns to your count frame. Verify that the resulting data frame includes a 'Class' column with expected metabolite categories (e.g., 'Organic acids', 'Carbohydrates'); unknown metabolites will be labeled 'Unknown' if keep_unknowns=TRUE. This annotated data frame then serves as input to omu_summary for differential abundance testing and plot_volcano for class-stratified visualization.

## Related tools

- **KEGGREST** (Retrieves hierarchical class data from the KEGG API via keggGet function calls during assignment)
- **omu_summary** (Consumes the hierarchical Class column to perform differential abundance tests stratified by metabolic class) — github.com/connor-reid-tiffany/Omu
- **plot_volcano** (Uses the Class column to color and filter volcano plot points by metabolic class (e.g., strpattern parameter)) — github.com/connor-reid-tiffany/Omu
- **plot_bar** (Visualizes metabolite counts aggregated by the assigned Class hierarchy) — github.com/connor-reid-tiffany/Omu

## Examples

```
assign_hierarchy(c57_nos2KO_mouse_countDF, identifier='KEGG', keep_unknowns=TRUE)
```

## Evaluation signals

- Resulting count data frame includes a new 'Class' column with non-null values for annotated metabolites
- Class values match expected KEGG pathway categories (Organic acids, Carbohydrates, Amino acids, etc.) or organism-level groups
- Metabolites with unmatched identifiers are labeled 'Unknown' if keep_unknowns=TRUE; row count is preserved
- Downstream omu_summary and plot_volcano calls execute without errors using the Class column as a grouping variable
- Class distribution (value counts) shows reasonable representation—no single class dominates unless expected from your metabolomics data

## Limitations

- Only four identifier schemes are supported: KEGG, KO_Number, Prokaryote, Eukaryote. Metabolites outside these schemes will be marked 'Unknown' or skipped if keep_unknowns=FALSE.
- Hierarchical assignment depends on live KEGG API availability (via KEGGREST); network failures or API rate limits may cause incomplete annotation.
- Metabolites with ambiguous or non-standard identifiers may fail to map and will be discarded or labeled 'Unknown', reducing effective sample size for downstream tests.
- The hierarchy depth and granularity are fixed by KEGG; custom multi-level hierarchies cannot be defined per your experimental design.

## Evidence

- [other] assign_hierarchy function call and identifier options: "To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
- [other] keep_unknowns parameter behavior: "identifier='KEGG' and keep_unknowns=TRUE"
- [other] KEGG API integration and data source: "which retrieves data from the KEGG API using the function ```keggGet``` from the package KEGGREST"
- [other] Class column output and downstream usage: "Call plot_volcano on the omu_summary output with column='Class', strpattern=c('Organic acids', 'Carbohydrates')"
- [other] Role in statistical testing workflow: "Assign hierarchical class data to the count dataframe using assign_hierarchy with identifier='KEGG' and keep_unknowns=TRUE"
