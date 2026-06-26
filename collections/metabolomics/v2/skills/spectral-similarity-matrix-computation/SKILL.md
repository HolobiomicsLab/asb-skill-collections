---
name: spectral-similarity-matrix-computation
description: Use when after preprocessing and filtering mass spectra (peak filtering,
  metadata cleaning) when you need to compare all spectrum pairs within a dataset
  or between a query set and a reference library to identify similar or related spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3373
  tools:
  - matchms
  - Python
  - Spec2Vec
  - MS2DeepScore
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing,
  cleaning, and comparing mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-matrix-computation

## Summary

Compute pairwise similarity scores across preprocessed mass spectra using matchms to generate a structured scores matrix. This skill enables large-scale spectral similarity comparisons essential for identifying spectral relationships and compound matches in untargeted metabolomics workflows.

## When to use

Apply this skill after preprocessing and filtering mass spectra (peak filtering, metadata cleaning) when you need to compare all spectrum pairs within a dataset or between a query set and a reference library to identify similar or related spectra. Use it when your input is a collection of cleaned spectra in mzML, mzXML, msp, MGF, or JSON format and your goal is to generate a pairwise similarity matrix for downstream filtering, clustering, or library matching.

## When NOT to use

- Input spectra have not been preprocessed or peak-filtered—apply preprocessing and cleaning steps first.
- Your goal is to compare individual spectra against a single query rather than generate comprehensive pairwise comparisons; use targeted search instead.
- You require real-time or streaming similarity computation across continuously arriving spectra; this skill assumes a static, complete input dataset.

## Inputs

- preprocessed mass spectra in mzML, mzXML, msp, MGF, or JSON format
- peak-filtered spectra or reference spectral library
- spectrum metadata (compound names, retention times, molecular weights)

## Outputs

- pairwise similarity scores matrix (CSV or pickle format)
- structured matrix with spectrum identifiers as row and column labels
- sparse scores array for large-scale comparisons (optional)

## How to apply

Load preprocessed mass spectra from your input file using matchms's supported file parsers. Select an appropriate pairwise similarity measure—cosine-based scoring for straightforward spectral alignment, molecular fingerprint-based comparisons for structure-informed similarity, or metadata-based assessments for compound property matching. Apply the chosen measure across all spectrum pairs to compute similarity scores, constructing a scores matrix with spectrum identifiers as row and column labels. Store the resulting scores matrix in a structured format (CSV or pickle) with clear row/column indexing to enable downstream analysis. The choice of similarity metric should reflect your research question: use Cosine scores for peak-based spectral matching, fingerprint-based measures when structural information is available, or sparse storage formats when comparing hundreds of thousands of spectra to reduce memory overhead.

## Related tools

- **matchms** (core library for loading preprocessed spectra, applying pairwise similarity measures (Cosine, fingerprint-based, metadata-based), and constructing scores matrices) — https://github.com/matchms/matchms
- **Python** (execution environment for matchms workflows and matrix I/O operations)
- **Spec2Vec** (optional extensible spectrum similarity measure tailored for matchms workflows) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (optional deep learning-based spectrum similarity measure for matchms) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import Spectrum, calculate_scores
from matchms.similarity import CosineGreedy
import pickle

spectra = [Spectrum(...), Spectrum(...), ...]  # preprocessed spectra
similarity_measure = CosineGreedy()
scores = calculate_scores(spectra, spectra, similarity_measure)
with open('similarity_matrix.pickle', 'wb') as f:
    pickle.dump(scores, f)
```

## Evaluation signals

- Scores matrix dimensions match expected spectrum count (n × n for all-vs-all comparison).
- Row and column identifiers are correctly mapped to spectrum identifiers with no missing or duplicate entries.
- Similarity scores fall within expected range (0–1 for normalized measures; check for NaN or infinite values).
- Diagonal values equal 1.0 (perfect self-similarity) for cosine-based metrics; off-diagonal values are symmetric.
- Output file parses without errors in downstream analysis tools; spot-check known high-similarity spectrum pairs to confirm expected ranking.

## Limitations

- Similarity metric selection significantly influences results—cosine-based scores reflect peak overlap while fingerprint-based measures incorporate structural information; choose metric aligned with your research question.
- Memory usage scales quadratically with spectrum count (n²); for hundreds of thousands of spectra, sparse matrix formats are necessary to avoid memory exhaustion.
- Metadata-based assessments depend on data quality and completeness; missing or incorrect metadata can degrade comparison reliability.
- Preprocessing quality directly impacts scores—poor peak filtering or metadata cleaning upstream will propagate into the similarity matrix; validate preprocessing before computing scores.

## Evidence

- [other] matchms applies various pairwise similarity measures for comparing spectra, including common Cosine-related scores among other approaches such as molecular fingerprint-based comparisons and metadata-related assessments: "Matchms applies various pairwise similarity measures for comparing spectra, including common Cosine-related scores among other approaches such as molecular fingerprint-based comparisons and"
- [readme] matchms enables large-scale spectral similarity comparisons: "enabling large-scale spectral similarity comparisons"
- [readme] matchms supports multiple spectral data formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] sparse matrix formats enable comparison of large spectrum sets: "supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra"
- [readme] matchms facilitates reproducible workflows from raw to processed spectra: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
