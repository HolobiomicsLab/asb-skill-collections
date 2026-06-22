---
name: metabolite-ranking-by-network-centrality
description: Use when when you have a directed metabolic network (digraph) and want to identify which metabolites are most central to observed perturbations; specifically when you have (1) a global network as an edge list, (2) seed nodes with known or hypothesized perturbation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_2259
  tools:
  - FNICM
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-ranking-by-network-centrality

## Summary

Rank metabolites (nodes) in a directed metabolic network by their centrality scores computed via trust score propagation, identifying core metabolites that are significantly perturbed in a disease or treatment state. This skill applies network-level perturbation analysis to isolate functionally important nodes from a global metabolic digraph.

## When to use

When you have a directed metabolic network (digraph) and want to identify which metabolites are most central to observed perturbations; specifically when you have (1) a global network as an edge list, (2) seed nodes with known or hypothesized perturbation (e.g., significantly changed metabolites), and (3) a goal to rank all nodes by their proximity to and influence on these perturbations rather than by abundance or statistical significance alone.

## When NOT to use

- Input is an undirected or unweighted network where edge directionality and flow asymmetry are not meaningful.
- Seed node set is unknown or poorly justified; FNICM ranking is sensitive to seed selection, and arbitrary seeds will produce misleading core node lists.
- You require node ranking based on statistical abundance or univariate significance; FNICM ranks by network topology and perturbation proximity, not by fold-change or p-value.

## Inputs

- Directed metabolic network as .txt digraph edge list (two columns: source node, target node)
- Initial trust score file (.txt format) assigning scalar scores (0–1) to each node, with seed nodes typically set to 1.0

## Outputs

- Ranked node list with FNICM scores in descending order (tab-separated .txt file)
- Constructed subnetwork digraph (edge list of retained nodes and edges)
- Subnetwork node list (all nodes in the filtered subnetwork)
- Core nodes list (top-ranked nodes identified via controllability analysis)

## How to apply

Load the directed metabolic network as a two-column edge list (.txt format, columns A and B representing directed edges from A to B), then create an initial trust score file assigning 1.0 to seed nodes (typically significantly perturbed metabolites) and 0 to all others. Execute the FNICM algorithm to propagate trust scores iteratively through the digraph, computing a centrality-like score for each node based on its path distance and connectivity to high-scoring neighbors. Rank all nodes by their final FNICM scores in descending order. Select the top k nodes (where k is set based on downstream validation capacity or domain knowledge of subnetwork size) as core metabolites. The rationale is that nodes with high propagated scores are both topologically close to perturbed metabolites and occupy bottleneck positions in the network, making them functionally central.

## Related tools

- **FNICM** (Core executable for trust score propagation, subnetwork construction, and core node identification via controllability analysis) — https://github.com/LiQi94/FNICM

## Evaluation signals

- Verify that all input nodes appear in the initial trust score file and that seed nodes have scores of 1.0 (or other justified high value) while non-seeds are 0.0.
- Check that output ranked node list is strictly sorted in descending order by FNICM score and contains no missing or duplicate node IDs.
- Confirm that the top-ranked nodes correspond to known or validated core metabolites from independent experiments (e.g., mass-spec validation, pathway databases, or literature).
- Validate that the subnetwork digraph contains only edges and nodes present in the original input network (no false positives introduced during construction).
- Assess that the subnetwork size and core node count are consistent with the specified top-k parameter and the propagation dynamics of the network topology.

## Limitations

- FNICM is compatible exclusively with the Windows operating system, limiting accessibility on Linux, macOS, or cloud environments.
- Ranking is highly sensitive to seed node selection; misidentified or incomplete seed sets will produce unreliable core node lists.
- Algorithm performance and interpretation depend critically on network quality; sparse or incomplete metabolic networks may not capture real biological relationships, leading to spurious rankings.
- No formal statistical significance testing is provided for FNICM scores; practitioners must validate rankings against independent measurements or biological knowledge.
- The choice of top-k parameter (number of core nodes to extract) is not data-driven; it relies on domain knowledge and is closely related to subnetwork size, which must be calibrated per study.

## Evidence

- [readme] Input file format and structure for digraph edge list: "Here you need to input a digraph list file in a .txt format, which contains two columns of data, A and B. There is an edge from column A to column B."
- [readme] Trust score initialization and seed node specification: "Firstly, you need to select some nodes as seed nodes. Then according to your purpose of research, the initial scores can take a value between 0 and 1. Generally, the scores of seed nodes are set to"
- [readme] FNICM algorithm identifies core nodes from perturbed subnetworks: "FNICM is a tool to identify core nodes from significantly perturbed subnetwork."
- [readme] Output files including ranked node scores and core nodes: "(1) TrustRank_scores: the list of the nodes in descending order with their scores. (4) Core_nodes: the list of core nodes identified from the above subnetwork using controllability analysis."
- [readme] Windows operating system requirement: "Compatible exclusively with the Windows operating system"
- [readme] Initial global network foundation for subnetwork construction: "Note that this is an initial global network, and the subsequent subnetwork is constructed based on this network."
