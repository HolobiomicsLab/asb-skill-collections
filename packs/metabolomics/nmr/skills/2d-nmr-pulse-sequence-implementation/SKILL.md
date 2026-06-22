---
name: 2d-nmr-pulse-sequence-implementation
description: Use when when you need to generate 2D metabolomic NMR spectra (COSY for homonuclear or HSQC/HMQC for heteronuclear correlations) from parsed metabolite concentration and spin-system J-coupling data, and you want to simulate realistic peak patterns including indirect-dimension evolution and phase.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  tools:
  - MetAssimulo 2
  techniques:
  - NMR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# 2D NMR Pulse Sequence Implementation

## Summary

Design and execute 2D NMR pulse sequences (COSY, HSQC/HMQC) to compute 1H–1H or 1H–13C correlation multiplets with appropriate indirect-dimension evolution, enabling metabolomic structure elucidation. This skill bridges simulated spin systems to 2D frequency-domain spectra by applying phase-encoding and indirect-dimension time steps.

## When to use

When you need to generate 2D metabolomic NMR spectra (COSY for homonuclear or HSQC/HMQC for heteronuclear correlations) from parsed metabolite concentration and spin-system J-coupling data, and you want to simulate realistic peak patterns including indirect-dimension evolution and phase encoding.

## When NOT to use

- Input is already a measured 2D NMR spectrum (no simulation needed; use acquisition software instead)
- Metabolite identities or J-couplings are unknown or unavailable (simulation requires explicit spin-system topology)
- Goal is to process or interpret experimental 2D spectra rather than generate synthetic reference data

## Inputs

- Metabolite concentration values (numeric array or list)
- Spin-system coupling constants (J-values) per metabolite (Hz)
- Chemical shifts for involved nuclei (ppm)
- Pulse sequence parameters (indirect-dimension increments, phase encoding steps, receiver phases)
- Lineshape function specification (Lorentzian or Gaussian bandwidth)

## Outputs

- 2D NMR spectral array (frequency-domain, real or complex)
- Indirect and direct dimension frequency axes (ppm)
- 2D spectral data in HDF5 or netCDF format
- Cross-peak multiplet patterns (COSY or HSQC/HMQC correlation map)

## How to apply

Starting from parsed metabolite concentrations and spin-system coupling constants (J-values), select the appropriate 2D pulse sequence (COSY for 1H–1H correlation or HSQC/HMQC for 1H–13C heteronuclear correlation). Implement the sequence by evolving the spin system through indirect-dimension time increments with phase encoding, computing cross-peak multiplets that reflect scalar coupling between correlated nuclei. Apply the same lineshape convolution (Lorentzian or Gaussian) used in the 1D simulation to account for realistic peak broadening. Fourier-transform both direct and indirect dimensions to produce a 2D frequency-domain array. Save the result in standard NMR data formats (HDF5 or netCDF) compatible with downstream NMR analysis software.

## Related tools

- **MetAssimulo 2** (Web application that implements 2D pulse sequences (COSY, HSQC/HMQC) for simulating 1H–1H and 1H–13C correlations from metabolite inputs) — https://github.com/yanyan5420/MetAssimulo_2

## Examples

```
python3 apps/index.py -p Input/parameters.txt
```

## Evaluation signals

- Cross-peaks appear at expected chemical shift intersections corresponding to coupled spin pairs (COSY) or coupled nuclei (HSQC/HMQC)
- Multiplet structure in cross-peaks matches theoretical J-coupling patterns (e.g., doublet, triplet) for the underlying spin system
- Indirect and direct dimension Fourier transforms produce peak frequencies (ppm) that align with input chemical shifts and J-couplings
- Output 2D spectral array conforms to HDF5 or netCDF schema with labeled frequency axes and metadata
- Lineshape convolution produces realistic peak widths without excessive broadening or ringing artifacts

## Limitations

- Simulation uses first-order or density-matrix approximations; higher-order coupling effects are not explicitly modeled
- Pulse sequence parameters (flip angles, phase cycles, gradient strengths) must be manually specified; default values may not match all experimental protocols
- No experimental validation of simulated spectra against real NMR data is performed within the tool; realism depends on accurate input J-values and lineshape assumptions
- Complex spin systems (>4 coupled spins) may require longer computation or density-matrix methods; scalability limits are not documented

## Evidence

- [other] For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution.: "For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution."
- [other] Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling.: "Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling."
- [other] Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening.: "Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening."
- [other] Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats.: "Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats."
- [readme] This repository contains all the necessary code for the MetAssimulo 2 project.: "This repository contains all the necessary code for the MetAssimulo 2 project."
