---
name: lda-model-training-convergence
description: Use when you have a preprocessed bag-of-fragments corpus derived from tandem mass spectrometry spectra and need to discover recurring fragmentation motifs without prior compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3372
  tools:
  - MS2LDA
  - Latent Dirichlet Allocation (LDA)
  - Python
  - MS2LDA.modeling
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

# LDA Model Training and Convergence Assessment

## Summary

Train a Latent Dirichlet Allocation model on a bag-of-fragments corpus to infer Mass2Motifs from mass spectrometry fragmentation patterns, then evaluate convergence quality through objective/likelihood metrics across iterations. This skill bridges preprocessing (corpus generation) and downstream annotation by producing a trained model artifact and convergence curve.

## When to use

Apply this skill when you have a preprocessed bag-of-fragments corpus derived from tandem mass spectrometry spectra and need to discover recurring fragmentation motifs without prior compound identification. Use it as the modeling stage after converting MS/MS spectra into fragment/loss pairs and filtering noise, and before attempting motif annotation or visualization.

## When NOT to use

- Input is unprocessed raw MS/MS spectral data (e.g., mzML, mzXML) — apply preprocessing (filtering, neutral loss extraction, fragmentation normalization) first.
- Fragmentation corpus is not in bag-of-fragments format — convert spectra to discrete fragment/neutral-loss pairs before LDA training.
- You require supervised structure assignment with known compound identities — MS2LDA is unsupervised; use it before or in parallel with compound databases.

## Inputs

- bag-of-fragments corpus (preprocessed from MS/MS spectra)
- hyperparameters (alpha, beta, n_motifs, n_iterations)

## Outputs

- trained LDA model (ms2lda.bin, serialized via pickle)
- Mass2Motif set (motifset.json, MS2LDA JSON schema)
- convergence curve plot (convergence_curve.png)

## How to apply

Initialize an LDA model with hyperparameters (alpha, beta) and topic count (n_motifs) tuned to your spectral dataset size. Train the model on the bag-of-fragments corpus for a specified number of iterations (n_iterations), monitoring convergence metrics (LDA objective or log-likelihood) at each step. After training completes, extract the learned topic-fragment associations from the model and serialize both the trained model (as Python pickle, ms2lda.bin) and the discovered Mass2Motif set (as JSON schema, motifset.json). Generate and retain a convergence curve (convergence_curve.png) plotting the objective/likelihood trajectory—this QA artifact documents model stability and informs decisions about iteration count and hyperparameter adequacy.

## Related tools

- **MS2LDA** (Core framework implementing LDA inference on bag-of-fragments corpus to train and serialize the model) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Topic modeling algorithm that infers which motifs best explain observed fragmentation patterns)
- **Python** (Implementation language for model training and serialization via pickle)
- **MS2LDA.modeling** (Module that loads preprocessed corpus and exposes LDA training and convergence APIs) — https://github.com/vdhooftcompmet/MS2LDA

## Evaluation signals

- Convergence curve shows monotonic or smoothly decreasing LDA objective/likelihood across iterations, with no erratic spikes or divergence.
- Trained model file (ms2lda.bin) is present and deserializable via Python pickle; model object contains topic-fragment probability matrices.
- motifset.json conforms to MS2LDA JSON schema and contains mass-to-motif mappings with fragment/neutral-loss probabilities for each inferred motif.
- Number of discovered motifs (Mass2Motifs) is close to the requested n_motifs parameter, indicating successful topic inference.
- Convergence plateaus within n_iterations; if plateau occurs early, model may be undertrained; if still rising sharply at n_iterations, training may be incomplete.

## Limitations

- LDA hyperparameters (alpha, beta, n_motifs) require tuning for each dataset; no universal defaults are provided; poor choices lead to underfitting or overfitting of motif patterns.
- Convergence speed and final model quality depend on corpus size and preprocessing quality (noise filtering, neutral loss extraction); small or poorly filtered corpora may produce uninformative motifs.
- LDA is an unsupervised method and does not assign chemical meaning to discovered motifs; motif interpretation requires downstream annotation (e.g., with MAG/Spec2Vec) and manual validation.
- Training time scales with corpus size and iteration count; large spectral datasets may require extended compute; the article provides no runtime benchmarks.

## Evidence

- [other] Load the preprocessed bag-of-fragments corpus (generated by the Preprocessing module) in the format expected by MS2LDA.modeling. Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs). Train the LDA model on the corpus for the specified number of iterations (n_iterations), recording convergence metrics.: "Load the preprocessed bag-of-fragments corpus (generated by the Preprocessing module) in the format expected by MS2LDA.modeling. 2. Initialize an LDA model with specified hyperparameters (alpha,"
- [other] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns, learning Mass2Motifs that describe recurring fragmentation patterns from processed spectra.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns, learning Mass2Motifs that describe recurring fragmentation patterns"
- [other] Serialize the trained LDA model to ms2lda.bin using Python pickle. Serialize the discovered motifset (Mass2Motifs with fragment/loss probabilities) to motifset.json in the MS2LDA JSON schema. Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact.: "Serialize the trained LDA model to ms2lda.bin using Python pickle. 6. Serialize the discovered motifset (Mass2Motifs with fragment/loss probabilities) to motifset.json in the MS2LDA JSON schema. 7."
- [readme] MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs.: "MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs."
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis.: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis."
