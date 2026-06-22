---
name: in-silico-fragment-m-z-calculation
description: Use when when you have experimental UHPLC-HRMS/MS or direct infusion MS/MS data and need to identify lipid species by comparing observed fragment m/z values against a library of simulated fragments. Apply this skill when your lipid library is incomplete or specialized (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  techniques:
  - GC-MS
  - direct-infusion-MS
  - NMR
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch_cq
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# in-silico-fragment-m-z-calculation

## Summary

Generation of theoretical fragment m/z values for lipid species using in-silico fragmentation rules, enabling mass-to-charge ratio matching against experimental tandem MS data. This skill is foundational to lipid identification workflows where experimental fragment peaks must be matched to predicted fragmentation patterns across comprehensive lipid libraries.

## When to use

When you have experimental UHPLC-HRMS/MS or direct infusion MS/MS data and need to identify lipid species by comparing observed fragment m/z values against a library of simulated fragments. Apply this skill when your lipid library is incomplete or specialized (e.g., non-standard lipid types), requiring custom in-silico fragment prediction based on lipid structural properties (molecular formula, adduct type, lipid class).

## When NOT to use

- Your lipid species are already confidently identified by orthogonal methods (NMR, GC-MS standards); in-silico prediction is redundant.
- You lack machine-readable lipid structure definitions or fragmentation rules for your lipid classes of interest.
- Your experimental data are from Waters instruments; LipidMatch does not currently support Waters files, limiting the utility of pre-computed fragments.

## Inputs

- Lipid structure definitions (lipid name, molecular formula, adduct type)
- Fragmentation rules or mechanism templates for lipid classes
- User-generated lipid library in .csv format following LipidMatch schema

## Outputs

- In-silico fragmentation library with predicted fragment m/z values
- Library table (.csv) with lipid metadata and simulated fragment m/z columns
- Fragment m/z predictions for matching against experimental MS/MS data

## How to apply

Define lipid structures in the LipidMatch .csv schema format, specifying lipid names, molecular formulas, adduct types, and fragmentation rules. Apply in-silico fragmentation algorithms to compute expected fragment m/z values for each lipid entry across common adduct types (e.g., [M+H]+, [M+Na]+, [M−H]−). Store these predicted m/z values in the library table alongside lipid metadata. During identification, match experimental fragment m/z values (from peak picking tools like MZmine, XCMS, or MS-DIAL) against the pre-computed in-silico library using mass tolerance windows appropriate to your instrument's resolution (e.g., 5 ppm for Orbitrap). Score matches based on fragmentation pattern similarity; lipids with greater agreement between experimental and predicted fragment m/z patterns receive higher identification confidence.

## Related tools

- **LipidMatch** (Core software that implements in-silico fragmentation and fragment m/z matching against experimental tandem MS data) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature detection upstream of fragment m/z matching; integrates with LipidMatch workflow)
- **XCMS** (Alternative peak picking and alignment tool compatible with LipidMatch)
- **MS-DIAL** (Peak picking and spectral deconvolution tool that preprocesses data for LipidMatch)
- **Compound Discoverer** (Commercial peak picking software compatible with LipidMatch workflow)

## Evaluation signals

- In-silico library contains ≥500,000 lipid entries across ≥60 lipid types, matching the breadth of built-in LipidMatch libraries.
- .csv library file validates against LipidMatch schema (lipid names, molecular formulas, adduct types, in-silico fragment m/z columns present and non-empty).
- Fragment m/z predictions are consistent with known fragmentation pathways for the lipid class (e.g., characteristic head-group neutral losses for phospholipids).
- When integrated and tested on experimental UHPLC-HRMS/MS data, lipid identifications show improved recall for species in your specialized application without degradation of precision compared to built-in library alone.
- Manual inspection of ≥5 high-confidence identifications confirms that matched experimental fragments align with predicted in-silico m/z values within instrument tolerance (e.g., ±5 ppm for Orbitrap).

## Limitations

- LipidMatch does not currently support Waters instrument files, restricting applicability to certain laboratory environments.
- In-silico fragmentation accuracy depends on the completeness and correctness of fragmentation rules; misspecified or incomplete rules will produce incorrect predictions and false identifications.
- User-generated libraries must be manually curated and validated against known standards or literature; no automatic quality assessment is performed by LipidMatch.
- Fragment m/z matching relies on empirical mass tolerance thresholds; selection of inappropriate tolerance windows may cause false positives or false negatives depending on instrument resolution.

## Evidence

- [intro] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [readme] Over 500,000 lipid species in-silico library across 60+ lipid types: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] User-generated library integration mechanism with .csv format support: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [readme] Validated on multiple instrument types and fragmentation approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [intro] User library formatting specification requirement: "Create a user-generated lipid library in .csv format following LipidMatch schema specifications (lipid names, molecular formulas, adduct types, and in-silico fragment m/z values)"
- [readme] Waters file format not supported: "The software does not currently support Waters files"
