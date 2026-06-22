---
name: fragmentation-motif-learning
description: Use when you have preprocessed mass spectrometry fragmentation data (neutral losses and fragment masses extracted and noise-filtered) and want to discover hidden structural motifs across a spectral dataset in an unsupervised manner.
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
  - Conda
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- Apply LDA to the processed spectra
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-motif-learning

## Summary

Apply Latent Dirichlet Allocation (LDA) to a preprocessed bag-of-fragments corpus to infer Mass2Motifs—recurring fragmentation patterns that explain observed tandem MS fragmentation data without prior compound identification. This skill produces a trained LDA model, motif distributions, and convergence diagnostics.

## When to use

You have preprocessed mass spectrometry fragmentation data (neutral losses and fragment masses extracted and noise-filtered) and want to discover hidden structural motifs across a spectral dataset in an unsupervised manner. Apply this skill when you need to identify which fragmentation patterns co-occur most frequently and assign probabilities to fragment–loss associations within each motif.

## When NOT to use

- Input spectra have not been preprocessed into a bag-of-fragments format (convert and filter first via the Preprocessing module).
- The spectral dataset is very small (< 100 spectra) or highly homogeneous; LDA may not discover meaningful motif variation.
- You already have annotated substructure assignments and seek only to validate them; use Annotation and comparison workflows instead.

## Inputs

- bag-of-fragments corpus (preprocessed MS/MS spectra in MS2LDA-compatible format)
- hyperparameters: alpha (float), beta (float), n_motifs (int), n_iterations (int)

## Outputs

- trained LDA model (ms2lda.bin, Python pickle serialized)
- motifset (JSON, MS2LDA schema with fragment/loss probabilities per motif)
- convergence_curve.png (visualization of LDA objective/likelihood vs. iteration)

## How to apply

Load the bag-of-fragments corpus (output from the Preprocessing module) into MS2LDA.modeling and initialize an LDA model with specified hyperparameters (alpha for document–topic prior, beta for topic–word prior) and a target number of topics (n_motifs). Train the model for a set number of iterations (n_iterations), recording convergence metrics at each step. The LDA inference learns which fragments and neutral losses are most likely to co-occur within each topic. Upon convergence, extract the learned topic–fragment associations (the Mass2Motif distributions) and serialize both the trained model (via Python pickle) and the motif set (as JSON following the MS2LDA schema). Generate a convergence curve (plotting LDA objective or likelihood across iterations) as a quality-assurance artifact to verify that the model has stabilized.

## Related tools

- **MS2LDA** (Framework for LDA-based unsupervised motif discovery; performs model initialization, training, and motif extraction.) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Probabilistic topic model applied to the bag-of-fragments corpus to infer latent motifs.)
- **Python** (Programming language for model training, serialization (pickle), and convergence curve generation.)
- **Conda** (Environment management for MS2LDA installation and dependency resolution.)

## Evaluation signals

- Convergence curve shows monotonic or plateau behavior (no divergence) in LDA objective/likelihood; inspect convergence_curve.png for smooth trend.
- Motifset JSON is valid and conforms to MS2LDA schema; each motif has non-negative fragment and loss probabilities summing to 1 across the vocabulary.
- Trained model file (ms2lda.bin) is loadable and reproducible; re-running with the same random seed produces identical motif assignments.
- Discovered motifs show interpretable chemical patterns (e.g., common neutral losses like 18 Da for water, 44 Da for CO₂) and high between-motif distinctness.
- Number of topics and hyperparameter choices are documented and justified; sensitivity analysis (varying alpha, beta, n_motifs) confirms stability of key motifs.

## Limitations

- LDA convergence and motif quality depend strongly on hyperparameter selection (alpha, beta, n_motifs); no automatic tuning is provided; systematic grid search or cross-validation is recommended.
- Bag-of-fragments representation discards MS/MS spectrum peak ordering and intensity ratios; spurious co-occurrences may inflate weak motifs.
- Training time scales with corpus size and n_iterations; very large datasets (> 100k spectra) may require subsampling or distributed LDA variants.
- Discovered motifs are latent topics without inherent chemical meaning; post-hoc annotation (via MAG, Spec2Vec, or MotifDB comparison) is required for interpretation.

## Evidence

- [other] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns, learning Mass2Motifs that describe recurring fragmentation patterns from processed spectra.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns, learning Mass2Motifs that describe recurring fragmentation patterns"
- [other] 1. Load the preprocessed bag-of-fragments corpus (generated by the Preprocessing module) in the format expected by MS2LDA.modeling. 2. Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs). 3. Train the LDA model on the corpus for the specified number of iterations (n_iterations), recording convergence metrics. 4. Extract the learned Mass2Motif distributions (topic-fragment associations) from the trained model. 5. Serialize the trained LDA model to ms2lda.bin using Python pickle. 6. Serialize the discovered motifset (Mass2Motifs with fragment/loss probabilities) to motifset.json in the MS2LDA JSON schema. 7. Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact.: "Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs). 3. Train the LDA model on the corpus for the specified number of iterations"
- [readme] MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry: "MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry"
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis.: "identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [other] Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact.: "Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact"
