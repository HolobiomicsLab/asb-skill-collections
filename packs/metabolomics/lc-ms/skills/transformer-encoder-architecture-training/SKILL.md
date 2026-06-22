---
name: transformer-encoder-architecture-training
description: Use when you have paired tandem MS spectra and either (1) molecular fingerprints or structures as labels for supervised fingerprint prediction, or (2) both spectra and unpaired structure/SMILES libraries and want to train embeddings for database-free structure lookup.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2476
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - MIST
  - Transformer
  - PyTorch
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s42256-023-00708-3
  title: MIST (chemical formula transformer)
evidence_spans:
- and, when trained in a contrastive learning framework, enable embedding and structure annotation by database lookup.
- MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula
- github.com/samgoldman97/mist
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mist_chemical_formula_transformer_cq
    doi: 10.1038/s42256-023-00708-3
    title: MIST (chemical formula transformer)
  dedup_kept_from: coll_mist_chemical_formula_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-023-00708-3
  all_source_dois:
  - 10.1038/s42256-023-00708-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Transformer-Encoder Architecture Training

## Summary

Train a transformer encoder to learn representations of chemical formulae or fingerprints from tandem mass spectrometry data, either for direct fingerprint prediction or as the foundation for contrastive learning-based structure annotation. This skill combines multi-head self-attention over tokenized chemical inputs with end-to-end supervised or contrastive loss to produce joint embedding spaces for metabolite inference.

## When to use

You have paired tandem MS spectra and either (1) molecular fingerprints or structures as labels for supervised fingerprint prediction, or (2) both spectra and unpaired structure/SMILES libraries and want to train embeddings for database-free structure lookup. Apply this skill when you need to learn a non-linear, context-aware mapping from fragmentation patterns (encoded as chemical formulae) to molecular properties, rather than using handcrafted spectral features or database matching alone.

## When NOT to use

- You have only raw MS/MS spectra without chemical formula extraction or structural ground truth—the model requires structured formula inputs and paired or contrastive labels to learn effectively.
- You need real-time or low-latency inference on embedded devices—transformer encoders are computationally expensive compared to small MLPs or lookup tables.
- Your spectra are from a single instrument type with very narrow mass range—the transformer's multi-head attention may overfit on small, domain-specific datasets without sufficient negative sampling or regularization.

## Inputs

- Tandem mass spectrometry data (MGF or .ms format)
- Extracted chemical formula collections (peak-level or fragment-level)
- Molecular fingerprint labels (for supervised mode) or SMILES/structure strings (for contrastive mode)
- Molecular vocabulary/tokenizer definition
- Reference metabolite database with spectra and structures (for contrastive mode)

## Outputs

- Trained transformer encoder model (PyTorch weights and architecture)
- Spectrum embeddings (fixed-dimensional vectors)
- Predicted fingerprint vectors or joint embedding space
- Model checkpoint files with architecture serialization

## How to apply

Tokenize and embed chemical formulae extracted from tandem MS peaks using a learned vocabulary. Pass the embedded formula sequences through a transformer encoder stack with multi-head self-attention to capture dependencies among fragments. Pool the final transformer output (e.g., via mean pooling or a [CLS] token) to obtain a fixed-dimensional spectrum representation. For supervised training: project this representation through a dense layer to predict a molecular fingerprint vector; optimize end-to-end using fingerprint prediction loss (e.g., binary cross-entropy for bit-level fingerprints). For contrastive training: encode a reference database of spectra and structures into a joint embedding space, initialize the spectrum and structure encoders, and train using contrastive loss with negative sampling from unpaired spectra-structure pairs per batch, ensuring alignment of positive pairs while pushing apart negatives. Use convergence criteria (validation loss plateau, fingerprint Tanimoto similarity, or retrieval recall) to determine when training is complete. Save both architecture definition and trained weights.

## Related tools

- **MIST** (Reference implementation of transformer encoder architecture for fingerprint prediction from tandem MS) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extended transformer encoder variant with sinusoidal formula embeddings, adduct type embedding, and neutral loss fragments for chemical formula prediction) — https://github.com/samgoldman97/mist-cf
- **PyTorch** (Deep learning framework for implementing transformer encoder architecture and training loop)
- **Transformer** (Multi-head self-attention encoder for learning representations of chemical formula sequences)
- **SIRIUS** (Dependency tool for extracting chemical formula collections (subformulae) from tandem MS peaks via dynamic programming) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
. quickstart/00_download_models.sh && . quickstart/01_run_models.sh
```

## Evaluation signals

- Fingerprint prediction accuracy: Tanimoto similarity between predicted and ground-truth fingerprints on held-out test spectra should be ≥ 0.7 for reliable predictions.
- Embedding space alignment (contrastive mode): cosine similarity between positive spectrum-structure pairs should be significantly higher than negative pairs; retrieval recall@k (k=1, 10, 100) on a validation database lookup should exceed baseline/random expectation.
- Training convergence: validation loss should plateau and not decrease further over multiple epochs; no signs of divergence or NaN losses.
- Model reproducibility: loading saved weights and architecture on a fresh environment should produce identical predictions on the same input spectra (deterministic up to floating-point precision).
- Attention visualization: learned self-attention patterns should show non-trivial dependencies among formula tokens rather than uniform or random attention weights.

## Limitations

- MIST and MIST-CF assume H+ ionization mode ([M+H]+) or positive-mode spectra; negative-mode spectra or multi-adduct datasets may require retraining or fine-tuning.
- Chemical formula extraction (subformula assignment) is a preprocessing bottleneck—errors in fragmentation tree or formula decomposition propagate to the transformer encoder and degrade performance.
- Contrastive training requires careful negative sampling strategy and batch size tuning; insufficient or biased negative pairs may lead to poor embedding generalization or mode collapse.
- The transformer encoder does not natively incorporate instrument metadata, mass resolution, or collision energy—these must be embedded as separate covariates if available, as described in MIST-CF.
- Training on small or imbalanced datasets (e.g., rare metabolite classes) may lead to overfitting; data augmentation via forward mass prediction models is used in the paper but requires a separate trained augmentation model.

## Evidence

- [other] MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formulae extracted from tandem mass spectrometry data to produce molecular fingerprint predictions: "MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formulae, rather than directly embedding binned spectra, and uses this encoding to predict"
- [other] Supervised fingerprint prediction workflow including tokenization, transformer encoding, pooling, and projection: "Tokenize and embed chemical formulae using a learned vocabulary. Pass embedded formula sequences through a transformer encoder stack with multi-head self-attention. Pool the transformer output (e.g.,"
- [other] Contrastive learning framework for structure annotation via embedding and database lookup: "When trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup"
- [other] Contrastive training procedure with negative sampling from unpaired spectra-structure pairs: "Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch"
- [other] Nearest-neighbor retrieval after embedding database into joint space: "For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores"
- [readme] MIST-CF advances including sinusoidal formula embeddings and instrument type embedding: "Utilizing sinusoidal *formula* embeddings as developed in our previous work. Embedding instrument type used to measure the MS/MS as an additional model 'covariate' to help make predictions"
- [readme] Installation and environment setup instructions: "After git cloning the repository, the environment and package can be installed. Please note that the environment downloaded attempts to utilize cuda11.1"
