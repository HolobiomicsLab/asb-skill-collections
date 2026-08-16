---
name: cytoscape-network-format-export
description: Use when after constructing or filtering a metabolomic network in MetaMapR
  (e.g., after applying the unique-edges hierarchy filter to resolve multiple edge
  types between node pairs), and you need to visualize, share, or further analyze
  the network using cytoscape.js or compatible tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - MetaMapR
  - cytoscape.js
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btv194
  title: MetaMapR
evidence_spans:
- MetaMapR - A metabolomic network mapping tool
- add cytoscape.js networks
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

# cytoscape-network-format-export

## Summary

Export a filtered metabolomic network to cytoscape.js-compatible JSON format for interactive visualization and analysis. This skill converts an in-memory network graph (after applying edge-type prioritization or other filters) into a standardized JSON structure that cytoscape.js can render.

## When to use

After constructing or filtering a metabolomic network in MetaMapR (e.g., after applying the unique-edges hierarchy filter to resolve multiple edge types between node pairs), and you need to visualize, share, or further analyze the network using cytoscape.js or compatible tools.

## When NOT to use

- The network has not yet been loaded or filtered — export requires a computed edge list as input.
- You need to export to a non-cytoscape format (e.g., GraphML, GML, or Gephi formats) — this skill is specific to cytoscape.js JSON.
- The node ID mapping is ambiguous or not yet resolved — export requires unambiguous numeric-to-analyte ID correspondence.

## Inputs

- Filtered metabolomic network graph (in-memory representation after edge selection)
- Edge list with source, target, edge type, and weight attributes
- Node attributes table mapping numeric node IDs to analyte identifiers

## Outputs

- cytoscape.js-compatible JSON network file
- Network visualization-ready format with node and edge elements

## How to apply

After the network filtering step (e.g., applying the Biochemical > Structural > Mass Spectral > Correlation priority hierarchy to unique edges), serialize the resulting edge list and node attributes into cytoscape.js JSON format. The JSON must encode both the filtered edge set and node metadata (including the mapping between numeric node IDs and original analyte identifiers from the uploaded data). The export preserves edge type information and node attribute annotations so that downstream cytoscape.js rendering and interactive exploration remain faithful to the original network computation.

## Related tools

- **MetaMapR** (Metabolomic network construction and filtering; generates the edge list and node attributes before export) — https://github.com/dgrapov/MetaMapR
- **cytoscape.js** (Interactive network visualization and exploration framework that consumes the exported JSON format)

## Evaluation signals

- Output JSON validates against cytoscape.js schema (contains 'elements' array with 'nodes' and 'edges' sub-arrays)
- Every edge in the exported JSON corresponds to exactly one edge in the filtered network (no duplicates, no missing edges after unique-edge filtering)
- Node IDs in the JSON are numeric and match the 'edge index' used during network calculation; node attributes include the 'identifier' field mapping to original analyte names
- Edge type information (Biochemical, Structural, Mass Spectral, Correlation) is preserved as an edge attribute in the JSON
- Exported JSON file can be successfully imported and rendered by cytoscape.js without errors

## Limitations

- Export format is specific to cytoscape.js; users requiring GraphML, GML, or other network formats must use additional conversion tools.
- Node ID mapping relies on correct assignment during network calculation; if custom node IDs were used, the exported JSON must preserve the mapping or re-mapping is required.
- Partial correlations are not yet supported in MetaMapR (listed in TODO), so correlation-based networks may be incomplete.
- The README and task description do not specify whether network attributes (e.g., edge weights, statistical confidence scores) are included in the cytoscape.js JSON export — this may limit downstream filtering or styling.

## Evidence

- [other] Construct the filtered network retaining only the selected edges per pair. 5. Export the filtered network in a cytoscape.js-compatible format (JSON).: "Construct the filtered network retaining only the selected edges per pair. 5. Export the filtered network in a cytoscape.js-compatible format (JSON)."
- [other] MetaMapR returns a single edge per node pair selected according to a fixed priority hierarchy: Biochemical edges are preferred over Structural, which are preferred over Mass Spectral, which are preferred over Correlation edges.: "MetaMapR returns a single edge per node pair selected according to a fixed priority hierarchy: Biochemical edges are preferred over Structural, which are preferred over Mass Spectral, which are"
- [readme] By default the numeric node IDs are assigned based on the order (row) of the uploaded data. For example 1 corresponds to the analyte in the first row. The node attributes tab also shows the mapping between the identifier used for the network and the assigned numeric node ID.: "By default the numeric node IDs are assigned based on the order (row) of the uploaded data. For example 1 corresponds to the analyte in the first row. The node attributes tab also shows the mapping"
- [readme] add cytoscape.js networks: "add cytoscape.js networks"
