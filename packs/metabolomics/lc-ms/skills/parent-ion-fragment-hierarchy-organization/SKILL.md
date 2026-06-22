---
name: parent-ion-fragment-hierarchy-organization
description: Use when after ISF features have been identified and annotated in Part 4 of the ISFrag workflow, and you need to represent the structural relationships among ISF features and their parent ions hierarchically.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ISFrag
  - R
  - RStudio
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# parent-ion-fragment-hierarchy-organization

## Summary

Organize identified in-source fragment (ISF) features and their parent ions into a hierarchical relationship tree that represents fragmentation dependencies and structural relationships. This is a necessary intermediate step before exporting ISF results for downstream visualization or analysis.

## When to use

After ISF features have been identified and annotated in Part 4 of the ISFrag workflow, and you need to represent the structural relationships among ISF features and their parent ions hierarchically. Use this skill when preparing ISF results for export or when the fragmentation hierarchy itself is the object of analysis—for example, to understand which features are fragments of which parent ions.

## When NOT to use

- Input feature table does not yet contain ISF identifications from Part 4 — run Part 4 first.
- Your goal is only to export individual feature properties (e.g., m/z, retention time, intensity) without hierarchical structure — use Part 5.1 (Export ISF Result Feature Table) instead.
- You do not intend to visualize or export the relationship tree; you only need the ISF-annotated feature table for downstream statistical or chemical analysis.

## Inputs

- ISFrag R package (loaded)
- Feature table with identified ISF features from Part 4 output
- ISF identification results (parent–child fragment linkages)

## Outputs

- ISF Relationship Tree structure (in-memory R object)
- Exported relationship tree artifact (format specified by user, e.g., CSV, JSON, or graphical format)

## How to apply

Load the ISFrag R package and the feature table output from Part 4 (Identification of ISF Features) into R or RStudio. Use ISFrag's internal relationship-tree construction functions to organize ISF features according to their parent–child fragmentation relationships, where each parent ion is the root of a subtree containing its identified fragment features. The hierarchy is built by examining the ISF identification results, which link each fragment to its parent ion via mass and retention-time proximity rules established in Part 4. The resulting tree structure encodes both the mass differences (fragment losses) and the hierarchical containment relationships among features, which can then be exported or visualized.

## Related tools

- **ISFrag** (Core R package providing the relationship-tree construction and export functions (Part 5.2)) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment (version ≥4.0.0 required))
- **RStudio** (Recommended IDE for loading packages, managing the feature table, and executing ISFrag workflow steps)

## Examples

```
library(ISFrag); isf_ft <- read.csv('ISFrag_part4_output.csv'); isf_tree <- ISFrag::construct_relationship_tree(isf_ft); ISFrag::export_relationship_tree(isf_tree, output_file='isf_relationship_tree.csv')
```

## Evaluation signals

- All identified ISF features from Part 4 appear in the tree as leaf or internal nodes.
- Parent–child relationships in the tree match the fragmentation assignments made in Part 4 (i.e., each fragment feature is linked to its assigned parent ion).
- The exported artifact is valid in its declared format (e.g., well-formed CSV, JSON, or graphical file with no truncation or encoding errors).
- The tree structure is acyclic: no fragment feature appears as its own ancestor.
- Mass differences between parent and child nodes align with known loss patterns (e.g., neutral losses of H₂O, CO₂, etc., if annotated in Part 3 MS2 results).

## Limitations

- Relationship tree construction depends on the quality of ISF identifications from Part 4; incorrect parent–child assignments will propagate into the tree hierarchy.
- The README does not specify the supported export formats for the relationship tree; users should consult Part 5.2 documentation or ISFrag function help for available output formats.
- Hierarchical organization assumes a tree structure; if ISF features can share multiple parent ions or exhibit complex fragmentation networks, the tree representation may not capture all relationships.

## Evidence

- [other] Part 5.2 dedicated export function: "ISFrag includes a dedicated export function (Part 5.2) for exporting the ISF Relationship Tree, which represents the structural relationships among identified in-source fragment features."
- [other] Hierarchical organization workflow: "Construct the relationship tree by organizing ISF features and their parent ions hierarchically according to fragmentation relationships."
- [readme] Part 5.2 in manual structure: "[Part 5: Results Export](#part-5-results-export) - [5.2 Export ISF Relationship Tree](#52-export-isf-relationship-tree)"
- [readme] Feature table input from Part 4: "Load the ISFrag R package and the feature table containing identified ISF features from Part 4 output."
