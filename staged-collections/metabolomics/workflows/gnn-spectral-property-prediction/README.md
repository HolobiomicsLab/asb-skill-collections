# gnn-spectral-property-prediction-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **featurize** — SMILES structures -> attributed molecular graphs (RDKit + PyTorch Geometric)  →  `molecular-graph-construction-from-smiles`, `molecular-graph-construction-pytorch-geometric`, `feature-encoding-atoms-bonds`, `molecular-structure-parsing-rdkit`, `pytorch-graph-serialization`
2. **architect** — molecular graph representation -> GNN architecture (message-passing layers + property head)  →  `graph-neural-network-architecture-assembly`, `graph-neural-network-architecture-design`, `gnn-architecture-design-for-molecular-graphs`, `graph-neural-network-implementation`, `graph-neural-network-architecture-implementation`
3. **train** — GNN architecture + labelled property dataset -> trained model checkpoint  →  `graph-neural-network-model-training`, `pytorch-model-checkpoint-management`, `pytorch-model-training-and-optimization`, `retention-time-prediction-validation`
4. **predict** — trained GNN + candidate structures -> predicted property values  →  `gnn-model-inference-and-prediction`, `graph-neural-network-model-inference`, `neural-network-inference-execution`, `molecular-property-prediction-feature-construction`
5. **rescore** — predicted property + experimental evidence -> re-ranked / filtered annotation candidates  →  `metabolite-annotation-by-chromatographic-behavior`, `candidate-ranking-by-score`, `metabolite-candidate-ranking`, `candidate-structure-ranking`, `ranked-annotation-prioritization`, `metabolite-annotation-ensemble-ranking`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
