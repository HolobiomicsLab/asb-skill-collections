---
name: sub-cluster-assignment-extraction
description: Use when after PRESTO-TOP topic modelling has been run on redundancy-filtered tokenised BGCs and raw topic assignments have been generated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0749
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

# sub-cluster-assignment-extraction

## Summary

Extract and structure gene-to-sub-cluster assignments and topic-assignment weights from Latent Dirichlet Allocation topic modelling results. This skill transforms the raw output of topic models into a queryable assignment table that links gene identifiers to detected sub-cluster IDs with associated confidence scores.

## When to use

Apply this skill after PRESTO-TOP topic modelling has been run on redundancy-filtered tokenised BGCs and raw topic assignments have been generated. Use it when you need to convert unstructured topic model output into a relational format suitable for downstream linkage to natural product substructures or for validation against known biosynthetic pathways.

## When NOT to use

- Input has not yet been tokenised and redundancy-filtered; run tokenization and Adjacency Index-based filtering first.
- Topic modelling has not been performed; this skill assumes LDA output already exists.
- Assignment table already exists in downstream format; extraction is redundant.

## Inputs

- Raw topic model output from PRESTO-TOP (LDA posterior distributions)
- Redundancy-filtered tokenised BGCs with gene identifiers
- Topic-gene membership matrix or similar LDA output format

## Outputs

- Sub-cluster assignment table (gene ID, sub-cluster ID, topic-assignment weight)
- Structured sub-cluster membership with topic scores
- Gene-to-sub-cluster mapping suitable for linkage to natural product substructures

## How to apply

After PRESTO-TOP topic modelling completes, parse the topic-gene membership matrix and extract three key components: (1) gene identifiers from the input tokenised BGCs; (2) topic assignments (the detected sub-cluster IDs inferred by LDA); (3) topic-assignment weights (posterior probabilities or membership scores reflecting the strength of each gene–sub-cluster association). Structure these into a table where each row represents one gene, with columns for gene ID, assigned sub-cluster ID, and corresponding topic score. The topic score indicates confidence: higher scores reflect stronger coherence with the sub-cluster's domain co-occurrence pattern. Filter or flag assignments with low confidence scores if downstream analysis requires high-confidence links only.

## Related tools

- **iPRESTO** (Command-line tool that performs tokenization, redundancy filtering, and PRESTO-TOP topic modelling; sub-cluster extraction operates on its output) — https://github.com/medema-group/iPRESTO

## Evaluation signals

- All genes from the input tokenised BGCs appear exactly once in the output assignment table.
- Topic-assignment weights are valid probabilities or membership scores in the expected range (e.g., 0–1 or 0–100); no NaN or infinite values.
- Sub-cluster IDs are consistent with the number of topics K inferred by the LDA model; no orphaned or duplicate assignments.
- Gene identifiers in the output table match identifiers from the input redundancy-filtered tokenised BGCs exactly (no truncation or corruption).
- Assignment table is joinable with tokenised BGC domain annotations and natural product substructure labels without reconciliation errors.

## Limitations

- Topic assignment quality depends on the quality of tokenisation (Pfam/subPfam resolution) and redundancy filtering (Adjacency Index threshold); poor upstream choices degrade output.
- LDA is stochastic; replicate runs with the same K may produce different topic orderings or label permutations; post-hoc matching or consensus strategies may be needed for reproducibility.
- Sub-cluster biological interpretability requires downstream validation (e.g., linkage to known natural product substructures); high topic scores do not guarantee functional relevance.
- Genes assigned to multiple topics with similar weights reflect genuine ambiguity in domain co-occurrence patterns; hard assignment (single sub-cluster per gene) may lose information.

## Evidence

- [other] Extract and structure detected sub-clusters with gene membership and topic-assignment weights: "Extract and structure detected sub-clusters with gene membership and topic-assignment weights."
- [other] Produce a sub-cluster output table linking gene identifiers to assigned sub-cluster IDs and topic scores: "Produce a sub-cluster output table linking gene identifiers to assigned sub-cluster IDs and topic scores."
- [other] PRESTO-TOP is a novel sub-cluster detection method that applies topic modelling with Latent Dirichlet Allocation to identify gene sub-clusters from redundancy-filtered tokenised BGCs: "PRESTO-TOP is a novel sub-cluster detection method that applies topic modelling with Latent Dirichlet Allocation to identify gene sub-clusters from redundancy-filtered tokenised BGCs."
- [intro] The sub-clusters found with iPRESTO can then be linked to Natural Product substructures: "The sub-clusters found with iPRESTO can then be linked to Natural Product substructures"
