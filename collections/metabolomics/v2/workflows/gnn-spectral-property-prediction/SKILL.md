---
name: gnn-spectral-property-prediction-workflow
description: 'Use when you want to train or apply a graph neural network over molecular
  graphs to predict a structure-dependent property — retention time, collision cross
  section (CCS), or an MS2 spectrum — and use that predicted property to filter or
  re-rank candidate structures for untargeted metabolomics annotation: build RDKit/PyTorch-Geometric
  molecular graphs from SMILES, design and train a GNN against a labelled property
  dataset, run inference to predict the property for candidate structures, and rescore
  a candidate pool by comparing predicted vs observed property values.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  - ion-mobility-MS
  stage_count: 5
  member_skills:
  - molecular-graph-construction-from-smiles
  - molecular-graph-construction-pytorch-geometric
  - feature-encoding-atoms-bonds
  - molecular-structure-parsing-rdkit
  - pytorch-graph-serialization
  - graph-neural-network-architecture-assembly
  - graph-neural-network-architecture-design
  - gnn-architecture-design-for-molecular-graphs
  - graph-neural-network-implementation
  - graph-neural-network-architecture-implementation
  - graph-neural-network-model-training
  - pytorch-model-checkpoint-management
  - pytorch-model-training-and-optimization
  - retention-time-prediction-validation
  - gnn-model-inference-and-prediction
  - graph-neural-network-model-inference
  - neural-network-inference-execution
  - molecular-property-prediction-feature-construction
  - metabolite-annotation-by-chromatographic-behavior
  - candidate-ranking-by-score
  - metabolite-candidate-ranking
  - candidate-structure-ranking
  - ranked-annotation-prioritization
  - metabolite-annotation-ensemble-ranking
  member_tools:
  - manual expert review
  - RDKit
  - PyTorch
  - Graphormer
  - DGL
  - Python
  - PyG
  - NumPy
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - PyG (PyTorch Geometric)
  - TorchMetrics
  - torch-scatter, torch-sparse, torch-cluster
  - PyTorch Geometric
  - Retip
  - Retip (R package)
  - pyRetip (Python package)
  - Retip app
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# GNN Molecular Property Prediction for Annotation Rescoring (RDKit graph -> PyTorch GNN -> candidate re-ranking)

## Summary

SMILES + labelled property dataset in, a property-rescored candidate table out: RDKit/PyG molecular graph construction, GNN architecture design and supervised training, trained-model inference on candidate structures, and predicted-vs-observed candidate re-ranking.


## When to use

Use when you want to train or apply a graph neural network over molecular graphs to predict a structure-dependent property — retention time, collision cross section (CCS), or an MS2 spectrum — and use that predicted property to filter or re-rank candidate structures for untargeted metabolomics annotation: build RDKit/PyTorch-Geometric molecular graphs from SMILES, design and train a GNN against a labelled property dataset, run inference to predict the property for candidate structures, and rescore a candidate pool by comparing predicted vs observed property values.


## When NOT to use

- The data is not LC-MS, ion-mobility-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — featurize

**Goal:** SMILES structures -> attributed molecular graphs (RDKit + PyTorch Geometric)

**EDAM operation:** operation_0292

**Inputs:** tsv · **Outputs:** pyg-graph-dataset

**Candidate leaf skills:** `molecular-graph-construction-from-smiles` (primary), `molecular-graph-construction-pytorch-geometric`, `feature-encoding-atoms-bonds`, `molecular-structure-parsing-rdkit`, `pytorch-graph-serialization`

**Tools (primary):** manual expert review, RDKit, PyTorch

**Other candidate tools:** torch_geometric, torch, Python, rdkit-pypi, RT-Transformer, Python pickle module, HDF5 (h5py)

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.0c04071, 10.1038/s41467-019-13680-7, 10.1093/bioinformatics/btae084, 10.1186/s13321-024-00899-w

### Stage 2 — architect

**Goal:** molecular graph representation -> GNN architecture (message-passing layers + property head)

