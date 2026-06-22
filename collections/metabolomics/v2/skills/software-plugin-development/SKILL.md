---
name: software-plugin-development
description: Use when when you have a scientific software tool (e.g., Met-ID) that is architected to support plugins or configuration-driven modules, and you need to register and apply a novel reagent, derivatizing matrix, or analytical method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - RDKit
  - Met-ID
  techniques:
  - MS-imaging
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-plugin-development

## Summary

Extend a scientific software tool by creating and registering new plugin modules or configuration files that add support for novel reagents, matrices, or analysis parameters without modifying the core codebase. This skill is essential when a tool is designed with extensibility in mind but needs to support user-defined or newly documented derivatizing matrices, ionization behaviors, or similar domain-specific extensions.

## When to use

When you have a scientific software tool (e.g., Met-ID) that is architected to support plugins or configuration-driven modules, and you need to register and apply a novel reagent, derivatizing matrix, or analytical method (e.g., TAHS instead of FMP-10) that is not yet bundled in the default installation. Use this skill when the tool's documentation indicates extensibility is built-in and you have domain knowledge of the new reagent's ionization behavior, adduct forms, or expected chemical transformations.

## When NOT to use

- The tool does not document or support a plugin interface or configuration extension mechanism — use direct source code modification instead.
- The new reagent or matrix is not chemically or analytically well-characterized (ionization behavior and expected adducts are unknown or unstable) — establish ground truth first.
- The tool is a black-box or closed-source system with no documented extensibility architecture — contact vendor or maintain a parallel tool.

## Inputs

- Tool's extensibility architecture documentation (plugin interface, configuration schema)
- New derivatizing matrix or reagent chemical specification (composition, ionization behavior, expected adduct forms)
- Test set of metabolite standards or reference compounds with known derivatization behavior
- Tool's configuration file template or plugin skeleton (if provided)

## Outputs

- Configuration file or plugin module registering the new matrix (e.g., TAHS configuration)
- Met-ID output with adduct annotations using the newly registered matrix
- Comparison report of predicted versus ground-truth adducts for test compounds
- Validation summary confirming correct matrix application

## How to apply

First, review the tool's extensibility architecture (e.g., plugin registry, configuration loader, or documented matrix interface) to understand the structure and required parameters. Second, create a configuration file or plugin module that specifies the new matrix or reagent's composition, ionization behavior, characteristic adduct forms (e.g., [M+matrix_adduct]+), and any other chemical properties the tool uses for annotation. Third, register the new plugin by integrating it into the tool's plugin system or configuration loader. Fourth, run the tool on a test set of internal standards or reference compounds with known behavior under the new reagent to verify that predicted adducts match ground truth. Fifth, compare output annotations against literature-reported adducts or experimental MS data for the test compounds to confirm the plugin correctly recognizes and applies the new matrix.

## Related tools

- **Met-ID** (Primary software platform for metabolite identification in mass spectrometry imaging; provides the extensibility architecture and plugin registry into which new derivatizing matrices are registered and applied) — https://github.com/pbjarterot/Met-ID
- **RDKit** (Underlying cheminformatics library used by Met-ID to compute molecular transformations, ionization behavior, and adduct annotations for registered matrices)

## Evaluation signals

- Configuration file or plugin module is syntactically valid and accepted by the tool's configuration loader or plugin registry without parse errors.
- Test run on reference compounds produces adduct annotations matching the new matrix's expected ionization forms (e.g., [M+matrix_adduct]+ for TAHS).
- Predicted adducts correlate with literature-reported or experimentally validated MS/MS spectra and ground-truth chemical standards for the test compounds.
- Tool's output logs confirm the new matrix is being selected and applied (vs. default FMP-10) for the test metabolites.
- Adduct predictions remain consistent across multiple runs on the same test set (reproducibility check).

## Limitations

- Plugin extensibility is only as flexible as the tool's documented interface allows — if the interface does not support the specific chemical properties of the new reagent (e.g., multi-step adduct formation), the plugin approach may fail.
- Incorrect specification of ionization behavior or adduct forms in the configuration will lead to incorrect annotations; validation against ground-truth standards is critical and cannot be skipped.
- Changes to the plugin or configuration only affect the specific local installation of the tool and do not propagate to other users' copies or to the public repository.
- Met-ID is under active development; plugin files may need to be manually removed and the tool reinstalled when updating to newer versions (as noted in the README regarding database bundling issues).

## Evidence

- [other] Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10: "Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10 which was developed in-house."
- [other] Review Met-ID's extensibility architecture and existing derivatizing matrix configuration: "Review Met-ID's extensibility architecture and existing derivatizing matrix configuration (e.g. the documented matrix currently supported) to understand the plugin or configuration interface."
- [other] Create a configuration file or plugin module for the second derivatizing matrix: "Create a configuration file or plugin module for the second derivatizing matrix (TAHS or similar publicly documented reagent), specifying the matrix composition, ionization behavior, and expected"
- [other] Register the new matrix in Met-ID's system by integrating it into the tool's configuration loader or plugin registry: "Register the new matrix in Met-ID's system by integrating it into the tool's configuration loader or plugin registry."
- [other] Verify that adduct annotations match the expected ions produced by the second matrix: "Parse Met-ID's output and verify that adduct annotations match the expected ions produced by the second matrix (e.g. [M+matrix_adduct]+ or other characteristic forms)."
- [readme] Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software.: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software."
- [readme] all changes to the database only affect that specific install of Met-ID and not any other: "all changes to the database only affect that specific install of Met-ID and not any other."
