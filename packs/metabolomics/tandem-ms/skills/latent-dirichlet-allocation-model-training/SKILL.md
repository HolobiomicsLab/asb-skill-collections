---
name: latent-dirichlet-allocation-model-training
description: Use when when you have preprocessed MS/MS spectral data (filtered, noise-reduced, with neutral losses extracted) and need to discover recurring fragmentation patterns across a spectral dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3373
  tools:
  - MS2LDA
  - Latent Dirichlet Allocation (LDA)
  - Python
  - Conda
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- ms2lda_runfull.py
- MS2LDA uses **Latent Dirichlet Allocation (LDA)** to infer which motifs are most likely to explain the observed fragmentation patterns.
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- These steps assume you have [Conda](http://conda.io/) installed.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_2_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_2_cq
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

# latent-dirichlet-allocation-model-training

## Summary

Apply Latent Dirichlet Allocation to preprocessed MS/MS spectra in bag-of-fragments format to infer recurring fragmentation and neutral-loss patterns as Mass2Motifs. This unsupervised topic modeling approach discovers hidden substructure motifs without prior compound identification.

## When to use

When you have preprocessed MS/MS spectral data (filtered, noise-reduced, with neutral losses extracted) and need to discover recurring fragmentation patterns across a spectral dataset. Use this skill when you want to identify which fragment and neutral-loss combinations co-occur systematically across spectra, particularly for structure elucidation in natural product research or analytical chemistry where fragmentation mechanisms are not fully characterized.

## When NOT to use

- If spectra have not been preprocessed (converted to bag-of-fragments, noise filtered, neutral losses extracted) — preprocessing must precede this skill.
- If input data is already annotated to known compounds or if compound structure is known — use targeted fragmentation methods instead.
- If the number of spectra is very small (< 50) or dataset is highly homogeneous — LDA requires sufficient diversity and corpus size to learn robust motif distributions.

## Inputs

- Preprocessed MS/MS spectral data in bag-of-fragments format
- Neutral loss matrix (extracted from spectra)
- Noise-filtered peak lists
- LDA hyperparameter configuration (alpha, beta, number of topics, iterations)

## Outputs

- Trained LDA model (binary format)
- Inferred Mass2Motifs (motif representations describing recurring fragmentation patterns)
- Spectra-motif loadings (JSON: probability of each motif in each spectrum)
- Motif-fragment distributions (JSON: probability of each fragment/neutral-loss in each motif)

## How to apply

Load the preprocessed spectra corpus (already converted to bag-of-fragments format with neutral losses extracted and noise filtered) into MS2LDA's modeling module. Configure LDA hyperparameters including alpha (document-topic concentration), beta (topic-word concentration), the number of topics (Mass2Motifs to infer), and iteration count via command-line flags or JSON parameter file. Execute LDA training iterations, monitoring convergence until reaching the iteration threshold or meeting convergence criteria. The algorithm learns which fragment and neutral-loss patterns co-occur across the corpus and assigns each spectrum a probability distribution over inferred motifs. Extract the trained model, serialize to binary format, and export discovered motifs and spectra-motif loadings to JSON. Success is indicated by stable motif representations, interpretable fragment groupings, and spectra-motif loadings that capture meaningful fragmentation diversity.

## Related tools

- **MS2LDA** (Probabilistic topic modeling engine that applies LDA to preprocessed MS/MS spectra to infer Mass2Motifs; handles model training, convergence monitoring, and output serialization) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Underlying Bayesian probabilistic model that learns co-occurring fragment and neutral-loss patterns as topics (Mass2Motifs) from the bag-of-fragments corpus)
- **Python** (Environment and scripting language for configuring LDA hyperparameters and executing MS2LDA training pipeline)
- **Conda** (Environment management system for installing MS2LDA and its dependencies)

## Evaluation signals

- Motif representations are interpretable: each Mass2Motif contains a coherent set of fragment and neutral-loss ions that represent a plausible fragmentation mechanism (e.g., common neutral losses like -18 (H₂O) or -44 (CO₂) grouped with corresponding fragment ions).
- Spectra-motif loading distributions are non-degenerate: most spectra show non-uniform probability distributions across inferred motifs, indicating the model has learned distinguishing patterns rather than trivial uniform assignments.
- Motif counts and hyperparameter choices reflect convergence: training iterations reach stability (log-likelihood plateau) and motif assignments stabilize; no single motif dominates all spectra or remains inactive.
- JSON output schema is valid and complete: all spectra have normalized motif loadings (sum to 1.0), all motifs have normalized fragment/neutral-loss distributions, and binary model can be deserialized without corruption.
- Cross-dataset or known-motif validation: inferred motifs match or overlap with known fragmentation patterns in literature or previously curated motif databases (e.g., MotifDB), confirming biological/chemical validity.

## Limitations

- LDA assumes a bag-of-fragments representation, discarding spectral peak intensity variation and order; mass spectral isotope patterns and fine intensity ratios are not captured.
- Model quality depends critically on hyperparameter choices (alpha, beta, number of topics); no automatic tuning is provided in the workflow — users must perform sensitivity analysis or use heuristics (e.g., Held-out likelihood, perplexity) to select topic count.
- Convergence and motif interpretability are not guaranteed for datasets with insufficient diversity, poor signal-to-noise, or very large numbers of unique fragments; small or contaminated datasets may yield spurious motifs.
- The skill applies only to preprocessed, normalized spectra in bag-of-fragments format; heterogeneous ion modes (positive/negative mixed), unconverted m/z values, or raw peak lists will produce unreliable motifs.

## Evidence

- [other] MS2LDA applies LDA to preprocessed spectra to learn Mass2Motifs that describe recurring fragmentation patterns, operating on spectra converted into a bag-of-fragments format with neutral losses extracted and noise filtered.: "MS2LDA applies LDA to preprocessed spectra to learn Mass2Motifs that describe recurring fragmentation patterns, operating on spectra converted into a bag-of-fragments format with neutral losses"
- [other] Configure LDA hyperparameters including alpha, beta, number of topics (Mass2Motifs to infer), and iteration count (set via command-line flags or JSON parameter file).: "Configure LDA hyperparameters including alpha, beta, number of topics (Mass2Motifs to infer), and iteration count (set via command-line flags or JSON parameter file)."
- [other] Apply Latent Dirichlet Allocation to the processed spectra corpus using MS2LDA's modeling module to learn co-occurring fragment and neutral-loss patterns.: "Apply Latent Dirichlet Allocation to the processed spectra corpus using MS2LDA's modeling module to learn co-occurring fragment and neutral-loss patterns."
- [other] Extract inferred Mass2Motifs describing the recurring fragmentation patterns and generate optimized motif representations.: "Extract inferred Mass2Motifs describing the recurring fragmentation patterns and generate optimized motif representations."
- [other] Serialize the trained LDA model to binary format and export all discovered motifs and spectra-motif loadings to JSON output files.: "Serialize the trained LDA model to binary format and export all discovered motifs and spectra-motif loadings to JSON output files."
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
- [intro] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [methods] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data.: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data."
