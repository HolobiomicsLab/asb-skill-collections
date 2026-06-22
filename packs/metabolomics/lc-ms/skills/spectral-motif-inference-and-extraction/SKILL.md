---
name: spectral-motif-inference-and-extraction
description: Use when you have preprocessed MS/MS spectral data (converted to bag-of-fragments format with neutral losses extracted and noise filtered) and seek to identify recurring fragmentation patterns indicative of molecular substructures across a spectral cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MS2LDA
  - Python
  - Conda
  - Latent Dirichlet Allocation (LDA)
  - Spec2Vec
  - MotifDB
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- ms2lda_runfull.py
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- These steps assume you have [Conda](http://conda.io/) installed.
- You can install MS2LDA using pip, Conda, or Poet
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

# spectral-motif-inference-and-extraction

## Summary

Apply Latent Dirichlet Allocation (LDA) to preprocessed MS/MS spectra in bag-of-fragments format to infer recurring fragmentation and neutral-loss patterns (Mass2Motifs) that describe molecular substructures without prior compound identification. This unsupervised topic modeling approach discovers hidden structural motifs across spectral datasets for structure elucidation and annotation.

## When to use

You have preprocessed MS/MS spectral data (converted to bag-of-fragments format with neutral losses extracted and noise filtered) and seek to identify recurring fragmentation patterns indicative of molecular substructures across a spectral cohort. Use this skill when prior compound identification is unavailable or when you wish to discover unannotated structural motifs that co-occur across spectra.

## When NOT to use

- Input spectral data has not been preprocessed into bag-of-fragments format or contains unfiltered noise; LDA requires clean, standardized input.
- Your goal is to identify known compounds or annotate spectra against reference libraries; use spectral library matching or molecular networking instead.
- Spectral dataset is very small (< 50 spectra); LDA requires sufficient data to reliably infer topic distributions; smaller cohorts risk overfitting and unstable motif inference.

## Inputs

- Preprocessed MS/MS spectral data in bag-of-fragments format (fragments and neutral losses extracted, noise filtered)
- LDA hyperparameters (alpha, beta, number of topics/Mass2Motifs, iteration count)

## Outputs

- Inferred Mass2Motifs (each represented as a probability distribution over fragments and neutral losses)
- Spectra-motif loadings (topic assignments per spectrum in JSON format)
- Trained LDA model (binary serialized format)
- Motif metadata and visualization-ready exports

## How to apply

Load the preprocessed spectral corpus (in bag-of-fragments format) into MS2LDA's modeling pipeline and configure LDA hyperparameters: set alpha (Dirichlet prior for document-topic distribution), beta (prior for topic-word distribution), the number of topics (Mass2Motifs to infer), and iteration count via command-line flags or JSON parameter file. Execute LDA training to learn co-occurring fragment and neutral-loss patterns; monitor convergence until completion or iteration threshold is reached. Extract the inferred Mass2Motifs—each representing a recurring fragmentation pattern characterized by a probability distribution over fragments and neutral losses—and export motif representations and spectra-motif loadings (fractional topic assignments per spectrum) to JSON output. Validation: verify that discovered motifs show interpretable fragment compositions consistent with known fragmentation rules, that spectra-motif loadings reflect meaningful stratification across the dataset, and that motif stability is confirmed across multiple LDA runs with identical hyperparameters.

## Related tools

- **MS2LDA** (Primary modeling pipeline for applying LDA to MS/MS spectra and inferring Mass2Motifs) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Probabilistic topic modeling algorithm that learns recurring fragment and neutral-loss co-occurrence patterns from the spectral corpus)
- **Python** (Runtime environment for configuring and executing the MS2LDA modeling pipeline)
- **Conda** (Environment manager for installing MS2LDA and managing Python dependencies)
- **Spec2Vec** (Downstream tool for automated annotation guidance (MAG) of inferred Mass2Motifs using spectral embeddings) — https://zenodo.org/records/15688609
- **MotifDB** (Searchable database and repository for comparing inferred motifs to known entries and assigning substructure meaning)

## Evaluation signals

- Each inferred Mass2Motif exhibits a coherent probability distribution over fragments and neutral losses that is interpretable in terms of known fragmentation chemistry (e.g., motifs corresponding to characteristic losses like water, ammonia, or CO₂).
- Spectra-motif loadings show non-random, interpretable stratification: spectra expected to share structural features exhibit high co-occurrence on the same motifs; conversely, structurally diverse spectra show distinct motif signatures.
- Motif stability is confirmed: re-running LDA with identical hyperparameters on the same spectral corpus yields motifs with high similarity (e.g., Jaccard overlap, cosine similarity between fragment distributions > 0.8) across independent runs.
- Convergence is monitored: log-likelihood or perplexity plateaus by the final iteration, indicating the model has learned a stable representation.
- Cross-validation or held-out test spectra show reasonable motif assignments: spectra with known structural annotations or external validation map to motifs consistent with their chemical profiles.

## Limitations

- LDA assumes a bag-of-fragments representation and does not preserve peak intensity ordering or fine-grained m/z neighborhood structure; very similar fragments differing only in exact mass may be conflated.
- Hyperparameter selection (number of topics, alpha, beta) is not data-driven in the workflow; suboptimal choices can result in underfitting (too few motifs, generic patterns) or overfitting (too many motifs, fragmentation noise captured as real patterns). Cross-validation or domain expertise is required.
- Motif interpretability depends on the quality of preprocessing: if neutral losses are incorrectly extracted or noise filtering removes genuine low-intensity peaks, inferred motifs may be chemically implausible or miss rare fragmentation pathways.
- LDA is unsupervised and provides no direct link to chemical structure or molecular function; automated annotation via Spec2Vec or manual curation is necessary to assign biological or structural meaning to discovered motifs.
- Performance scales with dataset size: very large spectral collections (> 1 million spectra) may require distributed LDA implementations or sampling strategies not detailed in this workflow.

## Evidence

- [other] MS2LDA applies LDA to preprocessed spectra to learn Mass2Motifs that describe recurring fragmentation patterns, operating on spectra converted into a bag-of-fragments format with neutral losses extracted and noise filtered.: "MS2LDA applies LDA to preprocessed spectra to learn Mass2Motifs that describe recurring fragmentation patterns, operating on spectra converted into a bag-of-fragments format with neutral losses"
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
- [other] Load preprocessed MS/MS spectral data in bag-of-fragments format (with neutral losses and noise already filtered) into the MS2LDA modeling pipeline. 2. Configure LDA hyperparameters including alpha, beta, number of topics (Mass2Motifs to infer), and iteration count (set via command-line flags or JSON parameter file). 3. Apply Latent Dirichlet Allocation to the processed spectra corpus using MS2LDA's modeling module to learn co-occurring fragment and neutral-loss patterns.: "Load preprocessed MS/MS spectral data in bag-of-fragments format (with neutral losses and noise already filtered) into the MS2LDA modeling pipeline. 2. Configure LDA hyperparameters including alpha,"
- [other] Extract inferred Mass2Motifs describing the recurring fragmentation patterns and generate optimized motif representations. 6. Serialize the trained LDA model to binary format and export all discovered motifs and spectra-motif loadings to JSON output files.: "Extract inferred Mass2Motifs describing the recurring fragmentation patterns and generate optimized motif representations. 6. Serialize the trained LDA model to binary format and export all"
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [readme] MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs.: "MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs."
