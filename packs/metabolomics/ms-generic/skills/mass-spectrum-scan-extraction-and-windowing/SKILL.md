---
name: mass-spectrum-scan-extraction-and-windowing
description: Use when when you have a full mass spectrum scan (e.g., FT1 or FT2 scan from an Orbitrap or IonTrap instrument) and need to isolate a narrow m/z window containing a known or predicted precursor ion before matching it to theoretical isotopic envelopes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - mzR
  - Raxport
  - R
  - ThermoRawFileParser
  techniques:
  - mass-spectrometry
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

# mass-spectrum-scan-extraction-and-windowing

## Summary

Extract and isolate specific mass-to-charge (m/z) regions from full-scan mass spectra stored in raw or processed formats, preparing precursor ion data for isotopic annotation and scoring. This skill bridges raw instrument output to targeted isotope pattern analysis by windowing observed peaks within defined isolation boundaries.

## When to use

When you have a full mass spectrum scan (e.g., FT1 or FT2 scan from an Orbitrap or IonTrap instrument) and need to isolate a narrow m/z window containing a known or predicted precursor ion before matching it to theoretical isotopic envelopes. Apply this skill when the precursor m/z and isolation window parameters (center and width) are known in advance, as required for stable isotope probing (SIP) analysis of labeled peptides.

## When NOT to use

- Input data is already windowed or processed to a single m/z feature; re-windowing may introduce artifacts or lose context.
- Isolation window parameters are unknown or absent; windowing without validated boundaries risks including or excluding true isotopic peaks.
- Full-scan spectrum has not been centroided or has very low signal-to-noise ratio; extracted window will contain insufficient information for isotopic pattern matching.

## Inputs

- raw mass spectrum file (Thermo .raw, mzML, MGF, or Raxport-processed FT1/FT2 file)
- scan ID or scan number (integer)
- isolation window center (m/z, float)
- isolation window width (m/z, float)

## Outputs

- observed precursor m/z and intensity pairs within the isolation window (data.frame or matrix with columns m/z, intensity)
- extracted spectrum subset (m/z range, intensity array)

## How to apply

Load the raw mass spectrum file using a file-format parser such as mzR (for mzML/MGF) or Raxport (for Thermo FT1/FT2 files). Retrieve the target scan by scan ID (e.g., scan 107695). Extract the m/z range defined by isoCenter ± (isoWidth / 2); for example, if isoCenter=886.65 and isoWidth=4.0, extract the m/z interval [884.65, 888.65]. Validate that observed peaks within the window have been detected and that the window spans the full isotopic envelope (typically 4–5 m/z units for singly or doubly charged ions, wider for higher charge states). Return the extracted intensities and m/z values as a structured array or matrix for downstream annotation by tools such as annotatePrecursor. The windowing step is essential to reduce computational overhead and focus the isotopic pattern matching on the region of interest.

## Related tools

- **mzR** (parse and read mass spectrum scans from mzML and MGF file formats)
- **Raxport** (extract scans from Thermo RAW files and convert to FT1/FT2 format for downstream analysis) — xyz1396/Raxport.net
- **ThermoRawFileParser** (convert Thermo RAW mass spectrometry files to open formats (MGF, mzML) on multiple platforms) — CompOmics/ThermoRawFileParser
- **Aerith** (read and write mass spectrum scans and manage windowed spectrum data within R workflow) — xyz1396/Aerith

## Evaluation signals

- Extracted m/z range matches the specified window boundaries (isoCenter ± isoWidth/2) with no off-by-one or boundary errors.
- All observed peaks within the window are retained; no peaks at window edges are incorrectly truncated or duplicated.
- Intensity values are positive and non-zero for all retained peaks; no negative or NaN values introduced by windowing.
- Extracted window contains the full isotopic envelope (typically 3–5 observed peaks for natural-abundance or SIP-labeled peptides); if fewer than 2 peaks are present, the window may be too narrow or the spectrum too noisy.
- The extracted spectrum can be successfully passed to annotatePrecursor or a downstream scoring function without format errors or missing metadata (charge state, scan ID).

## Limitations

- Windowing assumes the isolation window parameters are accurate and known; if isoCenter or isoWidth are miscalibrated, true isotopic peaks may be excluded or noise included.
- For very narrow isolation windows (< 2 m/z), baseline noise or spectral artifacts may dominate; widen the window or apply noise filtering before annotation.
- Thermo FT2 files from IonTrap scans may lack charge state information; charge must be inferred or provided separately for accurate isotopic pattern calculation.
- High-complexity spectra (e.g., overlapping precursor ions from different charge states) may require deconvolution or peak separation before windowing to avoid false matches.

## Evidence

- [other] Load FT1 scan 107695 from the mass spectrum file using mzR or Raxport-processed FT2 input. Extract the m/z range 880–890 from the full scan spectrum.: "Load FT1 scan 107695 from the mass spectrum file using mzR or Raxport-processed FT2 input. Extract the m/z range 880–890 from the full scan spectrum."
- [intro] Aerith is an R package that provides interfaces to read and write mass spectrum scans: "Aerith is an R package that provides interfaces to read and write mass spectrum scans"
- [intro] Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files: "Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files"
- [readme] Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans.: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans."
- [other] Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak envelope: "Call annotatePrecursor with the peptide sequence HSQVFSTAEDNQSAVTIHVLQGER, charge state +3, C13 labeling, probability 0.0107, isoCenter 886.65, and isoWidth 4.0 to compute theoretical isotopic peak"
