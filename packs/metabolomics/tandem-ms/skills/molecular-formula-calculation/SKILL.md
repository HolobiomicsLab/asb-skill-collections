---
name: molecular-formula-calculation
description: Use when you have user-specified lipid class constraints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LSG
  - Excalibur
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04518
  all_source_dois:
  - 10.1021/acs.analchem.2c04518
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-calculation

## Summary

Calculate and output molecular formulas for enumerated lipid species by combining lipid class identifiers with fatty acid chain descriptors (carbon count, degree of unsaturation). This skill enables systematic generation of lipid molecular identities for spectral library construction and mass spectrometry-based identification workflows.

## When to use

Apply this skill when you have user-specified lipid class constraints (e.g., phosphatidylcholine, triacylglycerol) and fatty acid composition ranges (carbon count and degree of unsaturation), and need to generate a comprehensive, structured list of lipid molecular species with their corresponding formulas for downstream spectral library generation or mass spectrometry analysis.

## When NOT to use

- Input is already a pre-computed molecular formula table or spectral library; use this skill only to generate formulas from compositional parameters.
- Analysis goal requires custom or organism-specific lipid modifications not covered by peer-reviewed fragmentation patterns; LSG uses standard fragmentation patterns and may not capture non-canonical lipid structures.
- Lipid species are already assigned and you need only to predict their fragmentation or adduct patterns; use spectral generation downstream after formula enumeration.

## Inputs

- Lipid class constraints (list of lipid class identifiers)
- Fatty acid composition ranges (carbon count range, degree of unsaturation range)
- Lipid class structural templates (elemental composition per class)

## Outputs

- Enumerated lipid species list (structured format: CSV or JSON)
- Molecular formula per lipid species
- Lipid class annotation per species
- Fatty acid composition descriptor per species

## How to apply

Parse the user-specified lipid class constraints and fatty acid composition ranges (defined by carbon count and degree of unsaturation). Iterate systematically over all valid combinations of lipid classes and fatty acid compositions within the specified ranges. For each combination, generate the lipid molecular species by concatenating the class identifier with fatty acid chain descriptors (e.g., PC C16:0, TG C18:1/C16:0). Calculate the molecular formula for each species by summing the elemental composition of the lipid class backbone and all constituent fatty acid chains. Output the complete enumerated lipid species list in a structured format (CSV or JSON) that includes the lipid class, fatty acid composition, and calculated molecular formula.

## Related tools

- **LSG** (Orchestrates lipid enumeration by class and fatty acid composition, calculates molecular formulas, and generates on-demand mass spectral libraries) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Accepts exported precursor lists (CSV format with molecular formulas and m/z values) for data-dependent acquisition (DDA) on Orbitrap instruments)

## Evaluation signals

- All enumerated lipid species have valid molecular formulas with correct elemental composition (C, H, O, N, P atoms) consistent with the lipid class and fatty acid composition.
- Output file schema matches specified format (CSV or JSON) with required columns: lipid class, fatty acid composition descriptor, molecular formula, and calculated m/z values.
- No duplicate lipid species in the output list; each unique combination of class + fatty acid composition is represented exactly once.
- Fatty acid descriptors follow the standard notation (e.g., C16:0, C18:1) and carbon count and degree of unsaturation values fall within the user-specified input ranges.
- Molecular formula mass (calculated from elemental composition) is consistent with the m/z values used in downstream spectral library or precursor list export.

## Limitations

- Fragmentation patterns used are based on peer-reviewed studies and may not capture novel or rare lipid modifications.
- LSG generates lipids deterministically from combinatorial enumeration; lipids not explicitly covered by user-specified ranges are not generated.
- No validation of biological plausibility or organism-specific lipid abundance; enumeration is exhaustive within the specified parameter space, not filtered by prevalence.
- Output molecular formulas assume standard lipid backbone and fatty acid structures; custom or non-standard modifications require manual formula adjustment outside LSG.

## Evidence

- [other] Demonstrates the workflow of parsing, iterating, and generating lipid identities: "Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation). Iterate over all combinations of lipid classes and fatty acid compositions"
- [readme] States the high-level purpose of the tool in relation to formula generation: "This program is intended to enable the user to generate on-demand (mass)spectral libraries for the identification of lipid species."
- [readme] Confirms the two key input parameters driving enumeration: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [readme] Specifies the export formats that include molecular formula data: "Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may"
