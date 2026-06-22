---
name: similarity-network-construction-from-domain-adjacency
description: Use when you have a collection of tokenized BGCs (each gene represented as a combination of Pfam domains and subPfams) and need to identify and remove redundant or highly similar clusters before downstream analysis such as sub-cluster detection or natural product annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3500
  tools:
  - iPRESTO
derived_from:
- doi: 10.1371/journal.pcbi.1010462
  title: iPRESTO
evidence_spans:
- iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# similarity-network-construction-from-domain-adjacency

## Summary

This skill constructs a similarity network from tokenized biosynthetic gene clusters (BGCs) using the Adjacency Index of Pfam domains as a distance metric. It enables identification and removal of redundant BGCs by measuring pairwise domain-level similarity and organizing results into a graph topology amenable to clustering and filtering.

## When to use

Apply this skill when you have a collection of tokenized BGCs (each gene represented as a combination of Pfam domains and subPfams) and need to identify and remove redundant or highly similar clusters before downstream analysis such as sub-cluster detection or natural product annotation. Use it specifically when domain composition similarity is a meaningful proxy for functional or structural redundancy in your BGC dataset.

## When NOT to use

- Input BGCs are not yet tokenized or lack Pfam domain annotations.
- You require similarity metrics based on nucleotide or protein sequence alignment rather than domain composition.
- Your downstream analysis explicitly requires the full population of BGCs including known redundancy (e.g., population statistics or diversity surveys).

## Inputs

- Collection of tokenized BGCs (Pfam domain token sequences)
- GenBank-format BGC records or equivalent structured BGC representation

## Outputs

- Pairwise distance matrix (BGC × BGC, using Adjacency Index metric)
- Similarity network (nodes = BGCs, edges = similarity/distance relationships)
- Filtered, non-redundant BGC set

## How to apply

Load all tokenized BGCs where each gene is encoded as its constituent Pfam domains and subPfams. Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance metric—this metric quantifies how similar the domain compositions and their adjacency patterns are between pairs of clusters. Construct a similarity network by treating BGCs as nodes and connecting them with edges weighted by or thresholded by the computed distances. Apply network topology analysis or a similarity threshold to identify clusters of redundant BGCs, then remove one representative per redundant group, retaining the non-redundant BGC set. The rationale is that domain-level adjacency patterns capture the functional and biosynthetic signature of a BGC; clusters with high Adjacency Index similarity represent largely redundant genetic content and can be safely deduplicated.

## Related tools

- **iPRESTO** (Command-line tool that implements tokenization of BGCs via Pfam domains and redundancy filtering via Adjacency Index similarity networks)

## Evaluation signals

- Verify that the distance matrix is symmetric and square (n BGCs × n BGCs) with zero diagonal.
- Confirm that the resulting similarity network has expected connectivity—isolated nodes or very dense regions may indicate parameter mistuning.
- Check that the filtered BGC set size is smaller than the input and that removed BGCs are indeed high-similarity neighbors in the network.
- Validate that Adjacency Index distances correlate with visual inspection or independent similarity measures (e.g., shared domain counts or Jaccard similarity on domain sets).
- Ensure that the non-redundant set retains sufficient diversity to capture all major BGC archetypes present in the original collection.

## Limitations

- The Adjacency Index metric is sensitive to domain order and adjacency; BGCs with identical domains in different orders may be scored as less similar than expected.
- The skill requires pre-computed or readily available Pfam domain annotations; poor or incomplete annotations will reduce the quality of redundancy detection.
- The choice of similarity threshold for filtering is not data-driven in the current description and must be set manually or via external validation; no principled threshold selection is provided.
- The method may not distinguish between genuinely redundant BGCs and functionally distinct clusters that happen to share similar domain compositions.

## Evidence

- [intro] Tokenization and redundancy filtering approach: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] Adjacency Index as distance metric in similarity network: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [intro] Workflow structure for network construction and filtering: "The sub-clusters found with iPRESTO can then be linked to Natural Product substructures"
- [intro] iPRESTO tool context: "iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters"
