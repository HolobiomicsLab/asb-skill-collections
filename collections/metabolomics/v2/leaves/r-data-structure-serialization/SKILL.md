---
name: r-data-structure-serialization
description: Use when after completing Part 4 (Identification of ISF Features) in
  the ISFrag workflow, when you have a feature table with identified ISF features
  and their hierarchical fragmentation relationships, and you need to export this
  relationship structure for interpretation, integration with external.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ISFrag
  - R
  - RStudio
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
- we recommend using RStudio to complete the installation and usage of ISFrag
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Export ISF Relationship Tree Structure

## Summary

Serialize the hierarchical structure of identified in-source fragment (ISF) features and their parent-ion relationships from an ISFrag analysis into a portable export format. This skill captures the fragmentation relationships discovered during ISF identification and makes them available for downstream analysis or visualization.

## When to use

After completing Part 4 (Identification of ISF Features) in the ISFrag workflow, when you have a feature table with identified ISF features and their hierarchical fragmentation relationships, and you need to export this relationship structure for interpretation, integration with external tools, or archival.

## When NOT to use

- You have not yet completed Part 4 (Identification of ISF Features) — the relationship tree requires identified ISF features as input.
- Your analysis goal is only to export the raw ISF result feature table; use Part 5.1 (Export ISF Result Feature Table) instead.
- You need to visualize the relationship tree interactively; this skill produces a static serialized structure, not a visualization.

## Inputs

- ISFrag feature table with identified ISF features (from Part 4 output)
- Relationship tree object constructed from ISF features and fragmentation relationships

## Outputs

- Exported ISF Relationship Tree artifact in user-specified format

## How to apply

Load the ISFrag R package and the feature table output from Part 4 containing identified ISF features with their fragmentation annotations. Call ISFrag's dedicated export function (Part 5.2) on the relationship tree object to serialize the hierarchical structure organizing ISF features and their parent ions according to fragmentation relationships. The export function produces a relationship tree artifact in the specified output format (e.g., CSV, JSON, or native R serialization). Verify the export by checking that the output file contains all identified ISF features, their parent-ion links, and hierarchical organization, and that the file format matches the intended downstream use.

## Related tools

- **ISFrag** (R package providing the relationship tree export function (Part 5.2) to serialize ISF feature hierarchies and fragmentation relationships) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment (version 4.0.0 or above required) for executing ISFrag export functions)
- **RStudio** (Recommended interactive development environment for running ISFrag package functions and managing export workflows)

## Examples

```
library(ISFrag); isf_result <- identify.ISF(featureTable, MS2data); export_tree <- export.ISFrelationtree(isf_result, outputFormat="csv", outputPath="./isf_relationship_tree.csv")
```

## Evaluation signals

- Export file is successfully created in the specified output format and is readable (e.g., valid CSV, JSON, or R object serialization).
- All identified ISF features from Part 4 are present in the exported relationship tree.
- Parent-ion relationships and hierarchical organization are correctly represented in the export (spot-check a subset of feature linkages against the source table).
- Export file size is non-zero and consistent with the number of ISF features and relationships identified.
- The exported structure can be loaded back into R or parsed by downstream analysis tools without format errors.

## Limitations

- Export format must be specified before the function is called; format options and their compatibility with downstream tools are not detailed in the README excerpt.
- The README truncates at Part 3 MS2 Annotation; full export function parameters, output schema, and edge cases for complex fragmentation trees are not provided in the available documentation.
- The skill depends on successful completion of all prior ISFrag workflow steps (Parts 2–4); errors or incomplete ISF identification will result in incomplete relationship trees.

## Evidence

- [other] ISFrag includes a dedicated export function (Part 5.2) for exporting the ISF Relationship Tree, which represents the structural relationships among identified in-source fragment features.: "ISFrag includes a dedicated export function (Part 5.2) for exporting the ISF Relationship Tree, which represents the structural relationships among identified in-source fragment features."
- [readme] Part 5: Results Export with subsections 5.1 Export ISF Result Feature Table and 5.2 Export ISF Relationship Tree: "[Part 5: Results Export](#part-5-results-export)
    -   [5.1 Export ISF Result Feature
        Table](#51-export-isf-result-feature-table)
    -   [5.2 Export ISF Relationship"
- [other] Construct the relationship tree by organizing ISF features and their parent ions hierarchically according to fragmentation relationships.: "Construct the relationship tree by organizing ISF features and their parent ions hierarchically according to fragmentation relationships."
