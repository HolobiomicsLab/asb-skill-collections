---
name: psm-annotation-and-ion-matching
description: Use when when you have an MS2 scan with observed peak data (m/z, intensity, charge state), a known peptide sequence, and need to determine which observed ions correspond to B and Y fragment ions. Apply this skill particularly when working with natural abundance (1.
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

# PSM Annotation and Ion Matching

## Summary

Annotate peptide-spectrum matches (PSMs) by matching observed MS2 fragment ions (m/z, intensity, charge) to theoretical B and Y ion series calculated for a peptide sequence at specified isotopic enrichment. This skill enables validation and interpretation of fragment assignments in both unlabeled and stable-isotope-labeled proteomics data.

## When to use

When you have an MS2 scan with observed peak data (m/z, intensity, charge state), a known peptide sequence, and need to determine which observed ions correspond to B and Y fragment ions. Apply this skill particularly when working with natural abundance (1.07% 13C) or enriched stable-isotope labeled samples where isotopic envelope matching is critical for accurate PSM interpretation.

## When NOT to use

- Input is an already-validated PSM table from a database search engine (e.g., Sipros or Percolator output); use only if manual re-annotation or isotopic validation is required.
- The observed spectrum contains only MS1 data or precursor-level information; B and Y ion annotation requires MS2 spectra.
- Peptide sequence is unknown or ambiguous; annotatePSM requires a definite sequence to compute theoretical fragment envelopes.

## Inputs

- MS2 scan data (m/z, intensity, charge state per peak)
- Peptide amino acid sequence
- Precursor m/z and charge state
- Isolation window width (Da)
- Isotope type and natural abundance or enrichment level (e.g., 0.0107 for natural 13C)

## Outputs

- ExpectedBYions table with matchedIndices (non-negative when matched, negative when unmatched)
- residuePositions indicating amino acid positions contributing to each fragment ion
- Annotated fragment ion list with B/Y ion type and theoretical m/z assignments
- Tabular export of matched ions with intensity and residue position information

## How to apply

Load the experimental MS2 scan data (m/z, intensity, charge) and peptide sequence using Aerith's file parsing interface (supporting FT2, mzML, or MGF formats via mzR integration). Calculate theoretical B and Y ion isotopic envelopes for the peptide using sequential convolution, specifying the isotope type (C13), natural abundance probability (0.0107 for unlabeled; adjust for labeled samples), fragment charge states (typically 1–2), precursor m/z, and isolation window width (e.g., 4.0 Da). Run annotatePSM to match experimental ions against the theoretical envelopes. Extract the matched-ion subset where matchedIndices are non-negative and residuePositions indicate which amino acids contribute to each observed peak. Validate results by confirming coverage of expected B and Y series and checking for chimeric or noise peaks outside the isolation window.

## Related tools

- **Aerith** (R package for reading MS scans, calculating theoretical isotopic envelopes for peptide B/Y ions, executing annotatePSM annotation, and visualizing PSM results) — https://github.com/xyz1396/Aerith
- **Raxport** (Converts Thermo RAW files to FT2 format for input to Aerith's file parsing interface) — https://github.com/xyz1396/Raxport.net
- **mzR** (Bioconductor package integrated with Aerith to parse mzML and MGF spectral files)
- **MSnbase** (Bioconductor package integrated with Aerith to parse pepXML PSM files)
- **Sipros** (Peptide search engine that generates TSV PSM input files readable by Aerith for annotation and validation) — https://github.com/thepanlab/Sipros4
- **R** (Language and runtime for executing Aerith and dependent packages)

## Examples

```
Load scan 107728 from FT2 file and peptide HSQVFSTAEDNQSAVTIHVLQGER; calculate B/Y ion envelopes at 1.07% 13C using Aerith; run annotatePSM with precursor m/z, 4.0 Da isolation window, and fragment charges 1–2; export matched ions with residue positions to TSV.
```

## Evaluation signals

- Matched ions have non-negative matchedIndices and residuePositions corresponding to valid amino acid positions in the peptide sequence.
- B and Y ion series coverage is contiguous or near-contiguous (no unexplained gaps in expected fragment positions).
- Theoretical m/z values of matched fragments agree with observed m/z within the instrument's mass accuracy tolerance (e.g., <5 ppm for Orbitrap).
- Isotopic envelope fine structure (if present) aligns with expected 13C multiplet patterns for the specified enrichment level.
- Unmatched peaks fall outside the isolation window, are below noise threshold, or correspond to neutral loss or immonium ions not captured by B/Y ion model.

## Limitations

- annotatePSM matches only B and Y ion series; neutral loss ions (e.g., -H2O, -NH3), immonium ions, or internal fragments are not annotated.
- Matching accuracy depends on accurate precursor m/z and isolation window specification; incorrect window width can exclude or include off-target ions.
- Sequential convolution algorithm for isotopic envelopes may lose fine-structure detail in highly enriched samples; Monte Carlo simulation is available for fine isotopic structures but at higher computational cost.
- Performance on very large peptides (>40 amino acids) or highly complex spectra with many overlapping isotopic envelopes has not been detailed in the article.

## Evidence

- [other] annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance): "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance)"
- [other] returning an ExpectedBYions table where matched fragments have non-negative matchedIndices and residuePositions indicating which amino acid positions contribute to observed peaks: "returning an ExpectedBYions table where matched fragments have non-negative matchedIndices and residuePositions indicating which amino acid positions contribute to observed peaks"
- [other] Calculate theoretical B and Y ion isotopic envelopes for the peptide at 1.07% 13C enrichment using sequential convolution algorithm for peptide fragments: "Calculate theoretical B and Y ion isotopic envelopes for the peptide at 1.07% 13C enrichment using sequential convolution algorithm for peptide fragments"
- [abstract] employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites"
- [intro] Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros"
- [intro] calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files: "Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files"
- [intro] Aerith enables visualization and manual validation of both unlabeled and SIP-labeled peptide-spectrum matches (PSMs), facilitating interpretation of complex mass spectrometry data: "Aerith enables visualization and manual validation of both unlabeled and SIP-labeled peptide-spectrum matches (PSMs), facilitating interpretation of complex mass spectrometry data"
