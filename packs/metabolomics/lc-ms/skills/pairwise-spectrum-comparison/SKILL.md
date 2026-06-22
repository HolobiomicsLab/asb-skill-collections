---
name: pairwise-spectrum-comparison
description: Use when you have a collection of cleaned mass spectrometry spectra (in mzML, mzXML, msp, MGF, or JSON format) and need to identify spectral similarities, find related compounds, or generate a comprehensive similarity matrix for downstream analysis such as spectral library matching or clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
  - build: coll_comparems2_2_0_cq
    doi: 10.1021/acs.jproteome.2c00457
    title: compareMS2 2.0
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pairwise-spectrum-comparison

## Summary

Compute pairwise similarity scores across a collection of mass spectrometry spectra using Cosine-related measures to generate a scored matrix. This skill enables large-scale spectral comparisons and identification of similar spectra or compounds within a dataset.

## When to use

Apply this skill when you have a collection of cleaned mass spectrometry spectra (in mzML, mzXML, msp, MGF, or JSON format) and need to identify spectral similarities, find related compounds, or generate a comprehensive similarity matrix for downstream analysis such as spectral library matching or clustering.

## When NOT to use

- Input spectra have not yet been cleaned or processed—apply data cleaning and peak filtering first before pairwise comparison.
- You require non-spectral similarity measures (e.g., only metadata-based or molecular fingerprint-based comparisons) without peak-level spectral comparison.
- Raw, uncalibrated spectra in unsupported formats—first convert to mzML, mzXML, msp, MGF, or JSON and apply matchms processing steps.

## Inputs

- Collection of cleaned mass spectrometry spectra (MS/MS)
- Spectral data in supported formats: mzML, mzXML, msp, MGF, or JSON
- Spectrum identifiers (for indexing output matrix)

## Outputs

- Pairwise similarity scores matrix (sparse format, rows and columns indexed by spectrum identifiers)
- Similarity scores (Cosine-related values, typically 0–1 range)
- Pre-selected spectrum pairs above similarity threshold (optional, for downstream workflows)

## How to apply

Load cleaned spectral data using the matchms Python API in a supported format (mzML, mzXML, msp, MGF, JSON). Select an appropriate pairwise similarity measure—most commonly Cosine-related scores, which compare peak m/z values and intensities between spectra pairs. Apply the similarity function across all spectra in the collection to compute pairwise comparisons. Store results in a sparse scores matrix (indexed by spectrum identifiers, with cells containing similarity scores) to optimize memory efficiency, especially for large datasets with hundreds of thousands of spectra. The choice of Cosine-related measures is grounded in their effectiveness for comparing spectral peak patterns and their computational efficiency for initial pre-selection workflows.

## Related tools

- **matchms** (Core library providing pairwise Cosine-related similarity computation, spectrum I/O, and sparse scores matrix generation) — https://github.com/matchms/matchms
- **Python** (Programming language and runtime for executing matchms workflows and custom similarity pipelines)
- **Spec2Vec** (Optional extensible similarity measure tailored for matchms that can complement or replace Cosine-related scores) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional deep-learning-based similarity measure compatible with matchms for advanced spectral comparison) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import calculate_scores
from matchms.similarity import CosineGreedy
scores = calculate_scores(spectra, spectra, CosineGreedy())
# spectra is a list of cleaned Spectrum objects; scores is a sparse scores matrix
```

## Evaluation signals

- Scores matrix dimensions match the number of input spectra (N × N for all-vs-all comparison).
- Similarity scores fall within expected range (0–1 for normalized Cosine measures); diagonal elements (self-similarity) equal or near 1.0.
- Sparse matrix storage format reduces memory footprint compared to dense matrix; only non-null computed scores are retained.
- Spectrum identifiers in matrix rows and columns match input spectrum identifiers and metadata.
- Reproducibility: repeated runs on the same cleaned input spectra produce identical scores (deterministic computation).

## Limitations

- Cosine-related measures compare only peak m/z and intensity patterns; they do not account for differences in metadata, molecular structure, or retention time unless explicitly combined with metadata or fingerprint-based measures.
- Pairwise comparison computational cost scales as O(N²) for N spectra; very large datasets (millions of spectra) may require computational optimization or iterative pre-filtering.
- Sparse scores matrix storage omits zero or null scores; downstream analyses must handle sparse data structures appropriately.
- Similarity scores depend critically on prior spectral cleaning and normalization; poorly cleaned data (e.g., uncalibrated m/z, noisy peaks) will degrade score reliability.

## Evidence

- [other] Matchms applies pairwise Cosine-related similarity measures for comparing extensive amounts of spectra to produce similarity scores across spectral collections.: "Matchms applies pairwise Cosine-related similarity measures for comparing extensive amounts of spectra to produce similarity scores across spectral collections."
- [other] Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API. Apply Cosine-related similarity measure to compute pairwise comparisons across all spectra in the collection using matchms similarity functions. Generate and export scores matrix (rows and columns indexed by spectrum identifiers, cells containing similarity scores).: "Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API. Apply Cosine-related similarity measure to compute pairwise comparisons across all spectra."
- [readme] A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related assessments.: "A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also"
- [readme] Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra.: "supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra."
- [readme] One of the strengths of matchms is its extensibility, allowing users to integrate custom similarity measures. Notable examples of spectrum similarity measures tailored for Matchms include Spec2Vec and MS2DeepScore.: "Notable examples of spectrum similarity measures tailored for Matchms include Spec2Vec and MS2DeepScore."
