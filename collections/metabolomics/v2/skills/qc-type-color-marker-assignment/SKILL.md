---
name: qc-type-color-marker-assignment
description: Use when configuring a new injection-plate design template in InjectionDesign
  if you have multiple QC types to position on a plate and need to visually distinguish
  them in the final worksheet.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - InjectionDesign
  techniques:
  - GC-MS
  license_tier: restricted
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

# QC-type color-marker assignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assign distinct color markers to each of five predefined quality-control (QC) types in LC/GC-MS injection-plate design to enable visual discrimination during sample layout configuration. This skill ensures QC sample roles (Blank, Solvent, Pooled, Long-Term Reference, and custom) are unambiguous in plate visualization and experimental documentation.

## When to use

Apply this skill when configuring a new injection-plate design template in InjectionDesign if you have multiple QC types to position on a plate and need to visually distinguish them in the final worksheet. Specifically, use it after uploading your sample list and before randomization, when setting plate type, maximum samples per plate, and layout direction parameters.

## When NOT to use

- You are designing a single-QC-type plate (e.g., only Blank QC) — color assignment is unnecessary when visual discrimination is not required.
- Your laboratory uses non-visual (e.g., numeric or text-based) QC identification codes in downstream data processing — color markers serve only visual presentation and do not affect computational outputs.
- The plate design has already been finalized and exported — color reassignment would require re-running the entire design workflow.

## Inputs

- InjectionDesign template file with five predefined QC types
- Sample list (uploaded via Excel template)
- Plate configuration parameters (plate type, max samples, layout direction)

## Outputs

- Color-coded QC type configuration (persisted in InjectionDesign session)
- Plate layout visualization with color-marked QC sample positions
- Downloadable worksheet with color-differentiated QC samples

## How to apply

In InjectionDesign Step 2 (Design Parameters and Predefinition for QC samples position), access the color palette configuration for the five predefined QC types: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, and one custom QC type. Assign a distinct color to each type such that they are visually separable in the final plate layout visualization. The color assignment persists through inter-batch balancing (Step 3) and appears in the final downloadable worksheet. Verify that the color coding matches your laboratory's QC documentation standards and that each type's color remains consistent across all output plate visualizations.

## Related tools

- **InjectionDesign** (Web service for multi-omics injection-plate design; hosts the color palette configuration interface and executes plate layout visualization with color-coded QC markers.) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- Each of the five QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, custom QC) is assigned a distinct color in the configuration panel.
- The assigned colors persist and appear consistently in the real-time plate layout visualization during inter-batch balancing adjustments (Step 3).
- The final exported worksheet displays all QC sample positions with their assigned color markers matching the configuration.
- Color assignments are visually discriminable (e.g., no two QC types share the same hue or lightness level) in standard laboratory monitor displays.
- The color configuration can be saved and reloaded for the same template across multiple experimental batches.

## Limitations

- InjectionDesign supports only five fixed QC types; custom QC is a single category and cannot be further subdivided by color.
- Color marker assignment is a visual feature only and does not affect computational plate randomization or balancing logic.
- The README does not specify support for colorblind-accessible palettes; end users should verify color contrast independently if accessibility is required.
- Color persistence is tied to the InjectionDesign session; if the session is lost or the template is reloaded, the color assignment must be re-entered.

## Evidence

- [readme] InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC.: "InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC."
- [readme] Different QC type has be marked as different color.: "Different QC type has be marked as different color."
- [intro] InjectionDesign marks each of the five QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, and custom QC) with different colors: "InjectionDesign marks each of the five QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, and custom QC) with different colors"
- [readme] Design Parameters and Predefinition for QC samples position: "Design Parameters and Predefinition for QC samples position"
