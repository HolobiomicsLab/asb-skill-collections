---
name: stable-isotope-labeling-proteomics
description: Use when when you have mass spectrometry data (MS1/MS2 scans from ThermoFisher .raw files, mzML, or MGF) from cells or organisms cultured with stable isotope-enriched substrates (e.g., 13C, 15N, 2H) at any enrichment level (natural 1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0943
  tools:
  - Aerith
  - R
  - Raxport
  - mzR
  - MSnbase
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
- Aerith is an R package
- Extract visualization information from `.FT2` files
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

# stable-isotope-labeling-proteomics

## Summary

A proteomics workflow for tracing metabolic labels incorporated into peptides using stable isotope probing (SIP), enabling identification and quantification of isotopically enriched peptides through theoretical isotopic envelope prediction, peptide-spectrum matching, and interactive visualization.

## When to use

When you have mass spectrometry data (MS1/MS2 scans from ThermoFisher .raw files, mzML, or MGF) from cells or organisms cultured with stable isotope-enriched substrates (e.g., 13C, 15N, 2H) at any enrichment level (natural 1.07% abundance through 50%+), and you need to identify peptides whose isotopic fine structure reveals incorporation of the label, quantify the degree of enrichment, and match observed fragment ions to theoretical B/Y ion series computed under the isotopic regime of the experiment.

## When NOT to use

- Input data is already fully processed (deisotoped, deconvoluted to monoisotopic masses) and isotopic fine structure has been discarded; Aerith requires raw or minimally preprocessed centroided peaks to reconstruct isotopic envelopes.
- Experimental design does not specify isotopic enrichment level or atom type; Aerith requires explicit enrichment probability and isotope identity to compute theoretical spectra.
- Only unlabeled peptide identifications are needed and no SIP labeling was performed; use standard proteomics search engines (e.g., Mascot, Sequest) instead for faster turnaround.

## Inputs

- ThermoFisher .raw binary mass spectrometry scan files (Orbitrap or IonTrap)
- Spectral data in mzML, MGF, or FT2 (Raxport-processed) format
- Peptide amino acid sequence(s) as strings
- Experimental parameters: isotope atom type (C13, N15, H2), enrichment probability (decimal, 0.0107 for natural, 0–1.0 for labeled)
- Fragment ion charge state range (e.g., 1:2)
- Precursor m/z and isolation window width (Da)
- Observed MS2 peak list (m/z, intensity, charge state per scan)

## Outputs

- AAspectra object (S4 class) containing theoretical B/Y ion table with MZ, intensity, and fragment ion annotations
- ExpectedBYions table with matched fragment indices, residue positions, and ion assignments
- Filtered ion table (TSV or data frame) with peaks below specified m/z threshold
- Interactive PSM visualization with observed vs. theoretical isotopic envelope overlay
- Quality control summary: number of matched fragments, matchedIndices coverage, and isotopic pattern fit

## How to apply

Convert ThermoFisher .raw files to open formats (mzML, MGF) using ThermoRawFileParser or Raxport, then load the spectral data into Aerith using mzR or Raxport interfaces. For each peptide sequence of interest, compute theoretical B and Y ion isotopic envelopes at the experimental enrichment level (specified as atom type—e.g., C13—and enrichment probability—e.g., 0.01 for 1% or 0.50 for 50%) using getSipBYionSpectra() with sequential convolution algorithm. Run annotatePSM() to match observed MS2 peaks (m/z, intensity, charge) against the theoretical ions, specifying fragment charge states (typically 1:2), isolation window width (default 4.0 Da), and precursor m/z. Filter matched fragments to retain only those below your mass threshold (e.g., m/z < 2000 for high-mass peptides) and inspect residuePositions and matchedIndices to confirm assignments. Visualize PSMs interactively to validate that the observed isotopic pattern aligns with the theoretical envelope, confirming enrichment status and amino acid composition.

## Related tools

- **Aerith** (Core R package for calculating theoretical isotopic peak envelopes, scoring and visualizing PSMs, and interpreting SIP-labeled peptide spectra.) — https://github.com/xyz1396/Aerith
- **mzR** (Bioconductor package for parsing mzML and MGF spectral data files into R objects compatible with Aerith.)
- **MSnbase** (Bioconductor package for parsing pepXML files containing PSM search results to feed into Aerith.)
- **Raxport** (.NET tool to extract and convert ThermoFisher .raw files to .FT2 format, preserving charge information from Orbitrap scans for input to Aerith.) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Multi-platform .NET tool to convert ThermoFisher .raw files to mzML, MGF, or Parquet; supports cross-platform Linux/macOS/Windows deployment.) — https://github.com/CompOmics/ThermoRawFileParser
- **Sipros** (Peptide search engine for unlabeled or SIP-labeled tandem mass spectrometry; outputs TSV files of identified peptides and PSMs for downstream visualization in Aerith.) — https://github.com/thepanlab/sipros5

