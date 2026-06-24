---
name: multi-constraint-metabolic-modeling
description: Use when you have metabolic models for multiple biological samples and
  need to distinguish between samples based on their metabolic phenotype, but single
  constraints (e.g., gene expression alone or nutrient availability alone) fail to
  segregate them adequately.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3379
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_0199
  tools:
  - constraint-based stoichiometric metabolic models
  - optGpSampler
  - COBRApy
  - t-SNE (scikit-learn or standalone)
  - Flux Variability Analysis (FVA)
  - GLPK solver
  - qLSLab/integrate (pipeline scripts)
  license_tier: restricted
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

# multi-constraint-metabolic-modeling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply simultaneous nutrient availability, extracellular flux ratio, and transcriptomics-derived constraints to constraint-based metabolic models to segregate cell line phenotypes and characterize multi-level metabolic regulation. This skill integrates three orthogonal regulatory layers—substrate availability, measured metabolic exchange ratios, and gene expression—to achieve superior discrimination of steady-state flux distributions compared to single or paired constraint applications.

## When to use

Apply this skill when you have metabolic models for multiple biological samples and need to distinguish between samples based on their metabolic phenotype, but single constraints (e.g., gene expression alone or nutrient availability alone) fail to segregate them adequately. Use it when you have concurrent measurements of transcriptomics, intracellular metabolomics (for substrate availability inference), and extracellular flux ratios (lactate/glucose, lactate/glutamine, glutamate/glutamine), and you want to validate whether integrating all three constraint types improves model predictions or sample discrimination compared to partial constraint sets.

## When NOT to use

- Input transcriptomics, metabolomics, or extracellular flux measurements are missing or incomplete for multiple cell lines—constraint integration requires all three data types; partial data will undermine the rationale for multi-layer modeling.
- The metabolic model has poor coverage of reactions relevant to the biological question or does not include GPR rules linking genes to reactions; RAS scoring cannot proceed without GPR annotations.
- The research question targets a single well-characterized cell line or condition; multi-constraint segregation is designed to discriminate between multiple samples, not to improve predictions within a single phenotype.
- Enzymatic activity, allosteric regulation, or product inhibition are known to dominate the system; the workflow relies on substrate availability (mass action) and gene expression and cannot capture posttranslational or allosteric control without additional extensions.

## Inputs

- SBML or MAT metabolic model (e.g., ENGRO2)
- Transcriptomics dataset (FPKM or relative gene expression, mapped to GPR rules)
- Extracellular flux ratio measurements (lactate/glucose, lactate/glutamine, glutamate/glutamine; CSV format with ratios and cell line replicates)
- Nutrient availability constraints (CSV with reaction IDs, lower bounds, upper bounds per cell line and replica)
- Intracellular metabolomics dataset (metabolite abundances per cell line, mapped to model metabolite IDs)
- Experimental growth yield data (glucose consumption and biomass accumulation, measured over 48 hours)

## Outputs

- Sampled flux distribution matrices (10,000 solutions per cell line × number of reactions; CSV or HDF5)
- t-SNE-reduced 2D coordinates for all sampled solutions (CSV with cell line labels)
- Visual t-SNE plots showing segregation quality for each constraint scenario (PNG/PDF)
- Spearman correlation coefficients and p-values comparing experimental vs. in silico growth yield for each constraint set (CSV or table)
- Cell-relative constraint-based models (SBML files with integrated constraints)
- Quantitative segregation metrics (e.g., intra-model vs. inter-model Euclidean distance in t-SNE space)

## How to apply

Begin by constructing cell-relative constraint-based models using the ENGRO2 (or comparable) metabolic scaffold. Sequentially apply constraints: (1) Type 1: nutrient availability constraints derived from medium composition and uptake measurements (set reaction lower and upper bounds); (2) Type 2: extracellular flux ratio constraints computed from exo-metabolomics data (lactate/glucose, lactate/glutamine, glutamate/glutamine ratios); (3) Type 3: transcriptomics-derived Reaction Activity Score (RAS) constraints, computed from GPR rules and gene expression, scaled by maximum gene expression per reaction. For each constraint scenario (null, Type 1, Type 1+2, Type 1+2+3), sample 10,000 steady-state flux distributions from the feasible null space using uniform sampling (e.g., optGpSampler). Apply t-SNE dimensionality reduction to the resulting flux distributions and visually compare inter-model separation quality across constraint scenarios. Validate model accuracy by computing Spearman correlation between experimental and in silico growth yield on glucose for each constraint set, reporting p-values. Superior segregation under Type 1+2+3 constraints indicates that metabolic control operates across all three regulatory layers and that integration is necessary.

## Related tools

