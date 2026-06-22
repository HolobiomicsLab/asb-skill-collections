---
name: j-coupling-multiplet-generation
description: Use when you have parsed metabolite identities with known spin-system coupling constants (J-values) and chemical shifts, and need to generate the theoretical multiplet patterns that will form the basis of a simulated 1D or 2D NMR spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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

# j-coupling-multiplet-generation

## Summary

Generate theoretical spin multiplets from metabolite spin systems by applying J-coupling constants and chemical shifts, using first-order or density-matrix NMR simulation to produce realistic multiplet patterns for 1H NMR spectral reconstruction. This skill is essential for converting metabolite structural information into realistic spectral peak shapes that can be combined into simulated metabolomic NMR spectra.

## When to use

Apply this skill when you have parsed metabolite identities with known spin-system coupling constants (J-values) and chemical shifts, and need to generate the theoretical multiplet patterns that will form the basis of a simulated 1D or 2D NMR spectrum. Use it as the intermediate step between metabolite concentration inputs and full spectral simulation.

## When NOT to use

- When experimental (observed) multiplets are already available — use those directly rather than simulating
- When only singlet peaks are expected (no coupled spins) — skip to lineshape convolution
- When metabolite structure or J-values are not known or unreliable — multiplet generation requires accurate coupling constant input

## Inputs

- Metabolite identifiers with assigned spin systems
- Spin-system coupling constants (J-values in Hz)
- Chemical shift values (in ppm or Hz)
- Spin multiplicities (number of equivalent neighboring spins)

## Outputs

- Theoretical spin multiplets (intensity vs. frequency arrays)
- Multiplet peak positions and intensities
- First-order or density-matrix simulated line shapes for each spin system

## How to apply

Parse the spin-system coupling constants (J-values) and chemical shift values for each metabolite from the input parameter file. For each metabolite, select either first-order or density-matrix NMR simulation depending on the complexity of the spin system and overlap regime. Apply the chosen simulation method to generate theoretical spin multiplets that account for both chemical shift and J-coupling interactions. The output multiplets should reflect the multiplicities (singlet, doublet, triplet, etc.) expected from the n+1 rule applied to the parsed coupling constants. These multiplets will subsequently be convolved with a Lorentzian or Gaussian lineshape function and combined into the full spectrum.

## Related tools

- **MetAssimulo 2** (Web application framework that encapsulates J-coupling multiplet generation as a pipeline step before lineshape convolution and Fourier transformation) — https://github.com/yanyan5420/MetAssimulo_2

## Examples

```
python3 apps/index.py -p Input/parameters.txt
```

## Evaluation signals

- Verify that simulated multiplet multiplicities match the expected n+1 rule for the parsed spin system (e.g., a proton coupled to two equivalent neighbors produces a triplet with 1:2:1 intensity ratio)
- Check that peak spacing (in Hz) matches the input J-coupling constants within numerical tolerance
- Confirm that the total integrated area under each simulated multiplet is proportional to the spin population (number of equivalent protons)
- Validate that chemical shifts of multiplet centers align with the input chemical shift values
- Compare first-order vs. density-matrix results for overlapping or high-field spin systems — density-matrix should handle second-order effects absent from first-order approximation

## Limitations

- First-order approximation is only valid when the chemical shift difference between coupled spins (Δν in Hz) is much larger than the coupling constant J; high-field magnets and overlapping signals may require density-matrix simulation
- Accuracy of multiplet generation depends critically on the accuracy of input J-coupling constants and chemical shift values; literature or database values may vary by 0.5–2 Hz or ±0.1 ppm
- Simulated multiplets assume idealized spin systems and do not account for exchanging protons, paramagnetic effects, or solvent interactions that distort real multiplet shapes

## Evidence

- [other] Parse metabolite concentration inputs and spin-system coupling constants (J-values) for each metabolite: "Parse metabolite concentration inputs and spin-system coupling constants (J-values) for each metabolite."
- [other] Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling: "Generate theoretical spin multiplets using first-order or density-matrix NMR simulation for each spin system, accounting for chemical shift and J-coupling."
- [other] Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening: "Convolve simulated multiplets with a Lorentzian or Gaussian lineshape function to approximate realistic peak broadening."
