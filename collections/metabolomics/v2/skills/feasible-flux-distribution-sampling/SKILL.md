---
name: feasible-flux-distribution-sampling
description: 'Use when after integrating transcriptomics-derived (RAS), metabolomics-derived
  (RPS), and extracellular flux constraints into cell-relative metabolic models, sample
  the feasible flux region when you need to: (1) visualize and compare the metabolic
  phenotype distributions across biological samples.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3577
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
  - GLPK
  - MATLAB (optional)
  license_tier: restricted
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

# feasible-flux-distribution-sampling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Uniformly sample the constrained null space of a cell-relative metabolic model to generate a Feasible Flux Distribution (FFD) that characterizes the landscape of metabolic fluxes compatible with transcriptomics, metabolomics, and extracellular flux constraints. This captures the solution space uncertainty inherent in constraint-based modeling when multiple flux solutions satisfy all integrated omic constraints.

## When to use

After integrating transcriptomics-derived (RAS), metabolomics-derived (RPS), and extracellular flux constraints into cell-relative metabolic models, sample the feasible flux region when you need to: (1) visualize and compare the metabolic phenotype distributions across biological samples (e.g., via t-SNE embedding); (2) compute reaction-level concordance statistics across all flux solutions satisfying the constraints; or (3) assess the robustness of predicted flux patterns against the uncertainty inherent in constraint-based prediction.

## When NOT to use

- Input model lacks GPR associations or has incomplete constraint definitions (missing RAS values, medium bounds, or extracellular flux ratios) — incomplete constraints prevent meaningful exploration of the feasible space.
- Sampling goal is to identify a single optimal flux solution rather than characterize the distribution of feasible solutions — use flux balance analysis (FBA) or parsimonious FBA instead.
- Model is already in the reversible format or has not been converted to the irreversible representation required by optGpSampler.

## Inputs

- Irreversible metabolic model in SBML or .mat format with GPR associations (e.g., ENGRO2_MCF102A_irrev.xml)
- Type 1 constraints: nutrient availability bounds (medium.csv with columns Rxn, cellLine_LB, cellLine_UB)
- Type 2 constraints: extracellular flux ratio bounds (ysi_ratio.csv with columns Ratio, cellLine values across replicates)
- Type 3 constraints: RAS-scaled reaction flux bounds (ENGRO2_wNormalizedRAS.csv with normalized RAS scores per reaction and cell line)
- Biomass reaction identifier (e.g., 'Biomass')
- Sampling parameters: nSamples (integer ≥ 100,000), nBatches (integer ≥ 1), thinning factor (integer, typically 10)

## Outputs

- Feasible Flux Distribution (FFD) matrix: CSV file with dimensions nSamples × nReactions, filename pattern 'randomSampling_MODELID_nSol_NSAMPLES_CELLLINE_TIMESTAMP.csv'
- FFD rows represent individual flux solutions; columns are reaction IDs; values are flux magnitudes in mmol/gDW/h units
- One FFD file per cell line; suitable for downstream dimensionality reduction (e.g., t-SNE), statistical comparison (e.g., Mann-Whitney U), or concordance analysis

## How to apply

Convert each constrained, irreversible metabolic model to the required solver format (typically .mat for MATLAB or native COBRApy format), then apply the optGpSampler algorithm to uniformly sample from the feasible null space. Specify: number of samples (typically 1 million), thinning parameter (typically 10 to reduce autocorrelation), batch size (typically 100,000 for memory efficiency), and biomass lower bound (epsilon ≈ 1e-4 to enforce metabolically active states). The algorithm generates a matrix where rows are flux solutions and columns are reaction fluxes. Validate that the output dimensions match (n_samples × n_reactions) and that sampled solutions satisfy all constraint equations (substrate uptake ratios, RAS-scaled bounds, and medium nutrient limits) by spot-checking a subset against the original constraints.

## Related tools

