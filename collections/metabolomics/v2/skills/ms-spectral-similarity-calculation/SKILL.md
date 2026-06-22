---
name: ms-spectral-similarity-calculation
description: Use when when comparing two or more MS/MS spectra for compound identification, library matching, or spectral validation. Triggered when raw spectral data requires quantitative similarity assessment before database lookup, or when validating that two spectra originate from the same chemical compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - spectral_similarity
  - MSEntropy
  - SpectralEntropy
  - ms_distance
  - Entropy Search GUI
  - MS Viewer
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
- '.. automodule:: spectral_similarity :members:'
- These are all integrated into the [MSEntropy package
- These are all integrated into the MSEntropy package (https://github.com/YuanyueLi/MSEntropy)
- This repository contains the original source code for the paper
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_entropy_cq
    doi: 10.1038/s41592-021-01331-z
    title: Spectral entropy
  dedup_kept_from: coll_spectral_entropy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01331-z
  all_source_dois:
  - 10.1038/s41592-021-01331-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-spectral-similarity-calculation

## Summary

Compute similarity scores between pairs of preprocessed MS/MS spectra using entropy-based or distance metrics to enable compound identification and spectral library searching. This skill applies a range of 43+ spectral comparison algorithms—with entropy similarity as the primary method—to quantify peak alignment and intensity distribution agreement between two spectra.

## When to use

When comparing two or more MS/MS spectra for compound identification, library matching, or spectral validation. Triggered when raw spectral data requires quantitative similarity assessment before database lookup, or when validating that two spectra originate from the same chemical compound. Most commonly used after spectral noise removal (peaks <1% of max intensity filtered) to ensure peak quality does not confound similarity scores.

## When NOT to use

- Input spectra still contain noise peaks (intensity <1% max) — filter first to avoid spurious similarity artifacts
- Spectra are from different ionization modes or precursor charge states without prior alignment — normalize to same charge/mode
- Similarity score is the only output needed but compound identity confidence thresholds, library hit ranking, or false discovery control are required — this skill alone does not provide those downstream decisions

## Inputs

- MS/MS spectrum pair (preprocessed, noise-filtered: m/z and intensity arrays)
- Spectral metadata (compound identifiers, precursor m/z, collision energy)
- Optional: reference dataset (NIST, MassBank) for validation

## Outputs

- Similarity score (float, range [0, 1])
- Structured output table (spectrum IDs, peak counts, entropy values, similarity metrics)
- Comparison report with element-wise agreement and performance metrics (for validation)

## How to apply

Load two preprocessed MS/MS spectra with noise already removed (peaks below 1% of maximum intensity discarded). Select a similarity metric from the 43+ available algorithms; entropy similarity is recommended for small-molecule compound identification because it outperforms traditional dot-product methods. Apply the chosen similarity function from the spectral_similarity module (or Flash entropy search in MSEntropy for faster performance on large libraries). The function merges peaks within MS2-tolerance to avoid double-counting and computes a normalized similarity score in the range [0, 1]. Validate output by confirming the score falls within [0, 1] and comparing against known reference spectrum pairs to detect implementation errors (e.g., incorrect peak merging). Document similarity score alongside spectrum identifiers, peak counts, and entropy values in a structured output table for downstream analysis or decision-making.

## Related tools

- **MSEntropy** (Core package providing entropy similarity, spectral entropy, and Flash entropy search algorithm for fast MS/MS spectral comparison) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity** (Module within SpectralEntropy/MSEntropy that implements 43+ spectral similarity algorithms including entropy distance and classical metrics) — https://github.com/YuanyueLi/SpectralEntropy
- **ms_distance** (Module providing distance computation utilities for MS spectral comparisons) — https://github.com/YuanyueLi/SpectralEntropy
- **Entropy Search GUI** (Standalone graphical interface for real-time spectral file comparison and library searching using entropy similarity, supports .mgf, .msp, .mzML, .lbm2 formats) — https://github.com/YuanyueLi/EntropySearch
- **MS Viewer** (Web app for visualizing and calculating entropy similarity for two MS/MS spectra in real time) — https://yuanyueli.github.io/MSViewer

## Examples

```
import numpy as np
import ms_entropy as me
peaks_query = np.array([[69.071, 7.917962], [86.066, 1.021589]])
peaks_reference = np.array([[69.071, 9.9], [86.066, 1.5]])
similarity_score = me.spectral_entropy_similarity(peaks_query, peaks_reference)
print(f'Entropy similarity: {similarity_score:.4f}')
```

## Evaluation signals

- Similarity score is within the valid range [0, 1]; scores >1 or <0 indicate peak merging errors or implementation bugs
- Similarity scores for known identical or reference spectrum pairs match published reference output within floating-point tolerance (e.g., ±1e-6)
- Element-wise comparison of similarity matrices from original SpectralEntropy and Flash entropy MSEntropy implementations agrees within floating-point tolerance, confirming algorithmic equivalence
- Wall-clock execution time for Flash entropy search is measurably faster than original implementation (speedup ratio >1) while maintaining numerical accuracy
- Output table contains all required metadata (spectrum identifiers, peak counts, entropy values) with no missing or NaN entries for valid input pairs

## Limitations

- If entropy similarity score exceeds 1.0 in self-implemented code, this indicates errors in peak merging within MS2-tolerance; use provided repository code to avoid
- Similarity metric selection affects compound identification performance; entropy similarity outperforms dot-product for small molecules but may not be optimal for all analyte classes or ionization modes
- Flash entropy search algorithm currently available only in Python; R, C/C++, and JavaScript support is limited to classical entropy similarity without acceleration
- Spectral preprocessing (noise filtering, peak normalization, precursor filtering) is required upstream and not handled by this skill; garbage input produces unreliable similarity scores

## Evidence

- [other] Before calculating spectral similarity, it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed to improve identification performance.: "Before calculating spectral similarity, it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed"
- [other] The SpectralEntropy package integrates entropy similarity as a core function alongside spectral entropy and other analytical functions for MS/MS spectrum comparison.: "The SpectralEntropy package integrates entropy similarity as a core function alongside spectral entropy and other analytical functions for MS/MS spectrum comparison"
- [other] Load two preprocessed MS/MS spectra (with noise removed: peaks <1% of maximum intensity filtered) from input files. Apply the entropy similarity function from the spectral_similarity module to compute the similarity score between the two spectra. Validate that the calculated entropy similarity value is within the expected range [0, 1].: "Load two preprocessed MS/MS spectra (with noise removed: peaks <1% of maximum intensity filtered) from input files. Apply the entropy similarity function from the spectral_similarity module to"
- [other] The MSEntropy package has rewritten the entropy similarity calculation method using the Flash entropy search algorithm, indicating an algorithmic improvement over the original SpectralEntropy implementation.: "The MSEntropy package has rewritten the entropy similarity calculation method using the Flash entropy search algorithm, indicating an algorithmic improvement over the original SpectralEntropy"
- [readme] With the MSEntropy package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising accuracy.: "With the MSEntropy package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising"
- [readme] Please note: If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance. Use the code provided in our repository to avoid this issue.: "If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance. Use the code provided in our repository to"
- [readme] The code in this repository provides 43 different spectral similarity algorithms for MS/MS spectral comparison.: "The code in this repository provides 43 different spectral similarity algorithms for MS/MS spectral comparison"
- [readme] Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification.: "Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification"
