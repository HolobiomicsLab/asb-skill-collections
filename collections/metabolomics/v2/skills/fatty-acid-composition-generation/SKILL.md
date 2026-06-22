---
name: fatty-acid-composition-generation
description: Use when you need to systematically enumerate all possible lipid species within a defined analytical scope—specifically when you have specified one or more lipid classes (e.g., phosphatidylcholine, triacylglycerol) and fatty acid composition ranges (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LSG
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- https://github.com/98104781/LSG/releases/tag/v1.3.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipid_spectrum_generator_cq
    doi: 10.1021/acs.analchem.2c04518
    title: Lipid Spectrum Generator
  dedup_kept_from: coll_lipid_spectrum_generator_cq
schema_version: 0.2.0
---

# fatty-acid-composition-generation

## Summary

Generate enumerated lipid molecular species by combining user-specified lipid class constraints with fatty acid composition parameters (carbon count and degree of unsaturation). This skill produces structured lists of lipid species that serve as inputs to mass spectral library generation for downstream identification workflows.

## When to use

Use this skill when you need to systematically enumerate all possible lipid species within a defined analytical scope—specifically when you have specified one or more lipid classes (e.g., phosphatidylcholine, triacylglycerol) and fatty acid composition ranges (e.g., C14–C22, 0–6 degrees of unsaturation) and require a complete, non-redundant list of molecular species for library construction or targeted analysis.

## When NOT to use

- Input is already a curated, non-redundant lipid species list—use only if systematic enumeration is needed to fill gaps or validate coverage.
- Fatty acid composition ranges are unknown or unspecified—this skill requires explicit numeric bounds on carbon count and unsaturation.
- The workflow does not require mass spectral libraries or downstream spectral generation—enumeration alone may be insufficient.

## Inputs

- lipid class constraint specification (one or more class names)
- fatty acid composition range parameters (minimum/maximum carbon count, minimum/maximum degree of unsaturation)
- user preferences for output format (CSV or JSON)

## Outputs

- enumerated lipid species list (CSV or JSON format)
- structured table with columns: lipid class, fatty acid composition, molecular formula

## How to apply

Parse the user-specified lipid class constraints and fatty acid composition ranges (carbon count and degree of unsaturation) as categorical and numeric parameters. Iterate systematically over all combinations of lipid classes and fatty acid compositions within the specified ranges. Generate lipid molecular species by combining class identifiers with fatty acid chain descriptors (e.g., C16:0, C18:1). Validate that all enumerated species respect the input parameter bounds. Output the complete enumerated list in a structured format (CSV or JSON) with explicit fields for lipid class, fatty acid composition, and molecular formula. Use this output as the canonical input to downstream mass spectral library generation steps.

## Related tools

- **LSG** (Platform that executes lipid enumeration and generates mass spectral libraries for lipid species identification) — https://github.com/98104781/LSG/releases/tag/v1.3.0

## Evaluation signals

- All enumerated species respect input parameter bounds (carbon count and unsaturation within specified ranges).
- No duplicate lipid species appear in the output list.
- Each lipid species record includes non-empty, consistent values for lipid class, fatty acid composition string (e.g., 'C16:0/C18:1'), and molecular formula.
- Output file format matches user-specified selection (valid CSV or JSON schema).
- Enumerated species count increases monotonically with expansion of input carbon and unsaturation ranges (e.g., extending from C16–C18 to C14–C20 produces a superset).

## Limitations

- Enumeration assumes all combinations of class and fatty acid composition are chemically valid and biologically relevant; species that are rare or non-existent in vivo are not filtered.
- Fatty acid composition is specified only by carbon count and degree of unsaturation; regioisomers and stereoisomers are not distinguished.
- The generated species are used for library construction but do not guarantee detection or identification in any given mass spectrometry experiment.

## Evidence

- [other] Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation): "Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation)"
- [other] Generate lipid molecular species by combining class identifiers with fatty acid chain descriptors: "Generate lipid molecular species by combining class identifiers with fatty acid chain descriptors (e.g., C16:0, C18:1)"
- [other] Output the enumerated lipid species list in a structured format with lipid class, fatty acid composition, and molecular formula: "Output the enumerated lipid species list in a structured format (CSV or JSON) with lipid class, fatty acid composition, and molecular formula"
- [readme] Lipids are generated with respect to class and fatty acid composition: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts"
- [readme] This program is intended to enable the user to generate on-demand mass spectral libraries for the identification of lipid species: "This program is intended to enable the user to generate on-demand (mass)spectral libraries for the identification of lipid species"
