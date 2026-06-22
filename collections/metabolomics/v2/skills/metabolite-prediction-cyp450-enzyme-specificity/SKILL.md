---
name: metabolite-prediction-cyp450-enzyme-specificity
description: Use when you have a small-molecule query (acetaminophen, drug candidate, xenobiotic, or other compound as SMILES or SDF) and need to predict which metabolites would be formed if that molecule were metabolized by a defined subset of the nine major human CYP450 isoforms (1A2, 2A6, 2B6, 2C8, 2C9.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0202
  - http://edamontology.org/topic_3375
  tools:
  - CyProduct
  - Java
  - BioTransformerAPI
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
---

# metabolite-prediction-cyp450-enzyme-specificity

## Summary

Predict phase I metabolites of a query molecule by simulating biotransformation reactions catalyzed by one or more cytochrome P450 (CYP450) enzymes using CyProduct. Use this skill when you need to enumerate probable metabolite structures and their enzymatic origins for drug development, toxicity assessment, or mechanistic pathway analysis.

## When to use

You have a small-molecule query (acetaminophen, drug candidate, xenobiotic, or other compound as SMILES or SDF) and need to predict which metabolites would be formed if that molecule were metabolized by a defined subset of the nine major human CYP450 isoforms (1A2, 2A6, 2B6, 2C8, 2C9, 2C19, 2D6, 2E1, 3A4). Apply this skill when your hypothesis or experimental design requires enzyme-specific metabolite predictions rather than generic biotransformation or when you need to validate predicted metabolite outcomes against literature or experimental data.

## When NOT to use

- Your input molecule is not a discrete small molecule (e.g., you have a protein sequence, DNA, or a complex mixture)
- You need to predict phase II metabolism (glucuronidation, sulfation, acetylation) rather than phase I CYP450-catalyzed oxidation
- You require kinetic parameters (Km, Vmax) or relative turnover rates; CyProduct predicts structures, not enzyme kinetics

## Inputs

- Query molecule as SMILES string (format: SMILES=CC(=O)Nc1ccc(O)cc1) or file path to SDF
- Comma-separated list of CYP450 enzyme codes (e.g., 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4)
- Output folder path for storing predicted results

## Outputs

- Predicted metabolite structures (SDF or equivalent format) catalyzed by specified CYP450 enzymes
- Site-of-metabolism (SoM) scores and confidence metrics for each predicted metabolite
- Enzymatic attribution for each metabolite (which CYP450(s) catalyze its formation)

## How to apply

Prepare your query molecule as either a SMILES string (prefixed with 'SMILES=') or as a path to an SDF file; then specify which CYP450 enzymes (comma-separated list, without the 'CYP' prefix—e.g., '1A2,3A4,2D6') you want to run predictions against. Invoke CyProduct via command-line Java execution with these three parameters: the query molecule, the enzyme list, and an output folder path. By default, CyProduct applies its CypReact filter module to refine predictions; you can disable this by setting useCypReact to false if you want unfiltered metabolite generation. Collect predicted metabolites from the output folder; each result includes metabolite structures and enzymatic associations. The CypBoM module scores site-of-metabolism predictions using the formula Score = (prob−threshold)/(1−threshold), where threshold = 1/(1+beta) and beta derives from the learning process; review these scores to prioritize high-confidence predictions.

## Related tools

- **CyProduct** (Primary execution engine for CYP450-specific metabolite prediction via command-line or embedded BioTransformerAPI) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment required to execute CyProduct.jar)
- **BioTransformerAPI** (Embedded static API class within CyProduct.jar for programmatic metabolite prediction and CypReact filter control) — https://github.com/Le0nT1/CyProduct

## Examples

```
java -jar CyProduct.jar CC(=O)Nc1ccc(O)cc1 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4 E:\Users\cyproduct\
```

## Evaluation signals

- Output folder contains predicted metabolite files with no errors or missing entries for each queried enzyme
- Returned metabolites show plausible structural transformations consistent with known CYP450 reaction chemistry (e.g., hydroxylation, epoxidation, N-dealkylation for acetaminophen)
- Each predicted metabolite is tagged with at least one enzyme identifier (1A2, 3A4, etc.) indicating its catalytic origin
- Site-of-metabolism scores fall within the expected range (0–1 after normalization by Score formula) with higher scores for chemically reactive positions
- When CypReact is disabled (useCypReact=false), metabolite count increases or remains stable; when enabled, count may decrease due to filtering

## Limitations

- CyProduct predictions are in silico and should be validated experimentally; predicted metabolites may not reflect in vivo biotransformation rates or enzyme competition
- The tool is trained on Zaretzki's CYP450 substrate datasets (679 compounds in EBoMD.sdf); accuracy may degrade for structurally novel query molecules far outside the training distribution
- Prediction quality depends on correct enzyme nomenclature (must omit 'CYP' prefix); inputting 'CYP1A2' instead of '1A2' will cause errors
- CyProduct does not model enzyme inhibition, induction, or allosteric effects; it assumes independent, parallel enzyme action
- No changelog or version history is documented; development changes and model updates are not tracked

## Evidence

- [readme] Query molecule SMILES and enzyme list format: "The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString. The enzymeList is the list"
- [readme] Command-line invocation syntax: "Java -jar CyProduct.jar QueryMolecule enzymeList OutputFolderPath"
- [readme] Enzyme nomenclature requirement: "Please note that when you use the CyProduct tool or its API, please input enzyme without 'CYP'. For example, please use 1A2 other than CYP1A2 in both cases."
- [readme] CypReact filter module control: "Note that if the useCypReact is set as false, then the CypReact filter module will be disabled."
- [readme] SoM scoring formula: "The score is computed using formula Score = (prob-threshold)/(1-threshold) where prob is the value predicted for the SoM and threshold = 1/(1+beta)."
- [readme] BioTransformerAPI static functions: "There is a class called BioTransformerAPI in the jar file. It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as"
- [readme] Multi-enzyme metabolite union behavior: "If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them. For example, if the input enzyme list is 1A2,3A4, then metabolites predicted are catalyzed by"
