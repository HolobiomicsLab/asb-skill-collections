---
name: charge-state-determination-and-assignment
description: Use when when analyzing high-resolution mass spectrometry data from natural-abundance or labeled peptides where multiple charge states (+2, +3, +4, etc.) may be present within the same m/z isolation window (e.g., 880–890 m/z).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - mzR
  - Raxport
  - R
  - ThermoRawFileParser
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
- Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files
- Extract visualization information from `.FT2` files
- Aerith is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aerith_cq
    doi: 10.1021/acs.analchem.5c03207
    title: Aerith
  dedup_kept_from: coll_aerith_cq
schema_version: 0.2.0
---

# Charge-State Determination and Assignment

## Summary

Assign charge states to observed precursor ions and matched theoretical isotopic peaks by integrating isolation window coordinates, peptide sequence, and isotopic enrichment models. This skill disambiguates multiply-charged species in stable isotope probing (SIP) experiments where accurate charge state is essential for correct m/z-to-mass conversion and isotopic pattern matching.

## When to use

When analyzing high-resolution mass spectrometry data from natural-abundance or labeled peptides where multiple charge states (+2, +3, +4, etc.) may be present within the same m/z isolation window (e.g., 880–890 m/z). Charge state is especially critical when the observed precursor envelope spans several peaks and theoretical isotopic patterns must be matched to empirical data to enable correct SIP abundance calculation and peptide identification.

## When NOT to use

- If the charge state is already confidently determined by the instrument (e.g., from Orbitrap high-resolution charge detection), this manual re-assignment step may be redundant.
- When the isolation window is extremely narrow (< 0.5 m/z) and only a single isotopic peak is isolated; ambiguity in charge state is minimal and the skill adds no discriminative value.
- If the peptide sequence is unknown or the mass spectrum is too noisy to resolve individual isotopic peaks (signal-to-noise < 3 for the expected envelope).

## Inputs

- Observed precursor mass (m/z)
- Precursor charge state (integer: +2, +3, +4, etc.)
- Peptide sequence (string)
- Isotope atom type and incorporation probability (e.g., C13 at 0.0107)
- Isolation window center (m/z) and width (m/z)
- Full scan mass spectrum in mzML, MGF, or Raxport-processed FT2 format
- Observed peak m/z and intensity values

## Outputs

- ExpectedPrecursorIons table with columns: m/z, intensity, charge, matchedIndices, SIPabundances
- Assigned charge states for each matched observed peak
- Theoretical vs. observed peak alignment summary

## How to apply

Accept the observed precursor mass, charge state, probability, and isolation window parameters (center and width in m/z) along with the peptide sequence. Use annotatePrecursor to compute a theoretical isotopic peak envelope via sequential convolution for the specified charge state (+3 for the example peptide HSQVFSTAEDNQSAVTIHVLQGER), then match the resulting theoretical m/z positions and intensities to observed ions within the isolation window. Assign matched indices to each observed peak that falls within the expected m/z region for that charge state; peaks outside the window or inconsistent with the envelope are not assigned. Calculate SIP abundances for matched peaks using the isotopic enrichment model (e.g., C13 incorporation probability 0.0107). The charge state assignment is validated by ensuring that the full theoretical envelope (including fine structure isotopic peaks) aligns with observed intensities; mismatched charge states will produce poor peak correlation and low confidence scores.

## Related tools

- **Aerith** (Computes theoretical isotopic peak envelopes via sequential convolution and matches them to observed precursor ions; implements annotatePrecursor function that accepts charge state and produces ExpectedPrecursorIons table with matched indices and SIP abundances.) — https://github.com/xyz1396/Aerith
- **mzR** (Parses mzML and MGF mass spectrometry files to extract observed m/z and intensity data for charge state assignment validation.)
- **Raxport** (Converts Thermo Fisher RAW files to .FT2 format; extracts charge information for Orbitrap scans and MS1/MS2 scan data needed as input to charge assignment workflow.) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Cross-platform tool to convert Thermo RAW mass spectrometer files to mzML, MGF, or other formats compatible with Aerith's charge state assignment pipeline.) — https://github.com/CompOmics/ThermoRawFileParser

## Examples

```
annotatePrecursor(observedMass=886.65, peptideSequence='HSQVFSTAEDNQSAVTIHVLQGER', chargeState=3, isotopeType='C13', incorporationProb=0.0107, isoCenter=886.65, isoWidth=4.0)
```

## Evaluation signals

- Theoretical isotopic peak envelope matches observed peak positions within ±5 ppm mass tolerance for all peaks within the isolation window.
- Calculated SIP abundances for matched peaks sum to ≤ 1.0 (representing isotope fraction for the labeling experiment) and are consistent with the specified incorporation probability.
- For natural-abundance control peptides, matched peaks show monotonic or unimodal intensity profile typical of isotopic distributions (highest intensity at the monoisotopic or M+1 position).
- Charge state assignment is stable across replicate scans and consistent with peptide mass and expected ionization state (e.g., +3 for a 25 kDa peptide is more likely than +1).
- When charge state is incorrect, theoretical envelope fails to cover observed peaks or predicts peaks with zero observed intensity (false positive matches).

## Limitations

- Sequential convolution for peptide isotopic envelopes becomes computationally expensive for very long peptides (> 100 amino acids); Monte Carlo simulation may be preferred for fine isotopic structure but adds stochastic variability.
- Charge state assignment relies on accurate specification of isolation window center and width; mismatched window parameters will exclude true peaks or include spurious background noise.
- Natural-abundance peptides with unresolved or overlapping isotopic peaks (low m/z or low charge state, e.g., +1) may show ambiguous charge state signature; the skill requires sufficient spectral resolution (FWHM ≤ 0.1 m/z for Orbitrap).
- SIP abundance calculation assumes accurate knowledge of isotope incorporation probability; incorrect enrichment model (e.g., assuming 1% 13C when the experiment used 50% 13C) will produce incorrect matched peak scores and false assignments.
- The skill does not resolve isobaric peptides (same m/z and charge) or overlapping charge envelopes from coeluting precursor ions; additional filtering (e.g., retention time, peptide database search) is required.

## Evidence

- [other] annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence, charge state, isotope atom type, incorporation probability, isolation window center and width to produce a table of ExpectedPrecursorIons with matched indices and SIP abundances for peaks within the specified m/z region.: "annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence, charge state, isotope atom type, incorporation probability, isolation window center and width"
- [other] Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak envelope using sequential convolution.: "Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak"
- [other] Match theoretical peaks to observed ions within the m/z window and assign charge states and matched indices.: "Match theoretical peaks to observed ions within the m/z window and assign charge states and matched indices"
- [abstract] Aerith employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate isotopic distributions.: "sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate isotopic distributions"
- [intro] Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files: "Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files"
- [intro] Extract visualization information from `.FT2` files: "Extract visualization information from `.FT2` files"
