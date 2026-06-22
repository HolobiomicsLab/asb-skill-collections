---
name: plate-layout-parameter-configuration
description: Use when after uploading a sample list to InjectionDesign and before performing inter-batch balancing and intra-batch randomization.
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

# Plate Layout Parameter Configuration

## Summary

Configure plate type, sample capacity, injection order, and axis labeling in InjectionDesign to define the physical and logical layout constraints for LC/GC-MS injection plate design. This skill bridges sample list preparation and QC sample position predefinition by establishing the plate geometry and visualization parameters.

## When to use

After uploading a sample list to InjectionDesign and before performing inter-batch balancing and intra-batch randomization. Use this skill when you need to specify how many analytical samples fit on a single plate (excluding QC samples), choose between 96-well or 384-well plate formats, and define whether samples will be injected row-wise or column-wise to match your LC/GC-MS instrument's autosampler configuration.

## When NOT to use

- Plate parameters have already been frozen and inter-batch balancing has begun; reconfiguring mid-optimization will invalidate prior randomization assignments.
- Input sample list is empty or contains fewer samples than specified plate capacity; configuration will proceed but Step 3 randomization will be degenerate.
- Your LC/GC-MS autosampler does not support the chosen injection direction (row-wise vs. column-wise); verify instrument compatibility before finalizing configuration.

## Inputs

- Uploaded sample list with classification metadata (from Step 1)
- Plate type specification (96-well or 384-well)
- Target number of analytical samples per plate (excluding QC)
- Injection direction preference (row-wise or column-wise)
- yAxis label format choice

## Outputs

- Plate layout configuration object (stored in InjectionDesign project)
- Validated plate geometry and sample capacity constraints
- Layout direction and axis label mappings
- Configuration parameters passed to inter-batch balancing engine (Step 3)

## How to apply

In InjectionDesign Step 2 (Design Parameters and Predefinition for QC samples position), set the plate type (e.g., 96-well, 384-well) based on your physical plate format. Specify the maximum number of analytical samples per plate, excluding QC sample positions—this determines how many rows or columns remain available for experimental samples after QC slots are reserved. Define the layout direction (row-wise or column-wise) to match your autosampler's injection sequence capability. Configure the yAxis label format for plate visualization (typically row labels A–H for 96-well plates). These parameters constrain the optimization algorithms in Step 3 and determine the final worksheet structure in Step 4.

## Related tools

- **InjectionDesign** (Web service GUI for interactive plate layout configuration, QC type color assignment, and real-time validation of plate geometry constraints) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Plate type and maximum sample count are correctly reflected in the Step 2 configuration form and cannot be changed once inter-batch balancing begins.
- Layout direction (row-wise or column-wise) produces injection sequences in Step 3 that match the specified order—verify by inspecting the visualized distribution sequence in real time.
- yAxis label format renders correctly in the final worksheet download; row/column indices align with plate dimensions (e.g., A1–H12 for 96-well plate).
- Total positions available (plate capacity minus QC slots) match the constraint imposed during Step 3 randomization—no sample is assigned outside the configured bounds.
- Configuration survives validation checkpoint and allows progression to Step 3 without error messages about geometry mismatch or invalid plate type.

## Limitations

- InjectionDesign supports only standard plate formats (96-well, 384-well); non-standard or custom plate geometries are not configurable.
- The maximum sample count per plate is a static setting; dynamic adjustment during randomization is not supported—users must restart if capacity needs to change.
- yAxis label format is a display-only parameter; changing it after Step 3 randomization may cause misalignment between worksheet and internal plate coordinate system.
- Injection direction (row-wise vs. column-wise) is set globally for all plates in a project; mixed directions across plates are not supported.

## Evidence

- [readme] users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate: "users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate"
- [intro] Design Parameters and Predefinition for QC samples position: "Design Parameters and Predefinition for QC samples position"
- [readme] For each adjustment, the system displays the final visualized distribution sequence in real time: "For each adjustment, the system displays the final visualized distribution sequence in real time"
- [other] Set plate type (e.g., 96-well, 384-well) and specify the maximum number of analytical samples per plate (excluding QC samples): "Set plate type (e.g., 96-well, 384-well) and specify the maximum number of analytical samples per plate (excluding QC samples)"
