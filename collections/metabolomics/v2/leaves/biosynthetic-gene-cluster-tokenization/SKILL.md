---
name: biosynthetic-gene-cluster-tokenization
description: Use when you have GenBank-formatted BGC records and need to prepare them
  for sub-cluster detection, domain pattern analysis, or comparison across multiple
  BGCs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0160
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

# biosynthetic-gene-cluster-tokenization

## Summary

Convert Biosynthetic Gene Clusters (BGCs) into standardized token sequences by representing each gene as a combination of Pfam domains and subPfams, enabling quantitative comparison and downstream detection of functionally coherent sub-clusters. This tokenization is the essential preprocessing step that converts unstructured genomic annotations into discrete, comparable feature vectors.

## When to use

You have GenBank-formatted BGC records and need to prepare them for sub-cluster detection, domain pattern analysis, or comparison across multiple BGCs. Apply this skill when your input is raw BGC annotations (gene coordinates, functional annotations) and your goal is to enable statistical or topic-modelling-based sub-cluster discovery. Skip this if your BGCs are already represented as domain token sequences.

## When NOT to use

- Input BGCs lack Pfam or subPfam annotations — tokenization requires pre-computed domain assignments.
- BGCs are already tokenized or represented as domain feature matrices — re-tokenization would be redundant.
- Your goal is to study nucleotide-level or protein sequence-level features directly, not domain architecture patterns.

## Inputs

- GenBank-formatted Biosynthetic Gene Cluster records
- Gene functional annotations with Pfam domain assignments
- subPfam annotation tables or lookup resources

## Outputs

- Tokenized BGC sequences (each gene as Pfam+subPfam token)
- Structured token table with gene ID, genomic position, and token representation
- Metadata linking tokens back to original gene coordinates and annotations

## How to apply

Load BGC sequences in GenBank format and systematically convert each gene into a token by identifying its constituent Pfam domains and subPfams. Represent each gene as an ordered combination (e.g., 'PF00001+subPF_a', 'PF00042+subPF_b') to capture both broad functional class and fine-grained specificity. The use of subPfams increases resolution beyond standard Pfam annotations, allowing detection of subtle domain variations. Store the resulting token sequence with genomic coordinates (gene index, position) preserved. Output should be a structured table or file where each row represents one gene, with columns for gene ID, genomic position, and token representation (Pfam+subPfam combination). This tokenized representation is then ready for redundancy filtering via similarity networks (Adjacency Index distance metric) or direct input to PRESTO-STAT or PRESTO-TOP sub-cluster detection methods.

## Related tools

- **iPRESTO** (Command-line tool that implements BGC tokenization and sub-cluster detection; uses Pfam and subPfam tokenization as input to PRESTO-STAT and PRESTO-TOP methods)

## Evaluation signals

- All genes in the BGC are assigned a token; no gene is skipped or marked as unknown.
- Each token is a valid Pfam+subPfam combination present in the reference annotation set.
- Token sequences preserve gene order and genomic coordinates; can be aligned back to the original BGC record.
- Redundancy-filtered networks can be constructed from tokenized BGCs using Adjacency Index; similar BGCs cluster together.
- Downstream sub-cluster detection (PRESTO-STAT or PRESTO-TOP) produces coherent, biologically interpretable sub-clusters from the tokenized input.

## Limitations

- Tokenization quality depends on completeness and accuracy of Pfam and subPfam annotations; unannotated or misannotated genes reduce signal.
- Genes with no detected Pfam domains cannot be tokenized and may be excluded or assigned a null token, potentially losing important genomic context.
- SubPfam resolution is not standardized across all BGC domains; some gene families may have sparse or inconsistent subPfam coverage.
- Tokenization discards sequence-level information (nucleotide composition, codon usage, regulatory elements) that may be relevant for some analyses.

## Evidence

- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters: "iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters"
- [intro] Tokenise BGCs by representing each gene as a combination of Pfam domains and subPfams: "Tokenize BGCs by representing each gene as a combination of Pfam domains and subPfams"
