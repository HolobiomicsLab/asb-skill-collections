---
name: ras-dependent-flux-boundary-setting
description: Use when when you have a generic constraint-based metabolic model, cell-line-specific
  or sample-specific transcriptomics data (e.g., FPKM or RNA-seq), and need to generate
  cell-relative metabolic models that account for differential gene expression.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2259
  tools:
  - Flux Variability Analysis
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - optGpSampler
  - COBRApy
  - Flux Variability Analysis (FVA)
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36] and TRFBA
- We used relative gene-expression values as in GX-FBA
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available
  in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72]
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# RAS-dependent flux boundary setting

## Summary

Set flux boundaries for metabolic reactions proportionally to Reaction Activity Scores (RAS) derived from gene expression, enabling cell-line-specific constraint-based models. This integrates transcriptomic regulation into stoichiometric metabolic models by scaling FVA-determined bounds by normalized RAS values.

## When to use

When you have a generic constraint-based metabolic model, cell-line-specific or sample-specific transcriptomics data (e.g., FPKM or RNA-seq), and need to generate cell-relative metabolic models that account for differential gene expression. Apply this skill when you want to predict how gene expression differences translate into metabolic flux differences within a population of related cell lines or samples.

## When NOT to use

- Input model lacks GPR annotations or gene associations; RAS computation will fail or be uninformative.
- Transcriptomics data is not available or does not align temporally/developmentally with metabolic state being modeled.
- Metabolic reactions are purely enzymatic but have no transcriptomic proxy (e.g., spontaneous reactions, transport); scaling by gene expression is not justified.

## Inputs

- Generic SBML metabolic model (e.g., ENGRO2) with GPR associations
- Cell-line or sample-specific transcriptomics data (FPKM, RNA-seq, or normalized expression values as TSV/CSV)
- FVA-derived minimum and maximum flux bounds per reaction
- Gene expression mapping table (if gene IDs in transcriptomics differ from model GPR notation)

## Outputs

- Cell-line-specific SBML metabolic model(s) with RAS-dependent flux bounds integrated
- RAS score table (CSV) with reactions as rows and normalized RAS per cell line as columns
- Bounded metabolic models ready for sampling, FBA, or flux prediction analysis

## How to apply

First, compute Reaction Activity Scores (RAS) by resolving GPR (Gene-Protein-Reaction) logical expressions from the metabolic model: for AND operators, take the minimum of subunit gene expression values; for OR operators, sum isoform values. Normalize RAS by dividing each reaction's RAS by the maximum RAS value across all samples. Then perform Flux Variability Analysis (FVA) on a generic model to obtain baseline minimum and maximum flux bounds (v_L and v_U) for each internal reaction. For each reaction r in each cell c, apply RAS-scaled bounds: lower bound = RAS_r^c × v_L,r^c and upper bound = RAS_r^c × v_U,r^c. Reactions without GPR rules retain symmetric FVA bounds. Ensure all three constraint types (nutrient availability, extracellular flux ratios, and transcriptomics-derived flux boundaries) are applied together to the resulting cell-relative models before downstream sampling or flux analysis.

## Related tools

- **COBRApy** (Python framework for constructing, analyzing, and manipulating metabolic models; used to load SBML models, resolve GPR rules, and apply flux bounds) — https://github.com/opencobra/cobrapy
- **Flux Variability Analysis (FVA)** (Determines the maximum and minimum achievable flux through each reaction under baseline constraints; FVA bounds serve as the input for RAS scaling)
- **optGpSampler** (Uniformly samples the constrained null space of stoichiometric matrices; applied downstream after RAS-dependent bounds are set to generate feasible flux distributions)

## Examples

```
python pipeline/getRASscore.py --gprRule ENGRO2_GPR.csv --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2
```

## Evaluation signals

