---
name: genome-scale-metabolic-flux-modeling-workflow
description: 'Use when you have a genome-scale constraint-based metabolic model (GEM,
  SBML/JSON) for one or more organisms and want predicted flux states grounded in
  your own omics data — integrate transcriptomics / metabolomics-derived constraints
  (eFlux-style Reaction Activity/Propensity Scores, extracellular uptake-secretion
  rates) into the model, sample the feasible flux space with optGpSampler, interpret
  and compare the resulting flux distributions across samples or conditions, and,
  when multiple organism or community-member models exist, gap-fill and merge them
  into a consensus community model (COMMIT-style) — connecting metabolomics features
  to predicted flux states.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - metabolic-model-constraint-application
  - constraint-based-flux-balance-analysis
  - reaction-activity-score-computation-from-gpr
  - gene-expression-constraint-integration
  - transcriptomics-reaction-activity-scoring
  - irreversible-model-conversion
  - feasible-flux-distribution-sampling
  - dimensionality-reduction-and-clustering-evaluation
  - flux-distribution-segregation-visualization
  - flux-distribution-interpretation-across-cell-lines
  - flux-variability-analysis-interpretation
  - flux-variability-analysis-for-scaling
  - constraint-based-flux-sampling-and-analysis
  - metabolic-model-merging-consensus-building
  - community-metabolic-reconstruction-synthesis
  - metabolic-model-consensus-integration
  - community-metabolic-pathway-integration
  - systems-biology-model-standardization
  - constraint-based-model-sampling-and-flux-prediction
  - mass-action-law-flux-prediction
  - extracellular-flux-constraint-integration
  member_tools:
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - constraint-based stoichiometric metabolic models
  - optGpSampler
  - COBRApy
  - Flux Variability Analysis (FVA)
  - GLPK solver
  - YSI bioanalyzer (YSI2950)
  - Flux Variability Analysis
  - t-SNE (scikit-learn or standalone)
  - scipy.stats.spearmanr
  - COMMIT
  - COBRApy (optGpSampler algorithm)
  - YSI2950 bioanalyzer
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Genome-Scale Metabolic Model Flux Sampling / Consensus (GEM -> constrained flux states -> community consensus)

## Summary

A GEM plus omics data in, a constrained flux-state report out: eFlux-style constraint integration, optGpSampler flux-space sampling, flux-distribution interpretation, and (for multi-member models) COMMIT consensus community-model integration.


## When to use

Use when you have a genome-scale constraint-based metabolic model (GEM, SBML/JSON) for one or more organisms and want predicted flux states grounded in your own omics data — integrate transcriptomics / metabolomics-derived constraints (eFlux-style Reaction Activity/Propensity Scores, extracellular uptake-secretion rates) into the model, sample the feasible flux space with optGpSampler, interpret and compare the resulting flux distributions across samples or conditions, and, when multiple organism or community-member models exist, gap-fill and merge them into a consensus community model (COMMIT-style) — connecting metabolomics features to predicted flux states.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — constrain

**Goal:** generic GEM + omics data -> sample-constrained metabolic model

**EDAM operation:** operation_3660

**Inputs:** sbml, tsv · **Outputs:** sbml

**Candidate leaf skills:** `metabolic-model-constraint-application` (primary), `constraint-based-flux-balance-analysis`, `reaction-activity-score-computation-from-gpr`, `gene-expression-constraint-integration`, `transcriptomics-reaction-activity-scoring`

**Tools (primary):** eFlux, TRFBA, scFBA, GX-FBA, constraint-based stoichiometric metabolic models, optGpSampler, COBRApy, Flux Variability Analysis (FVA), GLPK solver, YSI bioanalyzer (YSI2950)

