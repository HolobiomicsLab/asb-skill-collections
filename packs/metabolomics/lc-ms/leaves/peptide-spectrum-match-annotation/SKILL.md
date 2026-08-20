---
name: peptide-spectrum-match-annotation
description: Use when when you have a peptide sequence, observed MS2 spectrum peaks (m/z, intensity, charge state), and need to determine which theoretical fragment ions (B and Y ions) match the observed data—particularly in stable isotope probing (SIP) experiments where peptides carry heavy isotope labels (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3648
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - Raxport
  - R
  - mzR
  - MSnbase
  - Sipros
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peptide-spectrum-match-annotation

## Summary

Annotate observed MS2 peaks by matching them against theoretical B and Y ion envelopes calculated for a peptide sequence with specified isotopic labeling parameters. This skill enables validation and quantification of peptide identifications in stable isotope labeling experiments by scoring the correspondence between measured and expected fragment ion distributions.

## When to use

When you have a peptide sequence, observed MS2 spectrum peaks (m/z, intensity, charge state), and need to determine which theoretical fragment ions (B and Y ions) match the observed data—particularly in stable isotope probing (SIP) experiments where peptides carry heavy isotope labels (e.g., 13C, 15N, 2H) at known incorporation probabilities. Use this skill to produce a scored table of matched B/Y ions with residue-position-specific isotope label counts.

## When NOT to use

- Input spectrum is MS1 or contains no B/Y ion fragments (e.g., internal fragments only)—annotatePSM targets MS2 data with sequential fragmentation patterns
- Peptide sequence is unknown or ambiguous—annotatePSM requires a definitive sequence to calculate theoretical fragments
- Incorporation probability is not known or varies significantly across residues—the method assumes a fixed, predefined labeling probability; variable or unknown labeling requires alternative annotation strategies

## Inputs

- Mass spectrum scan data (m/z, intensity pairs; from .FT2, mzML, MGF, or pepXML files)
- Peptide sequence (string, e.g., 'HYAHVDCPGHADYVK')
- Precursor m/z and charge state
- Isotope labeling metadata: isotope atom (C13, N15, 2H), incorporation probability (0.0–1.0)
- Isolation window width (Da, e.g., 5.0)

## Outputs

- ExpectedBYions table with matched B and Y ion m/z, intensity, and charge
- matchedIndices vector indicating which theoretical fragments matched observed peaks
- Residue-position-specific heavy isotope label counts per fragment
- Summary statistics (e.g., annotation coverage, intensity correlation)

## How to apply

Load the raw mass spectrum scan (e.g., from .FT2, mzML, or MGF formats using Raxport or mzR). Define the peptide sequence, charge state(s), isotope atom (C13, N15, etc.), and incorporation probability (e.g., 0.52 for 52% labeling). Use Aerith's sequential convolution algorithm to calculate theoretical isotopic peak envelopes for all B and Y fragment ions of the peptide. Run annotatePSM, which accepts observed peak data and the theoretical envelopes, scores matches using a probability threshold (typically the incorporation probability), and returns an ExpectedBYions table with matchedIndices indicating which theoretical fragments matched observed peaks. Filter results to non-negative matchedIndices to extract only successful annotations. Compute residue-position-specific counts reflecting the number of heavy isotope labels per fragment position for downstream quantification and validation.

## Related tools

- **Aerith** (Core R package for theoretical isotopic peak envelope calculation (sequential convolution for peptide fragments) and PSM scoring/annotation via annotatePSM function) — https://github.com/xyz1396/Aerith
- **Raxport** (Extracts MS2 scans from Thermo .FT2 raw files into formats compatible with Aerith parsing) — https://github.com/xyz1396/Raxport.net
- **mzR** (Bioconductor package for direct parsing of mzML and MGF files as alternative data inputs)
- **MSnbase** (Bioconductor package for parsing pepXML files containing candidate peptide-spectrum matches)
- **Sipros** (Upstream peptide identification and sequencing engine that produces TSV outputs compatible with Aerith annotation) — https://github.com/thepanlab/sipros5

## Evaluation signals

- matchedIndices contains only non-negative values and count matches the number of observed peaks successfully assigned to theoretical B/Y ions
- Annotated fragment ions satisfy mass accuracy constraints (theoretical m/z within 5 ppm or isolation window width of observed m/z)
- Residue-position label counts are integers ≥ 0 and ≤ theoretical maximum (number of eligible C, N, or other atoms per position)
- Isotopic envelope peak intensity ratios of matched fragments align with theoretical distributions (Monte Carlo fine structure simulation for verification)
- Summary statistics (e.g., number of matched B ions, Y ions, total annotation coverage) are reproducible across repeated runs with identical parameters

## Limitations

- annotatePSM only returns matchedIndices for B and Y ions; internal fragments and other fragmentation patterns are not annotated
- Scoring assumes a uniform, fixed incorporation probability across all eligible positions in the sequence; variable or position-specific labeling is not modeled
- Annotation accuracy depends on correct specification of precursor m/z, charge state, and isolation window width; misspecification can result in false negatives
- The method does not distinguish between multiply-charged fragment ions and singly-charged ions with identical nominal m/z; resolving such ambiguities requires additional downstream filtering
- Heavy isotope labels at lower incorporation probabilities (<10%) may produce weak peak envelopes that fall below noise thresholds and fail to match observed data

## Evidence

- [other] annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, charge states, isotope atom, incorporation probability, precursor m/z, and isolation window width; returns ExpectedBYions table with matchedIndices: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence (HYAHVDCPGHADYVK), charge states (1:2), isotope atom (C13), incorporation probability (0.52), precursor m/z, and"
- [abstract] Sequential convolution is used to calculate theoretical isotopic peak envelopes for B and Y ion fragments: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] Aerith calculates theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Aerith supports flexible specification of isotopic abundances for stable isotope probing experiments with any degree of isotopic enrichment: "Unlike existing tools, Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic"
- [intro] Aerith accepts spectral data in multiple formats including Raxport-processed FT2, mzML, MGF, pepXML, and Sipros TSV files: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros"
- [readme] Raxport extracts scans from raw files generated by ThermoFisher mass spectrometers into .FT2 files: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans."