- **COBRApy** (Core library for constraint-based metabolic modeling, stoichiometric matrix manipulation, and FBA/flux sampling)
- **optGpSampler** (Uniform sampling of steady-state flux distributions from the feasible region of the null space)
- **t-SNE (scikit-learn or standalone)** (Dimensionality reduction of high-dimensional flux distribution matrices to 2D for visualization of cell line segregation)
- **Flux Variability Analysis (FVA)** (Computation of min/max flux bounds for each reaction under given constraints; used to scale fluxes for RAS integration)
- **GLPK solver** (Linear programming solver for FBA and flux sampling operations) — https://www.gnu.org/software/glpk/
- **qLSLab/integrate (pipeline scripts)** (End-to-end implementation of constraint integration, RAS scoring, metabolomic concordance, and flux sampling) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/rasIntegration.py --imposeYSI Y --imposeMedium Y --imposeRasConstraints Y --modelId ENGRO2
```

## Evaluation signals

- t-SNE visualization of Type 1+2+3 constraint scenario shows visibly larger inter-model separation and tighter intra-model clustering than null, Type 1, or Type 1+2 scenarios; quantify by computing mean pairwise Euclidean distances between and within cell line clusters in t-SNE space.
- Spearman correlation between experimental growth yield (glucose) and in silico predictions improves monotonically from null → Type 1 → Type 1+2 → Type 1+2+3 constraint sets, with associated p-values < 0.05 for the full constraint model.
- Sampled flux distributions (10,000 solutions per cell line) show reduced variance and more constrained feasible regions under Type 1+2+3 constraints compared to partial constraint sets, indicating successful integration of regulatory information.
- RAS scores (derived from transcriptomics) show significant differential expression (t-test p < 0.05) between cell line pairs, and constraint-based models integrating RAS reproduce at least 50% of these differences in predicted flux space (concordance analysis).
- Extracellular flux ratio constraints (lactate/glucose, lactate/glutamine, glutamate/glutamine) are satisfied within experimental error bounds (e.g., ±20% of measured values) in sampled flux solutions for all cell lines.

## Limitations

- Enzymatic activity is not explicitly modeled; only substrate availability (via mass action) and gene expression (via RAS) are integrated. Allosteric regulation, product inhibition, and cofactor/prosthetic group availability cannot be discriminated from flux patterns alone without additional kinetic or biochemical data.
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions amenable to concordance analysis; reactions with unmeasured substrates are excluded, potentially missing important regulatory nodes.
- RAS score computation assumes that differential gene expression directly reflects differential reaction activity; this breaks down for highly regulated enzymes with posttranslational modifications or for reactions where substrate availability is the primary control lever.
- The workflow was validated only on immortalized breast cancer cell lines (MCF102A, MDAMB231, SKBR3, MCF7, MDAMB361); generalizability to other tissues, growth conditions, or primary cell types is uncertain.
- t-SNE is a stochastic dimensionality reduction method; visualization results can vary across runs. Reproducibility requires fixing random seeds and validation with complementary methods (e.g., PCA, UMAP) to confirm segregation patterns.

## Evidence

- [other] Does the simultaneous application of all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) segregate the five breast cell lines better than any subset of constraints, as evaluated by t-SNE visualization of feasible flux distributions?: "Does the simultaneous application of all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) segregate the five breast cell lines better than"
- [other] Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization showing decreased intra-model and increased inter-model separation of steady-state solutions.: "Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization"
- [other] Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling (optGpSampler). Apply t-SNE dimensionality reduction to the sampled flux distributions to produce a two-dimensional map and visualize the segregation of the five cell lines.: "Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling (optGpSampler). Apply t-SNE dimensionality reduction to the"
- [abstract] use constraint-based stoichiometric metabolic models as a scaffold for integration of multi-omics data: "using constraint-based stoichiometric metabolic models as a scaffold"
- [intro] We compute differential expression from transcriptomics data and use constraint-based modeling to predict if the differential expression of metabolic enzymes directly originates differences in metabolic fluxes.: "We compute differential expression from transcriptomics data and use constraint-based modeling to predict if the differential expression of metabolic enzymes directly originates differences in"
- [intro] differences in metabolic fluxes are only partially determined by variations in protein/gene expression; metabolic control through substrate availability also contributes significantly: "differences in metabolic fluxes are only partially determined by variations in protein/gene expression. Let us take, for example, a specific, irreversible metabolic reaction"
- [results] For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted: "For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted"
- [readme] imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated. Default value: 'Y'. imposeMedium: 'Y' (yes) or 'N' (no) according to whether nutrients availability constraints have to be integrated. Default value: 'Y'. imposeRasConstraints: 'Y' (yes) or 'N' (no) according to whether transcriptomics derived constraints have to be integrated. Default value: 'Y'.: "imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated. Default value: 'Y'. imposeMedium: 'Y' (yes) or 'N' (no) according to whether"
