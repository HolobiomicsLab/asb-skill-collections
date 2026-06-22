---
name: nmr-spectrum-normalization
description: Use when when preparing library compound spectra and observed mixture spectra for mcfNMR analysis, normalize both spectra to cumulative distribution functions (CDFs) scaled by total intensity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - mcfNMR
  - SciPy (scipy.stats.wasserstein_distance)
  - spec2csv
  techniques:
  - NMR
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

# NMR Spectrum Normalization

## Summary

Normalize NMR spectra (library compounds and mixture targets) to a common intensity scale before spectral comparison and compound assignment. This ensures that intensity distributions are comparable across spectra of different absolute concentrations or measurement conditions, enabling fair application of distance metrics like Earth Mover's Distance.

## When to use

When preparing library compound spectra and observed mixture spectra for mcfNMR analysis, normalize both spectra to cumulative distribution functions (CDFs) scaled by total intensity. This is mandatory before computing Earth Mover's Distance, because EMD measures the work required to transport one probability distribution to another—it assumes normalized, probability-like inputs.

## When NOT to use

- If spectra are already in probability or normalized form (e.g., already divided by total intensity).
- If using a distance metric that does not require probability distributions (e.g., raw Euclidean distance on peak lists).
- If analyzing 1D spectra that have been pre-normalized by instrument calibration or vendor software as part of acquisition.

## Inputs

- NMR spectrum as intensity distribution (peak weights and chemical shift coordinates; 1D or 2D)
- Library compound spectra (CSV with columns '1H', '13C', and optional 'weights')
- Target/mixture spectrum (CSV with columns '1H', '13C', and optional 'weights')

## Outputs

- Normalized cumulative distribution function (CDF) for each spectrum, scaled to [0, 1]
- Spectrum represented as (chemical_shift, cumulative_intensity) pairs ready for Earth Mover's Distance computation

## How to apply

Load each spectrum (library compound or mixture target) as a set of peak intensities mapped to NMR chemical shift bins. Compute the cumulative distribution function (CDF) for each spectrum by sorting by chemical shift coordinate and accumulating intensity values. Normalize the CDF to the range [0, 1] by dividing by the total intensity (the final cumulative value). This converts each spectrum into a probability distribution over chemical shift space. The normalized CDF ensures that spectra with different absolute peak heights or total signal levels are placed on equal footing before EMD computation. Store the normalized CDFs for downstream distance calculation.

## Related tools

- **mcfNMR** (integrates spectrum normalization as part of the compound assignment workflow; normalizes both library and target spectra to CDFs before computing Earth Mover's Distance) — https://github.com/GeoMetabolomics-ICBM/mcfNMR
- **SciPy (scipy.stats.wasserstein_distance)** (computes Earth Mover's Distance on normalized CDFs; assumes input distributions are normalized to [0, 1])
- **spec2csv** (converts raw spectrum file formats (USCF, Bruker .txt.gz, peak lists) into standardized CSV format with coordinates and weights, preparing for normalization) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
from scipy.stats import wasserstein_distance; import numpy as np; lib_spectrum = np.array([0.5, 1.2, 0.8]); cdf_lib = np.cumsum(lib_spectrum) / np.sum(lib_spectrum); target_spectrum = np.array([0.3, 1.5, 0.9]); cdf_target = np.cumsum(target_spectrum) / np.sum(target_spectrum); emd = wasserstein_distance(cdf_lib, cdf_target)
```

## Evaluation signals

- Each normalized CDF has minimum value 0 and maximum value 1 (or very close, within floating-point tolerance)
- The CDF is monotonically non-decreasing across the chemical shift domain
- The sum of intensity differences in the original spectrum equals the final CDF value (1.0) after normalization
- Two spectra with identical peak patterns but different absolute intensities produce identical normalized CDFs
- Earth Mover's Distance computed between two normalized CDFs falls in the range [0, 1] and is symmetric

## Limitations

- Normalization assumes all peaks in the spectrum represent genuine signal; artifacts or noise peaks will contribute to and distort the CDF. Pre-filtering by signal-to-noise ratio is recommended.
- For 2D spectra represented as 1D (by setting the second coordinate to zero), normalization treats all peaks equally regardless of their 2D context; this may reduce discrimination power.
- If a spectrum contains zero total intensity (empty or no peaks), normalization by total intensity will fail; such spectra should be excluded or handled separately.
- Bin size and resolution chosen during spectrum preparation (e.g., via spec2csv -b option) influence the normalized CDF shape; finer binning will produce smoother CDFs.

## Evidence

- [other] Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity.: "Compute the cumulative distribution functions (CDFs) for both spectra normalized by total intensity."
- [other] Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute difference between the two CDFs across the chemical shift domain.: "Calculate the Earth Mover's Distance (Wasserstein distance) as the integral of the absolute difference between the two CDFs across the chemical shift domain."
- [intro] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [readme] Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'.: "Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'."
- [readme] Although developed with the goal of processing 2D spectra, it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value).: "Although developed with the goal of processing 2D spectra, it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero."
