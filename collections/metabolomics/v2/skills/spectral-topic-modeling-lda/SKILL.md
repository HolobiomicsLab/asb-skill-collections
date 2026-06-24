---
name: spectral-topic-modeling-lda
description: Use when when you have a collection of normalized mass spectrometry spectra
  (peak intensities or binned m/z representations) and seek to enrich neural network
  training signals for metabolite identification by discovering latent spectral patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0154
  tools:
  - LDA (Latent Dirichlet Allocation)
  - scikit-learn
  techniques:
  - mass-spectrometry
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae490
  all_source_dois:
  - 10.1093/bioinformatics/btae490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Topic Modeling with LDA

## Summary

Apply Latent Dirichlet Allocation (LDA) to preprocessed mass spectrometry spectral features to generate topic probability distributions and assign dominant topic labels per spectrum. These labels serve as auxiliary multi-task learning targets to enhance neural network predictors (MLP and GNN) in metabolite annotation workflows.

## When to use

When you have a collection of normalized mass spectrometry spectra (peak intensities or binned m/z representations) and seek to enrich neural network training signals for metabolite identification by discovering latent spectral patterns. Use this skill if baseline MLP or GNN models lack sufficient training signal diversity and you want to leverage unsupervised topic discovery to create auxiliary classification targets for multi-task learning.

## When NOT to use

- Input spectra are already annotated with ground-truth metabolite class labels; LDA topics may be redundant or conflict with supervised targets.
- Spectral features are not normalized or preprocessed; LDA expects comparable feature scales across spectra.
- Dataset is too small (<100 spectra) or topics do not converge; LDA may extract noise rather than meaningful patterns.

## Inputs

- Normalized spectral feature matrix (shape: n_spectra × n_features, e.g., 1000 bins)
- Spectrum identifiers or indices
- Hyperparameter: number of topics (integer, typically 5–50)

## Outputs

- Topic probability distributions per spectrum (shape: n_spectra × n_topics)
- Dominant topic label assignments per spectrum (1D array, integers 0 to n_topics-1)
- Structured topic label table (spectrum_id, topic_label)

## How to apply

Load the preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation, e.g., 1000-bin resolution). Apply LDA to the spectral features, setting the number of topics as a hyperparameter inferred from domain knowledge or cross-validation (typical range: 5–50 topics). Extract the topic probability distribution for each spectrum and assign the dominant topic label (argmax of the distribution) as the multi-task label. Compile topic assignments into a structured table mapping spectrum identifiers to their topic labels. Validate that the topic distribution covers the dataset reasonably (avoid sparse or imbalanced topics) and that emergent topics capture meaningful spectral patterns (e.g., by inspecting high-probability m/z features per topic) before passing labels to MLP and GNN multi-task training pipelines.

## Related tools

- **LDA (Latent Dirichlet Allocation)** (Unsupervised topic discovery on normalized spectral feature matrices to generate topic probability distributions and dominant topic labels for multi-task learning in MLP and GNN models.)
- **scikit-learn** (Standard Python library implementation of LDA for fitting topic models on spectral features.)

## Examples

```
from sklearn.decomposition import LatentDirichletAllocation; lda = LatentDirichletAllocation(n_components=20, max_iter=10, learning_method='online'); topic_dist = lda.fit_transform(X_spectral); dominant_topics = topic_dist.argmax(axis=1); topic_labels = pd.DataFrame({'spectrum_id': spectrum_ids, 'topic_label': dominant_topics})
```

## Evaluation signals

- Topic distribution is non-degenerate: each topic is assigned to ≥5% of spectra (avoid collapse to a single topic).
- Dominant topic assignments vary across the dataset (entropy or uniqueness check: topics 0 to n_topics-1 all appear in label set).
- High-probability features (m/z bins) per topic exhibit interpretable chemical or spectral patterns (manual inspection or domain validation).
- When used in multi-task training, MLP and GNN models show improved average rank or Rank@K metrics compared to single-task baselines.
- Topic label table schema is valid: every spectrum_id has exactly one topic label in [0, n_topics-1].

## Limitations

- LDA assumes bag-of-words semantics; spectral ordering and m/z continuity are ignored, potentially discarding structural information.
- Topic number selection is a hyperparameter requiring domain knowledge or cross-validation; incorrect choice may produce uninformative or overfragmented topics.
- LDA is unsupervised; generated topics may not align with metabolite classes or chemical structure, requiring downstream validation.
- Preprocessing quality (normalization, binning, noise removal) strongly influences topic quality; poor preprocessing leads to low-signal topics.
- Performance gains from LDA-based multi-task learning are dataset- and architecture-dependent; not guaranteed for all MLP or GNN configurations.

## Evidence

- [other] Spectral topic labels obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors: "Spectral topic labels are obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors alongside an attention mechanism."
- [other] Workflow steps for LDA spectral topic generation: "1. Load preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation) from the dataset. 2. Apply LDA (Latent Dirichlet Allocation) to the spectral features, setting"
- [intro] LDA multi-task enhancement in ESP model: "the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among"
- [readme] Multi-task learning weight parameter in training: "mt_lda_weight=0.01, correlation_mix_residual_weight=0.7, disable_two_step_pred=True"
- [readme] Expected output metrics with LDA multi-task learning enabled: "Average rank 339.350 +- 1264.715"
