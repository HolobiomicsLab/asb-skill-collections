---
name: gene-protein-reaction-association-evaluation
description: Use when you have a constraint-based metabolic model with embedded GPR rules (AND/OR associations between genes and reactions), paired with quantified gene-expression data (RNA-seq FPKM or read counts per cell line).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0218
  tools:
  - getGPRsFromModel.py
  - getRASscore.py
  - getNormalizedRAS.py
  - constraint-based stoichiometric metabolic models (SBML format, COBRApy library)
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Gene-Protein-Reaction Association Evaluation

## Summary

Systematically extract and validate Gene-Protein-Reaction (GPR) rules from a metabolic model, then use those rules to compute Reaction Activity Scores (RAS) by integrating transcriptomics data via logical AND/OR resolution. This skill bridges gene-expression levels to reaction-level constraints, enabling discrimination of transcriptionally controlled metabolic reactions.

## When to use

You have a constraint-based metabolic model with embedded GPR rules (AND/OR associations between genes and reactions), paired with quantified gene-expression data (RNA-seq FPKM or read counts per cell line). Apply this skill when you need to assess whether differential metabolic reaction activity is driven by transcriptional regulation (enzyme expression) rather than substrate availability or other post-translational mechanisms.

## When NOT to use

- The metabolic model lacks GPR associations or contains only a small fraction of reactions with GPR rules; you cannot reliably link gene expression to reaction activity without this mapping.
- Gene-expression data are not quantitative (e.g., only fold-change signs, not absolute or normalized abundances); RAS requires numeric transcript levels to resolve AND/OR logic meaningfully.
- You have only proteomics data, not transcriptomics; RAS is designed for RNA-seq or transcript abundance, and protein abundance may not correlate with mRNA.
- Your goal is to predict metabolic flux directly; RAS predicts enzyme-level expression constraints, not steady-state flux distributions, which require additional constraint-based modeling steps.

## Inputs

- SBML or JSON metabolic model file with embedded GPR rules
- RNA-seq expression dataset (FPKM or normalized read counts) with rows as genes, columns as cell lines or samples
- List of biological replicate identifiers for averaging

## Outputs

- GPR rule extraction table (reaction ID, GPR rule as string)
- Raw RAS matrix (reactions × cell lines, pre-normalization values)
- Normalized RAS matrix (reactions × cell lines, values in [0, 1] for GPR-associated reactions and 1.0 for non-GPR reactions)
- Validation report confirming RAS range constraints and spot-checked GPR resolution accuracy

## How to apply

First, extract all GPR rules from the metabolic model (Step 1 in the pipeline). For each reaction in each cell line, resolve the logical GPR expression: treat AND-linked genes (representing subunit requirements) as the minimum transcript abundance; treat OR-linked genes (isoforms or alternatives) as the sum of transcript abundances, applying standard AND/OR precedence. Compute raw RAS as the resolved transcript value, then normalize by dividing each cell line's RAS by the maximum RAS observed across all cell lines, ensuring all GPR-associated reactions fall in [0, 1]; assign RAS = 1.0 to reactions lacking GPR associations. Average normalized RAS across biological replicates to obtain the final RAS per reaction per cell line. Validate by spot-checking 5–10 reactions: manually resolve their GPR expressions against the normalized RAS output to confirm correct AND/OR logic application and that RAS values match expected ranges.

## Related tools

- **getGPRsFromModel.py** (Extracts GPR rules from input metabolic model and outputs a CSV table of reaction–rule pairs) — https://github.com/qLSLab/integrate
- **getRASscore.py** (Computes raw RAS by resolving GPR logical expressions against transcriptomics data using AND (minimum) and OR (sum) operators) — https://github.com/qLSLab/integrate
- **getNormalizedRAS.py** (Normalizes RAS values per reaction by dividing by maximum RAS across all cell lines, producing [0, 1] bounded scores and assigning RAS = 1 to non-GPR reactions) — https://github.com/qLSLab/integrate
- **constraint-based stoichiometric metabolic models (SBML format, COBRApy library)** (Data structure and computational framework for storing reactions, metabolites, GPR rules, and constraints)

## Examples

```
python pipeline/getGPRsFromModel.py && python pipeline/getRASscore.py --gprRule ENGRO2_GPR --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2 && python pipeline/getNormalizedRAS.py --inputFileName ENGRO2_RAS --outputFileName ENGRO2_wNormalizedRAS
```

## Evaluation signals

- All GPR-associated reactions in the normalized RAS matrix have values in the range [0, 1]; all non-GPR reactions have RAS = 1.0 exactly.
- Spot-check validation: manually resolve the GPR expression for 5–10 randomly selected reactions (using AND = min, OR = sum precedence) and confirm the computed RAS matches the output matrix within expected numerical precision.
- RAS values show expected biological patterns: reactions whose genes are highly expressed in a given cell line have higher RAS in that cell line; reactions with no gene expression in a cell line have RAS near 0.
- Replication consistency: RAS values averaged across biological replicates show lower variance than raw values; replicate-specific RAS values cluster tightly before averaging.
- No NaN or infinity values in the normalized RAS matrix; all cells are numeric and bounded.

## Limitations

- GPR resolution assumes AND represents strict subunit requirements and OR represents true isoform substitutability; if the model contains complex regulatory logic (e.g., feedback-mediated gene switching), standard AND/OR resolution may not capture the mechanistic truth.
- RAS does not account for post-translational regulation (phosphorylation, allosteric regulation, protein degradation, compartmentalization) that may alter enzyme activity independent of transcript level; it predicts potential enzyme availability only.
- Missing gene-expression measurements in the transcriptomics dataset may cause reactions to be excluded from RAS calculation if their GPR genes are not quantified; coverage depends on the RNA-seq annotation.
- Normalization by maximum RAS across cell lines makes RAS values relative rather than absolute; comparisons across studies or models using different normalization references may not be directly comparable.
- Reactions with complex OR logic (many isoforms) may have inflated RAS if transcript abundances are summed without saturation constraints; the summing assumption may overestimate total enzyme capacity.

## Evidence

- [other] For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript abundances; handle mixed AND/OR using standard precedence rules.: "For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript"
- [other] Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed: RAS^c_r = RAS^c_r,x / max{RAS^c_r} across all c. Set RAS to 1 for reactions not associated with any GPR.: "Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed: RAS^c_r = RAS^c_r,x / max{RAS^c_r} across all c. Set RAS to 1 for reactions not associated with any"
- [other] Validation: confirm RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions against manually resolved GPR expressions.: "Validation: confirm RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions"
- [other] RAS computation integrates Gene-Protein-Reaction rules with RNA-seq read counts. For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes (isoforms), RAS equals the sum of transcript values. RAS values are then normalized by dividing each cell line's RAS by the maximum RAS across all cell lines.: "RAS computation integrates Gene-Protein-Reaction rules with RNA-seq read counts. For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes"
- [readme] Step 1: getGPRsFromModel. Aim: Takes input model and returns the GPR rules associated to each reaction.: "Step 1: getGPRsFromModel. Aim: Takes input model and returns the GPR rules associated to each reaction."
- [readme] Step 2: getRASscore. Aim: generate RAS starting from GPR rules and transcriptomics data.: "Step 2: getRASscore. Aim: generate RAS starting from GPR rules and transcriptomics data."
- [readme] Step 3: getNormalizedRAS. Aim: normalize RAS scores.: "Step 3: getNormalizedRAS. Aim: normalize RAS scores."
