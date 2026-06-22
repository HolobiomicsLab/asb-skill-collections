---
name: wasserstein-distance-computation
description: Use when when you have both an observed NMR mixture spectrum and a candidate reconstructed spectrum (each represented as intensity distributions across chemical shift bins), and you need a scalar similarity metric to evaluate how closely the reconstruction matches the observed data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0218
  tools:
  - SciPy (scipy.stats.wasserstein_distance or scipy.optimize.linprog for optimal transport)
  - SciPy
  - mcfNMR
  techniques:
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01652
  all_source_dois:
  - 10.1021/acs.analchem.4c01652
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# wasserstein-distance-computation

## Summary

Compute the Wasserstein distance (Earth Mover's Distance) between two NMR intensity distributions to quantify how well a reconstructed mixture spectrum approximates an observed mixture spectrum. This metric enables objective scoring of spectral reconstruction quality in compound identification workflows.

## When to use

When you have both an observed NMR mixture spectrum and a candidate reconstructed spectrum (each represented as intensity distributions across chemical shift bins), and you need a scalar similarity metric to evaluate how closely the reconstruction matches the observed data. Particularly useful in iterative optimization routines where multiple candidate reconstructions must be ranked or when validating the quality of compound assignments.

## When NOT to use

- When comparing spectra with fundamentally different chemical shift scales or bin resolutions without prior alignment or resampling.
- When intensities are not normalized or when one spectrum has zero total intensity (degenerate case).
- When you need peak-by-peak correspondence rather than global distribution similarity—EMD is a global metric and does not identify which peaks match between spectra.

## Inputs

- Observed mixture NMR spectrum (intensity distribution across chemical shift bins or coordinates)
- Reconstructed mixture spectrum (intensity distribution across same chemical shift domain)
- Chemical shift bin coordinates or coordinates (shared between both spectra)

## Outputs

- Earth Mover's Distance score (scalar, non-negative float; lower values indicate better fit)

## How to apply

Represent both the observed and reconstructed mixture spectra as normalized intensity distributions across the NMR chemical shift domain (bins or coordinates). Compute the cumulative distribution function (CDF) for each spectrum by integrating intensities from the minimum to maximum chemical shift. Calculate the Earth Mover's Distance as the integral of the absolute difference between the two CDFs across the chemical shift domain—this represents the minimum cost to transport one intensity distribution to the other. Use the resulting scalar EMD score to compare competing reconstructions: lower scores indicate better approximations. In the mcfNMR workflow, this metric drives the optimization to select compound combinations that minimize spectral discrepancy.

## Related tools

- **SciPy** (Provides scipy.stats.wasserstein_distance for direct EMD computation or scipy.optimize.linprog for optimal transport formulation) — https://scipy.org
- **mcfNMR** (Implements Wasserstein distance as the primary metric to score and optimize mixture spectrum reconstructions from compound libraries) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
from scipy.stats import wasserstein_distance; emd_score = wasserstein_distance(observed_cdf, reconstructed_cdf)
```

## Evaluation signals

- EMD score is non-negative and symmetric with respect to the two input spectra (swapping observed and reconstructed should yield the same distance).
- EMD equals zero only when both spectra are identical; EMD is positive for any non-identical distributions.
- As the reconstructed spectrum becomes a closer match to the observed spectrum (visually or in peak overlap), the EMD score should monotonically decrease.
- When tested on synthetic data where the reconstructed spectrum is a known weighted combination of observed peaks, EMD should reflect the reconstruction error magnitude.
- EMD scores across multiple candidate reconstructions should be comparable on the same scale, enabling ranking without rescaling.

## Limitations

- EMD treats intensity distributions as continuous and ignores the identity or chemical interpretation of individual peaks—two spectra with the same overall shape but different peak assignments will have low EMD even if chemically distinct.
- Requires both spectra to be defined over the same chemical shift domain; partial or offset spectra require prior alignment.
- Computational cost increases with the resolution (number of bins) of the spectra; high-resolution grids may incur performance overhead in iterative optimization.
- EMD is sensitive to the choice of bin width; coarse binning may mask local discrepancies, while fine binning can amplify noise.

## Evidence

- [intro] mcfNMR constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library"
- [other] mcfNMR uses Earth Mover's Distance as the metric to measure the quality of approximation when combining single compound spectra from a library to reconstruct a mixture spectrum.: "mcfNMR uses Earth Mover's Distance as the metric to measure the quality of approximation when combining single compound spectra from a library to reconstruct a mixture spectrum"
- [other] Load the observed mixture spectrum and a candidate reconstructed spectrum (both as intensity distributions across NMR chemical shift bins). Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity. Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute difference between the two CDFs across the chemical shift domain.: "Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity. Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute"
- [readme] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library"
