---
name: mass-spectrometry-fragmentation-pattern-discovery
description: Use when you have preprocessed MS/MS spectral data (in positive or negative ion mode) and seek to discover recurring fragmentation and neutral-loss patterns that characterize molecular substructures across a dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3174
  tools:
  - MS2LDA
  - Python
  - Conda
  - Latent Dirichlet Allocation (LDA)
  - Spec2Vec
  - MotifDB
  techniques:
  - tandem-MS
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

# mass-spectrometry-fragmentation-pattern-discovery

## Summary

Unsupervised discovery of recurring fragmentation substructures (Mass2Motifs) in tandem MS/MS spectral datasets using Latent Dirichlet Allocation applied to bag-of-fragments representations. This skill enables identification of hidden structural patterns without prior compound identification, accelerating structure elucidation in analytical chemistry and natural product research.

## When to use

Apply this skill when you have preprocessed MS/MS spectral data (in positive or negative ion mode) and seek to discover recurring fragmentation and neutral-loss patterns that characterize molecular substructures across a dataset. Use it when traditional compound-centric approaches have not fully captured structural information in your spectra, or when you aim to annotate unknown spectra by comparing them to motif patterns rather than individual reference compounds.

## When NOT to use

- Spectra have not been preprocessed or converted to bag-of-fragments format — preprocessing and filtering must precede LDA application.
- You have only a small number of spectra (< 50–100) — LDA requires sufficient corpus size to reliably infer topic distributions; sparse datasets may yield unstable or uninformative motifs.
- Your goal is to identify specific known compounds — use spectral library matching or direct compound identification instead; MS2LDA excels at discovering unknown substructures, not matching known reference spectra.

## Inputs

- Preprocessed MS/MS spectral data in bag-of-fragments format
- Spectra with neutral losses extracted and noise filtered
- LDA hyperparameter configuration (JSON or command-line flags)
- Spectral dataset corpus in format suitable for LDA modeling pipeline

## Outputs

- Inferred Mass2Motifs describing recurring fragmentation patterns
- Trained LDA model in binary format
- Spectra-motif loadings (JSON)
- Optimized motif representations (JSON)
- Motif annotations (via MAG/Spec2Vec integration)

## How to apply

Load preprocessed MS/MS spectra that have been converted to bag-of-fragments format with neutral losses extracted and noise filtered. Configure LDA hyperparameters (alpha, beta, number of topics representing Mass2Motifs, iteration count) via command-line flags or JSON parameter file. Apply the MS2LDA modeling module to the processed spectra corpus using Latent Dirichlet Allocation to infer co-occurring fragment and neutral-loss patterns. Execute LDA training iterations, monitoring convergence until completion or iteration threshold. Extract the inferred Mass2Motifs describing recurring fragmentation patterns and serialize the trained model and motif representations to binary and JSON formats. The rationale is that LDA, originally developed for natural language processing, treats each spectrum as a document and mass fragments as words, discovering latent topics (motifs) that best explain the co-occurrence structure of fragments across the dataset.

## Related tools

- **MS2LDA** (Core modeling framework that implements LDA-based topic modeling on bag-of-fragments MS/MS spectra to infer Mass2Motifs) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Probabilistic topic modeling algorithm applied to the preprocessed spectra corpus to discover co-occurring fragment and neutral-loss patterns)
- **Spec2Vec** (Enables automated annotation of discovered Mass2Motifs through spectral embedding and similarity-based annotation guidance (MAG)) — https://zenodo.org/records/15688609
- **MotifDB** (Searchable database of known motifs for comparison and validation of inferred Mass2Motifs)
- **Python** (Programming environment for configuring and executing MS2LDA modeling pipeline)
- **Conda** (Environment management for installing and managing MS2LDA dependencies and execution)

## Examples

```
git clone https://github.com/vdhooftcompmet/MS2LDA.git && cd MS2LDA && python -m ms2lda.cli model --input preprocessed_spectra.json --alpha 0.1 --beta 0.01 --num_topics 50 --iterations 1000 --output_model model.pkl --output_motifs motifs.json
```

## Evaluation signals

- Convergence: LDA training iterations complete or reach specified iteration threshold without numerical instability; log-likelihood or perplexity metrics stabilize across iterations.
- Motif interpretability: Inferred Mass2Motifs exhibit biologically or chemically meaningful co-occurrence of fragments and neutral losses (e.g., motifs corresponding to known functional groups or fragmentation pathways).
- Spectra-motif loadings: Distribution of motif assignments across spectra is non-trivial (i.e., not all spectra dominated by a single motif); loadings sum to 1.0 per spectrum as a probability distribution.
- Reproducibility: Running LDA with fixed random seed and identical hyperparameters reproduces the same motif set and spectra-motif loadings within numerical tolerance.
- Motif annotation rate: Comparison of inferred motifs to MotifDB entries yields successful annotation (via Spec2Vec similarity or direct matching) for a substantial fraction of discovered motifs, increasing confidence in biological relevance.

## Limitations

- LDA requires careful tuning of the number of topics (Mass2Motifs); choosing too few topics conflates distinct fragmentation patterns, while too many topics fragment genuine patterns into uninformative noise. No principled automatic selection method is provided in the documentation.
- The bag-of-fragments representation loses information about fragment intensity and relative ordering within spectra; LDA treats all fragment co-occurrences as equally important regardless of abundance or position in the fragmentation tree.
- Preprocessing quality directly impacts motif discovery; spectra with high noise or incomplete neutral-loss extraction prior to LDA will result in spurious or poorly-defined motifs.
- Small spectral datasets (< 50–100 spectra) may not provide sufficient co-occurrence statistics for LDA to converge to stable, generalizable motifs.
- Motif interpretation relies on domain expertise and external validation (e.g., MotifDB comparison); LDA provides statistical patterns but does not independently verify chemical validity of inferred substructures.

## Evidence

- [other] MS2LDA applies LDA to preprocessed spectra to learn Mass2Motifs that describe recurring fragmentation patterns, operating on spectra converted into a bag-of-fragments format with neutral losses extracted and noise filtered.: "MS2LDA applies LDA to preprocessed spectra to learn Mass2Motifs that describe recurring fragmentation patterns, operating on spectra converted into a bag-of-fragments format with neutral losses"
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
- [methods] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data.: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data."
- [readme] MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs.: "MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs."
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis.: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis."
- [methods] Convert MS/MS spectra into a bag-of-fragments format; Extract neutral losses; Filter out noise; Apply LDA to the processed spectra; Learn Mass2Motifs that describe recurring fragmentation patterns.: "Convert MS/MS spectra into a bag-of-fragments format; Extract neutral losses; Filter out noise; Apply LDA to the processed spectra; Learn Mass2Motifs that describe recurring fragmentation patterns."
- [other] Configure LDA hyperparameters including alpha, beta, number of topics (Mass2Motifs to infer), and iteration count (set via command-line flags or JSON parameter file).: "Configure LDA hyperparameters including alpha, beta, number of topics (Mass2Motifs to infer), and iteration count (set via command-line flags or JSON parameter file)."