- RAS values are computed correctly: verify AND operator (minimum gene expression) and OR operator (sum of isoforms) logic is applied as specified; RAS range after normalization should be 0 ≤ RAS ≤ 1 per reaction and cell line.
- Scaled flux bounds are mathematically consistent: lower_bound ≤ upper_bound for all reactions after scaling; bounds should tighten (shrink) relative to FVA baseline when normalized RAS < 1, and remain unchanged when RAS = 1.
- Cell-line-specific models produce differential flux distributions: when sampled (e.g., optGpSampler), models with different RAS profiles should exhibit statistically different flux ranges for genes with differential expression (e.g., Mann-Whitney U test p < 0.05 between pairs of cell lines).
- GPR resolution and gene mapping are faithful: spot-check a subset of reactions with known multi-gene catalysis (isoforms, subunits) to confirm AND/OR operators are applied correctly and gene expression values are correctly mapped.
- Compatibility with downstream constraints: integrate RAS-dependent bounds with nutrient availability and extracellular flux ratio constraints; verify that the resulting bounded models are non-empty (feasible region exists) via a test FBA solve.

## Limitations

- RAS computation assumes GPR logic can be faithfully represented by minimum (AND) and sum (OR) operators; complex allosteric, cofactor-dependent, or post-translational regulation is not captured.
- Gene expression is treated as a proxy for enzyme abundance and activity; protein-level measurements (e.g., proteomics) are not integrated, and translationally/post-translationally regulated reactions may not be accurately reflected.
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can be validated or further constrained after RAS-dependent bounds are set.
- The method scales bounds proportionally to RAS without accounting for saturation kinetics or enzyme-level cooperativity; linear scaling may overestimate or underestimate flux capacity in some reactions.
- Reactions without GPR annotations retain symmetric FVA bounds and do not benefit from transcriptomics integration; such reactions may act as bottlenecks in the model if they are not otherwise constrained.

## Evidence

- [other] For each reaction r in cell c, the lower and upper flux bounds are constrained as: RAS_r^c × v_L,r^c ≤ v_r^c ≤ RAS_r^c × v_U,r^c, where v_L,r^c and v_U,r^c are cell-specific FVA-determined bounds.: "For each reaction r in cell c, the lower and upper flux bounds are constrained as: RAS_r^c × v_L,r^c ≤ v_r^c ≤ RAS_r^c × v_U,r^c, where v_L,r^c and v_U,r^c are cell-specific FVA-determined bounds."
- [other] Compute Reaction Activity Scores (RAS) for each cell line by resolving GPR logical expressions—taking the minimum of subunit gene expression values (AND operator) and summing isoform values (OR operator)—then normalize RAS by dividing by the maximum RAS value across all cell lines.: "Compute Reaction Activity Scores (RAS) for each cell line by resolving GPR logical expressions—taking the minimum of subunit gene expression values (AND operator) and summing isoform values (OR"
- [other] Perform Flux Variability Analysis (FVA) on ENGRO2 with type 1 and type 2 constraints (nutrient availability and extracellular flux ratios) to determine the maximum and minimum flux through each internal reaction for each cell line.: "Perform Flux Variability Analysis (FVA) on ENGRO2 with type 1 and type 2 constraints (nutrient availability and extracellular flux ratios) to determine the maximum and minimum flux through each"
- [other] Set RAS-dependent flux boundaries for each reaction in each cell line as: lower bound = RAS × FVA_min, upper bound = RAS × FVA_max, ensuring reactions without GPRs use symmetric FVA bounds.: "Set RAS-dependent flux boundaries for each reaction in each cell line as: lower bound = RAS × FVA_min, upper bound = RAS × FVA_max, ensuring reactions without GPRs use symmetric FVA bounds."
- [readme] Aim: generate RAS starting from GPR rules and transcriptomics data. Usage: `python pipeline/getRASscore.py`. Inputs: Users may decided to leave the following inputs associated to their default values or set them as preferred: gprRule: output file of Step 1, rnaSeqFileName = transcriptomics dataset file name, modelId: the input model name.: "Aim: generate RAS starting from GPR rules and transcriptomics data. Usage: `python pipeline/getRASscore.py`. Inputs: gprRule: output file of Step 1, rnaSeqFileName = transcriptomics dataset file"
