---
name: similarity-matrix-generation
description: Use when you have a collection of cleaned spectra in supported formats (mzML, mzXML, msp, MGF, JSON) and need to compute all pairwise similarity scores to identify related or duplicate spectra, support spectral library searching, or enable network-based analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - matchms
  - Spec2Vec
  - MS2DeepScore
  techniques:
  - LC-MS
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

# similarity-matrix-generation

## Summary

Generate a pairwise similarity scores matrix from a collection of mass spectrometry spectra using Cosine-related similarity measures. This skill is essential for large-scale spectral comparison workflows where all-against-all similarity relationships must be computed and stored in matrix form for downstream analysis.

## When to use

Apply this skill when you have a collection of cleaned spectra in supported formats (mzML, mzXML, msp, MGF, JSON) and need to compute all pairwise similarity scores to identify related or duplicate spectra, support spectral library searching, or enable network-based analysis. Use it as the intermediate step between data cleaning and similarity-based interpretation (e.g., spectral clustering, compound matching).

## When NOT to use

- Input spectra have not been cleaned or validated — incomplete metadata or unfiltered peaks will produce unreliable similarity scores.
- You need to compare spectra using only molecular fingerprints or metadata attributes rather than peak-based Cosine similarity.
- Your workflow requires real-time or streaming similarity computation rather than batch all-against-all comparison.

## Inputs

- Collection of cleaned spectra in one of: mzML, mzXML, msp, MGF, JSON format
- Spectrum objects with processed metadata and peaks (after cleaning/validation)

## Outputs

- Pairwise similarity scores matrix (dense or sparse format)
- Matrix with spectrum identifiers as row/column indices and cosine similarity scores in cells

## How to apply

Load cleaned spectral data using the matchms Python API, specifying the appropriate file format. Apply the Cosine-related similarity measure through matchms similarity functions to compute pairwise comparisons across all spectra in the collection. Matchms now supports sparse matrix storage (as of version ≥0.18.0) to efficiently handle comparisons of hundreds of thousands of spectra. Export the resulting scores matrix with rows and columns indexed by spectrum identifiers and cells containing numerical similarity scores. Use the Pipeline class for complex workflows, optionally storing results in sparse data formats to reduce memory footprint while preserving all computed similarity relationships.

## Related tools

- **matchms** (Implements Cosine-related pairwise similarity computation, spectral data import/export, and sparse matrix storage for large-scale comparisons) — https://github.com/matchms/matchms
- **Python** (Programming language for loading spectral data, invoking matchms API, and managing similarity matrix workflows)
- **Spec2Vec** (Optional extensible similarity measure for matchms that can augment or replace Cosine-based scoring) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional deep-learning-based similarity measure tailored for matchms spectral comparisons) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import Spectrum; from matchms.importing import load_from_json; from matchms.similarity import CosineGreedy; spectra = load_from_json('spectra.json'); scores = CosineGreedy().matrix(spectra)
```

## Evaluation signals

- Matrix dimensions match the input spectrum count (n×n) and row/column labels match spectrum identifiers.
- All similarity scores fall within [0, 1] range for normalized Cosine similarity.
- Diagonal elements (self-similarity) are 1.0 or very close to 1.0, indicating high self-match.
- Matrix is symmetric (score[i,j] = score[j,i]) if using undirected similarity; asymmetry signals implementation error.
- Sparse matrix format correctly encodes only non-zero or computed values; total stored values << n² for large n confirms memory efficiency.

## Limitations

- Cosine-related similarity measures depend critically on peak alignment and normalization; poorly cleaned spectra yield misleading scores.
- Large-scale comparisons (hundreds of thousands of spectra) require sparse matrix storage and may still be computationally expensive; matchms recommends using faster pre-filtering measures before full similarity computation.
- Metadata-only or fingerprint-based similarity information is not captured by peak-based Cosine scoring; users needing multi-modal similarity must apply additional measures or use extensible interfaces (Spec2Vec, MS2DeepScore).
- The choice of Cosine-related variant (e.g., modified Cosine, neutral loss Cosine) is not specified in the workflow; users must select appropriate variant for their spectral data type and research question.

## Evidence

- [other] Matchms applies pairwise Cosine-related similarity measures for comparing extensive amounts of spectra to produce similarity scores across spectral collections.: "Matchms applies pairwise Cosine-related similarity measures for comparing extensive amounts of spectra to produce similarity scores across spectral collections."
- [other] Load cleaned spectral data using matchms Python API, apply Cosine-related similarity to compute pairwise comparisons, generate and export scores matrix.: "Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API. 2. Apply Cosine-related similarity measure to compute pairwise comparisons across all spectra"
- [readme] Matchms now shifted to sparse handling of scores whereby only computed, non-null values are stored.: "We realized that many matchms-based workflows aim to compare many-to-many spectra whereby not all pairs and scores are equally important... For this reason, we now shifted to a sparse handling of"
- [readme] Matchms supports storing results in sparse data formats, enabling comparison of several hundred thousands of spectra.: "Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred thousands of"
- [readme] The software supports mzML, mzXML, msp, metabolomics-USI, MGF, and JSON formats for spectral data.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] One of the strengths of matchms is its extensibility, allowing users to integrate custom similarity measures.: "One of the strengths of matchms is its extensibility, allowing users to integrate custom similarity measures."
