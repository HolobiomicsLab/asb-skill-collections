---
name: gene-expression-constraint-integration
description: Use when when you have a generic constraint-based metabolic model, RNA-seq
  or transcriptomics data (FPKM or similar), and you want to reduce the underdetermination
  of metabolic flux predictions by encoding which reactions are expected to be active
  or inactive based on their constituent enzymes'.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2259
  tools:
  - constraint-based stoichiometric metabolic models
  - optGpSampler
  - COBRApy
  - getRASscore (INTEGRATE step 2)
  - getNormalizedRAS (INTEGRATE step 3)
  - rasIntegration (INTEGRATE step 4)
  - rasTtest (INTEGRATE step 8)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- using constraint-based stoichiometric metabolic models as a scaffold
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available
  in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72]
- the implementation of optGpSampler algorithm [71] available in COBRApy [72]
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

# gene-expression-constraint-integration

## Summary

Integrate transcriptomics-derived gene expression constraints into constraint-based metabolic models by computing Reaction Activity Scores (RAS) from GPR rules and normalized expression data, then applying these scores as flux bounds to restrict the feasible solution space and improve model predictions of cell-line-specific metabolism.

## When to use

When you have a generic constraint-based metabolic model, RNA-seq or transcriptomics data (FPKM or similar), and you want to reduce the underdetermination of metabolic flux predictions by encoding which reactions are expected to be active or inactive based on their constituent enzymes' expression levels. This is especially valuable when comparing multiple cell lines or conditions where differential enzyme expression likely drives metabolic reprogramming.

## When NOT to use

- Model lacks GPR annotations or GPR rules are incomplete/inconsistent; RAS computation will fail or produce uninformative bounds.
- Transcriptomics data quality is poor, has extreme outliers, or is from a different growth condition than the metabolic measurements; bounds will be misleading rather than informative.
- The metabolic phenotype is known to be driven primarily by post-translational modifications, allosteric regulation, or cofactor/prosthetic group availability rather than transcriptional control; gene expression constraints alone will miss these regulatory layers.

## Inputs

- Generic constraint-based metabolic model (SBML XML format)
- GPR rules extracted from model (CSV with reaction ID and Boolean expression of gene identifiers)
- Transcriptomics dataset (FPKM or normalized gene expression values, CSV/TSV with genes as rows and samples/cell lines as columns)
- Optional: reference experimental metabolic measurements (growth yield, extracellular flux ratios) for validation

## Outputs

- Reaction Activity Scores (RAS) per reaction per cell line (CSV with reaction ID and RAS values)
- Normalized RAS scores (CSV with mean and normalized RAS per reaction per cell line)
- Cell-line-specific constraint-based models with gene-expression-derived flux bounds (SBML XML per cell line)
- Validation statistics (Spearman correlation coefficients, p-values, Mann–Whitney U test results comparing predicted vs. experimental growth yields)

## How to apply

First, extract Gene-Protein-Reaction (GPR) rules from the metabolic model using regex matching. Second, compute Reaction Activity Scores (RAS) for each reaction by aggregating normalized gene expression values according to the Boolean logic of each GPR rule (e.g., averaging expression of genes connected by OR operators). Third, normalize RAS scores across reactions within each cell line (e.g., by subtracting the mean and dividing by the standard deviation). Fourth, integrate the normalized RAS scores as upper and lower bounds on reaction flux by scaling them relative to the maximum expression level and applying them during constraint-based model construction. Use these transcriptomics-derived constraints in combination with nutrient availability and extracellular flux ratio constraints to generate cell-specific models. Validate the improvement by comparing predictions (e.g., growth yield) against experimental data using correlation and statistical tests (Spearman rank, Mann–Whitney U, or t-test).

## Related tools

