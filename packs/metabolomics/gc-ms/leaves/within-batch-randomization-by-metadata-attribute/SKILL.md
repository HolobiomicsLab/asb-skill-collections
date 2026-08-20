---
name: within-batch-randomization-by-metadata-attribute
description: Use when you have already assigned samples to batches (inter-batch balance is fixed) and need to shuffle injection order within each batch to decorrelate sample properties from time-dependent instrumental effects. Use it when your metadata table includes a randomization dimension (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# within-batch-randomization-by-metadata-attribute

## Summary

Randomize sample injection order within each batch according to a user-specified metadata dimension (e.g., replicate ID, technical variable) to reduce systematic bias while preserving batch-level balance. This skill is critical for LC/GC-MS multi-omics experiments where injection sequence can introduce instrumental drift or carryover artifacts.

## When to use

Apply this skill when you have already assigned samples to batches (inter-batch balance is fixed) and need to shuffle injection order within each batch to decorrelate sample properties from time-dependent instrumental effects. Use it when your metadata table includes a randomization dimension (e.g., replicate label, technical treatment) that should govern the within-batch shuffle pattern.

## When NOT to use

- If samples have not yet been assigned to batches — apply inter-batch balancing first.
- If no metadata-driven randomization dimension is relevant to your experimental design (e.g., all samples are independent singletons with no replicate structure).
- If you require deterministic (non-randomized) injection order for regulatory or method-validation purposes.

## Inputs

- Sample metadata table (Excel or CSV) with sample IDs, batch assignments, and a designated randomization dimension column
- Pre-computed batch assignments from inter-batch balancing step
- Specification of randomization dimension (e.g., 'replicate_id', 'treatment_group')

## Outputs

- Injection-Plate Layout table with columns: batch ID, injection order (randomized), sample ID, and metadata
- Visualized distribution sequence showing randomized order per batch
- Downloadable worksheet(s) with final injection sequence per plate

## How to apply

After inter-batch balancing assigns samples to batches, extract the randomization dimension (e.g., replicate ID or technical variable) from the sample metadata. Within each batch independently, group or sort samples by the randomization dimension, then apply a randomization algorithm (e.g., Fisher-Yates shuffle or stratified randomization) to reorder samples while preserving the batch-level balance achieved in the prior step. The system should display the final shuffled injection sequence in real time so users can verify that balance is maintained and no systematic clustering by metadata attribute remains. Export the final Injection-Plate Layout with columns for batch ID, injection order, sample ID, and metadata.

## Related tools

- **InjectionDesign** (Primary tool for defining randomization dimension, executing within-batch shuffle, and generating visualized and exportable Injection-Plate Layout) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Verify that injection order within each batch is shuffled according to the randomization dimension (no time-correlated clustering by metadata attribute).
- Confirm that inter-batch balance from the prior step is preserved: each batch still contains the target distribution across the balance dimension.
- Check that the visualized distribution sequence shows no systematic patterns (e.g., all replicates of one condition clustered together) within a batch.
- Validate that all samples assigned to a batch appear exactly once in the randomized injection order with no duplicates or omissions.
- Export and inspect the worksheet to ensure batch ID, injection order, sample ID, and metadata columns are present and consistent.

## Limitations

- Randomization dimension must be a categorical or discrete metadata attribute; continuous variables may require binning or stratification first.
- Small batch sizes or highly imbalanced randomization dimensions may result in apparent clustering despite random shuffling; consider batch size and dimension cardinality when designing the experiment.
- The skill does not account for sample-level properties (e.g., solubility, ionization efficiency) that may still correlate with injection order; additional QC samples (Pooled QC, Blank QC) are recommended to detect residual instrumental effects.

## Evidence

- [other] Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance.: "Within each batch, apply randomization by the randomization dimension to shuffle sample order while preserving batch-level balance."
- [readme] Users need to define the balance dimension and the randomization dimension separately. For each adjustment, the system displays the final visualized distribution sequence in real time.: "Users need to define the balance dimension and the randomization dimension separately. For each adjustment, the system displays the final visualized distribution sequence in real time."
- [readme] Step3 Inter-batch balancing and intra-batch randomization: "Step3 Inter-batch balancing and intra-batch randomization"
- [other] Generate and export the final Injection-Plate Layout table with columns for batch ID, injection order, sample ID, and metadata.: "Generate and export the final Injection-Plate Layout table with columns for batch ID, injection order, sample ID, and metadata."
