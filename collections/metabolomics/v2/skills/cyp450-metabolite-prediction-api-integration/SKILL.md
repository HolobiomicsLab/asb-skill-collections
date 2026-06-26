---
name: cyp450-metabolite-prediction-api-integration
description: Use when you need to embed CYP450 metabolite prediction directly into
  a larger Java software pipeline or require dynamic toggling of the CypReact filter
  module based on experimental parameters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0305
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3325
  tools:
  - BioTransformerAPI
  - CyProduct
  - Java
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.1c00144
  title: CyProduct
evidence_spans:
- there is a class called BioTransformerAPI in the jar file
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

# cyp450-metabolite-prediction-api-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate the BioTransformerAPI static functions into custom Java applications to predict CYP450-catalyzed metabolites with optional CypReact filtering. This skill enables programmatic control over metabolite prediction workflows without relying on command-line invocation.

## When to use

You need to embed CYP450 metabolite prediction directly into a larger Java software pipeline or require dynamic toggling of the CypReact filter module based on experimental parameters. Use this skill when command-line execution is impractical or when you need to iterate over multiple molecules and enzyme sets within a single application session.

## When NOT to use

- Input molecule is not in SMILES or SDF format — CyProduct does not support other chemical structure representations.
- Enzyme list includes 'CYP' prefix (e.g., 'CYP1A2') — the API requires enzyme identifiers without this prefix.
- You need to process results outside Java — the BioTransformerAPI is accessible only through Java instantiation and requires Java memory access to capture outputs.

## Inputs

- Query molecule as SMILES string (format: 'SMILES=yourSmilesString') or SDF file path
- Comma-separated list of CYP450 enzyme identifiers (e.g., '1A2,3A4', '2C9,2D6,3A4')
- Boolean parameter useCypReact (true or false)

## Outputs

- Predicted metabolites catalyzed by specified CYP450 enzymes
- Metabolite predictions with or without CypReact filter constraints depending on useCypReact parameter
- Score values computed as (prob-threshold)/(1-threshold) for each predicted site of metabolism

## How to apply

Instantiate or access the BioTransformerAPI class from the CyProduct JAR file. Prepare inputs: a query molecule as a SMILES string (formatted as 'SMILES=yourSmilesString') or an SDF file path, a comma-separated list of CYP450 enzyme identifiers (without 'CYP' prefix, e.g., '1A2,3A4'), and a boolean useCypReact parameter. Invoke the appropriate BioTransformerAPI static function with these inputs. Set useCypReact to false to disable CypReact filtering (metabolites predicted without module constraints) or true to enable CypReact-based filtering. Capture the predicted metabolite output and compare results between filter states to validate that the boolean parameter correctly controls the filter module activation state.

## Related tools

- **BioTransformerAPI** (Static function class providing direct metabolite prediction with useCypReact boolean control; accessed via CyProduct JAR instantiation in Java) — https://github.com/Le0nT1/CyProduct
- **CyProduct** (JAR file containing the BioTransformerAPI class and CypBoM/CypReact modules; must be downloaded and imported into Java project) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment for instantiating BioTransformerAPI and invoking static functions; required version not specified)

## Examples

```
BioTransformerAPI.predictMetabolites("SMILES=CC(=O)Nc1ccc(O)cc1", "1A2,3A4", true);
```

## Evaluation signals

- Verify output metabolites are catalyzed by the specified enzyme list: when enzyme list is '1A2,3A4', metabolites should be those catalyzed by 1A2 or 3A4 or both.
- Compare metabolite predictions with useCypReact=false vs. useCypReact=true: the false case should include metabolites filtered out in the true case.
- Validate SMILES input format: confirm that enzyme names lack 'CYP' prefix (e.g., use '1A2' not 'CYP1A2') and SMILES strings use 'SMILES=...' format.
- Check score computation: verify that reported scores follow the formula Score = (prob-threshold)/(1-threshold) where threshold = 1/(1+beta).
- Confirm no exceptions or null returns when invoking static functions with valid inputs; verify metabolite output objects are non-empty.

## Limitations

- Version history and development changes are undocumented — no changelog found; users cannot easily track API evolution or breaking changes.
- API requires Java expertise and direct JAR file manipulation; integration into non-Java ecosystems requires bridging layers (e.g., JNI, REST wrapper).
- The CypReact filter toggle is coarse-grained (all-or-nothing boolean); no fine-grained control over individual CypReact sub-rules or filtering thresholds is documented.
- Enzyme identifiers must exclude the 'CYP' prefix; this convention differs from standard IUPAC nomenclature and is a common source of user error.

## Evidence

- [readme] BioTransformerAPI provides static functions to enable direct metabolite prediction in Java.: "Note that there is a class called BioTransformerAPI in the jar file. It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable"
- [readme] The useCypReact boolean parameter controls whether CypReact filtering is active.: "Note that if the useCypReact is set as false, then the CypReact filter module will be disabled."
- [readme] Multiple enzyme inputs produce union of metabolites across all specified enzymes.: "If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them. For example, if the input enzyme list is 1A2,3A4, then metabolites predicted are catalyzed by"
- [readme] SMILES and SDF are the supported input molecule formats.: "The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString."
- [readme] Enzyme identifiers must be provided without the 'CYP' prefix.: "Please note that when you use the CyProduct tool or its API, please input enzyme without "CYP". For example, please use 1A2 other than CYP1A2 in both cases."