- **COBRApy** (Core library for loading SBML models, setting reaction bounds, and running constraint-based simulations and flux sampling) — https://github.com/opencobra/cobrapy
- **optGpSampler** (Generates uniform random samples of steady-state flux distributions from the null space to validate constraint integration)
- **getRASscore (INTEGRATE step 2)** (Computes RAS by parsing GPR rules and aggregating normalized gene expression values per reaction) — https://github.com/qLSLab/integrate
- **getNormalizedRAS (INTEGRATE step 3)** (Normalizes raw RAS scores (e.g., z-score) across reactions within each cell line prior to model integration) — https://github.com/qLSLab/integrate
- **rasIntegration (INTEGRATE step 4)** (Integrates normalized RAS as flux bounds into SBML model to create cell-specific constraint-based models) — https://github.com/qLSLab/integrate
- **rasTtest (INTEGRATE step 8)** (Computes t-test statistics on RAS scores between cell line pairs to identify significantly differentiated reactions) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/getRASscore.py --gprRule ENGRO2_GPR --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2; python pipeline/getNormalizedRAS.py --inputFileName ENGRO2_RAS --outputFileName ENGRO2_wNormalizedRAS; python pipeline/rasIntegration.py --imposeRasConstraints Y --rasNormFileName ENGRO2_wNormalizedRAS.csv --modelId ENGRO2
```

## Evaluation signals

- RAS values range from near 0 to 1 after normalization, with expected bimodal distribution (highly expressed vs. inactive reactions) reflecting known metabolic differences between cell lines.
- Spearman rank correlation between predicted growth yield (from models with gene-expression constraints applied) and experimentally measured growth yield is statistically significant (p < 0.05) and higher than for unconstrained baseline models.
- t-SNE or other dimensionality reduction of sampled flux distributions shows improved separation (decreased intra-cell-line and increased inter-cell-line distance) when gene-expression constraints are applied relative to models with only nutrient availability constraints.
- Reactions with high RAS and high flux in the optimal solution are confirmed to have high gene expression in the input transcriptomics data; conversely, zero-flux reactions have low RAS.
- Integration of gene-expression constraints does not render any cell-line model infeasible (i.e., all models retain at least one feasible solution meeting biomass constraint).

## Limitations

- RAS computation assumes Boolean logic of GPR rules is sufficient; does not account for allosteric regulation, product inhibition, post-translational modifications, or cofactor availability, which can disconnect gene expression from actual enzymatic flux.
- Limited metabolite coverage in metabolomics datasets constrains validation of substrate-availability-driven vs. transcription-driven regulatory distinctions; reactions lacking quantified substrates must be excluded from concordance analysis.
- Uniform sampling of flux space is computationally expensive; for visualization, sampling is typically limited to 10,000 steady-state solutions per model, potentially missing rare phenotypes.
- Gene expression data from bulk transcriptomics reflects cell population averages and cannot capture single-cell heterogeneity or temporal dynamics within the 48-hour growth window.

## Evidence

- [intro] set flux boundaries as a function of gene expression using relative gene-expression values: "we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA [37]. We used relative gene-expression values as in GX-FBA"
- [readme] RAS computation from GPR and transcriptomics: "Aim: generate RAS starting from GPR rules and transcriptomics data. Users may decided to leave the following inputs associated to their default values or set them as preferred: gprRule: output file"
- [readme] normalize RAS scores across reactions and cell lines: "Aim: normalize RAS scores. Output: File named modelId + 'wNormalizedRAS.csv' containing for each reaction (column *Rxn*) the mean (*mean_XXX* column) and normalized (*norm_XXX* column) RAS for each"
- [readme] integrate RAS as flux constraints into SBML models: "Aim: integrate RAS scores within the input generic models to generate cell relative models. Usage: python pipeline/rasIntegration.py. Inputs: imposeRasConstraints: 'Y' (yes) or 'N' (no) according to"
- [other] superior segregation of flux distributions with combined constraints: "Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization"
- [methods] validation via correlation with experimental growth yield: "Compute the Spearman correlation coefficient between experimental and in silico growth yield on glucose for each constraint scenario and report p-values"
- [results] allosteric and post-translational regulation not captured: "The phenomenon according to which gene expression and substrate availability agree with one another, but the flux does not agree with any of the two, might be imputed to model inaccuracy, as well as"
