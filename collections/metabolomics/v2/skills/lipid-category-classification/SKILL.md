---
name: lipid-category-classification
description: Use when a spatial metabolomics dataset contains semicolon-delimited isomer name annotations (e.g., 'all_IsomerNames' column in SpaMTP Seurat objects) and you need to collapse multiple lipid nomenclature variants into their parent lipid categories and classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - SpaMTP
  - dplyr
  - tidyr
  - ggplot2
  - R
  - Seurat
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

# Lipid Category Classification

## Summary

Simplifies complex lipid nomenclature annotations into standardized Lipid Maps categories and classes using the RefineLipids function. This skill reduces annotation redundancy in spatial metabolomics datasets, enabling clearer biological interpretation when multiple isomers or nomenclature variants map to the same lipid category.

## When to use

Apply this skill when a spatial metabolomics dataset contains semicolon-delimited isomer name annotations (e.g., 'all_IsomerNames' column in SpaMTP Seurat objects) and you need to collapse multiple lipid nomenclature variants into their parent lipid categories and classes. Particularly useful when annotation complexity obscures biological patterns or when downstream pathway analysis requires standardized lipid identities rather than exhaustive isomer enumeration.

## When NOT to use

- Input annotations are already in standardized Lipid Maps format with no isomer disambiguation needed
- Dataset contains primarily non-lipid metabolites with sparse lipid annotations
- Downstream analysis requires preservation of regioisomer or stereoisomer specificity (classification discards this granularity)

## Inputs

- Seurat object with Spatial assay containing metadata with semicolon-delimited isomer name annotations
- Annotation column (e.g., 'all_IsomerNames') with lipid nomenclature strings
- Assay metadata data.frame extracted from SpaMTP object

## Outputs

- Refined lipid annotations data.frame with Lipid Maps categories and classes
- Summary table of annotation counts per m/z before and after refinement
- Updated Seurat object with simplified lipid nomenclature in assay metadata

## How to apply

Extract the annotation metadata column containing semicolon-delimited lipid isomer names from the Spatial assay. Call RefineLipids() on this metadata with parameters annotation.column specifying the source column and lipid_info='simple' to map nomenclature to Lipid Maps lipid categories and classes. Count annotations per m/z before and after refinement (handling NA values for non-lipid metabolites) to quantify reduction. The function consolidates isomer variants into canonical lipid categories, which facilitates downstream statistical and pathway analyses. Validate by comparing the maximum annotation reduction against expected thresholds—the article demonstrates reductions from 161 to 1 annotation per m/z in optimal cases.

## Related tools

- **SpaMTP** (Provides RefineLipids() function for lipid nomenclature simplification and hosts Seurat-based data structures for spatial metabolomic analysis) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Supplies the Seurat class object framework and assay metadata infrastructure that RefineLipids operates on)
- **dplyr** (Used for counting and summarizing annotation statistics (grouping, summarization of before/after counts))
- **tidyr** (Handles data reshaping when splitting and recombining semicolon-delimited annotation strings)

## Examples

```
refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email], annotation.column='all_IsomerNames', lipid_info='simple')
```

## Evaluation signals

- Annotation count per m/z is reduced (ideally to 1 or a small fixed number) after refinement for lipid m/z values
- No NA values introduced for lipid metabolites; non-lipid metabolites retain NA values appropriately
- Refined annotations conform to Lipid Maps nomenclature standards (e.g., 'Triacylglycerol', 'Phosphatidylcholine')
- Downstream pathway analysis or differential expression results show improved clarity or statistical power compared to pre-refinement annotations
- Manual spot-check of 5–10 representative m/z values confirms correct mapping from isomer names to parent lipid categories

## Limitations

- RefineLipids simplification is irreversible; regioisomer and stereoisomer information is lost, limiting use cases requiring fine structural discrimination
- Function assumes semicolon-delimited isomer names in a single column; alternative annotation formats (e.g., JSON, separate rows per isomer) require preprocessing
- Lipid Maps database coverage is incomplete; non-standard or novel lipid species may not be recognized and will return NA
- Classification performance depends on upstream annotation accuracy; erroneous isomer names propagate into refined classifications

## Evidence

- [methods] Lipid nomenclature simplification: "RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes"
- [methods] RefineLipids function call with lipid_info parameter: "refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email]"
- [methods] Annotation reduction from 161 to 1: "annotation reduction from 161 to 1 when running RefineLipids with lipid_info=simple on the spotted dataset"
- [methods] Task workflow describing pre/post-refinement quantification: "Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings"
