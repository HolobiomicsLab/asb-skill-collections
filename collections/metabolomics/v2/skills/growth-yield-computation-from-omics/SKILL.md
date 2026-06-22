---
name: growth-yield-computation-from-omics
description: Use when you have constraint-based metabolic models with integrated transcriptomics (gene expression), intracellular metabolomics (substrate concentrations), and extracellular flux measurements (glucose uptake, lactate production, etc.), and you need to test whether differential expression of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3577
  - http://edamontology.org/topic_3307
  tools:
  - COBRApy (optGpSampler algorithm)
  - COBRApy
  - optGpSampler algorithm (in COBRApy)
  - Flux Variability Analysis (FVA)
  - YSI2950 bioanalyzer
  - Bradford assay
  - qLSLab/integrate pipeline
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions of the ENGRO2 model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate
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

# growth-yield-computation-from-omics

## Summary

Compute in silico growth yield (protein synthesized per glucose consumed) by sampling the feasible flux distribution of constraint-based metabolic models and calculating median flux ratios, then validate against experimental growth yield measured via protein assay and metabolite quantification. This skill bridges transcriptomics, metabolomics, and extracellular flux constraints to discriminate metabolic regulation mechanisms across cell lines.

## When to use

You have constraint-based metabolic models with integrated transcriptomics (gene expression), intracellular metabolomics (substrate concentrations), and extracellular flux measurements (glucose uptake, lactate production, etc.), and you need to test whether differential expression of metabolic enzymes or differences in substrate availability translate into observable differences in growth yield across multiple cell lines or conditions.

## When NOT to use

- Metabolic models lack gene-protein-reaction (GPR) associations, so transcriptomics constraints (Type 3) cannot be integrated.
- Experimental growth yield measurements are missing or incomplete for comparison (e.g., only protein measured without glucose consumption, or measured at time points other than 48 h).
- Cell lines exhibit unstable protein-to-cell-number scaling (i.e., linear correlation does not hold over the 48 h culture period, violating the assumption of constant cell size).
- Constraint-based models are not well-curated or validated for the cell types in question, leading to infeasible or biologically implausible flux distributions.

## Inputs

- Cell-line-specific constraint-based metabolic models (SBML format) with Type 1, Type 2, and Type 3 constraints applied separately and in combination
- Experimental growth yield data table (rows: cell lines; columns: protein produced / glucose consumed over 48 h in grams/hour from Bradford and YSI assay)
- Biomass protein fraction constant (default 0.131972 for human cells)
- Growth yield constraint equation parameters (e.g., 0.001 lower bound, mw_Glc stoichiometric coefficient)

## Outputs

- In silico growth yield table (rows: cell lines; columns: median protein synthesis flux / median glucose uptake flux for each constraint scenario, in grams/hour)
- Spearman rank correlation table (rows: constraint scenarios; columns: ρ, p-value, sample count)
- Correlation plot (matching Fig 3E) with ρ and p-value annotations for all four constraint scenarios

## How to apply

Load cell-line-specific constraint-based metabolic models with Type 1 (nutrient availability), Type 2 (extracellular flux ratios), and/or Type 3 (transcriptomics-derived) constraints applied separately and in combination. Use optGpSampler to uniformly sample the feasible flux region (e.g., 10 batches of 100,000 samples per model per constraint scenario, retaining growth yield constraint Eq. 6: 0.001 · 0.131972 · v_Biomass ≤ v_ExGlc · mw_Glc ≤ 0.001). For each cell line under each scenario, compute the median protein synthesis flux divided by median glucose uptake flux and convert the flux ratio to grams/hour using the biomass protein fraction (0.131972). Load experimental growth yield data (protein produced over 48 h / glucose consumed over 48 h, in grams/hour from Bradford assay and YSI analysis). Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario. Generate correlation plots with annotations to identify which constraint type(s) best separate cell lines and achieve highest overall agreement with experiment.

## Related tools

- **COBRApy** (Constraint-based modeling and FVA to compute flux variability and define flux bounds from constraint integration) — opencobra/cobrapy
- **optGpSampler algorithm (in COBRApy)** (Uniformly sample the feasible flux region to generate population of steady-state solutions per cell line and constraint scenario) — opencobra/cobrapy
- **Flux Variability Analysis (FVA)** (Identify minimum and maximum achievable flux for each reaction under given constraints, supporting constraint integration and sampling validation)
- **YSI2950 bioanalyzer** (Enzymatic quantification of glucose, lactate, glutamine, and glutamate in spent media for experimental growth yield calculation)
- **Bradford assay** (Protein quantification for experimental growth yield determination (protein produced over culture period))
- **qLSLab/integrate pipeline** (Automates constraint integration (Steps 1–4: GPR extraction, RAS computation, normalization, model constraint integration) and statistical analysis (Steps 7–10: Mann-Whitney, t-test, concordance analysis)) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/randomSampling.py 100000 10
```

## Evaluation signals

- In silico and experimental growth yield distributions are positively correlated (Spearman ρ > 0.5, p < 0.05) for at least one constraint scenario, indicating that model constraints capture biologically relevant regulation.
- Type 3 (transcriptomics-derived) constraints alone show better cell-line discrimination (larger separation between median growth yields across five cell lines) than Type 1+2 constraints alone, validating the added value of gene expression data.
- Combining all constraint types (Type 1+2+3) achieves the highest Spearman correlation with experiment, demonstrating synergistic information from transcriptomics, metabolomics, and nutrient availability.
- Median protein synthesis flux and median glucose uptake flux are both positive and finite across all cell lines and scenarios (no infeasible or unbounded solutions).
- Sampled flux distributions from optGpSampler respect all imposed constraint bounds (e.g., growth yield constraint Eq. 6) and converge across batches (no artificial batch-to-batch variance in median flux ratios).

## Limitations

- Direct determination of metabolic fluxes through labeled substrate tracing lags behind omic technologies, so in silico growth yield is an indirect proxy dependent on model accuracy and constraint quality.
- Cell-line-specific models require curated nutrient availability constraints (Type 1) and extracellular flux ratio measurements (Type 2); missing or inaccurate constraints reduce model fidelity.
- If intracellular metabolomics measurements are incomplete (one substrate missing for a reaction), the reaction is omitted from metabolic regulation analysis, potentially losing important flux information.
- RAS (Reaction Activity Score) computation depends on accurate gene-protein-reaction (GPR) associations; reactions without GPR rules are excluded from transcriptomics-constrained analysis.
- The skill assumes linear protein-to-cell-number scaling over the 48 h culture period; cell-line-specific deviations (e.g., asynchronous growth, size variation) will introduce systematic error into experimental growth yield normalization.

## Evidence

- [other] For each of the four constraint scenarios, uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each: "uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario)"
- [other] Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass protein fraction (0.131972).: "Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass"
- [other] Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File).: "Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File)"
- [other] Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario.: "Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario"
- [other] Type 3 constraints alone (Type 3) result in good separation of feasible flux distributions and better discrimination of growth rates across five cell lines, with further improvement when extracellular flux constraints (Type 1+2) are simultaneously applied.: "Transcriptomics-derived constraints alone (Type 3) result in good separation of feasible flux distributions and better discrimination of growth rates across five cell lines, with further improvement"
- [results] Between 0 and 48 hours, the protein content linearly correlates with the number of cells (Fig 2C). Hence, biomass accumulation and cell division are balanced and cell size is constant in this time: "Between 0 and 48 hours, the protein content linearly correlates with the number of cells. Hence, biomass accumulation and cell division are balanced and cell size is constant"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [results] Missing RPSvsRAS values occur when a reaction is not associated with a GPR: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
