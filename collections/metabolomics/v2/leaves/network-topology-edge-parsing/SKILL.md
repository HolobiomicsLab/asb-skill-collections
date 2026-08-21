---
name: network-topology-edge-parsing
description: Use when you have a metabolic or biological network encoded as pairwise
  directed interactions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2269
  tools:
  - FNICM
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04131
  title: FNICM
evidence_spans:
- FNICM is a tool to identify core nodes from significantly perturbed subnetwork.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fnicm_cq
    doi: 10.1021/acs.analchem.3c04131
    title: FNICM
  dedup_kept_from: coll_fnicm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04131
  all_source_dois:
  - 10.1021/acs.analchem.3c04131
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# network-topology-edge-parsing

## Summary

Parse a directed edge list from a two-column text file into an adjacency structure to initialize a global metabolic network for FNICM core-node identification. This skill bridges raw edge data into a computable digraph representation.

## When to use

Apply this skill when you have a metabolic or biological network encoded as pairwise directed interactions (e.g., A→B enzyme–substrate relationships, metabolite conversions, or regulatory edges) in plain-text format, and you need to construct an initial global network topology before trust-score propagation and subnetwork analysis.

## When NOT to use

- The input is already a serialized graph object (e.g., adjacency matrix, .gml, .graphml, or NetworkX pickle); skip directly to trust-score input.
- The network is undirected or edge directionality is irrelevant to your analysis; simpler symmetric adjacency parsing may be preferable.
- Your input is a metabolite concentration matrix or feature table rather than a network topology; use dimensionality reduction or correlation-based network inference first.

## Inputs

- digraph edge list file (.txt format, tab- or space-delimited, two columns A and B)

## Outputs

- parsed adjacency structure (adjacency list or matrix representation of directed graph)
- validated node set (all unique nodes extracted from A and B columns)

## How to apply

Load the input .txt file containing exactly two columns (A and B), where each row represents a directed edge from source node A to target node B. Parse each row into an adjacency structure (e.g., adjacency list or matrix) that preserves directionality. Validate that all node identifiers are consistently formatted and non-empty. The resulting adjacency structure serves as the foundation for FNICM's trust-score propagation algorithm, which requires accurate representation of the network's topology to compute node centrality and identify statistically significant perturbations. Ensure no self-loops or duplicate edges are inadvertently introduced during parsing, as these can bias downstream trust ranking.

## Related tools

- **FNICM** (downstream consumer of parsed digraph for trust-score propagation and core-node ranking) — https://github.com/LiQi94/FNICM

## Evaluation signals

- Adjacency structure has |E| entries where E is the number of edge rows, with no duplicate or reversed edges unless intentional.
- All nodes appearing in column B have corresponding entries accessible from the adjacency structure (i.e., no orphaned target nodes).
- Node count equals the unique values in columns A and B combined; validate against expected metabolite or enzyme cardinality.
- Directionality is preserved: edge (A, B) is not equivalent to (B, A) in the adjacency representation.
- No parsing errors (e.g., malformed rows, non-ASCII characters, or misaligned column counts) are logged; file integrity check passes.

## Limitations

- The skill assumes the input file is well-formed; malformed or inconsistent delimiter usage (mixing tabs and spaces) may cause parsing failures.
- Self-loops and duplicate edges are not filtered automatically; manual validation or preprocessing may be required if the source data contains redundancies.
- Large networks (>>10,000 nodes) may require memory-efficient data structures (e.g., sparse adjacency lists); dense matrix representations could exceed RAM.
- The skill does not validate biological plausibility or reconcile conflicting edge definitions (e.g., A→B from one source and B→A from another); domain-specific curation is necessary.
- FNICM is compatible exclusively with the Windows operating system, limiting reproducibility on Linux or macOS systems.

## Evidence

- [readme] you need to input a digraph list file in a .txt format, which contains two columns of data, A and B. There is an edge from column A to column B.: "you need to input a digraph list file in a .txt format, which contains two columns of data, A and B. There is an edge from column A to column B."
- [readme] Note that this is an initial global network, and the subsequent subnetwork is constructed based on this network.: "Note that this is an initial global network, and the subsequent subnetwork is constructed based on this network."
- [other] Load the digraph edge list from the input .txt file (two columns A and B representing directed edges from A to B) and parse into an adjacency structure.: "Load the digraph edge list from the input .txt file (two columns A and B representing directed edges from A to B) and parse into an adjacency structure."
- [other] FNICM requires a digraph list input file in .txt format with two columns (A and B) where each row represents a directed edge from node A to node B, forming the initial global network upon which subsequent subnetwork construction is based.: "FNICM requires a digraph list input file in .txt format with two columns (A and B) where each row represents a directed edge from node A to node B"
