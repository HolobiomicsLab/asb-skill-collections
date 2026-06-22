---
name: motif-pseudo-spectra-optimization-filtering
description: Use when after LDA has converged and inferred Mass2Motifs from preprocessed mass spectrometry spectral data, when the raw motif-fragment distributions contain noise or low-confidence associations that obscure the dominant fragmentation patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MS2LDA
  - Python
  - MotifDB
  - MAG (Automated Mass2Motif Annotation Guidance)
  - Spec2Vec
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# motif-pseudo-spectra-optimization-filtering

## Summary

Filter and optimize inferred Mass2Motifs (topic-fragment probability distributions) by removing low-probability fragments and neutral losses according to configurable probability thresholds, producing a refined set of interpretable pseudo-spectra suitable for annotation and comparison against reference motif databases.

## When to use

After LDA has converged and inferred Mass2Motifs from preprocessed mass spectrometry spectral data, when the raw motif-fragment distributions contain noise or low-confidence associations that obscure the dominant fragmentation patterns. Use this skill when you need to generate clean pseudo-spectra representations that emphasize the most probable fragments and losses for each motif before downstream annotation or motif database comparison.

## When NOT to use

- The raw LDA motif distributions have not yet converged or likelihood tracking shows ongoing volatility — apply convergence diagnostics first.
- You require per-motif Bayesian posterior credible intervals rather than point-estimate filtering; use proper uncertainty quantification instead.
- The goal is exploratory discovery of ALL fragmentation associations, including rare ones; aggressive thresholding may discard rare but genuine motifs.

## Inputs

- Converged LDA model state (fitted topic-fragment probability matrix and fragment-loss distributions)
- Inferred Mass2Motifs (topic-to-fragment and topic-to-neutral-loss probability distributions)
- Probability threshold parameter (configurable cutoff value, typically 0.01–0.10)

## Outputs

- Optimized Mass2Motif set (filtered pseudo-spectra with low-probability fragments/losses removed)
- Mass2Motif JSON serialization (annotated with fragment masses, losses, and retained probabilities)
- Motif cardinality and coverage metrics (number of fragments/losses per motif post-filtering)

## How to apply

Extract the inferred Mass2Motifs (topic-fragment probability distributions and fragment-loss distributions over topics) from the converged LDA model. Apply configurable probability thresholds to filter fragments and neutral losses below a specified cutoff; this threshold selection should balance specificity (keeping only high-confidence fragments) against sensitivity (retaining motifs with sufficient discriminatory power). Iteratively evaluate threshold values by inspecting the resulting motif cardinality and comparing pseudo-spectra to known reference entries in MotifDB or via annotation tools like MAG+Spec2Vec. Serialize the optimized motif set to JSON format for downstream visualization and validation. The rationale is that topic models infer sparse but noisy distributions; probability thresholding concentrates the motif representation on the most plausible fragmentation signatures, improving interpretability and reducing false-positive structural inferences.

## Related tools

- **MS2LDA** (LDA modeling framework that infers Mass2Motifs; this skill refines its output motif distributions post-convergence) — https://github.com/vdhooftcompmet/MS2LDA
- **MotifDB** (Reference database of known Mass2Motifs; used to validate and annotate optimized pseudo-spectra) — https://zenodo.org/records/15688609
- **MAG (Automated Mass2Motif Annotation Guidance)** (Automated annotation tool that interprets optimized motifs by comparison to MotifDB and structural databases)
- **Spec2Vec** (Spectral embedding and similarity metric used by MAG to match optimized pseudo-spectra against reference motifs)
- **Python** (Programming environment for threshold configuration and JSON serialization of optimized motifs)

## Evaluation signals

- Motif pseudo-spectra cardinality post-filtering is reduced compared to raw LDA output (fewer low-probability fragments retained), confirming threshold application.
- Optimized Mass2Motif JSON schema validates: each motif contains fragment/loss entries with non-zero probabilities above the chosen threshold.
- Filtered pseudo-spectra show improved cosine similarity or Spec2Vec alignment with reference MotifDB entries, indicating sharper motif signatures.
- Manual inspection of a subset of optimized motifs confirms that retained fragments are chemically plausible (e.g., common losses, known neutral eliminations) and noise (singleton or random high-mass fragments) is removed.
- Motif coverage (total % of spectral intensity explained by optimized motifs) does not drop significantly after filtering, indicating that thresholding removed noise rather than true signal.

## Limitations

- Probability threshold selection is empirically driven and data-dependent; no universal optimal threshold is provided in the article. Requires iterative validation or comparison to a curated reference set.
- Filtering may discard rare but genuine motifs if thresholds are set too aggressively; balance between specificity and sensitivity must be determined case-by-case.
- Filtered pseudo-spectra are context-dependent on the input spectral corpus and LDA hyperparameters; the same motif may have different cardinality across experiments with different sample distributions.
- No explicit guidance is provided on whether to filter fragment distributions and neutral-loss distributions with the same threshold; asymmetric thresholding may be needed for different ion modes.

## Evidence

- [other] Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings: "Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings, then serialize to JSON format."
- [other] Optimize motif pseudo-spectra by filtering low-probability fragments and losses: "Optimize motif pseudo-spectra by filtering low-probability fragments and losses according to probability thresholds, producing the optimized Mass2Motif set."
- [other] MS2LDA applies LDA to learn topic distributions over fragments/losses: "Apply Latent Dirichlet Allocation via the MS2LDA modeling module to learn topic distributions over fragments/losses and fragment/loss distributions over topics across the full spectral dataset."
- [methods] Compare motifs to known entries in MotifDB: "Compare motifs to known entries in MotifDB"
- [methods] Automated annotation of M2M using MAG: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [readme] Topic modeling applied to MS/MS fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
