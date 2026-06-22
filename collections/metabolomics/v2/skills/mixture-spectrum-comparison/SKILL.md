---
name: mixture-spectrum-comparison
description: Use when you have an observed NMR mixture spectrum and one or more candidate reconstructed spectra (each formed by summing weighted single-compound spectra), and need a continuous, transportable distance metric to score how well the reconstruction approximates the observed mixture.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - scipy.stats.wasserstein_distance
  - scipy.optimize.linprog
  - mcfNMR
derived_from:
- doi: 10.1021/acs.analchem.4c01652
  title: mcfNMR
evidence_spans: []
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

# mixture-spectrum-comparison

## Summary

Quantify the similarity between an observed NMR mixture spectrum and a reconstructed mixture spectrum (formed by combining single-compound spectra from a library) using Earth Mover's Distance (Wasserstein metric). This metric enables optimization of compound selection and abundance weighting in NMR-based mixture deconvolution.

## When to use

You have an observed NMR mixture spectrum and one or more candidate reconstructed spectra (each formed by summing weighted single-compound spectra), and need a continuous, transportable distance metric to score how well the reconstruction approximates the observed mixture. Use this when optimizing compound selection or relative abundances in NMR mixture analysis, or when comparing the quality of competing reconstructions.

## When NOT to use

- Input spectra are already converted to an alternative distance representation (e.g., cosine similarity, Euclidean distance already computed)
- Spectra contain missing or invalid chemical shift coordinates or negative intensity values
- The chemical shift domain is not aligned or normalized across observed and reconstructed spectra (preprocessing required)

## Inputs

- observed mixture spectrum (1D or 2D NMR, as CSV with columns '1H', '13C', 'weights', or peak list with coordinates and intensities)
- reconstructed mixture spectrum (intensity distribution across chemical shift bins, same format as observed spectrum)

## Outputs

- Earth Mover's Distance score (scalar, non-negative real number; lower values indicate better approximation)
- cumulative distribution functions (CDFs) for both spectra (optional, for visualization or debugging)

## How to apply

Represent both the observed mixture spectrum and candidate reconstructed spectrum as intensity distributions across NMR chemical shift bins (represented as peak coordinates and weights). Normalize each distribution by its total intensity to obtain probability measures. Compute cumulative distribution functions (CDFs) for both spectra along the chemical shift domain. Calculate Earth Mover's Distance as the integral of the absolute difference between the two CDFs. This distance is scale-invariant, handles partial overlap naturally, and quantifies the minimum cost required to 'transport' the probability mass of one spectrum to match the other—making it well-suited for optimizing mixture reconstructions where both observed and reconstructed spectra may have different peak patterns and intensities.

## Related tools

- **scipy.stats.wasserstein_distance** (Direct computation of Earth Mover's Distance (Wasserstein distance) between two normalized intensity distributions) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wasserstein_distance.html
- **scipy.optimize.linprog** (Alternative backend for optimal transport computation via linear programming when explicit Wasserstein implementation is unavailable) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
- **mcfNMR** (Full NMR mixture deconvolution workflow that uses Earth Mover's Distance as the core scoring metric for compound library matching) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
from scipy.stats import wasserstein_distance; import numpy as np; obs_cdf = np.cumsum(obs_spectrum['weights']) / obs_spectrum['weights'].sum(); recon_cdf = np.cumsum(recon_spectrum['weights']) / recon_spectrum['weights'].sum(); emd = wasserstein_distance(obs_spectrum['1H'], recon_spectrum['1H'], u_weights=obs_spectrum['weights'], v_weights=recon_spectrum['weights'])
```

## Evaluation signals

- EMD score is non-negative and finite for valid, aligned spectra
- EMD score is zero only when observed and reconstructed spectra have identical cumulative intensity distributions
- EMD score increases monotonically as the reconstructed spectrum diverges from the observed spectrum (verified on synthetic perturbations)
- CDFs are monotonically increasing and bounded between 0 and 1 after normalization
- Score is insensitive to peak-by-peak alignment errors but sensitive to overall intensity distribution mismatches across the chemical shift domain

## Limitations

- EMD requires normalized, aligned chemical shift domains; spectra with different bin resolutions or chemical shift ranges must be preprocessed
- EMD is sensitive to outliers or isolated peaks far from the main distribution; robust preprocessing of spurious peaks is recommended
- Computational cost scales with number of bins; very high-resolution spectra may require binning or downsampling
- EMD alone does not indicate *which* compounds are present or their absolute concentrations; it is a similarity metric for optimization, not identification

## Evidence

- [other] mcfNMR uses Earth Mover's Distance as the metric to measure the quality of approximation when combining single compound spectra from a library to reconstruct a mixture spectrum.: "mcfNMR uses Earth Mover's Distance as the metric to measure the quality of approximation when combining single compound spectra from a library to reconstruct a mixture spectrum."
- [intro] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [other] Load the observed mixture spectrum and a candidate reconstructed spectrum (both as intensity distributions across NMR chemical shift bins). 2. Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity. 3. Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute difference between the two CDFs across the chemical shift domain.: "Load the observed mixture spectrum and a candidate reconstructed spectrum (both as intensity distributions across NMR chemical shift bins). 2. Compute the cumulative distribution functions (CDFs) for"
- [other] SciPy (scipy.stats.wasserstein_distance or scipy.optimize.linprog for optimal transport): "SciPy (scipy.stats.wasserstein_distance or scipy.optimize.linprog for optimal transport)"
- [readme] it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value).: "it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value)."
