---
name: theoretical-fragment-ion-generation
description: Use when when you have a peptide sequence and need to predict its fragment
  ion spectrum for stable isotope labeling validation, particularly when comparing
  against observed mass spectrometry data with natural or enriched isotopic abundance
  (e.g., 1% or 50% 13C incorporation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Aerith
  - R
  - Rcpp
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

# theoretical-fragment-ion-generation

## Summary

Generate theoretical B and Y ion m/z values for a peptide sequence under specified isotopic labeling conditions (isotope type, enrichment probability, charge states). This enables comparison of predicted fragment patterns against experimental mass spectrometry data for validation of stable isotope probing experiments.

## When to use

When you have a peptide sequence and need to predict its fragment ion spectrum for stable isotope labeling validation, particularly when comparing against observed mass spectrometry data with natural or enriched isotopic abundance (e.g., 1% or 50% 13C incorporation). Apply this skill before PSM scoring or manual spectrum inspection to establish the expected isotopic fine structure.

## When NOT to use

- Input is already experimental mass spectrometry data (raw scans or peak lists) — use spectrum reading/preprocessing instead.
- Peptide sequence contains non-standard or post-translationally modified amino acids not supported by the isotopic calculation model.
- Analysis requires metabolite isotopic patterns rather than peptide fragments — use FFT-based metabolite calculation instead.

## Inputs

- peptide amino acid sequence (string, e.g., 'HSQVFSTAEDNQSAVTIHVLQGER')
- isotope atom specification (string, e.g., 'C13')
- enrichment probability (numeric, 0–1 range; 0.01 for natural, >0.01 for labeled)
- charge state range (integer vector, e.g., 1:2)

## Outputs

- AAspectra object with spectra slot containing MZ (m/z values), intensity, and fragment annotations
- filtered ion table (data frame or TSV) with m/z < threshold

## How to apply

Load the Aerith R package and invoke getSipBYionSpectra() with your peptide sequence, specifying the isotopic atom (e.g., C13), enrichment probability (0.01 for natural abundance, or higher for labeled samples), and charge state range (typically 1:2). The function returns an AAspectra object containing m/z, intensity, and fragment annotations. Filter the resulting spectrum to retain only fragments below your mass threshold (e.g., m/z < 2000) to match your instrument's dynamic range. The theoretical spectrum can then be exported as a structured data frame or TSV for downstream comparison with experimental spectra. Use sequential convolution for accurate isotopic distribution calculation across all fragment masses.

## Related tools

- **Aerith** (R package providing getSipBYionSpectra() function to compute theoretical B and Y ion m/z values with specified isotopic enrichment and charge states) — https://github.com/xyz1396/Aerith
- **R** (runtime environment for Aerith package execution)
- **Rcpp** (underlying C++ acceleration for efficient isotopic envelope calculation)

## Examples

```
library(Aerith); spectrum <- getSipBYionSpectra(sequence='HSQVFSTAEDNQSAVTIHVLQGER', isotope='C13', enrichment=0.01, charge=1:2); filtered <- spectrum@spectra[spectrum@spectra$MZ < 2000, ]; write.table(filtered, 'theoretical_spectrum.tsv', sep='\t', row.names=FALSE)
```

## Evaluation signals

- Verify that returned m/z values are strictly positive and increase monotonically with fragment size.
- Check that intensity values sum to approximately 1.0 (normalized probability distribution across isotopic peaks).
- Confirm that the number of returned peaks and intensity ratios match expected isotopic fine structure for the specified enrichment probability (e.g., at 1% 13C, monoisotopic peak should dominate).
- Validate that filtered spectrum contains only m/z values below the specified threshold (e.g., all MZ < 2000).
- Ensure fragment annotations correctly identify B and Y ions with expected length and charge states matching the input charge range.

## Limitations

- Algorithm assumes sequential convolution for peptide fragments; accuracy degrades for very long sequences or extreme enrichment levels not validated in training data.
- Only supports standard proteinogenic amino acids; post-translational modifications or non-standard residues must be handled separately or excluded.
- Enrichment probability parameter applies uniformly across all atoms of the specified isotope; heterogeneous labeling patterns cannot be modeled.
- m/z calculation assumes standard peptide ionization (protonation); other adduct types or charge assignment strategies are not directly supported.

## Evidence

- [other] getSipBYionSpectra() function behavior: "getSipBYionSpectra computes theoretical B and Y ion m/z values for a peptide sequence with specified isotopic atom (C13), incorporation probability (0.01), and charge states (1:2)"
- [other] AAspectra output structure: "returning an AAspectra object whose spectra slot contains MZ, intensity, and fragment annotations"
- [other] Filtering and export workflow: "Filter the resulting ion table to retain only fragments with m/z < 2000. Export the filtered AAspectra theoretical spectrum table as a structured data frame or TSV file."
- [abstract] Algorithm for isotopic distribution: "employs efficient algorithms—including sequential convolution for peptide fragments, Monte Carlo simulation for fine isotopic structures, and FFT-based methods for metabolites—to accurately generate"
- [intro] Aerith package scope: "Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
- [intro] SIP flexibility in Aerith: "Aerith supports flexible specification of isotopic abundances for stable isotope probing (SIP) experiments, allowing users to model compounds with any degree of isotopic enrichment"
