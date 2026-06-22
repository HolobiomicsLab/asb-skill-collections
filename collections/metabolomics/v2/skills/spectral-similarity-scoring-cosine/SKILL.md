---
name: spectral-similarity-scoring-cosine
description: Use when you have a collection of preprocessed and cleaned mass spectrometry spectra (in mzML, mzXML, msp, MGF, or JSON format) and need to compute all-pairs or targeted spectral similarity scores to identify related spectra, perform spectral library searches, or build a similarity network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0491
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - matchms
  - Spec2Vec
  - MS2DeepScore
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- matchms is a versatile open-source Python package
- A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_cq
schema_version: 0.2.0
---

# spectral-similarity-scoring-cosine

## Summary

Apply pairwise Cosine-related similarity measures to compute spectral similarity scores across a collection of cleaned mass spectrometry spectra, generating a dense or sparse scores matrix indexed by spectrum identifiers. This skill quantifies spectral relatedness for large-scale spectral comparisons and downstream compound matching or library searching.

## When to use

You have a collection of preprocessed and cleaned mass spectrometry spectra (in mzML, mzXML, msp, MGF, or JSON format) and need to compute all-pairs or targeted spectral similarity scores to identify related spectra, perform spectral library searches, or build a similarity network. Use this skill when you require reproducible, standardized spectral comparison metrics rather than ad-hoc scoring.

## When NOT to use

- Input spectra are already in an intermediate processed state (e.g., already binned, already normalized differently than matchms expects) without re-importing via matchms API — use direct import and cleaning workflow instead.
- You require non-Cosine-based similarity measures (e.g., molecular fingerprint-based, Spec2Vec, MS2DeepScore) — those are separate matchms similarity operations.
- Your goal is metadata-only comparison (e.g., compound name matching or retention time correlation) rather than m/z peak-based similarity — use metadata-related assessment measures instead.

## Inputs

- Collection of cleaned mass spectrometry spectra (mzML, mzXML, msp, MGF, or JSON format)
- Spectrum metadata (compound names, precursor m/z, retention time, if available)
- Optionally, subset or parameters specifying which spectrum pairs to compare

## Outputs

- Pairwise similarity scores matrix (dense or sparse array; rows and columns indexed by spectrum identifiers)
- Spectrum identifier mapping (to link matrix indices back to original spectrum objects)
- Optional: ranked lists of most similar spectra per query spectrum

## How to apply

Load cleaned spectral data using the matchms Python API in a supported format (mzML, mzXML, msp, MGF, JSON). Apply the Cosine-related similarity measure via matchms similarity functions to compute pairwise comparisons across all spectra or a targeted subset. Matchms supports both dense and sparse score matrix outputs; choose sparse representation when comparing hundreds of thousands of spectra to reduce memory footprint. Store results in a scores matrix with rows and columns indexed by spectrum identifiers and cells containing similarity scores (typically ranging 0–1). Validate output by verifying that the scores matrix has consistent dimensions, symmetric structure (if all-pairs), and that similarity scores fall within expected ranges for your spectral data type.

## Related tools

- **matchms** (Core Python package that implements pairwise Cosine-related similarity functions and matrix generation for spectral comparison) — https://github.com/matchms/matchms
- **Python** (Programming language required to invoke matchms API and manage spectral data workflows)
- **Spec2Vec** (Optional: alternative spectrum similarity measure tailored for matchms that can be substituted for Cosine-based scoring) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional: alternative deep-learning spectrum similarity measure tailored for matchms) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import calculate_scores_array; scores = calculate_scores_array(references=spectra_ref, queries=spectra_query, score_function=CosineGreedy())
```

## Evaluation signals

- Scores matrix dimensions match the number of input spectra (square matrix for all-pairs, or rectangular for targeted comparisons)
- All similarity scores fall within the expected range [0, 1] for Cosine-based measures
- Diagonal elements equal 1.0 (or close to 1.0) if all-pairs comparison and spectrum is compared to itself
- Scores matrix is symmetric if all-pairs comparison (scores[i,j] ≈ scores[j,i])
- Spectrum identifier index is preserved and can be mapped back to original spectrum objects to validate identity of top-scoring pairs

## Limitations

- Cosine-based similarity only compares m/z peak intensities and their bin positions; it does not account for structural information or molecular properties unless supplemented with fingerprint-based measures.
- Large-scale comparisons (hundreds of thousands of spectra) require sparse matrix representation; dense representation may exhaust memory.
- Spectral quality and preprocessing (peak filtering, normalization, mass calibration) significantly impact score reliability; scores reflect input data integrity.
- Cosine similarity is symmetric but does not account for missing peaks (absent in one spectrum but present in another) — only shared peaks contribute to the score.
- Score thresholds for declaring spectra 'similar' or 'related' are not provided by matchms and must be determined empirically for your specific application and spectral library.

## Evidence

- [other] Matchms applies pairwise Cosine-related similarity measures for comparing extensive amounts of spectra to produce similarity scores across spectral collections.: "Matchms applies pairwise Cosine-related similarity measures for comparing extensive amounts of spectra to produce similarity scores across spectral collections"
- [other] Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API. Apply Cosine-related similarity measure to compute pairwise comparisons across all spectra in the collection using matchms similarity functions. Generate and export scores matrix (rows and columns indexed by spectrum identifiers, cells containing similarity scores).: "Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API. Apply Cosine-related similarity measure to compute pairwise comparisons across all spectra in"
- [readme] A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related assessments.: "A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also"
- [readme] Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra.: "supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra"
- [readme] Matchms facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data, and enabling large-scale spectral similarity comparisons.: "enabling large-scale spectral similarity comparisons"
