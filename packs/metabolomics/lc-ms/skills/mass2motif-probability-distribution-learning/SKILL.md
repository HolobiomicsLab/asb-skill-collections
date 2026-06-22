---
name: mass2motif-probability-distribution-learning
description: Use when when you have preprocessed MS/MS spectra converted to a bag-of-fragments format (fragments and neutral losses extracted, noise filtered) and you seek to discover recurring fragmentation patterns without prior compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - Python
  - Latent Dirichlet Allocation (LDA)
  - MotifDB
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass2motif-probability-distribution-learning

## Summary

Apply Latent Dirichlet Allocation (LDA) to a bag-of-fragments representation of preprocessed MS/MS spectra to learn topic distributions over fragment ions and neutral losses (Mass2Motifs), thereby inferring the probability that each fragment/loss belongs to each recurring fragmentation pattern. This skill transforms uninterpreted spectral data into interpretable motif-fragment probability tables suitable for structure elucidation and substructure discovery.

## When to use

When you have preprocessed MS/MS spectra converted to a bag-of-fragments format (fragments and neutral losses extracted, noise filtered) and you seek to discover recurring fragmentation patterns without prior compound identification. Apply this skill when you want to learn which fragment and loss combinations co-occur systematically across a spectral dataset, expressed as probability distributions over topics (Mass2Motifs).

## When NOT to use

- Input spectra have not been preprocessed (not converted to bag-of-fragments, neutral losses not extracted, or noise not filtered).
- You already have annotated compound structures and seek only to match spectra to a known library; use spectral similarity or database search instead.
- The spectral dataset is very small (fewer than ~50 spectra); LDA requires sufficient data to estimate stable topic distributions.

## Inputs

- Preprocessed MS/MS spectral corpus in bag-of-fragments format
- Extracted neutral loss list per spectrum
- LDA hyperparameter configuration (alpha, beta, number of topics, iteration count)
- Noise-filtered fragment and loss abundance matrix

## Outputs

- Mass2Motif set (topic-fragment probability distributions in JSON)
- Document-motif loading matrix (spectrum-to-motif probability assignments)
- Optimized pseudo-spectra (filtered fragment lists per motif above probability threshold)
- Convergence likelihood trace (monitoring LDA training)

## How to apply

Load the preprocessed spectral corpus (bag-of-fragments representation with neutral losses extracted and noise filtered) into memory using Python. Configure LDA hyperparameters—alpha (document-topic concentration), beta (topic-word concentration), number of topics/Mass2Motifs (typically determined by prior experimentation or grid search), and iteration count for convergence—from an input parameter configuration file. Apply Latent Dirichlet Allocation via the MS2LDA modeling module to learn topic distributions over fragments/losses and fragment/loss distributions over topics across the full spectral dataset. Execute LDA training for the specified number of iterations, monitoring convergence via likelihood tracking to ensure stable parameter estimates. Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings (spectrum-to-motif probabilities), then serialize both to JSON format. Finally, optimize motif pseudo-spectra by filtering low-probability fragments and losses according to probability thresholds (e.g., retaining only fragments with probability above a cutoff) to produce the final, interpretable Mass2Motif set.

## Related tools

- **MS2LDA** (Probabilistic topic modeling framework that implements LDA for tandem MS/MS data; orchestrates hyperparameter configuration, LDA training, and Mass2Motif extraction.) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Underlying probabilistic model that infers topic (Mass2Motif) distributions over fragments and losses; learns which motifs explain observed fragmentation patterns.)
- **Python** (Programming language for loading spectral data, configuring LDA hyperparameters, executing training, and serializing output to JSON.)
- **MotifDB** (Searchable motif database for post-hoc comparison and annotation of inferred Mass2Motifs; enables validation of learned motifs against known fragmentation patterns.) — https://zenodo.org/records/15688609

## Evaluation signals

- LDA likelihood converges (does not diverge) over iterations, indicating stable parameter estimation.
- Inferred Mass2Motifs exhibit coherent fragment and loss groupings (i.e., fragments within each motif share chemical or structural logic).
- Document-motif loading matrix sums to 1.0 per spectrum (valid probability distribution).
- Probability thresholds for motif optimization filter out low-probability fragments consistently; resulting pseudo-spectra are interpretable and less sparse than raw input.
- Cross-validation or held-out test set likelihood remains stable and comparable to training likelihood (no severe overfitting).

## Limitations

- LDA hyperparameter selection (alpha, beta, number of topics) is often empirical; the article does not prescribe defaults, requiring trial-and-error or grid search.
- Only a fraction of available mass spectrometry information is traditionally utilized; motif interpretation depends on downstream annotation and comparison to MotifDB or manual validation.
- LDA assumes bag-of-fragments exchangeability, which may not capture fragmentation pathway dynamics or ion source dependencies.
- Very small datasets (< 50 spectra) or highly heterogeneous spectral classes may yield unstable or uninformative motifs.

## Evidence

- [other] MS2LDA applies Latent Dirichlet Allocation to infer which motifs are most likely to explain the observed fragmentation patterns in mass spectrometry data.: "MS2LDA applies Latent Dirichlet Allocation to infer which motifs are most likely to explain the observed fragmentation patterns in mass spectrometry data."
- [other] Load the preprocessed spectral corpus (bag-of-fragments representation with neutral losses extracted and noise filtered) into memory using Python. Configure LDA hyperparameters (alpha, beta, number of topics/Mass2Motifs, and iteration count) from the input parameter configuration. Apply Latent Dirichlet Allocation via the MS2LDA modeling module to learn topic distributions over fragments/losses and fragment/loss distributions over topics across the full spectral dataset. Execute LDA training for the specified number of iterations, monitoring convergence via likelihood tracking.: "Load the preprocessed spectral corpus (bag-of-fragments representation with neutral losses extracted and noise filtered) into memory using Python. Configure LDA hyperparameters (alpha, beta, number"
- [other] Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings, then serialize to JSON format. Optimize motif pseudo-spectra by filtering low-probability fragments and losses according to probability thresholds, producing the optimized Mass2Motif set.: "Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings, then serialize to JSON format. Optimize motif pseudo-spectra by filtering low-probability"
- [readme] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
- [readme] Mass spectrometry fragmentation patterns hold abundant structural information vital for analytical chemistry, natural product research, and food safety assessments.: "Mass spectrometry fragmentation patterns hold abundant structural information vital for analytical chemistry, natural product research, and food safety assessments."
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
