---
name: latent-dirichlet-allocation-topic-inference
description: Use when you have a preprocessed corpus of mass spectrometry spectra converted to bag-of-fragments format (with neutral losses extracted and noise filtered), and you seek to discover recurring fragmentation patterns or substructures that characterize multiple spectra without prior knowledge of the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3520
  tools:
  - Latent Dirichlet Allocation (LDA)
  - MS2LDA
  - Python
  - Spec2Vec
  - MotifDB
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA uses **Latent Dirichlet Allocation (LDA)** to infer which motifs are most likely to explain the observed fragmentation patterns.
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

# Latent Dirichlet Allocation Topic Inference

## Summary

Apply Latent Dirichlet Allocation (LDA) to infer recurring fragment and neutral-loss patterns (Mass2Motifs) from preprocessed mass spectrometry spectral data represented as a bag-of-fragments. This unsupervised topic modeling approach discovers recurring substructures without prior compound identification.

## When to use

Apply this skill when you have a preprocessed corpus of mass spectrometry spectra converted to bag-of-fragments format (with neutral losses extracted and noise filtered), and you seek to discover recurring fragmentation patterns or substructures that characterize multiple spectra without prior knowledge of the underlying compounds. Use it when traditional spectral library matching is insufficient and you need to uncover latent motifs that explain fragmentation variability across a dataset.

## When NOT to use

- Input spectra have not been preprocessed, converted to bag-of-fragments format, or noise-filtered; preprocessing is a prerequisite.
- The goal is to match spectra to a known compound library using spectral similarity; use library search or cosine similarity metrics instead.
- Dataset contains fewer than ~100 spectra; LDA requires sufficient data volume to reliably learn topic distributions and avoid overfitting.

## Inputs

- Preprocessed spectral corpus in bag-of-fragments format
- Extracted neutral losses from MS/MS spectra
- Noise-filtered fragment intensity data
- LDA hyperparameter configuration (alpha, beta, topic count, iteration count)
- Mass spectrometry spectral dataset (MS/MS data)

## Outputs

- Inferred Mass2Motifs (topic-fragment probability distributions)
- Document-motif loadings (topic assignments per spectrum)
- Mass2Motif JSON serialization with fragment probabilities
- Optimized motif pseudo-spectra (filtered by probability thresholds)
- Convergence likelihood trajectory

## How to apply

Load the preprocessed spectral corpus (bag-of-fragments representation with neutral losses and noise filtering applied) into memory. Configure LDA hyperparameters—specifically alpha (document-topic concentration), beta (topic-fragment concentration), the number of topics/Mass2Motifs to infer, and iteration count for convergence—based on your dataset size and domain expectations. Apply Latent Dirichlet Allocation via the MS2LDA module to jointly learn topic distributions over fragments/losses and fragment/loss distributions over topics across the full spectral dataset. Execute LDA training for the specified iteration count, monitoring convergence via likelihood tracking to ensure stable topic assignments. Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings, then serialize to JSON. Optimize motif pseudo-spectra by filtering low-probability fragments and losses according to probability thresholds, producing a refined Mass2Motif set suitable for downstream annotation and interpretation.

## Related tools

- **MS2LDA** (Primary implementation module for applying LDA to MS/MS spectra; orchestrates preprocessing, LDA model training, and Mass2Motif extraction.) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Core probabilistic topic modeling algorithm; infers latent topic (Mass2Motif) distributions over fragments and neutral losses.)
- **Spec2Vec** (Downstream tool for automated annotation of discovered Mass2Motifs (MAG); used after LDA inference to assign structural meaning.)
- **MotifDB** (Searchable database for comparing inferred Mass2Motifs to known entries; enables validation and interpretation of discovered motifs.)
- **Python** (Programming environment for configuring LDA hyperparameters, loading spectral data, and serializing outputs.)

## Examples

```
from ms2lda import MS2LDA; model = MS2LDA(n_topics=50, alpha=0.1, beta=0.01, iterations=1000); model.fit(bag_of_fragments_corpus); motifs_json = model.export_motifs(probability_threshold=0.01)
```

## Evaluation signals

- LDA likelihood monotonically increases (or plateaus) across iterations, indicating convergence; no divergence or NaN values in log-likelihood trajectory.
- Inferred Mass2Motifs contain coherent sets of fragment m/z values and neutral losses with meaningful probability distributions (e.g., non-uniform, interpretable peaks).
- Document-motif loadings show sparse, interpretable topic assignments; no motif is equally probable across all spectra (would indicate failed model).
- Optimized motif pseudo-spectra after probability thresholding retain 5–20 dominant fragments per motif; filtered motifs are reproducible across re-runs with the same hyperparameters.
- JSON output schema is valid and contains all required fields: motif identifiers, fragment probabilities, neutral-loss probabilities, and per-spectrum topic loadings.

## Limitations

- LDA hyperparameter selection (alpha, beta, topic count) is dataset-dependent and requires tuning or held-out validation; no automatic defaults guarantee optimal motif discovery.
- Convergence speed and solution quality depend on data preprocessing quality; noise filtering and neutral-loss extraction must be accurate to avoid spurious motifs.
- LDA assumes a fixed number of topics upfront; discovering the optimal number of Mass2Motifs typically requires multiple runs or model selection criteria (e.g., perplexity, coherence).
- Inferred motifs are probabilistic abstractions and may not correspond directly to known chemical structures without downstream validation via Spec2Vec or MotifDB annotation.
- Computational cost scales with dataset size (number of spectra, unique fragments) and iteration count; large datasets may require distributed LDA or subsampling.

## Evidence

- [other] LDA hyperparameters (alpha, beta, number of topics/Mass2Motifs, and iteration count): "Configure LDA hyperparameters (alpha, beta, number of topics/Mass2Motifs, and iteration count) from the input parameter configuration."
- [other] LDA application to MS/MS data for motif inference: "Apply Latent Dirichlet Allocation via the MS2LDA modeling module to learn topic distributions over fragments/losses and fragment/loss distributions over topics across the full spectral dataset."
- [other] Convergence monitoring via likelihood tracking: "Execute LDA training for the specified number of iterations, monitoring convergence via likelihood tracking."
- [other] Mass2Motif extraction and serialization: "Extract inferred Mass2Motifs (topic-fragment probability distributions) and document-motif loadings, then serialize to JSON format."
- [other] Optimization via probability thresholding: "Optimize motif pseudo-spectra by filtering low-probability fragments and losses according to probability thresholds, producing the optimized Mass2Motif set."
- [readme] MS2LDA unsupervised substructure discovery rationale: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [readme] LDA application to tandem MS data: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
