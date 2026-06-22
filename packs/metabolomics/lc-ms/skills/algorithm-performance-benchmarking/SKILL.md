---
name: algorithm-performance-benchmarking
description: Use when you have refactored or reimplemented a core computational method (e.g., entropy similarity calculation) and need to verify that the new implementation produces mathematically equivalent results to the original before deploying it to production.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - MSEntropy
  - SpectralEntropy
  - spectral_similarity
  - ms_distance
  techniques:
  - LC-MS
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

# algorithm-performance-benchmarking

## Summary

Systematically compare the numerical accuracy and computational efficiency of an improved algorithm implementation against a reference implementation by computing identical metrics on the same input dataset and measuring wall-clock execution time. This skill validates that algorithmic rewrites preserve correctness while quantifying performance gains.

## When to use

You have refactored or reimplemented a core computational method (e.g., entropy similarity calculation) and need to verify that the new implementation produces mathematically equivalent results to the original before deploying it to production. The trigger is the existence of two implementations of the same algorithm on the same problem domain.

## When NOT to use

- The two implementations use fundamentally different algorithmic approaches that are not equivalent by design (e.g., comparing dot-product similarity to entropy similarity) — this is algorithm validation, not benchmarking.
- Input datasets are too small (<10 spectral pairs) to yield statistically meaningful timing measurements.
- Floating-point tolerance thresholds are not defined a priori, making numerical equivalence assessment subjective.

## Inputs

- MS/MS spectral pairs (m/z and intensity tuples) from a reference database
- Annotated compound identities or metadata linking spectral pairs
- Original algorithm implementation (source code or callable module)
- Improved algorithm implementation (source code or callable module)

## Outputs

- Similarity score matrix from original implementation
- Similarity score matrix from improved implementation
- Element-wise comparison report (agreement rate, max absolute difference)
- Execution time measurements for both implementations
- Speedup ratio (original time / improved time)
- Tabulated performance and accuracy metrics

## How to apply

Load a reference dataset of MS/MS spectral pairs with annotated identities (e.g., from NIST or MassBank). Preprocess spectra uniformly using the same filter (e.g., remove peaks with intensity < 1% of maximum intensity). Compute the target metric (e.g., entropy similarity scores) using both the original and improved implementations on identical preprocessed inputs. Compare output matrices element-wise for numerical equivalence within floating-point tolerance (typically 1e-10 to 1e-15 for IEEE 754 doubles). Measure wall-clock execution time for each implementation and compute the speedup ratio as (original time / improved time). Document agreement statistics (e.g., percentage of elements matching, max absolute difference) and performance metrics in a structured report.

## Related tools

- **SpectralEntropy** (Reference implementation for entropy similarity calculation) — https://github.com/YuanyueLi/SpectralEntropy
- **MSEntropy** (Improved implementation using Flash entropy search algorithm for entropy similarity calculation) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity** (Module providing similarity computation utilities) — https://github.com/YuanyueLi/MSEntropy
- **ms_distance** (Module providing MS-specific distance metrics) — https://github.com/YuanyueLi/MSEntropy

## Examples

```
import numpy as np; import ms_entropy as me; peaks = np.array([[69.071, 7.917962], [86.066, 1.021589]]); sim_old = spectral_entropy_original(peaks, peaks); sim_new = me.entropy_similarity(peaks, peaks); assert np.allclose(sim_old, sim_new, atol=1e-10); print(f'Match: {sim_old:.6f} vs {sim_new:.6f}')
```

## Evaluation signals

- Similarity score matrices are element-wise identical within floating-point tolerance (e.g., max absolute difference < 1e-10).
- Agreement rate is 100% (or ≥99.99% after accounting for IEEE 754 rounding) across all spectral pairs in the reference dataset.
- Improved implementation exhibits measurable speedup (e.g., ≥2× faster wall-clock execution) on the same spectral pairs without accuracy loss.
- Preprocessing (noise filtering) is applied identically to both implementations before metric computation.
- Output matrices have matching dimensionality and ordering (both computed on the same spectral pair sequence).

## Limitations

- Floating-point arithmetic may introduce small numerical discrepancies; tolerance thresholds must be set conservatively to account for rounding across different code paths and compiler optimizations.
- Wall-clock timing measurements are sensitive to system load, cache state, and implementation language differences; multiple runs and statistical analysis (mean ± SD) are recommended.
- Speedup ratios are hardware- and input-size-dependent; benchmarking should be conducted on representative datasets and target hardware to generalize results.
- Self-implemented variants of entropy similarity may produce scores higher than 1.0 due to incorrect peak merging within MS/MS tolerance; only validated reference implementations should be used for comparison.

## Evidence

- [other] The MSEntropy package has rewritten the entropy similarity calculation method using the Flash entropy search algorithm, indicating an algorithmic improvement over the original SpectralEntropy implementation.: "the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising accuracy."
- [other] Benchmark workflow includes data loading, preprocessing, dual implementation execution, element-wise comparison, and timing measurement.: "Load MS/MS spectral pairs from a reference dataset (e.g., NIST or MassBank) with annotated compound identities. Preprocess spectra by removing peaks with intensity less than 1% of maximum intensity"
- [readme] Entropy similarity computation is the target metric for algorithmic improvement and benchmarking.: "Entropy similarity, which measured spectral similarity based on spectral entropy, has been shown to outperform dot product similarity in compound identification."
- [readme] Risk of incorrect peak merging in self-implemented versions.: "Please note: If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance. Use the code provided in our"
- [other] Preprocessing step: noise removal via intensity filtering.: "peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance"
