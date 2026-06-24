---
name: bgc-tokenization-with-pfam-domains
description: Use when you have GenBank-format BGC sequences annotated with Pfam domain
  assignments and you need to prepare them for sub-cluster detection, redundancy filtering
  via similarity networks, or linking to natural product substructures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0202
  - http://edamontology.org/topic_0749
  tools:
  - iPRESTO
  - Pfam
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

# BGC tokenization with Pfam domains

## Summary

Represent each gene in a Biosynthetic Gene Cluster as a token string combining its Pfam domain and subPfam annotations, enabling downstream sub-cluster detection and redundancy filtering. This tokenization transforms raw domain annotations into a standardized symbolic representation suitable for similarity metrics and pattern discovery.

## When to use

Apply this skill when you have GenBank-format BGC sequences annotated with Pfam domain assignments and you need to prepare them for sub-cluster detection, redundancy filtering via similarity networks, or linking to natural product substructures. Use it as the entry point to the iPRESTO pipeline before any filtering or sub-cluster search.

## When NOT to use

- BGC sequences that lack Pfam domain annotations or lack sufficient domain coverage to produce meaningful tokens
- If your analysis goal is direct sequence alignment or phylogenetic comparison rather than functional sub-cluster discovery
- When input genes are already represented as domain tokens or feature vectors; re-tokenization would be redundant

## Inputs

- GenBank-format BGC sequences
- Pfam domain annotations per gene
- subPfam assignments (optional but recommended for increased resolution)

## Outputs

- Tokenized BGC data (one token string per gene)
- Token vocabulary or domain-to-token mapping

## How to apply

Load BGC sequences from GenBank files and annotate each gene with Pfam domain assignments via domain scanning. Augment the Pfam annotations with subPfam assignments to increase functional resolution and discriminatory power. Represent each gene as a single token string that concatenates its Pfam domains and subPfams in a consistent order. The rationale is that this tokenization creates a discrete, comparable representation of gene function that allows Adjacency Index distance metrics to measure similarity between BGCs and supports detection of functionally coherent sub-clusters within larger clusters.

## Related tools

- **iPRESTO** (Command-line tool that integrates BGC tokenization, redundancy filtering, and sub-cluster detection; performs domain scanning and orchestrates the full pipeline) — https://github.com/medema-group/iPRESTO
- **Pfam** (Database and tool for protein domain identification; provides the domain annotations that form the basis of tokenization) — https://pfam.xfam.org/

## Evaluation signals

- Each gene in the tokenized BGC has exactly one token string (no missing or duplicate tokens per gene)
- All Pfam and subPfam domain IDs referenced in tokens exist in the Pfam database and are consistent across the dataset
- Tokenized genes within the same BGC are identical in format; tokens can be directly compared using Adjacency Index distance
- Token strings for genes with identical domain compositions (same Pfam + subPfam set) are identical across different BGCs, enabling correct similarity computation
- Downstream redundancy filtering using Adjacency Index produces a non-redundant BGC set with expected cluster topology (connected components in similarity network)

## Limitations

- Tokenization relies on complete and accurate Pfam annotations; genes with no detected domains or incomplete scans will produce empty or uninformative tokens
- subPfam resolution increases specificity but also sparsity; rare domain combinations may not cluster well if subPfam assignments are too granular
- The token representation discards domain order and structural context within the gene; only domain composition is preserved
- Tokenization does not account for domain copy number or tandem repeats unless explicitly encoded in the subPfam hierarchy

## Evidence

- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [other] Each gene in a BGC is tokenised by representing it as a combination of its Pfam domains, with subPfams employed to increase resolution of the domain annotation.: "Each gene in a BGC is tokenised by representing it as a combination of its Pfam domains, with subPfams employed to increase resolution of the domain annotation."
- [other] Load BGC sequences from GenBank format files. Annotate each gene in the BGC with Pfam domain assignments using domain scanning. Augment Pfam annotations with subPfam assignments to increase functional resolution.: "Load BGC sequences from GenBank format files. Annotate each gene in the BGC with Pfam domain assignments using domain scanning. Augment Pfam annotations with subPfam assignments"
- [other] Represent each gene as a token string combining its Pfam domains and subPfams. Output tokenized BGC data with one token string per gene.: "Represent each gene as a token string combining its Pfam domains and subPfams. Output tokenized BGC data with one token string per gene."
