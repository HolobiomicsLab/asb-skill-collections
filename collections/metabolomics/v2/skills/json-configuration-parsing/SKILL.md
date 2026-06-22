---
name: json-configuration-parsing
description: Use when you need to implement a converter or standardization system that must map multiple incompatible nomenclature styles (e.g., lipid abbreviations from 5+ databases and 17+ software programs) into a single unified format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
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
---

# JSON configuration parsing

## Summary

Parse and validate JSON configuration files to extract nomenclature mapping rules, controlled vocabularies, and format specifications for standardizing heterogeneous scientific nomenclature. This skill is essential when implementing unified identifier systems that must reconcile multiple incompatible naming conventions from different databases and software tools.

## When to use

Apply this skill when you need to implement a converter or standardization system that must map multiple incompatible nomenclature styles (e.g., lipid abbreviations from 5+ databases and 17+ software programs) into a single unified format. Use it specifically when the mapping rules are stored in JSON format and you need to load, parse, and apply those rules programmatically to rename or normalize incoming identifiers.

## When NOT to use

- Input nomenclature is already in the target unified identifier format (no conversion needed).
- Configuration rules are stored in non-JSON formats (XML, YAML, plain text) without prior conversion to JSON.
- The nomenclature database is not included in the tested set (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids, or 17 named software tools) and no compatible configuration file has been generated or validated by the project maintainers.

## Inputs

- JSON configuration files specifying nomenclature mapping rules (e.g., `defined_alias.json`, database-specific input rules)
- Heterogeneous lipid nomenclature strings in multiple formats (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids database styles; ALEX123, Greazy, LipidSearch, etc. software formats)
- Shorthand notation variants: space-separated (e.g., 'PC 16:0_18:2') and bracket notation (e.g., 'PC(16:0_18:2)')

## Outputs

- Parsed nomenclature mapping rule objects extracted from JSON
- Structured table (CSV or XLSX) mapping input nomenclature variants to unified identifiers
- Validation report indicating conversion success/failure and consistency across variants

## How to apply

Load the JSON configuration files from the designated configuration directory (e.g., `lynx/configurations/rules/input` for LipidLynxX). Parse each JSON file to extract the nomenclature mapping rules, which define how to transform heterogeneous input notation styles into canonical unified identifiers. Apply the parsed rules sequentially to test lipid names representing different notation styles (shorthand with spaces, bracket notation, database-specific abbreviations). For each input name, match it against the applicable rule set and apply the corresponding transformation. Validate that all variants of the same lipid produce identical unified identifiers, indicating rule consistency. Format and store results in a structured table mapping input names to output identifiers, checking for conversion errors or missing mappings.

## Related tools

- **LipidLynxX** (Unified lipid identifier conversion system that uses JSON configurations to map heterogeneous lipid nomenclature from 5 databases and 17 software tools into standardized identifiers) — https://github.com/SysMedOs/LipidLynxX
- **Visual Studio Code** (Editor for formatting and validating JSON configuration files before deployment)
- **PyCharm** (IDE for editing JSON configurations and debugging Python code that parses and applies the rules)
- **Black** (Python code formatter used in LipidLynxX to ensure consistent style in scripts that parse and apply JSON rules) — https://github.com/psf/black

## Evaluation signals

- All input nomenclature variants representing the same lipid (e.g., 'PC 16:0_18:2', 'PC(16:0_18:2)', HMDB name, LIPID MAPS name) produce identical unified identifiers after parsing and rule application.
- Output unified identifiers follow the expected canonical format specified in the JSON schema and contain all required hierarchical levels (e.g., lipid class, chain composition, oxidation state).
- No conversion errors or missing mappings are reported in the validation log; input/output table shows 100% successful conversion for supported nomenclature styles.
- JSON schema validation passes: all parsed configuration objects conform to the strict JSON schema defined in the project, with no missing or malformed fields.
- Cross-level match consistency: identifiers from the same lipid across different annotation levels (e.g., species level vs. molecular species level) share the expected common prefix or hierarchical relationship.

## Limitations

- Conversion is only supported for lipid nomenclature from the explicitly tested set: 5 databases (HMDB, LIPID MAPS LMSD & COMP_DB, LipidHome, RefMet, SwissLipids) and 17 named software tools (ALEX123, Greazy, LDA 2, LipidBlast, etc.). Nomenclature from untested sources requires generation and validation of new configuration files.
- API and documentation in the source code may not be synchronized with rapid feature changes; developers should contact maintainers before using the LipidLynxX API in production systems.
- Known issue in the Windows .exe version: if the Linker module runs for more than 300 seconds or more than 30 seconds per ID, it must be restarted; conversion may fail or hang beyond these thresholds.
- Modified lipids (e.g., oxidized lipids) require specially structured JSON rules in the epilipidome domain; not all lipid modifications are covered by the default configuration set.

## Evidence

- [methods] LipidLynxX source code use [code style Black](https://github.com/psf/black) for all python codes: "LipidLynxX source code use [code style Black] for all python codes"
- [methods] JSON configurations are formatted by Visual Studio Code / PyCharm editor: "JSON configurations are formatted by Visual Studio Code / PyCharm editor"
- [other] Load LipidLynxX source code from the SysMedOs/LipidLynxX repository and review the nomenclature mapping configuration (JSON format).: "Load LipidLynxX source code from the SysMedOs/LipidLynxX repository and review the nomenclature mapping configuration (JSON format)"
- [readme] The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: Databases (5): `HMDB`, `LIPID MAPS LMSD & COMP_DB`, `LipidHome`, `RefMet`, `SwissLipids`: "The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: Databases (5): `HMDB`, `LIPID MAPS LMSD &"
- [readme] Abbreviations such as DHA, PAPE, PLPC, PONPC .etc are also included as `defined alias`. detailed settings can be found in `lynx/configurations/defined_alias.json`: "Abbreviations such as DHA, PAPE, PLPC, PONPC .etc are also included as `defined alias`. detailed settings can be found in `lynx/configurations/defined_alias.json`"
- [readme] Strictly controlled format using JSON schema: "Strictly controlled format using JSON schema"
- [other] Validate output identifiers by checking that they follow the expected canonical format and that all input nomenclature variants for the same lipid produce identical unified identifiers.: "Validate output identifiers by checking that they follow the expected canonical format and that all input nomenclature variants for the same lipid produce identical unified identifiers"
- [readme] If your database / program is not included in the list above, you can test if any of the configuration files located in `lynx/configurations/rules/input` would fit to your database / program.: "If your database / program is not included in the list above, you can test if any of the configuration files located in `lynx/configurations/rules/input` would fit to your database / program"