## Examples

```
library(Aerith); spec <- getSipBYionSpectra(sequence='HSQVFSTAEDNQSAVTIHVLQGER', isotope='C13', enrichment=0.01, charge=1:2); matched <- annotatePSM(observed_peaks, sequence='HSQVFSTAEDNQSAVTIHVLQGER', isotope='C13', prob=0.0107, charge=1:2, precursor_mz=1234.5, iso_width=4.0); filtered <- matched[matched$MZ < 2000, ]
```

## Evaluation signals

- ExpectedBYions table contains non-negative matchedIndices and residuePositions for all matched fragments, confirming successful ion assignment.
- Theoretical B/Y ion m/z values span the expected mass range (below m/z threshold) and match observed peaks within instrument mass accuracy (typically ≤ 5 ppm for Orbitrap).
- Observed isotopic peak cluster aligns visually with theoretical envelope in PSM visualization; full-width at half-maximum and relative peak heights should match computational predictions.
- Enrichment probability parameter correctly reflects experimental protocol; for natural 13C, enrichment should be 0.0107; for fully labeled samples, ≥ 0.50.
- Charge state assignments (1+ or 2+) for fragments are consistent with precursor charge and peptide length; all output fragments should have charge ≤ precursor charge.

## Limitations

- Aerith currently supports only MS1 and MS2 scans; higher-order MS (MS3+) fragmentation is not modeled.
- Raxport extracts charge information only from Orbitrap-acquired scans; IonTrap .raw files will lack charge annotation unless supplemented by external prediction.
- Monte Carlo simulation for fine isotopic structure (used for metabolites) may be computationally expensive for very high-mass peptides (>10 kDa) or at extreme enrichment levels; sequential convolution for peptide fragments is preferred.
- Isolation window width (default 4.0 Da) must match the instrument method used to acquire spectra; mismatches will cause false negatives if co-fragmented peptides fall outside the window.
- Natural 13C abundance (0.0107) assumes standard Earth isotope ratios; non-standard isotopic sources or fractionation effects are not accounted for.

## Evidence

- [intro] Stable isotope probing (SIP) is indeed a powerful technique for tracing the fate of metabolic labels incorporated into cells, offering insights into substrate assimilation and associated metabolic pathways.: "Stable isotope probing (SIP) is indeed a powerful technique for tracing the fate of metabolic labels incorporated into cells, offering insights into substrate assimilation and associated metabolic"
- [other] getSipBYionSpectra computes theoretical B and Y ion m/z values for a peptide sequence with specified isotopic atom (C13), incorporation probability (0.01), and charge states (1:2), returning an AAspectra object: "getSipBYionSpectra computes theoretical B and Y ion m/z values for a peptide sequence with specified isotopic atom (C13), incorporation probability (0.01), and charge states (1:2), returning an"
- [other] annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance), precursor m/z, and isolation window width (4.0 Da): "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance), precursor m/z,"
- [intro] Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files, and TSV files from the Sipros: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files, and TSV files from the Sipros"
- [readme] Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans.: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans."
- [abstract] employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] Aerith enables visualization and manual validation of both unlabeled and SIP-labeled peptide-spectrum matches (PSMs), facilitating interpretation of complex mass spectrometry data: "Aerith enables visualization and manual validation of both unlabeled and SIP-labeled peptide-spectrum matches (PSMs), facilitating interpretation of complex mass spectrometry data"
