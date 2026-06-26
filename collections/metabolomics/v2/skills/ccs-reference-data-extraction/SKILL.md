---
name: ccs-reference-data-extraction
description: Use when you have obtained or need to prepare a DTCCS_N2 reference library
  for U13C-labeled lipids (typically provided as part of a lipidomics tool distribution)
  and need to extract, validate, and normalize its contents into a machine-readable
  table format before using it for CCS bias calculation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MobiLipid
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates
  into IM-MS lipidomics workflows
- MobiLipid aims to streamline lipidomics workflows by offering a fully automated
  solution for assessing and correcting collision cross section (CCS) bias
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

# ccs-reference-data-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and validate collision cross section (CCS) reference values for labeled lipids from a structured library file, converting them into a curated reference table for use in ion mobility–mass spectrometry quality control workflows. This skill ensures that CCS bias assessment and correction algorithms have access to canonicalized, numerically validated reference data.

## When to use

You have obtained or need to prepare a DTCCS_N2 reference library for U13C-labeled lipids (typically provided as part of a lipidomics tool distribution) and need to extract, validate, and normalize its contents into a machine-readable table format before using it for CCS bias calculation or correction against measured IM-MS data.

## When NOT to use

- You are using measured IM-MS CCS values directly without reference library comparison; this skill is for reference data preparation, not raw data processing.
- Your samples do not include U13C-labeled internal standards; the DTCCS_N2 library is specific to U13C lipids and will not correctly standardize unlabeled data.
- You already have a pre-validated, canonicalized CCS reference table in the exact format required by your analysis tool; re-extraction adds unnecessary overhead.

## Inputs

- U13C_DT_CCS_library.csv file from MobiLipid distribution
- Raw library data with lipid class, lipid species, and CCS columns

## Outputs

- Validated, curated CCS reference table (CSV/TSV format)
- Lipid class–species–CCS reference mapping
- Validation report (presence/absence of entries, numeric validity, range checks)

## How to apply

Locate the U13C_DT_CCS_library.csv file within the MobiLipid repository or tool package. Parse the CSV into a structured table, extracting columns for lipid class, lipid species identifier (using nomenclature consistent with the library), and corresponding CCS reference values. Validate that all expected U13C-labeled lipid entries are present and that CCS values are numeric and fall within physically plausible ranges (typically 50–300 Ų for small lipids). Check for missing values, duplicates, or out-of-range entries; flag or exclude records that fail validation. Export the curated, validated table as the canonical reference file in CSV or TSV format, ensuring it matches the input schema expected by downstream CCS bias calculation and correction functions.

## Related tools

- **MobiLipid** (Provides the DTCCS_N2 reference library file and serves as the end consumer of the extracted and validated CCS reference table for bias calculation and correction) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Language and environment for parsing CSV, validating numeric ranges, and exporting curated reference tables)

## Evaluation signals

- All expected U13C-labeled lipid entries are present in the output table with no rows omitted due to parsing errors or missing values.
- CCS values are numeric and fall within the physically plausible range of 50–300 Ų for small lipids; any out-of-range values are flagged or documented.
- Lipid class and species nomenclature in the curated table exactly matches the expected input schema for downstream MobiLipid CCS bias calculation functions.
- No duplicate lipid class–species–adduct records exist in the final reference table.
- The output CSV/TSV file can be successfully imported by MobiLipid's data input workflow without schema or data type errors.

## Limitations

- The DTCCS_N2 library is specific to U13C-labeled yeast lipid extract and cannot be used as a reference for unlabeled natural lipids or lipids from other organisms.
- CCS correction based on this library requires a minimum of 3 lipids per lipid class–adduct combination; lipid classes or adducts represented by fewer than 3 entries in the measured data cannot be corrected.
- The library supports only a defined set of lipid classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, AcCa, Co, LPE, PG, SPH) and specific adducts; lipid classes or adduct forms outside this scope cannot be validated against this reference.

## Evidence

- [other] Locate and extract the DTCCS_N2 reference library file for U13C labeled lipids from the package distribution. Parse the library data into a structured table format (CSV or TSV) containing lipid class, lipid species identifier, and CCS reference value columns.: "Locate and extract the DTCCS_N2 reference library file for U13C labeled lipids from the package distribution. Parse the library data into a structured table format (CSV or TSV) containing lipid"
- [other] Validate that all U13C labeled lipid entries are present and CCS values are numeric and within physically plausible ranges (typically 50–300 Ų for small lipids).: "Validate that all U13C labeled lipid entries are present and CCS values are numeric and within physically plausible ranges (typically 50–300 Ų for small lipids)."
- [readme] Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code: "Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code"
- [readme] This needs to be a .csv file containing the DT CCS N2 library. It is provided with the code and called 'U13C_DT_CCS_library.csv'.: "This needs to be a .csv file containing the DT CCS N2 library. It is provided with the code and called 'U13C_DT_CCS_library.csv'."
