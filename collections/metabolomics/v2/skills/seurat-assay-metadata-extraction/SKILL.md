---
name: seurat-assay-metadata-extraction
description: Use when you have a SpaMTP Seurat object with a 'Spatial' assay containing metabolomics features (m/z values) and their associated metadata columns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SpaMTP
  - dplyr
  - tidyr
  - ggplot2
  - R
  - Seurat
  - Cardinal
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

# Seurat Assay Metadata Extraction

## Summary

Extract feature-level metadata (m/z values, annotation columns, and derived attributes) from a Seurat object's assay slot to enable downstream filtering, refinement, and statistical analysis of spatial metabolomics data. This skill bridges the gap between Cardinal MSI objects and Seurat-based annotation workflows by preserving and accessing feature-level metadata that would otherwise be inaccessible through standard Seurat accessors.

## When to use

Use this skill when you have a SpaMTP Seurat object with a 'Spatial' assay containing metabolomics features (m/z values) and their associated metadata columns (e.g., 'all_IsomerNames', adduct types, or lipid nomenclature), and you need to: (1) extract all annotations for a given m/z to apply lipid simplification or nomenclature refinement; (2) count annotation cardinality per feature before and after refinement to validate reduction; (3) filter features by annotation presence/quality; or (4) prepare metadata for statistical testing or pathway association. This is essential when the original Cardinal object's metadata was transferred during CardinalToSeurat conversion and must be accessed or manipulated in R data frames.

## When NOT to use

- Input Seurat object lacks a 'Spatial' assay or the assay contains no feature metadata (e.g., only intensities, no annotations) — use direct Cardinal object access instead.
- You only need to access intensity values or spatial coordinates, not feature-level annotations — use standard Seurat accessors (GetAssayData, GetTissueCoordinates) instead.
- The original Cardinal object is still available and you need to preserve its complete provenance — work directly with Cardinal assay metadata rather than the Seurat conversion.

## Inputs

- SpaMTP Seurat object with 'Spatial' assay (containing normalized m/z intensities)
- Seurat assay slot containing feature metadata ([redacted-email])
- Annotation column name(s) as strings (e.g., 'all_IsomerNames')

## Outputs

- R data frame with m/z values as row names and metadata columns (e.g., isomer names, lipid classes, adduct types)
- Optionally: filtered or transformed metadata for downstream analysis (e.g., count of annotations per m/z, simplified lipid nomenclature)

## How to apply

Access the feature metadata of a Seurat spatial assay using `object@assays$[redacted-email]`, which returns an R data frame indexed by feature names (m/z values as row names). Each row corresponds to one m/z feature; each column represents a metadata attribute (e.g., 'all_IsomerNames' containing semicolon-delimited isomer strings, or other annotation columns). Use standard R data frame operations (dplyr::select, tidyr::separate_rows, base R subsetting) to extract, filter, or transform specific columns. For example, to count annotations per m/z, split the semicolon-delimited strings using tidyr::separate_rows and count unique metabolite entries per m/z; to prepare for RefineLipids, pass the extracted metadata frame with the target annotation column specified (annotation.column='all_IsomerNames'). Validate the extraction by checking row count (should equal total m/z features in the object) and confirming that NA values are preserved for non-lipid or unannotated metabolites. The extracted data frame can then be manipulated independently or re-assigned to the assay slot after refinement.

## Related tools

- **SpaMTP** (Provides CardinalToSeurat conversion and RefineLipids function for downstream refinement of extracted metadata) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Object model and assay slot architecture for storing and accessing feature metadata) — https://satijalab.org/seurat/
- **dplyr** (Data frame manipulation and filtering (select, filter, mutate operations on extracted metadata))
- **tidyr** (Reshaping and splitting of semicolon-delimited annotation strings (separate_rows))
- **Cardinal** (Original MSI object model from which metadata is transferred via CardinalToSeurat) — https://github.com/Vitek-Lab/Cardinal3-vignettes

## Examples

```
# Extract metadata from Seurat spatial assay and prepare for RefineLipids
refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email], annotation.column='all_IsomerNames', lipid_info='simple')
```

## Evaluation signals

- Row count of extracted data frame equals total number of m/z features in the Seurat object (verify with nrow(metadata_df) == nrow(GetAssayData(object, slot='counts')))
- Row names of extracted data frame match the feature names of the Seurat object (verify with identical(rownames(metadata_df), rownames(GetAssayData(object))))
- Annotation columns contain expected content: semicolon-delimited isomer strings, NA values for unannotated m/z, or simplified lipid nomenclature after RefineLipids application
- After splitting semicolon-delimited annotations (tidyr::separate_rows), the maximum count of unique annotations per m/z matches the reported reduction metric (e.g., 161 unique annotations before refinement)
- No unexpected NA patterns or all-NA columns, indicating metadata was correctly transferred during CardinalToSeurat conversion

## Limitations

- Metadata preservation depends entirely on successful transfer during CardinalToSeurat conversion; if the original Cardinal object lacked complete metadata, extraction will yield incomplete data.
- Semicolon-delimited annotation strings (e.g., 'all_IsomerNames') must be consistently formatted; inconsistent delimiters or embedded semicolons will cause splitting errors during downstream refinement.
- NA values in feature metadata are preserved but require explicit handling (e.g., na.omit or dplyr::filter(!is.na(column))) to avoid errors in count operations or refinement functions.
- The article notes that the CardinalToSeurat conversion module is incompletely documented ('Unable to produce a finding — the provided section text contains only a README header'); exact behavior regarding edge cases (e.g., non-lipid metabolites, missing spatial coordinates) is not fully specified.

## Evidence

- [methods] Extract the Spatial assay metadata containing the 'all_IsomerNames' annotation column.: "Extract the Spatial assay metadata containing the 'all_IsomerNames' annotation column."
- [methods] Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames' and lipid_info='simple' to simplify lipid nomenclature into Lipid Maps categories and classes.: "Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames' and lipid_info='simple' to simplify lipid nomenclature"
- [methods] Preserve feature metadata (m/z values) in the feature meta.data slot.: "preserve feature metadata (m/z values) in the feature meta.data slot"
- [other] Runs lipid nomenclature simplification on annotations: refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email]: "refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email]"
- [methods] Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings.: "Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings."