**EDAM operation:** operation_0337

**Inputs:** pyg-graph-dataset · **Outputs:** model-architecture

**Candidate leaf skills:** `graph-neural-network-architecture-assembly` (primary), `graph-neural-network-architecture-design`, `gnn-architecture-design-for-molecular-graphs`, `graph-neural-network-implementation`, `graph-neural-network-architecture-implementation`

**Tools (primary):** Graphormer, DGL, RDKit, PyTorch

**Other candidate tools:** Python, torch, torch-scatter, torch-sparse, torch-cluster, torch_geometric, PyTorch (torch), RDKit (rdkit-pypi), torch-scatter, torch-sparse, torch-cluster, scanpy, STAGATE, pandas, h5py, GNN-RT (repository), Python 3, PyG, NumPy, conda, pip, PyTorch Geometric (PyG), NumPy and pandas

**Grounding:** 8 KB(s); DOIs: 10.1002/cem.70040, 10.1021/acs.analchem.0c04071, 10.1021/acs.analchem.3c03177, 10.1021/acs.analchem.4c05859 …

### Stage 3 — train

**Goal:** GNN architecture + labelled property dataset -> trained model checkpoint

**EDAM operation:** operation_3445

**Inputs:** model-architecture, pyg-graph-dataset · **Outputs:** model-checkpoint

**Candidate leaf skills:** `graph-neural-network-model-training` (primary), `pytorch-model-checkpoint-management`, `pytorch-model-training-and-optimization`, `retention-time-prediction-validation`

**Tools (primary):** Python, PyG, RDKit, NumPy, Pandas, torch-scatter, torch-sparse, torch-cluster, PyTorch, PyG (PyTorch Geometric), TorchMetrics, torch-scatter, torch-sparse, torch-cluster

**Other candidate tools:** Anaconda

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.0c04071, 10.1021/acs.jcim.4c02179

### Stage 4 — predict

**Goal:** trained GNN + candidate structures -> predicted property values

**EDAM operation:** operation_3659

**Inputs:** model-checkpoint, tsv · **Outputs:** tsv

**Candidate leaf skills:** `gnn-model-inference-and-prediction` (primary), `graph-neural-network-model-inference`, `neural-network-inference-execution`, `molecular-property-prediction-feature-construction`

**Tools (primary):** PyTorch Geometric

**Other candidate tools:** PyTorch or TensorFlow, PyTorch, TensorFlow, RDKit, ms-pred, ICEBERG WebUI, ICEBERG model, ms-pred repository, PubChem, chemprop, chemprop-IR

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.3c04654, 10.1021/acs.jcim.1c00055, 10.1186/s13321-024-00899-w

### Stage 5 — rescore

**Goal:** predicted property + experimental evidence -> re-ranked / filtered annotation candidates

**EDAM operation:** operation_3800

**Inputs:** tsv, feature-table · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-annotation-by-chromatographic-behavior` (primary), `candidate-ranking-by-score`, `metabolite-candidate-ranking`, `candidate-structure-ranking`, `ranked-annotation-prioritization`, `metabolite-annotation-ensemble-ranking`

**Tools (primary):** Retip, Retip (R package), pyRetip (Python package), Retip app

**Other candidate tools:** Python 3.11.7, MVP (MultiView Projection), PyTorch Geometric, DGL (Deep Graph Library), RDKit, Streamlit, MassSpecGym, pip, CUDA, PyTorch, CUDA 11.8, Python, pyrwr, MetFrag, ChemWalker, DiffSpectra, Diffusion Molecule Transformer (DMT), SpecFormer, mWISE, R, FELLA, igraph, MLP (Multi-Layer Perceptron) baseline model, GNN (Graph Neural Network) baseline model, LDA (Latent Dirichlet Allocation), PyTorch & DGL

**Grounding:** 7 KB(s); DOIs: 10.1021/acs.analchem.1c00238, 10.1021/acs.analchem.9b05765, 10.1093/bioinformatics/btad078/7067745, 10.1093/bioinformatics/btae490 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
