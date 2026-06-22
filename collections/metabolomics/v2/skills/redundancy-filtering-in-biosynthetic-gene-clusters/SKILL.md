---
name: redundancy-filtering-in-biosynthetic-gene-clusters
description: Use when when you have a collection of tokenised BGCs (represented as combinations of Pfam domains and subPfams) that may contain redundant or near-identical sequences, and you need to reduce computational burden and avoid biased sub-cluster detection caused by over-representation of similar BGCs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0204
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Redundancy filtering in biosynthetic gene clusters

## Summary

Remove duplicate or highly similar tokenised biosynthetic gene clusters (BGCs) by constructing a similarity network and applying an Adjacency Index distance metric to identify and filter redundant clusters. This preprocessing step ensures downstream sub-cluster detection operates on a non-redundant set of BGCs.

## When to use

When you have a collection of tokenised BGCs (represented as combinations of Pfam domains and subPfams) that may contain redundant or near-identical sequences, and you need to reduce computational burden and avoid biased sub-cluster detection caused by over-representation of similar BGCs in the input set.

## When NOT to use

- Input BGCs are already known to be non-redundant or have been pre-filtered by other clustering methods
- You lack reliable Pfam domain annotations; the Adjacency Index metric depends on accurate domain tokenisation
- Your analysis goal requires preserving all input BGCs for population-level statistics or diversity assessments

## Inputs

- Tokenised BGCs (gene cluster collections with Pfam domain and subPfam annotations)
- Distance matrix or pairwise similarity scores computed via Adjacency Index of domains

## Outputs

- Filtered non-redundant BGC set (subset of input BGCs)
- Redundancy network or clustering assignment (optional, for QC)

## How to apply

Load the tokenised BGCs where each gene is represented by its Pfam domains and subPfams. Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance metric, which measures domain co-occurrence patterns. Construct a similarity network from the resulting distance matrix. Apply a similarity threshold or network topology analysis to identify clusters of redundant BGCs. Remove redundant members from each cluster, retaining a single representative per group. Export the resulting filtered, non-redundant BGC set for downstream analysis (e.g., sub-cluster detection).

## Related tools

- **iPRESTO** (Command-line tool that performs tokenisation of BGCs, computes Adjacency Index distance metrics, constructs similarity networks, and filters redundant BGCs as part of its automated sub-cluster detection pipeline)

## Evaluation signals

- Output BGC count is strictly less than or equal to input count; no BGCs are duplicated in the output
- Pairwise Adjacency Index distances between any two BGCs in the filtered set exceed the applied similarity threshold
- Network topology shows no connected components with more than one member; each redundant cluster is reduced to a single representative
- Manual spot-check: compare a sample of filtered BGCs against pre-filtered input to confirm removal of similar domains/subPfam patterns
- Downstream sub-cluster detection yields distinct, non-overlapping topic distributions or statistical patterns (indicating less biasing redundancy)

## Limitations

- Adjacency Index metric is sensitive to incomplete or low-confidence Pfam domain annotations; poor tokenisation will produce unreliable distances
- Choice of similarity threshold is not data-driven in the article; users must set or calibrate the threshold empirically
- The method does not preserve phylogenetic or ecological metadata; filtering is purely based on domain composition
- No guidance provided on handling edge cases (e.g., BGCs with no Pfam domains, singleton clusters)

## Evidence

- [other] Tokenised BGCs are filtered for redundancy by constructing a similarity network that uses the Adjacency Index of domains as a distance metric to measure similarity between BGCs and remove redundant clusters.: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [other] Each gene in a BGC is represented as a combination of Pfam domains, where subPfams increase resolution.: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [other] The workflow includes loading tokenized BGCs, computing pairwise distances, constructing a similarity network, identifying and removing redundant BGCs, and exporting the filtered set.: "1. Load tokenized BGCs (each gene represented as a combination of Pfam domains and subPfams). 2. Compute pairwise distances between all BGCs using the Adjacency Index of domains as the distance"
- [other] iPRESTO is the tool that performs this filtering operation.: "iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters"
