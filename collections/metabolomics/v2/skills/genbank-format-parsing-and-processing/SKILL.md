---
name: genbank-format-parsing-and-processing
description: Use when you have BGC sequences in GenBank format and need to extract gene-level features (coordinates, sequences, functional annotations) as input to domain annotation and tokenization pipelines. Use this skill when starting a BGC analysis from raw GenBank files rather than pre-parsed gene lists.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3209
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0080
  tools:
  - iPRESTO
  - BioPython
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

# GenBank format parsing and processing

## Summary

Load and parse Biosynthetic Gene Cluster sequences from GenBank format files to extract gene coordinates, annotations, and metadata. This is the foundational step for downstream tokenization and sub-cluster detection workflows.

## When to use

You have BGC sequences in GenBank format and need to extract gene-level features (coordinates, sequences, functional annotations) as input to domain annotation and tokenization pipelines. Use this skill when starting a BGC analysis from raw GenBank files rather than pre-parsed gene lists.

## When NOT to use

- Input is already a pre-computed domain annotation matrix or token string — skip directly to tokenization or filtering.
- BGC data is already in a parsed, tabular format (e.g., CSV or TSV with gene IDs and sequences) — you may skip file parsing and begin with domain annotation.
- You are working with non-BGC sequences or sequences without gene feature annotations — parsing will succeed but downstream tokenization will lack the necessary domain context.

## Inputs

- GenBank format files (.gb, .gbk) containing Biosynthetic Gene Cluster sequences
- BGC sequence records with gene feature annotations

## Outputs

- Parsed gene records with coordinates and sequence data
- Structured feature table mapping genes to BGCs
- Gene sequences ready for domain annotation

## How to apply

Load GenBank format files containing BGC sequences using a BioPython-compatible parser or iPRESTO's input module. Extract gene records including their genomic coordinates, CDS features, and existing annotations. Validate that each record contains sequence data and identifiable gene features. The parsed output should be a structured representation (e.g., a feature table or sequence object list) where each gene is linked to its parent BGC and ready for subsequent Pfam domain annotation. iPRESTO uses this parsed structure to enable the tokenization step.

## Related tools

- **iPRESTO** (Command-line tool that ingests GenBank files and orchestrates parsing, tokenization, and sub-cluster detection of BGCs)
- **BioPython** (Python library for parsing and manipulating GenBank format files and sequence records)

## Evaluation signals

- All genes in each BGC are successfully extracted with non-null coordinates and sequence data.
- Parsed gene records maintain one-to-one correspondence with CDS features in the original GenBank file.
- Sequence lengths match coordinate spans (end − start); no truncation or corruption of sequences.
- Downstream Pfam annotation step successfully receives and processes gene sequences without parse errors.
- Parsed BGC structure preserves metadata (organism, cluster name, accession) for traceability.

## Limitations

- GenBank files with incomplete or malformed feature annotations may yield partial gene records; validation and error handling are required.
- Some older or non-standard GenBank submissions may lack structured gene features; manual curation may be needed.
- Large GenBank files (thousands of genes) may require memory-efficient streaming or chunked parsing to avoid resource exhaustion.

## Evidence

- [other] Load BGC sequences from GenBank format files: "Load BGC sequences from GenBank format files."
- [intro] GenBank is the input format for BGC data in iPRESTO workflows: "a set of Biosynthetic Gene Clusters (BGCs) in GenBank format"
- [other] Parsed sequences enable subsequent domain annotation and tokenization: "Annotate each gene in the BGC with Pfam domain assignments using domain scanning."
