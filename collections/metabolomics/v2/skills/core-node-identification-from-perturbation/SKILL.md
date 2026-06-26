---
name: core-node-identification-from-perturbation
description: Use when you have a directed metabolic network (digraph) with node perturbation
  data (e.g., from metabolomics fold-changes or experimental treatment effects) and
  you need to identify which nodes are core drivers of the observed perturbation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
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

# core-node-identification-from-perturbation

## Summary

Identify core metabolites or nodes from a significantly perturbed metabolic network by propagating trust scores through a directed graph and applying controllability analysis. This skill is used when you have a global metabolic network, baseline node perturbation or confidence values, and need to rank and extract the most influential nodes driving observed metabolic changes.

## When to use

Apply this skill when you have a directed metabolic network (digraph) with node perturbation data (e.g., from metabolomics fold-changes or experimental treatment effects) and you need to identify which nodes are core drivers of the observed perturbation. The workflow is most appropriate when you wish to construct a subnetwork centered on significantly perturbed nodes and rank them by their propagated influence scores rather than raw perturbation alone.

## When NOT to use

- Input digraph is already filtered to a subnetwork; FNICM requires the full global network to propagate scores meaningfully.
- All nodes have equal initial trust scores (undifferentiated perturbation); FNICM requires seed nodes or prior perturbation signal to rank meaningfully.
- Operating system is not Windows; FNICM (executable version) is compatible exclusively with Windows.

## Inputs

- Digraph edge list (.txt file with two columns A and B, one directed edge per row)
- Initial trust scores file (nodes with confidence or perturbation values between 0 and 1)

## Outputs

- TrustRank_scores (ranked node list with propagated trust scores in descending order)
- Subnetwork_digraph (edge list of the constructed subnetwork)
- Subnetwork_nodes (identifier list of all nodes in the subnetwork)
- Core_nodes (ranked list of core nodes identified via controllability analysis)

## How to apply

Load a digraph edge list (two-column .txt file with directed edges from node A to node B forming the initial global network) and an initial trust score file (seed nodes set to 1.0, others to 0.0, with scores between 0 and 1 representing baseline confidence or perturbation magnitude). Execute the FNICM algorithm to propagate trust scores through the directed network, identifying nodes with statistically significant perturbation. Specify the number of top-ranked nodes to extract based on domain knowledge and the desired subnetwork size. The algorithm ranks nodes by their FNICM scores (derived from score propagation and controllability metrics) and outputs four files: TrustRank scores (all nodes ranked), the constructed subnetwork digraph, subnetwork node list, and core nodes list. Judge success by verifying that core nodes have high FNICM scores, are reachable from seed nodes in the digraph, and form a coherent subnetwork of biologically relevant size.

## Related tools

- **FNICM** (Executable tool that implements trust score propagation through the digraph and controllability analysis to identify core nodes from significantly perturbed subnetworks) — https://github.com/LiQi94/FNICM

## Evaluation signals

- Core nodes have FNICM scores substantially higher than non-core nodes in the ranked output.
- Subnetwork size (number of nodes and edges) is proportional to the specified top-rank parameter and reflects biological relevance.
- All core nodes are reachable from seed nodes following directed edges in the input digraph.
- Output file schemas match expected format: tab-separated node IDs and scores for TrustRank and Core_nodes files; edge lists in A–B format for digraph files.
- Core nodes show enrichment for known metabolic hub or regulatory roles when validated against external pathway databases.

## Limitations

- FNICM is compatible exclusively with the Windows operating system; no Linux or macOS version is provided.
- The software does not include a changelog, limiting transparency on version history and bug fixes.
- Quality of core node identification is sensitive to seed node selection and initial trust score assignment; poor seed selection may yield biologically irrelevant results.
- The algorithm requires manual specification of the number of top-ranked nodes to extract; no automatic cutoff or statistical threshold is provided to guide this choice.
- Scalability to very large networks or highly complex digraphs with dense connectivity is not discussed in the article or README.

## Evidence

- [intro] FNICM identifies core nodes from significantly perturbed subnetworks: "FNICM is a tool to identify core nodes from significantly perturbed subnetwork."
- [readme] Digraph input format is two columns A and B representing directed edges: "you need to input a digraph list file in a .txt format, which contains two columns of data, A and B. There is an edge from column A to column B."
- [readme] Initial trust scores are assigned to seed and non-seed nodes between 0 and 1: "you need to set the initial trust scores of all nodes in the above digraph. Firstly, you need to select some nodes as seed nodes. Then according to your purpose of research, the initial scores can"
- [readme] Four output files are generated: TrustRank scores, Subnetwork digraph, Subnetwork nodes, and Core nodes: "After the program finishes, you can obtain the following four files. These files are stored in the folder named Output_results within the directory where the software is saved. (1) TrustRank_scores:"
- [readme] Windows-only compatibility: "Compatible exclusively with the Windows operating system"
