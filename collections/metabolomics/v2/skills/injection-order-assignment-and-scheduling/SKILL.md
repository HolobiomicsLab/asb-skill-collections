---
name: injection-order-assignment-and-scheduling
description: Use when designing multi-batch LC/GC-MS experiments where you need to
  control for batch effects (e.g., instrument drift, reagent lot variation) and have
  identified both a balance dimension (e.g., sample group, treatment condition) and
  a randomization dimension (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - InjectionDesign
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2023.02.26.530140v1.article-info
  title: InjectionDesign
evidence_spans:
- LC/GC-MS-based Multi-Omics Injection-Plate Design Web Service
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_injectiondesign_cq
    doi: 10.1101/2023.02.26.530140v1.article-info
    title: InjectionDesign
  dedup_kept_from: coll_injectiondesign_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.02.26.530140v1.article-info
  all_source_dois:
  - 10.1101/2023.02.26.530140v1.article-info
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# injection-order-assignment-and-scheduling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assigns sample injection order across LC/GC-MS plates while maintaining inter-batch balance along one dimension and intra-batch randomization along another, ensuring robust experimental design for multi-omics studies. This skill prevents systematic bias across batches and instrument drift effects within batches.

## When to use

Use this skill when designing multi-batch LC/GC-MS experiments where you need to control for batch effects (e.g., instrument drift, reagent lot variation) and have identified both a balance dimension (e.g., sample group, treatment condition) and a randomization dimension (e.g., replicate ID, technical variable). Applicable when you have a sample metadata table with ≥2 categorical or ordinal columns and need to distribute samples across multiple injection plates such that each plate receives balanced representation.

## When NOT to use

- Input samples are from a single batch or single condition (no inter-batch balancing needed).
- The sample set has already been randomized and scheduled by another method; re-applying this skill may re-shuffle and undo prior design.
- Balance or randomization dimensions are not well-defined or not present in the metadata table.

## Inputs

- Sample metadata table (Excel or CSV) with sample ID, classification dimensions (≥2 columns for grouping and randomization)

## Outputs

- Injection-Plate Layout table with columns: batch ID, injection order, sample ID, metadata
- Visualized distribution sequence (real-time display per adjustment)
- Downloadable worksheet(s) one plate at a time or all plates combined

## How to apply

First, parse the sample metadata table and identify two design dimensions: the balance dimension (categorical grouping variable you want equally represented across plates) and the randomization dimension (variable used to shuffle order within plates while preserving balance). Group samples by the balance dimension and calculate the target distribution required across all batches to achieve inter-batch balance. Assign samples to batches such that each batch receives proportional representation from each group in the balance dimension. Within each batch, apply randomization by the randomization dimension to shuffle injection order, preserving the batch-level balance achieved in the previous step. Generate and export the final Injection-Plate Layout table with columns for batch ID, injection order, sample ID, and associated metadata. Validate that each batch contains the target representation of all balance dimension groups and that randomization has been applied consistently within batches.

## Related tools

- **InjectionDesign** (Primary tool for defining balance and randomization dimensions, computing inter-batch balancing, applying intra-batch randomization, and generating and exporting the final Injection-Plate Layout.) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Each batch contains the target count or proportion of samples from each balance dimension group (no group is over- or under-represented in any batch).
- The sum of samples across all batches equals the total sample count in the input metadata table.
- Within each batch, the injection order reflects randomization by the randomization dimension without clustering samples from the same randomization group.
- The final Injection-Plate Layout table contains no missing or duplicate sample IDs.
- Real-time visualization shows balanced distribution sequence and updates correctly when balance or randomization parameters are adjusted.

## Limitations

- The tool supports visual presentation of up to three classification dimensions; more complex metadata structures may not be fully visualized.
- Balance is achieved only for the single user-specified balance dimension; interactions between multiple balance dimensions are not automatically optimized.
- The skill assumes balance dimension and randomization dimension are non-overlapping and that the sample set is large enough to achieve meaningful balance across all batches.

## Evidence

- [other] InjectionDesign performs inter-batch balancing and intra-batch randomization by requiring users to define a balance dimension and a randomization dimension as input parameters for plate layout generation.: "InjectionDesign performs inter-batch balancing and intra-batch randomization by requiring users to define a balance dimension and a randomization dimension as input parameters"
- [other] Group samples by balance dimension and calculate target distribution across batches to achieve inter-batch balance. Assign samples to batches such that each batch receives a balanced representation across the balance dimension.: "Group samples by balance dimension and calculate target distribution across batches to achieve inter-batch balance. Assign samples to batches such that each batch receives a balanced representation"
- [other] Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance.: "Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance."
- [readme] Users need to define the balance dimension and the randomization dimension separately. For each adjustment, the system displays the final visualized distribution sequence in real time.: "Users need to define the balance dimension and the randomization dimension separately. For each adjustment, the system displays the final visualized distribution sequence in real time."
- [intro] InjectionDesign supports visual presentation of up to three classification dimensions for sample lists: "InjectionDesign supports visual presentation of up to three classification dimensions"
