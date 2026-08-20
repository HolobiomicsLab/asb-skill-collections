---
name: unsupervised-pattern-discovery-spectra
description: Use when when you have preprocessed mass spectral data (normalized peak intensities or binned m/z representations) and need to discover latent spectral patterns to enhance neural network predictors without labeled spectral classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - LDA (Latent Dirichlet Allocation)
  - Latent Dirichlet Allocation (LDA)
  - scikit-learn
  - ESP (Ensembled Spectral Prediction)
  techniques:
  - LC-MS
  - GC-MS
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

# Unsupervised Pattern Discovery in Mass Spectra

## Summary

Apply Latent Dirichlet Allocation (LDA) to mass spectral features to discover latent topic distributions and assign dominant spectral topic labels unsupervised. This technique surfaces meaningful spectral patterns without manual annotation and generates auxiliary labels for downstream multi-task learning on MLP and GNN metabolite annotation models.

## When to use

When you have preprocessed mass spectral data (normalized peak intensities or binned m/z representations) and need to discover latent spectral patterns to enhance neural network predictors without labeled spectral classes. Particularly useful when training MLP or GNN models on metabolite annotation tasks and you want to leverage latent topic structure as additional multi-task learning signal.

## When NOT to use

- Input spectra are already manually annotated with spectral classes or substructure labels — LDA is redundant if ground-truth labels are available.
- Spectral data is unpreprocessed (raw, non-normalized, or contains extreme outliers) — LDA assumes cleaned, normalized input.
- The goal is peak-by-peak feature importance rather than global spectral pattern discovery — consider explainability methods instead.

## Inputs

- Preprocessed spectral feature matrix (normalized peak intensities or binned m/z values; shape: [num_spectra, num_features])
- Spectrum identifiers (e.g., NIST accession numbers or internal sample IDs)
- Number of topics (hyperparameter; domain-guided or cross-validation tuned)

## Outputs

- Topic probability distribution table (shape: [num_spectra, num_topics])
- Dominant topic label assignment per spectrum (shape: [num_spectra])
- Label distribution summary (counts and proportions per topic across dataset)
- Validation report of topic interpretability (e.g., top-weighted features per topic)

## How to apply

Load the preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation across all spectra in your dataset). Apply LDA with the number of topics set as a hyperparameter—typically inferred from domain knowledge or via cross-validation. Extract the topic probability distribution for each spectrum and assign the dominant topic label (argmax) per spectrum. Compile topic label assignments into a structured table indexed by spectrum identifiers. Validate that the resulting topic distribution is reasonably balanced across the dataset and that emergent topics capture interpretable spectral patterns (e.g., fragments, adducts, or structural motifs) before passing labels to multi-task training pipelines.

## Related tools

- **Latent Dirichlet Allocation (LDA)** (Unsupervised generative model to discover latent topic distributions in spectral feature space and assign topic labels per spectrum)
- **scikit-learn** (Provides LDA implementation (LatentDirichletAllocation) for fitting topic models on spectral features) — https://scikit-learn.org
- **ESP (Ensembled Spectral Prediction)** (Downstream framework that integrates LDA-derived topic labels as multi-task learning targets to enhance MLP and GNN metabolite annotation models) — https://github.com/HassounLab/ESP

## Evaluation signals

- Topic label distribution is reasonably balanced across the dataset (no single topic dominates >80% of spectra); histogram of topic assignments should show multi-modal coverage.
- Top-weighted spectral features per topic are interpretable and distinct (e.g., topic clusters around common neutral losses, adducts, or fragment ion patterns relevant to metabolomics).
- Dominant topic assignments are stable across runs (low variance when LDA is retrained with fixed random seed).
- Downstream multi-task MLP/GNN models trained with LDA topic labels show measurable performance gain (e.g., ≥ 1–2% improvement in Rank@1 or average rank) compared to models without multi-tasking.
- Topic-to-spectrum assignments pass consistency checks: no spectrum assigned to multiple dominant topics, and all spectra receive exactly one label.

## Limitations

- Number of topics is a critical hyperparameter; improper choice (too few or too many) may yield uninformative or over-fragmented patterns. Cross-validation guidance required.
- LDA assumes bag-of-words structure (feature independence); spectral features may have latent correlations that LDA does not capture.
- Topics discovered on one dataset (e.g., ESI/LC-MS) may not transfer to another instrument modality (e.g., EI/GC-MS) without retraining.
- Dominant topic assignment is hard (argmax); soft topic posteriors may be more informative for weakly-separated spectra but require modified downstream integration.
- LDA convergence and reproducibility depend on random initialization and hyperparameters (alpha, beta); reported results in ESP were limited to NPLIB1 dataset and may vary on external data.

## Evidence

- [other] Spectral topic labels are obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors alongside an attention mechanism.: "Spectral topic labels are obtained using LDA (Latent Dirichlet Allocation) and used as additional multi-tasking data to enhance both MLP and GNN predictors"
- [other] Load preprocessed spectral feature matrix from dataset, apply LDA setting the number of topics as a hyperparameter, extract topic probability distributions, and assign dominant topic label per spectrum.: "Load preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation) from the dataset. 2. Apply LDA (Latent Dirichlet Allocation) to the spectral features, setting the"
- [other] Extract topic probability distributions for each spectrum and assign the dominant topic label per spectrum. Compile topic label assignments into a structured table with spectrum identifiers and their corresponding topic labels.: "Extract topic probability distributions for each spectrum and assign the dominant topic label per spectrum. 4. Compile topic label assignments into a structured table with spectrum identifiers"
- [other] Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training.: "Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training"
- [readme] The MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among spectra peaks.: "the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation)"
