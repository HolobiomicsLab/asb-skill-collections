---
name: graph-based-identity-transfer
description: Use when when you have spectral library matches (seed identities with high confidence scores) mapped to initial candidate structures from in silico fragmentation, and you want to propagate those identities to related structures in the fragmentation candidate graph to improve annotation coverage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pyrwr
  - MetFrag
  - ChemWalker
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btad078/7067745
  title: ChemWalker
evidence_spans:
- ChemWalker is a python package
- using [random walk](https://github.com/jinhongjung/pyrwr)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemwalker_cq
    doi: 10.1093/bioinformatics/btad078/7067745
    title: ChemWalker
  dedup_kept_from: coll_chemwalker_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad078/7067745
  all_source_dois:
  - 10.1093/bioinformatics/btad078/7067745
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-based-identity-transfer

## Summary

Propagate confident spectral library match identities to structurally related candidate molecules through random walk algorithms on a fragmentation graph, improving annotation coverage in untargeted metabolomics. This skill transfers high-confidence identities from known spectral matches to in silico-generated structural candidates that share fragmentation relationships.

## When to use

When you have spectral library matches (seed identities with high confidence scores) mapped to initial candidate structures from in silico fragmentation, and you want to propagate those identities to related structures in the fragmentation candidate graph to improve annotation coverage. Typical scenario: untargeted LC-MS metabolomics where MetFrag generates thousands of candidate structures but only a subset have direct spectral library matches; you use identity transfer to rank and annotate remaining candidates based on their structural proximity to matched seeds.

## When NOT to use

- Input candidates are not connected by fragmentation relationships (no meaningful edge structure in the graph); RWR requires a connected or near-connected network to propagate signals effectively.
- Spectral library matches are already exhaustive for your compound set; identity transfer is most valuable when direct spectral matches are sparse relative to generated candidates.
- Seed identities have very low confidence or are known to be unreliable; RWR will amplify and spread incorrect annotations through the graph.

## Inputs

- candidate structure graph (nodes=structures, edges=fragmentation relationships from in silico fragmentation)
- spectral library match seed identities with confidence scores mapped to initial structures
- graph representation (edge list format: tab-separated source, target, optional weight)

## Outputs

- ranked candidate structures sorted by propagated identity scores
- RWR score vector (node-to-score mapping for all structures in the graph)
- annotated candidate structures with transferred identity labels and propagation confidence

## How to apply

Represent candidate structures from in silico fragmentation as a directed graph where nodes are structures and edges encode fragmentation relationships (parent-daughter fragments). Map spectral library match identities as seed node labels with associated confidence scores. Initialize a random walk with restart (RWR) engine using pyrwr, setting the restart probability (c parameter, typically 0.15) to balance exploration of distant candidates against return to high-confidence seeds. Execute RWR from each seed node to compute a personalized ranking vector over all candidate structures. The RWR score for each node represents the probability of reaching it from the seed via fragmentation paths, weighted by edge traversal costs. Collect propagated identity scores for all candidates, rank them, and filter by a score threshold (e.g., retain candidates with RWR score above percentile cutoff) to produce a ranked annotation list. The rationale is that structures close to spectral-matched seeds in fragmentation space are more likely to share the same identity.

## Related tools

- **pyrwr** (Executes random walk with restart (RWR) computation to propagate identity scores from seed nodes through the fragmentation candidate graph; supports single-seed RWR, Personalized PageRank (PPR) for multi-seed, and GPU acceleration.) — https://github.com/jinhongjung/pyrwr
- **MetFrag** (Generates in silico fragmentation candidates and candidate structure graph (edge relationships) that serve as input to the RWR graph; ChemWalker is tested on MetFrag 2.3-CL.) — https://ipb-halle.github.io/MetFrag/projects/metfragcl/
- **ChemWalker** (End-to-end implementation integrating MetFrag fragmentation output and pyrwr RWR engine specifically for spectral library identity propagation in molecular networks.) — https://github.com/computational-chemical-biology/ChemWalker

## Examples

```
from pyrwr.rwr import RWR; rwr = RWR(); rwr.read_graph('fragmentation_graph.tsv', 'directed'); r = rwr.compute(seed=101, c=0.15, epsilon=1e-9, max_iters=100)
```

## Evaluation signals

- Propagated RWR scores are highest for candidate structures that are topologically closest (fewest fragmentation hops) to seed nodes; RWR score should decay monotonically with graph distance from seed.
- Structures annotated by identity transfer share expected fragmentation patterns (fragment mass or neutral loss) with their seed identity's known spectrum; validate by re-checking against reference spectra.
- Seed nodes retain RWR scores near 1.0 (or maximal value); score mass is conserved across the graph (sum of all scores ≈ constant) indicating correct probability flow.
- Comparison of annotated structures pre- and post-identity-transfer shows increased coverage of candidate structures with assigned identities, without artificially high-scoring spurious matches.
- Parameter sensitivity: rerunning with different restart probabilities (c ∈ [0.05, 0.3]) yields qualitatively similar ranking order for top candidates, indicating robust transfer independent of hyperparameter tuning.

## Limitations

- RWR effectiveness depends on fragmentation graph connectivity; disconnected or sparse subgraphs may fail to propagate identities effectively, and deadend nodes (structures with no outgoing edges) can lose probability mass unless handled explicitly (pyrwr offers a `handles-deadend` flag).
- Identity transfer can amplify errors in spectral library matches or in silico fragmentation; a single incorrect seed annotation can spread to many candidates. Seed confidence thresholding is critical.
- RWR assumes undirected or directed fragmentation relationships; if fragmentation direction (parent→fragment vs. fragment→parent) is not correctly encoded in edges, propagation direction and scores will be misaligned.
- Computational cost scales with graph size and number of seeds; large metabolomics candidate sets (>10⁴ structures) may require GPU acceleration or batching to remain tractable.
- No changelog or discussion section in ChemWalker documentation to identify known bugs, performance bottlenecks, or validated parameter ranges for different metabolite classes.

## Evidence

- [readme] ChemWalker is a python package to propagate spectral library match identities through candidate structures provided by in silico fragmentation, using random walk: "ChemWalker is a python package to propagate spectral library match identities through candidate structures provided by _in silico_ fragmentation, using [random walk]"
- [other] Load candidate structures from in silico fragmentation as a graph representation (nodes=structures, edges=fragmentation relationships). Load spectral library matches as seed identities mapped to initial structures. Initialize a random walk engine using pyrwr with the candidate structure graph. Execute random walk propagation starting from seed nodes (spectral matches) to propagate identity scores through the graph.: "1. Load candidate structures from in silico fragmentation as a graph representation (nodes=structures, edges=fragmentation relationships). 2. Load spectral library matches as seed identities mapped"
- [readme] Random Walk with Restart (RWR) is one of famous link analysis algorithms, which measures node-to-node proximities in arbitrary types of graphs (networks).: "Random Walk with Restart (RWR) is one of famous link analysis algorithms, which measures node-to-node proximities in arbitrary types of graphs (networks)."
- [readme] pyrwr aims to implement algorithms for computing RWR scores based on Power Iteration using numpy and scipy in Python. More specifically, pyrwr focuses on computing a single source RWR score vector w.r.t. a given query (seed) node, which is used for a personalized node ranking w.r.t. the querying node.: "pyrwr focuses on computing a single source RWR score vector w.r.t. a given query (seed) node, which is used for a personalized node ranking w.r.t. the querying node."
- [readme] r is a column vector (ndarray) having the RWR score vector w.r.t. seed node. The shape of r will be (n, 1) where n is the number of nodes.: "r is a column vector (ndarray) having the RWR score vector w.r.t. seed node. The shape of r will be (n, 1) where n is the number of nodes."
- [readme] If there are redundant edges in an weighted network, their weights will be summed: "If there are redundant edges in an weighted network, their weights will be summed, e.g., 1   2   8"
