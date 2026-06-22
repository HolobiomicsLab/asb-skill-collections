---
name: numerical-equivalence-verification
description: Use when when you have reimplemented an algorithm in a new package or optimized an existing algorithm and need to verify that the new version produces the same numerical results as the original or reference implementation.
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
  - tandem-MS
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

# Numerical Equivalence Verification

## Summary

This skill validates that two implementations of an algorithm produce mathematically equivalent results by comparing output matrices element-wise within floating-point tolerance. It is essential for confirming that algorithmic improvements (e.g., the Flash entropy search algorithm) preserve numerical correctness while achieving performance gains.

## When to use

When you have reimplemented an algorithm in a new package or optimized an existing algorithm and need to verify that the new version produces the same numerical results as the original or reference implementation. Specifically, use this skill when comparing entropy similarity scores computed by the original SpectralEntropy implementation against the Flash entropy search algorithm in MSEntropy, or when validating that algorithmic changes do not introduce numerical drift.

## When NOT to use

- When comparing conceptually different algorithms (e.g., entropy similarity vs. dot product similarity); use performance benchmarking or statistical validation instead.
- When the two implementations use different preprocessing or normalization steps; align preprocessing first before numerical comparison.
- When one implementation is still under active development or uses stochastic/non-deterministic components; ensure both are deterministic and finalized.

## Inputs

- MS/MS spectral pairs from reference dataset (e.g. NIST or MassBank) with annotated compound identities
- Preprocessed spectra (noise-filtered, peaks below 1% max intensity removed)
- Output similarity matrix from original implementation
- Output similarity matrix from new/optimized implementation

## Outputs

- Element-wise comparison report (agreement/disagreement per matrix element)
- Floating-point tolerance used for comparison
- Fraction or count of elements in agreement
- Any discrepant elements (if found) and their magnitude of difference

## How to apply

Load identical input data (MS/MS spectral pairs from a reference dataset such as NIST or MassBank with annotated identities) and compute results using both the original and new implementations on the same dataset. Preprocess spectra identically—e.g., remove peaks with intensity less than 1% of maximum intensity—to ensure fair comparison. Compute the full output similarity matrices for both implementations. Compare the matrices element-wise and assess agreement using floating-point tolerance (typically machine epsilon × max magnitude, or a domain-appropriate threshold). Document the exact tolerance used and report the fraction of elements in agreement.

## Related tools

- **SpectralEntropy** (Original reference implementation for entropy similarity computation) — https://github.com/YuanyueLi/SpectralEntropy
- **MSEntropy** (Optimized implementation using Flash entropy search algorithm for comparison) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity** (Module for computing spectral similarity scores)
- **ms_distance** (Module for computing MS distance metrics)

## Examples

```
import numpy as np; similarity_original = compute_entropy_similarity(spectra_pairs, method='original'); similarity_flash = compute_entropy_similarity(spectra_pairs, method='flash'); agreement = np.allclose(similarity_original, similarity_flash, rtol=1e-14, atol=1e-14); print(f'Numerical equivalence: {agreement}')
```

## Evaluation signals

- All corresponding elements of the two similarity matrices agree within the declared floating-point tolerance (e.g., relative error < 1e-14 for double precision).
- No element-wise differences exceed the tolerance threshold by more than a small multiple (e.g., < 2× tolerance).
- The fraction of elements in full agreement is 100% (or very close, allowing for rounding in the last significant digit).
- When differences do occur, they are systematic and attributable to known sources (e.g., order of operations, accumulation order in summation) rather than algorithmic divergence.
- Performance metrics (e.g., wall-clock time, speedup ratio) are reported separately and do not influence the numerical equivalence verdict.

## Limitations

- Floating-point comparison tolerances must be set carefully; too loose a tolerance masks real errors, too tight a tolerance flags expected rounding artifacts. Domain knowledge and platform specifics (CPU architecture, compiler flags) affect what tolerance is appropriate.
- The verification is only as good as the reference dataset; ensure it covers the full expected input space (e.g., diverse spectral complexity, peak intensity ranges, precursor m/z values).
- Deterministic reproducibility may not hold across different operating systems, CPU architectures, or versions of numerical libraries; re-run validation on all target platforms.
- The skill confirms numerical equivalence but does not validate correctness against ground truth; use independent validation (e.g., manual inspection, published benchmarks) to confirm the reference implementation is itself correct.

## Evidence

- [other] Does the Flash entropy search algorithm implementation in the MSEntropy package compute entropy similarity scores that are mathematically equivalent to the original SpectralEntropy implementation while achieving faster performance?: "Does the Flash entropy search algorithm implementation in the MSEntropy package compute entropy similarity scores that are mathematically equivalent to the original SpectralEntropy implementation"
- [other] Compare output similarity matrices element-wise for numerical equivalence (within floating-point tolerance).: "Compare output similarity matrices element-wise for numerical equivalence (within floating-point tolerance)."
- [other] The MSEntropy package has rewritten the entropy similarity calculation method using the Flash entropy search algorithm, indicating an algorithmic improvement over the original SpectralEntropy implementation.: "The MSEntropy package has rewritten the entropy similarity calculation method using the Flash entropy search algorithm, indicating an algorithmic improvement over the original SpectralEntropy"
- [readme] With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising accuracy.: "With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising"
- [other] Preprocess spectra by removing peaks with intensity less than 1% of maximum intensity using the noise-removal filter.: "Preprocess spectra by removing peaks with intensity less than 1% of maximum intensity using the noise-removal filter."
