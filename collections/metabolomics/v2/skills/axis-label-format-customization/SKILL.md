---
name: axis-label-format-customization
description: Use when when designing injection plate layouts in InjectionDesign and needing to display sample positions with clear, domain-appropriate labels on the y-axis (e.g., row identifiers, well coordinates, or sample indices).
license: CC-BY-4.0
metadata:
  edam_topics: []
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

# axis-label-format-customization

## Summary

Configure the y-axis label format for plate visualization in LC/GC-MS injection design workflows to enhance readability and communicate sample organization across plate layouts. This customization is applied during QC predefinition to ensure that injection sequences are clearly labeled according to experimental requirements.

## When to use

When designing injection plate layouts in InjectionDesign and needing to display sample positions with clear, domain-appropriate labels on the y-axis (e.g., row identifiers, well coordinates, or sample indices). Apply this skill after selecting plate type and layout direction, but before finalizing inter-batch balancing and intra-batch randomization steps.

## When NOT to use

- When the plate layout has already been finalized and exported; re-configuring labels after Step 4 export would require re-running the entire design workflow.
- If no plate geometry has been selected yet; axis label format depends on knowing the plate type and layout direction first.

## Inputs

- Plate type specification (e.g., 96-well, 384-well)
- Layout direction configuration (row-wise or column-wise)
- Maximum samples per plate count (excluding QC samples)

## Outputs

- Configured y-axis label format for plate visualization
- Updated plate layout diagram with labeled axes
- Formatted injection sequence ready for inter-batch balancing

## How to apply

During Step 2 (Design Parameters and Predefinition for QC samples position) in InjectionDesign, after specifying plate type (e.g., 96-well, 384-well), maximum samples per plate, and layout direction (row-wise or column-wise), select the desired yAxis label format from the configuration interface. The format choice affects how sample positions are visualized on the final plate layout diagram. Choose formats that align with your plate geometry and downstream data interpretation needs (e.g., alphabetic row labels A–H for 96-well plates, or numeric coordinate systems). Validate that the selected format correctly renders in the real-time visualization preview before proceeding to Step 3 (inter-batch balancing and intra-batch randomization).

## Related tools

- **InjectionDesign** (Web service that provides the plate configuration interface where yAxis label format is customized during QC predefinition) — github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- The selected yAxis label format appears consistently in the real-time plate layout visualization preview.
- Labels on the y-axis match the plate geometry (e.g., 8 row labels A–H for 96-well plate in standard orientation).
- The format choice is retained when proceeding to Step 3 and does not revert to defaults.
- Downloaded worksheet in Step 4 displays the configured y-axis labels on all exported plate layouts.
- No label truncation or overlap occurs in the visualization even when maximum samples per plate is set to high values.

## Limitations

- The yAxis label format is a visualization-only parameter and does not affect the underlying injection sequence logic or QC sample placement algorithms.
- Format options available are predefined by InjectionDesign and may not support fully custom label schemes beyond what the interface provides.
- Changing yAxis label format after completing Step 3 (randomization) requires restarting the workflow; the format is applied at design time, not retroactively to finalized plates.

## Evidence

- [readme] users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate.: "users need to set the plate type, max samples on single plate(exclude qc samples), layout direction and the yAxis label format of the plate"
- [intro] Set plate type (e.g., 96-well, 384-well) and specify the maximum number of analytical samples per plate (excluding QC samples). 4. Define the layout direction (row-wise or column-wise injection order). 5. Configure the yAxis label format for visualization.: "Define the layout direction (row-wise or column-wise injection order). 5. Configure the yAxis label format for visualization."
