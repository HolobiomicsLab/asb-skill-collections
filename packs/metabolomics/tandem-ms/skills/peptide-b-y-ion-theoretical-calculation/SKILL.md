---
name: peptide-b-y-ion-theoretical-calculation
description: Use when when you have a peptide sequence and need to predict which fragment ions (B and Y series) should appear in an MS2 spectrum at a known isotopic abundance (e.g., natural 13C at 1.07%, or stable isotope labeling at 50% enrichment).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  - Raxport
  - Rcpp
  techniques:
  - tandem-MS
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

# peptide-b-y-ion-theoretical-calculation

## Summary

Calculate theoretical B and Y ion isotopic envelopes for peptide sequences at specified isotopic enrichment levels (natural or labeled). This foundational step generates expected fragment mass distributions needed to match experimental MS2 peaks and annotate fragment ions.

## When to use

When you have a peptide sequence and need to predict which fragment ions (B and Y series) should appear in an MS2 spectrum at a known isotopic abundance (e.g., natural 13C at 1.07%, or stable isotope labeling at 50% enrichment). Required before PSM annotation or spectrum scoring to establish the theoretical reference for peak matching.

## When NOT to use

- Input is already an observed peak list with assigned fragment annotations—use this skill to GENERATE the reference, not validate existing assignments.
- Peptide sequence is unknown or ambiguous—theoretical calculation requires unambiguous amino acid composition.
- Isotope enrichment level is not quantified or mixed within the sample—the algorithm requires a single, known isotopic abundance value to generate valid envelopes.

## Inputs

- peptide sequence (string)
- isotope type (e.g., 'C13')
- isotope probability (decimal: 0.0107 for natural abundance, 0.5 for 50% labeling)
- fragment charge states (integer list, typically [1, 2])
- precursor m/z (float)
- isolation window width (Da, e.g., 4.0)

## Outputs

- ExpectedBYions table
- theoretical m/z values per B and Y fragment
- isotopic envelope intensities per fragment
- matchable ion indices for each amino acid position

## How to apply

Provide the peptide sequence, isotope type (C13 or other), isotope probability matching your sample (0.0107 for natural 13C abundance), fragment charge states (typically 1 and 2), and precursor m/z. The algorithm uses sequential convolution to construct the isotopic envelope for each theoretical B and Y ion fragment by iteratively convolving amino acid isotopic patterns. The result is a table of expected m/z values and their relative intensities for each fragment position and charge state, which can then be compared against observed peaks from the scan.

## Related tools

- **Aerith** (R package that provides the sequential convolution algorithm and ExpectedBYions table generation interface; accepts isotope parameters and peptide sequence to calculate theoretical B/Y ion isotopic envelopes) — https://github.com/xyz1396/Aerith
- **R** (Runtime environment for executing Aerith package functions)
- **Rcpp** (Compiled backend for fast isotopic convolution calculations in Aerith)

## Evaluation signals

- ExpectedBYions table contains entries for all valid B and Y ion positions (1 to peptide_length − 1)
- Each fragment entry has non-negative m/z values and isotopic intensity distributions that sum to 1.0 or 100%
- Theoretical m/z values match expected mass calculations: B_n = sum(amino_acid_masses[0:n]) + H, Y_n = sum(amino_acid_masses[n:end]) + H + H2O
- Isotopic fine structure reflects the specified isotope probability (e.g., natural C13 envelopes show characteristic M+1, M+2 peaks with ~1% relative heights per carbon)
- Fragment charge states (if multiple) produce m/z values that differ by the reciprocal of charge state difference

## Limitations

- Sequential convolution algorithm scales linearly with peptide length; very long peptides (>100 amino acids) may show computational overhead but remains feasible.
- Isotopic envelope calculation assumes uniform enrichment across all atoms of the specified element; partial labeling at specific positions is not supported by the reported algorithm.
- Natural abundance calculation (0.0107 for C13) assumes standard Earth isotopes; non-standard or highly fractionated samples require adjusted probability input.
- B and Y ion theory does not account for neutral losses (e.g., loss of water or ammonia) that can produce secondary fragment peaks; the output represents unmodified ions only.

## Evidence

- [abstract] Sequential convolution for peptide fragments: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites"
- [intro] B and Y ion isotopic envelope calculation: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [other] annotatePSM function accepts isotope parameters: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence, fragment charge states (1:2), isotope type (C13), isotope probability (0.0107 for natural abundance)"
- [other] ExpectedBYions output table with matched indices: "returning an ExpectedBYions table where matched fragments have non-negative matchedIndices and residuePositions indicating which amino acid positions contribute to observed peaks"
- [other] Natural C13 abundance value: "peptide sequence HSQVFSTAEDNQSAVTIHVLQGER using Aerith's file parsing interface. 2. Calculate theoretical B and Y ion isotopic envelopes for the peptide at 1.07% 13C enrichment"
