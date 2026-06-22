---
name: node-pair-edge-deduplication
description: Use when your input network contains multiple edge types (Biochemical, Structural, Mass Spectral, Correlation) linking the same node pairs, and you want to export or visualize a single-edge-per-pair network to avoid visual clutter and ambiguous interpretations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - MetaMapR
  - cytoscape.js
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# node-pair-edge-deduplication

## Summary

Resolves multiple edge types between the same node pair in metabolomic networks by selecting a single edge per pair according to a fixed biochemical priority hierarchy. This filtering step reduces redundancy and ambiguity when exporting network data for visualization or downstream analysis.

## When to use

Apply this skill when your input network contains multiple edge types (Biochemical, Structural, Mass Spectral, Correlation) linking the same node pairs, and you want to export or visualize a single-edge-per-pair network to avoid visual clutter and ambiguous interpretations. Triggered by enabling the 'unique edges' checkbox in MetaMapR's network output tab.

## When NOT to use

- Input network contains only one edge type per node pair (deduplication is already complete)
- Analysis goal requires retention of all edge types for sensitivity analysis or multi-evidence reasoning
- Network is already in a format that does not support multi-edge representation (e.g., adjacency matrix with single values per pair)

## Inputs

- Multi-edge network graph (node pairs with ≥1 edge type each)
- Edge type labels (Biochemical, Structural, Mass Spectral, Correlation)

## Outputs

- Single-edge-per-pair network graph (JSON cytoscape.js format)
- Deduplicated edge list with one edge per node pair

## How to apply

Group all edges in the input network by their source–target node pair. For each pair with multiple edges, select the single edge with the highest priority according to the fixed hierarchy: Biochemical (highest) > Structural > Mass Spectral > Correlation (lowest). Retain only the selected edges and discard all others from the pair. The rationale is that biochemical edges (direct molecular interactions) are more informative than correlations (statistical associations), so they are preferred when both exist. Export the deduplicated network in cytoscape.js-compatible JSON format. The priority order reflects increasing distance from direct molecular evidence.

## Related tools

- **MetaMapR** (Primary tool for loading multi-edge metabolomic networks and applying unique-edges filtering via checkbox control in the network tab) — https://github.com/dgrapov/MetaMapR
- **cytoscape.js** (Target visualization and export format for the deduplicated network output)

## Evaluation signals

- For each unique node pair in the output, verify exactly one edge is present (cardinality check)
- Confirm the retained edge per pair is the highest-priority type according to the hierarchy (spot-check 10–20 pairs)
- Verify output JSON is valid cytoscape.js format (schema validation against cytoscape.js node/edge JSON schema)
- Count of output edges ≤ count of input edges (no spurious edges added)
- No node pair in output should have more than one edge, regardless of edge type

## Limitations

- The priority hierarchy is fixed and non-configurable: Biochemical > Structural > Mass Spectral > Correlation. Users who need a different ranking cannot alter it within the current implementation.
- Edges are selected purely on type rank with no consideration for edge weight, confidence score, or p-value; a low-confidence Biochemical edge will replace a high-confidence Structural edge.
- Filtering is destructive: metadata or details associated with discarded edges are lost; no provenance record of which edges were removed is retained by default.
- Partial correlations are not yet implemented as a distinct edge type, limiting the expressiveness of correlation-based edges.

## Evidence

- [intro] Finding: edge type priority hierarchy: "edges are returned based on a hierarchy Biochemical > Structural > Mass Spectral > Correlation"
- [readme] Mechanism: per-pair selection: "If the option is selected then edges are returned based on a hierarchy Biochemical > Structural > Mass Spectral > Correlation"
- [other] Workflow: grouping and selection steps: "For each node pair with multiple edges, select the single edge with the highest priority according to the hierarchy"
- [other] Output format: "Export the filtered network in a cytoscape.js-compatible format (JSON)"
- [readme] User trigger: "unique edges checkbox. If the option is selected then edges are returned based on a hierarchy"
