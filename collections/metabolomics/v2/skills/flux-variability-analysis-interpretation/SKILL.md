---
name: flux-variability-analysis-interpretation
description: Use when when you have sampled the feasible flux solution space of constraint-based
  metabolic models (via optGpSampler or equivalent uniform sampling) and need to normalize
  flux predictions across reactions and cell lines for concordance analysis with transcriptomics
  and metabolomics data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - COBRApy (optGpSampler)
  - constraint-based stoichiometric metabolic models
  - randomSampling.py (INTEGRATE pipeline)
  - mannWhitneyUTest.py (INTEGRATE pipeline)
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
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

# flux-variability-analysis-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret flux variability analysis (FVA) results by scaling metabolic reaction fluxes relative to maximum flux values identified across constraint-based model solutions, enabling normalized comparison of flux ranges across reactions and conditions. This approach standardizes flux predictions for downstream regulatory classification and cross-sample integration.

## When to use

When you have sampled the feasible flux solution space of constraint-based metabolic models (via optGpSampler or equivalent uniform sampling) and need to normalize flux predictions across reactions and cell lines for concordance analysis with transcriptomics and metabolomics data. Apply this skill specifically when preparing flux fold-change signatures (FFD) for intersection with RAS and RPS variation signs to classify metabolic reactions into regulatory categories.

## When NOT to use

- Input flux solutions are not uniformly sampled or are single point predictions (e.g., FBA optima only); FVA interpretation requires distributional data, not single solutions.
- Reactions lack associated substrate metabolites in the metabolomics dataset; such reactions are omitted and cannot be classified by FFD.
- The goal is purely to identify reaction flux bounds without concordance analysis; standard FVA reporting (min/max per reaction) is sufficient and does not require normalization.

## Inputs

- constraint-based metabolic models (SBML or MAT format, one per cell line)
- uniform sampled flux solutions (from optGpSampler or randomSampling step)
- intracellular metabolomics dataset (CSV format with metabolite concentrations per cell line)
- metabolite-to-model ID conversion table

## Outputs

- normalized flux values (0–1 scale) per reaction per sample
- FFD dataset (log₂ fold-change ratios) with pairwise cell-line comparisons
- sign-of-variation table (±1, 0) for each reaction per comparison
- Mann–Whitney U test p-values for flux distribution differences

## How to apply

Execute flux variability analysis on each cell-line-specific metabolic model by sampling the feasible flux region (e.g., using optGpSampler with uniform sampling constraints). For each reaction, compute the maximum flux value across all sampled solutions and all conditions. Normalize individual flux measurements by dividing by this maximum to produce scaled flux values between 0 and 1. Calculate log₂ fold-change ratios of normalized fluxes between pairwise cell-line comparisons using Mann–Whitney U test (p<0.05) on the sampled distributions. The resulting FFD (flux fold-change differences) dataset, together with computed sign of variation (up +1, down −1, no-change 0), becomes the metabolic counterpart to RAS and RPS variation signs for Cohen's kappa concordance analysis. This normalization ensures flux ranges are comparable across reactions with intrinsically different magnitude ranges.

## Related tools

- **COBRApy (optGpSampler)** (Uniform sampling of feasible flux solution space to generate distributions for FVA) — https://github.com/opencobra/cobrapy
- **constraint-based stoichiometric metabolic models** (Scaffold for integrating transcriptomics and metabolomics; used to predict metabolic flux distributions)
- **randomSampling.py (INTEGRATE pipeline)** (Samples the feasible flux region of each cell-relative model using COBRApy) — https://github.com/qLSLab/integrate
- **mannWhitneyUTest.py (INTEGRATE pipeline)** (Computes statistical differences between sampled flux distributions across pairwise cell-line comparisons) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/mannWhitneyUTest.py 5000 10 --lcellLines MCF102A SKBR3 MCF7 MDAMB231 MDAMB361 --modelId ENGRO2
```

## Evaluation signals

- Normalized flux values are bounded within [0, 1] for all reactions; any value outside this range indicates incorrect maximum-flux normalization.
- FFD log₂ fold-change ratios are symmetric around zero when compared between reciprocal cell-line pairs (e.g., cell_A vs cell_B and cell_B vs cell_A); absence of symmetry suggests directional error.
- Sign-of-variation table contains only {-1, 0, +1} entries; presence of other values indicates incorrect thresholding or sign computation.
- Mann–Whitney U test p-values are in [0, 1]; outliers or NaN values flag reactions with insufficient or malformed flux samples.
- Reactions with statistically significant FFD variation (p<0.05) show non-zero log₂ fold-change; reactions with p-values >0.05 should have fold-change ratios close to 0.

## Limitations

- If a single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the FFD dataset and cannot participate in concordance analysis.
- Direct determination of metabolic fluxes through labeled substrates lags behind other omic technologies and is not integrated; FVA predictions are computational estimates constrained by metabolomics and transcriptomics, not direct measurements.
- Reactions without gene-protein-reaction (GPR) associations cannot be classified via RAS-RPS-FFD concordance because RAS scores require enzyme expression data.
- FVA interpretation assumes the constraint-based model is correctly curated and that steady-state assumptions hold; model gaps or incorrect GPR annotations propagate into flux predictions.

## Evidence

- [intro] We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in GX-FBA: "We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in GX-FBA [26]"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [other] Compute the sign of FFD variation for each pair using Mann–Whitney U test on sampled flux distributions with log₂ fold-change ratio: "Compute the sign of FFD variation for each pair using Mann–Whitney U test on sampled flux distributions with log₂ fold-change ratio."
- [other] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [readme] randomSampling.py step samples the feasible flux region of each cell relative model: "sample the feasible flux region of each cell relative model"
