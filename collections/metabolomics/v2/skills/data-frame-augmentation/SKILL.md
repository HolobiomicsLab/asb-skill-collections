---
name: data-frame-augmentation
description: Use when after assign_hierarchy has added KEGG compound identifiers and hierarchical metadata to your metabolomics count data frame, and you need to link metabolites to their functional orthologs (KO numbers) and gene names for pathway or functional enrichment analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3172
  tools:
  - KEGGREST
  - R
  - Omu
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
---

# data-frame-augmentation

## Summary

Augment a metabolomics count data frame with functional orthology and gene information retrieved from the KEGG API via S3 dispatch. This enriches metabolite-annotated tables with KO numbers and associated gene names to enable downstream functional analysis.

## When to use

After assign_hierarchy has added KEGG compound identifiers and hierarchical metadata to your metabolomics count data frame, and you need to link metabolites to their functional orthologs (KO numbers) and gene names for pathway or functional enrichment analysis.

## When NOT to use

- Input data frame lacks KEGG compound identifiers or hierarchical metadata — run assign_hierarchy first
- Your metabolites use alternative identifiers (e.g., PubChem CIDs, InChI keys) rather than KEGG compound IDs
- You need gene expression data rather than functional orthology annotations — KEGG_gather returns annotation only

## Inputs

- metabolomics count data frame with KEGG compound identifiers
- hierarchical metadata columns (output from assign_hierarchy)
- S3 class metadata indicating data frame structure

## Outputs

- augmented data frame with original columns plus new KO (functional orthology) columns
- augmented data frame with original columns plus new gene name columns

## How to apply

Call the KEGG_gather S3 method on your metabolite-annotated data frame. The method dispatches based on the S3 class determined by existing metadata columns. For each metabolite's KEGG ID, keggGet from the KEGGREST package queries the KEGG API to retrieve functional orthology (KO numbers) and gene information. The internal make_omelette function parses and cleans the returned KEGG records to extract KO identifiers and gene names into a structured format. The plate_omelette S3 method then formats the cleaned data according to your data frame class. Finally, bind the new orthology and gene columns to the input data frame and return the augmented result.

## Related tools

- **KEGGREST** (R package providing keggGet function to query KEGG API for functional orthology and gene information)
- **R** (Host language for S3 dispatch and data frame manipulation)
- **Omu** (Metabolomics analysis package implementing KEGG_gather S3 method and associated helper functions) — github.com/connor-reid-tiffany/Omu

## Examples

```
KEGG_gather(metabolite_df)
```

## Evaluation signals

- Output data frame has same number of rows as input (no metabolites dropped)
- New columns for KO identifiers and gene names are present and non-empty where KEGG records were found
- KO column values match expected KEGG Orthology identifier format (e.g., 'K' followed by digits)
- Gene names are character vectors with non-null values corresponding to annotated metabolites
- No NA values introduced in pre-existing columns; only new columns contain NA where KEGG API returned no match

## Limitations

- Requires internet connectivity and KEGG API availability; API rate limits or downtime will block augmentation
- Only metabolites with valid KEGG compound identifiers will be enriched; others receive NA in new columns
- KEGG API coverage and gene naming conventions may not match all metabolites or all target organisms
- make_omelette and plate_omelette parsing depends on KEGG record format stability; API schema changes could break parsing

## Evidence

- [other] retrieves functional orthology and gene names from the KEGG API for metabolite-annotated data frames: "The KEGG_gather S3 method retrieves data from the KEGG API using the keggGet function from the KEGGREST package to obtain functional orthology and gene names for metabolite-annotated data frames."
- [other] For each metabolite's KEGG ID, invoke keggGet from KEGGREST package to query the KEGG API and retrieve functional orthology (KO numbers) and associated gene information.: "For each metabolite's KEGG ID, invoke keggGet from KEGGREST package to query the KEGG API and retrieve functional orthology (KO numbers) and associated gene information."
- [other] S3 method dispatch based on metadata columns and cleaning via make_omelette function: "Call KEGG_gather on the data frame, which dispatches based on the S3 class determined by existing metadata columns."
- [other] Parse and format results with plate_omelette before binding to input data frame: "Parse and clean the returned KEGG records using the internal make_omelette function to extract KO identifiers and gene names into a structured format."
- [other] To gather functional orthology and gene data, Omu uses an S3 method called KEGG_gather: "To gather functional orthology and gene data, Omu uses an S3 method called ```KEGG_gather```, which retrieves data from the KEGG API"
