---
name: validation-test-design-for-biochemical-identifiers
description: Use when you have implemented or integrated a biochemical identifier
  converter (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidLynxX
  - Black
  - Visual Studio Code
  - PyCharm
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.04.09.033894
  title: LipidLynxX
evidence_spans:
- The LipidLynxX project is aimed to provide a unified identifier for major lipids
- LipidLynxX source code use [code style Black](https://github.com/psf/black) for
  all python codes
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

# validation-test-design-for-biochemical-identifiers

## Summary

Design and execute validation tests to verify that a biochemical identifier converter correctly maps heterogeneous nomenclature variants into a unified, canonical identifier format. This skill ensures identifier consistency, completeness, and correctness across multiple input notation styles and biological databases.

## When to use

Apply this skill when you have implemented or integrated a biochemical identifier converter (e.g., LipidLynxX for lipid nomenclature) and need to verify that all supported input nomenclature styles—from major and oxidized lipid variants across multiple databases (HMDB, LIPID MAPS, LipidHome, RefMet, SwissLipids) and software tools (MS-DIAL, LipidSearch, LipidBlast, etc.)—consistently produce identical unified identifiers and follow the expected canonical format.

## When NOT to use

- Input lipid names are already in the unified LipidLynxX identifier format—skip conversion testing and proceed directly to cross-comparison or linking workflows.
- The converter configuration has not been finalized or validated against schema—first validate the JSON configuration before testing conversion output.
- You are only testing a single notation style or single database source—this skill requires heterogeneous input from multiple databases and software tools to verify cross-notation consistency.

## Inputs

- Heterogeneous lipid nomenclature strings (from major lipids and oxidized-lipid formats)
- Lipid names in multiple notation styles (shorthand space-delimited, bracket-enclosed, defined aliases)
- LipidLynxX nomenclature mapping configuration (JSON format)
- Test dataset with lipid abbreviations from supported databases (HMDB, LIPID MAPS LMSD & COMP_DB, LipidHome, RefMet, SwissLipids) and software (ALEX123, Greazy, LDA 2, LipidBlast, LipidCreator, LipiDex, LipidFrag, LipidHunter, LipidMatch, LipidPro, LipidSearch, Lipostar, LIQUID, LPPtiger, MetFrag, MS-DIAL, MZmine2)

## Outputs

- Structured validation table mapping input nomenclature to output unified identifiers
- Unified lipid identifiers in canonical format
- Conversion error report (if any input failed to map)
- Coverage report (completeness of mappings across all input styles)

## How to apply

Construct a test dataset containing lipid names in multiple notation styles (shorthand with spaces e.g. 'PC 16:0_18:2', bracket derivatives e.g. 'PC(16:0_18:2)', and defined aliases like 'DHA' or 'PLPC') sourced from the converter's supported databases and software. Load the converter's nomenclature mapping configuration (JSON format) and execute the core conversion function on each test lipid name, capturing the output unified identifier. Validate outputs by verifying that: (1) all output identifiers follow the expected canonical format defined by the converter's JSON schema; (2) all nomenclature variants for the same biological lipid produce identical unified identifiers; and (3) no conversion errors or missing mappings occurred. Format results as a structured table mapping input names to output identifiers and systematically check for conversion failures.

## Related tools

- **LipidLynxX** (Core biochemical identifier converter; provides unified identifier mapping rules via JSON configuration and executes conversion function on heterogeneous lipid nomenclature input) — https://github.com/SysMedOs/LipidLynxX
- **Black** (Python code formatter used to maintain code style consistency in LipidLynxX implementation during converter development and validation test authoring) — https://github.com/psf/black
- **Visual Studio Code** (Editor for formatting and reviewing LipidLynxX JSON nomenclature mapping configuration files used in validation test setup)
- **PyCharm** (IDE for formatting and reviewing LipidLynxX JSON nomenclature mapping configuration files and implementing validation test scripts)

## Examples

```
python cli_lynx.py --input test_lipids.csv --output validated_identifiers.csv --validate --format json
```

## Evaluation signals

- All test lipid names successfully convert without errors or missing mappings; conversion error report is empty.
- All nomenclature variants representing the same biological lipid produce identical unified identifiers (e.g., 'PC 16:0_18:2', 'PC(16:0_18:2)', and any database-specific aliases all map to the same canonical LipidLynxX ID).
- All output unified identifiers strictly conform to the expected canonical format defined in the LipidLynxX JSON schema (format validation passes).
- Coverage report shows 100% or near-100% successful mapping across test inputs from all supported databases and software tools; any unmapped inputs are documented and justified.
- Structured output table has no null/missing entries in the unified identifier column; each row has a 1:1 input–output mapping traceable to the configuration rule that produced it.

## Limitations

- If a database or software tool is not included in the pre-defined configuration files (located in `lynx/configurations/rules/input`), conversion may fail; a new custom configuration file must be generated and validated separately.
- The test dataset quality directly affects validation completeness—missing or incorrectly formatted nomenclature examples in the input test set will result in incomplete coverage assessment.
- LipidLynxX source code is under active development; API definitions and documentation may lag behind implementation changes, requiring validation logic to be updated or re-verified when the converter is upgraded.
- Known issue: if the Linker module runs for more than 300 seconds or more than 30 seconds per ID, the tool may timeout, affecting validation of lipid linking steps; restart LipidLynxX and retry if this occurs.

## Evidence

- [other] Prepare a test dataset containing lipid names in multiple notation styles (major lipids and oxidized-lipid formats) from supported databases or software.: "Prepare a test dataset containing lipid names in multiple notation styles (major lipids and oxidized-lipid formats) from supported databases or software."
- [other] Validate output identifiers by checking that they follow the expected canonical format and that all input nomenclature variants for the same lipid produce identical unified identifiers.: "Validate output identifiers by checking that they follow the expected canonical format and that all input nomenclature variants for the same lipid produce identical unified identifiers."
- [readme] The LipidLynxX project is aimed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome.: "The LipidLynxX project is aimed to provide a unified identifier for major lipids, especially oxidized lipids in the epilipidome."
- [readme] The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: Databases (5): HMDB, LIPID MAPS LMSD & COMP_DB, LipidHome, RefMet, SwissLipids; Programs (17): ALEX123 lipid calculator, Greazy, LDA 2, LipidBlast, LipidCreator, LipiDex, LipidFrag, LipidHunter, LipidMatch, LipidPro, LipidSearch, Lipostar, LIQUID, LPPtiger, MetFrag, MS-DIAL, MZmine2.: "The current LipidLynxX source code was tested using our collection of lipid abbreviations for major lipid classes from following databases and programs: Databases (5): HMDB, LIPID MAPS LMSD &"
- [readme] Shorthand notation using space: e.g. PC 16:0_18:2; Shorthand notation derivatives using brackets: e.g. PC(16:0_18:2): "Shorthand notation using space: e.g. PC 16:0_18:2; Shorthand notation derivatives using brackets: e.g. PC(16:0_18:2)"
- [readme] If your database / program is not included in the list above, you can test if any of the configuration files located in `lynx/configurations/rules/input` would fit to your database / program. If conversion is not possible, please contact us so that we can help you to generate suitable configuration file.: "If your database / program is not included in the list above, you can test if any of the configuration files located in `lynx/configurations/rules/input` would fit to your database / program."
- [readme] Strictly controlled format using JSON schema: "Strictly controlled format using JSON schema"
