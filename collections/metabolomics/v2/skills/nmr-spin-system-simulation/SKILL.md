---
name: nmr-spin-system-simulation
description: Use when when you have known metabolite concentrations and their spin-system coupling constants (J-values) and need to generate synthetic ¹H NMR spectra for method validation, metabolite library construction, or as a training dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MetAssimulo 2
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
---

# nmr-spin-system-simulation

## Summary

Simulate realistic 1D and 2D metabolomic ¹H NMR spectra by computing theoretical spin multiplets from metabolite concentration and J-coupling inputs, convolving with lineshape functions, and transforming to frequency domain. This skill enables in silico validation of metabolite identification and spectral interpretation without wet-lab acquisition.

## When to use

When you have known metabolite concentrations and their spin-system coupling constants (J-values) and need to generate synthetic ¹H NMR spectra for method validation, metabolite library construction, or as a training dataset. Use this skill if your goal is to predict what a real metabolomic NMR spectrum should look like given known chemical composition, or to validate NMR pulse sequence designs before experimental acquisition.

## When NOT to use

- Input spectra are already experimental NMR data (use this skill for forward simulation, not inverse deconvolution of measured spectra).
- Metabolite identities or J-coupling constants are unknown or highly uncertain (simulation requires accurate spin-system topology).
- Spin systems exhibit strong coupling (second-order effects); first-order approximation will not capture fine structure accurately.

## Inputs

- metabolite concentration vector (one value per metabolite)
- per-metabolite spin-system definitions (chemical shifts in ppm, J-coupling constants in Hz)
- lineshape parameters (Lorentzian or Gaussian function width, baseline offset)
- acquisition parameters (field strength, spectral width, number of points, experiment type: 1D or 2D)

## Outputs

- simulated 1D ¹H NMR spectrum (frequency-domain intensity array, ppm vs intensity)
- simulated 2D NMR spectrum (COSY or HSQC/HMQC; 2D intensity array in HDF5 or netCDF format)
- theoretical multiplet patterns (individual spin-system traces before convolution)
- 1D FID (time-domain complex data before Fourier transformation, for diagnostic purposes)

## How to apply

Parse metabolite concentration inputs and per-metabolite spin-system coupling constants (J-values) into structured format. Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling interactions. Convolve the simulated multiplets with a Lorentzian or Gaussian lineshape function to model realistic peak broadening. Combine individual metabolite spectra into a single 1D free-induction decay (FID) and apply Fourier transformation to produce the frequency-domain ¹H NMR spectrum. For 2D experiments, compute ¹H–¹H COSY or ¹H–¹³C HSQC/HMQC correlations using appropriate 2D pulse sequence encoding and indirect-dimension evolution. Export simulated 1D and 2D spectra as HDF5 or netCDF arrays compatible with standard NMR data formats for downstream analysis or comparison with experimental data.

## Related tools

- **MetAssimulo 2** (Web application that implements ¹H NMR spin-system simulation, multiplet generation, convolution, and 1D/2D Fourier transformation; provides parameter input interface and HDF5/netCDF export.) — https://github.com/yanyan5420/MetAssimulo_2

## Examples

```
python3 apps/index.py -p Input/parameters.txt
```

## Evaluation signals

- Simulated multiplet chemical shift positions match expected literature values for the metabolites within ±0.02 ppm tolerance.
- Peak multiplet splittings (coupling patterns) correspond correctly to input J-values: doublets for ²J ~12–15 Hz, triplets for ³J ~5–8 Hz, etc.
- Simulated spectrum baseline is flat and noise-free (artifact of perfect simulation; contrast with experimental data).
- 2D spectrum contours show expected cross-peak positions in COSY (diagonal + off-diagonal for coupled spins) or HSQC (only directly bound ¹H–¹³C pairs).
- Exported HDF5/netCDF files are readable by standard NMR processing software (e.g., TopSpin, MNova) and contain correct metadata (field strength, spectral width, time/frequency axis labels).

## Limitations

- First-order simulation assumes weak coupling; strong-coupling regimes (Δν < J, where Δν is chemical shift difference) produce inaccurate multiplets.
- Lineshape convolution uses simplified Lorentzian or Gaussian models; real NMR peaks may exhibit Voigt or other asymmetric profiles.
- Spin-spin relaxation (T2) and field inhomogeneity are not modeled; linewidth is set by manual lineshape parameter only.
- Metabolite concentration range and spin-system parameterization must be provided externally; no automatic inference from experimental spectra.
- No support for time-varying effects (e.g., chemical exchange, saturation transfer) or spectra from intact biological matrices with macromolecular background.

## Evidence

- [other] MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra.: "MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra."
- [other] Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling.: "Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling."
- [other] Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening.: "Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening."
- [other] Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum.: "Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum."
- [other] For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution.: "For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution."
- [other] Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats.: "Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats."
- [readme] After successfully running the project using the above provided commands, you should see a message indicating: `Dash is running on http://127.0.0.1:8060/` Just simply ***copy and open this URL*** in your browser, then start simulating NMR spectra!: "After successfully running the project using the above provided commands, you should see a message indicating: `Dash is running on http://127.0.0.1:8060/` Just simply copy and open this URL in your"
