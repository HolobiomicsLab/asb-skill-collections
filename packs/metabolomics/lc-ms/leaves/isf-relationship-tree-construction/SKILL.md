---
name: isf-relationship-tree-construction
description: Use when after completing ISFrag Part 4 (Identification of ISF Features)
  when you have a validated feature table with identified ISF features and need to
  visualize or export the hierarchical fragmentation structure linking parent ions
  to their in-source fragments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
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
  provenance_tier: literature
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

# isf-relationship-tree-construction

## Summary

Constructs and exports a hierarchical relationship tree representing structural relationships among identified in-source fragment (ISF) features in LCMS metabolite data. This skill organizes ISF features and their parent ions according to fragmentation relationships, producing a tree artifact suitable for downstream interpretation of fragment origins and mass relationships.

## When to use

Apply this skill after completing ISFrag Part 4 (Identification of ISF Features) when you have a validated feature table with identified ISF features and need to visualize or export the hierarchical fragmentation structure linking parent ions to their in-source fragments. Use this skill if your analysis goal requires understanding the structural topology of fragment relationships within your metabolite feature set.

## When NOT to use

- Input feature table has not yet completed ISFrag Part 4 (ISF identification); tree requires validated parent-fragment assignments.
- You only need to export the ISF result feature table itself (Part 5.1) without hierarchical structure visualization.
- Your analysis ends at feature identification and does not require downstream structural interpretation or network analysis of fragments.

## Inputs

- ISFrag feature table from Part 4 (data.frame with identified ISF features, parent ion assignments, and fragmentation annotations)
- R environment with ISFrag package loaded

## Outputs

- ISF Relationship Tree artifact (exported in ISFrag's specified format, representing hierarchical fragmentation structure)
- Relationship tree file in output directory specified by user

## How to apply

Load the ISFrag R package (version 4.0.0 or above) and the feature table output from Part 4 containing identified ISF features with parent-fragment assignments. Construct the relationship tree by organizing ISF features hierarchically according to fragmentation relationships—each node represents a feature, and edges connect parent ions to their identified in-source fragments. Call ISFrag's dedicated export function (Part 5.2) to serialize the tree structure into the specified output format (typically a network or hierarchical text structure). The export function automatically handles the tree topology; verify correctness by confirming that each fragment feature has a valid parent ion assignment and that the hierarchy preserves fragmentation mass differences consistent with neutral loss or adduct formation rules.

## Related tools

- **ISFrag** (Core R package providing the relationship tree export function (Part 5.2) and hierarchical fragmentation structure organization) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment; ISFrag requires R version 4.0.0 or above)
- **RStudio** (Recommended IDE for executing ISFrag functions and managing the relationship tree construction workflow)

## Examples

```
library(ISFrag); ft <- read.csv('Part4_ISF_Features.csv'); tree <- ISFrag::export_relationship_tree(ft); write.csv(tree, 'ISF_Relationship_Tree_Export.csv')
```

## Evaluation signals

- All identified ISF features from Part 4 are represented as nodes in the exported tree structure.
- Each fragment node maintains a valid parent ion link; no orphaned or circular relationships appear in the hierarchy.
- Tree depth and branching reflect the fragmentation cascade—parent ions have multiple children (fragments) and fragments have no children.
- Exported file is valid in the target format (e.g., parseable as a network adjacency list or hierarchical text structure) and contains expected metadata fields (m/z, retention time, parent assignments).
- Mass differences between parent and fragment nodes correspond to known neutral losses or adduct transformations (e.g., loss of H2O, NH3, or common metabolite modifications).

## Limitations

- Relationship tree export assumes Part 4 parent-fragment assignments are complete and accurate; erroneous or missing assignments will propagate into the tree structure.
- The export function is specialized to ISFrag's internal feature table schema; custom or externally-generated feature tables may require reformatting to Part 4 output standards before tree construction.
- Tree structure does not include MS2 spectral matching or chemical class annotation; those artifacts are exported separately in Part 5.1.

## Evidence

- [readme] Part 5.2 export function: "ISFrag includes a dedicated export function (Part 5.2) for exporting the ISF Relationship Tree, which represents the structural relationships among identified in-source fragment features."
- [readme] Workflow construction step: "Construct the relationship tree by organizing ISF features and their parent ions hierarchically according to fragmentation relationships."
- [readme] Input requirement: "Load the ISFrag R package and the feature table containing identified ISF features from Part 4 output."
- [readme] Output artifact: "Export the relationship tree structure using ISFrag's export function to produce a relationship tree artifact in the specified output format."
- [readme] Tool requirement: "To install `ISFrag` package R version 4.0.0 or above is required, and we recommend using RStudio to complete the installation and usage of `ISFrag`"
