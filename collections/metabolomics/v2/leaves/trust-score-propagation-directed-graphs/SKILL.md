---
name: trust-score-propagation-directed-graphs
description: Use when you have (1) a directed edge list representing a global network
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2258
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

# trust-score-propagation-directed-graphs

## Summary

Propagate initial trust scores (typically 0–1 confidence values) through a directed graph to compute node-level perturbation significance. This skill identifies nodes with statistically significant network propagation, enabling prioritization of core nodes in metabolic subnetwork analysis.

## When to use

Apply this skill when you have (1) a directed edge list representing a global network (e.g., metabolic reaction graph, protein–protein interaction network), (2) a set of seed nodes with known or hypothesized importance (assigned trust score 1) and background nodes (assigned trust score 0), and (3) a need to rank all nodes by their propagated influence or perturbation signal. This is particularly valuable when you want to identify which non-seed nodes are most affected by or connected to your seed set.

## When NOT to use

- Input digraph is undirected or contains no seed nodes — FNICM is designed specifically for directed networks with well-defined seed sets.
- Trust scores are already pre-computed or finalized — this skill performs the propagation step itself and is not a post-hoc scoring method.
- Operating system is not Windows — FNICM executable is exclusively compatible with Windows.

## Inputs

- Digraph edge list (.txt file, two columns: node_A, node_B representing directed edges)
- Initial trust score file (mapping each node to a trust score between 0 and 1, typically 1 for seed nodes, 0 for others)

## Outputs

- TrustRank_scores file (ranked list of all nodes in descending order with their propagated trust scores)
- Ranked core node list with FNICM scores

## How to apply

Load the digraph edge list (.txt format, two columns A and B representing directed edges) and the initial trust score file (assigning seed nodes score 1.0 and background nodes score 0.0, or domain-specific scores between 0 and 1). Execute the FNICM algorithm to propagate trust scores iteratively through the directed network, computing cumulative influence at each node. The algorithm ranks nodes by their final propagated scores; nodes with higher scores indicate stronger perturbation or connectivity to seed nodes. Extract the ranked node list with FNICM scores and use domain knowledge to set a threshold on the number of top-ranked nodes to retain for downstream subnetwork construction and controllability analysis.

## Related tools

- **FNICM** (Core tool that implements trust score propagation through the directed graph and ranks nodes by perturbation significance) — https://github.com/LiQi94/FNICM

## Evaluation signals

- Output TrustRank_scores file contains all nodes from the input digraph ranked in descending order with scores between 0 and 1.
- Seed nodes have trust scores equal to or near 1.0; non-seed nodes have scores ≤ seed scores (monotonicity check).
- Nodes directly connected to high-scoring seed nodes have elevated scores; path distance correlates with score decay.
- The sum or distribution of propagated scores reflects expected network connectivity (e.g., hub nodes or densely connected regions show higher aggregation).
- Output file formats match expected tab-separated structure with node identifiers and numeric scores, with no missing or malformed entries.

## Limitations

- FNICM is exclusively compatible with the Windows operating system; no Linux or macOS support is documented.
- The choice of seed nodes and initial trust score assignments is user-dependent and directly influences downstream results; inappropriate seed selection may yield spurious rankings.
- The algorithm's convergence and threshold sensitivity depend on network topology; small networks or disconnected components may show instability in score propagation.
- No changelog is available, limiting visibility into algorithmic changes or bug fixes across versions.

## Evidence

- [intro] FNICM requires a digraph list input file in .txt format with two columns (A and B) where each row represents a directed edge: "you need to input a digraph list file in a .txt format, which contains two columns of data, A and B. There is an edge from column A to column B."
- [readme] Initial trust scores are assigned per node, typically 1 for seed nodes and 0 for background nodes: "you need to set the initial trust scores of all nodes in the above digraph. Firstly, you need to select some nodes as seed nodes. Then according to your purpose of research, the initial scores can"
- [readme] The FNICM algorithm propagates trust scores and produces a ranked list of nodes with their scores: "TrustRank_scores: the list of the nodes in descending order with their scores."
- [readme] FNICM is exclusively Windows-compatible: "Compatible exclusively with the Windows operating system"
- [intro] The skill identifies core nodes from significantly perturbed subnetworks via trust score propagation: "FNICM is a tool to identify core nodes from significantly perturbed subnetwork."
