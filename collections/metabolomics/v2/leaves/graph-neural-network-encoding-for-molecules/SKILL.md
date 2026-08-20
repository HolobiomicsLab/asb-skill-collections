---
name: graph-neural-network-encoding-for-molecules
description: Use when you have molecular structures (SMILES or SDF format) that need
  to be matched against MS/MS spectra, or you need to compute similarity between query
  spectra and a reference library of compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - rdkit
  - PyTorch
  - PyTorch Geometric
  - matchms
  - Python
  - conda
  - pip
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01594
  title: CSU-MS2
evidence_spans:
- '- [rdkit](https://rdkit.org/)'
- '- [pytorch](https://pytorch.org/)'
- '- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '- [matchms](https://matchms.readthedocs.io/en/latest/)'
- '- [python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_csu_ms2_cq
    doi: 10.1021/acs.analchem.5c01594
    title: CSU-MS2
  dedup_kept_from: coll_csu_ms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01594
  all_source_dois:
  - 10.1021/acs.analchem.5c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-neural-network-encoding-for-molecules

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Encodes molecular structures as learnable vector embeddings using graph neural networks, enabling cross-modal comparison with spectral data for compound identification. This skill transforms SMILES strings or molecular graphs into a unified embedding space where structural similarity is preserved.

## When to use

You have molecular structures (SMILES or SDF format) that need to be matched against MS/MS spectra, or you need to compute similarity between query spectra and a reference library of compounds. The skill is essential when you want to enable cross-modal retrieval—matching spectral features to structural features in a learned shared embedding space.

## When NOT to use

- Input structures are already pre-encoded into embeddings; no GNN encoding needed
- You only need to identify structural properties (e.g., functional groups, molecular weight) without cross-modal matching to spectra
- Your reference library contains only chemical formula or mass; structure-to-spectrum matching requires full molecular graphs

## Inputs

- SMILES strings or SDF format molecular structure files
- Molecular graph representations (atom and bond features from rdkit)
- Reference molecular structure library with associated metadata
- Pre-trained or jointly-trained contrastive embedding model

## Outputs

- Fixed-dimensional molecular structure embeddings (vectors in shared embedding space)
- Ranked retrieval results with cosine similarity scores for top-k candidates
- Compound identifications with confidence scores

## How to apply

Convert molecular structures to graph representations using rdkit and PyTorch Geometric, capturing atoms, bonds, and connectivity as node and edge features. Train a graph neural network encoder jointly with a spectral encoder using contrastive learning (Siamese-style loss) to align structural and spectral embeddings in a shared feature space. During inference, encode candidate molecular structures through the trained GNN to obtain fixed-dimensional embeddings. Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings, then rank candidates by similarity score to retrieve top-k matches with confidence scores.

## Related tools

- **rdkit** (Converts SMILES and SDF molecular structures to graph representations with atom, bond, and connectivity features) — https://rdkit.org/
- **PyTorch Geometric** (Implements graph neural network layers for encoding molecular graphs into fixed-dimensional embeddings) — https://pytorch-geometric.readthedocs.io/en/latest/
- **PyTorch** (Provides the contrastive learning framework and Siamese-style loss function for jointly training spectral and structural encoders) — https://pytorch.org/
- **matchms** (Loads and preprocesses MS/MS spectrum data for paired training with molecular structures) — https://matchms.readthedocs.io/en/latest/

## Examples

```
from CSU_MS2 import ModelInference; model = ModelInference(config_path='/model/low_energy/checkpoints/config.yaml', pretrain_model_path='/model/low_energy/checkpoints/model.pth', device='cpu'); smiles_feature = model.molecule_encode(['CC(C)Cc1ccc(cc1)C(C)C(=O)O']); similarity_scores = (ms_feature @ smiles_feature.T).numpy()
```

## Evaluation signals

- Encoded embeddings have consistent dimensionality across all molecules and are real-valued vectors in the shared embedding space
- Cosine similarity scores between spectrally similar compounds and their correct molecular structures are significantly higher than random structure pairs
- Top-k retrieval results include the true compound identity within the top-k ranked candidates for held-out test spectra
- Embedding space exhibits clear clustering by molecular similarity or chemical family (visual inspection via t-SNE or UMAP)
- Cross-modal retrieval rank metrics (Mean Reciprocal Rank, Recall@k) are consistent with the training/validation loss trends

## Limitations

- Performance depends on quality and diversity of the structure-spectrum training dataset; limited or biased training data will degrade cross-modal alignment
- GNN encoding is sensitive to graph representation choices (atom features, bond types); different featurizations may affect retrieval accuracy
- Computational cost scales with library size during inference; exhaustive similarity computation against large reference libraries may be slow without approximate nearest-neighbor indexing
- Method assumes SMILES or SDF formats are correctly parsed; malformed structures will cause encoding failures or degraded embeddings

## Evidence

- [other] Convert molecular structures to graph representations using rdkit and PyTorch Geometric: "convert molecular structures to graph representations using rdkit and PyTorch Geometric"
- [other] Train contrastive embeddings using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a siamese-style loss function: "Train contrastive embeddings using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a siamese-style loss function"
- [other] Encode query spectra and candidate molecular structures into the learned embedding space: "Encode query spectra and candidate molecular structures into the learned embedding space"
- [other] Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings: "Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings"
- [other] Rank candidates by similarity score and output ranked retrieval results with top-k matches and confidence scores: "Rank candidates by similarity score and output ranked retrieval results with top-k matches and confidence scores"
- [readme] Load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the final score: "load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores"
