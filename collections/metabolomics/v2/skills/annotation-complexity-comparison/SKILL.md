---
name: annotation-complexity-comparison
description: Use when you have MS imaging or LC-MS data with pre-annotated m/z values that include multiple isomer or metabolite names per m/z (stored as semicolon-delimited or multi-record strings), and you want to measure whether a refinement step (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - SpaMTP
  - dplyr
  - tidyr
  - ggplot2
  - R
  - RefineLipids
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
---

# annotation-complexity-comparison

## Summary

Quantify and compare the reduction in annotation complexity (count of isomer/metabolite assignments per m/z) before and after applying lipid nomenclature simplification. This skill validates whether refinement strategies like RefineLipids successfully collapse redundant or over-specific lipid annotations into standardized categories.

## When to use

Apply this skill when you have MS imaging or LC-MS data with pre-annotated m/z values that include multiple isomer or metabolite names per m/z (stored as semicolon-delimited or multi-record strings), and you want to measure whether a refinement step (e.g., RefineLipids with lipid_info='simple') has meaningfully reduced annotation burden without losing critical structural information.

## When NOT to use

- Input annotations are already in a simplified or non-hierarchical form (e.g., already Lipid Maps class level only).
- Annotation column is sparse, missing, or contains no semicolon-delimited entries (no multi-assignment structure to simplify).
- The refinement tool (RefineLipids or equivalent) is not installed or the lipid_info parameter is not supported in your tool version.

## Inputs

- Seurat object or assay metadata with pre-annotated m/z values
- Annotation column containing semicolon-delimited isomer names or multi-record metabolite assignments (e.g., 'all_IsomerNames')
- RefineLipids parameter set: annotation.column name and lipid_info level (e.g., 'simple')

## Outputs

- Refined annotations dataframe with simplified lipid nomenclature
- Summary table with per-m/z base_count (before) and refined_count (after) columns
- Reduction statistics: per-m/z reduction magnitude, maximum reduction, mean reduction, and distribution

## How to apply

Count the number of unique annotations (isomers, metabolite names, or lipid classes) for each m/z before refinement by splitting delimited strings or tallying multi-record entries. Apply RefineLipids() with annotation.column (e.g., 'all_IsomerNames') and lipid_info='simple' to collapse lipid nomenclature into Lipid Maps categories and classes, or apply an equivalent simplification method. Recount annotations per m/z after refinement, handling NA values for non-lipid metabolites. Calculate per-m/z reduction as (base_count − refined_count), then aggregate to summary statistics (e.g., mean, max, distribution). Document the maximum and median reduction per m/z to validate the expected magnitude of simplification and detect edge cases (e.g., m/z values with zero or negative reduction).

## Related tools

- **RefineLipids** (Simplifies lipid nomenclature into common lipid categories and classes via the lipid_info parameter; applied to assay metadata annotation columns to collapse isomer/metabolite redundancy.) — https://github.com/GenomicsMachineLearning/SpaMTP
- **SpaMTP** (R package providing RefineLipids and related annotation functions; loads Seurat objects and manages assay metadata.) — https://github.com/GenomicsMachineLearning/SpaMTP
- **dplyr** (Used for grouping, counting, and summarizing annotation counts per m/z before and after refinement.)
- **tidyr** (Used for parsing and splitting delimited annotation strings into separate records for counting.)
- **ggplot2** (Used for visualization of reduction distributions (e.g., histogram or boxplot of per-m/z reduction magnitudes).)

## Examples

```
refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email], annotation.column='all_IsomerNames', lipid_info='simple'); summary_table <- data.frame(base_count = base_counts, refined_count = refined_counts, reduction = base_counts - refined_counts)
```

## Evaluation signals

- Base counts are consistently greater than or equal to refined counts for all m/z values (no negative reductions).
- Maximum reduction matches or approaches the reported benchmark (e.g., 161 → 1 in the spotted dataset study).
- Summary table schema is valid: contains m/z, base_count, refined_count, and reduction columns; row count equals unique m/z values.
- Refined annotations contain NA values only for non-lipid metabolites; lipid m/z values retain valid Lipid Maps class assignments.
- Reduction magnitude distribution (mean, median, quartiles) is reported and aligns with expected simplification scope for the dataset.

## Limitations

- The observed maximum reduction (e.g., 161 → 1) is specific to the spotted dataset's annotation depth; other datasets may exhibit smaller or larger reductions depending on m/z density and LCMS fragmentation patterns.
- RefineLipids with lipid_info='simple' collapses to Lipid Maps categories and classes only; structural isomerism within a class is lost, which may be undesirable for structure-activity or biomarker discovery studies.
- Handling of non-lipid metabolites and mixed-metabolite m/z entries requires explicit NA handling; incorrect handling may inflate or underestimate reduction counts.
- The article notes missing sections for 'Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data', suggesting alternative refinement pipelines are in development and may produce different reduction profiles.

## Evidence

- [other] The available document text does not contain explicit quantitative results stating the annotation reduction from 161 to 1 when running RefineLipids with lipid_info=simple on the spotted dataset.: "The available document text does not contain explicit quantitative results stating the annotation reduction from 161 to 1 when running RefineLipids with lipid_info=simple on the spotted dataset."
- [other] Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings. Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames' and lipid_info='simple' to simplify lipid nomenclature into Lipid Maps categories and classes. Count the number of annotations per m/z after refinement, handling NA values for non-lipid metabolites. Calculate the reduction in annotation count per m/z and identify the maximum reduction value.: "Count the number of annotations per m/z before refinement by splitting the semicolon-delimited isomer name strings. Call RefineLipids() on the assay metadata with annotation.column='all_IsomerNames'"
- [methods] RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes: "RefineLipids can be used to simplify the lipid nomenclature into common lipid categories and classes"
- [methods] Runs lipid nomenclature simplification on annotations refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email]: "Runs lipid nomenclature simplification on annotations refined_lipid_annotations <- RefineLipids(spotted@assays$[redacted-email]"
- [other] Output the refined annotations dataframe and a summary table showing base_count versus refined_count for validation against the reported 161→1 maximum reduction.: "Output the refined annotations dataframe and a summary table showing base_count versus refined_count for validation against the reported 161→1 maximum reduction."
