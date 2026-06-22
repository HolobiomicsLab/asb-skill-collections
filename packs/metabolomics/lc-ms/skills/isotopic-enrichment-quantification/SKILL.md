---
name: isotopic-enrichment-quantification
description: Use when you have MS2 spectra from peptides with known stable isotope enrichment (e.g., 52% ¹³C incorporation), a target peptide sequence, and you need to determine which B and Y ion fragments carry how many isotope labels at each position.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0543
  tools:
  - Aerith
  - Raxport
  - R
  - mzR
  - MSnbase
  - Sipros
  - ThermoRawFileParser
  techniques:
  - LC-MS
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

# isotopic-enrichment-quantification

## Summary

Quantify the incorporation and distribution of stable isotope labels (e.g., ¹³C) across peptide fragments by calculating theoretical isotopic peak envelopes, matching observed MS2 peaks to predicted B and Y ion patterns, and tabulating residue-position-specific label counts. This skill enables validation and interpretation of stable isotope probing (SIP) experiments in proteomics and metabolomics.

## When to use

Apply this skill when you have MS2 spectra from peptides with known stable isotope enrichment (e.g., 52% ¹³C incorporation), a target peptide sequence, and you need to determine which B and Y ion fragments carry how many isotope labels at each position. Use it to validate that observed fragment ions match theoretical isotopic envelopes, quantify label distribution across the peptide backbone, and generate summary statistics for SIP-based metabolic tracing studies.

## When NOT to use

- Input spectrum has no expected stable isotope labeling (unlabeled or natural abundance only); use standard peptide mass fingerprinting instead.
- Isotope incorporation probability is unknown or variable across the sample; the skill requires a fixed, pre-defined labeling parameter.
- Spectrum is very low resolution or noisy such that isotopic fine structure cannot be resolved; the theoretical envelopes will not match observed peaks reliably.

## Inputs

- Mass spectrum scan (MS2 data: m/z, intensity, charge state)
- Peptide sequence string
- Isotope specification (atom type, incorporation probability)
- Precursor m/z and charge state
- MS/MS isolation window width (Da)
- Raw or converted spectrum file (FT2, mzML, MGF, or pepXML)

## Outputs

- ExpectedBYions table with matchedIndices
- Matched B/Y ion fragments with assigned m/z and intensity
- Residue-position isotope label counts
- Summary statistics on labeling distribution
- Annotated PSM visualization

## How to apply

Load the raw mass spectrum file (e.g., FT2 format from Raxport or mzML/MGF via mzR) and extract the MS2 scan for your target peptide. Define the peptide sequence, specify the isotope atom (e.g., C13), and provide the incorporation probability (e.g., 0.52 for 52% labeling). Use Aerith's sequential convolution algorithm to compute theoretical isotopic peak envelopes for all B and Y ion fragments, accounting for the probabilistic distribution of labels at each atomic position. Run annotatePSM with your observed peak data (m/z, intensity, charge state), precursor m/z, and isolation window width (e.g., 5.0 Da) to score and match observed peaks against the theoretical envelopes. Filter results to retain only matches with non-negative matchedIndices, then extract the matched B/Y ions table and compute per-residue isotope label counts by summing the number of heavy atoms assigned to each fragment position.

## Related tools

- **Aerith** (Core R package for calculating theoretical isotopic peak envelopes of peptide precursors and B/Y ions, scoring and annotating PSMs, and visualizing isotopically enriched peptides) — https://github.com/xyz1396/Aerith
- **Raxport** (Extracts MS scans and metadata from Thermo RAW files and writes to FT2 format for downstream parsing by Aerith) — https://github.com/xyz1396/Raxport.net
- **mzR** (Bioconductor package integrated with Aerith for parsing mzML and MGF spectrum files)
- **MSnbase** (Bioconductor package integrated with Aerith for parsing pepXML peptide-spectrum match files)
- **Sipros** (Upstream peptide search engine providing PSM identifications (sequence, charge) that feed into Aerith's isotopic quantification workflow) — https://github.com/thepanlab/sipros5
- **ThermoRawFileParser** (Cross-platform tool to convert Thermo RAW files to open formats (mzML, MGF, Parquet) compatible with Aerith) — https://github.com/CompOmics/ThermoRawFileParser

## Examples

```
library(Aerith); spec <- readMS2Scan('X13_4068_2596_8182.FT2', scan=2596); ions <- annotatePSM(observed_peaks=spec$peaks, peptide='HYAHVDCPGHADYVK', isotope_atom='C13', incorporation_prob=0.52, precursor_mz=spec$precursor_mz, charge=2, isolation_width=5.0); matched <- ions[ions$matchedIndices >= 0, ]; label_counts <- tapply(matched$heavy_atom_count, matched$position, sum)
```

## Evaluation signals

- Matched B/Y ion indices are all non-negative; negative or missing indices indicate failed annotations and should trigger review of incorporation probability or peak picking parameters.
- Matched m/z values fall within the expected mass tolerance (e.g., <5 ppm for high-resolution Orbitrap data) of theoretical isotopic centroid positions; systematic offsets suggest calibration error.
- Residue-position label counts are integers ≥0 and ≤ the maximum number of carbon atoms at each position; fractional or out-of-range values indicate calculation error.
- The total number of heavy isotope labels across all matched fragments is consistent with the peptide's theoretical heavy-atom budget given the incorporation probability.
- Visualization of matched fragments overlaid on the observed spectrum shows clear peak alignment with theoretical isotopic envelopes; gaps or misalignments suggest suboptimal parameters.

## Limitations

- The skill assumes a fixed, homogeneous isotope incorporation probability across all atoms of a given type; heterogeneous labeling patterns require per-atom probability specification, which is not supported.
- Charge state determination relies on Orbitrap detection; IonTrap scans may lack reliable charge information in FT2 files, degrading annotation accuracy.
- High-order isotopic fine structure (Monte Carlo simulation for envelopes) is computationally expensive for large peptides (>50 amino acids); sequential convolution is more efficient but less precise.
- The skill requires accurate precursor m/z and isolation window width; errors in these parameters can lead to incorrect fragment assignment.
- Overlapping or multiplexed MS2 scans (e.g., from data-independent acquisition) are not directly supported; DIA data requires preprocessing into isolated fragment spectra.

## Evidence

- [abstract] Sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [other] annotatePSM accepts observed peak data, peptide sequence, isotope parameters, and returns ExpectedBYions table with matchedIndices: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence (HYAHVDCPGHADYVK), charge states (1:2), isotope atom (C13), incorporation probability (0.52), precursor m/z, and"
- [intro] Calculate theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Flexible specification of isotopic abundances for stable isotope probing experiments: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment"
- [intro] Stable isotope probing is a technique for tracing metabolic labels incorporated into cells: "Stable isotope probing (SIP) is indeed a powerful technique for tracing the fate of metabolic labels incorporated into cells, offering insights into substrate assimilation and associated metabolic"
- [intro] Aerith accepts spectral data in multiple formats including Raxport-processed FT2, mzML, MGF files: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros"
- [other] Workflow step: extract matched expected B/Y ions and compute residue-position counts reflecting heavy isotope labels: "Extract and tabulate the matched expected B/Y ions with their assigned m/z and intensity values. 6. Compute residue-position counts reflecting the number of heavy isotope labels per position"
