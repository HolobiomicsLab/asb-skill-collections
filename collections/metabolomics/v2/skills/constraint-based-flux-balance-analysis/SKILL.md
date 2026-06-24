---
name: constraint-based-flux-balance-analysis
description: Use when you have a generic genome-scale metabolic model (SBML format)
  and cross-sectional omics data (RNA-seq, intracellular metabolomics, extracellular
  flux measurements from bioanalyzer or similar) from multiple biological samples
  (cell lines, conditions).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3473
  tools:
  - constraint-based stoichiometric metabolic models
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
  - Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF MS
  - eFlux, TRFBA, GX-FBA, scFBA
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- using constraint-based stoichiometric metabolic models as a scaffold
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36]
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in GX-FBA [26]
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA [38]
- raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)
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

# constraint-based-flux-balance-analysis

## Summary

Apply constraint-based stoichiometric metabolic models to integrate multi-omics data (transcriptomics, metabolomics, extracellular flux measurements) and predict metabolic flux distributions under biological constraints. This skill discriminates whether metabolic differences arise from gene expression regulation, substrate availability regulation, or both.

## When to use

You have a generic genome-scale metabolic model (SBML format) and cross-sectional omics data (RNA-seq, intracellular metabolomics, extracellular flux measurements from bioanalyzer or similar) from multiple biological samples (cell lines, conditions). You need to determine whether observed metabolic differences are controlled at the transcriptional level (enzyme abundance) or metabolic level (substrate/product availability, allosteric effects), or both.

## When NOT to use

- Input metabolic model lacks gene-protein-reaction (GPR) annotations—RAS computation requires GPR rules, and reactions without GPRs cannot be integrated with transcriptomics
- No intracellular metabolomics data are available—Type 3 constraints and metabolic-level regulation cannot be discriminated without metabolite concentrations
- Transcriptomics data are time-series or single-cell rather than cross-sectional steady-state samples—FVA and constraint application assume steady-state metabolic state
- Goal is to predict absolute metabolic fluxes rather than relative regulation—this skill predicts flux differences and regulatory mechanisms, not absolute flux values (which require labeled substrate tracing)

## Inputs

- Generic metabolic model in SBML format (e.g., ENGRO2) with gene-protein-reaction (GPR) associations
- RNA-seq read counts or FPKM values (transcriptomics dataset, cross-sectional)
- Intracellular metabolomics measurements (e.g., from LC-MS/MS)
- Extracellular flux measurements (glucose, lactate, glutamine, glutamate concentrations in spent vs. fresh media, measured by YSI2950 bioanalyzer or equivalent)
- Nutrient concentration data for growth medium for each sample

## Outputs

- Reaction Activity Score (RAS) table: reactions × samples with normalized RAS values
- Sample-specific constrained metabolic models in SBML format (one per cell line/condition and constraint combination)
- Feasible Flux Distribution (FFD) samples: reactions × flux samples for each biological sample
- RAS vs. RPS (Reaction Predicted Score from metabolomics) concordance analysis table with Cohen κ and Pearson r
- Statistical test outputs (Mann-Whitney U test, t-test) comparing flux distributions between sample pairs

## How to apply

First, compute Reaction Activity Scores (RAS) from transcriptomics data using GPR (gene-protein-reaction) rules—apply the minimum function for AND-linked genes and sum for OR-linked genes, then normalize by maximum RAS across samples. Second, apply three tiers of constraints to the metabolic model: (1) Type 1 constraints on exchange reactions proportional to measured nutrient concentrations in each sample's growth medium; (2) Type 2 constraints on extracellular flux ratios (e.g., lactate-to-glucose, lactate-to-glutamine, glutamate-to-glutamine) derived from bioanalyzer measurements with ±1 standard deviation bounds; (3) Type 3 constraints from Flux Variability Analysis (FVA) where flux boundaries are scaled proportionally to RAS values (see Equations 7 and 8 in source). Generate sample-specific models for each biological replicate and constraint combination. Finally, uniformly sample the feasible flux space using optGpSampler (e.g., 1 million samples, thinning=10, batch size 100,000) to obtain Feasible Flux Distributions (FFD) for each sample. The intersection of transcriptomics-driven predictions and metabolomics-driven predictions identifies which reactions are controlled at each regulatory layer.

