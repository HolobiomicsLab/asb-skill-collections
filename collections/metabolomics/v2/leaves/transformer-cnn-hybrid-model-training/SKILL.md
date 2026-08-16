---
name: transformer-cnn-hybrid-model-training
description: Use when you have preprocessed 1H NMR spectral data with compound labels
  and need to identify multiple compounds in a flavor mixture where both local spectral
  patterns (handled by CNN) and long-range spectral dependencies (handled by Transformer)
  are diagnostic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Anaconda
  - PyTorch
  - FlavorFormer
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1016/j.microc.2025.115372
  title: FlavorFormer
evidence_spans:
- Python 3.13.2 and Pytorch (version 2.7.0+cu118)
- Install [Anaconda](https://www.anaconda.com/).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flavorformer_cq
    doi: 10.1016/j.microc.2025.115372
    title: FlavorFormer
  dedup_kept_from: coll_flavorformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2025.115372
  all_source_dois:
  - 10.1016/j.microc.2025.115372
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Transformer-CNN Hybrid Model Training

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Train a hybrid CNN-Transformer architecture to extract both local spectral features and global dependencies from 1H NMR data for compound identification. This skill combines separate bi-encoder and cross-encoder branches with fusion pooling and weighted loss to achieve accurate mixture component identification.

## When to use

Apply this skill when you have preprocessed 1H NMR spectral data with compound labels and need to identify multiple compounds in a flavor mixture where both local spectral patterns (handled by CNN) and long-range spectral dependencies (handled by Transformer) are diagnostic. Use it specifically when simple feature matching fails and you need joint spectrum-compound pair refinement via cross-encoder scoring.

## When NOT to use

- Input spectra are already pre-extracted as engineered features or hand-crafted descriptors (model requires raw or minimally processed spectral data to benefit from CNN-Transformer feature learning).
- Compounds in the mixture are well-separated in chemical shift space with minimal overlap (simpler methods like threshold-based peak matching or single-encoder architectures may suffice).
- Computational resources are severely constrained; hybrid CNN-Transformer models are more expensive than shallow classifiers or simple MLPs.

## Inputs

- Preprocessed 1H NMR spectral data (numeric arrays)
- Compound reference labels or embeddings
- Training dataset with spectrum-compound pair annotations
- Held-out test set spectra

## Outputs

- Trained hybrid CNN-Transformer model checkpoint
- Compound identification accuracy metrics
- Ranking metrics (e.g., MRR, NDCG)
- Performance report with validation results

## How to apply

Initialize a hybrid backbone combining CNN layers for local feature extraction and Transformer blocks for global dependency modeling on 1H NMR inputs. Build a bi-encoder branch that independently encodes spectra and compound reference embeddings, applying fusion pooling to merge CNN and Transformer outputs into a unified representation. In parallel, construct a cross-encoder branch that jointly processes spectrum-compound pairs to refine relevance scores. Combine logits from both branches using a weighted loss function that balances bi-encoder and cross-encoder contributions. Train end-to-end with backpropagation on the training dataset, then validate on held-out test spectra by computing compound identification accuracy and ranking metrics. Save the trained checkpoint and performance report for downstream prediction.

## Related tools

- **PyTorch** (Deep learning framework for building and training the hybrid CNN-Transformer architecture with bi-encoder, cross-encoder, fusion pooling, and weighted loss)
- **Python** (Primary programming language for implementing the training pipeline, data loading, and validation)
- **Anaconda** (Environment manager for installing and isolating Python dependencies and PyTorch) — https://www.anaconda.com/
- **FlavorFormer** (Reference implementation of the hybrid CNN-Transformer model with bi-encoder/cross-encoder and fusion pooling for NMR-based compound identification) — https://github.com/yfWang01/FlavorFormer

## Examples

```
cd FlavorFormer && conda activate FlavorFormer && jupyter notebook demo.ipynb
```

## Evaluation signals

- Compound identification accuracy on held-out test set should meet or exceed baseline single-encoder models, indicating that the hybrid architecture and dual-branch design improve discriminative power.
- Ranking metrics (Mean Reciprocal Rank, NDCG, or similar) confirm that correct compound labels are ranked higher than incorrect ones in the cross-encoder refinement scores.
- Weighted loss converges smoothly during training without divergence, showing that the balance between bi-encoder and cross-encoder losses is appropriate.
- Fusion pooling outputs (concatenated CNN + Transformer embeddings) are substantially different from either branch alone, confirming that both modalities contribute non-redundant information.
- Validation performance improves when the model is trained end-to-end versus training branches separately, demonstrating that joint optimization via backpropagation leverages the hybrid architecture.

## Limitations

- The skill requires well-preprocessed 1H NMR spectral data; raw spectra with phase distortions, baseline drift, or strong solvent peaks may degrade performance.
- Fusion pooling is a concatenation strategy that increases the embedding dimension; scaling to very large compound libraries may become computationally expensive.
- The weighted loss function requires manual tuning or validation of the balance parameter between bi-encoder and cross-encoder contributions; suboptimal weighting can bias the model toward one branch.
- Generalization to compounds not seen during training depends on the diversity and coverage of reference spectra; out-of-distribution flavor compounds may yield poor identifications.

## Evidence

- [readme] incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra: "incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra"
- [readme] leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly: "leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly"
- [other] Initialize a hybrid CNN-Transformer backbone to extract local features and global dependencies from spectral inputs.: "Initialize a hybrid CNN-Transformer backbone to extract local features and global dependencies from spectral inputs."
- [other] Build a bi-encoder branch that encodes spectra and compound reference embeddings independently, using fusion pooling to combine CNN and Transformer outputs.: "Build a bi-encoder branch that encodes spectra and compound reference embeddings independently, using fusion pooling to combine CNN and Transformer outputs."
- [other] Build a cross-encoder branch that jointly processes spectrum-compound pairs to refine relevance scoring.: "Build a cross-encoder branch that jointly processes spectrum-compound pairs to refine relevance scoring."
- [other] Combine bi-encoder and cross-encoder logits using the weighted loss function and train end-to-end with backpropagation.: "Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation."
- [other] Validate on held-out test set, compute compound identification accuracy and ranking metrics: "Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report."
