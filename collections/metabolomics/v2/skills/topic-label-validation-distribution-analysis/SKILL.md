---
name: topic-label-validation-distribution-analysis
description: Use when after LDA topic inference has assigned dominant topic labels to mass spectra, and before those labels are passed to MLP or GNN multi-task training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3238
  edam_topics:
  - http://edamontology.org/topic_3520
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae490
  all_source_dois:
  - 10.1093/bioinformatics/btae490
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# topic-label-validation-distribution-analysis

## Summary

Validate and analyze the distribution of LDA-derived spectral topic labels across a dataset to ensure they capture meaningful spectral patterns before use as multi-task learning targets. This skill verifies label quality and statistical representativeness to enable reliable enhancement of neural network models.

## When to use

After LDA topic inference has assigned dominant topic labels to mass spectra, and before those labels are passed to MLP or GNN multi-task training. Use this skill when you need to confirm that topic assignments are balanced across the dataset, that no topics are over- or under-represented, and that the inferred topics reflect genuine spectral heterogeneity rather than artifacts of the LDA fit.

## When NOT to use

- Topic labels have not yet been assigned by LDA (perform LDA inference first).
- The goal is exploratory LDA analysis rather than preparation for multi-task learning (use unsupervised topic coherence metrics instead).
- Spectra are from a completely homogeneous sample expected to cluster into a single topic (distribution validation is unnecessary when diversity is not expected).

## Inputs

- spectrum identifiers (string or integer array)
- LDA-inferred dominant topic labels (integer array, one label per spectrum)
- preprocessed spectral feature matrix or metadata (for validation cross-reference)

## Outputs

- topic label distribution table (topic ID, count, proportion)
- distribution statistics (mean, std, min, max topic frequency)
- validation report (flag for imbalance or anomalies)
- validated label assignments (confirmed safe for downstream multi-task training)

## How to apply

Load the structured table of spectrum identifiers and their corresponding LDA topic label assignments. Compute the frequency distribution (histogram or count table) of topic labels across all spectra in the dataset. Check for severe class imbalance (e.g., one topic dominating >80% of spectra) or near-empty topics, which would indicate poor topic separation or hyperparameter miscalibration. Validate that topics capture coherent spectral patterns by spot-checking representative spectra in each topic class and confirming that inferred topics align with domain knowledge of mass spectrometry fragmentation. Record the label distribution statistics (counts, proportions, min/max topic frequency) and flag any anomalies before passing validated labels to multi-task training pipelines.

## Related tools

- **LDA (Latent Dirichlet Allocation)** (Upstream inference tool that produces the topic labels being validated)
- **scikit-learn** (Provides histogram, counting, and statistical distribution functions for label validation)
- **ESP (Ensembled Spectral Prediction)** (Downstream multi-task learning pipeline that consumes validated topic labels) — https://github.com/HassounLab/ESP

## Examples

```
# Validate topic label distribution after LDA inference
topic_counts = pd.Series(topic_labels).value_counts().sort_index()
print(topic_counts)
if topic_counts.max() / len(topic_labels) > 0.8:
    print('WARNING: Severe class imbalance detected')
else:
    print('Topic distribution validated; safe for multi-task training')
```

## Evaluation signals

- No topic label is missing or null across the spectrum identifiers (100% label assignment rate).
- No single topic accounts for >80% of the dataset (severe class imbalance check).
- Each topic has at least 5–10 assigned spectra (minimum viable frequency to avoid overfitting in multi-task branch).
- Distribution plot shows multiple distinct topic clusters rather than a unimodal peak (confirms topic separation).
- When spot-checked, representative spectra within each topic show visual or chemical coherence (fragmentation patterns or m/z distributions align within topic groups).

## Limitations

- LDA hyperparameter (number of topics) must be set a priori; this validation cannot recover from severe over- or under-specification of topic count.
- Distribution validation does not guarantee that topics are chemically meaningful or align with reference metabolite classes; visual and domain-expert inspection is still required.
- Imbalanced distributions may reflect true underlying biology (e.g., a dataset dominated by lipids) rather than a methodological failure; domain context is necessary to interpret flagged anomalies.
- Small datasets (<500 spectra) may show high variance in topic label frequencies even with correct LDA settings; statistical significance of imbalance should be interpreted cautiously.

## Evidence

- [other] Compile topic label assignments into a structured table with spectrum identifiers and their corresponding topic labels.: "Compile topic label assignments into a structured table with spectrum identifiers and their corresponding topic labels."
- [other] Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training.: "Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training."
- [intro] spectral topic labels obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors alongside an attention mechanism.: "spectral topic labels obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors"
- [readme] multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among: "multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies"
