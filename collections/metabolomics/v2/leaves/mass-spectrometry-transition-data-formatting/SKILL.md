---
name: mass-spectrometry-transition-data-formatting
description: Use when when you have raw mass spectrometry transition data from a triple-quadrupole
  or other tandem MS instrument and need to prepare it for suspect chemical screening
  using EISA-EXPOSOME, or when merging custom compound libraries into the T3DB format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
  tools:
  - R Shiny
  - EISA-EXPOSOME
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c02697
  title: EISA-EXPOSOME
evidence_spans:
- We provide a Rshiny program for EISA-EXPOSOME
- We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown
  below
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eisa_exposome_cq
    doi: 10.1021/acs.analchem.3c02697
    title: EISA-EXPOSOME
  dedup_kept_from: coll_eisa_exposome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02697
  all_source_dois:
  - 10.1021/acs.analchem.3c02697
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-transition-data-formatting

## Summary

Conversion and validation of raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound identifiers) into the EISA-EXPOSOME tabular schema (.xlsx or .csv) to enable suspect chemical screening and database compatibility. This is a prerequisite data preparation step that ensures input files conform to the expected column structure and data types required by the EISA-EXPOSOME platform.

## When to use

When you have raw mass spectrometry transition data from a triple-quadrupole or other tandem MS instrument and need to prepare it for suspect chemical screening using EISA-EXPOSOME, or when merging custom compound libraries into the T3DB format. Specifically apply this skill when your data is in instrument-native, unstructured, or non-standard tabular formats and must be integrated into an EISA-EXPOSOME workflow.

## When NOT to use

- Input is already a validated EISA-EXPOSOME-compliant database file (.xlsx or .csv with correct schema) — skip to import step.
- You are working with full-scan or data-independent acquisition (DIA) spectra rather than targeted multiple reaction monitoring (MRM) transitions — EISA-EXPOSOME expects discrete precursor–product ion pairs.
- Retention time data is entirely absent and your use case requires RT-based peak extraction and feature disambiguation; RT is optional but strongly recommended for filtering and confidence.

## Inputs

- Raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound identifiers)
- Instrument-native or unstructured tabular data (e.g., CSV, TSV, Excel, XML from MS software)
- Reference T3DB database file (.xlsx format) for cross-validation

## Outputs

- Formatted transition database file (.xlsx or .csv) with columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID
- Validated database ready for import into EISA-EXPOSOME R Shiny application
- Data integrity report confirming schema compliance and reference compound validation

## How to apply

Obtain or prepare raw mass spectrometry transition data containing precursor m/z, product m/z, intensity, retention time (optional), and compound identifiers. Restructure the data into a tabular format with exactly six columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT (optional but recommended for peak extraction), and ID. Cross-reference formatted entries against the compiled T3DB reference database (provided in .xlsx format) to verify column alignment, data type consistency (numeric m/z and intensity values; string identifiers), and entry completeness. Validate the presence and correct formatting of reference compounds (e.g., Methamidophos with PrecursorMZ 142.0086, ProductMZ 94.0046, Intensity 100, RT 2.182, ID 1) as a sanity check. Export the validated table as .xlsx or .csv format and confirm file integrity by reloading into the R Shiny interface to verify all rows parse and filter operations function without error.

## Related tools

- **R Shiny** (Interactive interface for uploading, importing, and validating the formatted transition database; supports real-time schema checking and result filtering) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **EISA-EXPOSOME** (Downstream platform that consumes the formatted database for targeted peak extraction and suspect chemical screening; requires strict column schema compliance) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Evaluation signals

- File contains exactly six column headers: NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID (case-sensitive); no extra or missing columns.
- All PrecursorMZ and ProductMZ values are numeric and within expected m/z ranges (typically 50–2000 m/z); no text or missing values in these columns.
- All Intensity values are non-negative numbers; zero intensity is acceptable but may indicate low-abundance transitions.
- RT (retention time) values, where present, are numeric and within expected range (typically 0–60 minutes); absence of RT is acceptable.
- File successfully imports into R Shiny EISA-EXPOSOME interface without parsing errors; reference compound entries (e.g., Methamidophos) match T3DB reference values exactly; filtering and visualization functions operate without exception.

## Limitations

- RT (retention time) is not essential but is strongly recommended; absence of RT may reduce the effectiveness of targeted peak extraction and feature disambiguation in chromatography-rich samples.
- The schema assumes one precursor–product ion pair per row; multiple product ions from a single precursor must be formatted as separate rows with the same NAME and PrecursorMZ but different ProductMZ and ID values.
- No built-in handling for isomers or isobars; users must ensure NAME identifiers are unique or clearly distinguish stereoisomers and regioisomers within the ID or NAME field.
- Cross-referencing against T3DB is manual; no automated duplicate or conflict detection is described; users must verify that custom entries do not contradict or redundantly re-enter T3DB compounds.

## Evidence

- [readme] Database schema requirement: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [readme] Reference compound format and values: "Methamidophos|142.0086|94.0046|100|2.182|1"
- [other] Data preparation workflow: "1. Obtain or prepare raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, and compound identifiers). 2. Format the data into a tabular structure with required"
- [other] Validation and export step: "5. Export the validated database as .xlsx or .csv format and verify file integrity."
- [readme] R Shiny tool integration: "We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below, and you can filter the results according to the visualisation interface"
