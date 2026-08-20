---
name: derivatizing-matrix-configuration
description: Use when you have a derivatizing matrix (e.g., TAHS or other publicly
  documented reagent) with known composition and ionization behavior that you want
  to use in Met-ID for metabolite annotation, and the matrix is not yet configured
  in your Met-ID installation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - Met-ID
  techniques:
  - CE-MS
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00633
  all_source_dois:
  - 10.1021/acs.analchem.5c00633
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# derivatizing-matrix-configuration

## Summary

Register and configure novel chemical derivatizing matrices (beyond FMP-10) into Met-ID to enable automated metabolite identification with non-standard adduct annotations in mass spectrometry imaging. This skill extends Met-ID's extensibility architecture to support any derivatizing reagent with defined ionization behavior and expected adduct forms.

## When to use

You have a derivatizing matrix (e.g., TAHS or other publicly documented reagent) with known composition and ionization behavior that you want to use in Met-ID for metabolite annotation, and the matrix is not yet configured in your Met-ID installation. You have access to the matrix's expected adduct forms (e.g., [M+matrix_adduct]+ ) and can obtain or have reference MS/MS spectra from chemical standards derivatized with that matrix.

## When NOT to use

- The derivatizing matrix has no documented or characterizable ionization behavior or expected adduct forms.
- You only need to analyze data already derivatized with FMP-10 or another matrix already configured in Met-ID; configuration is unnecessary.
- Met-ID's existing matrix registry already includes your desired matrix and you simply need to select it from the user interface.

## Inputs

- Met-ID configuration schema or plugin interface specification
- Derivatizing matrix properties: composition, ionization behavior, expected adduct forms
- Test set of reference metabolites with known derivatization behavior
- Reference MS/MS spectra from chemical standards derivatized with the new matrix (optional but recommended)
- Ground-truth adduct annotations or literature-reported adducts for test compounds

## Outputs

- Configuration file or plugin module for the new derivatizing matrix
- Registered matrix integrated into Met-ID's configuration loader or plugin registry
- Met-ID adduct annotations for test metabolites using the new matrix
- Validation report comparing predicted adducts to ground truth

## How to apply

First, review Met-ID's plugin or configuration interface by examining the existing FMP-10 matrix configuration to understand the expected schema (matrix composition, ionization behavior, characteristic adduct forms). Create a configuration file or plugin module specifying the new derivatizing matrix properties—composition, ionization mode (positive/negative), and all expected adduct forms it produces. Integrate the configuration into Met-ID's configuration loader or plugin registry by following the documented extension pattern. Run Met-ID on a test set of reference compounds (internal standards or known metabolites with documented derivatization behavior) using the newly registered matrix. Parse Met-ID's output adduct annotations and compare them against ground-truth literature values or standards to verify correct ion recognition and application. The skill succeeds when predicted adducts (e.g., [M+matrix_adduct]+ forms) match expected values for the test metabolites.

## Related tools

- **RDKit** (Powered computational chemistry library used internally by Met-ID for molecular structure handling and adduct annotation) — https://www.rdkit.org/
- **Met-ID** (Core metabolite identification platform with extensible matrix configuration system; hosts the plugin registry and configuration loader) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- Configuration file is syntactically valid and accepted by Met-ID's configuration loader without errors.
- New matrix appears in Met-ID's matrix selection interface or plugin registry after registration.
- Met-ID successfully runs on test metabolites using the newly registered matrix without crashes or missing-configuration errors.
- Adduct annotations output by Met-ID for test compounds match expected adduct forms (e.g., [M+matrix_adduct]+ or literature-reported ions) with 100% accuracy on reference standards.
- Comparison of predicted vs. ground-truth adducts shows concordance for all test metabolites; any discrepancies are documented and justified by matrix ionization characteristics.

## Limitations

- Met-ID is currently under development; database file updates may require manual removal of cached configuration directories (e.g., 'com.farmbio.metid' in AppData/Roaming on Windows or Library/Application Support on macOS) before re-installation.
- MacOS users may encounter functional issues with adding functional groups in the Met-ID interface; consult the repository issues tab for workarounds.
- Configuration extensibility depends on the matrix having well-characterized ionization behavior and documented adduct forms; novel matrices with poorly understood or highly variable ionization may yield unreliable annotations.
- All changes to the database and matrix registry only affect the specific Met-ID installation and do not sync across other installations or users.

## Evidence

- [other] Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10: "Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10 which was developed in-house."
- [other] Create a configuration file or plugin module for the second derivatizing matrix specifying the matrix composition, ionization behavior, and expected adduct forms: "Create a configuration file or plugin module for the second derivatizing matrix (TAHS or similar publicly documented reagent), specifying the matrix composition, ionization behavior, and expected"
- [other] Register the new matrix in Met-ID's system by integrating it into the tool's configuration loader or plugin registry: "Register the new matrix in Met-ID's system by integrating it into the tool's configuration loader or plugin registry."
- [other] Verify that adduct annotations match the expected ions produced by the second matrix and compare against ground truth or literature-reported adducts: "Parse Met-ID's output and verify that adduct annotations match the expected ions produced by the second matrix (e.g. [M+matrix_adduct]+ or other characteristic forms). Compare predicted adducts"
- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [readme] Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software."
