---
name: deep-learning-model-training-and-inference
description: Use when you have paired tandem MS/MS spectra with known molecular fingerprints, chemical formulae, or SMILES annotations, and you want to learn a generalizable model that can predict molecular properties or annotate unknown spectra by ranking candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Transformer
  - SIRIUS
  - MIST
  - MIST-CF
derived_from:
- doi: 10.1038/s42256-023-00708-3
  title: MIST (chemical formula transformer)
evidence_spans:
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
---

# Deep Learning Model Training and Inference

## Summary

Train and deploy transformer-based neural networks to encode collections of chemical formulae extracted from tandem mass spectrometry (MS/MS) data and predict molecular fingerprints or chemical formula assignments. This skill applies multi-head self-attention mechanisms to learn structured representations of fragmentation patterns in an end-to-end, data-dependent fashion without relying on fragmentation tree databases.

## When to use

You have paired tandem MS/MS spectra with known molecular fingerprints, chemical formulae, or SMILES annotations, and you want to learn a generalizable model that can predict molecular properties or annotate unknown spectra by ranking candidates. Apply this skill when the data volume is sufficient to train a transformer (typically 10k–100k+ spectra) and when you need predictions on new spectra not seen during training.

## When NOT to use

- Input spectra are pre-binned into feature matrices or have already been featurized by another method; this skill expects raw or parsed formula collections as input.
- You have fewer than ~1,000 paired spectra; transformer models require sufficient data to learn robust representations and avoid overfitting.
- Your goal is to annotate spectra using only spectrum-to-spectrum similarity without learning molecular structure; use database lookup or spectral matching instead.

## Inputs

- Tandem mass spectrometry data (MGF or MS format files)
- Chemical formula collections (extracted via SIRIUS decomp or subformula assignment)
- Molecular fingerprints or reference structures (SMILES, InChIKey)
- Paired labels table (columns: dataset, spec, name, ionization, formula, smiles, inchikey, instrument)
- Data splits (train/validation/test assignments)

## Outputs

- Trained transformer model architecture and weights (PyTorch checkpoint)
- Predicted molecular fingerprint vectors (dimensions matching target space)
- Ranked chemical formula or adduct assignments with scores
- Spectrum embeddings in a dense continuous space (for contrastive retrieval)
- Model performance metrics (accuracy, top-k ranking, similarity scores)

## How to apply

Extract chemical formula collections (via SIRIUS decomposition or internal subformula assignment) from each MS/MS spectrum. Tokenize and embed formulae using a learned vocabulary, then pass embedded sequences through a transformer encoder stack with multi-head self-attention to capture formula interdependencies. Pool the transformer output using mean pooling or a CLS token to obtain a fixed-dimensional representation. For fingerprint prediction, project this pooled vector through a dense layer to match the target fingerprint dimensionality; for formula ranking, score each candidate formula by comparing its embedding to the spectrum encoding. Train end-to-end using a contrastive or classification loss function. Validate on a held-out test set and save both architecture and trained weights.

## Related tools

- **PyTorch** (Framework for implementing transformer encoder architecture, multi-head self-attention, and end-to-end training)
- **Transformer** (Neural network architecture for encoding formula sequences and learning structure-aware representations)
- **SIRIUS** (Dynamic programming algorithm for extracting potential chemical formulae from observed MS1 masses (SIRIUS decomp module)) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST** (End-to-end implementation of spectrum-to-fingerprint transformer for contrastive learning and retrieval annotation) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extension of MIST for ranking chemical formula and adduct assignments in de novo MS/MS annotation) — https://github.com/samgoldman97/mist-cf

## Examples

```
conda activate ms-gen && python -m mist.train --data_path data/paired_spectra/canopus_train --save_dir checkpoints/mist_fp --model_type transformer --batch_size 32 --epochs 50 && python -m mist.predict --model_path checkpoints/mist_fp/model.pt --spectra_file quickstart/quickstart.mgf --output_dir predictions/
```

## Evaluation signals

- Transformer output shape matches expected pooled representation dimensionality (e.g., matching fingerprint space or score vector length).
- Trained model weights are serializable and can be reloaded to reproduce inference on held-out test spectra without retraining.
- Predicted fingerprints or scores are numerically bounded (e.g., 0–1 for binary fingerprints, or calibrated probability-like scores) and match training data statistics.
- Validation set performance (e.g., top-k retrieval accuracy, Tanimoto similarity to reference fingerprints) matches or exceeds reported baselines in the literature or previous runs.
- Spectrum embeddings from the contrastive model form tight clusters around structurally similar molecules and separate isomers or different compound classes.

## Limitations

- Model performance on commercial high-resolution data (Orbitrap, QTOF) may degrade if trained primarily on public natural products libraries (GNPS, NPLIB1); NIST20 training improves performance but requires proprietary access.
- Transformer models require substantial GPU memory and training time for large datasets; inference is tractable but batch prediction is recommended for throughput.
- Chemical formula tokenization and embedding depend on vocabulary coverage; rare or novel formulae outside the training vocabulary may produce degraded predictions.
- The skill assumes formula collections are pre-computed (via SIRIUS or an internal protocol); if the fragmentation mechanism is poorly characterized or spectra are severely noisy, formula extraction will fail or produce spurious candidates.
- Model generalization is limited to the ionization mode, instrument type, and chemical space seen during training; cross-mode or out-of-distribution molecules require retraining or domain adaptation.

## Evidence

- [intro] MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formulae: "MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formulae extracted from tandem mass spectrometry data"
- [other] Transformer encoder with multi-head attention workflow: "Pass embedded formula sequences through a transformer encoder stack with multi-head self-attention. 4. Pool the transformer output (e.g., via mean pooling or CLS token) to obtain a fixed-dimensional"
- [readme] Energy-based modeling and de novo ranking approach: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [intro] Contrastive learning framework for embedding and annotation: "when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup"
- [readme] Data-dependent learning without fragmentation trees: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
