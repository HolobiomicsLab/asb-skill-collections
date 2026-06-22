---
name: qc-sample-type-classification
description: Use when when constructing a sample list from an Excel template for LC/GC-MS analysis, you must classify each QC sample by type before proceeding to plate layout and randomization steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - InjectionDesign
  - pandas or openpyxl
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

# QC Sample Type Classification

## Summary

Classify and designate quality control samples into predefined types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC) within a sample list prior to injection-plate design. This classification enables systematic QC positioning and visual differentiation across LC/GC-MS injection sequences.

## When to use

When constructing a sample list from an Excel template for LC/GC-MS analysis, you must classify each QC sample by type before proceeding to plate layout and randomization steps. Use this skill when you have a structured sample list with sample identifiers and metadata but QC samples lack explicit type assignments that the injection design algorithm requires.

## When NOT to use

- Input sample list has already been processed through injection-plate design and finalized; re-classification would require re-running the entire design pipeline.
- All samples in the list are biological/study samples with no QC samples; classification is unnecessary if no QC samples exist.
- QC type information is not required by the downstream injection-design algorithm (e.g., if using a different plate-design tool with different QC requirements).

## Inputs

- Parsed sample list (JSON or CSV) with sample identifiers, classification dimensions, and sample-type flags from Excel template ingestion
- Sample metadata rows including indicator columns or fields marking which samples are QC samples

## Outputs

- Classified sample list with QC type designation (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC) added to each QC sample record
- Color-coded sample list visualization showing QC sample types

## How to apply

After parsing the uploaded sample Excel template into a structured sample list (task_id=task_001), examine each sample row and assign a QC type designation from the five predefined categories: Blank QC (solvent or matrix blank), Solvent QC (solvent control), Pooled QC (pooled biological sample), Long-Term Reference QC (stability reference), or custom QC (user-defined). Mark each QC sample with its type in the sample metadata record. The system uses these type assignments to color-code QC samples in the visualization and to apply QC-specific positioning rules during inter-batch balancing in Step 3. Classification must occur before the Design Parameters step, as it determines how the algorithm reserves plate positions and applies balancing constraints.

## Related tools

- **InjectionDesign** (Web service that accepts classified sample lists and uses QC type designations to guide inter-batch balancing, QC positioning, and visualization of injection-plate layout) — https://github.com/CSi-Studio/InjectionDesign
- **pandas or openpyxl** (Spreadsheet parser used in Step 1 to load and validate the Excel template structure before QC type assignment)

## Evaluation signals

- Every QC sample record in the output list has a QC type field populated with one of the five allowed values (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC); no QC sample has a null or unrecognized type.
- Non-QC (biological study) samples have null or distinct non-QC type values; they are not mistakenly labeled as QC types.
- QC type assignments are consistently applied: identical QC samples (e.g., multiple blank controls) receive the same type designation across the list.
- Visualization in InjectionDesign Step 2 displays QC samples in distinct colors corresponding to their assigned types, confirming type information was correctly parsed downstream.
- The final injection worksheet generated after Steps 2–4 shows QC samples positioned according to their type-specific rules (e.g., Long-Term Reference QC samples appear at defined intervals for stability monitoring).

## Limitations

- InjectionDesign supports only five predefined QC types plus one custom type; if a workflow requires more than six distinct QC categories, custom types must be mapped to one of the five standard types, potentially losing granularity.
- Classification is manual or rule-based on sample metadata; no automated QC-type inference from sample name patterns or historical data is described in the article.
- Classification occurs before inter-batch balancing (Step 3); if balancing constraints later require reallocation of QC positions, QC type assignments are not retroactively refined—only plate positions adjust.

## Evidence

- [readme] InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC.: "InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC."
- [intro] Extract sample metadata rows and map each row to a sample record with sample identifier, classification dimensions (up to three), and QC type designation (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC).: "map each row to a sample record with sample identifier, classification dimensions (up to three), and QC type designation (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC)."
- [readme] Different QC type has be marked as different color.: "Different QC type has be marked as different color."
- [readme] After upload samples. Users can modify the sample list for future operation.: "After upload samples. Users can modify the sample list for future operation."
