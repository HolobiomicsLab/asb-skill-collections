---
name: metabolite-structure-format-conversion
description: Use when when importing candidate metabolite structures from public chemical
  databases (PubChem, ChEBI, etc.) for use in MAGMa-based annotation workflows, or
  when integrating external structure datasets that may use divergent molecular representation
  formats or contain non-standard chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - MAGMa
  - PubChem database
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma_cq
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-structure-format-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert and standardize chemical structure formats from public databases (e.g., PubChem) into formats compatible with in silico metabolite annotation pipelines. This skill ensures structural data integrity and computational compatibility across heterogeneous chemo-informatics workflows.

## When to use

When importing candidate metabolite structures from public chemical databases (PubChem, ChEBI, etc.) for use in MAGMa-based annotation workflows, or when integrating external structure datasets that may use divergent molecular representation formats or contain non-standard chemical notations incompatible with fragment-matching algorithms.

## When NOT to use

- Input structures are already validated and formatted for MAGMa ingestion—conversion is redundant.
- The annotation workflow does not depend on external structure databases (e.g., de novo fragment enumeration without candidate lookup).
- Structures are from a proprietary or curated database already integrated into the pipeline—no re-standardization is needed.

## Inputs

- PubChem compound records (SDF, SMILES, or InChI format)
- candidate structure dataset with molecular identifiers
- chemical structure raw data from external database
- molecular property tables (mass, formula, element counts)

## Outputs

- standardized candidate structure file in MAGMa-compatible format
- validated structure identifier and property mapping table
- processed candidate set ready for metabolite annotation job
- format compliance report with validation statistics

## How to apply

Extract and parse chemical structure records from the source database in their native format (e.g., SDF, SMILES, InChI). Apply standardization filters to normalize bond types, stereochemistry encoding, and protonation states. Validate each structure for chemical validity and molecular property constraints (e.g., mass range, element composition). Convert structures to the format required by the downstream tool (MAGMa expects specific structure identifiers and property metadata). Finally, export the processed candidate set in the exact format and field order required by the job calculation interface, and verify format compliance via schema validation before pipeline ingestion.

## Related tools

- **MAGMa** (recipient pipeline that consumes standardized metabolite structures and performs in silico fragment matching against MS/MS data) — https://github.com/NLeSC/MAGMa
- **PubChem database** (source chemical structure repository from which candidate metabolite structures are extracted and parsed)

## Evaluation signals

- All structures parse without chemical validity errors and round-trip through the standardization pipeline unchanged.
- Molecular formulas and masses derived from standardized structures match expected ranges for the metabolite class under study.
- The exported candidate file conforms to the MAGMa job input schema (field names, data types, required columns present).
- The number of candidate structures retained post-standardization is within expected bounds (e.g., >80% of input structures pass validation).
- Downstream MAGMa job execution completes without format-related errors and produces ranked metabolite annotations.

## Limitations

- Standardization may fail or discard structures with non-standard chirality notation or rare valence states not recognized by the parser.
- PubChem and other public databases may contain duplicate, mis-annotated, or stereochemically ambiguous entries that standardization alone cannot resolve.
- Format conversion is lossy if the target format (e.g., MAGMa's required input) does not preserve all stereochemical or isotopic information present in the source record.
- No discussion of algorithm robustness or edge cases is provided in the available documentation.

## Evidence

- [other] Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline.: "Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline."
- [other] Extract and parse PubChem compound records from the public PubChem database.: "Extract and parse PubChem compound records from the public PubChem database."
- [other] Validate the candidate set for completeness and format compliance.: "Validate the candidate set for completeness and format compliance."
- [other] Export the processed candidate structures to the format required by MAGMa job calculation.: "Export the processed candidate structures to the format required by MAGMa job calculation."
- [other] The job subproject implements metabolite annotation by generating in silico metabolites and matching them against MS/MS data, as part of MAGMa (Ms Annotation based on in silico Generated Metabolites).: "The job subproject implements metabolite annotation by generating in silico metabolites and matching them against MS/MS data"
