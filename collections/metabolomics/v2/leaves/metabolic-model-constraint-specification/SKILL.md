---
name: metabolic-model-constraint-specification
description: Use when you have a generic constraint-based metabolic model (SBML format)
  and cross-sectional omics data (RNA-seq, intracellular metabolomics, YSI or bioanalyzer
  extracellular flux measurements) for multiple biological samples and need to create
  sample-specific models that discriminate whether.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3172
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
  - COBRApy (optGpSampler algorithm)
  - COBRApy (with optGpSampler)
  - Agilent 1290 Infinity UHPLC + Agilent 6550 iFunnel Q-TOF
  - qLSLab/integrate pipeline
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

# metabolic-model-constraint-specification

## Summary

Integrate multi-omics data (transcriptomics, metabolomics, extracellular flux measurements) into constraint-based metabolic models by applying three complementary constraint types—nutrient availability (Type 1), extracellular flux ratios (Type 2), and transcriptomics-derived enzyme capacity (Type 3)—to generate cell-line-specific models that accurately predict metabolic regulation at transcriptional and metabolic levels.

## When to use

Apply this skill when you have a generic constraint-based metabolic model (SBML format) and cross-sectional omics data (RNA-seq, intracellular metabolomics, YSI or bioanalyzer extracellular flux measurements) for multiple biological samples and need to create sample-specific models that discriminate whether differential metabolic fluxes are controlled by gene expression, substrate availability, or both. Use this skill before flux sampling, FVA, or flux prediction tasks.

## When NOT to use

- Input model lacks Gene-Protein-Reaction (GPR) rules: RAS computation and transcriptomics constraint integration will fail or be incomplete.
- Extracellular flux data is missing or incomplete: Type 2 constraints cannot be applied; you can still apply Type 1 and Type 3, but discrimination between metabolic vs. transcriptional control will be limited.
- RNA-seq or metabolomics data are cross-sectional (single time point per sample) but your goal is to model temporal dynamics: this skill generates steady-state snapshot models, not time-series models.

## Inputs

- Generic constraint-based metabolic model (SBML format with GPR rules)
- RNA-seq gene expression data (read counts, FPKM, or normalized format)
- Intracellular metabolomics dataset (concentrations or log-ratios across cell lines)
- Extracellular flux measurements (glucose, lactate, glutamine, glutamate from YSI2950 bioanalyzer or equivalent)
- Growth medium composition (nutrient concentrations per cell line)
- Mapping file between metabolomics metabolite IDs and model metabolite IDs

## Outputs

- Cell-line-specific constraint-based metabolic models (SBML format, one per sample)
- Reaction Activity Score (RAS) table (reactions × samples, normalized 0–1)
- Constrained flux bounds per model (reaction-level upper and lower bounds)
- Feasible Flux Distribution samples (if sampling is performed; CSV with reactions × solutions)

## How to apply

Begin by computing Reaction Activity Scores (RAS) from RNA-seq read counts and Gene-Protein-Reaction (GPR) rules using Boolean logic (minimum for AND-linked genes, sum for OR-linked genes), then normalize RAS by maximum across samples. Apply Type 1 constraints by setting upper bounds on nutrient exchange reactions proportionally to measured concentrations in growth medium for each cell line. Apply Type 2 constraints by constraining extracellular flux ratios (e.g., lactate-to-glucose, lactate-to-glutamine, glutamate-to-glutamine) derived from YSI bioanalyzer measurements, with bounds set to mean ± 1 standard deviation. Apply Type 3 constraints by performing Flux Variability Analysis (FVA) on the generic model, then scaling maximum and minimum flux boundaries for internal reactions proportionally to their normalized RAS values using the scaling equations: v_i^max = (FVA_max_i / FVA_max_ref) × RAS_norm_i and v_i^min = (FVA_min_i / FVA_min_ref) × RAS_norm_i. Apply constraints in combination or independently depending on whether you aim to study transcriptional vs. metabolic regulation. The resulting cell-relative models are then ready for sampling or FVA to generate Feasible Flux Distributions (FFD).

## Related tools

