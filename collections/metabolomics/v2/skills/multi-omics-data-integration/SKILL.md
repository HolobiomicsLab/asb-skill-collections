---
name: multi-omics-data-integration
description: Use when when you have matched transcriptomics (RNA-seq read counts),
  intracellular metabolomics (LC-MS abundance data), and extracellular flux measurements
  (YSI bioanalyzer or similar) from multiple biological samples or cell lines, and
  you need to determine whether differences in metabolic enzyme.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - eFlux
  - TRFBA
  - GX-FBA
  - scFBA
  - STAR aligner (v.2.6.1d)
  - HTSeq (v.0.6.1)
  - YSI2950 bioanalyzer
  - Agilent 1290 Infinity UHPLC system
  - optGpSampler algorithm
  - t-SNE (t-distributed Stochastic Neighbor Embedding)
  - COBRApy
  - optGpSampler
  - Mann-Whitney U test
  - Agilent 1290 Infinity UHPLC + Agilent 6550 iFunnel Q-TOF mass spectrometer
  - Cohen's kappa metric
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36]
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in GX-FBA [26]
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA [38]
- raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)
- gene counts were calculated by HTSeq (v.0.6.1), using the hg38 Encode-Gencode GTF
  file (v28)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multi-omics data integration using constraint-based metabolic modeling

## Summary

A computational pipeline that integrates transcriptomics, intracellular metabolomics, and extracellular flux measurements with constraint-based stoichiometric metabolic models to discriminate whether metabolic flux differences are regulated at the transcriptional (gene expression) or metabolic (substrate availability) level.

## When to use

When you have matched transcriptomics (RNA-seq read counts), intracellular metabolomics (LC-MS abundance data), and extracellular flux measurements (YSI bioanalyzer or similar) from multiple biological samples or cell lines, and you need to determine whether differences in metabolic enzyme expression translate to flux changes, or whether substrate availability alone explains flux variation—particularly useful in cancer metabolism or metabolic engineering contexts.

## When NOT to use

- Input metabolomics data lacks substrate abundances for one or more reactions of interest (reactions missing any substrate measurement are filtered out and excluded from concordance analysis)
- Metabolic model lacks Gene-Protein-Reaction associations or GPR rules are incomplete (RAS computation requires valid GPR logic; reactions without GPR associations cannot be scored)
- Extracellular flux measurements are not available or not in steady-state (Type 2 constraints cannot be applied; the method discriminates transcriptional from metabolic control partly via flux ratio constraints)

## Inputs

- Genome-scale metabolic model (SBML format with GPR rules)
- RNA-seq read count matrix (gene × sample)
- Intracellular metabolomics abundance data (metabolite × sample, LC-MS quantified)
- Extracellular flux measurements (glucose, lactate, glutamine, glutamate consumed/produced; YSI2950 bioanalyzer output)
- Medium composition (nutrient concentrations for each cell line/condition)

## Outputs

- Reaction Activity Score (RAS) matrix (reaction × sample, normalized by maximum RAS per reaction)
- Reaction Propensity Score (RPS) matrix (reaction × sample, computed from metabolomics via mass-action law)
- Sample-specific constrained metabolic models (SBML, one per cell line/condition)
- Feasible Flux Distribution (FFD) samples (reaction × solution, ~1 million per sample)
- Cohen's kappa concordance table (RAS vs RPS, RAS vs FFD, RPS vs FFD directional agreement)
- Mann-Whitney U test results with directional change calls (up/down/no-change per pairwise comparison)
- t-SNE visualization of FFD clusters (2D embedding coloring by sample)

## How to apply

Load a genome-scale metabolic model (SBML format) with Gene-Protein-Reaction associations. Compute Reaction Activity Scores (RAS) from RNA-seq counts using GPR rules (minimum for AND-linked genes, sum for OR-linked). In parallel, compute Reaction Propensity Scores (RPS) from intracellular metabolomics data by raising substrate concentrations to their stoichiometric coefficients per mass-action kinetics. Apply three classes of constraints to the model: Type 1 (nutrient availability from measured medium composition), Type 2 (extracellular flux ratios from YSI measurements with ±1 SD bounds), and Type 3 (transcriptomics-scaled flux bounds derived from Flux Variability Analysis). Sample the constrained null space of each sample-specific model using uniform sampling (optGpSampler with ~1 million samples, thinning=10) to generate Feasible Flux Distributions. Finally, perform Mann-Whitney U testing (p < 0.05) on RAS and RPS distributions across pairwise sample comparisons and compute Cohen's kappa concordance between directional changes (up/down/no-change) to identify reactions controlled by transcription, metabolism, or both.

## Related tools

