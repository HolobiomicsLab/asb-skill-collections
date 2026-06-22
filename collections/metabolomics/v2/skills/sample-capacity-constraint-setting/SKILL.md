---
name: sample-capacity-constraint-setting
description: Use when when designing injection sequences for LC/GC-MS multi-omics experiments where you need to distribute samples across multiple plates and must account for mandatory QC sample positions (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, and custom QC).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - InjectionDesign
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
---

# sample-capacity-constraint-setting

## Summary

Configure plate-level sample capacity constraints in LC/GC-MS injection design by specifying the maximum number of analytical samples per plate (excluding QC samples) and plate geometry. This ensures balanced plate utilization and prevents QC sample overload during multi-omics injection-plate design.

## When to use

When designing injection sequences for LC/GC-MS multi-omics experiments where you need to distribute samples across multiple plates and must account for mandatory QC sample positions (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, and custom QC). Use this skill before inter-batch balancing if the total sample count exceeds a single plate's available positions after QC reservation.

## When NOT to use

- Sample count is already pre-assigned to fixed, immutable plate groups; capacity constraints should have been determined upstream.
- All samples fit on a single plate without QC sample conflicts; the skill adds overhead without benefit.
- QC sample positions are already hardcoded in the plate layout and cannot be adjusted; this skill assumes flexibility in QC placement.

## Inputs

- InjectionDesign template file with five predefined QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, custom QC) and color assignments
- Sample list with basic information (filled Excel template from Step 1)
- Plate specification (96-well, 384-well, or custom)

## Outputs

- Validated plate configuration object specifying: plate type, max analytical samples per plate (integer, excluding QC), layout direction, yAxis label format
- Calculated plate slot inventory (total_wells - QC_positions = available_analytical_slots per plate)
- Configuration saved in InjectionDesign project for use in Step 3 (inter-batch balancing)

## How to apply

In InjectionDesign Step 2, after assigning color markers to the five predefined QC types, specify the plate type (e.g., 96-well or 384-well) and set the maximum number of analytical samples per plate, explicitly excluding QC sample positions. The system uses this constraint to calculate how many analytical samples fit on each plate given the QC layout. Define layout direction (row-wise or column-wise injection order) and yAxis label format for downstream visualization. Validate that max_analytical_samples + total_QC_positions ≤ plate_total_wells; if violated, the system will reject the configuration or require plate count adjustment during balancing (Step 3).

## Related tools

- **InjectionDesign** (Web service that implements plate parameter configuration, capacity constraint storage, and validation during Step 2 (Design Parameters and Predefinition for QC samples position)) — github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Configuration submission succeeds without validation errors (plate_type and max_samples are non-null, max_samples is a positive integer ≤ plate capacity minus minimum QC count).
- Calculated available analytical slots per plate = (total_plate_wells - sum_of_QC_positions) ≥ specified max_analytical_samples; verify via system feedback or export worksheet inspection.
- When Step 3 (inter-batch balancing) is executed, the system respects the capacity constraint: no plate is assigned more than max_analytical_samples analytical samples, and QC samples fill reserved positions without overflow.
- Exported worksheet(s) in Step 4 show sample distribution across multiple plates with plate boundaries and QC marker colors consistent with the capacity and layout direction constraints.
- yAxis label format is applied consistently to all output plate visualizations and matches the configured format (e.g., row-wise or column-wise numbering).

## Limitations

- Plate capacity constraint does not account for sample-level exclusion criteria (e.g., failed QC samples or sample replicates); filtering must be applied in Step 1 before capacity planning.
- The skill assumes homogeneous plate geometry (all plates are the same type and size); mixed plate types across a single injection sequence are not supported.
- Constraint validation occurs at submission time only; if downstream steps (Step 3, balancing) fail due to insufficient capacity, the user must re-enter Step 2, modify constraints, and restart.
- Custom QC type positioning may introduce edge cases if the custom QC requirement varies per plate; the current workflow treats custom QC as a single type with uniform allocation.

## Evidence

- [readme] users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate: "users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate"
- [other] Set plate type (e.g., 96-well, 384-well) and specify the maximum number of analytical samples per plate (excluding QC samples): "Set plate type (e.g., 96-well, 384-well) and specify the maximum number of analytical samples per plate (excluding QC samples)"
- [readme] InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC: "InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC"
- [readme] Different QC type has be marked as different color. Besides, users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate: "Different QC type has be marked as different color. Besides, users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate"
