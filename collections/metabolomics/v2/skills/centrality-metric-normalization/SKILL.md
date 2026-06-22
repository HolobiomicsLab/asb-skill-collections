---
name: centrality-metric-normalization
description: Use when after computing raw betweenness centrality scores for metabolites in a bipartite pathway-metabolite igraph network, when you need to identify metabolites with high topological influence for visualization in ranked plots or when comparing centrality across multiple metabolite subsets or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
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

# centrality-metric-normalization

## Summary

Normalize raw betweenness centrality values computed on a pathway-metabolite network to Relative Betweenness Centrality (RBC) scores in the [0,1] range, enabling comparison of metabolite topological importance across networks of different sizes and densities. This is essential for identifying metabolites with high regulatory influence in metabolic pathway systems.

## When to use

Apply this skill after computing raw betweenness centrality scores for metabolites in a bipartite pathway-metabolite igraph network, when you need to identify metabolites with high topological influence for visualization in ranked plots or when comparing centrality across multiple metabolite subsets or network configurations.

## When NOT to use

- Raw centrality scores have not yet been computed using igraph—apply betweenness centrality computation first.
- Input network is not bipartite (metabolite + pathway nodes) or edges do not represent metabolite-pathway membership—use undirected or differently-typed networks with caution.
- Goal is purely to rank metabolites by raw (non-normalized) centrality without comparison across network sizes—normalization adds overhead without benefit.

## Inputs

- pathway-metabolite bipartite igraph object (nodes: pathways + metabolites, edges: membership relations)
- vector or list of metabolite identifiers to analyze (subset of network nodes)
- raw betweenness centrality scores (numeric vector indexed by metabolite ID)

## Outputs

- data.frame with columns: metabolite_id, RBC_score (normalized [0,1]), optional pathway_annotation
- RBC plot object (barplot or ranked scatter) with metabolites ordered by RBC value
- numeric vector of normalized RBC scores suitable for downstream filtering or ranking

## How to apply

Load the pathway-metabolite bipartite igraph network with metabolites and pathways as nodes and membership edges. Use igraph's betweenness centrality function to compute raw centrality values for metabolite nodes. Normalize the raw centrality values to the [0,1] range by dividing each metabolite's centrality by the graph's maximum possible centrality (or the observed maximum centrality in the metabolite subset). Store the normalized RBC scores in a data.frame keyed by metabolite identifier alongside optional pathway annotations. Create a ranked visualization (e.g., barplot or scatter plot) ordered by RBC values to highlight metabolites with the greatest topological importance in the pathway network.

## Related tools

- **igraph** (Constructs pathway-metabolite bipartite graph, computes raw betweenness centrality for metabolite nodes, and provides maximum centrality reference for normalization)
- **R** (Host language for data manipulation, normalization arithmetic, and RBC plot generation using base graphics or ggplot2)
- **KEGGREST** (Retrieves pathway-metabolite mappings from KEGG to construct the bipartite network topology)
- **enrichmet** (Automated wrapper that integrates betweenness centrality computation and RBC normalization within a unified pathway enrichment workflow) — https://github.com/biodatalab/enrichmet

## Examples

```
# In R, after computing raw betweenness centrality on the igraph network: rbc_df <- data.frame(metabolite = names(centrality_values), RBC = centrality_values / max(centrality_values)); barplot(rbc_df$RBC, names.arg = rbc_df$metabolite, main = 'Relative Betweenness Centrality')
```

## Evaluation signals

- RBC values are bounded in [0, 1]: min(RBC) ≥ 0 and max(RBC) ≤ 1, with at least one metabolite achieving RBC ≈ 1.
- Sum or distribution of RBC scores is invariant to the absolute scale of raw centrality; visual ranking order matches expected topological importance (hub metabolites have high RBC).
- data.frame output has one row per input metabolite, no missing RBC values for metabolites present in the network, and metabolite identifiers match input identifiers.
- RBC plot displays metabolites sorted by RBC value in ascending or descending order, with visual separation between high- and low-centrality metabolites.
- Normalized RBC scores correlate positively with raw centrality (Pearson r > 0.99), confirming monotonic transformation without rank inversion.

## Limitations

- Normalization by maximum centrality assumes at least one metabolite exists in the network; small or disconnected networks may yield uninformative RBC distributions.
- Betweenness centrality is sensitive to network topology; pathway-metabolite network composition (which metabolites and pathways are included) directly affects centrality values and relative rankings.
- RBC does not account for metabolite quantitative abundance, expression level, or biochemical flux—it reflects only topological position in the curated KEGG pathway structure.
- If the pathway-metabolite mapping (from KEGG or Zenodo curated file) contains errors or omissions, RBC calculations inherit those biases.
- Bipartite networks with metabolites of drastically different degrees may produce RBC distributions with little separation; consider degree-normalized variants for such cases.

## Evidence

- [other] Compute betweenness centrality for each metabolite node using igraph's betweenness centrality function.: "Compute betweenness centrality for each metabolite node using igraph's betweenness centrality function."
- [other] Normalize betweenness centrality values to Relative Betweenness Centrality (RBC) by scaling to the [0,1] range or by the graph's maximum possible centrality.: "Normalize betweenness centrality values to Relative Betweenness Centrality (RBC) by scaling to the [0,1] range or by the graph's maximum possible centrality."
- [other] enrichmet computes betweenness centrality for metabolites and produces a Relative Betweenness Centrality (RBC) plot that displays RBC values on the x-axis to highlight the topological importance and potential regulatory influence of metabolites within the metabolic network.: "enrichmet computes betweenness centrality for metabolites and produces a Relative Betweenness Centrality (RBC) plot that displays RBC values on the x-axis to highlight the topological importance and"
- [other] Generate a data.frame containing metabolite identifiers, RBC scores, and optional pathway annotations.: "Generate a data.frame containing metabolite identifiers, RBC scores, and optional pathway annotations."
- [other] Create the RBC plot visualization (e.g., barplot or ranked scatter) showing RBC values for all KrasG12D metabolites.: "Create the RBC plot visualization (e.g., barplot or ranked scatter) showing RBC values for all KrasG12D metabolites."
- [other] Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and metabolites and edges encoding membership.: "Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and metabolites and edges encoding membership."
