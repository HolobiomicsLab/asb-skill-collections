---
name: heavy-isotope-labeling-interpretation
description: Use when your peptide sample has been enriched with stable isotope labels (13C, 15N, etc.) at a known incorporation probability (e.g., 52% 13C).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - Raxport
  - R
  - mzR
  - MSnbase
  - Sipros 5
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03207
  all_source_dois:
  - 10.1021/acs.analchem.5c03207
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# heavy-isotope-labeling-interpretation

## Summary

Interpret and annotate peptide fragment ions from mass spectrometry data when peptides are heavily labeled with stable isotopes (e.g., 13C, 15N). This skill uses theoretical isotopic peak envelope calculation and PSM scoring to match observed MS2 peaks against expected B and Y ions with isotope incorporation probabilities.

## When to use

Your peptide sample has been enriched with stable isotope labels (13C, 15N, etc.) at a known incorporation probability (e.g., 52% 13C). You have extracted MS2 scans (observed m/z, intensity, charge) and a target peptide sequence, and you need to determine which observed peaks correspond to specific B and Y fragment ions while accounting for the isotopic mass shifts and peak envelope broadening caused by heavy labeling.

## When NOT to use

- Peptides are unlabeled or the isotope incorporation probability is unknown or highly variable across the sample.
- The observed spectrum has extremely low signal-to-noise ratio or the isolation window is too wide, making it impossible to distinguish true fragments from background noise.
- You are working with PSMs that have already been validated and annotated by a search engine with SIP-aware FDR control (e.g., Sipros 5); re-annotation may introduce inconsistencies.

## Inputs

- MS2 spectrum scan (m/z array, intensity array, charge state)
- Peptide sequence (e.g., HYAHVDCPGHADYVK)
- Precursor m/z value
- Isolation window width (Da)
- Isotope atom type (C13, N15, etc.)
- Isotope incorporation probability (0.0–1.0)

## Outputs

- ExpectedBYions table with matchedIndices
- Annotated B and Y ion fragments with assigned m/z and intensity values
- Residue-position heavy isotope label counts
- Summary statistics (e.g., annotation rate, label distribution)

## How to apply

Load the mass spectrum scan from its native format (FT2, mzML, or MGF) using Aerith/Raxport or similar parsers that preserve isolation window and charge information. Define the peptide sequence and isotope parameters (atom type, incorporation probability). Calculate theoretical isotopic peak envelopes for all possible B and Y ion fragments using sequential convolution, which efficiently models the multiplicative isotope distribution for each fragment length. Run annotatePSM with your observed peak list (m/z, intensity, charge), precursor m/z, isolation window width, and isotope incorporation probability to score and match observed peaks against theoretical B/Y ion envelopes. Filter matched results to retain only annotations with non-negative matchedIndices. Generate residue-position counts summarizing the number of heavy isotope labels per position and compute summary statistics. Verify that matched indices are plausible (e.g., consecutive or near-consecutive fragment positions) and that intensity ranks correlate with expected peak heights from isotopic envelope profiles.

## Related tools

- **Aerith** (Calculate theoretical isotopic peak envelopes for B and Y ions using sequential convolution; score and match observed peaks to expected fragments; visualize annotated PSMs) — https://github.com/xyz1396/Aerith
- **Raxport** (Extract MS1 and MS2 scans from Thermo RAW files and convert to FT2 format for Aerith-compatible parsing) — https://github.com/xyz1396/Raxport.net
- **mzR** (Parse mzML and MGF spectral data files for direct input to Aerith)
- **MSnbase** (Parse pepXML peptide identification files to retrieve peptide sequences and PSM context)
- **Sipros 5** (Search MS2 spectra against protein database with automatic SIP-labeling FDR control; generates TSV PSM input for Aerith visualization and validation) — https://github.com/thepanlab/sipros5

## Evaluation signals

- matchedIndices are non-negative and correspond to observed peaks within the isolation window width.
- Matched B and Y ions follow the expected fragmentation ladder (e.g., Y ions increase monotonically in m/z from C-terminus; B ions increase from N-terminus).
- Residue-position label counts are consistent with the specified isotope incorporation probability and peptide length (e.g., total labels ≈ sequence length × probability).
- Intensity ranks of matched fragments correlate with isotopic envelope heights (higher intensity peaks correspond to major isotopologues).
- Sum of matched fragment masses (accounting for isotopic shifts) approximates the precursor mass within the specified isolation window tolerance.

## Limitations

- Only MS1 and MS2 scans are supported by Raxport; MS3 and higher-order fragmentation cannot be directly annotated.
- Charge state detection from FT2 files is limited to Orbitrap-based instruments; IonTrap FT2 files lack reliable charge information and must be inferred or supplied manually.
- Sequential convolution for peptide fragments assumes a uniform isotope incorporation probability; heterogeneous labeling (position-specific or molecule-specific) is not modeled.
- Very high incorporation probabilities (>90%) or very low probabilities (<10%) may produce sparse isotope envelopes that are difficult to distinguish from noise, potentially leading to false-negative or false-positive matches.
- The annotatePSM scoring function is optimized for 13C labeling; other isotopes (15N, 18O, 2H) may require parameter tuning.

## Evidence

- [other] annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, charge states, isotope atom, incorporation probability, precursor m/z, and isolation window width; returns ExpectedBYions table with matchedIndices: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence (HYAHVDCPGHADYVK), charge states (1:2), isotope atom (C13), incorporation probability (0.52), precursor m/z, and"
- [other] Sequential convolution algorithm for peptide fragments to calculate theoretical isotopic peak envelopes: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] Aerith calculates theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Aerith accepts spectral data in multiple formats including Raxport-processed FT2, mzML, MGF, pepXML, PIN, and TSV files: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros"
- [readme] Raxport extracts scans from Thermo RAW files, supports Orbitrap and IonTrap, generates FT1/FT2 files with charge information from Orbitrap only: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans. However, the generated `.FT1` or `.FT2`"
- [intro] Aerith supports flexible specification of isotopic abundances for stable isotope probing experiments: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic"
- [other] Workflow step: calculate theoretical isotopic peak envelope and run annotatePSM with probability threshold to score and match observed peaks: "Calculate theoretical isotopic peak envelopes for B and Y ions of the peptide using sequential convolution for peptide fragments. 4. Run annotatePSM with probability threshold 0.52 to score and match"
