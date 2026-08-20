---
name: memo-ms-api-usage-and-parameter-configuration
description: Use when you have aligned feature tables (CSV format) with corresponding MS2 spectra data (MGF or mzML files), and need to construct a sample-level vectorization matrix where each row represents a sample and columns encode the occurrence counts of MS2 peaks and neutral losses observed in that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MEMO
  - memo-ms
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- '**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**) is a method allowing a Retention Time (RT) agnostic alignment'
- pip install memo-ms
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

# memo-ms API usage and parameter configuration

## Summary

Configure and invoke the memo-ms Python API to generate MS2 fingerprints and MemoMatrix artifacts from aligned feature tables and MS2 spectra. This skill covers environment setup, data format specification, function parameterization, and validation of the resulting matrix structure.

## When to use

You have aligned feature tables (CSV format) with corresponding MS2 spectra data (MGF or mzML files), and need to construct a sample-level vectorization matrix where each row represents a sample and columns encode the occurrence counts of MS2 peaks and neutral losses observed in that sample's constituent spectra.

## When NOT to use

- Input spectra lack MS2 fragmentation data (e.g., MS1-only or low-resolution spectra without peak lists)
- Feature tables are unaligned across samples or lack correspondence to input MS2 files
- Samples have identical or near-identical retention time properties across cohorts (RT-agnostic alignment not needed; use conventional feature matching instead)

## Inputs

- aligned feature table (CSV format with feature IDs and sample columns)
- MS2 spectra file(s) (MGF or mzML format containing fragmentation spectra)
- sample metadata or blank identifiers (for optional filtering)

## Outputs

- MemoMatrix artifact (2D array: samples × MS2 features, with counts of peak and neutral loss occurrences)
- validated feature and sample identifiers mapped to matrix rows/columns

## How to apply

Install memo-ms via pip (pip install memo-ms) into a Python 3.8+ environment with required dependencies (numpy, matchms, spec2vec, scikit-bio). Load aligned feature tables and MS2 spectra files in formats expected by memo-ms (CSV feature tables paired with MGF/mzML spectral files). Execute the memo_from_aligned function from the memo-ms package, specifying the input paths and any filtering parameters (e.g., blank sample identifiers for removal). The function counts MS2 peak and neutral loss occurrences across samples to construct the MemoMatrix. Validate the output by checking matrix dimensions (samples × features), data types (numeric counts), presence of expected sample/feature identifiers, and comparing against reference outputs from memo_publication_examples repository notebooks to confirm reproducibility.

## Related tools

- **memo-ms** (Primary Python package providing memo_from_aligned function and MemoMatrix construction logic) — https://github.com/mandelbrot-project/memo
- **matchms** (MS2 spectra parsing, metadata cleaning, and peak normalization underlying memo-ms) — https://github.com/matchms/matchms
- **spec2vec** (Spectral embedding and fragment relationship learning available for downstream similarity scoring of fingerprints) — https://github.com/iomega/spec2vec
- **numpy** (Numerical array operations for MemoMatrix construction and validation)
- **scikit-bio** (Optional statistical and diversity analysis on fingerprint matrices)

## Examples

```
from memo import memo_from_aligned; memo_matrix = memo_from_aligned(feature_table='features.csv', spectra_files=['spectra.mgf'], blank_samples=['blank_1', 'blank_2'])
```

## Evaluation signals

- MemoMatrix dimensions match the count of input samples (rows) and unique MS2 peaks/losses across all spectra (columns)
- All matrix values are non-negative integers (counts); no NaN or negative entries
- Sample and feature identifiers are present and correctly mapped to matrix axes
- MemoMatrix structure and content match reference outputs from memo_publication_examples repository notebooks when applied to the same dataset
- Blank samples (if filtered) are absent from the output matrix; filtered peak/loss counts reflect removal logic

## Limitations

- Method assumes MS2 fragmentation data quality and completeness; poor-quality or missing spectra will reduce fingerprint discriminative power
- Peak and neutral loss counting is RT-agnostic and does not account for potential isobaric or isomeric ambiguities in MS2 fragmentation patterns
- memo-ms requires Python 3.8+; compatibility with Python < 3.9 requires source code modification (removesuffix workaround noted in changelog); TMAP visualization requires Python > 3.7 on macOS/Linux only
- Filtering logic (e.g., blank sample removal) must be specified correctly; incorrect blank identifiers will fail to remove contaminating peaks
- Large spectral datasets may require substantial memory for MemoMatrix construction and storage

## Evidence

- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [other] MEMO generates MS2 fingerprints by counting the occurrence of MS2 peaks and neutral losses in each sample: "MEMO generates MS2 fingerprints by counting the occurrence of MS2 peaks and neutral losses in each sample, which serve as the basis for sample comparison and alignment"
- [other] Load aligned feature tables and corresponding MS2 spectra data files in formats expected by memo-ms: "Load aligned feature tables and corresponding MS2 spectra data files in formats expected by memo-ms (e.g., CSV feature tables and MGF/mzML spectral files)"
- [other] Execute the memo_from_aligned function to count MS2 peak and neutral loss occurrences: "Execute the memo_from_aligned function from the memo-ms package to count MS2 peak and neutral loss occurrences across samples and construct the MemoMatrix"
- [other] Validate the resulting MemoMatrix artifact for correct dimensions, data types, and presence of expected identifiers: "Validate the resulting MemoMatrix artifact for correct dimensions, data types, and presence of expected feature and sample identifiers"
- [other] Compare matrix structure and content against reference outputs from the memo_publication_examples repository: "Compare matrix structure and content against reference outputs from the memo_publication_examples repository to confirm reproducibility"
- [other] MEMO is mainly built on `matchms` and `spec2vec` packages for handling the MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [readme] Environment creation command specifying Python 3.8: "conda create --name memo python=3.8"
- [other] Python version compatibility note for removesuffix method: "Changed .removesuffix to allow support of python <3.9"
