---
name: reference-dataset-validation-for-metabolite-ions
description: Use when after computing expected adduct ions for a metabolite using a derivatizing matrix ruleset, validate the predicted m/z values and adduct formulas against a curated reference dataset that documents which ions are actually produced by that matrix under standard ionization conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - RDKit
  - Met-ID
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
---

# Reference Dataset Validation for Metabolite Ions

## Summary

Validate predicted metabolite adduct m/z values against published reference datasets (e.g., Nature Methods FMP-10 data) to ensure the derivatizing matrix ionization rules are correctly implemented and produce chemically plausible ions. This skill is essential for confirming that automated adduct enumeration workflows generate ions matching experimentally observed patterns.

## When to use

After computing expected adduct ions for a metabolite using a derivatizing matrix ruleset, validate the predicted m/z values and adduct formulas against a curated reference dataset that documents which ions are actually produced by that matrix under standard ionization conditions. Use this skill when the adduct enumeration module is newly configured, when testing support for a new derivatizing matrix, or when troubleshooting metabolite identification failures due to unexpected or missing ions.

## When NOT to use

- Input is a standard ionization mode (common [M+H]+ or [M-H]-) without a derivatizing matrix — use simpler, non-matrix-dependent adduct prediction instead.
- Reference dataset for the target matrix does not exist or is incomplete — validation cannot be performed until reference data is available.
- Metabolite input is already an observed m/z spectrum (not a structure) — reverse m/z lookup or spectral matching is the appropriate skill, not forward prediction validation.

## Inputs

- Metabolite SMILES string
- Derivatizing matrix identifier (e.g., 'FMP-10')
- Matrix-specific adduct ionization ruleset (table of adduct rules with mass shifts)
- Reference dataset for the matrix (curated adduct ions with formulas and expected m/z values)

## Outputs

- Validation report (predicted vs. reference adducts, match/mismatch status)
- Table of predicted adduct ions with formulas, mass shifts, and m/z values
- Flagged discrepancies (missing ions, unexpected ions, m/z deviations)
- Match rate and systematic bias metrics

## How to apply

Load the reference dataset for the target derivatizing matrix (e.g., FMP-10 reference from Nature Methods) into a structured format with documented adduct rules, mass shifts, and expected m/z values. For each metabolite input, compute predicted adducts using RDKit molecular weight calculations applied to the matrix-specific ionization ruleset. Compare the predicted adduct formulas, mass shifts, and m/z values against the reference entries using exact or near-exact matching (accounting for floating-point precision). Flag any discrepancies where predicted ions diverge from the reference (missing expected ions, extra unexpected ions, or m/z shifts outside tolerance). Return a validation report summarizing match rate, systematic biases, and flagged anomalies; use this feedback to refine the matrix profile or rule parameters. The reference dataset serves as ground truth because it encodes experimentally validated ionization behavior for the specific matrix.

## Related tools

- **RDKit** (Parses metabolite SMILES, constructs molecular graphs, and computes molecular weights for adduct m/z predictions) — https://www.rdkit.org/
- **Met-ID** (Integrates derivatizing matrix adduct enumeration and reference dataset validation for metabolite identification in mass spectrometry imaging) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- Predicted adduct formulas exactly match reference dataset entries for the same metabolite and matrix (100% formula match for all ions in reference).
- Computed m/z values fall within expected tolerance (typically <5 ppm or <0.005 Da, depending on instrument resolution) of reference m/z for each adduct.
- No systematic bias in mass shifts: the difference between predicted and reference m/z should be randomly distributed around zero, not consistently shifted in one direction.
- Validation report shows high match rate (>95%) for ions present in reference; any missing ions or extra ions are documented and justified by rule coverage or metabolite-specific chemistry.
- When reference dataset is extended with a new metabolite standard, predicted ions for that metabolite match the observed ions in >90% of cases.

## Limitations

- Reference dataset must be experimentally validated and maintained; incomplete or outdated reference data will produce false negatives (predicted ions marked as invalid when they are real).
- Validation depends on accurate SMILES input and correct matrix identifier; errors in structure or matrix assignment will cause systematic validation failures.
- RDKit molecular weight calculations assume standard isotopic composition; isotopically labeled metabolites or non-standard ionization pathways may produce ions outside the reference ruleset and will be flagged as discrepancies even if chemically real.
- The Met-ID software is under active development; database files may not update correctly on reinstall, requiring manual removal of cached database folders (noted in README for Windows, macOS, and Linux).

## Evidence

- [intro] Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] Adduct m/z values are computed using RDKit and compared against reference FMP-10 data from Nature Methods: "For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state. 4. Return a"
- [readme] The software is extensible to support any derivatizing matrix with locally configurable rules: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
- [readme] Reference FMP-10 adduct data is embedded in Met-ID and users can add custom spectra to the database: "The base version of Met-ID comes with a number of MS2 spectra collected from chemical standards with an FT-ICR using the FMP-10 chemical matrix. Met-ID allows the user to input MS2 spectra from"
