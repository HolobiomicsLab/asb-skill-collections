---
name: feature-table-alignment-and-integration
description: Use when you have aligned feature tables (CSV format) paired with MS2 spectral data (MGF or mzML files) and need to compare chemodiverse samples with poor feature overlap or strong retention-time shifts across different LC methods or mass spectrometer technologies (e.g., Orbitrap vs. Q-ToF).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
  - Python 3.8+
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Feature-Table Alignment and Integration

## Summary

Integrate aligned feature tables with their corresponding MS2 spectra to construct a MemoMatrix—a sample-by-MS2-fingerprint matrix that enables retention-time-agnostic sample comparison. This skill is essential when MS2 fragmentation patterns, rather than feature overlap, provide the most informative basis for metabolomics sample alignment.

## When to use

Apply this skill when you have aligned feature tables (CSV format) paired with MS2 spectral data (MGF or mzML files) and need to compare chemodiverse samples with poor feature overlap or strong retention-time shifts across different LC methods or mass spectrometer technologies (e.g., Orbitrap vs. Q-ToF). Use it when RT-agnostic sample comparison based on MS2 fragmentation patterns is more appropriate than feature-level alignment.

## When NOT to use

- Input feature table is not yet aligned across samples; perform feature alignment first using appropriate metabolomics tools.
- MS2 spectral data is unavailable or not linked to feature table samples; this method depends entirely on fragmentation patterns.
- Your primary goal is to compare samples based on feature abundance rather than fragmentation diversity; use feature-based distance metrics instead.

## Inputs

- Aligned feature table (CSV format)
- MS2 spectra data (MGF or mzML format)
- Sample metadata or identifiers

## Outputs

- MemoMatrix (sample-by-MS2-fingerprint matrix)
- MS2 fingerprint artifact with peak and neutral loss counts

## How to apply

Load aligned feature tables and corresponding MS2 spectra data files in formats expected by memo-ms (CSV feature tables and MGF/mzML spectral files). Execute the memo_from_aligned function from the memo-ms package to count MS2 peak and neutral loss occurrences across all samples, building an MS2 fingerprint for each sample. The function aggregates the occurrence counts of MS2 peaks and neutral losses (relative to precursor m/z) to generate a sample-by-fingerprint matrix. Validate the resulting MemoMatrix for correct dimensions (samples × unique peaks/losses), correct data types (integer counts), and presence of expected feature and sample identifiers. Compare matrix structure and content against reference outputs from the memo_publication_examples repository to confirm reproducibility and correctness of the alignment.

## Related tools

- **memo-ms** (Executes memo_from_aligned function to count MS2 peaks and neutral losses and construct the MemoMatrix from aligned feature tables and spectral data) — https://github.com/mandelbrot-project/memo
- **matchms** (Core dependency of MEMO for handling and processing MS2 spectra data in various formats (MGF, mzML, mzXML)) — https://github.com/matchms/matchms
- **spec2vec** (Optional dependency of MEMO for advanced spectral similarity scoring and spectral embeddings based on MS2 fragmentation relationships) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Runtime environment for executing memo-ms and associated dependencies)
- **numpy** (Numerical array operations for fingerprint matrix construction and manipulation)
- **scikit-bio** (Biological data structures and distance/similarity calculations for sample comparison)

## Examples

```
from memo_ms import memo_from_aligned; memo_matrix = memo_from_aligned(feature_table='aligned_features.csv', spectra_file='ms2_spectra.mgf')
```

## Evaluation signals

- MemoMatrix dimensions match expected shape: (number of samples, number of unique MS2 peaks + neutral losses detected across all samples)
- All matrix values are non-negative integers representing peak/loss occurrence counts; no NaN or negative values present
- Sample identifiers in matrix columns/rows match input feature table and spectral file sample names without missing or duplicated entries
- Peak and neutral loss counts are consistent: re-running memo_from_aligned on the same inputs produces identical matrix values
- Comparison with reference outputs from memo_publication_examples repository shows structural and content agreement (within expected variance from data differences)

## Limitations

- Requires paired and correctly linked MS2 spectral data; missing or mismatched spectra for samples will result in incomplete or incorrect fingerprints.
- MS2 fragmentation patterns must be sufficiently diverse across samples to enable meaningful comparison; very low-diversity samples may yield uninformative fingerprints.
- Retention time information is intentionally discarded; if RT is critical to your analysis, consider supplementing this method with RT-aware approaches.
- Neutral loss calculation depends on accurate precursor m/z annotation; errors in precursor assignment propagate to incorrect neutral loss counts.
- Performance and memory requirements scale with the number of unique MS2 peaks and neutral losses across the entire sample set; very large spectral datasets may be computationally intensive.

## Evidence

- [readme] MEMO is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their constituents: "**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**) is a method allowing a Retention Time (RT) agnostic alignment"
- [readme] MS2 fingerprints are generated by counting occurrences of MS2 peaks and neutral losses in each sample: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [readme] MEMO suits comparison of chemodiverse samples with poor feature overlap or strong RT shifts across different LC methods and mass spectrometer technologies: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [other] Execute memo_from_aligned function to construct the MemoMatrix from aligned feature tables and MS2 spectra: "Execute the memo_from_aligned function from the memo-ms package to count MS2 peak and neutral loss occurrences across samples and construct the MemoMatrix"
- [other] Validate the MemoMatrix for correct dimensions, data types, and feature/sample identifiers: "Validate the resulting MemoMatrix artifact for correct dimensions, data types, and presence of expected feature and sample identifiers"
- [readme] MEMO is built on matchms and spec2vec packages for handling MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
