---
name: large-scale-spectral-matching
description: Use when you have preprocessed mass spectra (peak-filtered, metadata-cleaned)
  in supported formats (mzML, mzXML, msp, MGF, JSON) and need to compare all-pairs
  or many-to-many spectrum similarity to identify related compounds, build spectral
  libraries, or perform large-scale library searching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - Python
  - Spec2Vec
  - MS2DeepScore
  techniques:
  - LC-MS
  license_tier: open
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

# large-scale-spectral-matching

## Summary

Compute pairwise cosine similarity scores across preprocessed mass spectra using matchms to enable efficient comparison of hundreds of thousands of spectra. This skill applies sparse data structures and optimized similarity measures to construct structured scores matrices suitable for spectral library searching and compound identification.

## When to use

Use this skill when you have preprocessed mass spectra (peak-filtered, metadata-cleaned) in supported formats (mzML, mzXML, msp, MGF, JSON) and need to compare all-pairs or many-to-many spectrum similarity to identify related compounds, build spectral libraries, or perform large-scale library searching without computing or storing all possible pairwise scores.

## When NOT to use

- Raw (unpreprocessed) spectra without prior peak filtering and metadata cleaning
- Single spectrum comparison; use pairwise similarity on two spectra instead
- Spectral data in unsupported formats not listed in matchms documentation

## Inputs

- preprocessed mass spectra (peak-filtered, metadata-cleaned)
- spectral data files (mzML, mzXML, msp, MGF, JSON, metabolomics-USI)
- spectrum identifiers or reference spectral library

## Outputs

- pairwise cosine similarity scores matrix
- sparse scores array (non-null computed values only)
- structured scores output file (CSV or pickle format)
- spectrum identifier labels (rows and columns)

## How to apply

Load preprocessed spectra from an input file using matchms' spectrum import function. Apply the cosine similarity measure (or another pairwise similarity measure such as molecular fingerprint-based or metadata-related assessments) to compute scores between spectrum pairs, leveraging sparse data formats to store only non-null computed values rather than dense matrices. Construct a scores matrix with spectrum identifiers as row and column labels. Optionally use faster similarity measures for initial pre-selection before refinement with more computationally expensive measures. Save the resulting scores matrix to a structured output file (CSV or pickle format). The sparse approach enables comparison of several hundred thousands of spectra without exhausting memory.

## Related tools

- **matchms** (Core library for loading preprocessed spectra, computing pairwise cosine similarity scores, and managing sparse scores matrices) — https://github.com/matchms/matchms
- **Python** (Programming language for implementing matchms workflows and score matrix construction)
- **Spec2Vec** (Optional extended similarity measure for spectrum comparison tailored to matchms) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional extended similarity measure for spectrum comparison tailored to matchms) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import Spectrum
from matchms.importing import load_spectra
from matchms.similarity import CosineGreedy
spectra = list(load_spectra('preprocessed_spectra.mgf'))
scores = [[CosineGreedy().pair(spectra[i], spectra[j]) for j in range(len(spectra))] for i in range(len(spectra))]
```

## Evaluation signals

- Output scores matrix has correct dimensions (number of spectra × number of spectra) with spectrum identifiers as labels
- Cosine similarity scores fall within expected range [0, 1] for valid spectrum pairs
- Sparse format contains only non-null computed values; verify sparsity ratio and memory usage are substantially reduced compared to dense matrix
- Row and column identifiers in output match input spectrum identifiers with no duplicates or missing values
- Output file is properly formatted (valid CSV with headers or readable pickle object) and can be loaded for downstream analysis

## Limitations

- Requires spectra to be preprocessed (peak-filtered and metadata-cleaned) prior to matching; raw spectra will produce poor or invalid similarity scores
- Cosine similarity scores alone may not capture domain-specific spectral relationships; fingerprint-based or metadata assessments may be necessary for compound identification
- Sparse storage format means all-pairs scores are not automatically available; workflow must explicitly compute desired score pairs
- Pipeline class and sparse scores implementation available only in matchms >= 0.18.0; older versions use dense matrix approach with higher memory overhead

## Evidence

- [other] Load preprocessed spectra from input file, apply cosine similarity, construct scores matrix with spectrum identifiers, save to output file: "1. Load preprocessed spectra from the input file (peak-filtered spectra or reference spectral library) using matchms. 2. Apply the cosine similarity measure to compute pairwise scores between all"
- [readme] Multiple pairwise similarity measures including cosine-related scores, fingerprint-based, and metadata assessments: "A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also"
- [readme] Sparse data format handling enables comparison of several hundred thousands of spectra: "Additionally, Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred"
- [readme] Supported spectral data formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] Reproducible workflows for transforming raw data to pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data, and enabling"
