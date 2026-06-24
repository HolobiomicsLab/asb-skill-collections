---
name: metabolite-output-interpretation
description: Use when after running CyProduct with a query molecule (SMILES or SDF)
  and a list of CYP450 enzymes, use this skill to collect, organize, and validate
  the predicted metabolite results stored in the output folder.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - CyProduct
  - BioTransformerAPI
  - Java
  license_tier: restricted
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

# metabolite-output-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret and validate predicted metabolite outputs from CyProduct by collecting results from specified output folders, verifying enzyme-specific catalysis assignments, and optionally filtering through the CypReact module to ensure metabolites are biochemically plausible.

## When to use

After running CyProduct with a query molecule (SMILES or SDF) and a list of CYP450 enzymes, use this skill to collect, organize, and validate the predicted metabolite results stored in the output folder. This is essential when you need to confirm that predictions are correctly attributed to the specified enzymes and meet the desired level of biochemical filtering.

## When NOT to use

- If you have not yet executed CyProduct and therefore have no output folder to interpret — run the prediction step first.
- If the output folder is empty or corrupted; troubleshoot the CyProduct run before attempting interpretation.
- If you need to filter or modify the enzyme list after prediction; re-run CyProduct with the desired enzyme subset rather than post-hoc filtering.

## Inputs

- Output folder path containing CyProduct predicted metabolite results
- List of CYP450 enzymes used in the prediction run (e.g., 1A2, 2A6, 2B6, 2C8, 2C9, 2C19, 2D6, 2E1, 3A4)
- Query molecule identifier (SMILES string or SDF file path used as input)
- CypReact filter status (boolean flag indicating whether filtering was enabled)

## Outputs

- Validated and organized metabolite predictions per enzyme
- Metabolite-to-enzyme catalysis mappings
- Ranked metabolite list with computed scores
- Verification report of output folder completeness and filter status

## How to apply

Navigate to the output folder path specified during CyProduct execution and retrieve all predicted metabolite files. Verify that the output contains results for each enzyme in the input enzyme list (e.g., 1A2, 2A6, 2B6, 2C8, 2C9, 2C19, 2D6, 2E1, 3A4). Cross-check that metabolites are correctly labeled with their catalyzing enzyme(s) — a metabolite may be catalyzed by one enzyme or multiple enzymes in the list. If the CypReact filter module was enabled (the default state), validate that predicted metabolites pass the biochemical plausibility filter; if useCypReact was set to false, expect unfiltered raw predictions. Compare score calculations using the formula Score = (prob-threshold)/(1-threshold), where threshold = 1/(1+beta), to understand the confidence ranking of predicted metabolites. Organize results by enzyme or by metabolite structure depending on your downstream analysis goal.

## Related tools

- **CyProduct** (Core metabolite prediction engine; produces output folder containing predicted metabolites catalyzed by specified CYP450 enzymes) — https://github.com/Le0nT1/CyProduct
- **BioTransformerAPI** (Embedded API class within CyProduct JAR for programmatic access to metabolite prediction and CypReact filter control) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment for executing CyProduct JAR and interpreting command-line output folder arguments)

## Examples

```
# After running: java -jar CyProduct.jar CC(=O)Nc1ccc(O)cc1 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4 E:\Users\cyproduct\
# Collect and verify predicted metabolites from E:\Users\cyproduct\ output folder, checking that results exist for all 9 CYP450 enzymes and contain metabolite-to-enzyme catalysis mappings.
```

## Evaluation signals

- Output folder exists and contains files for each CYP450 enzyme in the input enzyme list; no missing enzyme predictions.
- Each predicted metabolite record includes a catalyzing enzyme label (or enzyme combination) that matches the input enzyme list.
- Metabolite score values follow the formula Score = (prob-threshold)/(1-threshold) and fall within the valid range [0, 1] or indicate confidence ranking consistency.
- If CypReact filtering was enabled (default), predicted metabolites are biochemically feasible transformations; if disabled (useCypReact=false), raw predictions may include less-common or speculative metabolites.
- Query molecule SMILES or SDF identifier can be traced back to the input and all predictions are associated with that molecule, not cross-contaminated from other runs.

## Limitations

- CypReact filter module status must be known or recorded at prediction time; the output folder alone does not definitively indicate whether filtering was applied unless metadata is preserved.
- Enzyme list must use CYP450 nomenclature without the 'CYP' prefix (e.g., '1A2' not 'CYP1A2'); misnamed enzymes may produce silent failures or unexpected outputs.
- No changelog is available for CyProduct; version history and breaking changes are undocumented, which may affect reproducibility across versions.
- Output folder structure and file naming conventions are not formally specified in the README, so parsing results may require manual inspection of the first run to establish the expected format.
- Score computation relies on beta parameter from the CypBoM cost matrix training process; this parameter is not user-configurable and is fixed within the jar, limiting score customization.

## Evidence

- [other] Collect and verify predicted metabolites from the output folder, with results filtered according to the CypReact module (default enabled unless useCypReact is set to false).: "Collect and verify predicted metabolites from the output folder, with results filtered according to the CypReact module (default enabled unless useCypReact is set to false)."
- [readme] If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them. For example, if the input enzyme list is 1A2,3A4, then metabolites predicted are catalyzed by either 1A2 or 3A4 or both of them.: "If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them. For example, if the input enzyme list is 1A2,3A4, then metabolites predicted are catalyzed by"
- [readme] if the useCypReact is set as false, then the CypReact filter module will be disabled: "if the useCypReact is set as false, then the CypReact filter module will be disabled"
- [readme] The score is computed using formula Score = (prob-threshold)/(1-threshold) where prob is the value predicted for the SoM and threshold = 1/(1+beta).: "The score is computed using formula Score = (prob-threshold)/(1-threshold) where prob is the value predicted for the SoM and threshold = 1/(1+beta)."
- [readme] The OutputFoldPath is the path to the folder where you want to store the predicted results.: "The OutputFoldPath is the path to the folder where you want to store the predicted results."