- **COBRApy** (Python constraint-based modeling package for loading SBML models, defining constraints, and interfacing with LP solvers) — opencobra/cobrapy
- **optGpSampler** (Uniform sampling algorithm for the null space of constrained stoichiometric models to generate Feasible Flux Distributions)
- **STAR aligner (v.2.6.1d)** (RNA-seq read alignment to reference genome (hg38) for computing gene expression levels used in RAS calculation)
- **HTSeq (v.0.6.1)** (Gene quantification from aligned RNA-seq reads to produce read count matrix)
- **YSI2950 bioanalyzer** (Enzymatic quantification of extracellular glucose, lactate, glutamine, glutamate for Type 2 (flux ratio) constraints)
- **Agilent 1290 Infinity UHPLC + Agilent 6550 iFunnel Q-TOF mass spectrometer** (LC-MS/MS analysis for intracellular metabolomics quantification (substrate abundances for RPS scoring))
- **t-SNE (t-distributed Stochastic Neighbor Embedding)** (Dimensionality reduction and visualization of Feasible Flux Distributions across samples)
- **Mann-Whitney U test** (Non-parametric statistical test to determine directional changes (up/down/no-change) in RAS and RPS distributions across pairwise sample comparisons)
- **Cohen's kappa metric** (Quantification of concordance (agreement beyond chance) between RAS directional changes and RPS directional changes across reaction pairs)

## Examples

```
python pipeline/rasIntegration.py --imposeRasConstraints Y --imposeMedium Y --imposeYSI Y --rasNormFileName ENGRO2_wNormalizedRAS.csv --ysiFileName ysi_ratio.csv --mediumFileName medium.csv --modelId ENGRO2 --lcellLines MCF102A MDAMB231 SKBR3 MCF7 MDAMB361
```

## Evaluation signals

- RAS values are bounded [0, 1] after normalization by maximum RAS per reaction and span the full range across cell lines (indicating transcriptional variation is captured)
- RPS values are positive and proportional to substrate concentrations raised to stoichiometric coefficients; reactions with zero substrate abundance have RPS = 0
- FFD samples from optGpSampler respect all three constraint classes: exchange reaction bounds match medium composition, flux ratios (lactate/glucose, lactate/glutamine, glutamate/glutamine) fall within ±1 SD of YSI measurements, and internal reaction bounds scale with RAS scores
- Cohen's kappa values for reactions with full metabolomics coverage range from −1 to +1, with empirical probability of RAS–RPS agreement exceeding that of two independent random distributions (Monte Carlo validation)
- t-SNE visualization of FFD shows clear cluster separation between cell lines when all three constraint types are applied (Type 1+2+3), with degraded separation when constraints are omitted or type-wise; inter-model separation improves when Type 2 constraints are included

## Limitations

- Direct metabolic flux determination via labeled substrates is not performed; the pipeline infers fluxes from omics data and medium composition, introducing uncertainty when multiple flux patterns fit the constraints equally well
- Reactions are excluded from concordance analysis if any substrate is missing from the metabolomics dataset; coverage is limited to 81 of potentially hundreds of metabolic reactions in genome-scale models
- The mass-action kinetic assumption (RPS = ∏ substrate_conc^stoichiometry) ignores allosteric regulation, enzyme kinetic parameters (Km, Vmax), and cofactor effects, leading to incomplete prediction of metabolic flux control
- The method assumes steady-state and balanced cell growth; transient or oscillatory dynamics are not captured
- GPR rule parsing requires standardized gene naming conventions; reactions with missing or malformed GPR associations cannot receive RAS scores and are excluded from analysis

## Evidence

- [abstract] pipeline that integrates metabolomics and transcriptomics data: "We propose a computational pipeline to characterize the landscape of metabolic regulation in different biological samples. The method integrates intracellular and extracellular metabolomics, and"
- [abstract] discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting output datasets: "We discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting these two outputs"
- [results] Reaction Activity Scores (RAS) computed from RNA-seq counts and GPR rules: "Compute Reaction Activity Scores (RAS) from RNA-seq read counts using GPR rules (minimum for AND-linked genes, sum for OR-linked genes)"
- [methods] RPS computed from substrate concentrations via mass-action law: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [results] Three constraint types: nutrient availability, extracellular flux ratios, and transcriptomics-scaled bounds: "Integration of transcriptomics, metabolomics, and extracellular flux data into metabolic model"
- [methods] Feasible Flux Distributions sampled with optGpSampler: "Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions"
- [results] Cohen's kappa concordance analysis of RAS vs RPS directional changes: "For each reaction and each pairwise comparison, compute the Cohen's kappa coefficient quantifying agreement between RAS variation sign and RPS variation sign"
- [results] Reactions excluded if any substrate missing from metabolomics: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [readme] Pipeline steps from README Step 2–10 orchestration: "INTEGRATE takes as input 1) a generic metabolic network model, including GPRs 2) cross-sectional transcriptomics data 3) cross-sectional intracellular metabolomics data 4) steady-state extracellular"
- [methods] Mann-Whitney U testing for directional RAS/RPS changes: "For each of the 10 pairwise cell-line comparisons, perform Mann-Whitney U testing (p < 0.05) on RAS and RPS distributions to determine the sign of directional change (up, down, or no-change)"
