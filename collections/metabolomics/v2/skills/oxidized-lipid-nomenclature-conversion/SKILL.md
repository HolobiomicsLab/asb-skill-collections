---
name: oxidized-lipid-nomenclature-conversion
description: Use when you have lipid identifiers from multiple sources (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
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

# oxidized-lipid-nomenclature-conversion

## Summary

Convert heterogeneous lipid nomenclature from major lipids and oxidized lipids into a unified identifier system using LipidLynxX. This skill standardizes lipid names across databases and software tools, enabling consistent representation of both unmodified and oxidized lipids in lipidomics research.

## When to use

Apply this skill when you have lipid identifiers from multiple sources (e.g., HMDB, LIPID MAPS, LipidBlast, MS-DIAL, LipidSearch) and need to map them to a canonical form for cross-database comparison or when integrating oxidized lipid annotations from different nomenclature styles into a single standardized namespace.

## When NOT to use

- Input lipid names are already in LipidLynxX unified identifier format—conversion is redundant
- Lipid nomenclature is from a database or software not in the 22 supported sources and no matching configuration file exists
- Oxidized lipid modifications or position-specific annotations are not recognized in the current LipidLynxX JSON schema

## Inputs

- heterogeneous lipid nomenclature strings from HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids, ALEX123, Greazy, LDA 2, LipidBlast, LipidCreator, LipiDex, LipidFrag, LipidHunter, LipidMatch, LipidPro, LipidSearch, Lipostar, LIQUID, LPPtiger, MetFrag, MS-DIAL, MZmine2
- LipidLynxX JSON configuration files defining nomenclature mapping rules
- lipid names in shorthand notation (space-separated or bracket-enclosed)
- common lipid abbreviations (e.g., DHA, PAPE, PLPC, PONPC)

## Outputs

- unified LipidLynxX identifiers in canonical format
- structured table mapping input nomenclature to output unified identifiers
- validation report indicating conversion success/failure per input

## How to apply

Load the LipidLynxX nomenclature mapping configuration (JSON format) from the SysMedOs/LipidLynxX repository, which contains rules for major lipid classes and oxidized lipid modifications. Prepare input lipid names in any of the supported notation styles—shorthand with spaces (e.g., PC 16:0_18:2), bracketed shorthand (e.g., PC(16:0_18:2)), or abbreviations from the 22 supported databases and programs. Execute the core conversion function on each input lipid name, applying the unified identifier mapping rules sequentially. Validate that all nomenclature variants representing the same lipid produce identical unified identifiers and that output identifiers conform to the canonical format. Format results as a structured table mapping input names to output identifiers, and confirm no conversion errors or missing mappings occurred.

## Related tools

- **LipidLynxX** (Core converter tool that applies JSON nomenclature mapping rules to transform heterogeneous lipid identifiers into unified canonical identifiers for major and oxidized lipids) — https://github.com/SysMedOs/LipidLynxX
- **Black** (Python code formatter used in LipidLynxX source code to ensure consistent code style) — https://github.com/psf/black
- **Visual Studio Code** (Editor for formatting and editing LipidLynxX JSON nomenclature configuration files)
- **PyCharm** (IDE for formatting and editing LipidLynxX JSON nomenclature configuration files)

## Examples

```
from LipidLynxX import LipidLynxXConverter; converter = LipidLynxXConverter(); unified_id = converter.convert('PC 16:0_18:2'); print(unified_id)
```

## Evaluation signals

- All nomenclature variants for the same lipid produce identical unified identifiers (invariant: one lipid ↔ one unified ID)
- Output identifiers follow the expected LipidLynxX canonical format and pass JSON schema validation
- No conversion errors or missing mappings are reported for test dataset; conversion success rate equals 100% for supported notation styles
- Cross-validation: identifiers from different input notation styles can be extracted and compared at shared hierarchy levels using the LipidLynxX Equalizer
- Structured output table contains complete mapping rows with no null or malformed unified identifiers

## Limitations

- Lipid nomenclature from unsupported databases or software requires manual configuration file generation; the tool cannot convert notation styles outside its 22 predefined sources
- Rapid source code changes mean API definitions and documentation may not be updated synchronously; developers should contact the SysMedOs team before integrating LipidLynxX API into production systems
- Windows .exe version has known issues: Linker module fails if runtime exceeds 300 seconds or individual ID processing exceeds 30 seconds; maximum 3 concurrent tasks recommended

## Evidence

- [intro] LipidLynxX is designed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome, enabling standardization of heterogeneous lipid nomenclature across the lipid research domain.: "The LipidLynxX project is aimed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome."
- [methods] The conversion workflow loads configuration, applies rules to input nomenclature, and validates output identifiers.: "Load LipidLynxX source code from the SysMedOs/LipidLynxX repository and review the nomenclature mapping configuration (JSON format). 2. Implement or activate the core conversion function that accepts"
- [methods] Testing requires a diverse dataset spanning multiple supported databases and software programs.: "Prepare a test dataset containing lipid names in multiple notation styles (major lipids and oxidized-lipid formats) from supported databases or software."
- [methods] Validation confirms output identifiers are canonical and consistent across input variants.: "Validate output identifiers by checking that they follow the expected canonical format and that all input nomenclature variants for the same lipid produce identical unified identifiers."
- [readme] The tool supports 22 distinct data sources across databases and bioinformatics programs.: "The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: - Databases (5): `HMDB`, `LIPID MAPS LMSD &"
- [readme] Multiple nomenclature input formats are supported to accommodate existing workflows.: "Shorthand notation using space: e.g. PC 16:0_18:2 - Shorthand notation derivatives using brackets: e.g. PC(16:0_18:2) - Common abbreviations (customizable): Abbreviations such as DHA, PAPE, PLPC,"
- [readme] Configuration files are JSON-formatted and can be extended for new notation styles.: "If your database / program is not included in the list above, you can test if any of the configuration files located in `lynx/configurations/rules/input` would fit to your database / program."
- [readme] Known performance limitations exist for the Windows executable version.: "Known issues: if Linker runs more than 300s or more than 30s/per ID, please restart LipidLynxX and try again."
