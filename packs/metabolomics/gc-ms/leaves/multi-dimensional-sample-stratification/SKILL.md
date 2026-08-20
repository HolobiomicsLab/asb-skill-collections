---
name: multi-dimensional-sample-stratification
description: Use when you have a parsed sample list with metadata (sample IDs, classification dimensions, QC designations) and need to generate a physical injection-plate layout that (1) will be run across multiple batches, (2) has a known confounding dimension (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3897
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - InjectionDesign
  - pandas / openpyxl
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-dimensional-sample-stratification

## Summary

This skill partitions a sample cohort across multiple batches while preserving balance along a primary stratification axis and randomizing along a secondary axis to control for batch effects in LC/GC-MS injection-plate experiments. It ensures that each batch receives a representative distribution of sample groups or conditions, mitigating systematic bias in multi-batch metabolomics and proteomics workflows.

## When to use

Apply this skill when you have a parsed sample list with metadata (sample IDs, classification dimensions, QC designations) and need to generate a physical injection-plate layout that (1) will be run across multiple batches, (2) has a known confounding dimension (e.g., sample group, treatment condition) that must be balanced across batches, and (3) has a secondary dimension (e.g., replicate ID, technical variable) along which you want to randomize within-batch order to minimize instrumental drift artifacts.

## When NOT to use

- Input sample list is not yet parsed or does not conform to the InjectionDesign template schema (missing required fields, incorrect data types, or unknown QC type designations).
- No clear balance dimension exists in the metadata, or the practitioner does not have domain knowledge to specify which dimension should be balanced versus randomized.
- Samples are already assigned to batches and the task is only to order samples within a single known batch (use within-batch randomization directly instead).

## Inputs

- Parsed sample list (JSON or CSV) with columns: sample_id, classification_dimension_1, classification_dimension_2 (optional), classification_dimension_3 (optional), qc_type
- Balance dimension parameter (e.g., 'sample_group' or 'treatment_condition')
- Randomization dimension parameter (e.g., 'replicate_id' or 'technical_variable')
- Batch count and max samples per batch (excluding QC samples)

## Outputs

- Injection-Plate Layout table (CSV or Excel worksheet) with columns: batch_id, injection_order, sample_id, classification_dimension_1, classification_dimension_2, classification_dimension_3, qc_type
- Visualized distribution sequence showing balance and randomization per batch
- Summary statistics (e.g., count of each balance-dimension category per batch)

## How to apply

First, parse the sample metadata table to identify the balance dimension (e.g., sample group or condition) and the randomization dimension (e.g., replicate ID or technical variable). Calculate the target count of samples per group within each batch to achieve inter-batch balance—e.g., if you have 60 samples across 3 groups and 2 batches, aim for 10 samples per group per batch. Assign samples to batches such that each batch receives its target representation across the balance dimension. Within each batch, apply randomization by shuffling sample order according to the randomization dimension while preserving the batch-level balance already achieved. Generate and export the final injection-plate layout table with columns for batch ID, injection order, sample ID, and associated metadata. Validate that the output achieves target balance by checking that the observed count of each balance-dimension category per batch matches the target.

## Related tools

- **InjectionDesign** (Executes inter-batch balancing and intra-batch randomization to generate the final injection-plate layout with real-time visualization of distribution sequence) — https://github.com/CSi-Studio/InjectionDesign
- **pandas / openpyxl** (Parses uploaded Excel sample list and validates structure against InjectionDesign template schema)

## Evaluation signals

- For each balance dimension category, verify that the observed count per batch equals the target count (e.g., if 10 samples per group per batch is the target, check that each batch has exactly 10 samples in each group).
- Confirm that the total number of samples across all batches equals the input sample count minus any excluded QC samples.
- Verify that no sample appears twice in the output layout and that the injection order within each batch is a permutation (no duplicates, no gaps).
- Inspect the randomization dimension within each batch to confirm that the sample order does not follow a systematic pattern (e.g., all replicates of one condition clustered together before randomization).
- Check that all QC samples are placed at their user-specified positions and are not disrupted by the balancing and randomization logic.

## Limitations

- Maximum of three classification dimensions are supported for visual presentation; if metadata contains >3 independent dimensions, only three can be displayed simultaneously.
- The skill assumes that balance and randomization dimensions are orthogonal (non-overlapping); if a sample has the same value in both dimensions, the outcome is undefined.
- The tool requires exact specification of balance and randomization dimensions; incorrect or ambiguous dimension names may result in no balancing being applied.
- Batch size is fixed by the 'max samples per batch' parameter; if the total sample count is not evenly divisible by the batch size, some batches will be smaller, potentially affecting balance.

## Evidence

- [other] InjectionDesign performs inter-batch balancing and intra-batch randomization by requiring users to define a balance dimension and a randomization dimension as input parameters for plate layout generation.: "InjectionDesign performs inter-batch balancing and intra-batch randomization by requiring users to define a balance dimension and a randomization dimension as input parameters for plate layout"
- [other] Group samples by balance dimension and calculate target distribution across batches to achieve inter-batch balance. Assign samples to batches such that each batch receives a balanced representation across the balance dimension. Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance.: "Group samples by balance dimension and calculate target distribution across batches to achieve inter-batch balance. Assign samples to batches such that each batch receives a balanced representation"
- [readme] For each adjustment, the system displays the final visualized distribution sequence in real time.: "For each adjustment, the system displays the final visualized distribution sequence in real time"
- [readme] Users need to define the balance dimension and the randomization dimension separately.: "Users need to define the balance dimension and the randomization dimension separately"
