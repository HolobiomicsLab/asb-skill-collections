---
name: residue-position-mapping-to-spectrum-peaks
description: Use when when you have an MS2 spectrum (FT2 scan or mzML) with observed peak data (m/z, intensity, charge states), a peptide sequence, and need to annotate which amino acid residues generated each matched fragment ion—particularly in stable isotope labeling experiments where isotopic mass shifts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  - Raxport
  - mzR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# residue-position-mapping-to-spectrum-peaks

## Summary

Maps observed MS2 fragment ion peaks to specific amino acid positions in a peptide sequence by matching experimental m/z and intensity data against theoretical B and Y ion series calculated at specified isotope enrichment levels. This skill enables direct interpretation of which regions of a peptide contribute to observed spectral fragments.

## When to use

When you have an MS2 spectrum (FT2 scan or mzML) with observed peak data (m/z, intensity, charge states), a peptide sequence, and need to annotate which amino acid residues generated each matched fragment ion—particularly in stable isotope labeling experiments where isotopic mass shifts must be accounted for (e.g., 1.07% natural 13C abundance or higher SIP enrichment).

## When NOT to use

- Input spectrum is MS1 (precursor-level only); annotatePSM requires MS2 fragmentation data.
- Peptide sequence is unknown or ambiguous; residue position mapping requires an unambiguous sequence reference.
- Fragment ions are from non-standard cleavage (e.g., missed cleavage, complex fragmentation patterns); B/Y ion theory assumes standard tryptic or protease-specific cleavage.

## Inputs

- MS2 spectrum scan (FT2, mzML, or MGF format)
- Observed peak list with m/z, intensity, and charge state
- Peptide sequence (string)
- Fragment charge states (integer range, e.g., 1:2)
- Isotope type and probability (e.g., C13, 0.0107 for natural abundance)
- Precursor m/z value
- Isolation window width (Da, e.g., 4.0)

## Outputs

- ExpectedBYions table with theoretical B and Y ions
- Matched fragment annotations with matchedIndices
- Residue positions (amino acid indices) for each matched fragment
- Tabular export of matched-ion subset with residue assignments

## How to apply

Load the experimental MS2 scan using Aerith's file parsing interface (supporting FT2, mzML, or MGF formats). Define the peptide sequence, fragment charge states (typically 1–2 for B/Y ions), isotope type (e.g., C13), and isotope probability (0.0107 for natural abundance, or higher for SIP). Calculate theoretical B and Y ion isotopic envelopes using sequential convolution algorithm accounting for the isotopic distribution. Run annotatePSM with the observed peak data and theoretical ion table, specifying the precursor m/z and isolation window width (e.g., 4.0 Da). Extract the returned matchedIndices and residuePositions: matched fragments will have non-negative indices indicating which amino acid position(s) contributed to each observed peak. Validate by confirming that all matched peaks fall within the isolation window and that residue positions span the full peptide length.

## Related tools

- **Aerith** (Primary R package for parsing MS scans, calculating theoretical isotopic envelopes, and executing annotatePSM fragment ion matching and visualization.) — https://github.com/xyz1396/Aerith
- **Raxport** (Extracts MS2 scans from Thermo RAW files and exports to FT2 format for input to Aerith file parsing interface.) — https://github.com/xyz1396/Raxport.net
- **mzR** (Bioconductor package integrated into Aerith for direct parsing of mzML and MGF spectral files.)
- **R** (Runtime environment for executing Aerith package and annotatePSM function calls.)

## Examples

```
# R: Load Aerith, parse FT2 scan, calculate theoretical B/Y ions, and annotate PSM
library(Aerith)
scan_data <- read_scan('path/to/scan_107728.FT2')
theoretical_ions <- calculateBYions(peptide='HSQVFSTAEDNQSAVTIHVLQGER', charge_states=1:2, isotope='C13', enrichment=0.0107)
matched <- annotatePSM(observed_peaks=scan_data, theoretical_ions=theoretical_ions, precursor_mz=1234.56, isolation_width=4.0)
results <- extract_matched_residue_positions(matched)
```

## Evaluation signals

- All matched fragment peaks have non-negative matchedIndices (i.e., no unmatched fragments are assigned positions).
- Residue positions are contiguous integers spanning from position 1 to peptide length, with no gaps or out-of-range values.
- Observed m/z values of matched peaks fall within the theoretical m/z range ± 0.01 Da (or instrument mass accuracy tolerance) of the expected B/Y ions.
- Matched peaks respect the isolation window constraint: all matched m/z values lie within [precursor_mz ± isolation_window/2].
- For SIP experiments, matched peaks show expected isotopic mass shifts (e.g., +1.003 Da per 13C atom) consistent with the specified enrichment probability.

## Limitations

- annotatePSM assumes standard B and Y ion fragmentation; non-canonical fragmentation patterns (e.g., internal fragments, complex rearrangements) will not be mapped correctly.
- Isotope envelope calculation is approximate for very high enrichment (e.g., >90% 13C) due to Monte Carlo simulation limitations; natural abundance (1.07%) and moderate SIP labels (5–50%) are most reliable.
- Match quality depends on spectral peak picking; noisy or baseline-heavy scans may yield spurious or incomplete residue mappings.
- Precursor m/z and isolation window must be specified accurately; off-target values will exclude valid fragments or include noise peaks outside the true precursor population.

## Evidence

- [other] annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance), precursor m/z, and isolation window width (4.0 Da), returning an ExpectedBYions table where matched fragments have non-negative matchedIndices and residuePositions: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance), precursor m/z,"
- [other] Calculate theoretical B and Y ion isotopic envelopes for the peptide at 1.07% 13C enrichment using sequential convolution algorithm for peptide fragments.: "Calculate theoretical B and Y ion isotopic envelopes for the peptide at 1.07% 13C enrichment using sequential convolution algorithm for peptide fragments"
- [abstract] Aerith employs efficient algorithms including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites to accurately generate isotopic distributions.: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [readme] Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions, score and visualize the PSM (peptide and spectra match): "Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions, score and visualize"
- [intro] Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files"
