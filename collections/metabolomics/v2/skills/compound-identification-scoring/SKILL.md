---
name: compound-identification-scoring
description: Use when you have preprocessed MS/MS spectra (noise-filtered, normalized) and need to compute pairwise similarity or distance scores for compound library matching, when your goal is to rank candidate compounds by spectral match quality and maximize correct identification rate above dot-product.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2929
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSEntropy
  - SpectralEntropy
  - spectral_similarity
  - ms_distance
  - Entropy Search GUI
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
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

# Compound-identification-scoring

## Summary

Score MS/MS spectral pairs using entropy similarity or alternative distance metrics to rank and identify small-molecule compounds against reference databases. This skill replaces traditional dot-product similarity with entropy-based metrics that capture spectral complexity and achieve higher identification accuracy.

## When to use

You have preprocessed MS/MS spectra (noise-filtered, normalized) and need to compute pairwise similarity or distance scores for compound library matching, when your goal is to rank candidate compounds by spectral match quality and maximize correct identification rate above dot-product baselines.

## When NOT to use

- Input spectra have not been noise-filtered or peak-normalized — apply preprocessing first
- Reference database is very small (< 100 spectra) — entropy metrics require sufficient statistical signal; dot-product may suffice for toy datasets
- You need real-time single-spectrum search on a massive library without GPU acceleration — Flash entropy search is Python-only; C/C++ or JavaScript implementations do not yet include the Flash algorithm

## Inputs

- MS/MS spectral pairs (m/z–intensity tuples) from query and reference spectra
- Annotated compound reference dataset (NIST, MassBank, or similar; .mgf, .msp, .mzML formats supported)
- Spectral noise threshold parameter (intensity cutoff, typically 1% of max)

## Outputs

- Similarity or distance score matrix (pairwise scores between query and reference spectra)
- Ranked compound candidate list (compounds ordered by descending similarity or ascending distance)
- Performance comparison table (identification accuracy, speedup ratio, numerical agreement with baseline)

## How to apply

Load spectral pairs from a reference dataset (e.g., NIST, MassBank) where compounds are annotated. Preprocess spectra by removing peaks with intensity less than 1% of maximum intensity to reduce noise. Compute similarity scores using the entropy similarity metric (or an alternative from the 43 supported distance algorithms) via the MSEntropy or SpectralEntropy package. For large-scale searches, use the Flash entropy search algorithm in MSEntropy to accelerate computation without loss of accuracy. Compare output scores element-wise against baseline methods (dot product, Euclidean distance) to validate that entropy similarity achieves superior ranking performance. Tabulate identification accuracy (true positives ranked above false positives) and execution time to quantify improvement.

## Related tools

- **MSEntropy** (Primary package providing entropy similarity computation and Flash entropy search algorithm; recommended for production use with speed optimizations) — https://github.com/YuanyueLi/MSEntropy
- **SpectralEntropy** (Original reference implementation containing spectral_similarity, math_distance, and ms_distance modules; used for validation and baseline comparisons) — https://github.com/YuanyueLi/SpectralEntropy
- **spectral_similarity** (Module within SpectralEntropy/MSEntropy for computing spectral similarity scores across 43 distance metrics)
- **ms_distance** (Module for computing MS/MS-specific distance measures (entropy, dot product, Euclidean, Manhattan, etc.))
- **Entropy Search GUI** (Standalone graphical interface for comparing spectral files and searching against spectral libraries using entropy similarity; supports .mgf, .msp, .mzML, .lbm2 formats) — https://github.com/YuanyueLi/EntropySearch

## Examples

```
import ms_entropy as me; import numpy as np; peaks_query = np.array([[69.071, 7.918], [86.066, 1.022]]); peaks_ref = np.array([[69.070, 10.0], [86.065, 5.0]]); score = me.spectral_similarity(peaks_query, peaks_ref, method='entropy'); print(f'Entropy similarity: {score}')
```

## Evaluation signals

- Entropy similarity scores agree numerically with original SpectralEntropy implementation within floating-point tolerance (e.g., < 1e-6 relative error)
- Identified compounds rank higher (lower distance / higher similarity) in entropy-based method than in dot-product baseline for known correct matches
- Identification accuracy (precision@k, recall, area under ROC curve) exceeds dot-product baseline on the same reference dataset
- Wall-clock execution time for Flash entropy search is measurably faster than classical entropy computation (speedup ratio > 1.0) without accuracy loss
- No similarity scores exceed 1.0 (or distance scores fall outside valid range) — indicates proper peak merging and normalization

## Limitations

- Entropy similarity scores above 1.0 can result from errors in merging peaks within MS2-tolerance; use reference implementation from the repository to avoid this
- Flash entropy search algorithm is currently available only in Python; R, C/C++, and JavaScript implementations do not yet support the accelerated algorithm
- Performance gains from Flash entropy search scale with library size; benefit on very small reference sets (< 1000 spectra) may be negligible
- Self-implemented entropy similarity calculations may yield incorrect results if peak merging is not handled correctly; the provided code base is recommended

## Evidence

- [intro] Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification: "Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification"
- [other] Noise filtering threshold and its impact on performance: "peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance"
- [readme] Flash entropy search algorithm provides speed improvements: "With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising"
- [other] Workflow for computing and comparing entropy similarity scores: "Before calculating spectral similarity, it's highly recommended to remove spectral noise"
- [readme] Package integration and supported algorithms: "The code in this repository provides 43 different spectral similarity algorithms for MS/MS spectral comparison."
- [readme] Peak merging error warning: "If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance."
