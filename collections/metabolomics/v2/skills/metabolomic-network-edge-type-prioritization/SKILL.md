---
name: metabolomic-network-edge-type-prioritization
description: Use when when your metabolomic network contains multiple edge types (Biochemical,
  Structural, Mass Spectral, Correlation) between the same node pairs and you want
  to export a unique-edge network in which each node pair is connected by exactly
  one edge—the one with highest priority according to the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0121
  tools:
  - MetaMapR
  - cytoscape.js
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btv194
  title: MetaMapR
evidence_spans:
- MetaMapR - A metabolomic network mapping tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metamapr_cq
    doi: 10.1093/bioinformatics/btv194
    title: MetaMapR
  dedup_kept_from: coll_metamapr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv194
  all_source_dois:
  - 10.1093/bioinformatics/btv194
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-network-edge-type-prioritization

## Summary

Filter a metabolomic network to retain only one edge per node pair by applying a fixed priority hierarchy across edge types (Biochemical > Structural > Mass Spectral > Correlation). This is used when multiple edges of different types connect the same nodes and you need a simplified, non-redundant network representation.

## When to use

When your metabolomic network contains multiple edge types (Biochemical, Structural, Mass Spectral, Correlation) between the same node pairs and you want to export a unique-edge network in which each node pair is connected by exactly one edge—the one with highest priority according to the Biochemical > Structural > Mass Spectral > Correlation hierarchy. This is applicable when the user enables the 'unique edges' checkbox in MetaMapR's network tab.

## When NOT to use

- Your network contains only a single edge type per node pair (no filtering needed).
- You want to preserve all edge types for downstream analysis (use 'return all edges' mode instead).
- You require partial correlations or other edge types not yet implemented in MetaMapR.

## Inputs

- metabolomic network with multiple edge types
- edge list with source node ID, target node ID, and edge type (Biochemical|Structural|Mass Spectral|Correlation)

## Outputs

- filtered metabolomic network (unique edges per node pair)
- cytoscape.js-compatible JSON network representation

## How to apply

Load the input network containing all edge types between metabolite/protein node pairs. Group edges by their source–target node pair identifier. For each pair with multiple edges, compare the edge types and select the single edge with the highest priority in the fixed hierarchy: Biochemical (highest) > Structural > Mass Spectral > Correlation (lowest). Discard all other edges for that pair. Construct the filtered network containing only the selected edges, then export in cytoscape.js-compatible JSON format. The rationale is that Biochemical edges represent the strongest mechanistic evidence, so they are preferred when present; if absent, the next-highest priority type is chosen, ensuring deterministic and reproducible filtering.

## Related tools

- **MetaMapR** (Primary network filtering and export tool; implements the unique-edges checkbox and edge-type hierarchy selection) — https://github.com/dgrapov/MetaMapR
- **cytoscape.js** (Target format for filtered network export and visualization)

## Evaluation signals

- Verify that the output network has exactly one edge per unique source–target node pair (no duplicate pairs).
- Check that for any node pair that had multiple edge types in the input, only the highest-priority edge type is retained in the output.
- Confirm the output JSON is valid cytoscape.js format and can be imported without parsing errors.
- Manually inspect a sample of node pairs that had multiple edge types: verify the retained edge matches the hierarchy (e.g., if Biochemical and Mass Spectral were both present, only Biochemical remains).
- Compare edge count between input (all edges) and output (unique edges): output should have fewer or equal edges.

## Limitations

- The priority hierarchy is fixed and not user-customizable in the current implementation.
- Partial correlations are not yet supported as an edge type.
- The network mapping feature is still under development.
- Edge type assignment must be reliable upstream; errors in edge-type classification will propagate through the filtering step.

## Evidence

- [readme] The priority hierarchy and when it is applied: "If the option is selected then edges are returned based on a hierarchy Biochemical > Structural > Mass Spectral > Correlation"
- [other] Input data structure and node-pair grouping logic: "Group edges by their source–target node pair. For each node pair with multiple edges, select the single edge with the highest priority according to the hierarchy"
- [other] Output format specification: "Export the filtered network in a cytoscape.js-compatible format (JSON)"
- [readme] Rationale for the hierarchy ordering: "The default setting for returning all edge types or only unique edges can be found under the network tab using the unique edges checkbox"
