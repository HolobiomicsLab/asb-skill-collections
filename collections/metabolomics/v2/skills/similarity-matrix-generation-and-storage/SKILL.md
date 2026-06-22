---
name: similarity-matrix-generation-and-storage
description: Use when when you have cleaned and filtered mass spectrometry spectral data (in mzML, mzXML, msp, MGF, or JSON format) and need to identify or rank spectra by similarity for library matching, metabolite annotation, or network analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3809
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pytest
  - matchms
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# similarity-matrix-generation-and-storage

## Summary

Compute pairwise cosine-based spectral similarity scores across multiple mass spectrometry spectra and store results in sparse matrix formats to enable efficient large-scale comparison. This skill bridges data preprocessing and downstream spectral matching workflows.

## When to use

When you have cleaned and filtered mass spectrometry spectral data (in mzML, mzXML, msp, MGF, or JSON format) and need to identify or rank spectra by similarity for library matching, metabolite annotation, or network analysis. Use this skill specifically when comparing many-to-many spectrum pairs and memory efficiency is a concern (e.g., several hundred thousands of spectra).

## When NOT to use

- Input spectra have not been filtered for data accuracy and integrity (apply basic peak filtering first).
- You need similarity scores for only a small number of spectrum pairs (<100); dense matrix storage is acceptable and simpler.
- Your workflow requires non-cosine similarity measures (e.g., molecular fingerprint-based comparisons, metadata-related assessments); use alternative matchms similarity measures instead.

## Inputs

- Mass spectrometry spectral data in supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON)
- Preprocessed Spectrum objects with cleaned metadata and filtered peaks
- Spectrum collection or list with multiple spectra ready for pairwise comparison

## Outputs

- Sparse similarity score matrix (pairwise cosine-based scores)
- Structured output file containing similarity scores between all spectrum pairs
- Index mapping (spectrum identifiers to matrix row/column positions)

## How to apply

Load preprocessed spectral data using matchms import utilities, then apply pairwise Cosine-related similarity measures between all spectrum pairs using matchms' built-in similarity functions. Store the resulting similarity scores in sparse data formats to avoid storing zero or null values, which dramatically reduces memory overhead for large datasets. The sparse approach is especially valuable when not all scores are equally important—such as when searching for similar compounds or performing initial pre-selection. Verify that the similarity scores fall within expected ranges (typically 0 to 1 for cosine-based measures) and that the matrix dimensions match the input spectrum count.

## Related tools

- **matchms** (Provides pairwise similarity computation functions, spectral data import/export, and sparse matrix handling for mass spectrometry data) — https://github.com/matchms/matchms
- **Python** (Primary programming language for implementing the similarity computation workflow using matchms API)
- **pytest** (Testing framework to verify that similarity computation results are correct and consistent)

## Evaluation signals

- Similarity scores fall within valid range (0–1 for cosine-based similarity measures)
- Output matrix dimensions equal N×N where N is the number of input spectra
- Sparse matrix storage size is significantly smaller than dense equivalent (verify memory reduction)
- Diagonal elements (self-similarity) equal or approach 1.0 for identical spectra
- Matrix is symmetric: score(spectrum_i, spectrum_j) ≈ score(spectrum_j, spectrum_i) for cosine measures
- No NaN or infinite values in computed scores (except where expected from data quality issues)

## Limitations

- Similarity computation scales quadratically with spectrum count; comparing several hundred thousand spectra requires substantial computation time even with sparse storage.
- Cosine-based measures are sensitive to peak intensity normalization; inconsistent preprocessing can produce unreliable scores.
- Sparse matrix format does not store zero scores; if zero scores are meaningful for downstream analysis, dense storage or explicit zero indexing may be needed.
- The method assumes spectra are pre-filtered and cleaned; poor data quality upstream leads to uninformative or misleading similarity scores.

## Evidence

- [other] Load spectral data from supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import utilities. Apply basic peak filtering to ensure data accuracy and integrity. Compute pairwise Cosine-related similarity scores between all spectrum pairs using matchms similarity measures. Store the resulting similarity score matrix in a structured output format.: "Load spectral data from supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import utilities. 2. Apply basic peak filtering to ensure data accuracy and integrity. 3. Compute pairwise"
- [readme] A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related assessments.: "A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also"
- [readme] Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra.: "supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra"
- [readme] We realized that many matchms-based workflows aim to compare many-to-many spectra whereby not all pairs and scores are equally important. Often, for instance, it will be about searching similar or related spectra/compounds. This also means that often not all scores need to be stored (or computed). For this reason, we now shifted to a sparse handling of scores in matchms (that means: only storing actually computed, non-null values).: "many matchms-based workflows aim to compare many-to-many spectra whereby not all pairs and scores are equally important. Often, for instance, it will be about searching similar or related"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS). It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data, and enabling large-scale spectral similarity comparisons.: "enabling large-scale spectral similarity comparisons"
