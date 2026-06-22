---
name: lipid-nomenclature-standardization
description: Use when you have lipid names or abbreviations sourced from multiple databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) or software tools (LipidSearch, MS-DIAL, LipidBlast, etc.), and you need to unify them into a single canonical identifier system to enable cross-database comparison.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-nomenclature-standardization

## Summary

Apply LipidLynxX unified identifier mapping to convert heterogeneous lipid nomenclature from multiple databases and software into a canonical, standardized format suitable for cross-platform lipid data integration and epilipidome research. This skill is essential when working with oxidized lipids or aggregating lipid identifications from diverse sources.

## When to use

Use this skill when you have lipid names or abbreviations sourced from multiple databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) or software tools (LipidSearch, MS-DIAL, LipidBlast, etc.), and you need to unify them into a single canonical identifier system to enable cross-database comparison, standardized annotation, and oxidized-lipid tracking across the epilipidome.

## When NOT to use

- Input lipid identifiers are already in canonical LipidLynxX format — no conversion is needed.
- Lipid nomenclature is from an unsupported database or software not listed among the 5 databases and 17 programs; contact the SysMedOs team to generate appropriate configuration files first.
- The use case requires position-specific lipid fragment annotations or cross-database linking beyond unified naming; use LipidLynxX Linker or position annotation modules instead.

## Inputs

- Lipid abbreviation strings in heterogeneous notation (from HMDB, LIPID MAPS LMSD, LipidHome, RefMet, SwissLipids, or 17 supported software tools)
- LipidLynxX nomenclature mapping configuration file (JSON)
- Test dataset with lipid names in multiple notation styles (shorthand, bracketed, alias forms)

## Outputs

- Unified LipidLynxX identifier strings for each input lipid name
- Structured table mapping input heterogeneous lipid names to canonical LipidLynxX IDs
- Validation report confirming conversion correctness and detecting missing mappings

## How to apply

Load the LipidLynxX nomenclature mapping configuration (JSON format) from the SysMedOs/LipidLynxX repository and instantiate the core conversion function. Prepare a test dataset containing lipid names in their source notation styles (shorthand with space e.g. 'PC 16:0_18:2', bracketed format e.g. 'PC(16:0_18:2)', or common aliases like DHA, PAPE, PLPC). Execute the conversion function on each heterogeneous lipid name string and capture the unified LipidLynxX identifier output. Validate that all nomenclature variants representing the same lipid produce identical canonical identifiers and that the output follows the expected LipidLynxX format. Format results as a structured table mapping input names to unified identifiers and verify no conversion errors or missing mappings occurred.

## Related tools

- **LipidLynxX** (Core nomenclature conversion engine; loads and applies unified identifier mapping rules from JSON configuration; accepts heterogeneous lipid notation and outputs canonical LipidLynxX IDs) — https://github.com/SysMedOs/LipidLynxX
- **Black** (Code style formatter used in LipidLynxX source code; ensures consistent Python formatting during development and contribution) — https://github.com/psf/black
- **Visual Studio Code** (Editor for reviewing and editing LipidLynxX JSON configuration files and source code)
- **PyCharm** (IDE for editing and running LipidLynxX source code and JSON configuration files)

## Examples

```
from lynx.converter import LynxConverter; converter = LynxConverter(); unified_id = converter.convert('PC 16:0_18:2'); print(unified_id)
```

## Evaluation signals

- All nomenclature variants for the same lipid produce identical canonical LipidLynxX identifiers (zero variance across input styles)
- Output identifiers conform to the expected LipidLynxX canonical format defined in the JSON schema (no malformed or incomplete outputs)
- Conversion completion rate: 100% of input lipid names are successfully mapped with no missing mappings or errors logged
- Cross-validation: output identifiers can be reverse-mapped or queried against the LipidLynxX database to confirm correctness
- Structured output table contains no null or empty values in unified ID column; all rows have valid mappings

## Limitations

- LipidLynxX may not support databases or software not in the predefined list of 5 databases and 17 programs; custom configuration is required for unsupported sources.
- Common abbreviations such as DHA, PAPE, PLPC are customizable via the defined_alias.json configuration file; non-standard or domain-specific aliases may require manual updates.
- The project's API and documentation may lag behind rapid source code changes; developers planning to use the LipidLynxX API are advised to contact the SysMedOs team first.
- The Windows .exe version is for test purposes only and has known issues if the Linker module runs longer than 300 seconds or more than 30 seconds per ID; restart is required in those cases.

## Evidence

- [other] LipidLynxX is designed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome, enabling standardization of heterogeneous lipid nomenclature across the lipid research domain.: "LipidLynxX is designed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome"
- [other] Load LipidLynxX source code from the SysMedOs/LipidLynxX repository and review the nomenclature mapping configuration (JSON format). Implement or activate the core conversion function that accepts heterogeneous lipid notation strings as input and applies the unified identifier mapping rules.: "Load LipidLynxX source code from the SysMedOs/LipidLynxX repository and review the nomenclature mapping configuration (JSON format). Implement or activate the core conversion function that accepts"
- [other] Prepare a test dataset containing lipid names in multiple notation styles (major lipids and oxidized-lipid formats) from supported databases or software. Execute the conversion function on each test lipid name and capture the output unified identifiers. Validate output identifiers by checking that they follow the expected canonical format and that all input nomenclature variants for the same lipid produce identical unified identifiers.: "Prepare a test dataset containing lipid names in multiple notation styles (major lipids and oxidized-lipid formats) from supported databases or software"
- [readme] The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: Databases (5): HMDB, LIPID MAPS LMSD & COMP_DB, LipidHome, RefMet, SwissLipids; Programs (17): ALEX123 lipid calculator, Greazy, LDA 2, LipidBlast, LipidCreator, LipiDex, LipidFrag, LipidHunter, LipidMatch, LipidPro, LipidSearch, Lipostar, LIQUID, LPPtiger, MetFrag, MS-DIAL, MZmine2: "The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: Databases (5): HMDB, LIPID MAPS LMSD &"
- [readme] Shorthand notation using space: e.g. PC 16:0_18:2; Shorthand notation derivatives using brackets: e.g. PC(16:0_18:2); Common abbreviations (customizable): Abbreviations such as DHA, PAPE, PLPC, PONPC .etc are also included as defined alias: "Shorthand notation using space: e.g. PC 16:0_18:2; Shorthand notation derivatives using brackets: e.g. PC(16:0_18:2)"
- [readme] LipidLynxX source code use code style Black for all python codes; JSON configurations are formatted by Visual Studio Code / PyCharm editor: "JSON configurations are formatted by Visual Studio Code / PyCharm editor"
