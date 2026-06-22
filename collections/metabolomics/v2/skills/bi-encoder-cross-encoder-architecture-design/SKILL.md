---
name: bi-encoder-cross-encoder-architecture-design
description: Use when you have paired spectrum-compound reference data and need to simultaneously retrieve candidate compounds rapidly (bi-encoder) while also refining relevance scores through joint context modeling (cross-encoder).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Anaconda
  - PyTorch
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bi-encoder-cross-encoder-architecture-design

## Summary

Design and train a hybrid bi-encoder and cross-encoder architecture to identify compounds in NMR spectra by combining independent and joint encoding pathways with fusion pooling and weighted loss. This dual-pathway approach balances efficiency (bi-encoder) with refined ranking (cross-encoder) to achieve accurate compound identification in flavor mixtures.

## When to use

Use this skill when you have paired spectrum-compound reference data and need to simultaneously retrieve candidate compounds rapidly (bi-encoder) while also refining relevance scores through joint context modeling (cross-encoder). The architecture is particularly suited for mixture analysis tasks where both candidate recall and ranking precision matter—e.g., NMR-based flavor or chemical mixture profiling where a spectrum may match multiple compounds but the correct match must rank highest.

## When NOT to use

- Input is already a pre-computed compound ranking or relevance score matrix (skip architectural design and retrain only).
- Spectra contain only a single compound with no ambiguity; simpler single-encoder models suffice.
- NMR data is not preprocessed (e.g., uncalibrated chemical shifts, missing baseline correction); preprocess first before architecture design.

## Inputs

- preprocessed 1H NMR spectral data (numeric array or tensor)
- compound labels and reference embeddings for training set
- spectrum-compound pair annotations for cross-encoder supervision

## Outputs

- trained hybrid bi-encoder cross-encoder model checkpoint
- compound identification accuracy metrics
- ranking metrics (e.g., mean reciprocal rank, NDCG) on test set
- performance report

## How to apply

Initialize a hybrid CNN-Transformer backbone to extract both local spectral features (via CNN) and global dependencies (via Transformer) from 1H NMR input data. In parallel, build a bi-encoder branch that independently encodes preprocessed spectra and compound reference embeddings, then fuse CNN and Transformer outputs using fusion pooling to create unified spectrum and compound embeddings. Simultaneously, build a cross-encoder branch that processes spectrum-compound pairs jointly to refine relevance scores. Combine logits from both branches via a weighted loss function that balances bi-encoder and cross-encoder contributions during end-to-end backpropagation training. Validate on a held-out test set using compound identification accuracy and ranking metrics to confirm that the dual-pathway design captures both semantic similarity and contextual relevance.

## Related tools

- **PyTorch** (Deep learning framework for implementing CNN-Transformer backbone, bi-encoder and cross-encoder branches, fusion pooling, and weighted loss function training)
- **Python** (Primary language for data loading, model orchestration, validation loop, and metric computation)
- **Anaconda** (Environment and dependency management for reproducible setup of Python 3.13.2 and PyTorch 2.7.0+cu118) — https://www.anaconda.com/

## Examples

```
conda activate FlavorFormer && jupyter notebook demo.ipynb
```

## Evaluation signals

- Compound identification accuracy on held-out test set meets or exceeds baseline single-encoder model on the same dataset.
- Cross-encoder refinement step improves ranking metrics (MRR, NDCG, precision@k) compared to bi-encoder logits alone, confirming that joint spectrum-compound processing adds value.
- Weighted loss function converges smoothly during training, with both bi-encoder and cross-encoder loss components decreasing monotonically (no divergence).
- Fusion pooling output dimensions match expected embedding size; no shape mismatches between CNN and Transformer feature streams during pooling.
- Test set compound retrieval rankings are plausible: true compound labels rank significantly higher (top-k) than random baselines and single-encoder alternatives.

## Limitations

- Identifying components in mixtures using NMR spectra remains challenging; the architecture does not eliminate fundamental spectral overlap or ambiguity when multiple compounds share similar NMR signatures.
- Performance depends critically on quality and completeness of compound reference embeddings and training labels; missing or mislabeled training data degrades both branches.
- Computational cost scales with cross-encoder pair-wise processing; for very large compound libraries, inference time may become prohibitive unless approximate ranking (via bi-encoder only) precedes cross-encoder re-ranking.

## Evidence

- [readme] leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly: "leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly"
- [readme] incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra: "incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra"
- [other] Build a bi-encoder branch that encodes spectra and compound reference embeddings independently, using fusion pooling to combine CNN and Transformer outputs: "Build a bi-encoder branch that encodes spectra and compound reference embeddings independently, using fusion pooling to combine CNN and Transformer outputs"
- [other] Build a cross-encoder branch that jointly processes spectrum-compound pairs to refine relevance scoring: "Build a cross-encoder branch that jointly processes spectrum-compound pairs to refine relevance scoring"
- [other] Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation: "Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation"
- [other] Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report: "Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report"
