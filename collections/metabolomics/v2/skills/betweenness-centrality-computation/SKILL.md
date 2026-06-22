---
name: betweenness-centrality-computation
description: Use when when you have a pathway-metabolite bipartite network and a filtered set of input metabolites (e.g., from differential analysis or experimental selection), and you need to rank metabolites by their topological importance within the network structure—i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0577
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0209
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Betweenness Centrality Computation for Metabolites

## Summary

Computes betweenness centrality (BC) for metabolite nodes in a pathway-metabolite bipartite network using igraph, then normalizes to Relative Betweenness Centrality (RBC) by scaling to [0,1] range to identify topologically important metabolites with potential regulatory influence.

## When to use

When you have a pathway-metabolite bipartite network and a filtered set of input metabolites (e.g., from differential analysis or experimental selection), and you need to rank metabolites by their topological importance within the network structure—i.e., how often they lie on shortest paths between other nodes, indicating gatekeeping or hub roles in metabolic regulation.

## When NOT to use

- Input metabolite set is empty or contains only 1–2 nodes (BC is undefined or trivial in sparse graphs).
- Network is already reduced to a single pathway or metabolite; betweenness requires multiple alternative paths.
- You only need to rank metabolites by direct edge count or local neighborhood size (use degree centrality instead).

## Inputs

- Pathway-metabolite network data (bipartite graph structure)
- Input metabolite list (e.g., KEGG identifiers from differential analysis)
- igraph graph object or edge/node lists suitable for graph construction

## Outputs

- data.frame with columns: metabolite_id, RBC_score, and optional pathway_annotations
- Relative Betweenness Centrality (RBC) plot (barplot or ranked scatter visualization)

## How to apply

First, construct the pathway-metabolite bipartite graph in igraph with metabolites and pathways as nodes and membership relationships as edges. Filter the network to retain only metabolites in your input set (e.g., KrasG12D-associated metabolites). Apply igraph's betweenness centrality function to compute raw BC scores for each metabolite node. Normalize raw BC values by dividing by the graph's theoretical maximum (or scaling to [0,1] range) to obtain Relative Betweenness Centrality (RBC) scores. Store results in a data.frame with metabolite identifiers, RBC scores, and optional pathway annotations. Verify that RBC values fall in [0,1] and that high-RBC metabolites align with biological expectations (e.g., hub intermediates like pyruvate or acetyl-CoA in central metabolism). Generate a visualization (barplot or ranked scatter) showing RBC values for all input metabolites, ranked by RBC score.

## Related tools

- **igraph** (Computes betweenness centrality scores for metabolite nodes in the pathway-metabolite bipartite graph) — https://igraph.org
- **KEGGREST** (Retrieves pathway-to-metabolite mappings from KEGG resource to populate bipartite network) — https://bioconductor.org/packages/KEGGREST
- **enrichmet** (Orchestrates end-to-end pathway enrichment analysis including centrality computation and RBC visualization) — https://github.com/biodatalab/enrichmet

## Examples

```
library(igraph); library(enrichmet); results <- enrichmet(inputMetabolites=c('C00001','C00002','C00003'), PathwayVsMetabolites=PathwayVsMetabolites, analysis_type=c('centrality')); head(results$centrality_results)
```

## Evaluation signals

- RBC values range from 0 to 1 with no NaN or infinite values; max RBC ≤ 1.0.
- High-RBC metabolites correspond to biochemically central compounds (e.g., pyruvate, acetyl-CoA) with known hub roles in metabolism.
- RBC ranking is stable across repeated computations (deterministic); no randomness in igraph betweenness unless graph construction uses stochastic methods.
- Metabolites with degree 1 (leaf nodes in network) have RBC = 0; metabolites with high degree and many shortest paths between pairs have RBC > 0.5.
- Final RBC plot shows expected rank ordering—biologically plausible intermediates rank higher than peripheral metabolites.

## Limitations

- Betweenness centrality is computationally expensive (O(n³) for dense graphs); very large networks (>1000 nodes) may be slow.
- RBC interpretation depends on network topology; disconnected components or sparse subnetworks may produce artificially high RBC values for nodes within them.
- Bipartite network structure (pathways and metabolites as separate node types) may bias centrality scores toward metabolites at pathway intersections rather than purely metabolic importance.
- KEGG pathway data used to construct the network is static and may not reflect tissue-specific or condition-specific pathway activity.

## Evidence

- [intro] betweenness centrality computation and RBC visualization: "enrichmet performs pathway enrichment analysis using Fisher's exact test, computes betweenness centrality for metabolites, and performs Metabolite Set Enrichment Analysis (MetSEA)."
- [other] bipartite network construction: "Construct the pathway-metabolite bipartite graph using igraph, with nodes representing both pathways and metabolites and edges encoding membership."
- [other] RBC normalization procedure: "Normalize betweenness centrality values to Relative Betweenness Centrality (RBC) by scaling to the [0,1] range or by the graph's maximum possible centrality."
- [other] RBC output structure and visualization: "Generate a data.frame containing metabolite identifiers, RBC scores, and optional pathway annotations. Create the RBC plot visualization (e.g., barplot or ranked scatter) showing RBC values for all"
- [readme] igraph tool application: "enrichmet integrates fgsea for fast MetSEA, igraph for topology-based metrics, and curated KEGG data for enrichment using Fisher's Exact Test"
