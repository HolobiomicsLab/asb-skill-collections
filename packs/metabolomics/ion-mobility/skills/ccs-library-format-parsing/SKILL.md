---
name: ccs-library-format-parsing
description: Use when when you have received or cloned a CCS reference library (such as the DTCCSN2 library for U13C labeled lipids) bundled with lipidomics software and need to verify its integrity, understand its lipid class composition, or extract metadata before using it for CCS bias calculation or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3365
  tools:
  - R
  - data.table
  - MobiLipid
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- providing a R Markdown that integrates into IM-MS lipidomics workflows
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01253
  all_source_dois:
  - 10.1021/acs.analchem.4c01253
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Parse and validate CCS library file format

## Summary

Extract and validate the structure, metadata, and numeric ranges of a collision cross section (CCS) reference library file distributed with ion mobility–mass spectrometry lipidomics software. This skill ensures the library's lipid class coverage, CCS value distributions, and measurement conditions are correctly parsed and match documented specifications.

## When to use

When you have received or cloned a CCS reference library (such as the DTCCSN2 library for U13C labeled lipids) bundled with lipidomics software and need to verify its integrity, understand its lipid class composition, or extract metadata before using it for CCS bias calculation or correction in IM-MS workflows.

## When NOT to use

- Input CCS library is already validated and integrated into an active IM-MS analysis pipeline; use this skill only when receiving or auditing a new or unfamiliar library file.
- Your workflow does not require internal standardization or CCS bias correction (i.e., you are using only vendor-supplied external calibration).
- CCS library file is in a non-tabular format (e.g., binary, XML, or proprietary ion-mobility instrument format) that requires vendor-specific parsers.

## Inputs

- CCS library .csv file (e.g., U13C_DT_CCS_library.csv)
- Documentation or publication describing expected library structure and lipid class composition

## Outputs

- Parsed CCS library data frame with verified column structure
- Validation report summarizing lipid class coverage, CCS value ranges, and metadata integrity
- List of flagged anomalies or deviations from specification

## How to apply

Load the CCS library .csv file (e.g., U13C_DT_CCS_library.csv) into R using standard data import functions. Parse the file to extract all column headers and inspect rows for expected fields: lipid class, lipid species, adduct type, and CCS values. Verify that all documented lipid classes (e.g., Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG) are present. Check that CCS values are numeric and fall within physically plausible ranges for ion mobility data (typically 100–500 Ų for small organic ions). Cross-reference the observed lipid class counts and CCS value distributions against the repository documentation and publication claims. Document any deviations in a validation report.

## Related tools

- **R** (Language for parsing .csv library files, validating numeric ranges, and generating validation reports) — https://cran.r-project.org/
- **data.table** (R package for efficient import, parsing, and inspection of large CCS library .csv files)
- **MobiLipid** (Parent tool that distributes and uses the DTCCSN2 CCS library; this skill verifies the library component) — https://github.com/FelinaHildebrand/MobiLipid

## Examples

```
library(data.table); lib <- fread('U13C_DT_CCS_library.csv'); summary(lib); table(lib$LipidClass); range(lib$CCS, na.rm=TRUE)
```

## Evaluation signals

- All documented lipid classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, and any others in the library) are present in the parsed file with row counts matching repository claims.
- CCS values are numeric and within physically plausible ranges (no NaN, Inf, or negative values; typical range 100–500 Ų for small lipid ions).
- Column headers match the expected schema (e.g., LipidClass, LipidSpecies, Adduct, CCS_value, or equivalent nomenclature).
- Lipid species naming conventions are consistent with standard nomenclature (e.g., 'PC 32:0' format) and match examples given in documentation.
- No missing or malformed rows in critical fields; file parsing completes without truncation or encoding errors.

## Limitations

- Library file format assumes standard .csv delimiter (comma or tab); non-standard delimiters or quoting conventions will require format-specific adjustment.
- Validation checks lipid class coverage against publication and README claims, but cannot verify absolute accuracy of CCS values without independent reference measurements.
- Library is specific to U13C labeled lipids from yeast extract; validation does not apply to other labeling or biological sources.
- No changelog or version history is documented in the repository, so audit trail of library updates cannot be traced.

## Evidence

- [other] Locate and load the DTCCSN2 library file (U13C labeled lipids CCS reference data). 2. Parse the library file format and extract metadata including lipid classes, CCS values, and measurement conditions.: "Parse the library file format and extract metadata including lipid classes, CCS values, and measurement conditions."
- [other] Verify that all expected lipid classes are present and that CCS values are numeric and within physically plausible ranges for ion mobility data.: "Verify that all expected lipid classes are present and that CCS values are numeric and within physically plausible ranges for ion mobility data."
- [readme] It is provided with the code and called "U13C_DT_CCS_library.csv": "It is provided with the code and called "U13C_DT_CCS_library.csv"."
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG.: "lipid classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG."
