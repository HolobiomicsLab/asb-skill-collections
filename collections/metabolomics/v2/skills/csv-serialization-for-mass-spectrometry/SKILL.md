---
name: csv-serialization-for-mass-spectrometry
description: Use when you have generated or curated a lipid spectral library (with
  precursor m/z, adduct information, charge states, retention times, and fragmentation
  patterns) and need to export it for use in either Excalibur-based DDA experiments
  on an Orbitrap mass spectrometer, or in Skyline for targeted.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Excalibur
  - Skyline
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- Excalibur compatible precursor list (for DDA analysis via orbitrap)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipid_spectrum_generator_cq
    doi: 10.1021/acs.analchem.2c04518
    title: Lipid Spectrum Generator
  dedup_kept_from: coll_lipid_spectrum_generator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04518
  all_source_dois:
  - 10.1021/acs.analchem.2c04518
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CSV Serialization for Mass Spectrometry

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill conditionally exports lipid spectral library data to CSV format in two distinct schemas: Excalibur-compatible precursor lists for DDA analysis on Orbitrap instruments, or Skyline-compatible transition lists for targeted proteomics workflows. The choice of schema determines which columns and row structures are serialized, enabling downstream instrument-specific or software-specific analysis.

## When to use

Use this skill when you have generated or curated a lipid spectral library (with precursor m/z, adduct information, charge states, retention times, and fragmentation patterns) and need to export it for use in either Excalibur-based DDA experiments on an Orbitrap mass spectrometer, or in Skyline for targeted transition-based workflows. The skill is triggered by a user's explicit format selection (Excalibur or Skyline) and the availability of fully annotated lipid spectral data.

## When NOT to use

- Spectral library data has not been fully generated or annotated (missing precursor m/z, charge state, or fragmentation patterns).
- Output is intended for a mass spectrometry software or instrument other than Excalibur or Skyline; use the generic MSP export instead.
- User has not made an explicit format selection or the selection is ambiguous.

## Inputs

- Generated lipid spectral library data (in-memory representation with lipid identities, adduct annotations, m/z values, charge states, retention times, and fragmentation patterns)
- User format selection parameter (string: 'Excalibur' or 'Skyline')

## Outputs

- CSV file with Excalibur-compatible precursor list (columns: precursor m/z, charge state, retention time; rows: one per lipid-adduct)
- CSV file with Skyline-compatible transition list (columns: precursor m/z, product ion m/z, and transition metadata; rows: one per precursor–product pair)

## How to apply

First, accept a format selection parameter from the user (Excalibur or Skyline). Load the generated lipid spectral library data, which must contain precursor m/z values, charge states, retention times, product ion m/z values, and fragmentation metadata for each lipid-adduct combination. For Excalibur format: extract precursor m/z, charge state, and retention time; serialize with Excalibur-required column headers and row structure optimized for DDA on Orbitrap. For Skyline format: extract precursor m/z, product ion m/z values, and transition-specific metadata; serialize with Skyline-required column headers matching the transition list structure. Finally, write the formatted CSV to a file with a naming convention that reflects the selected format. The rationale is that Excalibur and Skyline have incompatible CSV schemas—Excalibur expects precursor-centric rows for DDA scheduling, while Skyline expects precursor-product pairs for targeted methods—so conditional serialization ensures compatibility with the downstream analysis tool.

## Related tools

- **Excalibur** (Target mass spectrometry instrument control and DDA data acquisition software; the Excalibur CSV precursor list schema is the input format for scheduling DDA experiments on Orbitrap instruments)
- **Skyline** (Targeted proteomics and lipidomics data processing software; the Skyline CSV transition list schema enables import of precursor–product ion pairs for targeted method design and analysis)

## Evaluation signals

- For Excalibur output: CSV contains exactly the required columns (precursor m/z, charge state, retention time) with no extra columns; each row corresponds to one unique precursor with consistent numeric formats and charge state notation (+1, +2, etc.)
- For Skyline output: CSV contains precursor m/z and product ion m/z columns; each row represents a single transition; all m/z values are within the expected mass range for the lipid class and adduct type
- CSV file is valid and parseable (no encoding errors, malformed quotes, or inconsistent delimiters); row counts match the expected number of unique precursors (Excalibur) or precursor–product pairs (Skyline)
- Naming convention of the output file reflects the selected format (e.g., '_Excalibur.csv' or '_Skyline.csv')
- Spot-check: manually verify that precursor m/z and retention time values in the CSV match the internal library representation

## Limitations

- The skill depends on prior complete generation and annotation of the lipid spectral library; missing or malformed precursor, adduct, or fragmentation data will propagate into the CSV export.
- Excalibur and Skyline CSV schemas are tool-specific and may change with software version updates; users must verify schema compatibility with their installed tool version.
- The skill does not validate or cross-reference m/z values against reference standards or external databases; accuracy is limited by the underlying spectral library generation process and peer-reviewed fragmentation patterns.

## Evidence

- [other] accept user format selection (Excalibur or Skyline) as input parameter: "Accept user format selection (Excalibur or Skyline) as input parameter."
- [other] Excalibur format extraction and serialization: "For Excalibur format: extract precursor m/z, charge state, and retention time; serialize as CSV with Excalibur-required column headers and row structure."
- [other] Skyline format extraction and serialization: "For Skyline format: extract precursor m/z, product ion m/z values, and transition-specific metadata; serialize as CSV with Skyline-required column headers and transition list structure."
- [intro] Two distinct export formats available: "Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'."
- [readme] Lipid spectral library generation with adduct information: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
