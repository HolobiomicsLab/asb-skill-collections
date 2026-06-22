---
name: functional-orthology-annotation
description: Use when after assigning hierarchical KEGG identifiers to a metabolomics count data frame (via assign_hierarchy with identifier='KEGG'), use this skill when you need to link metabolites to their functional roles (KO numbers) and associated genes for downstream functional analysis, pathway.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0821
  tools:
  - KEGGREST
  - R
  - assign_hierarchy
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- which retrieves data from the KEGG API using the function ```keggGet``` from the package KEGGREST
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

# functional-orthology-annotation

## Summary

Retrieve and annotate metabolite-associated functional orthology (KO numbers) and gene names from the KEGG API using S3 dispatch methods. This skill augments metabolomics count data frames with ortholog identifiers and gene information to enable functional interpretation of metabolite variation.

## When to use

After assigning hierarchical KEGG identifiers to a metabolomics count data frame (via assign_hierarchy with identifier='KEGG'), use this skill when you need to link metabolites to their functional roles (KO numbers) and associated genes for downstream functional analysis, pathway enrichment, or gene-centric interpretation of metabolic shifts.

## When NOT to use

- Input data frame does not contain KEGG compound identifiers or hierarchical metadata from assign_hierarchy
- KEGG API is unavailable or rate-limited; consider caching results or using offline KEGG databases
- Metabolite identifiers are from non-KEGG databases (e.g., PubChem, ChEBI, or other resources); use database-specific annotation retrieval instead

## Inputs

- metabolomics count data frame with KEGG compound identifiers
- hierarchical metadata columns (output from assign_hierarchy with identifier='KEGG')

## Outputs

- augmented metabolomics data frame with new functional orthology (KO number) columns
- augmented metabolomics data frame with new gene name columns

## How to apply

Call the KEGG_gather S3 method on a KEGG-annotated metabolomics data frame. The function dispatches based on the S3 class determined by existing metadata columns from assign_hierarchy. For each metabolite's KEGG compound ID, the method invokes keggGet from the KEGGREST package to query the KEGG API and retrieve functional orthology (KO numbers) and associated gene information. The returned KEGG records are parsed and cleaned using the internal make_omelette function to extract KO identifiers and gene names into structured format. Finally, the cleaned data is formatted via plate_omelette S3 method and new orthology and gene columns are bound to the input data frame. Success requires active KEGG API access and properly formatted KEGG compound identifiers in the input data frame.

## Related tools

- **KEGGREST** (R package that provides the keggGet function to query the KEGG API and retrieve functional orthology and gene information for metabolite KEGG IDs)
- **R** (Programming language environment in which the Omu package and S3 method dispatch system operate)
- **assign_hierarchy** (Omu function that must be run prior to KEGG_gather to assign hierarchical class data and KEGG identifiers to the metabolomics data frame) — github.com/connor-reid-tiffany/Omu

## Examples

```
# Assuming hierarchical annotation already applied via assign_hierarchy
kegg_annotated_df <- KEGG_gather(metabolomics_df)
```

## Evaluation signals

- Output data frame retains all rows and columns from input, plus new KO and gene name columns with no row reordering
- KO numbers in output columns match KEGG API format (e.g., 'K12345') and are not empty for metabolites with valid KEGG IDs
- Gene names extracted correspond to the correct organisms and match KEGG API records (spot-check against manual KEGG queries)
- No rows have NA or missing values in KO/gene columns if corresponding KEGG ID was successfully queried
- Function completes without errors related to KEGG API connection or malformed KEGG identifiers in input

## Limitations

- Depends on active KEGG API availability; network failures or API downtime will cause the function to fail or return incomplete results
- Some metabolites may not have associated functional orthology (KO numbers) in KEGG; these will return NA or empty values
- KEGG API rate limiting may impact performance on large data frames with many unique metabolites; consider batching or caching
- Accuracy of orthology and gene annotations is only as current as the KEGG database at the time of query

## Evidence

- [other] The KEGG_gather S3 method retrieves data from the KEGG API using the keggGet function from the KEGGREST package to obtain functional orthology and gene names for metabolite-annotated data frames.: "retrieves data from the KEGG API using the keggGet function from the KEGGREST package to obtain functional orthology and gene names"
- [other] For each metabolite's KEGG ID, invoke keggGet from KEGGREST package to query the KEGG API and retrieve functional orthology (KO numbers) and associated gene information. Parse and clean the returned KEGG records using the internal make_omelette function to extract KO identifiers and gene names into a structured format.: "For each metabolite's KEGG ID, invoke keggGet from KEGGREST package to query the KEGG API and retrieve functional orthology (KO numbers) and associated gene information"
- [other] To gather functional orthology and gene data, Omu uses an S3 method called KEGG_gather, which retrieves data from the KEGG API: "To gather functional orthology and gene data, Omu uses an S3 method called KEGG_gather"
- [other] To assign hierarchical class data, use the assign_hierarchy function and pick the correct identifier, either 'KEGG', 'KO_Number', 'Prokaryote', or 'Eukaryote': "use the assign_hierarchy function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
- [other] Bind the new orthology and gene columns to the input data frame and return the augmented result.: "Bind the new orthology and gene columns to the input data frame and return the augmented result"
