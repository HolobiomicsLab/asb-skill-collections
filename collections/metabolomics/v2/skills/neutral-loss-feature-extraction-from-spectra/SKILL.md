---
name: neutral-loss-feature-extraction-from-spectra
description: Use when you have MS2 spectra data (MGF/mzML format) and aligned feature tables, and your analysis goal is to compare samples that may have poor MS1 feature overlap, strong retention-time shifts across runs, or were acquired on different LC-MS platforms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
  - Python 3.8+
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- conda create --name memo python=3.8
- pip install numpy
- conda install -c conda-forge scikit-bio
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neutral-loss-feature-extraction-from-spectra

## Summary

Extract neutral loss features (mass shifts to precursor ion) from MS2 fragmentation spectra and count their occurrence per sample to generate MS2-based fingerprints for sample comparison. This approach enables retention-time-agnostic alignment of metabolomics samples, particularly suited for chemodiverse datasets with poor feature overlap or strong chromatographic shift.

## When to use

Apply this skill when you have MS2 spectra data (MGF/mzML format) and aligned feature tables, and your analysis goal is to compare samples that may have poor MS1 feature overlap, strong retention-time shifts across runs, or were acquired on different LC-MS platforms. Use it when you need sample-level vectorization independent of chromatographic alignment.

## When NOT to use

- Input spectra are MS1-only (no fragmentation data available)
- Sample comparison goal requires chromatographic alignment (use traditional LC-MS feature alignment instead)
- Spectra have already been processed into pre-computed molecular fingerprints incompatible with neutral loss extraction

## Inputs

- Aligned feature table (CSV format)
- MS2 spectra data (MGF or mzML format)
- Sample metadata (optional, for filtering blanks)

## Outputs

- MemoMatrix (sample × neutral loss count matrix)
- MS2 fingerprint per sample (vector of neutral loss occurrence counts)
- Neutral loss feature annotations (m/z identifiers)

## How to apply

Load aligned feature tables and corresponding MS2 spectra files (MGF or mzML format) into the memo-ms pipeline. For each spectrum, identify neutral losses by computing mass differences between the precursor ion and observed fragment peaks. Count the occurrence frequency of each unique neutral loss (m/z value) across all spectra within a sample. Aggregate these counts into a per-sample MS2 fingerprint vector. Validate the resulting fingerprint matrix for correct dimensions (samples × unique neutral losses), expected data types (integer counts), and presence of sample/feature identifiers. Compare the output matrix structure against reference outputs from the memo_publication_examples repository to confirm reproducibility. The fingerprints can then be used for downstream alignment, filtering (e.g., removing peaks/losses from blank samples), and visualization (MDS/PCoA, TMAP, Heatmap).

## Related tools

- **memo-ms** (Core package implementing neutral loss counting and MemoMatrix generation via memo_from_aligned function) — https://github.com/mandelbrot-project/memo
- **matchms** (Foundation library for importing, processing, and validating MS2 spectra in MGF/mzML/mzXML formats) — https://github.com/matchms/matchms
- **spec2vec** (Complementary spectral similarity measure based on fragment and neutral loss relationships learned via Word2Vec embeddings) — https://github.com/iomega/spec2vec
- **numpy** (Numerical array operations for fingerprint matrix construction and aggregation)
- **scikit-bio** (Statistical and distance metric computations for downstream sample comparison and visualization)
- **Python 3.8+** (Runtime environment; version ≥3.8 required, ≥3.9 preferred for matchms string operations)

## Examples

```
from memo_ms import memo_from_aligned; memo_matrix = memo_from_aligned(feature_table='features_aligned.csv', spectra='spectra.mgf'); print(memo_matrix.shape, memo_matrix.sum(axis=1))
```

## Evaluation signals

- MemoMatrix has correct shape: number of rows = number of samples, number of columns = number of unique neutral losses detected
- All matrix values are non-negative integers representing neutral loss occurrence counts; no NaN or negative counts
- Sample identifiers and neutral loss m/z values are present and match input feature tables and spectra metadata
- Matrix rows (samples) and columns (neutral losses) are labeled; identifiable features and sample names align with source data
- When compared against reference outputs from memo_publication_examples, the fingerprint structure, dimensionality, and distribution of neutral loss counts match expected baseline (up to platform-specific variation in spectral input)

## Limitations

- MS2 spectra must have sufficient depth (number of fragments) to yield informative neutral loss patterns; shallow or low-resolution spectra may produce sparse fingerprints
- Neutral loss extraction assumes accurate precursor m/z and mass calibration; systematic m/z errors propagate into false or merged neutral loss features
- Performance depends on spectral data quality: spectra with high chemical noise, instrument artifacts, or poor signal-to-noise ratio may inflate fingerprint dimensionality and reduce sample discriminability
- Retention-time agnostic alignment benefits samples with strong RT shifts, but does not resolve isomeric compounds or isobars if their MS2 fragmentation patterns are identical
- TMAP visualization (optional downstream step) is available only on macOS and Linux; Windows users require WSL (Windows Subsystem for Linux)

## Evidence

- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [intro] These fingerprints can in a second stage be aligned to compare different samples: "These fingerprints can in a second stage be aligned to compare different samples"
- [intro] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods"
- [intro] a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their consituents: "a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2)"
- [intro] different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap)"
- [readme] MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra: "MEMO is mainly built on `matchms` and `spec2vec` packages for handling the MS2 spectra"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS): "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
