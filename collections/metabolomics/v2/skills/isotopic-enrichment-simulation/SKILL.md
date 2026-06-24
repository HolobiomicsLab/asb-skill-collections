---
name: isotopic-enrichment-simulation
description: Use when you have a peptide sequence and need to predict its theoretical
  m/z values under partial or complete isotopic enrichment (e.g., 1% natural 13C abundance,
  50% 13C labeling, or other SIP conditions).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Aerith
  - R
  - Rcpp
  - mzR
  - MSnbase
  - Sipros
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans
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

# isotopic-enrichment-simulation

## Summary

Generate theoretical isotopic peak envelopes and B/Y ion spectra for peptides with specified stable isotope labeling patterns and enrichment probabilities. This skill enables quantitative prediction of how labeled peptides will appear in mass spectrometry data, supporting validation and interpretation of SIP (stable isotope probing) experiments.

## When to use

You have a peptide sequence and need to predict its theoretical m/z values under partial or complete isotopic enrichment (e.g., 1% natural 13C abundance, 50% 13C labeling, or other SIP conditions). Use this skill before or after MS data acquisition to validate peptide identifications, troubleshoot peak assignments, or design SIP labeling experiments with known isotopic atom targets and incorporation probabilities.

## When NOT to use

- You are analyzing unlabeled peptides with no isotopic enrichment — natural isotopic abundances are already implicit and require no special simulation.
- Your input is experimental MS/MS data already aligned to a known peptide — use scoring/matching algorithms instead of simulation.
- You need to model peptides with non-standard amino acids or post-translational modifications not supported by the sequence parser.

## Inputs

- Peptide amino acid sequence (string, e.g., 'HSQVFSTAEDNQSAVTIHVLQGER')
- Isotopic atom identifier (string, e.g., 'C13')
- Enrichment probability (numeric, 0.0–1.0; e.g., 0.01 for natural, 0.50 for 50% labeling)
- Charge state range (integer vector, e.g., 1:2 for +1 and +2 ions)

## Outputs

- AAspectra object with slots: spectra (data frame with MZ, intensity, fragment annotations)
- Filtered ion table (data frame; rows = fragment ions, columns = m/z, charge, isotope pattern, intensity)
- TSV or structured data frame export of theoretical spectrum

## How to apply

Call getSipBYionSpectra() with the peptide sequence, specify the isotopic atom (e.g., C13), set the enrichment probability (0.01 for 1% natural abundance, 0.50 for 50% labeling), and define charge states (typically 1:2 for singly and doubly charged ions). The function returns an AAspectra object containing MZ values, intensities, and fragment annotations. Filter the resulting spectra table to retain only ions below a specified mass threshold (e.g., m/z < 2000) to match your instrument's detection range. This produces a structured theoretical spectrum amenable to comparison with experimental data via similarity scoring or visual validation.

## Related tools

- **Aerith** (Primary R package implementing getSipBYionSpectra() and theoretical isotopic envelope calculation for peptides with flexible SIP enrichment specifications) — https://github.com/xyz1396/Aerith
- **R** (Runtime environment for executing Aerith functions and post-processing theoretical spectra)
- **Rcpp** (High-performance C++ backend for efficient isotopic peak convolution and envelope generation)
- **mzR** (Bioconductor package for parsing experimental mzML and MGF files to compare against theoretical spectra)
- **MSnbase** (Bioconductor package for handling pepXML and PSM (peptide-spectrum match) data structures)
- **Sipros** (Upstream SIP peptide search engine producing TSV outputs that can be validated or reprocessed using theoretical spectra from Aerith) — https://github.com/thepanlab/sipros5

## Examples

```
library(Aerith); result <- getSipBYionSpectra(sequence='HSQVFSTAEDNQSAVTIHVLQGER', isotope_atom='C13', enrichment_prob=0.01, charge_states=1:2); filtered <- result@spectra[result@spectra$MZ < 2000, ]; write.table(filtered, 'theoretical_spectrum.tsv', sep='\t', row.names=FALSE)
```

## Evaluation signals

- Returned m/z values are numeric, sorted in ascending order, and all fall below the specified mass threshold (e.g., m/z < 2000).
- Isotopic peak patterns match expected fine structure for the specified enrichment probability (e.g., 1% 13C shows dominant monoisotopic peak with small M+1 satellites; 50% 13C shows multimodal envelope).
- Fragment annotations correctly identify B and Y ion types with expected mass differences (neutral loss of H₂O or NH₃ when applicable).
- Intensity values sum to approximately 1.0 (normalized) and reflect isotopic abundance predictions from sequential convolution or Monte Carlo simulation.
- Output AAspectra object schema validates: spectra slot is a data frame with required columns (MZ, intensity, fragment_annotation, charge_state).

## Limitations

- Supports B and Y ions only; neutral losses and immonium ions are not modeled in the current getSipBYionSpectra() workflow.
- Enrichment model assumes uniform incorporation probability across all eligible atoms; does not account for positional isotope effects or incomplete labeling at specific residues.
- Sequential convolution algorithm for peptides may exhibit precision loss at very high charge states (>3) or for very long sequences (>100 amino acids); consider Monte Carlo for these edge cases.
- Theoretical predictions assume ideal mass spectrometry conditions and do not model instrument-specific effects (detector saturation, baseline noise, peak broadening due to calibration drift).
- Requires manual specification of isotopic atom and enrichment probability; automatic inference from experimental data is not provided.

## Evidence

- [other] getSipBYionSpectra computes theoretical B and Y ion m/z values for a peptide sequence with specified isotopic atom (C13), incorporation probability (0.01), and charge states (1:2), returning an AAspectra object: "getSipBYionSpectra computes theoretical B and Y ion m/z values for a peptide sequence with specified isotopic atom (C13), incorporation probability (0.01), and charge states (1:2), returning an"
- [intro] calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment"
- [abstract] employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate isotopic distributions: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [other] spectra slot contains MZ, intensity, and fragment annotations that can be filtered to retain only peaks below a specified mass threshold: "spectra slot contains MZ, intensity, and fragment annotations that can be filtered to retain only peaks below a specified mass threshold"
