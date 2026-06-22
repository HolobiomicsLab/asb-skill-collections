---
name: network-graph-filtering-by-hierarchy
description: Use when your network contains multiple edge types between the same pair of nodes and you need a deterministic, single-edge representation per node pair.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0323
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3071
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

# network-graph-filtering-by-hierarchy

## Summary

Filter multi-type network edges by selecting a single representative edge per node pair according to a fixed priority hierarchy. This skill resolves ambiguity when metabolomic or other biological data contain multiple edge types (e.g., Biochemical, Structural, Mass Spectral, Correlation) between the same nodes, retaining only the highest-priority edge type for each pair.

## When to use

Your network contains multiple edge types between the same pair of nodes and you need a deterministic, single-edge representation per node pair. This is especially relevant in metabolomic network analysis where correlations, biochemical relationships, structural similarities, and mass spectral matches may all be computed between the same metabolite pairs, and you wish to avoid redundancy or conflation of evidence types.

## When NOT to use

- Your analysis goal requires retention of all edge types (e.g., comparative or exploratory analysis of multiple evidence types).
- Your network contains only a single edge type; filtering by hierarchy has no effect.
- The priority hierarchy does not align with your scientific priorities (e.g., you prioritize Mass Spectral over Biochemical evidence).

## Inputs

- network graph with multiple edge types (Biochemical, Structural, Mass Spectral, Correlation)
- node-pair grouping or adjacency structure
- edge type labels and priority hierarchy specification

## Outputs

- filtered network graph with one edge per node pair
- cytoscape.js-compatible JSON network representation

## How to apply

Load the network with all computed edge types (Biochemical, Structural, Mass Spectral, Correlation) intact. Group edges by their source–target node pair. For each pair containing multiple edges, apply the fixed priority hierarchy—Biochemical (highest) > Structural > Mass Spectral > Correlation (lowest)—and select exactly one edge per pair according to this rank. Discard all other edges for that pair. Construct the filtered network retaining only the single selected edge per node pair. Export in a cytoscape.js-compatible JSON format for visualization and downstream analysis.

## Related tools

- **MetaMapR** (network construction and filtering engine; applies unique-edges checkbox option to enforce hierarchy-based edge selection) — https://github.com/dgrapov/MetaMapR
- **cytoscape.js** (JSON-based network format target for visualization and export of filtered network)

## Evaluation signals

- For each source–target node pair present in the input, verify exactly one edge exists in the output.
- Verify that the retained edge is the highest-priority type present for that pair according to the hierarchy Biochemical > Structural > Mass Spectral > Correlation.
- Confirm all output edges conform to cytoscape.js JSON schema (valid node references, edge type labels).
- Check that no edges of lower priority remain when a higher-priority edge exists for the same pair.
- Validate that the edge count in the output is ≤ the edge count in the input, with equality only if input contained at most one edge per pair.

## Limitations

- The priority hierarchy is fixed (Biochemical > Structural > Mass Spectral > Correlation) and cannot be customized per analysis; users with different evidence priorities must implement custom logic.
- Filtering discards all but one edge per pair; information from lower-priority edge types is permanently lost.
- Partial correlations are not yet implemented in MetaMapR, limiting the edge types available for filtering.
- The skill assumes edge types are explicitly labeled in the input; unlabeled or ambiguous edge types may cause incorrect filtering.

## Evidence

- [other] When the unique edges checkbox is enabled, MetaMapR returns a single edge per node pair selected according to a fixed priority hierarchy: Biochemical edges are preferred over Structural, which are preferred over Mass Spectral, which are preferred over Correlation edges.: "When the unique edges checkbox is enabled, MetaMapR returns a single edge per node pair selected according to a fixed priority hierarchy: Biochemical edges are preferred over Structural, which are"
- [other] For each node pair with multiple edges, select the single edge with the highest priority according to the hierarchy: Biochemical (highest) > Structural > Mass Spectral > Correlation (lowest).: "For each node pair with multiple edges, select the single edge with the highest priority according to the hierarchy: Biochemical (highest) > Structural > Mass Spectral > Correlation (lowest)."
- [readme] The default setting for returning all edge types or only unique edges can be found under the network tab using the unique edges checkbox. If the option is selected then edges are returned based on a hierarchy Biochemical > Structural > Mass Spectral > Correlation, otherwise all edges are returned.: "If the option is selected then edges are returned based on a hierarchy Biochemical > Structural > Mass Spectral > Correlation, otherwise all edges are returned."
- [other] Construct the filtered network retaining only the selected edges per pair. Export the filtered network in a cytoscape.js-compatible format (JSON).: "Construct the filtered network retaining only the selected edges per pair. Export the filtered network in a cytoscape.js-compatible format (JSON)."
