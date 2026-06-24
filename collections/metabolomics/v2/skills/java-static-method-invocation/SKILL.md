---
name: java-static-method-invocation
description: Use when you have a Java application or standalone tool that needs to
  predict CYP450-catalyzed metabolites for one or more molecules and you require the
  option to compare predictions with and without CypReact filtering applied.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3371
  edam_topics:
  - http://edamontology.org/topic_0152
  - http://edamontology.org/topic_3407
  tools:
  - BioTransformerAPI
  - CyProduct
  - Java
  - CyProduct.jar
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.1c00144
  title: CyProduct
evidence_spans:
- there is a class called BioTransformerAPI in the jar file
- Please download the CyProduct.jar to run the tool
- Java -jar CyProduct.jar QueryMolecule enzymeList OutputFolderPath
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

# Invoke BioTransformerAPI static functions to predict CYP450 metabolites with conditional filter toggling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Call static methods from the BioTransformerAPI class (packaged in CyProduct.jar) to predict metabolites of a query molecule for specified CYP450 enzymes, with the ability to toggle the CypReact filter module on or off via a boolean parameter. Use this skill when you need programmatic, fine-grained control over metabolite prediction and filter behavior within your own Java application or tool.

## When to use

You have a Java application or standalone tool that needs to predict CYP450-catalyzed metabolites for one or more molecules and you require the option to compare predictions with and without CypReact filtering applied. Typical triggers include: (1) you need to embed metabolite prediction in a larger computational workflow without calling the command-line interface; (2) you want to systematically evaluate the effect of the CypReact filter module on prediction outputs; or (3) you need to pass molecules and enzyme lists programmatically rather than via the command line.

## When NOT to use

- You do not have Java in your execution environment or cannot load the CyProduct.jar file.
- Your input molecule list is very large (>1000s) and you need batch processing — use the command-line interface instead for better resource management.
- You only need a single prediction with a fixed filter setting and do not need to compare filter-on vs. filter-off behavior.

## Inputs

- Query molecule (SMILES string formatted as 'SMILES=yourSmilesString' OR file path to SDF file)
- List of CYP450 enzyme identifiers (comma-separated, without 'CYP' prefix, e.g. '1A2,3A4')
- Boolean useCypReact parameter (true or false)

## Outputs

- Predicted metabolites collection with SoM scores
- Metabolite structures and associated enzyme annotations
- Score values computed per formula Score = (prob−threshold)/(1−threshold)

## How to apply

Import the BioTransformerAPI class from the CyProduct.jar file into your Java project. Prepare your input: a query molecule encoded as either a SMILES string (prefixed with 'SMILES=') or a file path to an SDF file, and a comma-separated list of CYP450 enzyme identifiers (e.g., '1A2,3A4') without the 'CYP' prefix. Call one of the two static functions provided by BioTransformerAPI, passing the molecule, enzyme list, and a boolean useCypReact parameter. When useCypReact is set to false, the CypReact filter module is disabled and all predicted metabolites are returned; when true, metabolites are filtered according to CypReact rules. Repeat the invocation with the opposite boolean value and compare the predicted metabolite sets to quantify the effect of the filter. The output will be a collection of predicted metabolites with their associated SoM (site of metabolism) scores, computed using the formula Score = (prob−threshold)/(1−threshold).

## Related tools

- **BioTransformerAPI** (Static function provider that accepts molecule, enzyme list, and useCypReact boolean to predict metabolites with optional CypReact filtering) — https://github.com/Le0nT1/CyProduct
- **CyProduct.jar** (Packaged Java archive containing the BioTransformerAPI class and supporting metabolite prediction modules (CypBoM, CypReact, MetaboGen)) — https://github.com/Le0nT1/CyProduct

## Examples

```
BioTransformerAPI.predictMetabolites("SMILES=CC(=O)Nc1ccc(O)cc1", "1A2,3A4", false); // Returns metabolites without CypReact filtering
```

## Evaluation signals

- Predicted metabolite sets are non-empty and contain valid molecule structures with valid SMILES representations.
- SoM scores are numeric values in a reasonable range and comply with the formula Score = (prob−threshold)/(1−threshold).
- When useCypReact is set to false, the metabolite set is equal to or larger than when useCypReact is true (CypReact filtering restricts, not expands, predictions).
- Metabolites are correctly annotated with the CYP450 enzymes that catalyze them (drawn from the input enzyme list).
- Calling the static function twice with identical inputs but different useCypReact values produces deterministic, reproducible outputs.

## Limitations

- The BioTransformerAPI is tightly coupled to the CyProduct.jar binary; no standalone or language-neutral interface is documented.
- No version history or changelog is available, so compatibility with specific CyProduct versions is not tracked.
- Enzyme identifiers must be provided without the 'CYP' prefix (e.g., '1A2' not 'CYP1A2'), which is a common source of user error.
- The CypReact filter module's behavior and thresholds are not user-configurable beyond the on/off toggle; no granular control over filter parameters is exposed.
- Performance and scalability characteristics for large-scale batch predictions are not documented.

## Evidence

- [readme] Note that there is a class called BioTransformerAPI in the jar file. It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input, and predict the corresponding metabolites.: "Note that there is a class called BioTransformerAPI in the jar file. It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable"
- [readme] Note that if the useCypReact is set as false, then the CypReact filter module will be disabled.: "if the useCypReact is set as false, then the CypReact filter module will be disabled"
- [readme] The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString.: "The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString."
- [readme] Please note that when you use the CyProduct tool or its API, please input enzyme without 'CYP'. For example, please use 1A2 other than CYP1A2 in both cases.: "please input enzyme without 'CYP'. For example, please use 1A2 other than CYP1A2"
- [readme] The score is computed using formula Score = (prob-threshold)/(1-threshold) where prob is the value predicted for the SoM and threshold = 1/(1+beta).: "The score is computed using formula Score = (prob-threshold)/(1-threshold) where prob is the value predicted for the SoM"
