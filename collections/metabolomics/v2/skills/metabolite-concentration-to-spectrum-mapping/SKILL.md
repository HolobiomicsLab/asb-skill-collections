---
name: metabolite-concentration-to-spectrum-mapping
description: Use when when you have a list of known metabolite concentrations and
  their corresponding J-coupling constants (spin systems) and need to generate realistic
  1D 1H NMR spectra or 2D correlation spectra (COSY, HSQC, HMQC) for simulation, validation,
  or educational purposes, without access to actual.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetAssimulo 2
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
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

# metabolite-concentration-to-spectrum-mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transform metabolite concentration inputs and spin-system coupling constants into realistic 1D and 2D metabolomic 1H NMR spectra by simulating first-order or density-matrix spin multiplets, convolving with lineshape functions, and applying Fourier transformation. This skill bridges quantitative metabolomic data to synthetic spectral predictions for validation, educational, or exploratory NMR simulation workflows.

## When to use

When you have a list of known metabolite concentrations and their corresponding J-coupling constants (spin systems) and need to generate realistic 1D 1H NMR spectra or 2D correlation spectra (COSY, HSQC, HMQC) for simulation, validation, or educational purposes, without access to actual experimental NMR instruments or time-series acquisition.

## When NOT to use

- Input is already an experimental FID or frequency-domain NMR spectrum — use spectral reconstruction or deconvolution instead.
- Metabolite identities or J-coupling constants are not known or are unavailable — first perform metabolite identification and coupling constant assignment.
- Goal is to analyze or quantify real experimental NMR spectra — use standard spectral fitting or deconvolution methods on measured data.

## Inputs

- Metabolite concentration array (molar or relative units)
- Spin-system coupling constants (J-values) per metabolite
- Chemical shift assignments (ppm)
- Lineshape parameters (Lorentzian or Gaussian width)

## Outputs

- 1D 1H NMR frequency-domain spectrum (HDF5 or netCDF format)
- 2D correlation array (COSY, HSQC, or HMQC; HDF5 or netCDF format)
- Free induction decay (FID) time-domain signal

## How to apply

Parse metabolite concentration inputs alongside spin-system J-values for each metabolite as initial parameters. Generate theoretical spin multiplets for each metabolite using first-order or density-matrix NMR simulation, accounting for chemical shift and J-coupling interactions. Convolve each simulated multiplet with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening. Combine individual metabolite spectra into a single 1D free induction decay (FID) and apply Fourier transformation to convert to frequency-domain 1H NMR spectrum. For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) arrays using appropriate 2D pulse-sequence evolution. Save output as HDF5 or netCDF arrays compatible with standard NMR data formats for downstream analysis or visualization.

## Related tools

- **MetAssimulo 2** (Web application that implements metabolite-concentration-to-spectrum mapping for 1D and 2D 1H NMR simulation with spin-system models and lineshape convolution.) — https://github.com/yanyan5420/MetAssimulo_2

## Examples

```
python3 apps/index.py -p Input/parameters.txt
```

## Evaluation signals

- Output spectra display characteristic multiplet patterns (singlets, doublets, triplets, etc.) consistent with input J-coupling values and spin multiplicities.
- Peak positions in frequency domain (ppm) match expected chemical shifts for input metabolites.
- Simulated spectral intensity is proportional to input metabolite concentrations.
- 2D correlation arrays show expected cross-peaks at 1H–1H or 1H–13C frequency intersections matching spin-coupling topologies.
- Output file format (HDF5 or netCDF) is parseable by standard NMR data readers and contains expected array dimensions and metadata.

## Limitations

- Simulation uses first-order or density-matrix approximations, which may not capture higher-order effects (second-order or strong-coupling regimes) in complex spin systems.
- Accuracy depends on accuracy of input J-coupling constants and chemical shift values; errors propagate to spectral prediction.
- Lineshape convolution with Lorentzian or Gaussian functions is a simplification; real NMR peaks may exhibit more complex lineshapes due to instrumental factors (field inhomogeneity, probe effects).
- No explicit support for exchange phenomena, relaxation dynamics, or time-dependent metabolite transformations.

## Evidence

- [other] MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra.: "MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra."
- [other] Parse metabolite concentration inputs and spin-system coupling constants (J-values) for each metabolite. Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling. Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening.: "Parse metabolite concentration inputs and spin-system coupling constants (J-values) for each metabolite. Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for"
- [other] Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum. For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution.: "Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum. For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C"
- [other] Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats.: "Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats."
- [readme] After successfully running the project using the above provided commands, you should see a message indicating: `Dash is running on http://127.0.0.1:8060/`: "After successfully running the project using the above provided commands, you should see a message indicating: `Dash is running on http://127.0.0.1:8060/`"
