---
name: cyp450-enzyme-list-specification
description: Use when when you need to predict drug or xenobiotic metabolites across
  multiple CYP450 isoforms and must communicate which specific enzymes (e.g., 1A2,
  2C9, 3A4) should be evaluated. Use this skill before invoking a metabolite prediction
  tool that accepts an enzyme list parameter.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0820
  - http://edamontology.org/topic_3407
  tools:
  - CyProduct
  - BioTransformerAPI
  - Java
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.1c00144
  title: CyProduct
evidence_spans:
- Please download the CyProduct.jar to run the tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cyproduct_cq
    doi: 10.1021/acs.jcim.1c00144
    title: CyProduct
  dedup_kept_from: coll_cyproduct_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.1c00144
  all_source_dois:
  - 10.1021/acs.jcim.1c00144
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cyp450-enzyme-list-specification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Specify a list of cytochrome P450 (CYP450) enzyme isoforms as a formatted input parameter for metabolite prediction tools like CyProduct. This skill ensures correct enzyme selection and proper formatting to enable multi-enzyme metabolic transformation prediction.

## When to use

When you need to predict drug or xenobiotic metabolites across multiple CYP450 isoforms and must communicate which specific enzymes (e.g., 1A2, 2C9, 3A4) should be evaluated. Use this skill before invoking a metabolite prediction tool that accepts an enzyme list parameter.

## When NOT to use

- Input enzyme list already includes the 'CYP' prefix (e.g., 'CYP1A2')—this will cause parsing errors; strip the prefix first.
- Predicting metabolites catalyzed by non-CYP450 enzymes (e.g., UGT, SULT, MAO)—use alternative enzyme specification workflows for those families.
- Enzyme list is empty or None—CyProduct requires at least one enzyme identifier to function.

## Inputs

- List of CYP450 enzyme identifiers (e.g., '1A2,3A4')
- Target enzyme isoforms from the major human CYP450 family (1A2, 2A6, 2B6, 2C8, 2C9, 2C19, 2D6, 2E1, 3A4)

## Outputs

- Formatted enzymeList parameter string suitable for command-line or API input
- Specification record identifying which CYP450 isoforms will be evaluated in downstream metabolite prediction

## How to apply

Construct a comma-separated list of CYP450 enzyme identifiers without the 'CYP' prefix (e.g., '1A2,2A6,2C9,3A4'). Verify that enzyme names match the tool's expected nomenclature—CyProduct requires bare enzyme names like '1A2' rather than 'CYP1A2'. Pass this formatted string as the enzymeList parameter to the command-line tool. If using the BioTransformerAPI class, pass the enzyme list to either of the two static functions that accept a list of CYP450 enzymes as input. The tool will then predict metabolites for all specified enzymes, and metabolites are reported as catalyzed by individual enzymes or combinations thereof depending on prediction consensus.

## Related tools

- **CyProduct** (Metabolite prediction engine that accepts the enzyme list to predict transformations across specified CYP450 isoforms) — https://github.com/Le0nT1/CyProduct
- **BioTransformerAPI** (Java API class within CyProduct.jar offering static functions that accept enzyme lists and optional useCypReact boolean parameter) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment for executing CyProduct.jar with the specified enzyme list parameter)

## Examples

```
java -jar CyProduct.jar CC(=O)Nc1ccc(O)cc1 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4 E:\Users\cyproduct\
```

## Evaluation signals

- Enzyme list contains only valid CYP450 isoform identifiers without 'CYP' prefix (e.g., '1A2,2C9' not 'CYP1A2,CYP2C9')
- Comma-separated format with no spaces or extraneous characters (e.g., '1A2,3A4' not '1A2, 3A4' or '1A2|3A4')
- Tool execution completes without enzyme nomenclature errors or 'unrecognized enzyme' warnings
- Output metabolite predictions are attributed to the correct subset of specified enzymes (e.g., metabolites from '1A2,3A4' list show only those two enzymes in results, not others)
- API call to BioTransformerAPI static functions accepts the formatted enzyme list without type mismatch or parameter rejection

## Limitations

- CyProduct supports only nine major human CYP450 isoforms (1A2, 2A6, 2B6, 2C8, 2C9, 2C19, 2D6, 2E1, 3A4); enzymes outside this set will not be recognized.
- Enzyme names must omit the 'CYP' prefix; using standard IUPAC nomenclature (e.g., 'CYP1A2') will cause parsing failure.
- No built-in validation of enzyme list order or redundancy; duplicate entries (e.g., '1A2,1A2') will be processed without warning.
- Metabolite predictions are filtered through the CypReact module by default; disabling this filter (useCypReact=false in API) alters predicted output and should be explicitly controlled.

## Evidence

- [readme] The enzymeList is the list of CYP450 enzymes you want to run CyProduct on. If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them. For example, if the input enzyme list is 1A2,3A4, then metabolites predicted are catalyzed by either 1A2 or 3A4 or both of them.: "The enzymeList is the list of CYP450 enzymes you want to run CyProduct on. If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them. For example, if"
- [readme] Please note that when you use the CyProduct tool or its API, please input enzyme without 'CYP'. For example, please use 1A2 other than CYP1A2 in both cases.: "Please note that when you use the CyProduct tool or its API, please input enzyme without 'CYP'. For example, please use 1A2 other than CYP1A2 in both cases."
- [readme] It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input, and predict the corresponding metabolites.: "It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input, and predict the corresponding metabolites."
- [other] Define the 9-enzyme CYP450 list (e.g., 1A2, 3A4, and 7 others) as the enzymeList parameter.: "Define the 9-enzyme CYP450 list (e.g., 1A2, 3A4, and 7 others) as the enzymeList parameter."
