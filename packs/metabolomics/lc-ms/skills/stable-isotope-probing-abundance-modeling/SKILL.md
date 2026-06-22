---
name: stable-isotope-probing-abundance-modeling
description: Use when you have a high-resolution mass spectrum (FT scan) containing a peptide precursor at known charge state with known or suspected stable isotope labeling (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - Aerith
  - mzR
  - Raxport
  - R
  - ThermoRawFileParser
  techniques:
  - LC-MS
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

# stable-isotope-probing-abundance-modeling

## Summary

Compute and match observed precursor isotope peaks to theoretical isotopic patterns for natural-abundance or enriched peptides, accounting for stable isotope incorporation probability and charge state. This skill enables quantitative SIP abundance assignment for isotope-labeled peptide precursors within specified m/z isolation windows.

## When to use

You have a high-resolution mass spectrum (FT scan) containing a peptide precursor at known charge state with known or suspected stable isotope labeling (e.g. ¹³C, ¹⁵N), a defined m/z isolation window (center and width), and you need to discriminate observed isotope peaks from noise and assign SIP abundances for each matched peak. This is essential when validating SIP-labeled peptide identifications or when manually inspecting PSMs where isotope pattern matching is ambiguous.

## When NOT to use

- Precursor m/z or charge state is unknown or highly uncertain; the model will produce spurious matches outside the intended m/z region.
- Isolation window is too narrow relative to peak width, resulting in truncated isotope envelopes and unreliable SIP abundance estimates.
- Input spectrum is unprocessed or contains excessive noise without baseline subtraction; matching will fail or produce false positives.

## Inputs

- High-resolution mass spectrum scan (FT1 or Raxport FT2 format, read via mzR)
- Peptide sequence (string, e.g. 'HSQVFSTAEDNQSAVTIHVLQGER')
- Charge state (integer, e.g. +2, +3)
- Isotope atom type (e.g. 'C13', 'N15')
- Incorporation probability (float between 0 and 1)
- Isolation window center m/z (float, e.g. 886.65)
- Isolation window width (float, e.g. 4.0)

## Outputs

- ExpectedPrecursorIons table with columns: m/z, intensity, charge, matchedIndices, SIPabundances
- Matched peak annotations linked to theoretical isotope peaks
- SIP abundance scores for each matched peak

## How to apply

Load the full-scan mass spectrum (e.g. FT1 scan) using mzR or Raxport-processed FT2 format and extract the m/z range around the expected precursor (e.g. 880–890 for a +3 charge state). Call annotatePrecursor with the peptide sequence, charge state, isotope atom type (C13, N15, etc.), incorporation probability (between 0 and 1, e.g. 0.0107 for natural ¹³C abundance), and isolation window parameters (center m/z and width). The function internally computes the theoretical isotopic peak envelope using sequential convolution, then matches each observed peak within the isolation window to a theoretical isotope peak, assigning matched indices and calculating SIP abundances based on the isotopic enrichment model. Validate the result by checking that matched peaks cluster near the theoretical envelope, that intensities and m/z values fall within expected ranges, and that the number of matched peaks is consistent with the charge state and incorporation probability.

## Related tools

- **Aerith** (R package providing annotatePrecursor function to compute theoretical isotopic envelopes and match observed peaks to theoretical isotope patterns with SIP abundance scoring) — https://github.com/xyz1396/Aerith
- **mzR** (Bioconductor package for reading and parsing mass spectrum files in mzML and MGF formats)
- **Raxport** (Extracts FT1/FT2 scan data from ThermoFisher RAW files for downstream annotation) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Alternative tool for converting ThermoFisher RAW files to open formats (mzML, MGF) compatible with mass spectrum readers) — https://github.com/CompOmics/ThermoRawFileParser

## Evaluation signals

- Matched peaks lie within the specified isolation window (isoCenter ± isoWidth/2 m/z) and cluster near the theoretical isotope envelope.
- ExpectedPrecursorIons table contains no gaps or NaN values in m/z, intensity, charge, or SIPabundances columns; all matched indices are non-negative integers.
- SIP abundances sum to approximately 1.0 (or a known fraction if labeled) and increase monotonically with isotope offset when incorporation probability is uniform.
- Manual visual inspection of the matched peaks against a plotted theoretical envelope confirms alignment within instrumental resolution (e.g. <5 ppm for Orbitrap).
- Number of matched peaks is consistent with the charge state and incorporation probability (e.g. +3 charge state with 1% ¹³C should yield ~3–5 prominent peaks).

## Limitations

- Requires accurate precursor m/z and charge state; misspecification leads to false matches in overlapping isotope envelopes.
- Sequential convolution algorithm assumes uniform isotope abundance within a peptide; does not handle intra-peptide positional enrichment biases.
- Isolation window must be wide enough to capture the full isotope envelope; narrow windows (e.g. <2 m/z width) will truncate the distribution and underestimate SIP abundance.
- Performance degrades for multiply-charged peptides (charge ≥ +4) where isotope peaks become closely spaced and harder to resolve.
- Only MS1 (precursor-level) annotation is supported; fragment-level (MS2) SIP annotation requires separate B/Y ion envelope computation via annotatePrecursor with fragment parameters.

## Evidence

- [full_text] annotatePrecursor function parameters and output: "annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence, charge state, isotope atom type, incorporation probability, isolation window center and width"
- [full_text] Workflow description from task_004: "Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak"
- [abstract] Sequential convolution algorithm: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] SIP definition and purpose: "Stable isotope probing (SIP) is indeed a powerful technique for tracing the fate of metabolic labels incorporated into cells, offering insights into substrate assimilation and associated metabolic"
- [intro] Flexible isotope abundance specification: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic"
