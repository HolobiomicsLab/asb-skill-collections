---
name: lipid-class-coverage-assessment
description: Use when when you have acquired a CCS reference library (such as DTCCSN2 for U13C labeled lipids) and need to verify that it contains the expected lipid classes, CCS values are physically plausible for ion mobility data, and coverage matches the library's advertised documentation before using it.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3678
  tools:
  - R
  - MobiLipid
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- providing a R Markdown that integrates into IM-MS lipidomics workflows
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid
schema_version: 0.2.0
---

# lipid-class-coverage-assessment

## Summary

Validates the structural completeness and CCS value distribution of a collision cross section (CCS) reference library for ion mobility-mass spectrometry lipidomics by verifying lipid class presence, extracting metadata, and confirming numeric ranges against documented specifications.

## When to use

When you have acquired a CCS reference library (such as DTCCSN2 for U13C labeled lipids) and need to verify that it contains the expected lipid classes, CCS values are physically plausible for ion mobility data, and coverage matches the library's advertised documentation before using it for CCS bias calculation or correction in IM-MS workflows.

## When NOT to use

- The library file is already validated and certified by the repository maintainers with a dated changelog.
- You are performing CCS bias calculation or correction and only need to use the library as-is without verification.
- The input data do not include lipid class annotations or are in a format other than tabular (e.g., raw mass spectrometry binary files).

## Inputs

- CCS reference library file (.csv format; e.g., U13C_DT_CCS_library.csv)
- Library metadata documentation (repository README, publication abstract, supplementary material)

## Outputs

- Validation report (text or structured summary) documenting library structure
- Lipid class coverage matrix (presence/absence by adduct type)
- CCS value statistics per lipid class (min, max, mean, SD)
- List of deviations or missing entries (if any)

## How to apply

First, parse the library file (typically a .csv file) and extract metadata including lipid class identifiers, lipid species, adduct types, and numeric CCS values. Second, validate that all expected lipid classes are present in the library—the MobiLipid DTCCSN2 library supports Cer, Co, DG, HexCer, LPC, LPE, PA, PC, PE, PG, PI, PS, SPH, TG, and AcCa across specific adduct combinations ([M+H], [M+Na], [M+NH4], [M-H], [M+HCOO]). Third, confirm CCS values are numeric and fall within physically plausible ranges for ion mobility measurements (no negative values, no anomalous outliers beyond 2–3 standard deviations of the distribution per lipid class). Fourth, cross-check the documented lipid class counts and CCS value ranges against the repository documentation and publication claims. Finally, generate a validation report summarizing library structure, lipid class coverage by adduct type, CCS distribution statistics, and flag any missing lipid classes or out-of-range values.

## Related tools

- **R** (Parsing and validation scripting: load .csv library file, extract and verify metadata, compute CCS distribution statistics, generate validation report) — https://cran.r-project.org/
- **MobiLipid** (Source tool that provides and distributes the DTCCSN2 library for U13C labeled lipids; validation confirms library integrity before use in CCS bias calculation workflows) — https://github.com/FelinaHildebrand/MobiLipid

## Examples

```
readRDS('MobiLipid_results.RData'); library_data <- read.csv('U13C_DT_CCS_library.csv'); lipid_classes <- unique(library_data$LipidClass); ccs_stats <- aggregate(library_data$CCS, by=list(library_data$LipidClass), function(x) c(min=min(x), max=max(x), mean=mean(x), sd=sd(x)))
```

## Evaluation signals

- All expected lipid classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, etc.) are present in the parsed library.
- CCS values are numeric, non-negative, and fall within domain-plausible ranges (e.g., typically 100–500 Ų for small lipid ions in nitrogen drift gas).
- Lipid class-adduct combinations in the library match those documented in the README (e.g., PC supports [M+H], [M+Na], [M+HCOO]).
- No records with missing, malformed, or duplicate lipid species entries within a lipid class.
- CCS value distribution per lipid class shows no extreme outliers (values ≥ 3σ outside the mean) that would suggest data entry errors.

## Limitations

- No changelog is provided in the MobiLipid repository, so version-to-version coverage changes cannot be tracked historically.
- Validation only confirms structural completeness and plausibility; it does not verify the accuracy or empirical quality of CCS values against independent ion mobility measurements.
- The library is specifically curated for U13C labeled lipids from yeast extract; validation does not apply to libraries for other organism sources or unlabeled lipids without explicit re-curation.

## Evidence

- [other] MobiLipid provides a newly established DTCCSN2 library for U13C labeled lipids distributed together with the code.: "MobiLipid provides a newly established DTCCSN2 library for U13C labeled lipids distributed together with the code."
- [other] Verify that all expected lipid classes are present and that CCS values are numeric and within physically plausible ranges for ion mobility data.: "Verify that all expected lipid classes are present and that CCS values are numeric and within physically plausible ranges for ion mobility data."
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG.: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid"
- [readme] The .csv file has to have the following headers: "File", "LipidClass", "LipidSpecies", "Adduct", "Label", "CCS": "The .csv file has to have the following headers: "File", "LipidClass", "LipidSpecies", "Adduct", "Label", "CCS""
