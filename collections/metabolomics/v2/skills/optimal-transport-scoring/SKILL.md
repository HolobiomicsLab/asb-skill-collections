---
name: optimal-transport-scoring
description: Use when when you have an observed NMR mixture spectrum and one or more candidate reconstructed spectra (each formed by combining single-compound reference spectra from a library), and you need a scalar similarity score to rank or select the approximation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - SciPy (scipy.stats.wasserstein_distance or scipy.optimize.linprog for optimal transport)
  - SciPy wasserstein_distance
  - SciPy linprog (linear programming)
  - mcfNMR
derived_from:
- doi: 10.1021/acs.analchem.4c01652
  title: mcfNMR
evidence_spans:
- github.com__GeoMetabolomics-ICBM__mcfNMR
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mcfnmr_cq
    doi: 10.1021/acs.analchem.4c01652
    title: mcfNMR
  dedup_kept_from: coll_mcfnmr_cq
schema_version: 0.2.0
---

# optimal-transport-scoring

## Summary

Compute Earth Mover's Distance (Wasserstein metric) between a reconstructed NMR mixture spectrum and an observed mixture spectrum to quantify the quality of compound library approximations. This metric measures the minimum cost to transform one intensity distribution into another across the chemical shift domain.

## When to use

When you have an observed NMR mixture spectrum and one or more candidate reconstructed spectra (each formed by combining single-compound reference spectra from a library), and you need a scalar similarity score to rank or select the best approximation. Use this skill specifically when mixture spectra are represented as intensity distributions across discretized NMR chemical shift bins.

## When NOT to use

- When comparing spectra that are not normalized to the same total intensity scale—normalize first.
- When the chemical shift bins are not aligned or comparable between observed and reconstructed spectra (e.g., different resolution or offset).
- When your goal is feature ranking or compound identification from an individual spectrum; this metric is for comparing two full distributions, not for single-spectrum analysis.

## Inputs

- observed mixture spectrum (intensity values indexed by NMR chemical shift bins)
- reconstructed mixture spectrum (intensity values indexed by NMR chemical shift bins)
- both spectra normalized by total intensity

## Outputs

- Earth Mover's Distance score (scalar float, non-negative)
- optimal transport plan (cumulative difference between CDFs)

## How to apply

Normalize both the observed and reconstructed spectra by their total intensity to obtain probability distributions. Compute cumulative distribution functions (CDFs) for each spectrum across the chemical shift domain. Calculate Earth Mover's Distance as the integral of the absolute difference between the two CDFs—this represents the minimum work required to transport one distribution to match the other. Return the EMD score as a scalar; lower scores indicate better approximation quality. Use this metric iteratively during optimization when fitting multiple compounds jointly to a target spectrum, as it respects the constraint that all allocated peak intensity must remain within the observed spectrum's total capacity.

## Related tools

- **SciPy wasserstein_distance** (Directly computes Earth Mover's Distance between two 1-D distributions; primary implementation option for this skill) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wasserstein_distance.html
- **SciPy linprog (linear programming)** (Alternative implementation for optimal transport computation via linear programming formulation when more control over the transport plan is needed) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
- **mcfNMR** (Production NMR mixture reconstruction tool that uses Earth Mover's Distance as its core scoring metric for evaluating compound library approximations) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
from scipy.stats import wasserstein_distance; emd_score = wasserstein_distance(observed_cdf, reconstructed_cdf)
```

## Evaluation signals

- EMD score is a non-negative scalar; verify the result is ≥ 0.
- EMD(A, A) = 0 (a spectrum should have zero distance to itself); test on identical inputs.
- EMD is symmetric: EMD(observed, reconstructed) = EMD(reconstructed, observed).
- When a reconstructed spectrum perfectly matches the observed spectrum across all bins, the EMD should be ≈ 0; when the spectra differ substantially, EMD should increase monotonically with the divergence.
- The EMD integral should respect cumulative mass balance: ∫|CDF_obs - CDF_recon| dshift ≤ 2 (maximum possible distance when distributions are completely separated).

## Limitations

- EMD requires both spectra to be normalized to the same total intensity; unnormalized or incorrectly scaled inputs will produce misleading scores.
- The metric is sensitive to alignment: if observed and reconstructed spectra have different chemical shift resolutions or bin boundaries, the result may not be meaningful. Ensure bins are synchronized.
- EMD is computationally more expensive than simple norm-based metrics (e.g., Euclidean distance); for very large bin counts or many pairwise comparisons, performance may become a bottleneck.
- EMD does not distinguish between small local shifts vs. large global shifts; it only measures the total transport cost, so systematic peak shifts may not be penalized differently than random noise.

## Evidence

- [intro] mcfNMR constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [other] Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity. Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute difference between the two CDFs across the chemical shift domain.: "Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity. 3. Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute"
- [other] mcfNMR uses Earth Mover's Distance as the metric to measure the quality of approximation when combining single compound spectra from a library to reconstruct a mixture spectrum: "mcfNMR uses Earth Mover's Distance as the metric to measure the quality of approximation when combining single compound spectra from a library to reconstruct a mixture spectrum."
- [other] SciPy (scipy.stats.wasserstein_distance or scipy.optimize.linprog for optimal transport): "tools: SciPy (scipy.stats.wasserstein_distance or scipy.optimize.linprog for optimal transport)"
- [other] Load the observed mixture spectrum and a candidate reconstructed spectrum (both as intensity distributions across NMR chemical shift bins): "Load the observed mixture spectrum and a candidate reconstructed spectrum (both as intensity distributions across NMR chemical shift bins)."
