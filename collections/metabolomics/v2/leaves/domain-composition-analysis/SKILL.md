---
name: domain-composition-analysis
description: Use when you have a set of Biosynthetic Gene Clusters in GenBank format
  and need to understand the domain architecture of constituent genes, either to detect
  statistically significant domain co-occurrence patterns within BGCs, to filter redundant
  BGCs by domain similarity, or to link detected.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3372
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

# Domain-Composition Analysis

## Summary

Analyze the Pfam domain and subPfam composition of genes within Biosynthetic Gene Clusters to identify and characterize domain patterns that distinguish sub-clusters. This skill enables tokenization and statistical profiling of BGC gene content to support sub-cluster detection and functional annotation.

## When to use

Apply this skill when you have a set of Biosynthetic Gene Clusters in GenBank format and need to understand the domain architecture of constituent genes, either to detect statistically significant domain co-occurrence patterns within BGCs, to filter redundant BGCs by domain similarity, or to link detected sub-clusters to specific natural product substructures.

## When NOT to use

- Input BGCs are already pre-filtered for domain redundancy or have been extensively curated; re-tokenization and re-filtering may introduce unnecessary computational overhead.
- Your goal is general BGC annotation or homology search rather than detection of statistically significant intra-cluster domain patterns or natural product sub-cluster linking.
- Pfam or subPfam annotations are unavailable or unreliable for the gene set; domain-based tokenization will not produce valid input for PRESTO-STAT.

## Inputs

- Biosynthetic Gene Clusters in GenBank format
- Pfam domain annotations per gene
- subPfam annotations (optional, for increased resolution)

## Outputs

- Tokenised BGC representations (gene × domain/subPfam vectors)
- Redundancy-filtered tokenised BGCs (via Adjacency Index similarity network)
- Detected sub-clusters with constituent genes and domain compositions
- Genomic positions and structural annotations of sub-clusters
- Structured sub-cluster output (linked to natural product substructures where available)

## How to apply

Tokenize each gene in the BGC by representing it as a vector of its Pfam domains, using subPfams to increase resolution where available. Compute the Adjacency Index of domains as a distance metric to quantify similarity between BGC domain compositions. Use this similarity network to filter the tokenised BGC set for redundancy, removing highly similar BGCs. For remaining non-redundant BGCs, apply the PRESTO-STAT statistical algorithm (based on Del Carratore et al. 2019) to detect statistically significant co-occurring domain patterns across the tokenised sequences. Extract and record detected sub-clusters with their constituent genes, full domain compositions, and genomic positions for downstream annotation and validation.

## Related tools

- **iPRESTO** (Command-line tool that orchestrates tokenization of BGCs using Pfam domains and subPfams, redundancy filtering via Adjacency Index similarity networks, and application of PRESTO-STAT and PRESTO-TOP statistical methods for sub-cluster detection and linking to natural product substructures.)

## Evaluation signals

- Tokenised BGC representations must contain valid Pfam and subPfam domain identifiers for every gene; check that no gene is represented as an empty token vector.
- Adjacency Index similarity values between BGC pairs must fall in the range [0, 1]; BGCs with similarity above a specified threshold (e.g., 0.9) should be marked as redundant and one retained per cluster.
- PRESTO-STAT sub-clusters must have statistically significant co-occurrence p-values (typically p < 0.05 or adjusted p < 0.01); verify that p-values are computed and reported for each detected sub-cluster.
- Detected sub-clusters must have genomic positions that fall within the span of their parent BGC; validate that all gene positions are contiguous or within acceptable gap thresholds.
- Sub-clusters linked to natural product substructures should have interpretable domain compositions consistent with known biosynthetic pathways (e.g., polyketide synthase domains for PKS-derived products).

## Limitations

- PRESTO-STAT relies on statistical power from sufficient redundancy-filtered BGC samples; small datasets may yield false negatives or unreliable co-occurrence estimates.
- Pfam and subPfam annotations are dependent on the completeness and curation of the reference database; novel or divergent domains may be missed or misclassified.
- Adjacency Index similarity is a coarse metric for redundancy filtering and may over-cluster functionally distinct BGCs with similar domain inventories but different arrangements.
- Sub-cluster detection is sensitive to tokenization granularity (i.e., choice of subPfams); different resolutions may yield overlapping or conflicting sub-cluster calls.
- Linking to natural product substructures requires a separate trained model or knowledge base; this skill produces sub-clusters but does not guarantee valid structure prediction.

## Evidence

- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] Tokenised BGCs are filtered for redundancy using similarity network with Adjacency Index of domains as distance metric: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [intro] PRESTO-STAT is based on statistical algorithm from Del Carratore et al. 2019 for detecting gene sub-clusters: "PRESTO-STAT, which is based on the statistical algorithm from Del Carratore et al. (2019)"
- [other] Sub-clusters are extracted with constituent genes, domain compositions, and genomic positions: "Extract and record detected sub-clusters with their constituent genes, domain compositions, and genomic positions"
- [intro] Sub-clusters found with iPRESTO can be linked to Natural Product substructures: "The sub-clusters found with iPRESTO can then be linked to Natural Product substructures"
