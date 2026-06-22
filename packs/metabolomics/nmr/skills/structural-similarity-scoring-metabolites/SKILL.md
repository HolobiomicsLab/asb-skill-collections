---
name: structural-similarity-scoring-metabolites
description: Use when when you have paired MS/MS spectra from unknown metabolites and a reference database of known metabolites, and you want to rank candidate structures for unknown compounds by their predicted structural similarity rather than exact spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - DeepMASS
  - Keras
  - RDKit
  - IsoSpecPy
  techniques:
  - LC-MS
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.8b05405
  all_source_dois:
  - 10.1021/acs.analchem.8b05405
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Deep Learning–Based Structural Similarity Scoring for Unknown Metabolite Identification

## Summary

A skill for predicting structural similarity between unknown metabolites and known reference metabolites by encoding MS/MS spectra into learned representations using a deep neural network, then ranking candidate structures by predicted similarity. This extends metabolite identification beyond the limited set of high-quality reference spectra in existing databases.

## When to use

When you have paired MS/MS spectra from unknown metabolites and a reference database of known metabolites, and you want to rank candidate structures for unknown compounds by their predicted structural similarity rather than exact spectral matching. Particularly useful when the unknown spectrum does not have a direct match in available MS/MS libraries but may share structural features with known compounds.

## When NOT to use

- When you have exact MS/MS spectral matches available in your reference database — use direct spectral matching (e.g., cosine similarity) instead, which is faster and more precise.
- When your unknown spectra come from a compound class not represented in your training dataset — the model's learned representations may not generalize well to out-of-distribution structural features.
- When you lack annotated training data with structural similarity labels — supervised training requires pairs with known similarities; unsupervised or transfer learning approaches would be needed otherwise.

## Inputs

- Paired MS/MS spectra datasets with metadata (unknown and known metabolite spectra)
- Annotated spectrum pairs with structural similarity labels or ground-truth similarity scores
- MS/MS spectrum files (format: implementation-dependent; see data/spectra directory)

## Outputs

- Trained deep learning model weights and inference function
- Predicted structural similarity scores for unknown-vs-reference metabolite pairs
- Ranked candidate structures for each unknown metabolite sorted by predicted similarity

## How to apply

Load and preprocess paired MS/MS spectra datasets by normalizing intensity values and extracting relevant m/z features from both unknown and reference spectra. Design and train a deep learning architecture (using Keras) that encodes spectral data into learned representations, trained on annotated spectrum pairs with structural similarity labels via supervised learning. Evaluate the trained model on held-out test spectra using Pearson correlation between predicted and reference similarities as the primary metric. Export the trained model weights and inference function, then apply the model to score all reference spectra against each unknown spectrum, ranking candidates by predicted structural similarity score. The model leverages transformational relationships and structural patterns in MS/MS spectra that deep learning can capture beyond direct spectral matching.

## Related tools

- **DeepMASS** (Core implementation of deep learning model for structural similarity prediction from MS/MS spectra; includes pre-trained model weights and inference pipeline for ranking candidate metabolites) — https://github.com/hcji/DeepMASS
- **Keras** (Deep learning framework used to design and train the neural network architecture for spectral encoding)
- **RDKit** (Used for chemical structure handling and possibly similarity calculations during evaluation and candidate ranking)
- **IsoSpecPy** (Isotope pattern calculation; used as dependency for spectral preprocessing or comparison)

## Examples

```
# After installing DeepMASS and placing your spectral data in data/spectra:
python test.py  # Train a model on your in-house database
# Then use example.py to identify unknown metabolites by scoring against known reference spectra
```

## Evaluation signals

- Pearson correlation between predicted and reference structural similarities on held-out test spectra should be positive and ≥0.6 (or threshold documented in training); correlation near 0 or negative indicates model failure.
- Ranked candidate list for unknown spectra should place known ground-truth structures in top-N positions (e.g., rank ≤10); metric: recall@N or mean reciprocal rank (MRR).
- Model inference should complete on all test spectra without crashes; output predictions should lie in a bounded range (e.g., [0, 1]) consistent with similarity score design.
- When the same unknown spectrum is scored against a subset of reference compounds, the ranking should be consistent across runs and reproducible given the same trained weights.
- Ablation or comparison: re-training with a known-good reference dataset should recover model performance metrics documented in the DeepMASS publication; deviation suggests implementation or data quality issues.

## Limitations

- Training requires high-quality annotated MS/MS spectra pairs with known structural similarity labels; the original DeepMASS model was trained on the MetDNA dataset, which has been removed and cannot be redistributed without permission. Users must train on their own in-house databases or wait for public datasets to be integrated.
- Model generalization is limited to the chemical and structural space represented in the training data; performance on unknown metabolite classes or novel structural scaffolds not seen during training may degrade significantly.
- The workflow predicts similarity but does not guarantee correctness; rankings should be validated by orthogonal methods (e.g., NMR, chemical standards, or computational structure prediction) before confident assignment.
- MS/MS spectral quality, instrument type, and fragmentation method (e.g., collision energy) affect both preprocessing and model input; spectra from different instruments or acquisition protocols may require retraining or domain adaptation.
- No changelog is available, and the original public dataset has been removed, limiting reproducibility and transparency of model versions.

## Evidence

- [readme] DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based on their MS/MS spectra and a rank method for picking out the possible candidate structures of the unknowns.: "DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based"
- [readme] Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified by the existing database.: "Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified by the existing database"
- [other] Preprocess spectra by normalizing intensity values and extracting relevant m/z features. Design a deep learning architecture to encode spectral data into learned representations. Train the model on annotated spectrum pairs with structural similarity labels using supervised learning.: "Preprocess spectra by normalizing intensity values and extracting relevant m/z features. Design a deep learning architecture to encode spectral data into learned representations. Train the model on"
- [other] Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities).: "Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities)"
- [readme] Since the experimental spectra has been removed, this package cannot be run directly. You can train your own model with your in-house database.: "Since the experimental spectra has been removed, this package cannot be run directly. You can train your own model with your in-house database"