**Other candidate tools:** STAR aligner (v.2.6.1d), HTSeq (v.0.6.1), YSI2950 bioanalyzer, Agilent 1290 Infinity UHPLC system, optGpSampler algorithm, t-SNE (t-distributed Stochastic Neighbor Embedding), Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF MS, eFlux, TRFBA, GX-FBA, scFBA, getRASscore (INTEGRATE step 2), getNormalizedRAS (INTEGRATE step 3), rasIntegration (INTEGRATE step 4), rasTtest (INTEGRATE step 8)

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1009337

### Stage 2 — sample_flux

**Goal:** constrained model -> feasible flux distribution samples (optGpSampler)

**EDAM operation:** operation_3927

**Inputs:** sbml · **Outputs:** tsv

**Candidate leaf skills:** `irreversible-model-conversion` (primary), `feasible-flux-distribution-sampling`, `dimensionality-reduction-and-clustering-evaluation`

**Tools (primary):** eFlux, TRFBA, scFBA, GX-FBA, optGpSampler, COBRApy

**Other candidate tools:** STAR aligner (v.2.6.1d), HTSeq (v.0.6.1), YSI2950 bioanalyzer, Agilent 1290 Infinity UHPLC system, optGpSampler algorithm, t-SNE (t-distributed Stochastic Neighbor Embedding), Mann-Whitney U test, GLPK, MATLAB (optional), t-SNE, Flux Variability Analysis (FVA)

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1009337

### Stage 3 — interpret_flux

**Goal:** sampled flux distributions -> normalized, compared flux-distribution report

**EDAM operation:** operation_3436

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `flux-distribution-segregation-visualization` (primary), `flux-distribution-interpretation-across-cell-lines`, `flux-variability-analysis-interpretation`, `flux-variability-analysis-for-scaling`, `constraint-based-flux-sampling-and-analysis`

**Tools (primary):** Flux Variability Analysis, optGpSampler, COBRApy, t-SNE (scikit-learn or standalone), scipy.stats.spearmanr

**Other candidate tools:** constraint-based stoichiometric metabolic models, Flux Variability Analysis (FVA), randomSampling (INTEGRATE pipeline Step 6), getRASscore (INTEGRATE pipeline Step 2), concordanceAnalysis (INTEGRATE pipeline Step 10), createMetabolicDataset (INTEGRATE pipeline Step 9), COBRApy (optGpSampler), randomSampling.py (INTEGRATE pipeline), mannWhitneyUTest.py (INTEGRATE pipeline), eFlux, TRFBA, scFBA, GX-FBA, GLPK (GNU Linear Programming Kit), t-SNE, YSI bioanalyzer (YSI2950)

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1009337

### Stage 4 — community_consensus

**Goal:** draft per-organism/community-member GEMs -> gap-filled consensus community model

**EDAM operation:** operation_3695

**Inputs:** sbml · **Outputs:** sbml

**Candidate leaf skills:** `metabolic-model-merging-consensus-building` (primary), `community-metabolic-reconstruction-synthesis`, `metabolic-model-consensus-integration`, `community-metabolic-pathway-integration`, `systems-biology-model-standardization`

**Tools (primary):** COMMIT


**Grounding:** 2 KB(s); DOIs: 10.1371/journal.pcbi.1009906, 10.5281/zenodo.363932874

### Stage 5 — report

**Goal:** consolidate sampled/interpreted flux states + consensus community model into a flux-state report

**EDAM operation:** operation_3434

**Inputs:** tsv, sbml · **Outputs:** tsv

**Candidate leaf skills:** `constraint-based-model-sampling-and-flux-prediction` (primary), `mass-action-law-flux-prediction`, `extracellular-flux-constraint-integration`

**Tools (primary):** COBRApy (optGpSampler algorithm), Flux Variability Analysis (FVA), constraint-based stoichiometric metabolic models, YSI2950 bioanalyzer

**Other candidate tools:** MassHunter ProFinder, COBRApy (implied by workflow), Flux Variability Analysis, eFlux, TRFBA, scFBA, GX-FBA, optGpSampler, COBRApy, YSI bioanalyzer (YSI2950), Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF MS, t-SNE

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1009337

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