- **optGpSampler** (Core algorithm for uniform sampling of the constrained null space; generates individual flux solutions from the feasible region defined by all Type 1, 2, and 3 constraints)
- **COBRApy** (Python interface for loading, manipulating, and validating constraint-based metabolic models; handles model format conversion and constraint application prior to sampling) — https://github.com/opencobra/cobrapy
- **GLPK** (Linear programming solver used by optGpSampler to solve sub-problems during null-space sampling) — https://www.gnu.org/software/glpk/
- **MATLAB (optional)** (Host environment for native optGpSampler implementation; models may require conversion to .mat format (Step 5 in README))

## Examples

```
python pipeline/randomSampling.py 1000000 10
```

## Evaluation signals

- FFD matrix shape is exactly (nSamples, nReactions); nSamples matches the requested sample count, and nReactions matches the irreversible model reaction count.
- All sampled flux values are finite (no NaN or infinite entries) and satisfy the sign constraints imposed by reaction reversibility (forward-only reactions ≥ 0).
- Spot-check: for a randomly selected flux solution, verify that extracellular flux ratios (lactate/glucose, lactate/glutamine, glutamate/glutamine) fall within the specified ysi_ratio bounds ± 1 standard deviation.
- Spot-check: for a randomly selected flux solution, verify that nutrient uptake rates respect the medium concentration bounds (Type 1 constraints) and that internal reaction bounds reflect the RAS-scaled limits (Type 3).
- Statistical comparison of FFD distributions across cell lines using Mann-Whitney U test (applied to per-reaction flux values) yields p-values and effect sizes consistent with known metabolic differences among the cell lines (e.g., higher lactate production in cancer lines).

## Limitations

- optGpSampler requires the model to be in irreversible format (forward and backward directions as separate reactions); reversible models must be pre-converted, adding computational overhead.
- Sampling is computationally intensive (1 million samples × 100,000 batch size = millions of LP solutions); runtime scales with model size and constraint complexity; may require hours on standard hardware.
- The uniform sampling assumes the constrained feasible region is well-connected; highly constrained models with disjoint feasible regions may yield biased or incomplete coverage.
- Sampling quality depends on thinning parameter and batch size; inappropriate choices can lead to autocorrelated samples or memory errors; the README recommends thinning=10 and batch_size=100,000 without adaptive tuning guidance.
- Reactions without complete metabolomics coverage (missing substrate abundances) or without GPR associations are omitted from downstream concordance analysis, reducing the scope of regulatory insights.

## Evidence

- [other] Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions (FFD) for all five cell lines.: "Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions (FFD)"
- [other] Apply Type 1 constraints: set upper bounds on exchange reactions proportionally to nutrient concentrations in growth medium for each cell line. Apply Type 2 constraints: constrain ratios of lactate-to-glucose, lactate-to-glutamine, and glutamate-to-glutamine fluxes based on YSI measurements with ±1 standard deviation bounds.: "Apply Type 1 constraints: set upper bounds on exchange reactions proportionally to nutrient concentrations; Type 2 constraints: constrain ratios with ±1 standard deviation bounds"
- [other] Apply Type 3 constraints: perform Flux Variability Analysis (FVA) on each cell-relative model to determine maximum and minimum flux capacity for each internal reaction, then scale flux boundaries proportionally to RAS values: "Apply Type 3 constraints: perform Flux Variability Analysis (FVA) to determine maximum and minimum flux capacity for each internal reaction, then scale flux boundaries proportionally to RAS values"
- [readme] File named 'randomSampling_' + modelId + '_nSol_' + str(nSamples) + '_' + cellLine + '_' + timeStamp + '.csv' containing the nSamples sampled solutions from each input sample model: "File named 'randomSampling_' + modelId + '_nSol_' + str(nSamples) + '_' + cellLine containing the nSamples sampled solutions"
- [readme] Each model needs to be converted to a mat file in order to exploit the MATLAB function to convert model from the reversible into the irreversible format: "Each model needs to be converted to a mat file in order to exploit the MATLAB function to convert model from the reversible into the irreversible format"
- [other] The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space: "The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space"
