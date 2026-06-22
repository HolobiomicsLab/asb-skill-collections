---
name: network-visualization-ranked-scoring
description: Use when when you have computed betweenness centrality (or other igraph topology metrics) for metabolites in a pathway-metabolite bipartite network and wish to highlight which metabolites occupy central positions—i.e., have high regulatory potential through bridging multiple pathways.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - R
  - igraph
  - KEGGREST
  - ComplexHeatmap
  - STITCH database
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
- integrates fgsea for fast MetSEA, igraph for topology-based metrics
- pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
---

# network-visualization-ranked-scoring

## Summary

Construct and visualize a metabolite–pathway interaction network ranked by topological centrality metrics, with node sizing and edge weighting reflecting metabolite importance and interaction strength. This skill reveals regulatory hubs and pathway connectivity patterns essential for interpreting metabolic reorganization in disease states.

## When to use

When you have computed betweenness centrality (or other igraph topology metrics) for metabolites in a pathway-metabolite bipartite network and wish to highlight which metabolites occupy central positions—i.e., have high regulatory potential through bridging multiple pathways. Apply this skill after filtering to top metabolites by centrality score (e.g., top 10–20) to avoid visual clutter and emphasize the most influential nodes.

## When NOT to use

- Input metabolites are already filtered to ≤3 nodes: network visualization adds no interpretive value and risks misrepresenting sparse data as meaningful topology.
- Centrality scores have not been computed or normalized: node sizing will be arbitrary and misleading about metabolite regulatory importance.
- STITCH interaction data is missing or sparse (<5 edges): edge weighting cannot be meaningful; use unweighted graph or pathway membership only.

## Inputs

- Metabolite-pathway bipartite igraph object (nodes: metabolites + pathways; edges: membership)
- Centrality scores (RBC or betweenness centrality values, normalized to [0,1])
- KEGG lookup table (kegg_id, name columns mapping KEGG identifiers to display names)
- Metabolite interaction data frame (chemical1, chemical2, combined_score, experimental, database, textmining columns; STITCH format)
- Mapping table with KEGG_ID to PubChem_CID or STITCH_ID columns
- Top-n filtering parameter (e.g., network_top_n=10 or heatmap_top_n=20)

## Outputs

- igraph graph object with vertex attributes (name, display_name, KEGG_ID, PubChem_CID, centrality_rank)
- Network visualization plot (S3/S4 plot object) with ranked node sizing by centrality and edge weighting by interaction strength
- Layout coordinates (x, y, z) from igraph layout algorithm (e.g., gem, fruchterman_reingold)
- Optional: adjacency matrix or edge list with centrality and interaction strength annotations

## How to apply

Load the pathway-metabolite bipartite graph and pre-computed centrality values (e.g., RBC scores from igraph's betweenness_centrality() function). Filter metabolites to the top-n by centrality rank (using parameters like network_top_n or heatmap_top_n). Map metabolite display names using a KEGG lookup table and join with interaction strength data (e.g., STITCH combined_score or similarity metrics). Construct the igraph graph object with vertex attributes (KEGG_ID, display_name, centrality_rank) and edge attributes (combined_score, experimental_score, database_score). Apply a layout algorithm (e.g., gem, fruchterman_reingold) that minimizes edge crossings and spaces high-centrality nodes more prominently. Size nodes proportionally to RBC or betweenness values, and color or weight edges by interaction confidence score. Verify that the network displays 10–20 metabolites with ≥5 interactions to avoid both over-crowding and under-representation.

## Related tools

- **igraph** (Computes betweenness centrality, constructs bipartite graph, applies layout algorithms (gem, fruchterman_reingold) for node positioning, and manages vertex/edge attributes (KEGG_ID, display_name, centrality_rank, combined_score))
- **KEGGREST** (Retrieves pathway-to-metabolite mappings and KEGG metabolite annotations to populate the KEGG_ID and name lookup table for display name resolution)
- **R** (Orchestrates network construction, centrality filtering, layout computation, and plot rendering via igraph and ComplexHeatmap libraries) — https://github.com/biodatalab/enrichmet
- **ComplexHeatmap** (Optional: alternative or complementary visualization for pathway membership heatmap and network adjacency matrices)
- **STITCH database** (Provides chemical–chemical interaction data (combined_score, experimental, database, textmining columns) to weight edges by interaction confidence) — http://stitch.embl.de/

## Examples

```
results <- enrichmet(inputMetabolites = c('C00001', 'C00002', 'C00003'), PathwayVsMetabolites = PathwayVsMetabolites, mapping_df = mapping_df, stitch_df = stitch_df, network_top_n = 10, analysis_type = 'network')
```

## Evaluation signals

- Network graph contains exactly top-n metabolites (e.g., 10–20 nodes) and ≥5 edges with non-zero combined_score; no orphan metabolites.
- Node size is monotonically increasing with RBC or betweenness centrality rank; highest-ranked metabolites are visibly largest.
- Edge weight (thickness or opacity) correlates positively with STITCH combined_score; high-confidence interactions (score ≥400) are visibly thicker.
- Vertex attributes are correctly populated: every node has valid KEGG_ID, display_name, and centrality_rank; no missing or NA values.
- Layout algorithm completes without error and produces no edge overlaps for >90% of edges; gem layout achieves spacing_score ≥300.
- Display names resolve correctly from KEGG lookup; no metabolite is labeled 'NA' or by raw KEGG ID alone if a name exists in the lookup table.

## Limitations

- Network visualization is restricted to top-n metabolites by centrality to reduce visual clutter; smaller but potentially biologically important metabolites may be excluded. Set network_top_n carefully (10–20 is typical) to balance interpretability and coverage.
- STITCH interaction data availability is incomplete for all metabolite pairs; networks with <5 edges may not support meaningful edge weighting and should fall back to unweighted or pathway-membership-only networks.
- igraph layout algorithms (gem, fruchterman_reingold) are non-deterministic without seed setting; replicate visualizations require explicit set.seed() or layout_as_tree() to ensure reproducibility.
- Bipartite network projection (metabolite–metabolite graph) requires collapsing pathway intermediaries; indirect pathway connections may be missed in the projected network.
- Node sizing by centrality assumes RBC or betweenness values are normalized to [0,1]; unnormalized or raw scores will produce uninformative or degenerate scaling.

## Evidence

- [intro] igraph_construction_and_centrality_computation: "Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and metabolites and edges encoding membership. Compute betweenness centrality for each metabolite"
- [intro] network_ranking_and_filtering: "Generate a data.frame containing metabolite identifiers, RBC scores, and optional pathway annotations. Using top 10 metabolites by centrality for network plot"
- [readme] display_name_mapping_and_vertex_attributes: "Applied KEGG pathway name mapping using 'kegg_id' and 'name' columns. Vertex attributes: name, display_name, KEGG_ID, PubChem_CID"
- [readme] edge_weighting_by_interaction_strength: "Found 50 valid interactions between 20 metabolites. Vertex attributes: name, display_name, KEGG_ID, PubChem_CID. Graph vertex attributes"
- [readme] layout_algorithm_and_spacing: "Using layout: gem (spacing score: 388.19)"
- [intro] filter_parameters_network_top_n: "Select top pathways for network visualization using network_top_n parameter"
- [intro] rbc_plot_and_centrality_ranking: "enrichmet computes betweenness centrality for metabolites and produces a Relative Betweenness Centrality (RBC) plot that displays RBC values on the x-axis to highlight the topological importance and"
- [intro] stitch_interaction_data_integration: "interactions between metabolites and proteins, obtained from the freely available STITCH database (http://stitch.embl.de/)"
