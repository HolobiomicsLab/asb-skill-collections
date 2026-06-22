---
name: peptide-isotopic-envelope-calculation
description: Use when you have a peptide sequence, precursor charge state, and observed m/z spectrum and need to generate the expected isotopic distribution to match against observed precursor or fragment ion peaks. This is especially critical in SIP workflows where incorporation probabilities (e.g., 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3292
  tools:
  - Aerith
  - mzR
  - Raxport
  - R
  - ThermoRawFileParser
  - Sipros
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peptide-isotopic-envelope-calculation

## Summary

Calculate theoretical isotopic peak envelopes for peptide precursors and fragment ions by convolving elemental isotope distributions according to peptide sequence and charge state. This is essential for matching observed mass spectrometry peaks to theoretical models in stable isotope probing (SIP) experiments and for validating peptide identifications in the presence of natural or incorporated isotopic labels.

## When to use

Apply this skill when you have a peptide sequence, precursor charge state, and observed m/z spectrum and need to generate the expected isotopic distribution to match against observed precursor or fragment ion peaks. This is especially critical in SIP workflows where incorporation probabilities (e.g., 0.0107 for C13 labeling) and isolation window coordinates (center m/z and width) constrain the theoretical envelope that must be computed and compared to observed intensities.

## When NOT to use

- When input is already a pre-computed isotopic distribution table (peak list) rather than a peptide sequence; envelope calculation is redundant.
- When the precursor m/z lies outside the observed spectrum m/z range or isolation window; no matching is possible.
- For unlabeled, natural-abundance peptides where isotopic fine structure is negligible relative to instrument resolution; simpler approximations may suffice.

## Inputs

- Mass spectrum scan (FT1 or FT2 format, or mzML/MGF via mzR)
- Peptide sequence string (amino acid codes)
- Precursor charge state (integer)
- Isotope atom type (e.g., 'C13', 'N15')
- Incorporation probability (0–1, e.g., 0.0107)
- Isolation window center m/z (float)
- Isolation window width (float)
- Observed precursor m/z and intensity values

## Outputs

- ExpectedPrecursorIons table with columns: m/z, intensity, charge, matchedIndices, SIPabundances
- Matched theoretical-to-observed peak indices
- SIP abundance values for each matched peak

## How to apply

Load the mass spectrum scan (e.g., FT1 scan via mzR or Raxport-processed FT2 input) and extract the m/z region of interest (e.g., 880–890 m/z). Provide the annotatePrecursor function with the peptide sequence, charge state (+3 in the example), isotope atom type (C13), incorporation probability (0.0107), and isolation window parameters (isoCenter 886.65, isoWidth 4.0). The function uses sequential convolution to compute the theoretical isotopic peak envelope, then matches theoretical peaks to observed ions and assigns matched indices and SIP abundances for each peak within the m/z window. Verify that all matched peaks fall within the specified isolation window and that SIP abundances reflect the isotopic enrichment model.

## Related tools

- **Aerith** (R package that implements annotatePrecursor and sequential convolution for theoretical isotopic envelope generation and PSM scoring) — https://github.com/xyz1396/Aerith
- **mzR** (Parses mzML and MGF mass spectrum files for extraction of scan data and observed m/z ranges)
- **Raxport** (Converts ThermoFisher .raw files to .FT1/.FT2 formats and extracts precursor charge information) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Cross-platform tool to convert Thermo RAW files to MGF, mzML, or Parquet for downstream processing) — https://github.com/CompOmics/ThermoRawFileParser
- **Sipros** (Peptide search engine that outputs PSM identifications in TSV format, which Aerith can read for SIP-labeled workflow integration) — https://github.com/thepanlab/sipros5

## Examples

```
# R code to compute isotopic envelope and match peaks
annotatePrecursor(observedMass = 886.65, charge = 3, peptideSeq = 'HSQVFSTAEDNQSAVTIHVLQGER', isotopeType = 'C13', incorporationProb = 0.0107, isoCenter = 886.65, isoWidth = 4.0)
```

## Evaluation signals

- All matched m/z values lie within the specified isolation window (isoCenter ± isoWidth/2).
- SIP abundance values sum to approximately 1.0 across all matched peaks for a single precursor ion.
- Matched indices are sequential and correspond to peaks in ascending m/z order.
- Theoretical peak intensities follow isotopic distribution ratios expected from the incorporation probability and charge state.
- The ExpectedPrecursorIons table contains no NaN or negative values in the m/z or SIPabundances columns.

## Limitations

- Sequential convolution is computationally efficient but assumes independent isotope contributions; may underestimate fine isotopic structure at very high mass accuracy.
- Incorporation probability is treated as uniform across all positions in the peptide; heterogeneous labeling patterns are not modeled.
- Isolation window parameters must be accurate; if the window is too narrow, peaks at envelope wings may not be captured; if too wide, off-target isotopic noise may be included.
- Charge state inference is instrument-dependent; FT1/FT2 formats from Orbitrap include charge info, but IonTrap scans may lack it, requiring alternative assignment logic.
- The method does not account for post-translational modifications or non-standard amino acids unless the peptide sequence is preprocessed accordingly.

## Evidence

- [other] annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence: "annotatePrecursor accepts observed precursor mass, probability, and charge along with peptide sequence, charge state, isotope atom type, incorporation probability, isolation window center and width"
- [other] Call annotatePrecursor with the peptide sequence, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak envelope using sequential convolution: "Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak"
- [abstract] employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [readme] Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions: "Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment"
