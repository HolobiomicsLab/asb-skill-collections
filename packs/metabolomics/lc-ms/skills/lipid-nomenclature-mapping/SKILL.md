---
name: lipid-nomenclature-mapping
description: Use when you need to generate a comprehensive, non-redundant inventory of lipid species that span a defined lipid class (e.g., phosphatidylcholine, triacylglycerol) and a range of fatty acid compositions (e.g., C14:0 to C22:6).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - LSG
  techniques:
  - LC-MS
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

# Lipid Nomenclature Mapping

## Summary

This skill enumerates lipid molecular species by systematically combining user-specified lipid class constraints with fatty acid composition parameters (carbon count and degree of unsaturation). It produces structured lists of lipid species with associated molecular formulas suitable for downstream mass spectral library generation.

## When to use

Apply this skill when you need to generate a comprehensive, non-redundant inventory of lipid species that span a defined lipid class (e.g., phosphatidylcholine, triacylglycerol) and a range of fatty acid compositions (e.g., C14:0 to C22:6). Use it as the first step before generating fragmentation spectra or precursor/transition lists for targeted lipidomics experiments.

## When NOT to use

- When the input is already a finalized, validated lipid spectral library (MSP format) — the species enumeration step is already complete.
- When you need to perform adduct-specific fragmentation pattern assignment — this skill generates species only; spectrum generation requires a separate fragmentation module.
- When lipid composition is known from experimental data (e.g., MS/MS fragmentation tree) rather than specified a priori — use targeted identification instead.

## Inputs

- User-specified lipid class constraints (e.g., PC, PE, TG)
- Fatty acid composition ranges (minimum and maximum carbon count, degree of unsaturation)
- Lipid class nomenclature definitions

## Outputs

- Enumerated lipid species list (CSV or JSON format)
- Structured table with columns: lipid_class, fatty_acid_composition, molecular_formula

## How to apply

Parse the user-specified lipid class(es) and fatty acid composition constraints, including carbon count range and degree of unsaturation range. Iterate over all valid combinations of lipid class identifiers and fatty acid chain descriptors (e.g., C16:0, C18:1) within those ranges. For each combination, generate a unique lipid molecular species record combining the class identifier with the fatty acid composition. Export the enumerated species list in a structured format (CSV or JSON) with explicit columns for lipid class, fatty acid composition, and molecular formula. Validation should confirm that each species appears exactly once and that all possible combinations within the specified constraints are represented.

## Related tools

- **LSG** (Generates lipid species by class and fatty acid composition; outputs enumerated species for input to spectrum generation and export modules) — https://github.com/98104781/LSG/releases/tag/v1.3.0

## Evaluation signals

- All enumerated species are unique (no duplicates) and respect both the lipid class and fatty acid composition constraints.
- The output table contains exactly N = (number of lipid classes) × (number of valid fatty acid combinations) rows.
- Molecular formula for each species is chemically valid and consistent with the lipid class definition and fatty acid composition.
- All combinations within the specified carbon count and unsaturation ranges are represented; no gaps or omissions.
- The output format (CSV or JSON) conforms to the expected schema with required columns populated for all rows.

## Limitations

- Enumeration does not validate whether generated species are biochemically plausible or observed in nature — it generates all mathematical combinations within the specified ranges.
- Overlapping fatty acid chains (e.g., sn-1 and sn-2 positions in phospholipids) are not distinguished; the skill treats composition as an aggregate descriptor.
- Enumeration does not account for stereoisomerism or positional isomerism of double bonds (e.g., cis vs. trans, or position within the chain).
- The skill does not filter out species that may be biochemically impossible for a given lipid class (e.g., very-short-chain fatty acids in certain glycerolipids).

## Evidence

- [other] Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation); iterate over combinations; generate species by combining class identifiers with fatty acid descriptors; output in structured format (CSV/JSON).: "Parse user-specified lipid class constraints and fatty acid composition ranges (carbon count, degree of unsaturation). 2. Iterate over all combinations of lipid classes and fatty acid compositions"
- [other] LSG enables enumeration with respect to both lipid class and fatty acid composition.: "LSG generates lipid species by enumerating them with respect to both lipid class and fatty acid composition as input parameters."
- [intro] Lipids are generated with respect to class and fatty acid composition as foundational workflow step.: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [intro] Program enables on-demand generation of mass spectral libraries for lipid species identification.: "This program is intended to enable the user to generate on-demand (mass)spectral libraries for the identification of lipid species."
