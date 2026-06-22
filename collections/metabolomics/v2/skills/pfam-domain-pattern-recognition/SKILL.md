---
name: pfam-domain-pattern-recognition
description: Use when when you have a set of Biosynthetic Gene Clusters (BGCs) in GenBank format and need to identify statistically significant or topic-modeled co-occurrence patterns of Pfam domains and subPfams across multiple genes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3678
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

# Pfam Domain Pattern Recognition

## Summary

Recognition and extraction of Pfam domain and subPfam patterns from genes within Biosynthetic Gene Clusters to create tokenized sequence representations. This skill enables systematic identification of co-occurring domain motifs that characterize functional gene sub-clusters.

## When to use

When you have a set of Biosynthetic Gene Clusters (BGCs) in GenBank format and need to identify statistically significant or topic-modeled co-occurrence patterns of Pfam domains and subPfams across multiple genes. Apply this skill as the initial tokenization step before redundancy filtering and sub-cluster detection, or when you seek to link detected sub-clusters back to conserved domain architectures.

## When NOT to use

- Input BGCs have no Pfam domain annotations or lack functional gene annotation — domain pattern recognition requires curated domain assignments as input.
- Goal is to predict biosynthetic product structure directly from gene sequence without intermediate sub-cluster identification — this skill focuses on domain tokenization, not end-to-end product prediction.
- BGC dataset is already redundancy-filtered and you only need to apply statistical or topic-based sub-cluster detection — skip to PRESTO-STAT or PRESTO-TOP instead.

## Inputs

- Biosynthetic Gene Clusters in GenBank format
- Gene annotations with Pfam domain assignments
- Pfam domain database with subPfam hierarchy

## Outputs

- Tokenized BGC representations (Pfam and subPfam token sequences per gene)
- Domain composition profiles per gene
- Adjacency matrices or co-occurrence frequency tables of domain patterns

## How to apply

First, represent each gene in the BGC as a combination of its annotated Pfam domains, using subPfams to increase resolution and granularity of the token representation. This creates a token string per gene that captures the domain architecture. The rationale is that Pfam domains encode functional modules of biosynthetic enzymes; subPfams further discriminate between functional subtypes (e.g., different condensation domain variants). Once tokenized, these representations become amenable to statistical co-occurrence analysis (PRESTO-STAT) or topic modeling (PRESTO-TOP) to detect patterns that recur across many BGCs. The choice of subPfam resolution affects sensitivity: finer tokenization reveals more specific domain combinations but risks over-segmentation; coarser Pfam-only tokenization is more robust but may mask functional distinction.

## Related tools

- **iPRESTO** (Command-line platform that implements Pfam/subPfam tokenization, redundancy filtering, and sub-cluster detection (PRESTO-STAT and PRESTO-TOP) on BGCs)

## Evaluation signals

- All genes in input BGCs have been assigned at least one Pfam or subPfam token; no genes are left untokenized.
- Token composition reflects known biosynthetic enzyme architectures (e.g., polyketide synthase genes contain expected condensation, ketoreductase, and ACP domain tokens).
- Adjacency Index or domain co-occurrence frequency matrix is symmetric and non-negative; no NaN or infinite values present.
- When redundancy filtering is subsequently applied, the Adjacency Index correctly identifies highly similar tokenized BGCs as neighbors in the similarity network.
- Detected sub-clusters contain genes whose tokens show statistically significant or topic-weighted co-occurrence patterns that are rare or absent in random BGC samples.

## Limitations

- Tokenization accuracy depends on completeness and quality of upstream Pfam domain annotation; unannotated genes or missing domains will degrade pattern detection.
- SubPfam resolution introduces trade-off: finer granularity increases sensitivity to domain variants but risks false fragmentation and reduces statistical power if individual sub-cluster patterns are rare.
- Pfam domains are ortholog-based and may not capture species-specific or novel biosynthetic adaptations that lie outside Pfam HMM definitions.
- The Adjacency Index distance metric assumes co-occurrence patterns are uniform across genomic contexts; gene order and synteny are not explicitly modeled in token representation.

## Evidence

- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] For the detection of sub-clusters two methods are used: PRESTO-STAT, which is based on the statistical algorithm from Del Carratore et al. (2019): "For the detection of sub-clusters two methods are used: PRESTO-STAT, which is based on the statistical algorithm from Del Carratore et al. (2019)"
- [intro] Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [intro] iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters: "iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters"
