---
name: cross-database-nomenclature-alignment
description: Use when when you have lipid abbreviations or names from different databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) or lipidomics software (LipidSearch, MS-DIAL, LipidBlast, etc.) that must be cross-referenced, compared, or integrated into a single annotation scheme.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3375
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-database-nomenclature-alignment

## Summary

Map heterogeneous lipid nomenclature variants from multiple databases and software tools into a unified canonical identifier system. This skill enables standardization and interoperability of lipid names across the research ecosystem, particularly for oxidized lipids.

## When to use

When you have lipid abbreviations or names from different databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) or lipidomics software (LipidSearch, MS-DIAL, LipidBlast, etc.) that must be cross-referenced, compared, or integrated into a single annotation scheme. Use this skill when nomenclature heterogeneity would prevent comparison of results across studies or platforms.

## When NOT to use

- Input lipid names are already in LipidLynxX canonical format or a single standardized identifier scheme — no alignment needed.
- Lipid database or software source is not in the supported list and no suitable configuration file exists in lynx/configurations/rules/input.
- The goal is taxonomy assignment or functional classification rather than nomenclature harmonization across heterogeneous sources.

## Inputs

- Lipid abbreviation strings in heterogeneous notation (shorthand with space, bracketed derivatives, common aliases)
- Lipid names from supported databases or software (HMDB, LIPID MAPS LMSD & COMP_DB, LipidHome, RefMet, SwissLipids, ALEX123, Greazy, LDA 2, LipidBlast, LipidCreator, LipiDex, LipidFrag, LipidHunter, LipidMatch, LipidPro, LipidSearch, Lipostar, LIQUID, LPPtiger, MetFrag, MS-DIAL, MZmine2)
- LipidLynxX configuration files (JSON) for nomenclature rules

## Outputs

- Unified LipidLynxX canonical identifiers for each input lipid name
- Structured table mapping input nomenclature variants to output unified identifiers
- Validation report confirming no conversion errors or missing mappings

## How to apply

Load the LipidLynxX configuration files (JSON format) that define nomenclature mapping rules for your source databases and software. Prepare a test dataset containing lipid names in multiple notation styles (e.g., 'PC 16:0_18:2', 'PC(16:0_18:2)', common abbreviations like DHA or PLPC). Execute the LipidLynxX converter function on each input lipid name, applying the unified identifier mapping rules. Validate that all nomenclature variants for the same lipid produce identical unified identifiers and follow the expected canonical format (position-specific annotations, controlled modification vocabularies). Format results as a structured table mapping input names to output unified identifiers and verify no conversion errors or missing mappings occurred.

## Related tools

- **LipidLynxX** (Core converter engine that applies unified identifier mapping rules to heterogeneous lipid nomenclature; provides GUI, API, and CLI interfaces for batch or programmatic nomenclature alignment) — https://github.com/SysMedOs/LipidLynxX
- **Black** (Code style formatter for LipidLynxX Python source code; ensures consistent codebase for maintenance and contribution) — https://github.com/psf/black
- **Visual Studio Code** (Editor for authoring and validating JSON configuration files that define nomenclature mapping rules)
- **PyCharm** (IDE for editing and formatting JSON configurations and running LipidLynxX converter from source code)

## Examples

```
from lynx.models import LynxConvertor; converter = LynxConvertor(); result = converter.convert('PC 16:0_18:2', style='LipidLynxX'); print(result.unified_id)
```

## Evaluation signals

- All input nomenclature variants for the same lipid produce identical unified identifiers (no divergence across notations).
- Output identifiers follow the expected canonical format with position-specific annotations and unified modification controlled vocabularies.
- Structured output table is complete with no missing mappings or conversion errors reported.
- Cross-validation: identifiers from different source databases for the same lipid species map to the same unified ID.
- Schema validation: output identifiers conform to LipidLynxX JSON schema constraints for structure and syntax.

## Limitations

- If your database or program is not in the supported list (5 databases + 17 programs), conversion may fail unless a suitable configuration file is generated or contributed to the project.
- Known API and documentation in the source code may not be fully updated; developers planning to use LipidLynxX API are advised to contact the team first.
- Windows .exe version has known issues: Linker module times out after 300s or more than 30s per ID and should be restarted; max 3 concurrent tasks recommended.
- The code is under active development; API definitions and nomenclature rules may change between releases.

## Evidence

- [other] LipidLynxX is designed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome, enabling standardization of heterogeneous lipid nomenclature across the lipid research domain.: "LipidLynxX is designed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome, enabling standardization of heterogeneous lipid nomenclature"
- [other] The workflow prepares a test dataset containing lipid names in multiple notation styles from supported databases or software, executes the conversion function, and validates output identifiers against expected canonical format.: "Prepare a test dataset containing lipid names in multiple notation styles (major lipids and oxidized-lipid formats) from supported databases or software. Execute the conversion function on each test"
- [readme] The current LipidLynxX source code was tested using lipid abbreviations from 5 databases and 17 programs, plus shorthand notations and customizable common abbreviations.: "The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: - Databases (5): `HMDB`, `LIPID MAPS LMSD &"
- [readme] LipidLynxX provides unified modification controlled vocabularies and unified position specific annotations to ensure consistent representation across all nomenclature variants.: "- Unified modification controlled vocabularies
- Unified position specific annotations"
- [readme] If conversion is not possible or your database is not included, you can contact the LipidLynxX team to generate suitable configuration files, and any issue reports will improve the project through community-wide collaboration.: "If conversion is not possible, please contact us so that we can help you to generate suitable configuration file. A robust and accurate converter can only be achieved by community-wide collaborations"
