---
name: lineshape-convolution-and-broadening
description: Use when after generating theoretical spin multiplets for individual
  metabolites via first-order or density-matrix NMR simulation, but before combining
  spectra or applying Fourier transformation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - MetAssimulo 2
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btaf045
  title: MetAssimulo 2.0
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metassimulo_2_0_cq
    doi: 10.1093/bioinformatics/btaf045
    title: MetAssimulo 2.0
  dedup_kept_from: coll_metassimulo_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf045
  all_source_dois:
  - 10.1093/bioinformatics/btaf045
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lineshape-convolution-and-broadening

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply realistic peak broadening to theoretically simulated NMR multiplets by convolving with a lineshape function (Lorentzian or Gaussian), producing spectral peaks that approximate experimental line widths and instrumental resolution.

## When to use

After generating theoretical spin multiplets for individual metabolites via first-order or density-matrix NMR simulation, but before combining spectra or applying Fourier transformation. Use this skill when input is idealized, zero-width multiplets and the goal is to produce realistic 1D or 2D NMR spectra with natural peak broadening that matches experimental conditions.

## When NOT to use

- Input spectra are already experimental or have been previously broadened; re-convolution introduces artifacts.
- Analysis goal requires resolution of closely-spaced multiplets; over-broadening reduces separation and interpretation confidence.
- Sample or instrument conditions are unknown and no experimental reference spectrum is available to calibrate line width.

## Inputs

- theoretical spin multiplets (intensity vs. chemical shift, zero-width or delta-function representation)
- spin-system coupling constants (J-values in Hz)
- lineshape function type (Lorentzian or Gaussian)
- instrumental line width parameter (FWHM in Hz)

## Outputs

- broadened multiplets (intensity vs. chemical shift, with realistic peak width)
- convolved FID or frequency-domain spectrum ready for Fourier transformation or 2D processing

## How to apply

Convolve each simulated multiplet (a collection of delta-function-like transitions) with a Lorentzian or Gaussian lineshape kernel parameterized by instrumental line width. The choice of lineshape function depends on the source of broadening: Lorentzian lineshapes approximate homogeneous broadening (spin-spin relaxation, T2 effects), while Gaussian lineshapes capture inhomogeneous broadening (magnetic field inhomogeneity, sample heterogeneity). The full width at half maximum (FWHM) of the kernel controls the final peak width; typical values range from 0.5–2 Hz depending on NMR probe quality and sample conditions. Perform convolution in the time domain (on the FID) or frequency domain (on the multiplet intensities) depending on computational efficiency. After convolution, peaks retain correct intensity ratios from the multiplet, but now exhibit realistic broadening suitable for downstream processing (Fourier transformation, spectral fitting, or visual comparison to experimental data).

## Related tools

- **MetAssimulo 2** (web application that integrates lineshape convolution into the full 1D and 2D NMR spectrum simulation pipeline) — https://github.com/yanyan5420/MetAssimulo_2

## Examples

```
python3 apps/index.py -p Input/parameters.txt
```

## Evaluation signals

- Broadened peaks exhibit smooth intensity profiles (no discontinuities or artifacts at peak edges).
- Full width at half maximum (FWHM) of simulated peaks matches the input lineshape FWHM parameter within ±5%.
- Intensity ratios between adjacent multiplet lines remain constant before and after convolution (multiplet structure is preserved).
- Visual or quantitative comparison to experimental NMR spectrum shows realistic peak overlap and resolution consistent with instrumental specifications.
- Convolved spectrum integrates to the same total area as the theoretical multiplet (conservation of intensity).

## Limitations

- Lorentzian and Gaussian lineshapes are idealized; real NMR peaks may exhibit hybrid or complex lineshapes due to spinning sidebands, radiation damping, or probe artifacts.
- Single fixed FWHM across the spectrum does not capture chemical-shift-dependent broadening, which occurs in heterogeneous samples or at high field strengths.
- Convolution in frequency domain assumes linearity; nonlinear instrumental effects (e.g., saturation, frequency modulation) are not captured.
- No automatic calibration of line width from experimental data; user must specify FWHM manually or derive it from a reference peak.

## Evidence

- [methods] Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening.: "Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening."
- [other] MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra.: "MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra."
- [methods] Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling.: "Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling."
