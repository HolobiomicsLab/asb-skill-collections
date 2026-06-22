---
name: identifier-mapping-implementation
description: Use when when you have lipid names or abbreviations sourced from multiple databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) or software tools (LipidSearch, MS-DIAL, MZmine2, LipidBlast, etc.) and need to normalize them into a single canonical representation to enable data integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - LipidLynxX
  - Black
  - Visual Studio Code
  - PyCharm
derived_from:
- doi: 10.1101/2020.04.09.033894
  title: LipidLynxX
evidence_spans:
- The LipidLynxX project is aimed to provide a unified identifier for major lipids
- LipidLynxX source code use [code style Black](https://github.com/psf/black) for all python codes
- JSON configurations are formatted by Visual Studio Code / PyCharm editor
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidlynxx_cq
    doi: 10.1101/2020.04.09.033894
    title: LipidLynxX
  dedup_kept_from: coll_lipidlynxx_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.04.09.033894
  all_source_dois:
  - 10.1101/2020.04.09.033894
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# identifier-mapping-implementation

## Summary

Implement a unified identifier conversion system that maps heterogeneous nomenclature from multiple lipid databases and software into a canonical, standardized ID format. This skill is essential for enabling cross-database lipid research by resolving nomenclature ambiguity and enabling reproducible annotation.

## When to use

When you have lipid names or abbreviations sourced from multiple databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) or software tools (LipidSearch, MS-DIAL, MZmine2, LipidBlast, etc.) and need to normalize them into a single canonical representation to enable data integration, comparison, or cross-tool validation. Particularly critical when working with oxidized lipids where nomenclature heterogeneity is high and manual harmonization is error-prone.

## When NOT to use

- Input lipid names are already in LipidLynxX unified identifier format or another standardized canonical representation — re-mapping will be redundant and may introduce errors.
- Your lipid dataset comes from a single source (e.g., only HMDB or only one software tool) with no cross-tool harmonization requirement — simple in-database ID lookup may be more efficient.
- The lipid nomenclature is from an unsupported database or software not listed in the 5 supported databases and 17 supported programs — the conversion rules will be missing and the skill cannot be applied without first extending the configuration.

## Inputs

- heterogeneous lipid abbreviation strings (multiple notation styles: shorthand space-separated, bracketed derivatives, tool-specific formats)
- lipid names from supported databases (HMDB, LIPID MAPS LMSD/COMP_DB, LipidHome, RefMet, SwissLipids)
- lipid identifiers from supported software (ALEX123, Greazy, LDA 2, LipidBlast, LipidCreator, LipiDex, LipidFrag, LipidHunter, LipidMatch, LipidPro, LipidSearch, Lipostar, LIQUID, LPPtiger, MetFrag, MS-DIAL, MZmine2)
- JSON nomenclature mapping configuration files
- test dataset with multiple lipid notation variants for the same molecules

## Outputs

- unified LipidLynxX identifiers (canonical format with position-specific annotations)
- mapping table (input nomenclature → output unified identifier)
- conversion validation report (success/failure status per input, schema compliance checks)

## How to apply

Load the nomenclature mapping configuration (JSON format) from the reference repository and review the input rules for each supported database/tool. Implement or activate the core conversion function that accepts lipid notation strings in any of the supported styles (space-separated shorthand like 'PC 16:0_18:2', bracketed derivatives like 'PC(16:0_18:2)', or tool-specific abbreviations) and applies the unified identifier mapping rules. Prepare a test dataset containing lipid names in multiple notation styles covering both major and oxidized lipids from the supported sources. Execute the conversion function on each test lipid name, capturing both successful conversions and any failures. Validate output identifiers by checking that they follow the expected canonical format (position-specific annotations, unified modification vocabularies, controlled JSON schema) and that all input nomenclature variants referring to the same lipid produce identical unified identifiers. Format results as a structured table and verify no conversion errors or missing mappings occurred.

## Related tools

- **LipidLynxX** (Core conversion engine that implements the unified identifier mapping logic and validates output format compliance) — https://github.com/SysMedOs/LipidLynxX
- **Black** (Code style formatter for maintaining Python code quality during LipidLynxX source code implementation and modification) — https://github.com/psf/black
- **Visual Studio Code** (Editor for viewing and editing JSON nomenclature configuration files)
- **PyCharm** (IDE for editing and debugging LipidLynxX source code and JSON configuration files)

## Examples

```
python cli_lynx.py
```

## Evaluation signals

- All input lipid names from the test dataset either produce a valid unified identifier or are explicitly flagged as unmapped; no silent failures or partial conversions occur.
- Output unified identifiers conform to the LipidLynxX JSON schema (position-specific annotations present, modification controlled vocabularies used, format validated against schema).
- Multiple input nomenclature variants representing the same lipid (e.g., 'PC 16:0_18:2', 'PC(16:0_18:2)', HMDB notation, MS-DIAL notation for identical molecule) all produce identical unified identifier output.
- Conversion table has no duplicate mappings (one input → one output) and the mapping is deterministic (re-running the same input produces identical output).
- For oxidized lipids specifically, position-specific annotations and modification annotations are preserved in the unified identifier and correctly sorted/formatted per canonical rules.

## Limitations

- If a database or software tool is not in the supported list (5 databases + 17 programs), no conversion rules exist and custom configuration files must be generated before the skill can be applied.
- The skill depends on the completeness and accuracy of the JSON nomenclature configuration files; outdated or incomplete configurations will result in unmapped lipids or incorrect conversions.
- Common abbreviations (e.g., DHA, PAPE, PLPC, PONPC) are supported via customizable defined_alias.json; if an abbreviation is missing from this configuration, it will not be recognized.
- Command-line and API performance limitations noted in the README: the Windows .exe version recommends running max 3 tasks simultaneously; Linker module may timeout if running >300s or >30s per ID.

## Evidence

- [other] LipidLynxX is designed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome, enabling standardization of heterogeneous lipid nomenclature across the lipid research domain.: "The LipidLynxX project is aimed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome."
- [other] The conversion process requires loading JSON nomenclature configurations, implementing a core function that accepts heterogeneous lipid notation, preparing a test dataset with multiple notation styles, executing the conversion, and validating that output identifiers follow canonical format and that all variants of the same lipid produce identical outputs.: "1. Load LipidLynxX source code from the SysMedOs/LipidLynxX repository and review the nomenclature mapping configuration (JSON format). 2. Implement or activate the core conversion function that"
- [readme] LipidLynxX supports conversion of lipid names from 5 major databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) and 17 software tools including LipidSearch, MS-DIAL, MZmine2, and LipidBlast.: "The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: - Databases (5): `HMDB`, `LIPID MAPS LMSD &"
- [readme] Multiple supported lipid notation styles include space-separated shorthand (e.g., 'PC 16:0_18:2'), bracketed derivatives (e.g., 'PC(16:0_18:2)'), and customizable common abbreviations.: "Shorthand notation using space: e.g. PC 16:0_18:2 - Shorthand notation derivatives using brackets: e.g. PC(16:0_18:2) - Common abbreviations (customizable): Abbreviations such as DHA, PAPE, PLPC,"
- [readme] Output format must strictly adhere to JSON schema with position-specific annotations and unified modification controlled vocabularies.: "Strictly controlled format using JSON schema"
