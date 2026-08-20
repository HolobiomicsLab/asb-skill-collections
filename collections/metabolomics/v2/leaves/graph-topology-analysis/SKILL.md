---
name: graph-topology-analysis
description: Use when you have (1) a set of input metabolites (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0264
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0091
  tools:
  - R
  - igraph
  - KEGGREST
  - enrichmet
  license_tier: open
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed
  through a single R function call
- integrates fgsea for fast MetSEA, igraph for topology-based metrics
- pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST
  package
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

# Compute Relative Betweenness Centrality for Metabolites in Pathway Networks

## Summary

Quantify the topological importance and regulatory influence of metabolites within a pathway-metabolite bipartite network by computing betweenness centrality and normalizing to Relative Betweenness Centrality (RBC) scores in the [0,1] range. This identifies hub metabolites that bridge multiple pathways.

## When to use

Apply this skill when you have (1) a set of input metabolites (e.g., from differential metabolomics analysis), (2) a pathway-metabolite mapping file defining bipartite edges, and (3) you need to rank metabolites by their topological role in the network to identify regulatory bottlenecks or central hubs that warrant further mechanistic investigation.

## When NOT to use

- Input metabolites are already ranked or scored by another method (e.g., fold-change, p-value): betweenness centrality measures network topology, not statistical significance
- Network is not bipartite or metabolite-pathway structure is unknown: centrality interpretation depends on valid bipartite structure
- Sample size is very small (< 5 metabolites in input set) or network is sparse: betweenness scores may be uninformative with insufficient connectivity

## Inputs

- pathway-metabolite bipartite network (edge list or adjacency matrix)
- input metabolite list (character vector of KEGG IDs or metabolite identifiers)
- optional: metabolite-level annotations (names, pathway assignments)

## Outputs

- data.frame with columns: metabolite identifier, raw betweenness centrality, Relative Betweenness Centrality (RBC) score [0,1]
- Relative Betweenness Centrality (RBC) plot (ranked barplot or scatter visualization)
- optional: igraph object representing the filtered pathway-metabolite network

## How to apply

Load the pathway-metabolite network and input metabolite list into R. Construct a bipartite igraph object with metabolites and pathways as nodes and membership relationships as edges. Filter the graph to retain only metabolites in your input set. Compute raw betweenness centrality for each metabolite node using igraph::betweenness(). Normalize betweenness values to the [0,1] range by dividing by the graph's maximum possible centrality (or scaling to the observed maximum), producing Relative Betweenness Centrality (RBC) scores. Generate a data.frame with metabolite identifiers, RBC scores, and optional pathway annotations. Visualize the RBC distribution using a ranked barplot or scatter plot to highlight which input metabolites occupy central topological positions.

## Related tools

- **igraph** (Construct bipartite graph, compute betweenness centrality for metabolite and pathway nodes) — https://igraph.org
- **KEGGREST** (Retrieve pathway-to-metabolite mappings from KEGG database) — https://bioconductor.org/packages/KEGGREST
- **enrichmet** (Wrapper function that integrates graph construction, centrality computation, and RBC visualization into a single workflow) — https://github.com/biodatalab/enrichmet
- **R** (Execution environment for igraph and data manipulation)

## Examples

```
results <- enrichmet(inputMetabolites = inputMetabolites, PathwayVsMetabolites = PathwayVsMetabolites, example_data = example_data, analysis_type = c('centrality'), top_n = 15)
```

## Evaluation signals

- RBC values fall within [0, 1] range and sum of normalized scores across all metabolites is meaningful relative to network density
- Metabolites with high RBC appear in multiple pathways in the input mapping; low-RBC metabolites are peripheral or pathway-specific
- RBC plot is sorted in descending order; visual inspection confirms hub metabolites (e.g., glucose, ATP, CoA) rank highest in typical metabolic networks
- Betweenness centrality and RBC rank order remain stable when recomputing on the same network, confirming reproducibility
- No metabolites have undefined or infinite centrality scores; all input metabolites present in output data.frame with valid numeric RBC

## Limitations

- Betweenness centrality is computationally expensive (O(n²) or O(n³) depending on algorithm); large networks (>10,000 nodes) may require approximation
- Centrality scores depend critically on network completeness and accuracy; missing pathway-metabolite edges or incorrect mapping undermine interpretation
- Isolated metabolites (degree 0) have zero betweenness; filtering or separate handling may be required for complete input sets
- RBC normalization scheme affects absolute scores; different normalization methods (divide by max, by theoretical maximum, by graph diameter) yield non-comparable numeric values across different studies
- Bipartite network topology may obscure direct metabolite-metabolite interactions (which are not represented as edges); consider supplementary analysis with metabolite-only or pathway-only projections

## Evidence

- [intro] task_003_finding_rbc_computation: "enrichmet computes betweenness centrality for metabolites and produces a Relative Betweenness Centrality (RBC) plot that displays RBC values on the x-axis to highlight the topological importance and"
- [intro] task_003_workflow_step_1: "Load the pathway-metabolite network data and KrasG12D metabolite input list into R. Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and"
- [intro] task_003_workflow_step_2: "Filter the network to retain only metabolites in the KrasG12D input set. Compute betweenness centrality for each metabolite node using igraph's betweenness centrality function. Normalize betweenness"
- [intro] task_003_workflow_step_3: "Generate a data.frame containing metabolite identifiers, RBC scores, and optional pathway annotations. Create the RBC plot visualization (e.g., barplot or ranked scatter) showing RBC values for all"
- [intro] enrichmet_igraph_integration: "enrichmet integrates fgsea for fast MetSEA, igraph for topology-based metrics, and curated KEGG data for enrichment using Fisher's Exact Test—all accessible via a single function call"
