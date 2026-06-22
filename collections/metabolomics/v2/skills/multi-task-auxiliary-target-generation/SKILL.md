---
name: multi-task-auxiliary-target-generation
description: Use when training neural network models (MLP or GNN) for metabolite annotation on mass spectrometry data and you have access to a large unlabeled or weakly labeled spectral dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3465
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LDA (Latent Dirichlet Allocation)
  - scikit-learn
  - ESP (Ensembled Spectral Prediction)
derived_from:
- doi: 10.1093/bioinformatics/btae490
  title: ESP
evidence_spans:
- spectral topic labels obtained using LDA (Latent Dirichlet Allocation)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_esp_cq
    doi: 10.1093/bioinformatics/btae490
    title: ESP
  dedup_kept_from: coll_esp_cq
schema_version: 0.2.0
---

# multi-task-auxiliary-target-generation

## Summary

Generate auxiliary task labels (spectral topic labels via LDA) to augment primary metabolite annotation tasks in MLP and GNN models. This skill enriches training data for multi-task learning, improving model generalization on mass spectrometry peak prediction without requiring additional labeled spectra.

## When to use

Apply this skill when training neural network models (MLP or GNN) for metabolite annotation on mass spectrometry data and you have access to a large unlabeled or weakly labeled spectral dataset. Use it specifically when primary annotation labels are sparse or when you want to leverage spectral structure (via unsupervised topic modeling) to regularize model learning and capture latent spectral patterns that correlate with compound identity.

## When NOT to use

- Input spectra are already annotated with high-confidence compound identities; auxiliary task labels add noise rather than regularization.
- Spectral feature matrix is too sparse or noisy to support meaningful topic inference (e.g., <100 spectra or <50 peaks per spectrum).
- Domain knowledge or prior studies indicate spectral topics do not correlate with metabolite classes in your sample; topic labels would be orthogonal to the primary task.

## Inputs

- Preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation)
- Spectrum identifiers mapping
- Number of topics (hyperparameter)

## Outputs

- Spectral topic label assignments (structured table: spectrum ID → dominant topic label)
- Topic probability distributions per spectrum
- Topic label distribution statistics (class balance verification)

## How to apply

Load preprocessed spectral feature matrices (normalized peak intensities or binned m/z representations) from your dataset. Apply Latent Dirichlet Allocation (LDA) to the spectral features, setting the number of topics as a hyperparameter inferred from domain knowledge or cross-validation. Extract the dominant topic assignment for each spectrum to create a topic label per spectrum. Compile these topic labels into a structured table indexed by spectrum identifier. Validate that the topic distribution is reasonably balanced and that topics capture meaningful spectral patterns (e.g., via domain expert review or correlation with known compound classes) before using these labels as auxiliary targets in multi-task training alongside the primary annotation loss.

## Related tools

- **LDA (Latent Dirichlet Allocation)** (Unsupervised probabilistic model to infer latent spectral topics from peak intensity distributions and assign dominant topic label per spectrum)
- **scikit-learn** (Provides LDA implementation and utilities for topic modeling and label assignment) — https://github.com/scikit-learn/scikit-learn
- **ESP (Ensembled Spectral Prediction)** (Downstream multi-task learning framework that consumes generated spectral topic labels as auxiliary targets for MLP and GNN model enhancement) — https://github.com/HassounLab/ESP

## Examples

```
from sklearn.decomposition import LatentDirichletAllocation as LDA; import pandas as pd; lda_model = LDA(n_components=10, random_state=42); topic_probs = lda_model.fit_transform(spectral_features); topic_labels = topic_probs.argmax(axis=1); topic_df = pd.DataFrame({'spectrum_id': spectrum_ids, 'topic_label': topic_labels}); topic_df.to_csv('spectral_topic_labels.csv', index=False)
```

## Evaluation signals

- Topic label distribution is balanced or reflects expected compound class proportions (no single topic dominates >80% of spectra unless domain-justified).
- Topic-to-spectrum assignment is reproducible across multiple LDA runs with the same hyperparameters (assess via adjusted Rand index or label stability).
- Spectra within the same topic exhibit correlated m/z peak patterns or known spectral signatures (spot-check by domain expert or compute topic-peak correlation matrix).
- Downstream multi-task MLP/GNN models trained with auxiliary topic labels show measurable performance gains (e.g., ≥5% improvement in average rank or Rank@K metrics) compared to models trained on primary task alone.
- Topic labels are orthogonal to primary annotation labels (low mutual information or low correlation with known compound class labels, ensuring complementary information).

## Limitations

- LDA hyperparameter (number of topics) is critical and must be tuned; too few topics conflate distinct spectral patterns, too many over-fragment data. No universally optimal setting exists; cross-validation or domain knowledge is required.
- LDA assumes bag-of-words (m/z peak) semantics and may miss sequential or relative peak intensity relationships important to spectral interpretation.
- Topic labels are derived from unsupervised clustering; no guarantee that emergent topics align with metabolite chemistry or functional classes. Validation against compound classes is required before use.
- LDA is computationally expensive on large spectral matrices; scalability may be limited for datasets >100k spectra.
- Spectral feature preprocessing (normalization, binning resolution) strongly influences LDA inference; inconsistent preprocessing across datasets can yield unstable or non-transferable topic models.

## Evidence

- [other] Spectral topic labels are obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors alongside an attention mechanism.: "Spectral topic labels are obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors"
- [other] Apply LDA to the spectral features, setting the number of topics as a hyperparameter (typically inferred from domain knowledge or cross-validation). Extract topic probability distributions for each spectrum and assign the dominant topic label per spectrum.: "Apply LDA (Latent Dirichlet Allocation) to the spectral features, setting the number of topics as a hyperparameter (typically inferred from domain knowledge or cross-validation). Extract topic"
- [other] Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training.: "Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training."
- [intro] the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among: "the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation)"
- [intro] Multi-tasking on spectral topic labels and attention mechanisms enhance MLP and GNN models: "Multi-tasking on spectral topic labels and attention mechanisms enhance MLP and GNN models"
