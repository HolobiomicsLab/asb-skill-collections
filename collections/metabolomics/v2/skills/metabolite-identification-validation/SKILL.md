---
name: metabolite-identification-validation
description: Use when you have extended a metabolite identification tool (such as
  Met-ID) to support a new derivatizing matrix beyond the default (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - RDKit
  - Met-ID
  techniques:
  - MS-imaging
  license_tier: restricted
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

# metabolite-identification-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a metabolite identification tool correctly recognizes and applies derivatizing matrices to produce expected adduct annotations in mass spectrometry imaging. This skill verifies both the extensibility of the identification system to novel matrices and the accuracy of predicted adduct forms against ground truth.

## When to use

You have extended a metabolite identification tool (such as Met-ID) to support a new derivatizing matrix beyond the default (e.g., beyond FMP-10) and need to verify that the system correctly registers the matrix, recognizes its ionization behavior, and produces accurate adduct annotations that match known or literature-reported standards.

## When NOT to use

- The metabolite identification tool does not support plugin registration or configuration extension — use only with tools designed with extensibility in mind (as Met-ID is).
- You lack ground truth adduct data or literature references for the test metabolites — validation requires a reference standard to judge correctness.
- The new derivatizing matrix's ionization behavior is not well-characterized — adduct form prediction requires documented chemistry for the matrix.

## Inputs

- Derivatizing matrix configuration file (specifying composition, ionization behavior, expected adducts)
- Test set of metabolites with known derivatization behavior (internal standards or chemical reference compounds)
- Literature-reported or experimentally verified ground truth adduct forms for the test metabolites

## Outputs

- Met-ID output containing registered matrix and predicted adduct annotations
- Comparison report matching predicted adducts against ground truth
- Validation success/failure status for each test metabolite

## How to apply

First, create a configuration file or plugin module for the new derivatizing matrix, specifying its composition, ionization behavior, and expected adduct forms (e.g., [M+matrix_adduct]+ or characteristic ions). Register the matrix in the tool's configuration loader or plugin registry. Run the identification tool on a test set of metabolites with known derivatization behavior (internal standards or reference compounds). Parse the tool's output to extract predicted adducts and compare them against ground truth adduct forms from literature or independent verification. The validation is successful when predicted adducts match expected ions produced by the new matrix across the test set.

## Related tools

- **Met-ID** (Metabolite identification system in mass spectrometry imaging; used to register new derivatizing matrices and predict adduct annotations) — https://github.com/pbjarterot/Met-ID
- **RDKit** (Molecular toolkit underlying Met-ID for chemical structure handling and adduct form computation)

## Evaluation signals

- Predicted adduct annotations for test metabolites match literature-reported or ground truth adduct forms with 100% accuracy across the test set.
- The configuration file or plugin module for the new matrix is successfully integrated into the tool's registry without runtime errors.
- Output files contain characteristic ion forms expected from the new matrix (e.g., correct [M+matrix_adduct]+ or other documented adduct signatures).
- Comparison between predicted and ground truth adducts shows no false positives (incorrect adduct assignments) or false negatives (missed known adducts).
- The tool correctly distinguishes adducts produced by the new matrix from those of the default matrix when both are registered.

## Limitations

- Validation requires well-characterized test metabolites and documented reference adduct forms; success depends on the quality and completeness of ground truth data.
- Met-ID's extensibility to any derivatizing matrix has been designed but is shown primarily through FMP-10 examples; support for unusual matrices may require custom development.
- The tool is noted to be under development; database and configuration file management may require manual cleanup (e.g., removal of cached files in AppData/Roaming) when updating matrix registrations.
- Platform-specific issues reported (e.g., functional group addition failures on macOS) may affect validation workflow on some operating systems.

## Evidence

- [other] Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10 which was developed in-house.: "Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10"
- [readme] Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software.: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
- [intro] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode.: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] Run Met-ID on a test set of metabolites (internal standards or reference compounds with known derivatization behavior) using the newly registered matrix.: "Run Met-ID on a test set of metabolites (internal standards or reference compounds with known derivatization behavior) using the newly registered matrix"
- [other] Compare predicted adducts against ground truth or literature-reported adducts for the test metabolites to confirm correct recognition and application.: "Compare predicted adducts against ground truth or literature-reported adducts for the test metabolites to confirm correct recognition and application"
