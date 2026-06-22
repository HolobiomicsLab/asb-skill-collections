---
name: cosine-similarity-scoring-computation
description: Use when when you have imported and filtered mass spectrometry spectral data (from mzML, mzXML, msp, MGF, or JSON formats) and need to identify similar or related spectra within a dataset or against a reference library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
  - Spec2Vec
  - MS2DeepScore
  techniques:
  - tandem-MS
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

# cosine-similarity-scoring-computation

## Summary

Compute pairwise Cosine-related similarity scores between mass spectrometry spectra to quantify spectral resemblance for large-scale spectral comparisons. This skill applies matchms' native Cosine similarity measures to transform spectrum pairs into numerical similarity matrices suitable for library searching, compound identification, and spectral clustering.

## When to use

When you have imported and filtered mass spectrometry spectral data (from mzML, mzXML, msp, MGF, or JSON formats) and need to identify similar or related spectra within a dataset or against a reference library. Use this skill when conducting many-to-many spectral comparisons, particularly when initial rapid pre-selection of candidate matches is required before applying more computationally expensive similarity measures.

## When NOT to use

- Input spectra have not been peak-filtered or cleaned; basic peak filtering must precede similarity computation to ensure accuracy.
- You need metadata-aware or molecular fingerprint-based comparisons; use alternative matchms similarity measures (e.g., metadata assessments or Spec2Vec) instead.
- The similarity metric must incorporate spectral intensity distributions beyond m/z matching; Cosine-related scores depend on aligned peak intensities but may not capture all spectral properties equally.

## Inputs

- Preprocessed mass spectrometry spectral data (Spectrum objects or collections)
- Spectral data in mzML, mzXML, msp, MGF, or JSON format
- Peak-filtered spectral datasets with m/z and intensity values

## Outputs

- Pairwise cosine similarity score matrix (sparse or dense)
- Structured similarity scores in numeric or sparse array format
- Indexed spectrum pair comparisons with computed cosine values

## How to apply

Load preprocessed spectral data from supported formats using matchms import utilities. Apply basic peak filtering to ensure data accuracy and remove noisy or low-intensity peaks. Use matchms' pairwise similarity computation functions to calculate Cosine-related scores across all spectrum pairs (or selected pairs for efficiency). Store results in a sparse matrix format to handle large datasets efficiently. Cosine similarity scores typically range from 0 (no resemblance) to 1 (identical spectra); validate that scores are non-null for computed pairs and null for non-computed pairs. For many-to-many comparisons of hundreds of thousands of spectra, the sparse storage format avoids memory overflow.

## Related tools

- **matchms** (Primary library providing pairwise Cosine similarity measure implementations and spectrum data structures) — https://github.com/matchms/matchms
- **pytest** (Testing framework to validate correctness of similarity computations and ensure reproducibility)
- **Spec2Vec** (Optional extension for enhanced spectrum similarity measures tailored for matchms workflows) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional extension for deep learning-based spectrum similarity measures integrated with matchms) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import calculate_scores_legacy; from matchms.similarity import CosineGreedy; scores = calculate_scores_legacy(spectrum_list, spectrum_list, CosineGreedy())
```

## Evaluation signals

- All computed pairwise scores fall within the valid range [0, 1] for normalized Cosine similarity.
- Similarity matrix sparsity is correct: non-null values appear only for computed spectrum pairs; uncomputed or invalid pairs remain null.
- Diagonal or self-similarity scores (spectrum compared to itself) equal or approach 1.0 after peak normalization.
- Symmetric property holds for undirected comparisons: score(spectrum_A, spectrum_B) ≈ score(spectrum_B, spectrum_A).
- Memory consumption is proportional to the number of computed pairs, not the theoretical maximum (validating sparse storage benefit).

## Limitations

- Cosine similarity depends critically on accurate peak alignment (matching m/z values); misaligned peaks or different mass calibration can reduce score reliability.
- The measure is sensitive to peak intensity normalization; different normalization strategies may yield different similarity scores for the same spectrum pair.
- Large-scale comparisons (hundreds of thousands of spectra) require sparse matrix handling; dense matrix computation is prohibitively memory-intensive.
- Cosine-related scores alone do not incorporate metadata or chemical structure information; supplementary measures may be needed for comprehensive library matching.

## Evidence

- [other] Compute pairwise Cosine-related similarity scores between all spectrum pairs using matchms similarity measures.: "Compute pairwise Cosine-related similarity scores between all spectrum pairs using matchms similarity measures"
- [readme] A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related assessments.: "A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [readme] Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra.: "Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats"
