---
name: lipid-nomenclature-simplification
description: Use when you have spatial metabolomics data with semicolon-delimited isomer name annotations (such as the 'all_IsomerNames' column in SpaMTP Seurat objects) and you need to reduce annotation complexity before pathway analysis, statistical testing, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - dplyr
  - tidyr
  - ggplot2
  - R
  - Seurat
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-nomenclature-simplification

## Summary

Simplify complex lipid nomenclature annotations into standardized Lipid Maps categories and classes, reducing annotation redundancy while preserving metabolite identity. This skill is essential when spatial metabolomic datasets contain multiple isomer names per m/z and you need a unified, interpretable annotation system for downstream analysis.

## When to use

Apply this skill when you have spatial metabolomics data with semicolon-delimited isomer name annotations (such as the 'all_IsomerNames' column in SpaMTP Seurat objects) and you need to reduce annotation complexity before pathway analysis, statistical testing, or visualization. Use it specifically when individual m/z values map to many structurally similar lipids and you want to collapse them into common Lipid Maps categories (e.g., 'PC', 'PE', 'TG') to enable robust biological interpretation.

## When NOT to use

- Input annotations are already simplified to single lipid classes; redundant simplification adds no value.
- Downstream analysis requires full structural specificity (e.g., stereoisomer or positional isomer distinction); collapsing to classes loses resolution.
- Non-lipid metabolites dominate the dataset; RefineLipids is lipid-specific and will return mostly NA, requiring separate handling.

## Inputs

- Seurat object with Spatial assay containing semicolon-delimited isomer name annotations
- Metadata dataframe with annotation column (e.g., 'all_IsomerNames')
- Annotation column name (string)

## Outputs

- Refined lipid annotations dataframe with m/z → simplified Lipid Maps category mapping
- Summary table with per-m/z annotation counts before and after refinement
- Simplified annotation column with NA values for non-lipid metabolites

## How to apply

Load the spatial metabolomics Seurat object and extract the assay metadata containing the semicolon-delimited annotation column (e.g., 'all_IsomerNames'). Call RefineLipids() on this metadata with parameters annotation.column set to the target column name and lipid_info='simple' to map complex isomer nomenclature to Lipid Maps lipid classes and categories. The function processes each annotation string, identifies lipid entities, and returns simplified class labels; non-lipid metabolites are assigned NA. After refinement, count annotations per m/z before and after to verify the reduction magnitude (the article reports maximum reductions from 161 to 1 annotation per m/z). Validate that the refined dataframe preserves the m/z-to-annotation mapping and that NA values appear only for non-lipid metabolites.

## Related tools

- **SpaMTP** (R package containing RefineLipids() function for lipid nomenclature simplification; invoked on Spatial assay metadata) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Data container and access framework for spatial metabolomics objects; metadata extraction and assay structure)
- **dplyr** (Annotation count aggregation and per-m/z summary table generation)
- **tidyr** (Handling and reshaping semicolon-delimited annotation strings for before/after comparison)

## Examples

```
refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email], annotation.column='all_IsomerNames', lipid_info='simple')
```

## Evaluation signals

- Refined annotation column contains only recognized Lipid Maps categories (e.g., 'PC', 'PE', 'TG', 'CE') or NA for non-lipids; no partial or malformed class names.
- Per-m/z annotation count after refinement is ≤ count before refinement; maximum reduction aligns with reported magnitude (161 → 1 in test dataset).
- All NA values in refined column correspond to metabolites not recognized as lipids; no legitimate lipid annotations become NA.
- Spatial assay metadata structure and m/z indexing are preserved; refined annotations map 1:1 back to original m/z values.
- Semicolon-delimited isomer strings are fully collapsed into single simplified class labels per m/z (no residual commas or multiple classes in a single cell).

## Limitations

- RefineLipids is lipid-specific; non-lipid metabolites (e.g., amino acids, nucleotides) are assigned NA and require separate annotation or handling.
- Simplification to Lipid Maps categories discards structural isomer and positional information; applications requiring stereochemical detail cannot use the simplified output.
- Nomenclature mapping depends on accuracy of input isomer name strings and Lipid Maps reference database; malformed or unrecognized lipid names may fail to map.

## Evidence

- [methods] RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes: "RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes"
- [methods] Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings; Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames' and lipid_info='simple': "Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings. 4. Call RefineLipids() on the assay metadata with"
- [methods] Count the number of annotations per m/z after refinement, handling NA values for non-lipid metabolites: "Count the number of annotations per m/z after refinement, handling NA values for non-lipid metabolites."
- [methods] The available document text does not contain explicit quantitative results stating the annotation reduction from 161 to 1 when running RefineLipids: "The available document text does not contain explicit quantitative results stating the annotation reduction from 161 to 1"
- [readme] SpaMTP is an R package designed for the integrative analysis of spatial metabolomics and spatial transcriptomics data: "SpaMTP is an R package designed for the integrative analysis of spatial metabolomics and spatial transcriptomics data"
