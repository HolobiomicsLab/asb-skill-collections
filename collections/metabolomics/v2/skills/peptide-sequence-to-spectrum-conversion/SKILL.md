---
name: peptide-sequence-to-spectrum-conversion
description: Use when when you have a peptide sequence and need to predict its fragmentation pattern under specific isotopic labeling conditions (e.g., natural 13C abundance at 1%, or enriched 13C at arbitrary levels).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  - mzR
  - MSnbase
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
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

# peptide-sequence-to-spectrum-conversion

## Summary

Convert a peptide amino acid sequence into theoretical B and Y ion m/z values under specified isotopic enrichment conditions. This skill generates annotated fragment ion spectra (AAspectra objects) that represent expected mass-to-charge ratios for both natural and stable-isotope-labeled peptides, enabling comparison with experimental MS data.

## When to use

When you have a peptide sequence and need to predict its fragmentation pattern under specific isotopic labeling conditions (e.g., natural 13C abundance at 1%, or enriched 13C at arbitrary levels). Apply this skill before or alongside experimental spectrum matching to validate peptide identifications, especially in stable isotope probing (SIP) workflows where isotopic enrichment shifts m/z values and creates diagnostic peak envelopes.

## When NOT to use

- When you already have experimental mass spectra and need only to match them to sequences (use getSipBYionSpectra output as reference, not input).
- When the peptide sequence is unknown or unavailable; this skill requires an explicit sequence as input.
- When working with non-peptide molecules or metabolites; use Aerith's Monte Carlo or FFT-based methods for chemical formulas instead.

## Inputs

- Peptide amino acid sequence (character string, e.g. 'HSQVFSTAEDNQSAVTIHVLQGER')
- Isotope atom label (character, e.g. 'C13')
- Incorporation probability (numeric between 0 and 1, e.g. 0.01)
- Charge state range (integer vector, e.g. 1:2)

## Outputs

- AAspectra object with spectra slot containing: MZ (mass-to-charge ratios), intensity (peak heights), and fragment annotations (ion type, sequence position, charge state)
- Filtered ion table (data frame or TSV) with m/z < threshold
- Theoretical isotopic peak envelope for each fragment

## How to apply

Load the Aerith R package and invoke getSipBYionSpectra() with four arguments: the peptide sequence (character string), the isotope atom (e.g., 'C13'), the incorporation probability as a decimal (e.g., 0.01 for 1% natural abundance), and charge range (e.g., 1:2 for singly and doubly charged ions). The function computes all B and Y ion m/z values using sequential convolution algorithms and returns an AAspectra object whose spectra slot contains MZ, intensity, and fragment annotations. Filter the resulting ion table to retain only fragments below a specified mass threshold (e.g., m/z < 2000) if needed, then export as a data frame or TSV for downstream comparison with experimental spectra. The enrichment probability directly modulates isotopic peak fine structure; higher probabilities shift m/z upward and narrow the isotopic envelope, while lower probabilities broaden it.

## Related tools

- **Aerith** (Executes getSipBYionSpectra() function to compute theoretical B/Y ion spectra with flexible isotopic enrichment specification) — https://github.com/xyz1396/Aerith
- **R** (Runtime environment and package system for loading and running Aerith)
- **mzR** (Optional Bioconductor package for reading experimental mzML/MGF spectra to compare against theoretical output)
- **MSnbase** (Optional Bioconductor package for parsing pepXML files containing experimental PSM data)

## Examples

```
library(Aerith); spec <- getSipBYionSpectra(sequence='HSQVFSTAEDNQSAVTIHVLQGER', isotope='C13', prob=0.01, charge=1:2); filtered_ions <- spec@spectra[spec@spectra$MZ < 2000, ]; write.table(filtered_ions, 'theoretical_spectrum.tsv', sep='\t', row.names=FALSE)
```

## Evaluation signals

- AAspectra object contains non-empty spectra slot with three columns (MZ, intensity, annotations) and ≥ 1 row per charge state
- All m/z values in output are positive and fall within expected range for peptide fragments (e.g., > 50 m/z for singly charged ions of typical peptides)
- Filtered output (m/z < 2000) contains only rows where MZ < 2000; no rows violate the threshold
- Fragment annotations correctly label each ion (e.g., 'B5 +1', 'Y10 +2') with sequence positions matching the input peptide length
- Isotopic enrichment probability parameter is reflected in isotopic envelope width: lower probabilities (e.g., 0.01) produce broader envelopes; higher probabilities (e.g., 0.99) produce narrower envelopes centered at higher m/z

## Limitations

- getSipBYionSpectra generates only B and Y fragment ions; a and b ions, neutral losses, and internal fragments are not produced by this function.
- Isotopic envelope calculations assume homogeneous enrichment across all atoms of the specified type (C13); heterogeneous or partial labeling must be approximated via multiple runs or external post-processing.
- Very long peptides (> ~50 residues) may produce overlapping m/z values in low charge states, reducing discriminative power; charge state range and mass threshold selection are user-driven.
- The output does not include retention time prediction, collision cross-section (CCS), or ion mobility drift time; these must be integrated from external tools if needed.

## Evidence

- [results] getSipBYionSpectra generates B and Y ion m/z values with isotopic enrichment specification: "getSipBYionSpectra computes theoretical B and Y ion m/z values for a peptide sequence with specified isotopic atom (C13), incorporation probability (0.01), and charge states (1:2), returning an"
- [abstract] Aerith computes isotopic peak envelopes for peptide fragments using sequential convolution: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] Aerith enables flexible specification of isotopic abundances for SIP experiments: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment"
- [results] AAspectra object structure and filtering workflow: "Filter the resulting ion table to retain only fragments with m/z < 2000"
- [intro] Aerith workflow step for B/Y ion spectrum calculation: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [readme] README confirms Aerith's function for theoretical spectrum generation: "Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
