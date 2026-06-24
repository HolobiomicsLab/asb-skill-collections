---
name: lipid-class-enumeration
description: Use when you have a lipid identification or library-generation task that
  requires you to define a target chemical space bounded by lipid classes (e.g., phosphatidylcholine,
  triglyceride) and fatty acid composition ranges (e.g., C14–C22 with 0–6 degrees
  of unsaturation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0199
  tools:
  - LSG
  - LSG (Lipid Spectrum Generator)
  - Excalibur
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- https://github.com/98104781/LSG/releases/tag/v1.3.0
- Excalibur compatible precursor list (for DDA analysis via orbitrap)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Lipid Class and Fatty Acid Composition Enumeration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate a comprehensive inventory of lipid molecular species by systematically combining user-specified lipid class constraints with fatty acid composition parameters (carbon count and degree of unsaturation). This skill produces structured enumerated lipid species lists that serve as input for downstream spectral library generation and mass spectrometry-based identification workflows.

## When to use

Apply this skill when you have a lipid identification or library-generation task that requires you to define a target chemical space bounded by lipid classes (e.g., phosphatidylcholine, triglyceride) and fatty acid composition ranges (e.g., C14–C22 with 0–6 degrees of unsaturation). Use it when you need to move from a high-level analytical design (e.g., 'catalog all major PC and TAG species in mammalian plasma') to a concrete, enumerated molecular inventory suitable for theoretical spectrum prediction or targeted mass spectrometry acquisition.

## When NOT to use

- Input is a measured mass spectrum or chromatogram; use spectral matching or feature extraction instead.
- You already have a curated, experimentally validated lipid species list; enumeration may introduce implausible or unavailable species.
- The task requires de novo lipid identification from raw MS/MS data; begin with fragmentation pattern matching, not enumeration.

## Inputs

- User-specified lipid class list (e.g., ['PC', 'PE', 'TAG'])
- Fatty acid carbon count range (e.g., 14–22)
- Fatty acid degree of unsaturation range (e.g., 0–6)

## Outputs

- Enumerated lipid species list (CSV or JSON format)
- Species-level metadata: lipid class, fatty acid composition, molecular formula

## How to apply

Parse user-specified lipid class constraints (e.g., PC, PE, TAG) and fatty acid composition ranges defined by carbon count and degree of unsaturation (DBE). Iterate over all valid combinations of lipid classes and fatty acid chain compositions within the specified parameter space. For each combination, generate lipid molecular species identifiers by concatenating class identifiers with standardized fatty acid chain descriptors (e.g., C16:0 for palmitic acid, C18:1 for oleic acid). Validate that generated species are chemically plausible (e.g., total carbon and DBE are consistent with the lipid class stoichiometry). Export the enumerated species list in a structured, machine-readable format (CSV or JSON) containing lipid class, fatty acid composition, and molecular formula for each entry.

## Related tools

- **LSG (Lipid Spectrum Generator)** (Primary enumeration and spectral generation platform; parses lipid class and fatty acid constraints, generates species inventory, and produces theoretical adduct spectra.) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Downstream targeted acquisition tool for DDA analysis on Orbitrap instruments; consumes precursor m/z lists exported from LSG enumeration.)

## Evaluation signals

- Enumerated species count matches expected combinatorial expansion: (number of lipid classes) × (number of valid fatty acid combinations).
- All generated species satisfy class-specific molecular constraints (e.g., PC species have exactly one phosphocholine headgroup and two fatty acids).
- Molecular formula for each species is chemically valid and consistent with lipid class definition.
- CSV/JSON export is parseable and contains no missing or malformed entries for lipid class, fatty acid descriptors, or molecular formula.
- Downstream spectral generation (adduct enumeration and fragmentation) completes without errors on the enumerated species list.

## Limitations

- Enumeration generates all combinatorially possible species within parameter ranges; not all generated species may be biologically present or experimentally detectable in a given sample.
- Fragmentation pattern accuracy depends on peer-reviewed literature coverage for the specified lipid class and adduct type; rare or poorly characterized lipid classes may lack validated fragmentation rules.
- Fatty acid composition ranges must be manually specified by the user; incorrect or overly broad ranges can produce computationally expensive enumerations or include implausible species.
- Enumeration does not account for stereoisomerism, regioisomerism, or double-bond positional isomerism; all C18:1 species are treated identically regardless of cis/trans configuration or Δ position.

## Evidence

- [other] Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation). Iterate over all combinations of lipid classes and fatty acid compositions within the specified ranges.: "Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation). Iterate over all combinations of lipid classes and fatty acid compositions"
- [other] Generate lipid molecular species by combining class identifiers with fatty acid chain descriptors (e.g., C16:0, C18:1). Output the enumerated lipid species list in a structured format (CSV or JSON).: "Generate lipid molecular species by combining class identifiers with fatty acid chain descriptors (e.g., C16:0, C18:1). Output the enumerated lipid species list in a structured format (CSV or JSON)"
- [readme] Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts.: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [other] LSG generates lipid species by enumerating them with respect to both lipid class and fatty acid composition as input parameters.: "LSG generates lipid species by enumerating them with respect to both lipid class and fatty acid composition as input parameters."
