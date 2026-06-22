---
name: m-z-annotation-reduction-quantification
description: Use when you have spatial metabolomics data with semi-colon-delimited multi-isomer annotations (e.g., 'all_IsomerNames' column in SpaMTP Seurat objects) and you want to quantify the benefit of RefineLipids simplification with lipid_info='simple' parameter.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - dplyr
  - tidyr
  - ggplot2
  - R
  - RefineLipids
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- library(dplyr)
- library(tidyr)
- library(ggplot2)
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z annotation reduction quantification

## Summary

Quantify the magnitude of annotation simplification achieved by applying RefineLipids lipid nomenclature simplification to spatial metabolomics annotations. This skill measures how many distinct lipid isomers or nomenclature variants collapse into unified Lipid Maps categories and classes per m/z value.

## When to use

Apply this skill when you have spatial metabolomics data with semi-colon-delimited multi-isomer annotations (e.g., 'all_IsomerNames' column in SpaMTP Seurat objects) and you want to quantify the benefit of RefineLipids simplification with lipid_info='simple' parameter. Use it to validate the annotation reduction efficiency reported in the literature or to assess annotation complexity before and after nomenclature harmonization in your own spotted or imaging MS dataset.

## When NOT to use

- Input is non-lipid metabolite annotations (e.g., proteins, carbohydrates) — RefineLipids targets lipid nomenclature specifically and will return NA for non-lipid compounds
- Annotation column is already simplified to single entries per m/z — no reduction to measure
- You need to preserve all isomer-level detail for structure elucidation — RefineLipids deliberately collapses isomers into categories, losing specificity

## Inputs

- SpaMTP Seurat object with pre-annotated Spatial assay metadata
- Multi-isomer annotation column (semicolon-delimited strings, e.g., 'all_IsomerNames')
- Lipidmaps reference database (optional, for validation)

## Outputs

- Refined lipid annotations dataframe with simplified Lipid Maps categories
- Summary table with columns: m/z, base_count (pre-refinement), refined_count (post-refinement), reduction_magnitude
- Maximum annotation reduction value per m/z
- Metadata on NA handling (non-lipid metabolites excluded from counts)

## How to apply

Load the annotated spatial metabolomics assay (e.g., spotted mouse liver dataset from Zenodo) and extract the metadata column containing multi-isomer annotations. Count the number of distinct annotation entries per m/z by splitting semicolon-delimited strings and excluding NA values for non-lipid metabolites. Call RefineLipids(assay_metadata, annotation.column='all_IsomerNames', lipid_info='simple') to collapse lipid nomenclature into Lipid Maps categories and classes. Re-count distinct annotations per m/z after refinement using the same method, handling NA values consistently. Calculate the reduction as base_count minus refined_count for each m/z, then identify the maximum reduction value and generate a summary table comparing pre- and post-refinement annotation counts. This quantification validates whether the reported reduction (e.g., 161→1) is reproducible and identifies which m/z values benefit most from simplification.

## Related tools

- **RefineLipids** (Simplifies lipid nomenclature into Lipid Maps categories and classes via lipid_info parameter) — https://github.com/GenomicsMachineLearning/SpaMTP
- **SpaMTP** (Container for Spatial assay metadata and host of RefineLipids function) — https://github.com/GenomicsMachineLearning/SpaMTP
- **dplyr** (Summarize and count annotation entries per m/z before/after refinement)
- **tidyr** (Reshape and pivot annotation counts for comparison tables)
- **R** (Execute counting and validation logic via string splitting and NA handling)

## Examples

```
refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email], annotation.column='all_IsomerNames', lipid_info='simple'); base_counts <- spotted@assays$[redacted-email] %>% count_annotations(); refined_counts <- refined_lipid_annotations %>% count_annotations(); summary_table <- tibble(mz = names(base_counts), base_count = base_counts, refined_count = refined_counts, reduction = base_count - refined_count)
```

## Evaluation signals

- base_count ≥ refined_count for all m/z values (refinement should only consolidate, never expand annotations)
- Maximum reduction value aligns with reported literature values (e.g., 161→1 for spotted dataset) or is documented in output table
- NA handling is consistent: non-lipid metabolites excluded from both pre- and post-refinement counts, and reported separately
- All semicolon-delimited isomer names in the base annotations are correctly parsed and counted (spot-check row with known isomer count)
- Refined annotations conform to Lipid Maps nomenclature (category:class format, e.g., 'Glycerophospholipids:Phosphatidylcholines')

## Limitations

- The article does not provide explicit quantitative results confirming the 161→1 reduction on the spotted dataset; reproducibility requires independent execution
- RefineLipids only simplifies lipid nomenclature; non-lipid metabolites return NA and are excluded from reduction counts, limiting scope to lipid-only analysis
- Reduction magnitude depends on diversity of isomer names in the original annotation; sparse or already-simplified annotations will show minimal reduction
- The method assumes semicolon-delimited format for multi-isomer annotations; other delimiters or formats require preprocessing

## Evidence

- [methods] Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings.: "Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings."
- [methods] Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames' and lipid_info='simple' to simplify lipid nomenclature into Lipid Maps categories and classes.: "Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames' and lipid_info='simple' to simplify lipid nomenclature into Lipid Maps categories and classes."
- [methods] Count the number of annotations per m/z after refinement, handling NA values for non-lipid metabolites.: "Count the number of annotations per m/z after refinement, handling NA values for non-lipid metabolites."
- [methods] RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes: "RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes"
- [methods] Load the spotted mouse liver dataset (SpaMTP Seurat object with pre-annotated m/z values) from Zenodo.: "Load the spotted mouse liver dataset (SpaMTP Seurat object with pre-annotated m/z values) from Zenodo."