- **COBRApy (with optGpSampler)** (Core library for loading SBML models, applying constraints, performing FVA, and sampling feasible flux regions using the optGpSampler algorithm) — https://github.com/opencobra/cobrapy
- **STAR aligner (v.2.6.1d)** (Aligns raw RNA-seq reads to human reference genome (hg38) to generate read counts for RAS computation) — https://github.com/alexdobin/STAR
- **HTSeq (v.0.6.1)** (Counts aligned reads per gene (using Encode-Gencode GTF v28) to generate gene expression values for RAS calculation) — https://github.com/htseq/htseq
- **YSI2950 bioanalyzer** (Enzymatic measurement of extracellular metabolite concentrations (glucose, lactate, glutamine, glutamate) in spent media, used to derive Type 2 flux ratio constraints)
- **Agilent 1290 Infinity UHPLC + Agilent 6550 iFunnel Q-TOF** (Liquid chromatography and high-resolution mass spectrometry for intracellular metabolomics quantification, providing metabolite concentrations for Type 2 constraint derivation and metabolic regulation concordance analysis)
- **qLSLab/integrate pipeline** (Reference implementation of the full INTEGRATE workflow, including steps for RAS computation (getRASscore.py), constraint integration (rasIntegration.py), and model-relative constraint application) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/rasIntegration.py --imposeYSI Y --imposeMedium Y --imposeRasConstraints Y --rasNormFileName ENGRO2_wNormalizedRAS.csv --ysiFileName ysi_ratio.csv --mediumFileName medium.csv --modelId ENGRO2 --lcellLines MCF102A MDA-MB231 SKBR3 MCF7 MDA-MB361
```

## Evaluation signals

- Cell-line-specific models successfully constrain the feasible flux space: verify by comparing flux variability ranges before and after constraint application; constrained models should show narrower bounds, especially for reactions with differential RAS or measured extracellular flux constraints.
- RAS values are normalized 0–1 per reaction and reflect relative gene expression differences across samples: check that max(RAS_i) = 1 for each reaction i, and that reactions with high expression in a cell line have RAS > 0.5 in that line.
- Type 2 constraint bounds are symmetric around measured extracellular flux ratios with ±1 std dev: verify that lower and upper bounds on lactate-to-glucose and other ratios fall within reported mean ± 1 SD from YSI measurements.
- Sampling of constrained models produces feasible flux distributions with no infeasible solutions: verify that all sampled solutions satisfy all constraints (Type 1, 2, 3) and that biomass ≥ ε (default ε = 1e-4) for viability.
- Cell lines cluster distinctly in t-SNE space of Feasible Flux Distributions when all three constraint types are applied: verify that silhouette score or other clustering quality metric improves monotonically from Type 1 alone → Type 1+2 → Type 1+2+3.

## Limitations

- RAS computation assumes that gene expression (via GPR rules) is the primary driver of enzyme capacity; when post-translational modifications, allosteric regulation, or protein degradation dominate, RAS-based constraints will misrepresent actual flux capacity. Reactions without GPR associations are excluded from RAS-based analysis.
- Type 2 constraints (extracellular flux ratios) rely on steady-state assumption and measured ratios at a single time point (48 h); dynamics or transient metabolic states are not captured. If a single substrate is missing from metabolomics measurements, the corresponding reaction is omitted from Type 2 concordance analysis.
- Type 1 constraints (nutrient availability) assume that measured medium composition and uptake stoichiometry are accurate; if actual nutrient depletion occurs within the 48 h window, constraints based on initial medium will overestimate uptake capacity.
- Integration quality depends on data alignment: mismatched metabolite or gene IDs between RNA-seq, metabolomics, and model will result in missing constraints and incomplete sample-specific models.

## Evidence

- [methods] Compute Reaction Activity Scores (RAS) from RNA-seq read counts using GPR rules (minimum for AND-linked genes, sum for OR-linked genes) and normalize by maximum RAS across cell lines.: "Compute Reaction Activity Scores (RAS) from RNA-seq read counts using GPR rules (minimum for AND-linked genes, sum for OR-linked genes) and normalize by maximum RAS across cell lines."
- [methods] Apply Type 1 constraints: set upper bounds on exchange reactions proportionally to nutrient concentrations in growth medium for each cell line.: "Apply Type 1 constraints: set upper bounds on exchange reactions proportionally to nutrient concentrations in growth medium for each cell line."
- [methods] Apply Type 2 constraints: constrain ratios of lactate-to-glucose, lactate-to-glutamine, and glutamate-to-glutamine fluxes based on YSI measurements with ±1 standard deviation bounds.: "Apply Type 2 constraints: constrain ratios of lactate-to-glucose, lactate-to-glutamine, and glutamate-to-glutamine fluxes based on YSI measurements with ±1 standard deviation bounds."
- [methods] Apply Type 3 constraints: perform Flux Variability Analysis (FVA) on each cell-relative model to determine maximum and minimum flux capacity for each internal reaction, then scale flux boundaries proportionally to RAS values: "Apply Type 3 constraints: perform Flux Variability Analysis (FVA) on each cell-relative model to determine maximum and minimum flux capacity for each internal reaction, then scale flux boundaries"
- [results] This dataset includes a RAS score for each input model reaction and for each sample. The score is based on the expression value (RNA-seq read counts) of the genes encoding for catalyzing enzymes: "This dataset includes a RAS score for each input model reaction and for each sample. The score is based on the expression value (RNA-seq read counts) of the genes encoding for catalyzing enzymes"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [readme] rasIntegration: 'Y' (yes) or 'N' (no) according to whether transcriptomics derived constraints have to be integrated. Default value: 'Y'.: "rasIntegration: 'Y' (yes) or 'N' (no) according to whether transcriptomics derived constraints have to be integrated."
- [readme] imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated. Default value: 'Y'.: "imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated."
- [readme] imposeMedium: 'Y' (yes) or 'N' (no) according to whether nutrients availability constraints have to be integrated. Default value: 'Y'.: "imposeMedium: 'Y' (yes) or 'N' (no) according to whether nutrients availability constraints have to be integrated."
