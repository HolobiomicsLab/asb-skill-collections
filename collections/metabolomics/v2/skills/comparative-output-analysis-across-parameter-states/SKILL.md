---
name: comparative-output-analysis-across-parameter-states
description: Use when when you need to validate that a boolean control parameter in BioTransformerAPI (useCypReact) properly gates a filtering module, or when you want to understand the qualitative and quantitative impact of CypReact filtering rules on predicted metabolite outputs for a given substrate and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformerAPI
  - CyProduct
  - Java
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
---

# comparative-output-analysis-across-parameter-states

## Summary

Compare metabolite predictions from BioTransformerAPI under different boolean parameter states (useCypReact on vs. off) to validate that the CypReact filter module toggles correctly and understand how filtering constraints affect predicted metabolite sets.

## When to use

When you need to validate that a boolean control parameter in BioTransformerAPI (useCypReact) properly gates a filtering module, or when you want to understand the qualitative and quantitative impact of CypReact filtering rules on predicted metabolite outputs for a given substrate and enzyme set.

## When NOT to use

- Input molecule is not a valid SMILES string or accessible SDF file path
- Enzyme list is empty or contains enzyme names with the CYP prefix (e.g., CYP1A2 instead of 1A2)
- You only need a single metabolite prediction without understanding filter effects—use direct API invocation instead

## Inputs

- query molecule as SMILES string (format: SMILES=yourSmilesString)
- query molecule as SDF file path
- list of CYP450 enzymes (format: 1A2,3A4,2C9, etc.; without CYP prefix)
- useCypReact boolean parameter (true or false)

## Outputs

- predicted metabolite set with useCypReact=false (CypReact filter disabled)
- predicted metabolite set with useCypReact=true (CypReact filter enabled)
- set difference analysis (metabolites exclusive to each state, intersection)

## How to apply

Invoke the BioTransformerAPI static function twice with identical inputs (query molecule as SMILES or SDF path, target CYP450 enzyme list) but set useCypReact to false in the first run and true in the second. Capture the predicted metabolite sets from both runs. Compare the outputs by examining which metabolites appear in the true-CypReact set versus the false-CypReact set; metabolites should be filtered according to CypReact rules when useCypReact=true. Compute set differences (union, intersection, metabolites exclusive to each state) to quantify the filtering effect. Verify that the boolean parameter deterministically controls filter activation state by confirming that repeated runs with the same parameter produce identical outputs.

## Related tools

- **BioTransformerAPI** (Java class that provides static functions accepting a molecule, CYP450 enzyme list, and useCypReact boolean to predict metabolites with optional CypReact filtering) — https://github.com/Le0nT1/CyProduct
- **CyProduct** (JAR executable that wraps BioTransformerAPI for command-line metabolite prediction with CypReact filter toggle support) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment required to instantiate BioTransformerAPI class and invoke static functions)

## Examples

```
BioTransformerAPI api = new BioTransformerAPI(); Molecule mol = Molecule.fromSMILES("CC(=O)Nc1ccc(O)cc1"); List<String> enzymes = Arrays.asList("1A2", "3A4"); List<Molecule> resultsFalse = api.predictMetabolites(mol, enzymes, false); List<Molecule> resultsTrue = api.predictMetabolites(mol, enzymes, true); // Compare resultsFalse (unfiltered) vs resultsTrue (CypReact-filtered)
```

## Evaluation signals

- Verify that the metabolite set with useCypReact=false is a superset of or equal to the set with useCypReact=true (CypReact filtering removes or constrains metabolites, never adds them)
- Confirm that repeated runs with identical inputs and parameter values produce identical metabolite outputs (deterministic behavior)
- Inspect that metabolites exclusive to the useCypReact=false set satisfy CypReact filtering rules; those exclusive to useCypReact=true should violate such rules
- Validate that the union of metabolites across both parameter states equals the full prediction space without filtering
- Check that all predicted metabolites are associated with the specified CYP450 enzymes and represent chemically reasonable biotransformations

## Limitations

- No changelog or version history is documented, making it difficult to track whether filter behavior has changed across CyProduct releases
- The CypReact filter module's exact rule set and thresholds are not detailed in the README; only the on/off toggle is documented
- Comparison outputs depend on the quality and completeness of the underlying metabolite prediction model; filtering cannot improve predictions of unreliable base predictions
- Enzyme list input requires careful formatting without CYP prefix; malformed enzyme names will silently fail or produce incorrect results

## Evidence

- [readme] BioTransformerAPI.static_function_invocation: "there is a class called BioTransformerAPI in the jar file. It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input"
- [readme] CypReact_filter_toggle: "if the useCypReact is set as false, then the CypReact filter module will be disabled"
- [readme] enzyme_list_formatting: "please input enzyme without "CYP". For example, please use 1A2 other than CYP1A2"
- [other] comparative_workflow: "Repeat steps 2–4 with useCypReact set to true and confirm that CypReact filtering is active (metabolites are filtered according to CypReact rules). Compare outputs between both runs to confirm the"
- [readme] input_formats: "The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString"
