---
name: probabilistic-topic-modeling-mass-spectrometry
description: Use when you have preprocessed tandem mass spectrometry spectra converted into a bag-of-fragments representation (with fragments and neutral losses extracted and noise filtered) and your goal is to discover recurring fragmentation patterns or substructures across a large spectral dataset without.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - Latent Dirichlet Allocation (LDA)
  - Python
  - Spec2Vec
derived_from:
- doi: 10.1093/bioinformatics/btx582
  title: ms2lda
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- Apply LDA to the processed spectra
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1093/bioinformatics/btx582
    title: ms2lda
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# Probabilistic Topic Modeling for Mass Spectrometry

## Summary

Apply Latent Dirichlet Allocation (LDA) to a bag-of-fragments corpus derived from tandem mass spectrometry data to infer Mass2Motifs—recurring fragmentation patterns that represent latent substructures without prior compound identification. This unsupervised approach learns topic-fragment associations that reveal structural motifs hidden across spectral datasets.

## When to use

Use this skill when you have preprocessed tandem mass spectrometry spectra converted into a bag-of-fragments representation (with fragments and neutral losses extracted and noise filtered) and your goal is to discover recurring fragmentation patterns or substructures across a large spectral dataset without relying on spectral library matching or compound annotation. Appropriate when you want to accelerate structure elucidation by identifying common fragmentation signatures that span multiple spectra.

## When NOT to use

- Input spectra have not been preprocessed, filtered for noise, or converted to bag-of-fragments format; LDA requires clean, featurized input.
- Your goal is to identify and annotate a single unknown compound's structure—LDA discovers population-level motifs, not individual compound structures.
- You have access to a comprehensive spectral library with high-confidence matches; library matching or reference-based methods are more direct.

## Inputs

- bag-of-fragments corpus (processed MS/MS spectra with fragments and neutral losses extracted)
- corpus format compatible with MS2LDA.modeling (e.g., preprocessed feature matrix or document-term representation)
- hyperparameter specification: alpha (topic Dirichlet prior), beta (vocabulary Dirichlet prior), n_motifs (number of topics), n_iterations (training iterations)

## Outputs

- trained LDA model artifact (serialized as ms2lda.bin via Python pickle)
- motifset JSON (MS2LDA JSON schema format encoding Mass2Motifs with fragment/loss probabilities and per-motif feature distributions)
- convergence curve visualization (convergence_curve.png showing LDA objective or likelihood across iterations as QA artifact)

## How to apply

Load the preprocessed bag-of-fragments corpus in the format expected by MS2LDA.modeling, then initialize an LDA model by specifying hyperparameters (alpha, beta controlling topic sparsity and vocabulary sparsity) and the desired number of topics (n_motifs). Train the LDA model on the corpus for a specified number of iterations (n_iterations), monitoring convergence metrics (objective or likelihood); continue training until convergence stabilizes. Extract the learned Mass2Motif distributions (topic-fragment and topic-neutral-loss associations) from the trained model. The quality of inferred motifs depends on appropriate choice of n_motifs (guided by domain knowledge or validation) and sufficient training iterations to achieve convergence; inspect the convergence curve to confirm LDA has learned stable topic structures.

## Related tools

- **MS2LDA** (Core framework implementing LDA training, model serialization, and Mass2Motif extraction on MS/MS fragmentation data) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Probabilistic generative model that infers latent topic-fragment associations from the bag-of-fragments corpus)
- **Python** (Programming language and execution environment for MS2LDA model training and serialization)
- **Spec2Vec** (Post-hoc annotation tool that can leverage LDA-discovered motifs for automated Mass2Motif annotation and validation) — https://zenodo.org/records/15688609

## Evaluation signals

- Convergence curve shows monotonic or quasi-monotonic improvement in LDA objective/likelihood over iterations, stabilizing before final iteration.
- Learned Mass2Motif JSON is well-formed (valid schema) and contains non-zero fragment/loss probability distributions across all inferred topics.
- motifset.json contains n_motifs distinct topics, each with interpretable fragment and neutral loss features (e.g., common losses like H2O, CO2 appearing with elevated probability in relevant motifs).
- Trained model (ms2lda.bin) is serializable via Python pickle and can be deserialized without errors for downstream annotation or visualization tasks.
- Per-motif feature counts and distributions are interpretable (no topics with uniform or degenerate probability distributions; topics show clear fragmentation pattern signatures).

## Limitations

- LDA assumes bag-of-fragments independence; the order and context of fragments in the original spectrum hierarchy are lost.
- Model quality is sensitive to choice of n_motifs; too few topics risk over-generalization, too many risk fragmentation and interpretability loss. Optimal n_motifs often requires prior domain knowledge or validation.
- Convergence can be slow on large corpora; training time scales with corpus size and n_iterations. Early stopping or sampling-based approximations may be necessary for very large datasets.
- Mass2Motifs are inferred without semantic labels; downstream annotation (e.g., via MAG or Spec2Vec) is required to assign biological or chemical meaning to discovered motifs.
- The method assumes the bag-of-fragments representation captures relevant structural variation; poor preprocessing (e.g., incomplete noise filtering, inconsistent fragment extraction) will propagate into learned motifs.

## Evidence

- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns"
- [methods] Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs). Train the LDA model on the corpus for the specified number of iterations (n_iterations), recording convergence metrics.: "Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs). Train the LDA model on the corpus for the specified number of iterations"
- [methods] Extract the learned Mass2Motif distributions (topic-fragment associations) from the trained model.: "Extract the learned Mass2Motif distributions (topic-fragment associations) from the trained model."
- [methods] Serialize the trained LDA model to ms2lda.bin using Python pickle. Serialize the discovered motifset (Mass2Motifs with fragment/loss probabilities) to motifset.json in the MS2LDA JSON schema.: "Serialize the trained LDA model to ms2lda.bin using Python pickle. Serialize the discovered motifset (Mass2Motifs with fragment/loss probabilities) to motifset.json in the MS2LDA JSON schema."
- [methods] Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact.: "Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact."
- [readme] MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling: "MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling"
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
