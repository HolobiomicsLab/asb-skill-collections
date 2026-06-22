---
name: reaction-activity-score-computation-from-gpr
description: Use when you have RNA-seq FPKM abundance data for genes across multiple cell lines or samples, a metabolic model with embedded GPR associations, and need to translate differential gene expression into reaction-level constraints for flux prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_2259
  tools:
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - optGpSampler
  - COBRApy
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
- We used relative gene-expression values as in GX-FBA
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]
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
---

# Reaction Activity Score Computation from Gene-Protein-Reaction Rules

## Summary

Compute Reaction Activity Scores (RAS) that represent differential expression of metabolic enzymes across cell lines by resolving Gene-Protein-Reaction (GPR) logical rules against RNA-seq transcript abundance data. RAS values integrate gene expression via AND (minimum) and OR (sum) operations, then normalize across cell lines to constrain flux boundaries in constraint-based metabolic models.

## When to use

You have RNA-seq FPKM abundance data for genes across multiple cell lines or samples, a metabolic model with embedded GPR associations, and need to translate differential gene expression into reaction-level constraints for flux prediction. Use this skill when transcriptomics alone is insufficient to discriminate metabolic regulation and you must weight metabolic reactions by the coordinated expression of their component enzymes.

## When NOT to use

- Input model lacks GPR annotations or GPR rules are incomplete/invalid — RAS computation requires correctly formatted logical associations between genes and reactions.
- RNA-seq data are already normalized to a reference state (e.g., log-fold changes relative to control) rather than raw or FPKM abundances — RAS requires absolute or relative abundance values, not fold-changes.
- Cell lines or samples are very few (n < 2) — normalization by maximum RAS across cell lines becomes unstable and loses discriminative power.

## Inputs

- SBML metabolic model file with embedded GPR rules (Gene-Protein-Reaction associations)
- RNA-seq FPKM abundance matrix (genes × cell lines/samples)

## Outputs

- CSV file with columns: reaction ID, mean RAS per cell line, normalized RAS per cell line
- Reaction Activity Score matrix (reactions × cell lines, values ∈ [0,1] for GPR-linked, 1.0 for non-GPR)

## How to apply

Load the metabolic model's GPR rules and RNA-seq FPKM abundance data for all genes. For each reaction in each cell line, resolve the GPR logical expression by applying AND logic (take minimum transcript level) to genes encoding subunits and OR logic (sum transcript abundances) to isoforms, following standard precedence rules for mixed expressions. Compute raw RAS for each reaction by evaluating the resolved expression. Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed for that reaction, ensuring RAS values fall in [0,1]. Set RAS = 1.0 for reactions with no associated GPR. Average normalized RAS across biological replicates within each cell line to obtain the final per-reaction, per-cell-line score. Validate by confirming all GPR-associated reactions have RAS ∈ [0,1], all non-GPR reactions equal 1.0, and spot-checking 5–10 reactions by manually resolving their GPR expressions.

## Related tools

- **COBRApy** (Read and manipulate SBML metabolic models, access GPR rules embedded in reaction objects)
- **eFlux** (Reference method for setting flux boundaries as a function of gene expression; RAS normalization is analogous to eFlux's relative expression scaling)
- **TRFBA** (Reference method for transcriptomics-constrained flux balance; RAS enables similar gene-expression-dependent flux constraints)
- **GX-FBA** (Reference method using relative gene-expression values to weight reaction fluxes; RAS follows similar logic for reaction-level aggregation)

## Examples

```
python pipeline/getRASscore.py --gprRule ENGRO2_GPR --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2
```

## Evaluation signals

- All RAS values for GPR-associated reactions fall in [0, 1]; all non-GPR reactions equal 1.0
- Manual verification of 5–10 reactions shows RAS values match expected GPR logic (e.g., AND operations yield minimum gene expression, OR operations yield sums)
- RAS scores show expected cell-line-specific variation (not constant across all cell lines unless gene expression is genuinely constant)
- Normalized RAS values differ from raw RAS by the maximum RAS per reaction, confirming normalization step was applied
- Downstream flux predictions using RAS-constrained bounds show improved concordance with measured metabolic fluxes compared to unconstrained models

## Limitations

- RAS computation assumes GPR rules are correctly formatted and complete; missing or misparsed GPR associations will yield incorrect scores for affected reactions.
- The AND (minimum) and OR (sum) operations are simplifications that do not account for enzyme kinetics, allosteric regulation, post-translational modification, or protein stability — transcript abundance does not necessarily reflect active enzyme levels.
- Reactions without any GPR association are assigned RAS = 1.0 regardless of actual expression, biasing downstream flux predictions if non-GPR reactions are actually regulated.
- Normalization by maximum RAS across cell lines is sensitive to outlier cell lines with extremely high or low expression; if one cell line has unusually high expression, other cell lines' RAS values will be artificially compressed.
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can later be validated using concordance analysis.

## Evidence

- [other] For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript abundances; handle mixed AND/OR using standard precedence rules.: "For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript"
- [other] Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed: RAS^c_r = RAS^c_r,x / max{RAS^c_r} across all c.: "Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed"
- [other] Set RAS to 1 for reactions not associated with any GPR.: "Set RAS to 1 for reactions not associated with any GPR"
- [other] Validation: confirm RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions against manually resolved GPR expressions.: "confirm RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions"
- [other] Load RNA-seq FPKM abundance data for all genes and the ENGRO2 metabolic model with embedded GPR rules (AND/OR logical associations between genes and reactions).: "Load RNA-seq FPKM abundance data for all genes and the ENGRO2 metabolic model with embedded GPR rules"
- [other] For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes (isoforms), RAS equals the sum of transcript values. RAS values are then normalized by dividing each cell line's RAS by the maximum RAS across all cell lines.: "For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes (isoforms), RAS equals the sum of transcript values. RAS values are then normalized by"
- [readme] python pipeline/getRASscore.py: "python pipeline/getRASscore.py"
- [readme] File named modelId + '_RAS.csv' containing a column including the reactions ID (column *Rxn*), and a column for each cell line in the input transcriptomics dataset corresponding to the computer RAS score.: "File named modelId + '_RAS.csv' containing a column including the reactions ID and a column for each cell line"
