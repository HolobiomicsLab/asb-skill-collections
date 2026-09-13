---
name: injection-order-direction-specification
description: Use when when configuring a multi-well plate design (96-well, 384-well,
  or other format) in InjectionDesign for LC/GC-MS analysis and you need to specify
  whether analytical samples and QC controls should be injected row-by-row or column-by-column.
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

# Injection-Order Direction Specification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Define the layout direction (row-wise or column-wise) for LC/GC-MS sample injection sequences across multi-well plates to control the physical order in which samples are analyzed. This parameter directly influences batch structure, randomization outcomes, and inter-batch balancing in high-throughput omics experiments.

## When to use

When configuring a multi-well plate design (96-well, 384-well, or other format) in InjectionDesign for LC/GC-MS analysis and you need to specify whether analytical samples and QC controls should be injected row-by-row or column-by-column. This choice is critical before defining inter-batch balancing and intra-batch randomization strategies, as the injection direction constrains how samples can be distributed and balanced across batches.

## When NOT to use

- Your instrument requires a fixed injection direction that cannot be modified—verify instrument compatibility before specifying direction in InjectionDesign.
- You have already finalized and committed to a specific inter-batch randomization or balancing strategy that depends on a different direction; changing direction mid-workflow may invalidate randomization logic.
- Your sample list has fewer samples than a single plate row or column; direction becomes irrelevant for single-row/single-column plate layouts.

## Inputs

- Sample list (uploaded Excel template with basic sample information)
- Plate type specification (e.g., 96-well, 384-well)
- QC type assignments with color coding (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, custom QC)
- Maximum samples per plate (excluding QC samples)

## Outputs

- Plate layout configuration with specified injection direction (row-wise or column-wise)
- Injection sequence order for all analytical and QC samples
- Visualized sample distribution across plate positions
- Exportable worksheet with final injection sequence

## How to apply

In InjectionDesign Step 2 (Design Parameters and Predefinition for QC samples position), after uploading your sample list and assigning color-coded QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, custom QC), select the layout direction parameter: choose row-wise to advance left-to-right across each row before moving to the next row, or column-wise to advance top-to-bottom down each column before moving to the next column. This directional constraint is then applied uniformly during Step 3 (Inter-batch balancing and intra-batch randomization), where the system visualizes how samples are distributed in real time. The direction you select affects which sample groupings can be balanced across batches and how the randomization algorithm permutes positions within the chosen direction, so verify that the visualized final distribution sequence aligns with your experimental design goals before exporting the worksheet.

## Related tools

- **InjectionDesign** (Web service in which layout direction is configured during Step 2 (Design Parameters and Predefinition for QC samples position) and applied during Step 3 (Inter-batch balancing and intra-batch randomization) to control the physical injection order across multi-well plates) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Verify that the chosen direction (row-wise or column-wise) is consistently applied to all sample positions in the visualized plate layout shown in InjectionDesign Step 3.
- Confirm that the injection sequence preview displays samples advancing in the specified direction (e.g., left-to-right for row-wise, top-to-bottom for column-wise) before export.
- Check that the exported worksheet's injection order column reflects the direction specification (samples should be ordered sequentially along the chosen axis).
- Validate that inter-batch balancing results respect the chosen direction; samples from the same balance dimension should be distributed according to the direction constraint.
- Cross-reference the final visualized distribution sequence with your experimental design documentation to ensure the direction choice supports your randomization and balancing goals.

## Limitations

- InjectionDesign applies the direction uniformly across all plates in the batch; if different plates require different directions, separate design workflows must be created.
- The direction specification alone does not guarantee optimal randomization; it is one constraint among several (balance dimension, randomization dimension, QC positioning) that together determine the final sequence.
- Direction choice may conflict with certain inter-batch balancing or intra-batch randomization strategies; the system displays conflicts in real-time visualization, but the user must resolve them manually by adjusting other parameters.
- Very small plates (e.g., fewer rows or columns than balance dimensions) may result in limited flexibility in applying the direction constraint; consult the visualized output to confirm feasibility.

## Evidence

- [readme] users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate: "users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate"
- [other] Define the layout direction (row-wise or column-wise injection order): "Define the layout direction (row-wise or column-wise injection order)"
- [readme] For each adjustment, the system displays the final visualized distribution sequence in real time: "For each adjustment, the system displays the final visualized distribution sequence in real time"
- [readme] InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC. Different QC type has be marked as different color: "InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC. Different QC type has be marked as different color"
