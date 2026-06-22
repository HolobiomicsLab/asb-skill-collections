---
name: sample-batch-balancing-across-classification-dimensions
description: Use when designing multi-batch LC/GC-MS experiments where samples belong to multiple groups or conditions and you need to ensure that each injection plate receives a balanced representation of all groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - InjectionDesign
  techniques:
  - GC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-batch-balancing-across-classification-dimensions

## Summary

A method to distribute samples across LC/GC-MS injection plates such that user-defined classification dimensions (e.g., sample group, experimental condition) are evenly represented within each batch, while preserving randomization within batches to control for instrument drift and technical variation.

## When to use

Apply this skill when designing multi-batch LC/GC-MS experiments where samples belong to multiple groups or conditions and you need to ensure that each injection plate receives a balanced representation of all groups. This is critical when batch effects or instrument drift could confound group-level inference and you cannot randomize all samples on a single plate.

## When NOT to use

- Samples can all fit on a single injection plate without batch constraints; batch balancing is unnecessary if no batch effect is expected.
- The balance dimension is unknown or not defined in the sample metadata; the algorithm requires explicit specification of which dimension to balance across batches.
- Sample counts per group are too small (e.g., <1 sample per group per plate) to achieve meaningful inter-batch balance; the method assumes sufficient replication within each group.

## Inputs

- Sample metadata table (Excel or TSV) with sample ID, classification dimensions (balance dimension, randomization dimension), and sample group/condition
- Balance dimension specification (e.g., column name for sample group or treatment condition)
- Randomization dimension specification (e.g., column name for replicate ID or technical variable)

## Outputs

- Injection-Plate Layout table with columns: batch ID, injection order, sample ID, metadata, and QC sample positions
- Visualized distribution sequence showing sample assignment across batches and within-batch randomization order
- Downloadable worksheet(s) in platform-native format for each plate or all plates combined

## How to apply

First, parse the sample metadata table and extract the balance dimension (e.g., sample group, treatment condition) and the randomization dimension (e.g., replicate ID, technical variable). Group samples by the balance dimension and calculate the target number of samples from each group that should appear on each plate to achieve inter-batch balance. Assign samples to batches such that each batch receives a proportionally balanced representation of the balance dimension. Within each batch, apply randomization by the randomization dimension to shuffle sample injection order while preserving the batch-level balance constraint. Finally, generate and export the Injection-Plate Layout table with columns for batch ID, injection order, sample ID, and metadata. The system displays the final visualized distribution in real time, allowing iterative adjustment.

## Related tools

- **InjectionDesign** (Platform for uploading sample metadata, defining balance and randomization dimensions, performing inter-batch balancing and intra-batch randomization, and exporting final Injection-Plate Layout.) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Verify that the count of samples from each balance-dimension group is equal (or near-equal) across all generated batches; no batch should be depleted of any group.
- Confirm that within each batch, the randomization dimension is shuffled (i.e., injection order does not follow the sorted order of the randomization dimension).
- Check that the final Injection-Plate Layout table contains all input samples with no duplicates or missing rows, and that batch IDs and injection orders are consistent with plate capacity constraints.
- Visually inspect the real-time distribution graph to confirm that sample groups are evenly distributed across batches before export.
- Validate that QC sample positions are correctly inserted according to the predefined QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC) and do not displace sample counts.

## Limitations

- Maximum of three classification dimensions can be visually presented in the sample list; if more dimensions are critical, additional metadata must be managed outside the tool.
- Balance is achieved only for the explicitly defined balance dimension; secondary or tertiary groupings are not simultaneously optimized.
- If sample counts per group are highly imbalanced (e.g., one group has 1 sample and another has 100), perfect inter-batch balance may be impossible; the algorithm does not handle such extreme imbalances.
- The tool requires JDK 17, MongoDB 4.2+, and Redis 5+ for local deployment; cloud-based or shared instances may have different latency and scalability characteristics.

## Evidence

- [other] InjectionDesign performs inter-batch balancing and intra-batch randomization by requiring users to define a balance dimension and a randomization dimension as input parameters for plate layout generation.: "InjectionDesign performs inter-batch balancing and intra-batch randomization by requiring users to define a balance dimension and a randomization dimension as input parameters for plate layout"
- [other] Group samples by balance dimension and calculate target distribution across batches to achieve inter-batch balance. Assign samples to batches such that each batch receives a balanced representation across the balance dimension.: "Group samples by balance dimension and calculate target distribution across batches to achieve inter-batch balance. Assign samples to batches such that each batch receives a balanced representation"
- [other] Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance.: "Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance."
- [readme] Users need to define the balance dimension and the randomization dimension separately. For each adjustment, the system displays the final visualized distribution sequence in real time.: "Users need to define the balance dimension and the randomization dimension separately. For each adjustment, the system displays the final visualized distribution sequence in real time."
- [intro] InjectionDesign supports visual presentation of up to three classification dimensions for sample lists: "InjectionDesign supports visual presentation of up to three classification dimensions for sample lists"
