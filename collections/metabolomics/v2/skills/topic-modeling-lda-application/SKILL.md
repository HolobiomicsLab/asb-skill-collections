---
name: topic-modeling-lda-application
description: Use when you have redundancy-filtered, tokenized BGCs (each gene represented as a Pfam domain or subPfam combination) and you want to identify fine-grained gene sub-clusters whose membership is driven by co-occurrence patterns of protein domains rather than statistical significance alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0102
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
---

# topic-modeling-lda-application

## Summary

Apply Latent Dirichlet Allocation (LDA) topic modeling to redundancy-filtered, tokenized Biosynthetic Gene Clusters (BGCs) to discover coherent gene sub-clusters based on domain co-occurrence patterns. This skill identifies functionally related gene groupings within BGCs by treating each gene as a bag of Pfam domains and inferring latent topics that represent conserved sub-cluster signatures.

## When to use

Use this skill when you have redundancy-filtered, tokenized BGCs (each gene represented as a Pfam domain or subPfam combination) and you want to identify fine-grained gene sub-clusters whose membership is driven by co-occurrence patterns of protein domains rather than statistical significance alone. Apply LDA when you expect multiple overlapping sub-cluster themes within your BGC collection and need soft cluster assignments with topic weights.

## When NOT to use

- Input BGCs have not yet been tokenized or redundancy-filtered; preprocess first using domain tokenization and similarity-network filtering.
- You expect hard, non-overlapping cluster assignments; LDA produces soft (probabilistic) assignments. Use PRESTO-STAT or hierarchical clustering if discrete, exclusive sub-clusters are required.
- Your BGC dataset is very small (<50 BGCs) or domain diversity is very low; LDA requires sufficient variation in domain co-occurrence to infer meaningful topics.

## Inputs

- Redundancy-filtered tokenized BGCs (text format: each gene represented as Pfam domain and subPfam combinations)
- Gene identifier mapping (linking tokens to source gene/BGC coordinates)
- LDA hyperparameters (number of topics, alpha, beta priors)

## Outputs

- Sub-cluster assignment table (gene identifiers → sub-cluster IDs with topic-weight scores)
- LDA model object (fitted topic-word distributions and document-topic distributions)
- Topic interpretation data (top Pfam domains per topic, co-occurrence profiles)

## How to apply

Load the redundancy-filtered tokenized BGCs where each gene is represented as a combination of Pfam domains and subPfams. Configure an LDA model with an appropriate number of topics (inferred from your data size and domain diversity); each topic will represent a gene sub-cluster signature. Fit the LDA model to the domain token vectors, allowing the algorithm to learn which domain combinations co-occur frequently across your BGC collection. Extract the posterior topic assignments for each gene, including both the assigned sub-cluster ID and the topic-assignment weights (probabilities), which reflect the strength of membership. Structure the output as a sub-cluster assignment table linking gene identifiers to sub-cluster IDs and numeric topic scores for downstream filtering or biological interpretation.

## Related tools

- **iPRESTO** (Command-line tool implementing PRESTO-TOP (LDA-based sub-cluster detection) and orchestrating the full BGC tokenization, filtering, topic modeling, and sub-cluster linking workflow)

## Evaluation signals

- Verify that the output sub-cluster table has one row per input gene with non-null topic-assignment weights that sum to 1.0 (valid probability distribution).
- Check that discovered topics show coherent domain co-occurrence patterns (e.g., domains from the same metabolic pathway cluster together in high-weight topics).
- Confirm that genes with similar domain compositions are assigned to overlapping sub-clusters with comparable topic scores.
- Validate that the number of inferred topics is interpretable and reflects known functional heterogeneity in your BGC collection (e.g., polyketide synthase vs. non-ribosomal peptide synthetase sub-clusters).
- Downstream: verify that detected sub-clusters can be linked to known or predicted natural product substructures, confirming functional relevance.

## Limitations

- LDA requires manual selection of the number of topics; suboptimal choices can yield uninformative or over-fragmented sub-clusters. Use perplexity or coherence metrics to tune this hyperparameter.
- The method relies entirely on Pfam domain co-occurrence and cannot leverage gene order, synteny, or other sequence context; sub-clusters may conflate unrelated genes that happen to share domains.
- Topic interpretation is data-dependent; topics inferred from a small or biased BGC collection may not generalize to novel BGCs or other domains.

## Evidence

- [other] PRESTO-TOP topic modelling using Latent Dirichlet Allocation to identify coherent gene sub-clusters based on domain co-occurrence patterns: "Apply PRESTO-TOP topic modelling using Latent Dirichlet Allocation to identify coherent gene sub-clusters based on domain co-occurrence patterns"
- [intro] Tokenization and domain filtering for LDA input: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] Redundancy filtering before topic modeling: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [other] Sub-cluster output structure: "Extract and structure detected sub-clusters with gene membership and topic-assignment weights"
- [intro] PRESTO-TOP as novel LDA method: "the novel method PRESTO-TOP, which uses topic"
