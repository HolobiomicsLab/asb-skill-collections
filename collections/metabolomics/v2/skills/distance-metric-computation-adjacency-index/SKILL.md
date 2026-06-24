---
name: distance-metric-computation-adjacency-index
description: Use when you have a collection of tokenised BGCs (each gene represented
  as a combination of Pfam domains and subPfams) and need to identify redundant or
  highly similar clusters before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0630
  - http://edamontology.org/topic_0749
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

# Distance Metric Computation via Adjacency Index

## Summary

Compute pairwise distances between tokenised Biosynthetic Gene Clusters (BGCs) using the Adjacency Index of Pfam domains as a distance metric. This metric quantifies structural similarity between BGCs by measuring how domain neighbourhoods differ, enabling construction of similarity networks to identify and filter redundant clusters.

## When to use

Apply this skill when you have a collection of tokenised BGCs (each gene represented as a combination of Pfam domains and subPfams) and need to identify redundant or highly similar clusters before downstream analysis. Specifically, when you must construct a similarity network to compare BGC structure at the domain-adjacency level and measure which clusters are functionally or structurally equivalent.

## When NOT to use

- Input BGCs are not yet tokenised (i.e., raw gene sequences rather than domain annotations)—tokenization must precede distance computation.
- You seek to measure similarity at the sequence level (e.g., nucleotide or protein BLAST identity) rather than domain-architecture level; Adjacency Index is domain-centric.
- BGCs contain genes with no annotated Pfam domains, making domain adjacency patterns uninformative or incomplete.

## Inputs

- collection of tokenised BGCs in GenBank or tabular format
- BGC tokenization mapping (each gene as Pfam domain + subPfam combination)
- set of all pairwise BGC comparisons (or indices for all BGCs)

## Outputs

- pairwise distance matrix (BGC × BGC)
- similarity network (nodes = BGCs, edges weighted by Adjacency Index distance)
- redundancy clusters or flags identifying similar BGCs above distance threshold

## How to apply

Load all tokenised BGCs where each gene is represented as its constituent Pfam domains and subPfams. For each pair of BGCs, compute the Adjacency Index distance by comparing the adjacency patterns of domains within each cluster—this captures how domain neighbours differ between pairs. Construct a distance matrix from all pairwise comparisons. The rationale is that domain adjacency reflects functional constraints and evolutionary relationships in biosynthetic pathways; clusters with similar domain neighbourhoods are likely redundant variants. Use the resulting distance matrix to build a similarity network, then apply a distance threshold or network topology analysis to identify and flag redundant BGCs for removal.

## Related tools

- **iPRESTO** (command-line tool that integrates BGC tokenisation, Adjacency Index distance computation, similarity network construction, and redundancy filtering into a single workflow)

## Evaluation signals

- Distance matrix is symmetric and has zero diagonal (each BGC has distance 0 to itself).
- No negative distances; all Adjacency Index values are non-negative.
- Redundant BGCs (flagged by the network) have low pairwise distances, and non-redundant BGCs have higher distances or are separated by a threshold.
- Similarity network topology correctly reflects domain-adjacency relationships—highly similar domain architectures cluster together.
- Filtered output (non-redundant BGC set) is smaller than input, with removed BGCs showing high Adjacency Index similarity to retained members.

## Limitations

- Adjacency Index depends on accurate Pfam annotation; missing or misannotated domains will distort distance estimates.
- The metric may not capture functional differences if two BGCs share similar domain neighbourhoods but differ in gene order, orientation, or regulatory elements outside the Pfam architecture.
- Choosing the distance threshold or network density parameter requires domain expertise or empirical validation; no universally optimal threshold is provided in the article.
- Computational cost scales quadratically with the number of BGCs; very large datasets may require approximate or hierarchical clustering strategies not detailed in the paper.

## Evidence

- [intro] Adjacency Index distance metric for similarity network construction: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [intro] Tokenization represents each gene as combination of Pfam domains and subPfams: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [other] Pairwise distance computation and network construction workflow: "Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance metric"
- [other] Network topology used to identify and remove redundant BGCs: "Identify and remove redundant BGCs based on network topology or similarity threshold"
