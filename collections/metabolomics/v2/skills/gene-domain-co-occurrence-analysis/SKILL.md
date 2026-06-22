---
name: gene-domain-co-occurrence-analysis
description: Use when you have a collection of BGCs tokenised as Pfam domain / subPfam combinations, have filtered them for redundancy using domain-based similarity networks, and need to discover latent gene sub-clusters that group together genes with correlated domain compositions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2495
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_0203
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

# gene-domain-co-occurrence-analysis

## Summary

Apply topic modelling with Latent Dirichlet Allocation (LDA) to redundancy-filtered, tokenised Biosynthetic Gene Clusters (BGCs) to detect coherent gene sub-clusters based on Pfam domain co-occurrence patterns. This skill identifies functionally related gene groupings within larger BGCs that may be linked to specific natural product biosynthetic steps.

## When to use

Apply this skill when you have a collection of BGCs tokenised as Pfam domain / subPfam combinations, have filtered them for redundancy using domain-based similarity networks, and need to discover latent gene sub-clusters that group together genes with correlated domain compositions. This is appropriate when seeking to link gene groupings to specific natural product substructures or to decompose large, complex BGCs into functionally coherent modules.

## When NOT to use

- Input BGCs have not been filtered for redundancy; apply redundancy filtering with domain-based similarity networks first.
- Genes in input BGCs are not yet tokenised as Pfam/subPfam combinations; tokenisation and domain annotation are prerequisites.
- You seek deterministic sub-cluster boundaries rather than probabilistic topic memberships; LDA produces soft assignments, not hard partitions.

## Inputs

- Redundancy-filtered tokenised BGCs in vector format (each gene represented as Pfam domain and subPfam combination)
- Domain co-occurrence frequency matrix or token-document representation suitable for LDA

## Outputs

- Gene sub-cluster assignments (mapping of gene identifiers to sub-cluster IDs)
- Topic-assignment weights table (per-gene topic probability scores across discovered sub-clusters)
- LDA topic model parameters (domain-topic and gene-topic distributions)

## How to apply

Load redundancy-filtered tokenised BGCs where each gene is represented as a Pfam domain / subPfam combination vector. Apply Latent Dirichlet Allocation topic modelling to the collection, treating domain co-occurrence patterns as the basis for topic inference. The LDA model learns latent topics (gene sub-clusters) by identifying which domains co-occur frequently across the BGC population. Extract topic-assignment weights for each gene and cluster genes by their dominant topic assignment. Structure the output as a table linking gene identifiers to assigned sub-cluster IDs and their corresponding topic-assignment weights. The rationale is that genes sharing similar domain compositions (high co-occurrence) likely participate in related biosynthetic steps and should cluster together; LDA captures this structure without requiring prior knowledge of sub-cluster boundaries.

## Related tools

- **iPRESTO** (Integrated command-line framework that orchestrates tokenisation, redundancy filtering, and sub-cluster detection (including PRESTO-TOP LDA-based sub-cluster inference) on BGCs) — https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1010462&type=printable

## Evaluation signals

- Gene-to-sub-cluster assignments are complete: every gene in the filtered input is assigned to at least one sub-cluster with a non-zero topic weight.
- Topic-assignment weights sum to 1.0 per gene (or are constrained to a valid probability simplex), confirming LDA model convergence.
- Detected sub-clusters exhibit high domain homogeneity: genes within the same sub-cluster share significantly more domain co-occurrence patterns than random sub-sets of genes.
- Sub-cluster granularity is biologically meaningful: when downstream linked to natural product substructures, sub-cluster domain composition aligns with known enzymatic roles in biosynthetic pathways.
- Model fit is reasonable: log-likelihood or perplexity metrics indicate the LDA model has converged and generalizes across held-out BGCs (if cross-validation is performed).

## Limitations

- LDA requires tuning of the number of latent topics (sub-clusters); no automatic method is provided in the article for selecting optimal topic count.
- Performance depends critically on prior redundancy filtering step; incomplete or aggressive filtering can distort co-occurrence patterns.
- LDA output is probabilistic and may assign single genes to multiple sub-clusters with comparable weights, complicating biological interpretation when hard assignments are needed.
- The method assumes that domain co-occurrence patterns alone are sufficient to detect functionally meaningful sub-clusters; it does not incorporate gene order, regulation, or other genomic context.

## Evidence

- [other] PRESTO-TOP is a novel sub-cluster detection method that applies topic modelling with Latent Dirichlet Allocation: "PRESTO-TOP is a novel sub-cluster detection method that applies topic modelling with Latent Dirichlet Allocation to identify gene sub-clusters from redundancy-filtered tokenised BGCs."
- [intro] Tokenisation by Pfam/subPfam combination: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] Redundancy filtering rationale: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [other] Domain co-occurrence as basis for sub-clustering: "Apply PRESTO-TOP topic modelling using Latent Dirichlet Allocation to identify coherent gene sub-clusters based on domain co-occurrence patterns."
- [other] Output structure with weights: "Extract and structure detected sub-clusters with gene membership and topic-assignment weights."
