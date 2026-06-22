---
name: neural-network-architecture-design-spectra
description: Use when you have preprocessed MS/MS spectra pairs (unknown and known metabolites) with annotated structural similarity labels, and you need to learn a generalizable model that can rank candidate structures for novel unknowns by predicting their similarity to reference compounds in a database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3172
  tools:
  - DeepMASS
  - Keras
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.8b05405
  title: Deep MS/MS similarity
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deep_ms_ms_similarity_cq
    doi: 10.1021/acs.analchem.8b05405
    title: Deep MS/MS similarity
  dedup_kept_from: coll_deep_ms_ms_similarity_cq
schema_version: 0.2.0
---

# neural-network-architecture-design-spectra

## Summary

Design and train a deep learning architecture to encode MS/MS spectral data into learned representations that predict structural similarity between unknown and known metabolites. This skill is essential when you have paired spectra datasets with structural similarity labels and need to extend metabolite identification beyond existing spectral databases.

## When to use

You have preprocessed MS/MS spectra pairs (unknown and known metabolites) with annotated structural similarity labels, and you need to learn a generalizable model that can rank candidate structures for novel unknowns by predicting their similarity to reference compounds in a database.

## When NOT to use

- Input spectra are raw, unnormalized, or lack paired training examples with similarity annotations — preprocessing and data labeling must precede architecture design.
- You only have single spectra or unpaired data; supervised similarity prediction requires annotated pairs.
- The goal is compound identification using exact mass or database matching rather than similarity-based ranking — this skill is for extending beyond exact matches.

## Inputs

- Paired MS/MS spectra datasets (unknown and known metabolite spectra) in text or binary format
- Spectra metadata including m/z values and intensity values
- Annotated structural similarity labels (ground-truth scores) for training pairs

## Outputs

- Trained deep learning model weights
- Learned spectral representations (embeddings)
- Predicted structural similarity scores (continuous values, typically 0–1 or normalized)
- Inference function for ranking candidate structures

## How to apply

Design a supervised deep learning model that takes normalized m/z intensity vectors from MS/MS spectra as input and outputs continuous structural similarity predictions. Preprocess spectra by normalizing intensity values and extracting m/z features relevant to molecular structure. Train the network on paired spectrum examples with annotated similarity scores using a regression loss (e.g., mean squared error). Use a held-out test set to evaluate model performance via Pearson correlation or similar metric between predicted and reference similarities. Once trained, export the model weights and inference function to score candidate structures by computing their predicted similarity to unknown spectra, enabling ranking of structural candidates.

## Related tools

- **DeepMASS** (Reference implementation of the deep learning architecture for MS/MS-aided structural similarity scoring; provides pre-trained model weights and inference pipeline for metabolite identification) — https://github.com/hcji/DeepMASS
- **Keras** (Neural network framework for designing and training the deep learning model architecture)
- **RDKit** (Cheminformatics library for validating structural representations and computing reference similarity scores)

## Evaluation signals

- Pearson correlation between predicted and reference structural similarity scores on held-out test set is statistically significant and ≥ 0.7 (or domain-appropriate threshold)
- Model training loss (e.g., MSE) converges and stabilizes; validation loss does not increase (no overfitting signals)
- Predictions are in expected range (e.g., 0–1 or normalized); no NaN, inf, or out-of-bound outputs
- Ranked candidate structures for unknown spectra place correct structural analogs in top-k positions compared to manual expert review or external validation set
- Model weights and architecture can be serialized and loaded without errors; inference on new spectra produces consistent, deterministic outputs

## Limitations

- Model performance depends critically on the quality, diversity, and quantity of annotated training spectrum pairs; limited training data or unrepresentative spectra lead to poor generalization.
- DeepMASS official training dataset (MetDNA) was removed from public distribution; users must train on their own in-house spectral databases or wait for public dataset inclusion.
- The skill assumes MS/MS spectra are comparable in acquisition protocol and instrument type; spectra from different ionization modes or mass analyzers may require retraining.
- Deep learning models are opaque; predictions cannot easily explain which spectral features drive similarity decisions, limiting interpretability for validation.

## Evidence

- [other] Design a deep learning architecture to encode spectral data into learned representations.: "Design a deep learning architecture to encode spectral data into learned representations."
- [other] Train the model on annotated spectrum pairs with structural similarity labels using supervised learning.: "Train the model on annotated spectrum pairs with structural similarity labels using supervised learning."
- [other] Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities).: "Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities)."
- [readme] DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based on their MS/MS spectra: "DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based"
- [readme] Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified by the existing database.: "Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified by the existing database."
- [readme] Since the experimental spectra has been removed, this package cannot be run directly. You can train your own model with your in-house database.: "Since the experimental spectra has been removed, this package cannot be run directly. You can train your own model with your in-house database."
