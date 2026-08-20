---
name: spectral-molecular-embedding-alignment
description: Use when you have MS/MS spectra in MGF or similar format and a reference
  library of molecular structures (SMILES or SDF), and your goal is to retrieve the
  most likely structures for an unknown compound spectrum by learning a joint embedding
  space rather than using traditional spectral similarity or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3814
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - rdkit
  - PyTorch
  - PyTorch Geometric
  - matchms
  - Python
  - conda
  - pip
  - Distributed Data Parallel (DDP)
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

# spectral-molecular-embedding-alignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Align MS/MS spectral embeddings and molecular structure embeddings in a shared latent space using contrastive learning, enabling cross-modal retrieval of candidate compounds from a structure library ranked by cosine similarity. This skill is essential when you have paired MS/MS spectra and molecular structures and need to identify unknowns by spectrum-to-structure matching rather than by spectral library matching alone.

## When to use

Apply this skill when you have MS/MS spectra in MGF or similar format and a reference library of molecular structures (SMILES or SDF), and your goal is to retrieve the most likely structures for an unknown compound spectrum by learning a joint embedding space rather than using traditional spectral similarity or mass-based filters alone. Use this when you want to exploit both spectral features and structural graph topology to improve compound identification accuracy across different collision energies or instrument platforms.

## When NOT to use

- Input spectra lack sufficient fragmentation peaks or signal-to-noise ratio; contrastive learning requires informative spectral patterns.
- Reference structure library is very small (<1000 compounds); embedding space generalization benefits from larger, diverse training sets.
- Query spectra are from a fundamentally different ionization method or mass analyzer than the training data (e.g., ESI-trained model applied to MALDI spectra without retraining).

## Inputs

- MS/MS spectra in MGF format with precursor m/z and fragmentation patterns
- Molecular structure library in SMILES or SDF format with associated metadata
- Preprocessed spectrum data (normalized, denoised intensity arrays)
- Training dataset of paired MS/MS spectra and known molecular structures

## Outputs

- Learned embedding weights for spectral and structural encoders (model.pth)
- Ranked retrieval results: candidate SMILES, cosine similarity scores, top-k matches
- Per-spectrum result file with structure predictions and confidence scores (CSV)

## How to apply

Load MS/MS spectrum data (MGF format) and molecular structure datasets (SMILES or SDF) using matchms and rdkit. Preprocess spectra (normalize, remove noise) and convert molecular structures to graph representations using rdkit and PyTorch Geometric. Train a siamese-style contrastive embedding model using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a contrastive loss function (e.g., NT-Xent or triplet loss). Encode both query spectra and reference structures into the learned embedding space. Compute cosine similarity between each query spectrum embedding and all reference structure embeddings, optionally weighting scores across multiple collision energy models if available. Rank candidates by similarity score and output top-k matches with confidence scores for downstream validation.

## Related tools

- **rdkit** (Convert SMILES and SDF molecular structures to graph representations for structural encoder input) — https://rdkit.org/
- **PyTorch** (Define and train the siamese contrastive embedding model with gradient-based optimization) — https://pytorch.org/
- **PyTorch Geometric** (Implement graph neural network layers to encode molecular structures as node/edge embeddings) — https://pytorch-geometric.readthedocs.io/en/latest/
- **matchms** (Load, preprocess, and normalize MS/MS spectrum data from MGF and other spectral formats) — https://matchms.readthedocs.io/en/latest/
- **Distributed Data Parallel (DDP)** (Enable multi-GPU or multi-node parallel training to scale model training on large spectral datasets)

## Examples

```
config_path = "/model/low_energy/checkpoints/config.yaml"
model_path = "/model/low_energy/checkpoints/model.pth"
model_inference = ModelInference(config_path=config_path, pretrain_model_path=model_path, device="cpu")
ms_feature = model_inference.ms2_encode(ms_list[i:i+1])
smiles_feature, _ = get_feature(smiles_lst, model_inference=model_inference, n=1, flag_get_value=True)
indice, score, candidate = get_topK_result(library=smiles_list, ms_feature=ms_feature, smiles_feature=smiles_feature, topK=100)
```

## Evaluation signals

- Cosine similarity scores are well-separated between correct and incorrect candidates (e.g., top-1 match significantly higher than top-2 and below).
- Top-k retrieval accuracy (k=1, 5, 10) on a held-out test set of paired spectra and structures meets or exceeds baseline methods (spectral matching alone).
- Embedding space validation: spectra of the same compound cluster together; structurally similar compounds occupy nearby regions regardless of spectral collision energy.
- Model generalization: performance is consistent across different collision energy levels (low, medium, high) without retraining.
- Output rank stability: repeated queries with identical spectra produce identical ranked results with identical cosine similarity scores.

## Limitations

- Cross-modal embedding alignment is sensitive to training data distribution; models trained on one ionization method or collision energy may not transfer well to substantially different experimental conditions without retraining or fine-tuning.
- Contrastive learning requires large, balanced paired datasets of spectra and structures; small or imbalanced training sets may lead to poor embedding quality and retrieval performance.
- Computational cost scales with reference library size; similarity computation against millions of structures may require approximate nearest-neighbor methods or library indexing for practical deployment.
- The method does not account for isomeric ambiguity; multiple structures with identical molecular formula but different connectivity may receive similar scores, requiring post-hoc mass accuracy or other filters for disambiguation.

## Evidence

- [other] CSU-MS2 implements contrastive spectral-structural unification to enable cross-modal retrieval, unifying MS/MS spectra and molecular structures for compound identification.: "CSU-MS2 implements contrastive spectral-structural unification to enable cross-modal retrieval, unifying MS/MS spectra and molecular structures for compound identification."
- [other] Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric.: "Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric."
- [other] Train contrastive embeddings using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a siamese-style loss function.: "Train contrastive embeddings using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a siamese-style loss function."
- [other] Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings.: "Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings."
- [other] Rank candidates by similarity score and output ranked retrieval results with top-k matches and confidence scores.: "Rank candidates by similarity score and output ranked retrieval results with top-k matches and confidence scores."
- [readme] Multi-gpu or multi-node parallel training can be performed using Distributed Data Parallel (DDP) provided in the code.: "Multi-gpu or multi-node parallel training can be performed using Distributed Data Parallel (DDP) provided in the code."
- [readme] users can load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the final score: "users can load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the"
