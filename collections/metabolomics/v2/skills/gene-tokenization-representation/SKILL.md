---
name: gene-tokenization-representation
description: Use when when you have GenBank-format BGC sequences with Pfam domain
  annotations and need to prepare them for sub-cluster detection, redundancy filtering,
  or natural product structure association.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
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

# gene-tokenization-representation

## Summary

Represent each gene in a Biosynthetic Gene Cluster as a token string combining its Pfam domains and subPfams to enable downstream sub-cluster detection and functional annotation. This tokenization converts sequence-level gene annotations into discrete, composable domain tokens suitable for pattern mining and similarity-based filtering.

## When to use

When you have GenBank-format BGC sequences with Pfam domain annotations and need to prepare them for sub-cluster detection, redundancy filtering, or natural product structure association. Specifically, use this skill when individual genes must be represented as domain combinations rather than raw sequences, and when Pfam domain resolution alone is insufficient and subPfam augmentation is desired.

## When NOT to use

- Input genes lack Pfam domain annotations or are unannotated sequences; use raw sequence comparison or ab initio domain prediction first.
- Genes are already represented as numerical feature vectors or pre-computed domain vectors; tokenization is for sequence-annotation-to-token conversion, not post-hoc featurization.
- Only standard Pfam families are required and subPfam resolution is not needed; simple Pfam concatenation without subPfam augmentation suffices.

## Inputs

- GenBank-format BGC sequence files
- Pfam domain scan results per gene
- subPfam annotations per gene (optional but recommended for increased resolution)

## Outputs

- Tokenized BGC data (one token string per gene)
- Gene-to-token mapping table
- Token vocabulary for the BGC collection

## How to apply

Load each BGC from GenBank format and annotate all genes with Pfam domain assignments using domain scanning tools. Augment Pfam annotations with subPfam assignments to increase functional resolution beyond standard Pfam families. For each gene, construct a token string by concatenating its assigned Pfam domains and corresponding subPfams in a consistent order. Output the tokenized BGC with one token string per gene, preserving gene-to-token mapping for downstream filtering or clustering steps. The token representation enables subsequent similarity-network construction using Adjacency Index metrics and PRESTO-STAT or PRESTO-TOP sub-cluster detection.

## Related tools

- **iPRESTO** (Command-line tool that tokenizes BGCs by representing each gene as a combination of Pfam domains and subPfams, and subsequently detects sub-clusters from tokenized representations)

## Evaluation signals

- Every gene in the input BGC has a corresponding non-empty token string in the output (no missing tokens).
- Token strings contain only valid Pfam identifiers (PF\d+) and subPfam identifiers, with consistent formatting across all tokens.
- Gene-to-token mapping preserves BGC genomic order and gene boundaries (no gene merging or loss).
- Tokenized BGC collection can be successfully ingested into downstream redundancy filtering (similarity network construction) without format errors.
- Token strings derived from genes with the same Pfam domain composition show identical or near-identical tokens, validating consistent concatenation logic.

## Limitations

- Tokenization quality depends entirely on upstream Pfam annotation accuracy; missing or mis-assigned domains will propagate into token representations.
- Token string representation discards spatial information (gene order and synteny context within the BGC), which may be recovered later in sub-cluster detection but is not explicit in the token itself.
- subPfam augmentation increases resolution but requires additional annotation resources; availability varies by organism and domain family.
- Concatenation order of domains within a token must be standardized; inconsistent ordering will create spurious token diversity and reduce clustering efficacy.

## Evidence

- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [other] Each gene in a BGC is tokenised by representing it as a combination of its Pfam domains, with subPfams employed to increase resolution of the domain annotation.: "Each gene in a BGC is tokenised by representing it as a combination of its Pfam domains, with subPfams employed to increase resolution of the domain annotation."
- [other] 1. Load BGC sequences from GenBank format files. 2. Annotate each gene in the BGC with Pfam domain assignments using domain scanning. 3. Augment Pfam annotations with subPfam assignments to increase functional resolution. 4. Represent each gene as a token string combining its Pfam domains and subPfams.: "Load BGC sequences from GenBank format files. 2. Annotate each gene in the BGC with Pfam domain assignments using domain scanning. 3. Augment Pfam annotations with subPfam assignments to increase"
