---
name: network-topology-analysis-for-bgc-deduplication
description: Use when when you have a collection of tokenised BGCs (each gene represented
  as Pfam domain tokens) and need to remove near-duplicate or highly similar clusters
  before detecting biosynthetic sub-clusters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0622
  tools:
  - iPRESTO
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1010462
  title: iPRESTO
evidence_spans:
- iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters
  Tool) is a command line tool for the detection of gene sub-clusters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ipresto_cq
    doi: 10.1371/journal.pcbi.1010462
    title: iPRESTO
  dedup_kept_from: coll_ipresto_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1010462
  all_source_dois:
  - 10.1371/journal.pcbi.1010462
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# network-topology-analysis-for-bgc-deduplication

## Summary

Filter redundant tokenised Biosynthetic Gene Clusters (BGCs) by constructing a similarity network where nodes are BGCs and edges are weighted by Adjacency Index distance between their Pfam domain tokens, then remove clusters based on network topology or similarity threshold. This identifies and retains only non-redundant BGCs for downstream sub-cluster detection.

## When to use

When you have a collection of tokenised BGCs (each gene represented as Pfam domain tokens) and need to remove near-duplicate or highly similar clusters before detecting biosynthetic sub-clusters. Use this skill if your BGC collection is large enough that redundancy poses a risk to statistical power or computational efficiency in sub-cluster detection (e.g., multiple similar strains in GenBank).

## When NOT to use

- Your BGC collection is already known to be non-redundant or curated for diversity (e.g., manually selected representatives from each species).
- You have not yet tokenised your BGCs into Pfam domain sequences; apply tokenisation before this skill.
- Your analysis goal requires retaining all BGCs, including close homologs, to study sequence variation or strain-level diversity; this skill removes such variants.

## Inputs

- Tokenised BGCs: collection of gene clusters, each represented as a sequence of Pfam domain and subPfam tokens
- Distance matrix or pairwise distance data computed using Adjacency Index metric

## Outputs

- Filtered non-redundant BGC set: a subset of the input BGCs with redundant clusters removed
- Similarity network graph: nodes (BGCs) and edges weighted by Adjacency Index distance
- Network topology metadata: cluster assignments or edge weight distributions for validation

## How to apply

Load all tokenised BGCs into memory, where each BGC is a sequence of Pfam domains and subPfams. Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance metric—this metric measures how similarly domains are arranged across BGCs. Construct an undirected weighted similarity network from the complete distance matrix, treating BGCs as nodes and distances as edge weights. Identify redundant BGCs by analyzing network topology (e.g., detecting highly connected clusters or cliques) or by applying a similarity threshold on edge weights (e.g., retaining only one representative from groups with Adjacency Index distance below a cutoff). Export the filtered BGC set, which contains only non-redundant clusters suitable for downstream sub-cluster analysis.

## Related tools

- **iPRESTO** (Command-line tool that orchestrates tokenisation, redundancy filtering via similarity network construction and Adjacency Index distance, and sub-cluster detection linked to natural product substructures)

## Evaluation signals

- Output BGC set size is smaller than input (redundant clusters successfully removed); document the reduction ratio.
- All output BGCs are mutually dissimilar according to the Adjacency Index metric above the chosen threshold; spot-check pairwise distances.
- Network connectivity is reduced after filtering (isolated nodes or sparse sub-graphs remain); inspect edge counts before and after.
- Downstream sub-cluster detection (PRESTO-STAT or PRESTO-TOP) shows improved statistical power or sensitivity; compare findings on filtered vs. unfiltered input.
- Visual inspection of the similarity network shows clear cluster structure and removal of high-degree hubs that represent redundant families.

## Limitations

- Adjacency Index metric is sensitive to domain order and spacing; highly divergent BGCs with rearranged domains may appear dissimilar even if functionally similar.
- Choice of similarity threshold is not data-driven in the provided work; users must select cutoff empirically or justify post-hoc.
- Network topology analysis scales quadratically with BGC count; very large collections (>10,000 BGCs) may require sampling or approximate methods.
- Filtering removes information; losing a rare variant or outlier BGC may reduce discovery of novel biosynthetic functions.
- Adjacency Index relies on complete Pfam domain annotation; poorly annotated or fragmented BGCs may not be reliably compared.

## Evidence

- [intro] Tokenised BGCs are filtered for redundancy by constructing a similarity network that uses the Adjacency Index of domains as a distance metric to measure similarity between BGCs and remove redundant clusters.: "Tokenised BGCs are filtered for redundancy by constructing a similarity network that uses the Adjacency Index of domains as a distance metric to measure similarity between BGCs and remove redundant"
- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [other] Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance metric.: "Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance metric."
- [other] Construct a similarity network from the distance matrix. Identify and remove redundant BGCs based on network topology or similarity threshold.: "Construct a similarity network from the distance matrix. 4. Identify and remove redundant BGCs based on network topology or similarity threshold."
- [intro] iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters: "iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters"
