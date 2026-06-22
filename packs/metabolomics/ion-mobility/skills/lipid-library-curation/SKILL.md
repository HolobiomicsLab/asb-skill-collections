---
name: lipid-library-curation
description: Use when you have obtained MobiLipid or a similar IM-MS lipidomics package that bundles a CCS reference library for labeled lipids, and you need to verify library integrity, validate that all expected lipid species are present with plausible numeric CCS values, and prepare a canonical curated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MobiLipid
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- MobiLipid aims to streamline lipidomics workflows by offering a fully automated solution for assessing and correcting collision cross section (CCS) bias
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid_cq
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01253
  all_source_dois:
  - 10.1021/acs.analchem.4c01253
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct and Validate Collision Cross Section Reference Library for Labeled Lipids

## Summary

Curate and validate a structured collision cross section (CCS) reference library for isotope-labeled lipids (e.g., U13C) by extracting, parsing, and quality-checking CCS values from a distributed package. This skill ensures the library meets physical and structural constraints required for downstream CCS bias assessment in ion mobility–mass spectrometry (IM-MS) lipidomics.

## When to use

You have obtained MobiLipid or a similar IM-MS lipidomics package that bundles a CCS reference library for labeled lipids, and you need to verify library integrity, validate that all expected lipid species are present with plausible numeric CCS values, and prepare a canonical curated version for use in CCS bias correction workflows.

## When NOT to use

- You are using a non-isotope-labeled lipid CCS library or a library not bundled with MobiLipid—this skill is specific to U13C-labeled reference libraries.
- Your input CCS values are already corrected or bias-adjusted—this skill curates raw reference libraries, not corrected measurements.
- You need only to run CCS bias correction on already-measured data without verifying the library itself—use the provided library file directly if trust in the distributor is sufficient.

## Inputs

- MobiLipid repository (GitHub clone or ZIP download)
- DTCCS_N2 reference library CSV file (e.g., 'U13C_DT_CCS_library.csv')

## Outputs

- Curated and validated CCS library table (CSV or TSV format)
- Library validation report (row counts, CCS range statistics, missing/duplicate flags)

## How to apply

Clone or download the MobiLipid repository and locate the DTCCS_N2 reference library file (e.g., 'U13C_DT_CCS_library.csv'). Parse the CSV into a structured table with columns for lipid class, lipid species identifier, and CCS reference value. Validate that all U13C-labeled lipid entries expected in the library are present, that CCS values are numeric, and that they fall within physically plausible ranges (typically 50–300 Ų for small lipids). Check for missing values, duplicates, and nomenclature consistency. Export the validated table as a canonical output file (CSV or TSV) for use as input to CCS bias calculation and correction steps in the MobiLipid workflow.

## Related tools

- **R** (Scripting language for parsing, validating, and exporting the library table; commonly used to check data types, ranges, and completeness) — https://cran.r-project.org/
- **MobiLipid** (Parent tool that bundles the DTCCS_N2 library; curated library is consumed by MobiLipid's CCS bias calculation and correction workflows) — https://github.com/FelinaHildebrand/MobiLipid

## Examples

```
# In R: Load, validate, and export the DTCCS_N2 library
library <- read.csv('U13C_DT_CCS_library.csv')
validated <- library[library$CCS >= 50 & library$CCS <= 300 & !is.na(library$CCS), ]
write.csv(validated, 'U13C_DT_CCS_library_curated.csv', row.names = FALSE)
```

## Evaluation signals

- All expected U13C-labeled lipid species (across all lipid classes in the library) are present in the curated table with no missing rows.
- All CCS values are numeric and fall within the physically plausible range of 50–300 Ų (or appropriate range for the lipid size and charge state being studied).
- No duplicate entries exist for the same lipid species–adduct combination; nomenclature is consistent across all rows.
- Row and column counts match expectations from library documentation; no null or malformed entries remain.
- Curated table successfully imports without type errors or parsing warnings into MobiLipid CCS bias calculation workflow.

## Limitations

- Library curation is restricted to U13C-labeled lipids; unlabeled or differently labeled lipids require separate reference libraries.
- CCS values are valid only for nitrogen (N2) drift gas at the conditions specified in the DTCCS_N2 library; values are not transferable to other drift gases or instruments without recalibration.
- CCS correction functions in MobiLipid require a minimum of 3 lipids per lipid class–adduct combination, so lipid classes with fewer detected U13C standards may not support bias correction.
- Nomenclature and adduct assignments in measured data must exactly match those in the reference library (e.g., 'PC', '[M+H]') for successful matching.

## Evidence

- [readme] library_file_location: "the .csv file of the DT CCS N2 library for U13C labeled lipids of yeast ('U13C_DT_CCS_library.csv') is downloaded"
- [other] validation_range_check: "Validate that all U13C labeled lipid entries are present and CCS values are numeric and within physically plausible ranges (typically 50–300 Ų for small lipids)"
- [intro] library_purpose: "Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code"
- [other] parsing_structure: "Parse the library data into a structured table format (CSV or TSV) containing lipid class, lipid species identifier, and CCS reference value columns"
- [other] export_step: "Export the curated library table as the canonical output file"
