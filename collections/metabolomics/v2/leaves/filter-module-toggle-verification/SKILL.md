---
name: filter-module-toggle-verification
description: Use when you need to confirm that a software API or tool correctly implements
  a boolean control over an optional filter module, particularly in contexts where
  filter activation state directly affects the set of predicted metabolites.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformerAPI
  - CyProduct
  - Java
  license_tier: restricted
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

# filter-module-toggle-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that a computational filter module (CypReact) in metabolite prediction can be toggled on and off via a boolean parameter, and confirm the toggle controls filter activation state by comparing prediction outputs. This skill is essential when validating API behavior for optional filtering in drug metabolism workflows.

## When to use

Apply this skill when you need to confirm that a software API or tool correctly implements a boolean control over an optional filter module, particularly in contexts where filter activation state directly affects the set of predicted metabolites. Use it when developing or validating metabolite prediction pipelines where CypReact filtering rules may or may not be appropriate for your analysis goals.

## When NOT to use

- Do not use this skill if you need to predict metabolites without access to the BioTransformerAPI class or CyProduct JAR file.
- Do not apply this skill if your goal is only to run metabolite prediction once; toggling verification requires paired runs with different filter states.
- Do not use this skill for tools or APIs that do not expose filter module control via a boolean parameter.

## Inputs

- Query molecule as SMILES string (format: SMILES=yourSmilesString) or path to SDF file
- List of CYP450 enzymes (comma-separated, without 'CYP' prefix; e.g., 1A2,3A4)
- useCypReact boolean parameter (true or false)

## Outputs

- Predicted metabolites for specified CYP450 enzymes (with CypReact filtering disabled)
- Predicted metabolites for specified CYP450 enzymes (with CypReact filtering enabled)
- Comparison of metabolite sets between useCypReact=false and useCypReact=true runs

## How to apply

Instantiate the BioTransformerAPI class from the CyProduct JAR file and prepare test inputs: a query molecule as a SMILES string (format: SMILES=yourSmilesString) or SDF file path, a list of target CYP450 enzymes (e.g., 1A2,3A4; note: input enzyme names without 'CYP' prefix), and the useCypReact boolean parameter. Invoke the static function with useCypReact set to false and capture the output metabolite predictions. Repeat the invocation with useCypReact set to true. Compare the two result sets: when useCypReact=false, the CypReact filter module is disabled and metabolites are predicted without CypReact module constraints; when useCypReact=true, metabolites are filtered according to CypReact rules. The boolean parameter controls filter module activation state if and only if the metabolite sets differ predictably between the two runs, with the true setting producing a subset constrained by CypReact logic.

## Related tools

- **BioTransformerAPI** (Provides static functions that accept a molecule, CYP450 enzyme list, and useCypReact boolean parameter to predict metabolites with or without CypReact filter module active) — https://github.com/Le0nT1/CyProduct
- **CyProduct** (JAR-based tool that wraps BioTransformerAPI and predicts metabolites catalyzed by specified CYP450 enzymes; supports CypReact filter module toggling) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment required to instantiate BioTransformerAPI class and invoke static functions from CyProduct JAR)

## Examples

```
BioTransformerAPI bioapi = new BioTransformerAPI(); List<String> enzymes = Arrays.asList("1A2", "3A4"); String molecule = "CC(=O)Nc1ccc(O)cc1"; List<?> metabolites_disabled = bioapi.predictMetabolites(molecule, enzymes, false); List<?> metabolites_enabled = bioapi.predictMetabolites(molecule, enzymes, true);
```

## Evaluation signals

- Metabolite prediction results differ between useCypReact=false and useCypReact=true runs, with the true setting producing a subset of predictions (filtered by CypReact rules).
- When useCypReact=false, metabolites predicted include those that would be filtered out by CypReact logic; when useCypReact=true, only CypReact-compliant metabolites remain.
- The enzyme list and query molecule inputs remain constant across both runs; only the useCypReact parameter changes, isolating the filter module's effect.
- Output files or returned metabolite objects can be compared element-by-element to confirm set difference; predictions should be reproducible within runs.
- Documentation or API behavior confirms that useCypReact=false disables the CypReact filter module and useCypReact=true re-enables it without affecting other prediction logic.

## Limitations

- No version history or changelog is available for CyProduct, so it is unclear whether the useCypReact boolean behavior has changed across releases.
- The skill assumes the query molecule is valid SMILES or a well-formed SDF; malformed input will not demonstrate filter module behavior.
- CypReact filtering logic is embedded in the JAR; users cannot inspect or modify the filtering rules themselves, only toggle the module on or off.
- Comparison of metabolite sets requires post-processing of output files or API responses; the BioTransformerAPI README does not specify output format or structure in detail.

## Evidence

- [readme] It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input, and predict the corresponding metabolites.: "It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input, and predict the corresponding metabolites."
- [readme] if the useCypReact is set as false, then the CypReact filter module will be disabled: "if the useCypReact is set as false, then the CypReact filter module will be disabled"
- [other] when useCypReact is set to false, the CypReact filter module is disabled (metabolites are predicted without CypReact module constraints): "when useCypReact is set to false, the CypReact filter module is disabled (metabolites are predicted without CypReact module constraints)"
- [readme] please input enzyme without "CYP". For example, please use 1A2 other than CYP1A2: "please input enzyme without "CYP". For example, please use 1A2 other than CYP1A2"
- [other] Compare outputs between both runs to confirm the boolean parameter controls filter module activation state.: "Compare outputs between both runs to confirm the boolean parameter controls filter module activation state."
