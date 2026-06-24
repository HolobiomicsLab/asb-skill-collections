---
name: fid-to-frequency-domain-fourier-transformation
description: Use when after simulating and convolving individual metabolite multiplets
  with realistic lineshapes (Lorentzian or Gaussian) and combining them into a single
  time-domain FID array.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
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

# fid-to-frequency-domain-fourier-transformation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transform time-domain free-induction decay (FID) data into frequency-domain 1H NMR spectra by applying Fourier transformation. This is a standard signal processing step in NMR spectral simulation that converts combined metabolite FID arrays into interpretable chemical-shift-resolved spectra.

## When to use

Apply this skill after simulating and convolving individual metabolite multiplets with realistic lineshapes (Lorentzian or Gaussian) and combining them into a single time-domain FID array. Use this step when you have completed the generation of all metabolite spin systems for a given 1D proton NMR simulation and need to convert to the frequency domain for display or analysis.

## When NOT to use

- Input is already a 2D COSY, HSQC, or HMQC correlation spectrum (apply 2D Fourier transformation instead, with indirect-dimension evolution).
- Input FID has not yet been convoluted with a realistic lineshape function (apply lineshape broadening before Fourier transformation to ensure realistic peak widths).
- Spectra are to be generated for nuclei other than 1H (e.g., 13C or 31P), where chemical shift ranges and J-coupling patterns differ.

## Inputs

- Combined 1D free-induction decay (FID) array from simulated metabolite spin systems
- Time-domain array with lineshape-broadened multiplets for each metabolite
- Receiver offset and spectral width parameters (Hz)

## Outputs

- Frequency-domain 1H NMR spectrum (complex or magnitude array)
- Chemical shift axis (ppm or Hz)
- HDF5 or netCDF spectral array file compatible with standard NMR formats

## How to apply

After constructing the combined 1D FID by superposing individual metabolite contributions (each accounting for chemical shift, J-coupling, and lineshape broadening), apply a discrete Fourier transformation to convert from the time domain to the frequency domain. This produces a complex-valued or magnitude spectrum indexed by chemical shift (typically expressed in ppm relative to a reference like tetramethylsilane). The Fourier-transformed output should yield peaks at positions corresponding to the metabolite 1H chemical shifts, with multiplet fine structure (doublets, triplets, etc.) preserved by the prior J-coupling simulation. Save the resulting frequency-domain spectrum in a standard NMR data format (HDF5 or netCDF) for downstream visualization or quantitative analysis.

## Related tools

- **MetAssimulo 2** (Web application that orchestrates 1D and 2D metabolomic 1H NMR spectral simulation, including FID generation, Fourier transformation, and output in HDF5/netCDF format) — https://github.com/yanyan5420/MetAssimulo_2

## Examples

```
python3 apps/index.py -p Input/parameters.txt
```

## Evaluation signals

- Frequency-domain spectrum peaks align with the known 1H chemical shifts of input metabolites (within ±0.05 ppm tolerance for standard aqueous NMR).
- Multiplet fine structure (coupling patterns from J-values) is preserved and visible in the transformed spectrum.
- Peak intensity ratios in the frequency domain match the relative metabolite concentrations and proton counts input to the simulation.
- Output file format (HDF5 or netCDF) is readable by standard NMR software and contains expected metadata (axis labels, chemical shift scale, acquisition parameters).
- Real and imaginary components (if retained) show conjugate symmetry properties expected from a real-valued time-domain signal.

## Limitations

- First-order or density-matrix NMR simulation assumptions may fail for strongly coupled or overlapping spin systems at low magnetic field strength; the article does not specify handling of these edge cases.
- Lineshape broadening is applied as Lorentzian or Gaussian convolution; realistic lineshapes in metabolomic samples may be more complex (e.g., Voigt profile, field inhomogeneity).
- No changelog or discussion of validation against experimental spectra is provided in the available documentation.
- The README does not specify numerical precision (32-bit vs. 64-bit float), zero-filling strategy, or apodization window parameters, which can affect spectral resolution and artifact magnitude.

## Evidence

- [other] Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum.: "Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum."
- [other] Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening.: "Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening."
- [other] Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats.: "Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats."
- [other] Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling.: "Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling."
