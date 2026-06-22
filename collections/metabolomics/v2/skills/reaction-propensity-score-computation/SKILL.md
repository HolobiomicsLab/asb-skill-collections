---
name: reaction-propensity-score-computation
description: Use when you have measured intracellular metabolite abundances (LC-MS or similar) across multiple cell lines or conditions and a stoichiometric metabolic model (with reaction-metabolite associations) to estimate how differences in substrate availability—independent of gene expression—translate into.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
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
  - constraint-based stoichiometric metabolic models (ENGRO2)
  - Mann-Whitney U test (scipy.stats)
  - Agilent 1290 Infinity UHPLC + Agilent 6550 iFunnel Q-TOF MS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36]
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in GX-FBA [26]
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA [38]
- raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)
- gene counts were calculated by HTSeq (v.0.6.1), using the hg38 Encode-Gencode GTF file (v28)
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

# Compute Reaction Propensity Scores (RPS) from intracellular metabolomics using mass action law formulation

## Summary

RPS quantifies the expected relative metabolic flux changes across cell lines based purely on substrate availability using the mass action law: each reaction's propensity is the product of substrate concentrations each raised to their stoichiometric coefficients. This skill predicts metabolic regulation at the substrate-availability level, complementing transcriptomics-based approaches to discriminate whether flux changes originate from gene expression or metabolite availability.

## When to use

Apply this skill when you have measured intracellular metabolite abundances (LC-MS or similar) across multiple cell lines or conditions and a stoichiometric metabolic model (with reaction-metabolite associations) to estimate how differences in substrate availability—independent of gene expression—translate into metabolic flux differences. Use RPS when you need to separate transcriptional from metabolic regulation by intersecting RPS predictions with transcriptomics-derived Reaction Activity Scores (RAS).

## When NOT to use

- Input metabolomics data is missing for >10–20% of substrates per reaction; RPS dataset will be too sparse and filtering thresholds in concordance analysis will exclude most reactions (only ~81 of 2,248 reactions in ENGRO2 had full substrate coverage in the published study).
- Metabolic model lacks stoichiometric coefficients or substrate identifiers are not resolvable to the model; RPS computation will fail or produce misleading results due to incorrect stoichiometry.
- You only have extracellular flux measurements (e.g., glucose uptake, lactate secretion) and no intracellular metabolite abundances; use extracellular constraint-based modeling (Type 2 constraints) instead.

## Inputs

- Intracellular metabolomics abundance data (metabolite concentrations per cell line, measured by LC-MS or equivalent)
- Stoichiometric metabolic network model in SBML format with reaction-metabolite-stoichiometric coefficient associations (e.g., ENGRO2)
- Metabolite identifier mapping table (if metabolomics IDs differ from model metabolite IDs)
- List of cell line or sample identifiers and their biological replicate labels

## Outputs

- CSV table with reactions as rows, cell lines as columns, and normalized RPS values (0–1) as entries
- Metadata on reaction coverage: number of reactions with complete substrate abundance measurements vs. omitted reactions
- Optional: Mann-Whitney U test results on RPS distributions for pairwise cell-line comparisons

## How to apply

For each reaction and each cell line, identify all substrate metabolites and their measured intracellular concentrations from the metabolomics dataset, retrieving stoichiometric coefficients from the metabolic model's stoichiometry matrix. Compute RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate q concentration and s_r,q is the stoichiometric coefficient; omit reactions if any substrate is unmeasured. Aggregate RPS values across biological replicates within each cell line using median or mean as appropriate. Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction, producing a normalized RPS matrix with reactions as rows and cell lines as columns. The workflow uses constraint-based stoichiometric metabolic models (e.g., ENGRO2) as the scaffold for stoichiometry lookup and optionally integrates with Mann-Whitney U testing on RPS distributions to identify directional changes in pairwise cell-line comparisons.

## Related tools

- **COBRApy** (Load and query stoichiometric metabolic models; retrieve reaction-metabolite associations and stoichiometric coefficients) — https://github.com/opencobra/cobrapy
- **constraint-based stoichiometric metabolic models (ENGRO2)** (Provide reaction-metabolite-stoichiometric coefficient associations to compute RPS) — https://github.com/qLSLab/integrate
- **Mann-Whitney U test (scipy.stats)** (Test for directional changes in RPS between pairwise cell-line comparisons)
- **Agilent 1290 Infinity UHPLC + Agilent 6550 iFunnel Q-TOF MS** (Instrument platform for measuring intracellular metabolite abundances (LC-MS))

## Evaluation signals

- RPS values are bounded [0, 1] after normalization by maximum RPS per reaction; values outside this range indicate computation error.
- Reactions with all substrates measured in the metabolomics dataset produce non-zero RPS scores; reactions with any missing substrate are completely filtered out (row absent from output table).
- RPS scores increase monotonically with substrate concentrations (when stoichiometric coefficients are positive); a reaction's RPS is highest in the cell line(s) with the highest substrate concentrations.
- The number of output reactions matches the count of reactions with complete substrate coverage in the input metabolomics data (e.g., 81 of 2,248 reactions in ENGRO2 when applied to the published breast cancer dataset).
- Cohen's kappa concordance between RPS directional changes and Feasible Flux Distribution (FFD) directional changes exceeds random agreement (empirical p < 0.05 when tested against shuffled RPS permutations).

## Limitations

- RPS is only computable for reactions whose substrates are all measured in the metabolomics dataset; reactions with even one unmeasured substrate are omitted, leading to sparse coverage (e.g., only 81/2,248 reactions in ENGRO2 had full substrate coverage in the published study).
- RPS assumes the mass action law is a valid approximation of enzymatic kinetics and does not account for allosteric regulation, enzyme kinetic parameters (Km, Vmax), or cofactor availability; it predicts flux propensity under substrate availability alone.
- RPS is normalized within each reaction across cell lines, which obscures absolute flux magnitudes; comparison of RPS scores across different reactions is not meaningful without additional context.
- RPS does not incorporate thermodynamic constraints (Gibbs free energy, reaction reversibility) or enzyme abundance (protein levels); high RPS does not guarantee the reaction is thermodynamically favorable or kinetically active in vivo.
- Metabolomics measurement error, batch effects, and cross-sample normalization artifacts propagate directly into RPS scores; quality control and reproducibility of metabolomics data is critical.

## Evidence

- [other] RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate concentration and s_r,q is the stoichiometric coefficient: "the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is"
- [other] If any substrate is unmeasured, the reaction is omitted from the RPS dataset: "If any substrate is unmeasured, the reaction is omitted from the RPS dataset"
- [other] For each reaction and each cell line, identify all substrate metabolites and retrieve their measured intracellular concentrations; omit reactions missing one or more substrate abundance measurements: "For each metabolic reaction and each cell line, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one"
- [other] Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction: "Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction"
- [other] Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction: "Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [results] When a single reaction substrate is missing from metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [other] Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values: "Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values"
