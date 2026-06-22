---
name: metabolite-network-construction
description: 'Use when when you have a list of input metabolites (e.g., from differential metabolomics analysis) and need to: (1) contextualize them within known metabolic pathways; (2) assess their structural importance in the pathway network rather than statistical significance alone;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - R
  - igraph
  - KEGGREST
  - enrichmet
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-network-construction

## Summary

Construct a bipartite pathway-metabolite network from curated KEGG mappings and compute graph topology metrics (betweenness centrality) to identify metabolites with high regulatory influence within metabolic pathways. This enables ranking of metabolites by their topological importance and potential functional impact.

## When to use

When you have a list of input metabolites (e.g., from differential metabolomics analysis) and need to: (1) contextualize them within known metabolic pathways; (2) assess their structural importance in the pathway network rather than statistical significance alone; (3) rank metabolites by their role as connectors or hubs between pathways. Use this skill before or in parallel with enrichment testing to identify metabolites that are statistically abundant AND topologically central.

## When NOT to use

- Input metabolites are already ranked by statistical significance (p-value, adjusted p-value, fold-change) and you only need to visualize or filter by these scores—use simple ranking or threshold filtering instead.
- You lack prior pathway-metabolite mapping or curated reference (e.g., no KEGG access, no local pathway database)—network construction requires valid edge definitions.
- The metabolites are from a non-human or non-standard organism and KEGG pathway mappings are not available or incomplete for that species.

## Inputs

- List of metabolite identifiers (e.g., KEGG IDs like C00001, C00002) from differential analysis or experimental selection
- PathwayVsMetabolites data.frame: two-column table mapping pathway names to comma-separated metabolite IDs
- Optionally, KEGG metabolite metadata (names, chemical class) for annotation

## Outputs

- Betweenness centrality table (data.frame): metabolite ID, RBC score [0,1], pathway membership counts
- RBC plot (ggplot2 or base R barplot/scatter): ranked visualization of input metabolites by centrality
- igraph graph object: the bipartite pathway-metabolite network with centrality attributes

## How to apply

Load the pathway-metabolite bipartite graph structure (nodes = pathways and metabolites; edges = membership relationships) from curated KEGG data via KEGGREST or pre-computed pathway mapping files (e.g., Human-Pathways.csv). Filter the network to retain only metabolites in your input set (e.g., significant metabolites from differential analysis). Compute betweenness centrality for each retained metabolite node using igraph's betweenness centrality function. Normalize centrality values to the [0,1] range (Relative Betweenness Centrality, RBC) by dividing by the graph's maximum possible centrality or by the observed maximum. Generate a ranked data.frame with metabolite IDs, RBC scores, and optional pathway annotations. Visualize as a barplot or ranked scatter plot (RBC plot) showing which input metabolites occupy central positions in the pathway network.

## Related tools

- **igraph** (Construct bipartite graph structure and compute betweenness centrality metrics on metabolite nodes)
- **KEGGREST** (Retrieve pathway-to-metabolite mappings from KEGG API; alternatively use pre-computed curated files)
- **R** (Scripting language for graph construction, normalization, filtering, and RBC plot generation)
- **enrichmet** (Integrated pipeline that wraps network construction, centrality computation, and RBC visualization within a single enrichment workflow) — https://github.com/biodatalab/enrichmet

## Examples

```
results <- enrichmet(inputMetabolites = c("C00001", "C00002", "C00003"), PathwayVsMetabolites = PathwayVsMetabolites, analysis_type = c("centrality", "network"), network_top_n = 10)
```

## Evaluation signals

- RBC values are bounded in [0, 1] (or [0, max_centrality]); verify no centrality scores fall outside expected range.
- Metabolite-pathway membership counts in output table are non-negative integers and match the input PathwayVsMetabolites structure.
- Network graph node count equals (number of input metabolites + number of unique pathways); edge count reflects membership relationships without duplicates.
- RBC plot shows input metabolites ranked in descending order of centrality; top-ranked metabolites appear in more pathways and have longer average shortest paths to other metabolites.
- Metabolites that appear in only one pathway have lower centrality than those appearing in multiple pathways (assumes minimum network size > 3 nodes).

## Limitations

- Betweenness centrality is sensitive to network connectivity: sparse, fragmented pathway networks may produce uninformative or zero centrality values for isolated metabolites.
- RBC computation assumes the pathway-metabolite bipartite structure is complete and accurate; missing or incorrect pathway annotations will bias centrality rankings.
- Centrality does not account for pathway flux, enzyme activity, or reaction directionality—it reflects structural topology only, not biochemical dynamics.
- If the input metabolite set is very small (< 5 metabolites) or covers only one or two pathways, centrality rankings may be trivial or non-discriminatory.
- KEGG-based pathway mappings are human-curated and subject to update; results may differ across KEGG versions or when using alternative pathway databases.

## Evidence

- [other] Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and metabolites and edges encoding membership.: "Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and metabolites and edges encoding membership."
- [other] Compute betweenness centrality for each metabolite node using igraph's betweenness centrality function.: "Compute betweenness centrality for each metabolite node using igraph's betweenness centrality function."
- [other] Normalize betweenness centrality values to Relative Betweenness Centrality (RBC) by scaling to the [0,1] range or by the graph's maximum possible centrality.: "Normalize betweenness centrality values to Relative Betweenness Centrality (RBC) by scaling to the [0,1] range or by the graph's maximum possible centrality."
- [other] enrichmet computes betweenness centrality for metabolites and produces a Relative Betweenness Centrality (RBC) plot that displays RBC values on the x-axis to highlight the topological importance and potential regulatory influence of metabolites within the metabolic network.: "enrichmet computes betweenness centrality for metabolites and produces a Relative Betweenness Centrality (RBC) plot that displays RBC values on the x-axis to highlight the topological importance and"
- [intro] pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package: "pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package"
- [intro] integrates fgsea for fast MetSEA, igraph for topology-based metrics: "integrates fgsea for fast MetSEA, igraph for topology-based metrics"