## Related tools

- **COBRApy** (Python framework for constraint-based modeling, FVA computation, and flux sampling)
- **optGpSampler** (Uniform sampling algorithm for feasible flux distributions from constrained null space)
- **STAR aligner (v.2.6.1d)** (Maps RNA-seq raw reads to reference genome (hg38) for read quantification)
- **HTSeq (v.0.6.1)** (Computes gene-level read counts from aligned RNA-seq BAM files using Gencode GTF)
- **YSI2950 bioanalyzer** (Enzymatic quantification of extracellular metabolites (glucose, lactate, glutamine, glutamate))
- **Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF MS** (LC-MS/MS system for intracellular metabolomics profiling)
- **eFlux, TRFBA, GX-FBA, scFBA** (Related constraint-based methods for integrating gene expression into flux boundaries)

## Examples

```
python pipeline/rasIntegration.py --imposeYSI Y --imposeMedium Y --imposeRasConstraints Y --rasNormFileName ENGRO2_wNormalizedRAS.csv --ysiFileName ysi_ratio.csv --mediumFileName medium.csv --modelId ENGRO2 --lcellLines MCF102A MDAMB231 SKBR3 MCF7 MDAMB361
```

## Evaluation signals

- RAS values across all reactions and samples are bounded in [0, 1] after normalization; verify mean and normalized columns exist in output RAS table
- Sample-specific models each have valid objective function (biomass reaction) and feasible solution space (FVA produces non-empty flux ranges for essential reactions)
- FFD samples show clear cluster separation in t-SNE or PCA when samples have distinct metabolic profiles; compare inter-sample variance to within-sample variance
- Concordance analysis (RAS vs RPS, RAS vs FFD) produces Cohen κ and Pearson r statistics with p-values; reactions with high concordance indicate transcriptional regulation, low concordance indicate metabolic-level regulation
- Extracellular flux ratio constraints are satisfied: simulated lactate-to-glucose, lactate-to-glutamine ratios fall within ±1 SD of measured values for each sample

## Limitations

- Direct determination of metabolic fluxes through labeled substrates is not performed—predictions are relative and mechanistic rather than absolute
- Reactions without GPR associations are excluded from RAS computation and concordance analysis, potentially missing enzymes with unknown genetic basis
- If a single metabolite substrate is missing from metabolomics measurements, the entire reaction is omitted from the dataset, risking loss of regulatory information
- Steady-state assumption may not hold in rapidly dividing or stress-responsive samples; dynamic metabolic states require flux time-series or alternative models
- Uniform sampling of the feasible flux region is computationally expensive (1 million samples per model) and may require high-performance computing infrastructure

## Evidence

- [abstract] constraint-based stoichiometric metabolic models as a scaffold: "using constraint-based stoichiometric metabolic models as a scaffold"
- [results] RAS computation from GPR rules and RNA-seq: "The score is based on the expression value (RNA-seq read counts) of the genes encoding for catalyzing enzymes and"
- [other] Type 1 constraints on exchange reactions: "Apply Type 1 constraints: set upper bounds on exchange reactions proportionally to nutrient concentrations in growth medium for each cell line."
- [other] Type 2 constraints from YSI bioanalyzer: "Apply Type 2 constraints: constrain ratios of lactate-to-glucose, lactate-to-glutamine, and glutamate-to-glutamine fluxes based on YSI measurements with ±1 standard deviation bounds."
- [other] Type 3 constraints from FVA and RAS scaling: "Apply Type 3 constraints: perform Flux Variability Analysis (FVA) on each cell-relative model to determine maximum and minimum flux capacity for each internal reaction, then scale flux boundaries"
- [other] optGpSampler for FFD generation: "Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions (FFD)"
- [abstract] Discriminating regulatory layers via intersection: "We discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting these two outputs"
- [intro] Metabolic fluxes depend on two regulatory layers: "Each metabolic flux depends on at least two intertwined regulatory layers [8–10]"
- [readme] README Step 4: rasIntegration: "rasIntegration: Aim: integrate RAS scores within the input generic models to generate cell relative models"
- [readme] README Step 6: randomSampling with optGpSampler: "randomSampling: Aim: sample the feasible flux region of each cell relative model"
